"""Reciteertoon-collaps in MuseScore MSCX (hub-encoding ||O||).

MCI / hub-afspraak 1-n-1:
  Eerst een rij zoeken van opeenvolgende noten met **zelfde toonhoogte** én
  **zelfde nootduur**, met lyrics (lettergrepen). Alleen als die rij ≥4
  lettergrepen heeft:
    eerste noot = gewone noot (behoud duur)
    middelste = één feathered ||O|| (glyph half; zelfde toon)
    laatste noot = gewone noot (zelfde duur als de eerste — want zelfde rij)

  Noten met andere toon of andere lengte horen niet in die rij (bijv. een
  half «Geest» of «A» na een reeks kwarten blijft erbuiten).

Maatlengte = som van de noten (geen opvulrusten aan het eind).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

_MIN_SYLLABLES = 4
_COLLAPSE_DURS = {
    "quarter",
    "eighth",
    "16th",
    "half",
    "whole",
    "breve",
}

_DUR_Q = {
    "long": Fraction(16),
    "breve": Fraction(8),
    "whole": Fraction(4),
    "half": Fraction(2),
    "quarter": Fraction(1),
    "eighth": Fraction(1, 2),
    "16th": Fraction(1, 4),
    "32nd": Fraction(1, 8),
    "64th": Fraction(1, 16),
}

CHORD_REST_RE = re.compile(r"<(Chord|Rest)\b.*?</\1>", re.S)
MEASURE_RE = re.compile(r"(<Measure\b[^>]*>)(.*?)(</Measure>)", re.S)
VOICE_RE = re.compile(r"(<voice>)(.*?)(</voice>)", re.S)
STAFF_BLOCK_RE = re.compile(
    r'(<Staff id="(\d+)">)(.*?)(</Staff>)',
    re.S,
)


@dataclass
class Ev:
    start: Fraction
    dur: Fraction
    xml: str

    @property
    def end(self) -> Fraction:
        return self.start + self.dur


@dataclass
class Run:
    i0: int
    i1: int
    start: Fraction
    end: Fraction
    first_bits: list[str]
    middle_bits: list[str]
    last_bits: list[str]


def _plain(xml_text: str) -> str:
    t = re.sub(r"<[^>]+>", "", xml_text)
    return (
        t.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .strip()
    )


def _xml_escape(s: str) -> str:
    return (
        s.replace("&amp;", "&")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _lyric_items(chord: str) -> list[tuple[str, str]]:
    """[(tekst zonder sleepstreepje, syllabic)]."""
    items: list[tuple[str, str]] = []
    for lm in re.finditer(r"<Lyrics\b.*?</Lyrics>", chord, re.S):
        block = lm.group(0)
        tm = re.search(r"<text>(.*?)</text>", block, re.S)
        if not tm:
            continue
        text = _plain(tm.group(1))
        if not text or "<sym>" in tm.group(1) or "metNote" in text:
            continue
        text = text.replace("--", "-").strip().strip("-")
        if not text:
            continue
        syll = re.search(r"<syllabic>(\w+)</syllabic>", block)
        kind = syll.group(1) if syll else "single"
        items.append((text, kind))
    return items


def _lyric_bits(chord: str) -> list[str]:
    """Eén entry per lyric (voor drempeltelling)."""
    return [t for t, _k in _lyric_items(chord)]


_FUNC_WORDS = frozenset(
    "de den der des het een en in aan op te van voor met nu of".split()
)

# Liturgische samenstellingen die na spaties weer een koppelteken verdienen.
_FORCE_HYPHEN: dict[tuple[str, ...], str] = {
    ("va", "der"): "Va-der",
    ("hei", "li", "ge"): "Hei-li-ge",
    ("al", "tijd"): "al-tijd",
    ("eeuw", "en"): "eeuw-en",
    ("on", "sterf", "lij", "ke"): "On-sterf'-lij-ke",
    ("sterf", "lij", "ke"): "sterf'-lij-ke",
}


def _rehyphenate_space_syllables(text: str) -> str:
    """Herstel bekende woordafbrekingen; geen de/en/aan-koppelingen."""
    from nl_hyphen import hyphenate_token

    tokens = text.split()
    if len(tokens) < 2:
        return text
    out: list[str] = []
    i = 0
    while i < len(tokens):
        best_j = i + 1
        best = tokens[i]
        for j in range(min(len(tokens), i + 5), i + 1, -1):
            chunk = tokens[i:j]
            cores: list[str] = []
            trailer = ""
            ok = True
            for k, tok in enumerate(chunk):
                m = re.match(r"^(.*?)([.,;:!?]+)?$", tok)
                if not m:
                    ok = False
                    break
                core, punct = m.group(1), m.group(2) or ""
                if not core or (punct and k != len(chunk) - 1):
                    ok = False
                    break
                cores.append(core)
                if punct:
                    trailer = punct
            if not ok or len(cores) < 2:
                continue
            key = tuple(c.lower().replace("'", "") for c in cores)
            if key in _FORCE_HYPHEN:
                # Behoud kapitaal van eerste kern waar relevant
                forced = _FORCE_HYPHEN[key]
                best = forced + trailer
                best_j = j
                break
            # Geen functiewoorden in een automatisch koppel
            if any(c.lower() in _FUNC_WORDS for c in cores):
                continue
            joined = "".join(cores)
            hy = hyphenate_token(joined)
            if hy == cores:
                best = "-".join(cores) + trailer
                best_j = j
                break
        out.append(best)
        i = best_j
    return " ".join(out)


def _merge_lyric_items(items: list[tuple[str, str]]) -> str:
    """Syllabic-keten begin/middle/end → koppelteken; anders spaties (+ herstel)."""
    out: list[str] = []
    buf = ""
    for text, kind in items:
        if kind == "begin":
            if buf:
                out.append(buf.rstrip("-"))
                buf = ""
            buf = text + "-"
        elif kind == "middle":
            buf = (buf + text + "-") if buf else (text + "-")
        elif kind == "end":
            if buf.endswith("-"):
                out.append(buf + text)
            elif buf:
                out.append(buf + "-" + text)
            else:
                out.append(text)
            buf = ""
        else:
            if buf:
                out.append(buf.rstrip("-"))
                buf = ""
            out.append(text)
    if buf:
        out.append(buf.rstrip("-"))
    text = " ".join(out)
    while "--" in text:
        text = text.replace("--", "-")
    text = re.sub(r"\s*-\s*", "-", text)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*", ", ", text)
    text = text.strip()
    # Als alles single was: probeer Nederlandse woordafbreking terug te zetten
    if items and all(k == "single" for _t, k in items):
        text = _rehyphenate_space_syllables(text)
    return text


def _merge_lyric_text(bits: list[str]) -> str:
    """Fallback zonder syllabic-info: spaties tussen lettergrepen."""
    if not bits:
        return ""
    return _merge_lyric_items([(b.rstrip("-"), "single") for b in bits])


def _pitch_key(chord: str) -> str | None:
    if chord.startswith("<Rest"):
        return None
    pitches = re.findall(r"<pitch>(-?\d+)</pitch>", chord)
    if not pitches or len(set(pitches)) != 1:
        return None
    return pitches[0]


def _duration_type(chord: str) -> str | None:
    m = re.search(r"<durationType>(\w+)</durationType>", chord)
    return m.group(1) if m else None


def _dots(chord: str) -> int:
    m = re.search(r"<dots>(\d+)</dots>", chord)
    return int(m.group(1)) if m else 0


def _event_dur(xml: str) -> Fraction:
    dt = _duration_type(xml) or "quarter"
    base = _DUR_Q.get(dt, Fraction(1))
    d = _dots(xml)
    if d == 1:
        return base * Fraction(3, 2)
    if d >= 2:
        return base * Fraction(7, 4)
    return base


def _is_already_recite(chord: str) -> bool:
    return chord.startswith("<Chord") and "<headType>breve</headType>" in chord and (
        "<noStem>1</noStem>" in chord or "<noStem>true</noStem>" in chord
    )


def _has_slur_begin(chord: str) -> bool:
    return bool(
        re.search(r"<Slur\b[^>]*>.*?<SlurType>start</SlurType>", chord, re.S)
        or re.search(r'<Spanner type="Slur">.*?<next>', chord, re.S)
    )


def _strip_lyrics(chord: str) -> str:
    return re.sub(r"\s*<Lyrics\b.*?</Lyrics>", "", chord, flags=re.S)


def _strip_ticks(chord: str) -> str:
    chord = re.sub(r"\s*<ticks>.*?</ticks>", "", chord)
    chord = re.sub(r"\s*<ticks_f>.*?</ticks_f>", "", chord)
    return chord


def _set_single_lyric(chord: str, text: str, syllabic: str = "single") -> str:
    chord = _strip_lyrics(_strip_ticks(chord))
    block = (
        "\n            <Lyrics>\n"
        "               <align>center,baseline</align>\n"
        f"               <syllabic>{syllabic}</syllabic>\n"
        f"               <text>{_xml_escape(text)}</text>\n"
        "               </Lyrics>"
    )
    return re.sub(
        r"(<durationType>\w+</durationType>)",
        r"\1" + block,
        chord,
        count=1,
    )


def _layout_duration(quarters: Fraction) -> Fraction:
    """Rond omhoog af naar ongedoteerde MuseScore-duur (1/2/4/8/16)."""
    if quarters <= 0:
        return Fraction(2)
    need = quarters if quarters == int(quarters) else Fraction(int(quarters) + 1)
    for val in (Fraction(1), Fraction(2), Fraction(4), Fraction(8), Fraction(16)):
        if val >= need:
            return val
    return Fraction(16)


def _set_duration_quarters(chord: str, quarters: Fraction) -> tuple[str, Fraction]:
    """Zet metrische duur; <dots> vóór <durationType> (MuseScore-conventie)."""
    table = [
        (Fraction(1), "quarter", 0),
        (Fraction(3, 2), "quarter", 1),
        (Fraction(2), "half", 0),
        (Fraction(3), "half", 1),
        (Fraction(4), "whole", 0),
        (Fraction(6), "whole", 1),
        (Fraction(8), "breve", 0),
        (Fraction(16), "long", 0),
    ]
    q: Fraction | None = None
    dtype, dots = "half", 0
    for val, dt, d in table:
        if val == quarters:
            q, dtype, dots = val, dt, d
            break
    if q is None:
        q = _layout_duration(quarters)
        for val, dt, d in table:
            if val == q:
                dtype, dots = dt, d
                break

    chord = re.sub(r"\s*<dots>\d+</dots>", "", chord)
    repl = f"<durationType>{dtype}</durationType>"
    if dots:
        repl = f"<dots>{dots}</dots>\n            {repl}"
    if not re.search(r"<durationType>\w+</durationType>", chord):
        return chord, q
    chord = re.sub(r"<durationType>\w+</durationType>", repl, chord, count=1)
    return chord, q


_FEATHERED_LEADING_SPACE = "2.5"  # spatium; ruimte na anker-noot vóór ||O||


def _feathered_chord(template: str, lyric_text: str | None) -> str:
    chord = _strip_ticks(template)
    chord = re.sub(
        r"<durationType>\w+</durationType>",
        "<durationType>half</durationType>",
        chord,
        count=1,
    )
    chord = re.sub(r"<dots>\d+</dots>\s*", "", chord)
    chord = re.sub(r"\s*<leadingSpace>[^<]*</leadingSpace>", "", chord)
    if "<noStem>" not in chord:
        chord = re.sub(
            r"(<durationType>half</durationType>)",
            r"\1\n            <noStem>1</noStem>",
            chord,
            count=1,
        )
    else:
        chord = re.sub(r"<noStem>[^<]*</noStem>", "<noStem>1</noStem>", chord)
    # Extra horizontale ruimte zodat ankerlettergreep en recite-tekst niet plakken
    chord = re.sub(
        r"(<durationType>half</durationType>)",
        rf"\1\n            <leadingSpace>{_FEATHERED_LEADING_SPACE}</leadingSpace>",
        chord,
        count=1,
    )

    def note_repl(m: re.Match[str]) -> str:
        note = m.group(0)
        if "<headType>" in note:
            return re.sub(
                r"<headType>\w+</headType>",
                "<headType>breve</headType>",
                note,
            )
        return re.sub(
            r"(<Note\b[^>]*>)",
            r"\1\n               <headType>breve</headType>",
            note,
            count=1,
        )

    chord = re.sub(r"<Note\b.*?</Note>", note_repl, chord, flags=re.S)
    chord = _strip_lyrics(chord)
    if lyric_text is not None:
        chord = _set_single_lyric(chord, lyric_text, "single")
    return chord


def _parse_voice_events(voice_inner: str) -> list[Ev]:
    events: list[Ev] = []
    t = Fraction(0)
    for m in CHORD_REST_RE.finditer(voice_inner):
        xml = m.group(0)
        events.append(Ev(start=t, dur=_event_dur(xml), xml=xml))
        t += events[-1].dur
    return events


def _syllabic_of(chord: str) -> str:
    m = re.search(r"<syllabic>(\w+)</syllabic>", chord)
    return m.group(1) if m else "single"


def _word_continues_ok(events: list[Ev], j: int, pitch: str) -> bool:
    if _syllabic_of(events[j].xml) != "begin":
        return True
    k = j
    while k < len(events):
        ev = events[k]
        if not ev.xml.startswith("<Chord"):
            return False
        if _pitch_key(ev.xml) != pitch:
            return False
        if _duration_type(ev.xml) not in _COLLAPSE_DURS:
            return False
        s = _syllabic_of(ev.xml)
        if k > j and s in ("single", "begin"):
            break
        if s == "end":
            return True
        if s in ("begin", "middle"):
            k += 1
            continue
        return True
    return False


def _lead_runs(events: list[Ev]) -> list[Run]:
    """Vind reeksen ≥4 lettergrepen: zelfde toonhoogte én dezelfde nootduur."""
    runs: list[Run] = []
    i = 0
    while i < len(events):
        ev = events[i]
        if not ev.xml.startswith("<Chord"):
            i += 1
            continue
        if _is_already_recite(ev.xml) or _has_slur_begin(ev.xml):
            i += 1
            continue
        pitch = _pitch_key(ev.xml)
        bits = _lyric_bits(ev.xml)
        dur_t = _duration_type(ev.xml)
        if pitch is None or not bits or dur_t not in _COLLAPSE_DURS:
            i += 1
            continue
        anchor_dur = _event_dur(ev.xml)
        run_idxs = [i]
        run_bits = list(bits)
        j = i + 1
        while j < len(events):
            nxt = events[j]
            if not nxt.xml.startswith("<Chord"):
                break
            if _is_already_recite(nxt.xml) or _has_slur_begin(nxt.xml):
                break
            if _pitch_key(nxt.xml) != pitch:
                break
            # Andere lengte (bijv. half na kwarten) hoort niet in de recite-rij
            if _event_dur(nxt.xml) != anchor_dur:
                break
            if _duration_type(nxt.xml) not in _COLLAPSE_DURS:
                break
            nb = _lyric_bits(nxt.xml)
            if not nb:
                break
            run_idxs.append(j)
            run_bits.extend(nb)
            j += 1
        if len(run_bits) >= _MIN_SYLLABLES and len(run_idxs) >= 3:
            first_bits = _lyric_bits(events[run_idxs[0]].xml)
            last_bits = _lyric_bits(events[run_idxs[-1]].xml)
            middle_items: list[tuple[str, str]] = []
            for ix in run_idxs[1:-1]:
                middle_items.extend(_lyric_items(events[ix].xml))
            runs.append(
                Run(
                    i0=run_idxs[0],
                    i1=run_idxs[-1] + 1,
                    start=events[run_idxs[0]].start,
                    end=events[run_idxs[-1]].end,
                    first_bits=first_bits,
                    middle_bits=[_merge_lyric_items(middle_items)] if middle_items else [],
                    last_bits=last_bits,
                )
            )
            i = run_idxs[-1] + 1
        else:
            i += 1
    return runs


def _edge_lyric(bits: list[str]) -> tuple[str, str]:
    """Eerste/laatste MCI-noot: altijd 'single' (geen doorkoppeling naar de ||O||)."""
    if not bits:
        return "", "single"
    text = _merge_lyric_text(bits).strip().strip("-")
    return text, "single"


def _collapse_events_for_run(
    events: list[Ev],
    run: Run,
    *,
    is_lead: bool,
    lead_shape: tuple[Fraction, Fraction, Fraction] | None = None,
) -> list[Ev]:
    before = events[: run.i0]
    mid_events = events[run.i0 : run.i1]
    after = events[run.i1 :]
    if not mid_events:
        return events

    first = mid_events[0]
    last = mid_events[-1]
    middle_src = mid_events[len(mid_events) // 2]

    if lead_shape is not None:
        first_dur, mid_dur, last_dur = lead_shape
    elif len(mid_events) >= 3:
        # MCI 1-n-1: ankers zelfde duur; middenbreedte ~ aantal lettergrepen
        first_dur = mid_events[0].dur
        last_dur = first_dur
        n_mid = max(1, len(mid_events) - 2)
        mid_dur = _layout_duration(n_mid * first_dur)
    else:
        return events

    if is_lead:
        ft, fs = _edge_lyric(run.first_bits)
        lt, ls = _edge_lyric(run.last_bits)
        first_xml = _set_single_lyric(first.xml, ft, fs) if ft else _strip_lyrics(first.xml)
        last_xml = _set_single_lyric(last.xml, lt, ls) if lt else _strip_lyrics(last.xml)
        mid_text = run.middle_bits[0] if run.middle_bits else ""
        src = (
            _defather_to_quarter(middle_src.xml)
            if _is_already_recite(middle_src.xml)
            else middle_src.xml
        )
        feathered = _feathered_chord(src, mid_text or None)
    else:
        first_xml = _strip_lyrics(
            _defather_to_quarter(first.xml) if _is_already_recite(first.xml) else first.xml
        )
        last_xml = _strip_lyrics(
            _defather_to_quarter(last.xml) if _is_already_recite(last.xml) else last.xml
        )
        src = (
            _defather_to_quarter(middle_src.xml)
            if _is_already_recite(middle_src.xml)
            else middle_src.xml
        )
        feathered = _feathered_chord(src, None)

    first_xml, first_dur = _set_duration_quarters(first_xml, first_dur)
    last_xml, last_dur = _set_duration_quarters(last_xml, last_dur)
    # Breedte naar lettergrepen; glyph blijft feathered (breve/noStem)
    feathered, mid_dur = _set_duration_quarters(feathered, mid_dur)
    # Glyph-markering behouden na durationType-wissel
    if "<noStem>" not in feathered:
        feathered = re.sub(
            r"(<durationType>\w+</durationType>)",
            r"\1\n            <noStem>1</noStem>",
            feathered,
            count=1,
        )
    if "<headType>breve</headType>" not in feathered:
        feathered = re.sub(
            r"(<Note\b[^>]*>)",
            r"\1\n               <headType>breve</headType>",
            feathered,
            count=1,
        )

    t = run.start
    new_mid = [
        Ev(start=t, dur=first_dur, xml=first_xml),
    ]
    t += first_dur
    new_mid.append(Ev(start=t, dur=mid_dur, xml=feathered))
    t += mid_dur
    new_mid.append(Ev(start=t, dur=last_dur, xml=last_xml))
    t += last_dur

    out = list(before) + new_mid
    for e in after:
        out.append(Ev(start=t, dur=e.dur, xml=e.xml))
        t += e.dur
    return out


def _run_for_ticks(events: list[Ev], start: Fraction, end: Fraction) -> Run | None:
    idxs = [i for i, e in enumerate(events) if e.start >= start and e.start < end]
    if len(idxs) < 3:
        return None
    return Run(
        i0=idxs[0],
        i1=idxs[-1] + 1,
        start=events[idxs[0]].start,
        end=events[idxs[-1]].end,
        first_bits=[],
        middle_bits=[],
        last_bits=[],
    )


def _rebuild_voice(prefix: str, events: list[Ev], suffix: str) -> str:
    return prefix + "".join(e.xml for e in events) + suffix


def _set_measure_len(meas_open: str, quarters: Fraction) -> str:
    whole = quarters / 4
    attr = (
        str(whole.numerator)
        if whole.denominator == 1
        else f"{whole.numerator}/{whole.denominator}"
    )
    if re.search(r"\blen=", meas_open):
        return re.sub(r'\blen="[^"]*"', f'len="{attr}"', meas_open, count=1)
    return re.sub(r"<Measure\b", f'<Measure len="{attr}"', meas_open, count=1)


def _collapse_measure_voices(voice_xmls: list[str]) -> tuple[list[str], int]:
    if not voice_xmls:
        return voice_xmls, 0
    parsed: list[tuple[str, list[Ev], str]] = []
    for inner in voice_xmls:
        events = _parse_voice_events(inner)
        m = CHORD_REST_RE.search(inner)
        if m:
            pre = inner[: m.start()]
            last = None
            for last in CHORD_REST_RE.finditer(inner):
                pass
            suf = inner[last.end() :] if last else ""
        else:
            pre, suf, events = inner, "", []
        parsed.append((pre, events, suf))

    runs = _lead_runs(parsed[0][1])
    if not runs:
        return voice_xmls, 0

    new_parsed = parsed
    for run in reversed(runs):
        lead_ev = new_parsed[0][1]
        mid_events = lead_ev[run.i0 : run.i1]
        if len(mid_events) < 3:
            continue
        # MCI 1-n-1: zelfde ankerduur; middenbreedte ~ lettergrepen (layout)
        edge = mid_events[0].dur
        n_mid = max(1, len(mid_events) - 2)
        mid_dur = _layout_duration(n_mid * edge)
        lead_shape = (edge, mid_dur, edge)
        updated: list[tuple[str, list[Ev], str]] = []
        for vi, (pre, events, suf) in enumerate(new_parsed):
            if vi == 0:
                updated.append(
                    (
                        pre,
                        _collapse_events_for_run(
                            events, run, is_lead=True, lead_shape=lead_shape
                        ),
                        suf,
                    )
                )
            else:
                other = _run_for_ticks(events, run.start, run.end)
                if other is None:
                    updated.append((pre, events, suf))
                else:
                    updated.append(
                        (
                            pre,
                            _collapse_events_for_run(
                                events,
                                other,
                                is_lead=False,
                                lead_shape=lead_shape,
                            ),
                            suf,
                        )
                    )
        new_parsed = updated

    return [_rebuild_voice(p, e, s) for p, e, s in new_parsed], len(runs)


def _break_function_hyphens(text: str) -> str:
    """aan-de / de-Zoon → spaties; Va-der / eeuw-en blijven intact."""
    out = text
    for fw in sorted(_FUNC_WORDS, key=len, reverse=True):
        # Alleen functiewoord aan het *begin* van een koppeling (aan-de),
        # niet aan het eind (Va-der, eeuw-en).
        out = re.sub(rf"(?i)(?<![-\w]){re.escape(fw)}-", rf"{fw} ", out)
    out = re.sub(r" +", " ", out)
    out = re.sub(r"\s+,", ",", out)
    return out.strip()


def _syllables_from_merged(text: str) -> list[tuple[str, str]]:
    """Splits hub-lyric (spaties + trailing '-') naar (syllable, syllabic)."""
    from nl_hyphen import hyphenate_token

    text = _break_function_hyphens(text)
    out: list[tuple[str, str]] = []
    for word in text.split():
        w = word.strip()
        if not w:
            continue
        if "-" in w.rstrip("-") or w.endswith("-"):
            parts = [p for p in w.replace("-", " ").split() if p]
            if not parts:
                continue
        else:
            parts = hyphenate_token(w) or [w]
        n = len(parts)
        for i, p in enumerate(parts):
            if n == 1:
                out.append((p, "single"))
            elif i == 0:
                out.append((p, "begin"))
            elif i == n - 1:
                out.append((p, "end"))
            else:
                out.append((p, "middle"))
    return out


def _quarter_from_template(template: str, syl: str | None, syllabic: str) -> str:
    chord = _strip_ticks(template)
    chord = re.sub(
        r"<durationType>\w+</durationType>",
        "<durationType>quarter</durationType>",
        chord,
        count=1,
    )
    chord = re.sub(r"<dots>\d+</dots>\s*", "", chord)
    chord = re.sub(r"\s*<noStem>[^<]*</noStem>", "", chord)
    chord = re.sub(r"\s*<headType>\w+</headType>", "", chord)
    if syl is None:
        return _strip_lyrics(chord)
    return _set_single_lyric(chord, syl, syllabic)


def _defather_to_quarter(chord: str) -> str:
    """Feathered glyph -> gewone kwart (lyrics behouden)."""
    chord = _strip_ticks(chord)
    chord = re.sub(
        r"<durationType>\w+</durationType>",
        "<durationType>quarter</durationType>",
        chord,
        count=1,
    )
    chord = re.sub(r"<dots>\d+</dots>\s*", "", chord)
    chord = re.sub(r"\s*<noStem>[^<]*</noStem>", "", chord)
    chord = re.sub(r"\s*<headType>\w+</headType>", "", chord)
    return chord


def _expand_feathered_events(
    events: list[Ev],
    *,
    count_at: dict[Fraction, int] | None,
    lyrics_at: dict[Fraction, list[tuple[str, str]]] | None,
) -> tuple[list[Ev], dict[Fraction, int], dict[Fraction, list[tuple[str, str]]]]:
    """Expand multi-syl ||O||; single-syl ||O|| -> gewone kwart. Lead vult counts."""
    out: list[Ev] = []
    counts = dict(count_at or {})
    lyrics = dict(lyrics_at or {})
    t = Fraction(0)
    for ev in events:
        is_rec = ev.xml.startswith("<Chord") and _is_already_recite(ev.xml)
        if not is_rec:
            out.append(Ev(start=t, dur=ev.dur, xml=ev.xml))
            t += ev.dur
            continue

        if count_at is None:
            merged = _merge_lyric_text(_lyric_bits(ev.xml))
            syls = _syllables_from_merged(merged) if merged else []
            if len(syls) > 1:
                n = len(syls)
                counts[ev.start] = n
                lyrics[ev.start] = syls
                each = Fraction(1)
                for i in range(n):
                    syl, syllabic = syls[i]
                    xml = _quarter_from_template(ev.xml, syl, syllabic)
                    out.append(Ev(start=t, dur=each, xml=xml))
                    t += each
                continue
            # Enkele lettergreep op ||O||: gewoon kwart + syllabic single
            counts[ev.start] = 1
            xml = _defather_to_quarter(ev.xml)
            xml = re.sub(
                r"<syllabic>\w+</syllabic>",
                "<syllabic>single</syllabic>",
                xml,
            )
            # Tekst zonder sleepstreepje
            def _fix_text(m: re.Match[str]) -> str:
                return "<text>" + _plain(m.group(1)).strip().strip("-") + "</text>"

            xml = re.sub(r"<text>(.*?)</text>", _fix_text, xml, count=1, flags=re.S)
            out.append(Ev(start=t, dur=Fraction(1), xml=xml))
            t += Fraction(1)
            continue

        n = counts.get(ev.start, 0)
        if n <= 0:
            out.append(Ev(start=t, dur=ev.dur, xml=ev.xml))
            t += ev.dur
            continue
        if n == 1:
            xml = _defather_to_quarter(ev.xml)
            xml = _strip_lyrics(xml)
            out.append(Ev(start=t, dur=Fraction(1), xml=xml))
            t += Fraction(1)
            continue
        each = Fraction(1)
        for _i in range(n):
            xml = _quarter_from_template(ev.xml, None, "single")
            out.append(Ev(start=t, dur=each, xml=xml))
            t += each
    return out, counts, lyrics


def _expand_existing_recite(mscx: str) -> str:
    """Zet bestaande ||O|| terug naar kwarten (alle voices, homofoon)."""
    staff_matches = [
        m for m in STAFF_BLOCK_RE.finditer(mscx) if "<Measure" in m.group(3)
    ]
    if not staff_matches:
        return mscx
    per_staff = [list(MEASURE_RE.finditer(sm.group(3))) for sm in staff_matches]
    n_measures = min(len(ms) for ms in per_staff)
    new_measures = [[m.group(0) for m in ms] for ms in per_staff]

    for mi in range(n_measures):
        opens: list[str] = []
        bodies: list[str] = []
        closes: list[str] = []
        # Alle voices over alle staven, zelfde volgorde als collapse.
        voice_parsed: list[tuple[int, int, str, list[Ev], str]] = []
        for si in range(len(staff_matches)):
            mo = MEASURE_RE.match(new_measures[si][mi])
            assert mo
            opens.append(mo.group(1))
            bodies.append(mo.group(2))
            closes.append(mo.group(3))
            voices = list(VOICE_RE.finditer(mo.group(2)))
            for vi, vm in enumerate(voices):
                voice_parsed.append(
                    (si, vi, vm.group(1), _parse_voice_events(vm.group(2)), vm.group(3))
                )

        if not voice_parsed:
            continue
        if not any(
            _is_already_recite(e.xml)
            for *_, events, _ in voice_parsed
            for e in events
            if e.xml.startswith("<Chord")
        ):
            continue

        lead_events, counts, lyrics = _expand_feathered_events(
            voice_parsed[0][3], count_at=None, lyrics_at=None
        )
        expanded: list[tuple[int, int, str, list[Ev], str]] = [
            (
                voice_parsed[0][0],
                voice_parsed[0][1],
                voice_parsed[0][2],
                lead_events,
                voice_parsed[0][4],
            )
        ]
        for si, vi, pre, events, suf in voice_parsed[1:]:
            ev2, _, _ = _expand_feathered_events(
                events, count_at=counts, lyrics_at=lyrics
            )
            expanded.append((si, vi, pre, ev2, suf))

        total_q = sum((e.dur for e in lead_events), Fraction(0))
        by_staff: dict[int, list[tuple[int, str]]] = {}
        for si, vi, _pre, events, _suf in expanded:
            by_staff.setdefault(si, []).append(
                (vi, "".join(e.xml for e in events))
            )

        for si in range(len(staff_matches)):
            body = bodies[si]
            entries = by_staff.get(si, [])
            state = {"i": 0}

            def repl_voice(vm: re.Match[str]) -> str:
                idx = state["i"]
                state["i"] += 1
                if idx < len(entries):
                    return vm.group(1) + entries[idx][1] + vm.group(3)
                return vm.group(0)

            body = VOICE_RE.sub(repl_voice, body)
            new_measures[si][mi] = (
                _set_measure_len(opens[si], total_q) + body + closes[si]
            )

    out = mscx
    for si in range(len(staff_matches) - 1, -1, -1):
        sm = staff_matches[si]
        old_body = sm.group(3)
        ms_old = list(MEASURE_RE.finditer(old_body))
        new_body = old_body
        for mi in range(len(ms_old) - 1, -1, -1):
            if mi >= len(new_measures[si]):
                continue
            m = ms_old[mi]
            new_body = (
                new_body[: m.start()] + new_measures[si][mi] + new_body[m.end() :]
            )
        out = (
            out[: sm.start()]
            + sm.group(1)
            + new_body
            + sm.group(4)
            + out[sm.end() :]
        )
    return out


def collapse_recite_mscx(mscx: str) -> tuple[str, int]:
    # Eerst bestaande (mogelijk verkeerde) ||O|| terugzetten, daarna MCI-collaps.
    mscx = _expand_existing_recite(mscx)
    staff_matches = [
        m for m in STAFF_BLOCK_RE.finditer(mscx) if "<Measure" in m.group(3)
    ]
    if not staff_matches:
        return mscx, 0

    per_staff = [list(MEASURE_RE.finditer(sm.group(3))) for sm in staff_matches]
    n_measures = min(len(ms) for ms in per_staff)
    if n_measures == 0:
        return mscx, 0

    total_runs = 0
    new_measures = [[m.group(0) for m in ms] for ms in per_staff]

    for mi in range(n_measures):
        voice_inners: list[str] = []
        voice_locs: list[tuple[int, int]] = []
        opens: list[str] = []
        bodies: list[str] = []
        closes: list[str] = []
        for si in range(len(staff_matches)):
            mo = MEASURE_RE.match(new_measures[si][mi])
            assert mo
            opens.append(mo.group(1))
            bodies.append(mo.group(2))
            closes.append(mo.group(3))
            voices = list(VOICE_RE.finditer(mo.group(2)))
            if not voices:
                voice_inners.append(mo.group(2))
                voice_locs.append((si, -1))
            else:
                for vi, vm in enumerate(voices):
                    voice_inners.append(vm.group(2))
                    voice_locs.append((si, vi))

        new_inners, n_runs = _collapse_measure_voices(voice_inners)
        if n_runs == 0:
            continue
        total_runs += n_runs

        by_staff: dict[int, list[tuple[int, str]]] = {}
        for (si, vi), inner in zip(voice_locs, new_inners):
            by_staff.setdefault(si, []).append((vi, inner))

        lead_events = _parse_voice_events(new_inners[0])
        total_q = sum((e.dur for e in lead_events), Fraction(0))

        for si in range(len(staff_matches)):
            body = bodies[si]
            entries = by_staff.get(si, [])
            if entries and entries[0][0] == -1:
                body = entries[0][1]
            else:
                state = {"i": 0}

                def repl_voice(vm: re.Match[str]) -> str:
                    idx = state["i"]
                    state["i"] += 1
                    if idx < len(entries):
                        return vm.group(1) + entries[idx][1] + vm.group(3)
                    return vm.group(0)

                body = VOICE_RE.sub(repl_voice, body)
            new_measures[si][mi] = (
                _set_measure_len(opens[si], total_q) + body + closes[si]
            )

    out = mscx
    for si in range(len(staff_matches) - 1, -1, -1):
        sm = staff_matches[si]
        old_body = sm.group(3)
        ms_old = list(MEASURE_RE.finditer(old_body))
        new_body = old_body
        for mi in range(len(ms_old) - 1, -1, -1):
            if mi >= len(new_measures[si]):
                continue
            m = ms_old[mi]
            new_body = (
                new_body[: m.start()] + new_measures[si][mi] + new_body[m.end() :]
            )
        out = (
            out[: sm.start()]
            + sm.group(1)
            + new_body
            + sm.group(4)
            + out[sm.end() :]
        )
    out, _n_trim = sync_measures_no_filler_rests(out)
    return out, total_runs


def _strip_nonleading_rests(voice_inner: str) -> str:
    """Houd alleen leidende rusten; wis rusten na de eerste noot (opvulling)."""
    parts: list[str] = []
    pos = 0
    seen_chord = False
    for m in CHORD_REST_RE.finditer(voice_inner):
        parts.append(voice_inner[pos : m.start()])
        if m.group(1) == "Rest" and seen_chord:
            pos = m.end()
            continue
        if m.group(1) == "Chord":
            seen_chord = True
        parts.append(m.group(0))
        pos = m.end()
    parts.append(voice_inner[pos:])
    return "".join(parts)


def sync_measures_no_filler_rests(mscx: str) -> tuple[str, int]:
    """Verwijder opvulrusten; zet elke maat-len op de som van de noten.

    MuseScore tekent anders rusten als Measure len langer is dan de noten
    (of als <dots> na durationType staat en genegeerd wordt).
    Leidende gap-rusten blijven staan.
    """
    staff_matches = [
        m for m in STAFF_BLOCK_RE.finditer(mscx) if "<Measure" in m.group(3)
    ]
    if not staff_matches:
        return mscx, 0
    per_staff = [list(MEASURE_RE.finditer(sm.group(3))) for sm in staff_matches]
    n_measures = min(len(ms) for ms in per_staff)
    trimmed = 0
    new_measures = [[m.group(0) for m in ms] for ms in per_staff]

    for mi in range(n_measures):
        opens: list[str] = []
        bodies: list[str] = []
        closes: list[str] = []
        voice_sums: list[Fraction] = []
        for si in range(len(staff_matches)):
            mo = MEASURE_RE.match(new_measures[si][mi])
            assert mo
            opens.append(mo.group(1))
            body = mo.group(2)
            closes.append(mo.group(3))

            def fix_voice(vm: re.Match[str]) -> str:
                nonlocal trimmed
                before = vm.group(2)
                after = _strip_nonleading_rests(before)
                if after != before:
                    trimmed += before.count("<Rest") - after.count("<Rest")
                return vm.group(1) + after + vm.group(3)

            body2 = VOICE_RE.sub(fix_voice, body)
            bodies.append(body2)
            voices = list(VOICE_RE.finditer(body2))
            if voices:
                evs = _parse_voice_events(voices[0].group(2))
                voice_sums.append(sum((e.dur for e in evs), Fraction(0)))
            else:
                voice_sums.append(Fraction(0))

        total_q = max(voice_sums) if voice_sums else Fraction(0)
        if total_q <= 0:
            continue
        for si in range(len(staff_matches)):
            new_measures[si][mi] = (
                _set_measure_len(opens[si], total_q) + bodies[si] + closes[si]
            )

    out = mscx
    for si in range(len(staff_matches) - 1, -1, -1):
        sm = staff_matches[si]
        old_body = sm.group(3)
        ms_old = list(MEASURE_RE.finditer(old_body))
        new_body = old_body
        for mi in range(len(ms_old) - 1, -1, -1):
            if mi >= len(new_measures[si]):
                continue
            m = ms_old[mi]
            new_body = (
                new_body[: m.start()] + new_measures[si][mi] + new_body[m.end() :]
            )
        out = (
            out[: sm.start()]
            + sm.group(1)
            + new_body
            + sm.group(4)
            + out[sm.end() :]
        )
    return out, trimmed
