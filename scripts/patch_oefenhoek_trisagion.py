"""Eenmalige inhoudelijke patch op de twee trisagion-.mscz (oefenhoek).

- 8a-trisagion: herhaling m1-m4 (start/end repeat + sectiebreuk, geen
  systeembreuk die het blok uitsmeert).
- Beide: maten met 'Hei-li-ge God,' krijgen de noten van Slavische maat 5
  en lyrics 'O Hei-li-ge God,'. Op *God* een melisma: huidige akkoord 3
  tellen + A/F/C/F 3 tellen.
- Slavische lyrics: hoofd-/kleine letter (zoals NL); transliteratie 2e couplet.

Niet in check. Daarna: apply_mscz_layout.py op dezelfde .mscz.
"""
from __future__ import annotations

import base64
import os
import re
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OEF = REPO / "content-source" / "praktijk" / "oefenhoek"
NL = OEF / "liturgiemap-hemelum" / "8a-trisagion" / "8a-trisagion.mscz"
SLAV = OEF / "liturgiemap-hemelum" / "8a-trisagion-slav" / "8a-trisagion-slav.mscz"

MEASURE_RE = re.compile(r"<Measure\b[^>]*>.*?</Measure>", re.S)
STAFF_RE = re.compile(r"(<Staff id=\"(\d+)\">)(.*?)(</Staff>)", re.S)

# Soprano-noten van Slavische m5: 6 akkoorden, 1 doorgangsnoot.
O_HEILIGE_GOD = [
    ("single", "O"),
    ("begin", "Hei"),
    ("middle", "li"),
    ("end", "ge"),
    None,
    ("single", "God,"),
]

TRANSLIT = {
    "СВЯ": "Svja",
    "Свя": "Svja",
    "ТЫЙ": "tyj",
    "тый": "tyj",
    "БО": "Bo",
    "Бо": "Bo",
    "ЖЕ,": "že,",
    "же,": "že,",
    "КРЕП": "Krep",
    "Креп": "Krep",
    "КЫЙ,": "kyj,",
    "кый,": "kyj,",
    "БЕЗ": "Bez",
    "Без": "Bez",
    "СМЕРТ": "smert",
    "смерт": "smert",
    "НЫЙ": "nyj",
    "ный": "nyj",
    "ПО": "Po",
    "По": "Po",
    "МИ": "mi",
    "ми": "mi",
    "ЛУЙ": "luj",
    "луй": "luj",
    "НАС.": "nas.",
    "нас.": "nas.",
}

CYRILLIC_CASE = {
    "СВЯ": "Свя",
    "ТЫЙ": "тый",
    "БО": "Бо",
    "ЖЕ,": "же,",
    "КРЕП": "Креп",
    "КЫЙ,": "кый,",
    "БЕЗ": "Без",
    "СМЕРТ": "смерт",
    "НЫЙ": "ный",
    "ПО": "По",
    "МИ": "ми",
    "ЛУЙ": "луй",
    "НАС.": "нас.",
}

# staff_id, voice-index -> (pitch, tpc, accidental or None)
GOD_MELISMA_SECOND = {
    ("1", 0): (69, 17, None),
    ("1", 1): (65, 13, "accidentalNatural"),
    ("2", 0): (60, 14, None),
    ("2", 1): (53, 13, "accidentalNatural"),
}


def new_eid() -> str:
    return base64.urlsafe_b64encode(os.urandom(16)).decode("ascii").rstrip("=")[:22]


def retag_eids(xml: str) -> str:
    return re.sub(r"<eid>.*?</eid>", lambda _m: f"<eid>{new_eid()}</eid>", xml)


def top_level(xml: str) -> list[str]:
    elems: list[str] = []
    i, n = 0, len(xml)
    while i < n:
        while i < n and xml[i].isspace():
            i += 1
        if i >= n or xml.startswith("</", i):
            break
        m = re.match(r"<([A-Za-z]+)\b", xml[i:])
        if not m:
            break
        name = m.group(1)
        mm = re.match(rf"<{name}\b[^>]*/>|<{name}\b.*?</{name}>", xml[i:], re.S)
        if not mm:
            raise ValueError(f"kan element {name} niet parsen")
        elems.append(mm.group(0))
        i += mm.end()
    return elems


def split_header_music(voice_inner: str) -> tuple[list[str], list[str]]:
    elems = top_level(voice_inner)
    idx = next(
        (i for i, e in enumerate(elems) if e.startswith(("<Chord", "<Rest"))),
        len(elems),
    )
    return elems[:idx], elems[idx:]


def set_measure_len(meas: str, frac: str) -> str:
    return re.sub(r"<Measure\b[^>]*>", f'<Measure len="{frac}">', meas, count=1)


def voices(meas: str) -> list[str]:
    return re.findall(r"<voice>(.*?)</voice>", meas, re.S)


def rebuild_measure(meas: str, new_voices: list[str]) -> str:
    out = meas
    for old, new in zip(voices(meas), new_voices, strict=True):
        out = out.replace(
            f"<voice>{old}</voice>",
            f"<voice>\n{new}\n          </voice>",
            1,
        )
    return out


def strip_lyrics(chord: str) -> str:
    return re.sub(r"\s*<Lyrics>.*?</Lyrics>", "", chord, flags=re.S)


def add_lyric(chord: str, syllabic: str, text: str, verse: int = 0) -> str:
    no = f"\n              <no>{verse}</no>" if verse else ""
    block = (
        "\n            <Lyrics>"
        f"{no}\n              <syllabic>{syllabic}</syllabic>"
        f"\n              <eid>{new_eid()}</eid>"
        f"\n              <text>{text}</text>"
        "\n              </Lyrics>"
    )
    return chord.replace("<Note>", block + "\n            <Note>", 1)


def apply_o_heilige(music: list[str]) -> list[str]:
    chords = [i for i, e in enumerate(music) if e.startswith("<Chord")]
    if len(chords) != len(O_HEILIGE_GOD):
        raise SystemExit(
            f"verwacht {len(O_HEILIGE_GOD)} sopraan-akkoorden, kreeg {len(chords)}"
        )
    out = list(music)
    for idx, spec in zip(chords, O_HEILIGE_GOD):
        ch = strip_lyrics(out[idx])
        if spec is not None:
            ch = add_lyric(ch, spec[0], spec[1], verse=0)
        out[idx] = ch
    return out


def copy_music_from(src_meas: str, dest_meas: str, *, lyrics: bool) -> str:
    src_vs = voices(src_meas)
    dest_vs = voices(dest_meas)
    if len(src_vs) != len(dest_vs):
        raise SystemExit("ongelijk aantal stemmen")
    new_vs: list[str] = []
    for vi, (sv, dv) in enumerate(zip(src_vs, dest_vs)):
        d_head, _d_music = split_header_music(dv)
        _s_head, s_music = split_header_music(sv)
        music = [retag_eids(e) for e in s_music]
        if lyrics and vi == 0:
            music = apply_o_heilige(music)
        else:
            music = [strip_lyrics(e) if e.startswith("<Chord") else e for e in music]
        inner = "\n".join(d_head + music)
        new_vs.append(inner)
    meas = rebuild_measure(dest_meas, new_vs)
    return set_measure_len(meas, "9/4")


def staff_measures(data: str, staff_id: str) -> list[str]:
    for m in STAFF_RE.finditer(data):
        if m.group(2) == staff_id:
            return [x.group(0) for x in MEASURE_RE.finditer(m.group(3))]
    raise SystemExit(f"geen staff {staff_id}")


def replace_staff_measures(data: str, staff_id: str, new: list[str]) -> str:
    def repl(m: re.Match[str]) -> str:
        if m.group(2) != staff_id:
            return m.group(0)
        body = m.group(3)
        it = iter(new)
        body2 = MEASURE_RE.sub(lambda _mm: next(it), body)
        return m.group(1) + body2 + m.group(4)

    return STAFF_RE.sub(repl, data)


def is_heilige_god(meas: str) -> bool:
    texts = re.findall(r"<text>(.*?)</text>", meas)
    joined = " ".join(texts)
    return bool(re.search(r"Hei\s+li\s+ge\s+God", joined)) and "O " not in joined


def insert_after_measure_open(meas: str, snippet: str) -> str:
    return re.sub(
        r"<Measure\b[^>]*>",
        lambda m: m.group(0) + snippet,
        meas,
        count=1,
    )


def ensure_repeat_nl(data: str) -> str:
    for sid in ("1", "2"):
        ms = staff_measures(data, sid)
        m1, m4 = ms[0], ms[3]
        if "<startRepeat" not in m1:
            m1 = insert_after_measure_open(m1, "\n        <startRepeat/>")
        if "<endRepeat" not in m4:
            m4 = insert_after_measure_open(m4, "\n        <endRepeat>2</endRepeat>")
        if sid == "1":
            if "<LayoutBreak>" in m4 and "<subtype>line</subtype>" in m4:
                m4 = m4.replace(
                    "<subtype>line</subtype>",
                    "<subtype>section</subtype>",
                    1,
                )
            elif "<LayoutBreak>" not in m4:
                m4 = insert_after_measure_open(
                    m4,
                    "\n        <LayoutBreak>\n          "
                    f"<eid>{new_eid()}</eid>\n          "
                    "<subtype>section</subtype>\n          </LayoutBreak>",
                )
        ms[0], ms[3] = m1, m4
        data = replace_staff_measures(data, sid, ms)
    return data


def _set_pitch(chord: str, pitch: int, tpc: int, acc: str | None) -> str:
    chord = re.sub(r"<pitch>\d+</pitch>", f"<pitch>{pitch}</pitch>", chord, count=1)
    chord = re.sub(r"<tpc>-?\d+</tpc>", f"<tpc>{tpc}</tpc>", chord, count=1)
    chord = re.sub(r"\s*<Accidental>.*?</Accidental>", "", chord, flags=re.S)
    if acc:
        acc_xml = (
            "\n              <Accidental>\n                "
            f"<subtype>{acc}</subtype>\n                "
            f"<eid>{new_eid()}</eid>\n                </Accidental>"
        )
        chord = chord.replace("<pitch>", acc_xml + "\n              <pitch>", 1)
    return chord


def _make_dotted_half(chord: str) -> str:
    chord = re.sub(r"\s*<dots>\d+</dots>", "", chord)
    chord = re.sub(
        r"<durationType>.*?</durationType>",
        "<durationType>half</durationType>",
        chord,
        count=1,
    )
    if not re.search(r"<dots>\d+</dots>", chord):
        chord = re.sub(
            r"(<durationType>)",
            r"<dots>1</dots>\n            \1",
            chord,
            count=1,
        )
    return chord


def _slur_start(chord: str, direction: str = "up") -> str:
    if '<Spanner type="Slur">' in chord:
        if "<up>" in chord:
            return re.sub(r"<up>.*?</up>", f"<up>{direction}</up>", chord)
        return chord
    block = (
        '\n            <Spanner type="Slur">\n              <Slur>\n                '
        f"<eid>{new_eid()}</eid>\n                <up>{direction}</up>\n                "
        "</Slur>\n              <next>\n                <location>\n                  "
        "<fractions>3/4</fractions>\n                  </location>\n                "
        "</next>\n              </Spanner>"
    )
    return chord.replace("<Note>", block + "\n            <Note>", 1)


def _slur_stop(chord: str) -> str:
    block = (
        '\n            <Spanner type="Slur">\n              <prev>\n                '
        "<location>\n                  <fractions>-3/4</fractions>\n                  "
        "</location>\n                </prev>\n              </Spanner>"
    )
    return chord.replace("<Note>", block + "\n            <Note>", 1)


def _extend_god_voice(music: list[str], staff_id: str, vi: int) -> list[str]:
    chords = [i for i, e in enumerate(music) if e.startswith("<Chord")]
    if not chords:
        return music
    direction = "down" if vi == 1 else "up"
    last_i = chords[-1]
    last = music[last_i]
    pit = re.search(r"<pitch>(\d+)</pitch>", last)
    want = GOD_MELISMA_SECOND[(staff_id, vi)]
    out = list(music)
    if pit is not None and pit.group(1) == str(want[0]) and len(chords) >= 2:
        god_i = chords[-2]
        out[god_i] = _slur_start(_make_dotted_half(out[god_i]), direction)
        extra = _make_dotted_half(out[last_i])
        extra = re.sub(r"\s*<up>up</up>", "<up>down</up>", extra) if vi == 1 else extra
        out[last_i] = extra
        return out
    last = _make_dotted_half(last)
    last = _slur_start(last, direction)
    extra = retag_eids(strip_lyrics(last))
    extra = _set_pitch(extra, want[0], want[1], want[2])
    extra = re.sub(r'\s*<Spanner type="Slur">.*?</Spanner>', "", extra, flags=re.S)
    extra = _slur_stop(extra)
    extra = _make_dotted_half(extra)
    out[last_i] = last
    out.insert(last_i + 1, extra)
    return out


def is_o_heilige_god(meas: str) -> bool:
    texts = re.findall(r"<text>(.*?)</text>", meas)
    joined = " ".join(texts)
    return "O" in texts and bool(re.search(r"God", joined))


def extend_god_melisma(data: str) -> str:
    s1 = staff_measures(data, "1")
    idxs = [i for i, meas in enumerate(s1) if is_o_heilige_god(meas)]
    for sid in ("1", "2"):
        ms = staff_measures(data, sid)
        for i in idxs:
            vs = voices(ms[i])
            new_vs: list[str] = []
            for vi, inner in enumerate(vs):
                head, music = split_header_music(inner)
                music = _extend_god_voice(music, sid, vi)
                new_vs.append("\n".join(head + music))
            meas = rebuild_measure(ms[i], new_vs)
            if "<irregular>" not in meas:
                meas = insert_after_measure_open(
                    meas, "\n        <irregular>1</irregular>"
                )
            ms[i] = set_measure_len(meas, "13/4")
            print(f"  staff {sid} maat {i + 1}: God-melisma 3+3 (A/F/C/F)")
        data = replace_staff_measures(data, sid, ms)
    return data


def cyrillic_mixed_case(meas: str) -> str:
    def fix_ly(ly: str) -> str:
        if "<no>" in ly:
            return ly
        t = re.search(r"<text>(.*?)</text>", ly)
        if t is None or t.group(1) not in CYRILLIC_CASE:
            return ly
        return ly[: t.start(1)] + CYRILLIC_CASE[t.group(1)] + ly[t.end(1) :]

    return re.sub(
        r"<Lyrics>.*?</Lyrics>", lambda m: fix_ly(m.group(0)), meas, flags=re.S
    )


def add_transliteration(meas: str) -> str:
    if "<no>1</no>" in meas:
        return meas
    def add_verse2(ly: str) -> str:
        if "<no>" in ly:
            return ly
        t = re.search(r"<text>(.*?)</text>", ly)
        if t is None:
            return ly
        raw = t.group(1)
        if raw not in TRANSLIT:
            return ly
        syll = re.search(r"<syllabic>(.*?)</syllabic>", ly)
        syllabic = syll.group(1) if syll else "single"
        extra = (
            "\n            <Lyrics>\n              <no>1</no>\n              "
            f"<syllabic>{syllabic}</syllabic>\n              "
            f"<eid>{new_eid()}</eid>\n              "
            f"<text>{TRANSLIT[raw]}</text>\n              </Lyrics>"
        )
        return ly + extra

    return re.sub(r"<Lyrics>.*?</Lyrics>", lambda m: add_verse2(m.group(0)), meas, flags=re.S)


def load_mscz(path: Path) -> tuple[str, bytes, dict[str, bytes]]:
    extras: dict[str, bytes] = {}
    mscx_name = None
    mscx = None
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            data = z.read(name)
            if name.endswith(".mscx"):
                mscx_name = name
                mscx = data.decode("utf-8")
            else:
                extras[name] = data
    if mscx_name is None or mscx is None:
        raise SystemExit(f"geen mscx in {path}")
    return mscx_name, mscx, extras


def write_mscz(path: Path, mscx_name: str, mscx: str, extras: dict[str, bytes]) -> None:
    buf = __import__("io").BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(mscx_name, mscx.encode("utf-8"))
        for name, data in extras.items():
            z.writestr(name, data)
    path.write_bytes(buf.getvalue())


def patch_heilige_god(data: str, donor_s1: str, donor_s2: str) -> str:
    s1 = staff_measures(data, "1")
    idxs = [i for i, meas in enumerate(s1) if is_heilige_god(meas)]
    if not idxs:
        return data
    donors = {"1": donor_s1, "2": donor_s2}
    for sid in ("1", "2"):
        ms = staff_measures(data, sid)
        donor = donors[sid]
        for i in idxs:
            ms[i] = copy_music_from(donor, ms[i], lyrics=(sid == "1"))
            print(f"  staff {sid} maat {i + 1}: O Heilige God (noten uit Slavisch m5)")
        data = replace_staff_measures(data, sid, ms)
    return data


def main() -> int:
    slav_name, slav, slav_ex = load_mscz(SLAV)
    donor_s1 = staff_measures(slav, "1")[4]
    donor_s2 = staff_measures(slav, "2")[4]

    print("==", NL.name)
    nl_name, nl, nl_ex = load_mscz(NL)
    nl = patch_heilige_god(nl, donor_s1, donor_s2)
    nl = extend_god_melisma(nl)
    nl = ensure_repeat_nl(nl)
    write_mscz(NL, nl_name, nl, nl_ex)

    print("==", SLAV.name)
    slav = patch_heilige_god(slav, donor_s1, donor_s2)
    slav = extend_god_melisma(slav)
    s1 = staff_measures(slav, "1")
    for i, meas in enumerate(s1):
        new = cyrillic_mixed_case(meas)
        if new != meas:
            print(f"  staff 1 maat {i + 1}: Cyrillisch hoofd-/kleine letter")
        s1[i] = add_transliteration(new)
    slav = replace_staff_measures(slav, "1", s1)
    write_mscz(SLAV, slav_name, slav, slav_ex)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
