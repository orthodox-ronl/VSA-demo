"""Eenmalige 4-kwartsproef voor 20d-in-waarheid-moeder-godslied.

Opmaat van 1 kwart (In), daarna 4/4. Geen zichtbare maatsoort, geen
lyric-underlines. Het origineel blijft staan.

Niet in check. Roept daarna apply_mscz_layout aan (zonder extenders).
"""
from __future__ import annotations

import io
import re
import sys
import zipfile
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_mscz_layout import musescore_convert, process_mscz

REPO = Path(__file__).resolve().parents[1]
SRC = (
    REPO
    / "content-source"
    / "praktijk"
    / "oefenhoek"
    / "20d-in-waarheid-moeder-godslied"
    / "20d-in-waarheid-moeder-godslied.mscz"
)
DEST = SRC.with_name("20d-in-waarheid-moeder-godslied-4kwart.mscz")

MEASURE_RE = re.compile(r"<Measure\b[^>]*>.*?</Measure>", re.S)
STAFF_RE = re.compile(r'(<Staff id="(\d+)">)(.*?)(</Staff>)', re.S)
VOICE_RE = re.compile(r"<voice>.*?</voice>", re.S)
CR_RE = re.compile(r"<(Chord|Rest)\b.*?</\1>", re.S)
TOKEN_RE = re.compile(
    r"(<(Chord|Rest)\b.*?</\2>|<Fermata>.*?</Fermata>)",
    re.S,
)
TIE_RE = re.compile(r"\s*<Spanner type=\"Tie\">.*?</Spanner>", re.S)
SLUR_RE = re.compile(r"\s*<Spanner type=\"Slur\">.*?</Spanner>", re.S)
ACC_RE = re.compile(r"\s*<Accidental>.*?</Accidental>", re.S)
LYRICS_RE = re.compile(r"\s*<Lyrics>.*?</Lyrics>", re.S)
DUR_MAP = {
    "long": Fraction(16),
    "breve": Fraction(8),
    "whole": Fraction(4),
    "half": Fraction(2),
    "quarter": Fraction(1),
    "eighth": Fraction(1, 2),
    "16th": Fraction(1, 4),
    "32nd": Fraction(1, 8),
}
NOTE_VALUES = [
    (Fraction(4), "whole", 0),
    (Fraction(3), "half", 1),
    (Fraction(2), "half", 0),
    (Fraction(3, 2), "quarter", 1),
    (Fraction(1), "quarter", 0),
    (Fraction(3, 4), "eighth", 1),
    (Fraction(1, 2), "eighth", 0),
    (Fraction(1, 4), "16th", 0),
]
FIRST_BAR = Fraction(1)
THEREAFTER = Fraction(4)

EXTRA_STYLE = {
    "minNoteDistance": "1.1",
    "minMeasureWidth": "13",
    "lyricsMinDistance": "0.55",
    "lyricsDashForce": "1",
    "lyricsDashMinLength": "0.5",
    "lyricsDashMaxLength": "0.8",
    "measureSpacing": "1.7",
    "genCourtesyTimesig": "0",
    "minSystemDistance": "6.5",
    "maxSystemDistance": "9",
}

LAYOUT_EVERY = 4


def _set_syllabic(xml: str, syll: str) -> str:
    if "<syllabic>" in xml:
        return re.sub(
            r"<syllabic>.*?</syllabic>",
            f"<syllabic>{syll}</syllabic>",
            xml,
            count=1,
        )
    return xml.replace(
        "<Lyrics>",
        f"<Lyrics>\n              <syllabic>{syll}</syllabic>",
        1,
    )


def _fix_prijzen(events: list[dict]) -> None:
    prev_i = None
    prev_word = None
    for i, ev in enumerate(events):
        if ev["kind"] != "chord":
            continue
        tm = re.search(r"<Lyrics>.*?<text>(.*?)</text>", ev["xml"], re.S)
        if tm is None:
            continue
        word = tm.group(1)
        if prev_word == "prij" and word.startswith("zen"):
            events[prev_i]["xml"] = _set_syllabic(events[prev_i]["xml"], "begin")
            ev["xml"] = _set_syllabic(ev["xml"], "end")
        prev_i, prev_word = i, word


def _dur_quarters(xml: str) -> Fraction:
    dt = re.search(r"<durationType>(.*?)</durationType>", xml)
    if dt is None:
        raise ValueError("geen durationType")
    base = DUR_MAP[dt.group(1)]
    dm = re.search(r"<dots>(\d+)</dots>", xml)
    dots = int(dm.group(1)) if dm else 0
    extra = base
    total = base
    for _ in range(dots):
        extra /= 2
        total += extra
    return total


def _encode(q: Fraction) -> tuple[str, int]:
    for val, name, dots in NOTE_VALUES:
        if val == q:
            return name, dots
    raise ValueError(f"geen nootwaarde voor {q} kwarten")


def _set_dur(xml: str, q: Fraction) -> str:
    name, dots = _encode(q)
    xml = re.sub(r"\s*<dots>.*?</dots>", "", xml)
    xml = re.sub(
        r"<durationType>.*?</durationType>",
        f"<durationType>{name}</durationType>",
        xml,
        count=1,
    )
    if dots:
        xml = xml.replace(
            f"<durationType>{name}</durationType>",
            f"<dots>{dots}</dots>\n            <durationType>{name}</durationType>",
            1,
        )
    return xml


def _frac_wholes(q: Fraction) -> str:
    w = q / 4
    return f"{w.numerator}/{w.denominator}"


def _tie_next(q: Fraction) -> str:
    return (
        "\n                <Spanner type=\"Tie\">\n"
        "                  <Tie>\n                    </Tie>\n"
        "                  <next>\n                    <location>\n"
        f"                      <fractions>{_frac_wholes(q)}</fractions>\n"
        "                      </location>\n                    </next>\n"
        "                  </Spanner>"
    )


def _tie_prev(q: Fraction) -> str:
    w = q / 4
    return (
        "\n                <Spanner type=\"Tie\">\n"
        "                  <prev>\n                    <location>\n"
        f"                      <fractions>-{w.numerator}/{w.denominator}</fractions>\n"
        "                      </location>\n                    </prev>\n"
        "                  </Spanner>"
    )


def _inject_note_spanner(xml: str, blob: str) -> str:
    def add(m: re.Match[str]) -> str:
        note = m.group(0)
        if "<Spanner type=\"Tie\">" in note:
            return note
        if "<eid>" in note:
            return re.sub(r"(</eid>)", r"\1" + blob, note, count=1)
        return note.replace("<Note>", "<Note>" + blob, 1)

    return re.sub(r"<Note>.*?</Note>", add, xml, flags=re.S)


def _strip_ties(xml: str) -> str:
    return TIE_RE.sub("", xml)


def _continuation(xml: str) -> str:
    xml = _strip_ties(xml)
    xml = SLUR_RE.sub("", xml)
    xml = LYRICS_RE.sub("", xml)
    xml = ACC_RE.sub("", xml)
    return xml


def _bar_ends(total: Fraction) -> list[Fraction]:
    ends = [FIRST_BAR]
    t = FIRST_BAR
    while t < total:
        t += THEREAFTER
        ends.append(min(t, total))
    return ends


def _hide_timesig(mscx: str) -> str:
    mscx = re.sub(r"\s*<TimeSig>.*?</TimeSig>", "", mscx, flags=re.S)

    def stafftype(m: re.Match[str]) -> str:
        block = m.group(0)
        if "<genTimesig>" in block:
            block = re.sub(
                r"<genTimesig>.*?</genTimesig>",
                "<genTimesig>0</genTimesig>",
                block,
            )
        else:
            block = block.replace(
                "</StaffType>",
                "          <genTimesig>0</genTimesig>\n          </StaffType>",
                1,
            )
        return block

    return re.sub(r"<StaffType\b.*?</StaffType>", stafftype, mscx, flags=re.S)


def _parse_voice(voice_xml: str) -> tuple[str, list[dict]]:
    inner = voice_xml[len("<voice>") : -len("</voice>")]
    events: list[dict] = []
    pending_fermata = ""
    first_cr = None
    for tok in TOKEN_RE.finditer(inner):
        block = tok.group(0)
        if block.startswith("<Fermata"):
            pending_fermata += block
            continue
        kind = "rest" if block.startswith("<Rest") else "chord"
        if first_cr is None:
            first_cr = tok.start()
        has_tie_next = bool(
            re.search(
                r'<Spanner type="Tie">(?:(?!</Spanner>).)*<next>',
                block,
                re.S,
            )
        )
        events.append(
            {
                "kind": kind,
                "xml": block,
                "dur": _dur_quarters(block),
                "fermata": pending_fermata,
                "tie_next": has_tie_next,
            }
        )
        pending_fermata = ""
    prefix = inner[:first_cr] if first_cr is not None else inner
    prefix = re.sub(r"<BarLine>.*?</BarLine>", "", prefix, flags=re.S)
    prefix = re.sub(r"<LayoutBreak>.*?</LayoutBreak>", "", prefix, flags=re.S)
    return prefix.strip(), events


def _flatten_staff(staff_body: str) -> tuple[list[str], list[list[dict]], Fraction]:
    measures = MEASURE_RE.findall(staff_body)
    nvoices = max(len(VOICE_RE.findall(m)) for m in measures)
    prefixes = [""] * nvoices
    streams: list[list[dict]] = [[] for _ in range(nvoices)]
    for mi, meas in enumerate(measures):
        voices = VOICE_RE.findall(meas)
        for vi, vxml in enumerate(voices):
            pref, evs = _parse_voice(vxml)
            if mi == 0:
                prefixes[vi] = pref
            streams[vi].extend(evs)
    totals = [sum((e["dur"] for e in s), Fraction(0)) for s in streams]
    if len(set(totals)) != 1:
        raise SystemExit(f"ongelijke stemduren: {totals}")
    return prefixes, streams, totals[0]


def _split_event(ev: dict, pieces: list[Fraction]) -> list[dict]:
    out = []
    for i, pq in enumerate(pieces):
        xml = ev["xml"] if i == 0 else _continuation(ev["xml"])
        xml = _strip_ties(xml)
        xml = _set_dur(xml, pq)
        out.append(
            {
                "kind": ev["kind"],
                "xml": xml,
                "dur": pq,
                "fermata": ev["fermata"] if i == 0 else "",
                "tie_to_next_piece": i < len(pieces) - 1 and ev["kind"] == "chord",
                "orig_tie_next": bool(ev["tie_next"] and i == len(pieces) - 1),
            }
        )
    return out


def _bar_index(t: Fraction, ends: list[Fraction]) -> int:
    for i, end in enumerate(ends):
        prev = ends[i - 1] if i else Fraction(0)
        if prev <= t < end:
            return i
    raise ValueError(f"tijd {t} past in geen maat {ends}")


def _cut_stream(events: list[dict], ends: list[Fraction]) -> list[list[dict]]:
    bars: list[list[dict]] = [[] for _ in ends]
    t = Fraction(0)
    for ev in events:
        start = t
        end = t + ev["dur"]
        cuts = [c for c in ends if start < c < end]
        if cuts:
            pts = [start, *cuts, end]
            piece_durs = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
        else:
            piece_durs = [ev["dur"]]
        parts = _split_event(ev, piece_durs)
        cursor = start
        for part in parts:
            bars[_bar_index(cursor, ends)].append(part)
            cursor += part["dur"]
        t = end
    return bars


def _apply_ties(bars: list[list[dict]]) -> None:
    flat = [p for bar in bars for p in bar]
    for i, p in enumerate(flat):
        if p["kind"] != "chord":
            continue
        if p.get("tie_to_next_piece"):
            p["xml"] = _inject_note_spanner(p["xml"], _tie_next(p["dur"]))
            nxt = flat[i + 1]
            nxt["xml"] = _inject_note_spanner(nxt["xml"], _tie_prev(p["dur"]))
        elif p.get("orig_tie_next"):
            p["xml"] = _inject_note_spanner(p["xml"], _tie_next(p["dur"]))
            for j in range(i + 1, len(flat)):
                if flat[j]["kind"] == "chord":
                    flat[j]["xml"] = _inject_note_spanner(
                        flat[j]["xml"], _tie_prev(p["dur"])
                    )
                    break


def _voice_xml(prefix: str, parts: list[dict], extra_head: str = "") -> str:
    chunks = ["        <voice>\n"]
    if extra_head:
        chunks.append(extra_head)
    if prefix:
        chunks.append(prefix)
        if not prefix.endswith("\n"):
            chunks.append("\n")
    for p in parts:
        if p["fermata"]:
            chunks.append(p["fermata"])
            if not p["fermata"].endswith("\n"):
                chunks.append("\n")
        chunks.append(p["xml"])
        if not p["xml"].endswith("\n"):
            chunks.append("\n")
    chunks.append("          </voice>\n")
    return "".join(chunks)


def _rebuild_staff(
    prefixes: list[str],
    streams: list[list[dict]],
    ends: list[Fraction],
    *,
    add_breaks: bool,
) -> str:
    per_voice_bars = [_cut_stream(s, ends) for s in streams]
    for vb in per_voice_bars:
        _apply_ties(vb)
    nbar = len(ends)
    lens = []
    prev = Fraction(0)
    for e in ends:
        lens.append(e - prev)
        prev = e
    out = []
    for bi in range(nbar):
        ln = lens[bi]
        w = ln / 4
        extra_m = ""
        if bi == 0:
            extra_m += "        <irregular>1</irregular>\n"
        if (
            add_breaks
            and (bi + 1) % LAYOUT_EVERY == 0
            and (nbar - (bi + 1)) > 1
        ):
            extra_m += (
                "        <LayoutBreak>\n"
                "          <subtype>line</subtype>\n"
                "          </LayoutBreak>\n"
            )
        out.append(
            f'      <Measure len="{w.numerator}/{w.denominator}">\n{extra_m}'
        )
        for vi, prefixes_i in enumerate(prefixes):
            pref = prefixes_i if bi == 0 else ""
            out.append(_voice_xml(pref, per_voice_bars[vi][bi]))
        out.append("        </Measure>\n")
    return "".join(out)


def _rebar_mscx(mscx: str) -> str:
    staff_data = {}
    total = None
    for m in STAFF_RE.finditer(mscx):
        sid = m.group(2)
        if sid not in ("1", "2"):
            continue
        body = m.group(3)
        if "<Measure" not in body:
            continue
        prefixes, streams, tot = _flatten_staff(body)
        for stream in streams:
            _fix_prijzen(stream)
        staff_data[sid] = (prefixes, streams, tot)
        if total is None:
            total = tot
        elif tot != total:
            raise SystemExit(f"staff {sid} duur {tot} != {total}")
    assert total is not None
    ends = _bar_ends(total)
    print(f"totaal {total} kwarten -> opmaat {FIRST_BAR} + {len(ends) - 1}x 4/4")

    def repl(m: re.Match[str]) -> str:
        sid = m.group(2)
        body = m.group(3)
        if sid not in staff_data or "<Measure" not in body:
            return m.group(0)
        prefixes, streams, _tot = staff_data[sid]
        vbox = ""
        vm = re.search(r"<VBox>.*?</VBox>", body, re.S)
        if vm:
            vbox = vm.group(0) + "\n"
        new_measures = _rebuild_staff(
            prefixes, streams, ends, add_breaks=(sid == "1")
        )
        return m.group(1) + "\n" + vbox + new_measures + m.group(4)

    return STAFF_RE.sub(repl, mscx)


def main() -> int:
    if not SRC.is_file():
        raise SystemExit(f"niet gevonden: {SRC}")
    with zipfile.ZipFile(SRC) as zin:
        names = zin.namelist()
        mscx_name = next(n for n in names if n.endswith(".mscx") and "/" not in n)
        mscx = zin.read(mscx_name).decode("utf-8")
        others = {n: zin.read(n) for n in names if n != mscx_name}
    new_mscx = _hide_timesig(_rebar_mscx(mscx))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        zout.writestr(
            "20d-in-waarheid-moeder-godslied-4kwart.mscx",
            new_mscx.encode("utf-8"),
        )
        for n, data in others.items():
            if n.endswith(".mscx"):
                continue
            zout.writestr(n, data)
    DEST.write_bytes(buf.getvalue())
    process_mscz(DEST, extra_style=EXTRA_STYLE, no_extenders=True)
    tmp_in = DEST.with_name("_in_20d_4kwart.mscz")
    tmp_in.write_bytes(DEST.read_bytes())
    musescore_convert(tmp_in, DEST)
    tmp_in.unlink(missing_ok=True)
    with zipfile.ZipFile(DEST, "r") as zin:
        names = zin.namelist()
        mscx_name = next(n for n in names if n.endswith(".mscx"))
        packed = {n: zin.read(n) for n in names}
    packed[mscx_name] = _hide_timesig(packed[mscx_name].decode("utf-8")).encode(
        "utf-8"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for n, data in packed.items():
            zout.writestr(n, data)
    DEST.write_bytes(buf.getvalue())
    notes = process_mscz(DEST, extra_style=EXTRA_STYLE, no_extenders=True)
    print(f"ok {DEST}")
    for n in notes:
        print(f"  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
