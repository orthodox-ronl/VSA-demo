"""Pas de A4-standaard-layout toe op een MuseScore 4 .mscz (idempotent).

Contract: scripts/mscz-layout-contract.md
Laag 4 (PDF/A4). Lagen 1-3: cleanup_capella_mxl.py. Niet in check.

  python scripts/apply_mscz_layout.py pad\\naar\\file.mscz
  python scripts/apply_mscz_layout.py pad\\naar\\file.mxl -o uit.mscz

Bestandsnamen: geen spaties (`scripts/score_filenames.py`). `.mxl` als
invoer wordt via MuseScore naar `.mscz` geconverteerd en daarna gelayout.

Opnieuw draaien is de bedoeling: style-overrides worden steeds gezet, titelvak
opnieuw opgebouwd. Muziek (noten, lyrics, stemmen) blijft staan.

Productierijp -> verhuizen naar VSA-tooling (docs + demo-verhaal in VSA-demo).
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from score_filenames import published_path, require_no_spaces

# A4 in inches (MuseScore pageWidth/pageHeight). 15 mm = 0.590551 in.
_A4_W = "8.26772"
_A4_H = "11.6929"
_M = "0.590551"
_PRINTABLE = "7.08662"  # A4_W - 2 * 15 mm

# Moet gelijk lopen met scripts/mscz-layout-contract.md
# Typografie: VSA-defaults (bron/VSA-tooling): Source Sans 3, lyrics 13 pt, word 12 pt.
_FONT = "Source Sans 3"
STYLE_OVERRIDES: dict[str, str] = {
    "pageWidth": _A4_W,
    "pageHeight": _A4_H,
    "pagePrintableWidth": _PRINTABLE,
    "pageEvenLeftMargin": _M,
    "pageOddLeftMargin": _M,
    "pageEvenTopMargin": _M,
    "pageOddTopMargin": _M,
    "pageEvenBottomMargin": _M,
    "pageOddBottomMargin": _M,
    "pageTwosided": "0",
    "enableIndentationOnFirstSystem": "0",
    "firstSystemIndentationValue": "0",
    "lastSystemFillLimit": "1",
    "enableVerticalSpread": "0",
    "maxPageFillSpread": "0",
    "minSystemDistance": "8",
    "maxSystemDistance": "14",
    "hideInstrumentNameIfOneInstrument": "1",
    "firstSystemInstNameVisibility": "0",
    "subsSystemInstNameVisibility": "0",
    "showMeasureNumber": "1",
    "showMeasureNumberOne": "1",
    "measureNumberSystem": "1",
    "measureNumberInterval": "0",
    "frameSystemDistance": "14",
    "lyricsPlacement": "1",
    "lyricsOddFontFace": _FONT,
    "lyricsEvenFontFace": _FONT,
    "lyricsOddFontSize": "13",
    "lyricsEvenFontSize": "13",
    "lyricsOddFontSpatiumDependent": "0",
    "lyricsEvenFontSpatiumDependent": "0",
    "staffTextFontFace": _FONT,
    "staffTextFontSize": "12",
    "staffTextFontSpatiumDependent": "0",
    "staffTextAlign": "left,baseline",
    "staffTextPosition": "left",
    "systemTextFontFace": _FONT,
    "systemTextFontSize": "12",
    "systemTextFontSpatiumDependent": "0",
    "systemTextAlign": "left,baseline",
    "systemTextPosition": "left",
    "titleFontFace": _FONT,
    "titleFontSize": "18",
    "composerFontFace": _FONT,
    "composerFontSize": "12",
    "subTitleFontFace": _FONT,
    "subTitleFontSize": "14",
    "frameFontFace": _FONT,
    "frameFontSize": "12",
}

CUE_RE = re.compile(r"^\s*[PDK]\s*[:;]", re.I)
VBOX_RE = re.compile(r"[ \t]*<VBox>.*?</VBox>", re.S)
STAFF_TEXT_RE = re.compile(r"<StaffText>.*?</StaffText>", re.S)
MEASURE_RE = re.compile(r"<Measure\b.*?</Measure>", re.S)
VOICE_RE = re.compile(r"<voice>.*?</voice>", re.S)
CHORD_REST_RE = re.compile(r"<(Chord|Rest)\b.*?</\1>", re.S)
LYRICS_RE = re.compile(r"<Lyrics>.*?</Lyrics>", re.S)
TEXT_INNER_RE = re.compile(r"<text>(.*?)</text>", re.S)
_QUARTERS = {
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
STYLE_INNER_RE = re.compile(r"<style>(.*?)</style>", re.S)
META_RE = re.compile(
    r'<metaTag name="(?P<name>[^"]*)">(?P<val>.*?)</metaTag>',
    re.S,
)


def _plain(fragment: str) -> str:
    return re.sub(r"<[^>]+>", "", fragment).replace("&amp;", "&").strip()


def _xml_text(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _is_cue(text: str) -> bool:
    return bool(CUE_RE.match(text or ""))


def _meta(mscx: str, name: str) -> str:
    for m in META_RE.finditer(mscx):
        if m.group("name") == name:
            return _plain(m.group("val"))
    return ""


def _set_meta(mscx: str, name: str, value: str) -> str:
    pat = rf'<metaTag name="{re.escape(name)}">.*?</metaTag>'
    repl = f'<metaTag name="{name}">{_xml_text(value)}</metaTag>'
    if re.search(pat, mscx, re.S):
        return re.sub(pat, repl, mscx, count=1, flags=re.S)
    insert = f"    {repl}\n    "
    if "</Score>" in mscx:
        return mscx.replace("</Score>", insert + "</Score>", 1)
    return mscx + insert


def _vbox_fields(vbox: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for tm in re.finditer(r"<Text>.*?</Text>", vbox, re.S):
        block = tm.group(0)
        sm = STYLE_INNER_RE.search(block)
        xm = TEXT_INNER_RE.search(block)
        if sm and xm:
            out[sm.group(1).strip()] = _plain(xm.group(1))
    return out


def _staff_plain(block: str) -> str:
    xm = TEXT_INNER_RE.search(block)
    return _plain(xm.group(1)) if xm else ""


def overlay_style(mss: str, extra: dict[str, str] | None = None) -> str:
    overrides = dict(STYLE_OVERRIDES)
    if extra:
        overrides.update(extra)
    if "<Style>" not in mss:
        body = "\n".join(
            f"    <{k}>{v}</{k}>" for k, v in overrides.items()
        )
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<museScore version="4.70">\n  <Style>\n'
            f"{body}\n  </Style>\n</museScore>\n"
        )
    for tag, value in overrides.items():
        pat = rf"<{tag}>.*?</{tag}>"
        repl = f"<{tag}>{value}</{tag}>"
        if re.search(pat, mss, re.S):
            mss = re.sub(pat, repl, mss, count=1, flags=re.S)
        else:
            mss = mss.replace(
                "</Style>",
                f"    <{tag}>{value}</{tag}>\n    </Style>",
                1,
            )
    return mss


def _build_vbox(title: str, composer: str) -> str:
    lines = [
        "      <VBox>",
        "        <boxAutoSize>1</boxAutoSize>",
        "        <bottomGap>2</bottomGap>",
        "        <Text>",
        "          <style>title</style>",
        f"          <text>{_xml_text(title)}</text>",
        "          </Text>",
    ]
    if composer:
        lines += [
            "        <Text>",
            "          <style>composer</style>",
            f"          <text>{_xml_text(composer)}</text>",
            "          </Text>",
        ]
    lines.append("        </VBox>")
    return "\n".join(lines)


def _ensure_first_measure_stafftext(mscx: str, cue: str) -> str:
    if not cue:
        return mscx
    for block in STAFF_TEXT_RE.findall(mscx):
        if _staff_plain(block) == cue:
            return mscx
    staff = re.search(r'<Staff id="1">', mscx)
    if not staff:
        return mscx
    meas = re.search(r"<Measure>", mscx[staff.end() :])
    if not meas:
        return mscx
    meas_abs = staff.end() + meas.start()
    voice = re.search(r"<voice>", mscx[meas_abs:])
    if not voice:
        return mscx
    voice_abs = meas_abs + voice.start()
    voice_open_end = mscx.find(">", voice_abs) + 1
    insert = (
        "\n          <StaffText>\n"
        f"            <text>{_xml_text(cue)}</text>\n"
        "            </StaffText>"
    )
    return mscx[:voice_open_end] + insert + mscx[voice_open_end:]


def _strip_arial_on_stafftext(mscx: str) -> str:
    def fix(m: re.Match[str]) -> str:
        b = m.group(0)
        b = re.sub(r"\s*<family>Arial</family>", "", b)
        b = re.sub(r'<font face="Arial"\s*/>', "", b)
        return b

    return STAFF_TEXT_RE.sub(fix, mscx)


def _double_bar(meas: str) -> bool:
    return bool(re.search(r"<BarLine>.*?<subtype>double</subtype>", meas, re.S))


def _ensure_rest_gap(rest: str) -> str:
    """Geen kolombreedte, wel ticks (MuseScore gap-rest)."""
    if "<gap>" not in rest:
        rest = rest.replace("<Rest>", "<Rest>\n            <gap>1</gap>", 1)
    else:
        rest = re.sub(r"<gap>.*?</gap>", "<gap>1</gap>", rest, count=1)
    if "<visible>0</visible>" not in rest:
        rest = rest.replace("<Rest>", "<Rest>\n            <visible>0</visible>", 1)
    return rest


def _move_last_rest_to_front(voice: str) -> str:
    items = list(CHORD_REST_RE.finditer(voice))
    if len(items) < 2:
        return voice
    if items[0].group(1) != "Chord" or items[-1].group(1) != "Rest":
        return voice
    last = items[-1]
    rest = last.group(0)
    without = voice[: last.start()] + voice[last.end() :]
    first = CHORD_REST_RE.search(without)
    if first is None:
        return voice
    return without[: first.start()] + rest + without[first.start() :]


def _gap_leading_rests(meas: str) -> str:
    def fix_voice(vm: re.Match[str]) -> str:
        v = vm.group(0)
        out = []
        pos = 0
        leading = True
        for cr in CHORD_REST_RE.finditer(v):
            out.append(v[pos : cr.start()])
            block = cr.group(0)
            if leading and cr.group(1) == "Rest":
                block = _ensure_rest_gap(block)
            else:
                leading = False
            out.append(block)
            pos = cr.end()
        out.append(v[pos:])
        return "".join(out)

    return VOICE_RE.sub(fix_voice, meas)


def _restore_swapped_leading_rest(meas: str) -> str:
    """Herstel: noten stonden na een leidende rust; korting zette de rust achteraan."""
    new_meas = VOICE_RE.sub(lambda vm: _move_last_rest_to_front(vm.group(0)), meas)
    donor = None
    for vm in VOICE_RE.finditer(new_meas):
        cr = CHORD_REST_RE.search(vm.group(0))
        if cr is not None and cr.group(1) == "Rest":
            donor = cr.group(0)
            break
    if donor is None:
        return new_meas

    def fill_voice(vm: re.Match[str]) -> str:
        v = vm.group(0)
        cr = CHORD_REST_RE.search(v)
        if cr is None or cr.group(1) != "Chord":
            return v
        return v[: cr.start()] + donor + v[cr.start() :]

    return VOICE_RE.sub(fill_voice, new_meas)


# Maten waar de pickup-korting rust en noot verwisselde (0-based, per balk).
_SWAPPED_LEADING_REST = {0, 10, 14, 56}


def _fix_leading_rest_spacing(mscx: str) -> tuple[str, int, int]:
    n_restore = 0
    n_gap = 0

    def fix_staff(staff_m: re.Match[str]) -> str:
        nonlocal n_restore, n_gap
        body = staff_m.group(0)
        if "<Measure" not in body:
            return body
        idx = 0
        prev = ""

        def fix_meas(mm: re.Match[str]) -> str:
            nonlocal idx, n_restore, n_gap, prev
            meas = mm.group(0)
            after_double = _double_bar(prev)
            if idx in _SWAPPED_LEADING_REST:
                before = meas
                meas = _restore_swapped_leading_rest(meas)
                if meas != before:
                    n_restore += 1
            if idx == 0 or after_double:
                before = meas
                meas = _gap_leading_rests(meas)
                if meas != before:
                    n_gap += 1
            prev = meas
            idx += 1
            return meas

        inner = MEASURE_RE.sub(fix_meas, body)
        return inner

    out = re.sub(
        r"<Staff id=\"\d+\">.*?</Staff>",
        fix_staff,
        mscx,
        flags=re.S,
    )
    return out, n_restore, n_gap


def _block_ticks(block: str, division: int) -> int:
    dt = re.search(r"<durationType>(.*?)</durationType>", block)
    if not dt:
        return 0
    base = _QUARTERS.get(dt.group(1).strip())
    if base is None:
        return 0
    dots_m = re.search(r"<dots>(\d+)</dots>", block)
    dots = int(dots_m.group(1)) if dots_m else (1 if "<dots>" in block else 0)
    add = base
    extra = Fraction(0)
    for _ in range(dots):
        add /= 2
        extra += add
    return int((base + extra) * division)


def _chord_lyric_plain(chord: str) -> str:
    ly = LYRICS_RE.search(chord)
    if ly is None:
        return ""
    t = TEXT_INNER_RE.search(ly.group(0))
    return _plain(t.group(1)) if t else ""


def _chord_syllabic(chord: str) -> str:
    ly = LYRICS_RE.search(chord)
    if ly is None:
        return "single"
    m = re.search(r"<syllabic>(.*?)</syllabic>", ly.group(0))
    return m.group(1).strip() if m else "single"


def _chord_midi(chord: str) -> str | None:
    m = re.search(r"<Note>.*?<pitch>(\d+)</pitch>", chord, re.S)
    return m.group(1) if m else None


def _chord_slur_starts(chord: str) -> bool:
    return bool(
        re.search(r'<Spanner type="Slur">(?:(?!</Spanner>).)*<next>', chord, re.S)
    )


def _set_chord_lyric_ticks(chord: str, ticks: int, division: int) -> str:
    ly_m = LYRICS_RE.search(chord)
    if ly_m is None:
        return chord
    ly = ly_m.group(0)
    ly = re.sub(r"\s*<ticks>.*?</ticks>", "", ly)
    ly = re.sub(r"\s*<ticks_f>.*?</ticks_f>", "", ly)
    if ticks > 0:
        fr = Fraction(ticks, division)
        ins = (
            f"\n              <ticks>{ticks}</ticks>"
            f"\n              <ticks_f>{fr.numerator}/{fr.denominator}</ticks_f>"
        )
        if "</syllabic>" in ly:
            ly = ly.replace("</syllabic>", "</syllabic>" + ins, 1)
        else:
            ly = ly.replace("<text>", ins + "\n              <text>", 1)
    return chord[: ly_m.start()] + ly + chord[ly_m.end() :]


def _melisma_ticks_for_blocks(blocks: list[str], division: int) -> tuple[list[str], int]:
    kinds: list[str] = []
    for b in blocks:
        if b.startswith("<Rest"):
            kinds.append("rest")
        elif _chord_lyric_plain(b):
            kinds.append("lyric")
        else:
            kinds.append("bare")
    out = list(blocks)
    n = 0
    for i, b in enumerate(blocks):
        if kinds[i] != "lyric":
            continue
        total = 0
        j = i + 1
        while j < len(blocks) and kinds[j] == "bare":
            total += _block_ticks(blocks[j], division)
            j += 1
        next_lyric = j < len(blocks) and kinds[j] == "lyric"
        syll = _chord_syllabic(b)
        key = _chord_midi(b)
        same = key is not None and all(
            _chord_midi(blocks[k]) == key for k in range(i + 1, j)
        )
        if syll in ("begin", "middle"):
            ticks = 0
        elif not next_lyric:
            ticks = total
        elif _chord_slur_starts(b) or not same:
            ticks = 0
        else:
            ticks = total
        new = _set_chord_lyric_ticks(b, ticks, division)
        if new != b:
            n += 1
            out[i] = new
    return out, n


def _strip_lyric_ticks(mscx: str) -> tuple[str, int]:
    n = len(re.findall(r"<ticks>.*?</ticks>", mscx))
    mscx = re.sub(r"\s*<ticks>.*?</ticks>", "", mscx)
    mscx = re.sub(r"\s*<ticks_f>.*?</ticks_f>", "", mscx)
    return mscx, n


def _apply_melisma_extenders(mscx: str) -> tuple[str, int]:
    dm = re.search(r"<Division>(\d+)</Division>", mscx)
    division = int(dm.group(1)) if dm else 480
    n_total = 0

    def fix_staff(staff_m: re.Match[str]) -> str:
        nonlocal n_total
        body = staff_m.group(0)
        measures = [m.group(0) for m in MEASURE_RE.finditer(body)]
        if not measures:
            return body
        nvoices = max(len(VOICE_RE.findall(m)) for m in measures)
        per: dict[tuple[int, int], list[str]] = defaultdict(list)
        for vi in range(nvoices):
            for mi, meas in enumerate(measures):
                voices = list(VOICE_RE.finditer(meas))
                if vi >= len(voices):
                    continue
                blocks = [
                    cr.group(0) for cr in CHORD_REST_RE.finditer(voices[vi].group(0))
                ]
                new_blocks, n = _melisma_ticks_for_blocks(blocks, division)
                n_total += n
                per[(mi, vi)] = new_blocks

        new_measures: list[str] = []
        for mi, meas in enumerate(measures):
            state = {"vi": 0}

            def fix_voice(vm: re.Match[str]) -> str:
                vi = state["vi"]
                state["vi"] += 1
                nb = per.get((mi, vi))
                if not nb:
                    return vm.group(0)
                it = iter(nb)
                return CHORD_REST_RE.sub(lambda _m: next(it), vm.group(0))

            new_measures.append(VOICE_RE.sub(fix_voice, meas))

        itm = iter(new_measures)
        return MEASURE_RE.sub(lambda _m: next(itm), body)

    out = re.sub(
        r'<Staff id="\d+">.*?</Staff>',
        fix_staff,
        mscx,
        flags=re.S,
    )
    return out, n_total


def _promote_composer(mscx: str, composer: str) -> tuple[str, str, list[str]]:
    notes: list[str] = []
    if not composer:
        for block in STAFF_TEXT_RE.findall(mscx):
            plain = _staff_plain(block)
            if plain and not _is_cue(plain):
                composer = plain
                notes.append(f"StaffText composer -> VBox: {plain!r}")
                break

    def keep_or_drop(m: re.Match[str]) -> str:
        plain = _staff_plain(m.group(0))
        if composer and plain == composer:
            return ""
        return m.group(0)

    before = mscx
    mscx = STAFF_TEXT_RE.sub(keep_or_drop, mscx)
    if mscx != before and composer and not any("composer -> VBox" in n for n in notes):
        notes.append(f"StaffText composer verwijderd: {composer!r}")
    return mscx, composer, notes


def apply_mscx(mscx: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    vbox_m = VBOX_RE.search(mscx)
    fields = _vbox_fields(vbox_m.group(0)) if vbox_m else {}

    title = _meta(mscx, "workTitle") or fields.get("title") or ""
    composer = _meta(mscx, "composer")
    cue = ""

    sub = fields.get("subtitle") or ""
    if _is_cue(sub):
        cue = sub
        notes.append(f"subtitle-cue -> StaffText: {cue[:60]!r}")
    mov = _meta(mscx, "movementTitle")
    if _is_cue(mov) and not cue:
        cue = re.sub(r"^P;", "P:", mov, count=1).strip()
        notes.append(f"movementTitle-cue -> StaffText: {cue[:60]!r}")

    mscx, composer, cnotes = _promote_composer(mscx, composer)
    notes.extend(cnotes)

    mscx = _set_meta(mscx, "composer", composer)
    mscx = _set_meta(mscx, "workTitle", title)
    if _is_cue(_meta(mscx, "movementTitle")):
        mscx = _set_meta(mscx, "movementTitle", "")
        notes.append("movementTitle (cue) leeggemaakt")

    new_vbox = _build_vbox(title, composer)
    if VBOX_RE.search(mscx):
        mscx = VBOX_RE.sub(new_vbox, mscx, count=1)
    else:
        staff = re.search(r'<Staff id="1">', mscx)
        if staff:
            ins = staff.end()
            mscx = mscx[:ins] + "\n" + new_vbox + mscx[ins:]
    notes.append(f"VBox title={title!r} composer={composer!r}")

    mscx = _strip_arial_on_stafftext(mscx)
    mscx, n_restore, n_gap = _fix_leading_rest_spacing(mscx)
    if n_restore:
        notes.append(f"leidende rust terug voor de noten: {n_restore} maten")
    if n_gap:
        notes.append(f"leidende rusten na dubbele streep/start: gap (geen kolom): {n_gap}")
    no_ext = bool(_meta(mscx, "vsaNoLyricExtenders"))
    if no_ext:
        mscx, n_strip = _strip_lyric_ticks(mscx)
        notes.append(f"lyric-underlines (ticks) verwijderd: {n_strip}")
    else:
        mscx, n_mel = _apply_melisma_extenders(mscx)
        if n_mel:
            notes.append(f"melisma-extenders (ticks): {n_mel}")

    if cue:
        mscx = _ensure_first_measure_stafftext(mscx, cue)

    return mscx, notes


def _pick_mscx_name(names: list[str]) -> str:
    top = [
        n
        for n in names
        if n.lower().endswith(".mscx") and "/" not in n and "\\" not in n
    ]
    if top:
        return top[0]
    nested = [n for n in names if n.lower().endswith(".mscx")]
    if not nested:
        raise FileNotFoundError("geen .mscx in het archief")
    return nested[0]


MUSESCORE_CANDIDATES = (
    Path(r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"),
    Path(r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"),
)


def find_musescore() -> Path:
    which = shutil.which("MuseScore4") or shutil.which("mscore") or shutil.which("MuseScore3")
    if which:
        return Path(which)
    for path in MUSESCORE_CANDIDATES:
        if path.is_file():
            return path
    raise SystemExit(
        "MuseScore niet gevonden (verwacht o.a. "
        r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe)"
    )


def musescore_convert(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    musescore = find_musescore()
    job = [{"in": str(src.resolve()), "out": [str(dest.resolve())]}]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump(job, fh)
        job_path = Path(fh.name)
    try:
        proc = subprocess.run(
            [str(musescore), "-j", str(job_path)],
            timeout=180,
        )
        if proc.returncode != 0 or not dest.is_file():
            subprocess.run(
                [str(musescore), "-f", "-o", str(dest), str(src)],
                check=True,
                timeout=180,
            )
    finally:
        job_path.unlink(missing_ok=True)
    if not dest.is_file():
        raise RuntimeError(f"MuseScore schreef geen {dest}")


def process_mscz(
    path: Path,
    *,
    extra_style: dict[str, str] | None = None,
    no_extenders: bool = False,
) -> list[str]:
    notes: list[str] = []
    with zipfile.ZipFile(path, "r") as zin:
        names = zin.namelist()
        mscx_name = _pick_mscx_name(names)
        mscx = zin.read(mscx_name).decode("utf-8")
        mss_name = "score_style.mss" if "score_style.mss" in names else None
        mss = zin.read(mss_name).decode("utf-8") if mss_name else ""
        others = {
            n: zin.read(n)
            for n in names
            if n != mscx_name and n != mss_name
        }

    if no_extenders:
        mscx = _set_meta(mscx, "vsaNoLyricExtenders", "1")
    new_mscx, mscx_notes = apply_mscx(mscx)
    notes.extend(mscx_notes)
    new_mss = overlay_style(mss, extra_style)
    notes.append("score_style.mss overlays toegepast")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        zout.writestr(mscx_name, new_mscx.encode("utf-8"))
        zout.writestr("score_style.mss", new_mss.encode("utf-8"))
        for n, data in others.items():
            zout.writestr(n, data)
    path.write_bytes(buf.getvalue())
    return notes


def main() -> int:
    p = argparse.ArgumentParser(description="A4-standaard-layout op .mscz (idempotent).")
    p.add_argument("mscz", type=Path, help=".mscz of opgekuiste .mxl")
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Doel-.mscz (verplicht bij .mxl-invoer; anders in-place)",
    )
    p.add_argument(
        "--no-extenders",
        action="store_true",
        help="Geen lyric-underlines (ticks); zet meta vsaNoLyricExtenders",
    )
    args = p.parse_args()
    src = args.mscz
    if not src.is_file():
        raise SystemExit(f"niet gevonden: {src}")
    suffix = src.suffix.lower()
    if suffix == ".mxl":
        dest = args.output if args.output is not None else src.with_suffix(".mscz")
        if dest.suffix.lower() != ".mscz":
            dest = dest / published_path(src.with_suffix(".mscz")).name
        dest = published_path(dest)
        require_no_spaces(dest)
        print(f"mxl -> mscz via MuseScore: {dest}")
        musescore_convert(src, dest)
        path = dest
    elif suffix == ".mscz":
        path = published_path(args.output) if args.output is not None else src
        require_no_spaces(path)
        if path != src:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(src.read_bytes())
    else:
        raise SystemExit("verwacht een .mscz of .mxl")
    if " " in src.name and suffix == ".mscz" and args.output is None:
        raise SystemExit(f"bestandsnaam mag geen spaties hebben: {src.name}")
    notes = process_mscz(path, no_extenders=args.no_extenders)
    print(f"ok {path}")
    for n in notes:
        print(f"  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
