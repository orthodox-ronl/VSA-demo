"""Pas de A4-standaard-layout toe op een MuseScore 4 .mscz (idempotent).

Contract: scripts/mscz-partituur-contract.md (was: mscz-partituur-contract.md /
mscz-layout-contract.md)
Laag 4 (PDF/A4). Lagen 1-3: cleanup_capella_mxl.py. Niet in check.

  python scripts/apply_mscz_layout.py pad\\naar\\file.mscz
  python scripts/apply_mscz_layout.py pad\\naar\\file.mxl -o uit.mscz

Publicatie-basispartituur: bij voorkeur onder
`oefenhoek/bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/` met
publicatiestam `{zangstuk}-{variant}-{uitvoeringsvorm}.mscz`
(`scripts/bibliotheek.py`). Bestandsnamen: geen spaties
(`scripts/score_filenames.py`). `.mxl` als invoer wordt via MuseScore naar
`.mscz` geconverteerd en daarna gelayout. Geen PDF of Coria-`.mxl`: dat is
`scripts\\mscz-products.cmd` na de editslag.

Copyright: notice uit de bron, of default CC BY-SA 4.0 (deze uitgave) plus
eredienst-kopieertoestemming. Standaard: korte footer (letterlijke notice op alle
pagina's) + colofon.
Contract: `scripts/mscz-partituur-contract.md`.

Opnieuw draaien is de bedoeling: style-overrides worden steeds gezet, titelvak
opnieuw opgebouwd. Lettergrepen op een noot die nog meerdere klinkergroepen
hebben (`melse` -> `mel` + `se`) worden gesplitst: extra noten met dezelfde
duur, SATB homofoon. Waar S een lettergreep heeft en T/B een langere noot
over die inzet heen, wordt die noot geknipt (zelfde toon, som van duren
gelijk) zodat elke partij per lettergreep minstens een noot heeft. Een lege
extra notenbalk (na SAT+B-import) verdwijnt. Overige pitches/slurs blijven.

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

from nl_hyphen import hyphenate_token, split_syllabic
from score_filenames import published_path, require_no_spaces, is_print_mscz
from bibliotheek import id_from_path, stem as bibliotheek_stem
from recite_collapse_mscx import collapse_recite_mscx, sync_measures_no_filler_rests

# A4 in inches (MuseScore pageWidth/pageHeight). 15 mm = 0.590551 in.
_A4_W = "8.26772"
_A4_H = "11.6929"
_M = "0.590551"
_PRINTABLE = "7.08662"  # A4_W - 2 * 15 mm

# Moet gelijk lopen met scripts/mscz-partituur-contract.md
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
    # 0 = laatste systeem altijd over de volle breedte (lyric-ruimte; zie partituur-contract)
    "lastSystemFillLimit": "0",
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
    # Lyrics: gecentreerd onder de noot; iets meer min. afstand zodat
    # ankerlettergreep en recite-tekst niet aan elkaar plakken.
    "lyricsOddAlign": "center,baseline",
    "lyricsEvenAlign": "center,baseline",
    "lyricsMinDistance": "0.6",
    "minNoteDistance": "0.5",
    "measureSpacing": "1.2",
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
    # Copyright-footer: letterlijke notice (niet $C/$c). $C = alleen pagina 1;
    # $c zou alle pagina's moeten doen, maar basispartituren bleven op $C hangen. Letterlijke
    # tekst in odd/even footer verschijnt op elke pagina. Colofon = VBox achteraan.
    # oddFooterC/evenFooterC worden in process_mscz gezet uit meta copyright.
    "showFooter": "1",
    "footerFirstPage": "1",
    "footerOddEven": "1",
    "oddFooterL": "",
    "oddFooterR": "",
    "evenFooterL": "",
    "evenFooterR": "",
    "footerFontFace": _FONT,
    "footerFontSize": "8",
    "footerFontSpatiumDependent": "0",
    "copyrightFontFace": _FONT,
    "copyrightFontSize": "8",
    "copyrightFontSpatiumDependent": "0",
}

_META_COPYRIGHT_FULL = "vsaCopyrightFull"
_META_BIBLIOTHEEK_ID = "vsaBibliotheekId"
_COLOPHON_TITLE = "Colofon"
_SEE_COLOPHON = "zie colofon"
_BIB_ID_LABEL = "Bibliotheek-id:"
_LITURGY_COPY = (
    "Voor gebruik in de orthodoxe eredienst is kopiëren toegestaan."
)
_VOW_SHORT = f"CC BY-SA 4.0 - orthodoxekerkmuziek.nl - {_SEE_COLOPHON}"
_VOW_FULL = (
    "Naamsvermelding - GelijkDelen 4.0 Internationaal (CC BY-SA 4.0)\n"
    "Bron: orthodoxekerkmuziek.nl\n"
    "Licentie: https://creativecommons.org/licenses/by-sa/4.0/\n"
    "Deze uitgave is aangepast (layout/opkuis) t.o.v. de bron; "
    "ShareAlike blijft van kracht.\n"
    f"{_LITURGY_COPY}"
)
_DEFAULT_SHORT = _VOW_SHORT
_DEFAULT_FULL = (
    "Naamsvermelding - GelijkDelen 4.0 Internationaal (CC BY-SA 4.0)\n"
    "Bron: deze uitgave (orthodoxekerkmuziek.nl / orthodox-ronl)\n"
    "Licentie: https://creativecommons.org/licenses/by-sa/4.0/\n"
    f"{_LITURGY_COPY}"
)
_DEFAULT_TEMPO_BPM = 120
_CONTRACT_VERSION = "partituur-1"
_CONTRACT_META = "vsaPartituurContract"
_CONTRACT_META_LEGACY = "vsaHubContract"
_COLOPHON_VBOX_RE = re.compile(
    r"[ \t]*<VBox>(?:(?!</VBox>).)*?"
    + re.escape(_COLOPHON_TITLE)
    + r"(?:(?!</VBox>).)*?</VBox>",
    re.S,
)

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


def extract_rights_from_mxl(path: Path) -> str:
    """Haal <rights> of MuseScore-achtige copyright uit een .mxl/.xml."""
    try:
        with zipfile.ZipFile(path, "r") as z:
            names = [
                n
                for n in z.namelist()
                if n.endswith(".xml") and not n.startswith("META")
            ]
            if not names:
                return ""
            text = z.read(names[0]).decode("utf-8", errors="replace")
    except zipfile.BadZipFile:
        text = path.read_text(encoding="utf-8", errors="replace")
    rights = [
        re.sub(r"<[^>]+>", "", m).strip()
        for m in re.findall(r"<rights\b[^>]*>(.*?)</rights>", text, re.S | re.I)
    ]
    rights = [r for r in rights if r]
    if rights:
        return rights[0]
    # Sommige exports zetten het al als credit-words type rights
    for m in re.finditer(
        r'<credit-type>\s*rights\s*</credit-type>\s*<credit-words[^>]*>(.*?)</credit-words>',
        text,
        re.S | re.I,
    ):
        plain = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if plain:
            return plain
    return ""


def _looks_like_vow_cc(text: str) -> bool:
    t = text.lower()
    return "cc by-sa" in t or "gelijkdelen" in t or "orthodoxekerkmuziek" in t


def _looks_like_short_footer(text: str) -> bool:
    return _SEE_COLOPHON in text.lower()


def _ensure_liturgy_copy(full: str) -> str:
    text = (full or "").strip()
    if _LITURGY_COPY.lower() in text.lower():
        return text
    if not text:
        return _LITURGY_COPY
    return f"{text}\n{_LITURGY_COPY}"


def format_copyright_notices(source_notice: str) -> tuple[str, str]:
    """(korte footer-tekst, volledige colofontekst).

    Lege bron -> default CC BY-SA 4.0 (deze uitgave). Altijd eredienst-zin
    in het colofon. Bibliotheek-id wordt apart toegevoegd via
    with_bibliotheek_id_line.
    """
    raw = (source_notice or "").strip()
    if not raw:
        return _DEFAULT_SHORT, _DEFAULT_FULL
    if _looks_like_vow_cc(raw):
        return _VOW_SHORT, _ensure_liturgy_copy(_VOW_FULL)
    if _looks_like_short_footer(raw):
        full = re.sub(r"\s*[·•-]\s*zie colofon\s*$", "", raw, flags=re.I).strip()
        short = raw if raw else full
        return short, _ensure_liturgy_copy(full or raw)
    short = raw
    if len(short) > 70:
        short = short[:67].rstrip(" ,;.-") + "…"
    short = f"{short} - {_SEE_COLOPHON}"
    return short, _ensure_liturgy_copy(raw)


def strip_bibliotheek_id_line(text: str) -> str:
    """Verwijder bestaande Bibliotheek-id-regels (idempotent herschrijven)."""
    cleaned = re.sub(
        rf"(?im)^\s*{re.escape(_BIB_ID_LABEL)}\s*.*$",
        "",
        text or "",
    )
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def with_bibliotheek_id_line(full_text: str, bibliotheek_id: str) -> str:
    """Zet of vervang de Bibliotheek-id-regel aan het eind van de colofontekst."""
    body = strip_bibliotheek_id_line(full_text)
    ident = (bibliotheek_id or "").strip()
    if not ident:
        return body
    line = f"{_BIB_ID_LABEL} {ident}"
    if not body:
        return line
    return f"{body}\n{line}"


def resolve_copyright_source(mscx: str, rights_hint: str = "") -> str:
    """Bronnotice voor deze representatie: full-meta, anders copyright, anders MXL-hint.

    Geen sibling-VOW of andere map raadplegen. Leeg = default CC BY-SA.
    Bibliotheek-id-regels in meta tellen niet als copyrightbron.
    """
    full = strip_bibliotheek_id_line(_meta(mscx, _META_COPYRIGHT_FULL))
    if full and not _looks_like_short_footer(full):
        return full
    cr = _meta(mscx, "copyright").strip()
    if cr and not _looks_like_short_footer(cr):
        return cr
    if full:
        return full
    if cr:
        return cr
    return (rights_hint or "").strip()


def _build_colophon_vbox(full_text: str) -> str:
    """Colofon-frame direct na de muziek; MuseScore plaatst het op dezelfde
    pagina als er ruimte is, anders op de volgende."""
    body = f"{_COLOPHON_TITLE}\n\n{full_text.strip()}"
    return "\n".join(
        [
            "      <VBox>",
            "        <height>8</height>",
            "        <boxAutoSize>1</boxAutoSize>",
            "        <topGap>8</topGap>",
            "        <bottomGap>2</bottomGap>",
            "        <Text>",
            "          <style>frame</style>",
            "          <align>left,top</align>",
            f"          <text>{_xml_text(body)}</text>",
            "          </Text>",
            "        </VBox>",
        ]
    )


def _strip_colophon_vbox(mscx: str) -> str:
    return _COLOPHON_VBOX_RE.sub("", mscx)


def _measure_staff(mscx: str, staff_id: str = "1") -> re.Match[str] | None:
    """Eerste `<Staff id>`-blok dat maten bevat (niet de Part-definitie)."""
    pat = re.compile(
        rf'<Staff id="{re.escape(staff_id)}">.*?</Staff>',
        re.S,
    )
    for m in pat.finditer(mscx):
        if "<Measure" in m.group(0):
            return m
    return None


def _strip_page_break_on_last_measure(mscx: str, staff_id: str = "1") -> str:
    """Verwijder gedwongen paginabreuk op de laatste maat (oude colofon-layout)."""
    staff = _measure_staff(mscx, staff_id)
    if staff is None:
        return mscx
    measures = list(re.finditer(r"<Measure\b[^>]*>.*?</Measure>", staff.group(0), re.S))
    if not measures:
        return mscx
    last = measures[-1]
    block = last.group(0)
    block2 = re.sub(
        r"\s*<LayoutBreak>\s*(?:<eid>[^<]*</eid>\s*)?<subtype>page</subtype>\s*"
        r"(?:<eid>[^<]*</eid>\s*)?</LayoutBreak>",
        "",
        block,
        count=1,
    )
    if block2 == block:
        return mscx
    abs_start = staff.start() + last.start()
    abs_end = staff.start() + last.end()
    return mscx[:abs_start] + block2 + mscx[abs_end:]


def _ensure_page_break_on_last_measure(mscx: str, staff_id: str = "1") -> str:
    """Verouderd: colofon gaat niet meer naar een aparte pagina.

    Behouden als no-op-helper voor eventuele callers; strip juist de breuk.
    """
    return _strip_page_break_on_last_measure(mscx, staff_id)


def _insert_colophon_after_staff1(mscx: str, full_text: str) -> str:
    mscx = _strip_colophon_vbox(mscx)
    if not full_text.strip():
        return mscx
    # Geen paginabreuk: VBox volgt op de laatste maat; past het niet, dan
    # laat MuseScore zelf een nieuwe pagina beginnen.
    mscx = _strip_page_break_on_last_measure(mscx, "1")
    vbox = _build_colophon_vbox(full_text)
    staff = _measure_staff(mscx, "1")
    if staff is None:
        return mscx
    # Vóór </Staff> van de maat-balk
    close = staff.end() - len("</Staff>")
    return mscx[:close] + vbox + "\n      " + mscx[close:]


def _ensure_visible_system_barlines(mscx: str) -> tuple[str, int]:
    """Maak verborgen BarLine-elementen weer zichtbaar (systeem-einden)."""
    n = 0

    def fix_bar(m: re.Match[str]) -> str:
        nonlocal n
        block = m.group(0)
        if re.search(r"<visible>\s*0\s*</visible>", block):
            n += 1
            return re.sub(
                r"<visible>\s*0\s*</visible>",
                "<visible>1</visible>",
                block,
                count=1,
            )
        return block

    return re.sub(r"<BarLine\b.*?</BarLine>", fix_bar, mscx, flags=re.S), n


def apply_copyright_notices(
    mscx: str,
    rights_hint: str = "",
    bibliotheek_id: str = "",
) -> tuple[str, list[str]]:
    """Footer kort + colofon; bronnotice of default CC BY-SA + eredienst-zin.

    bibliotheek_id: als gezet, colofonregel + meta vsaBibliotheekId.
    """
    notes: list[str] = []
    source = resolve_copyright_source(mscx, rights_hint)
    short, full = format_copyright_notices(source)
    ident = (bibliotheek_id or "").strip()
    if ident:
        full = with_bibliotheek_id_line(full, ident)
    if not source:
        notes.append("geen copyright in bron: default CC BY-SA 4.0 (deze uitgave)")
    mscx = _set_meta(mscx, "copyright", short)
    mscx = _set_meta(mscx, _META_COPYRIGHT_FULL, full)
    if ident:
        mscx = _set_meta(mscx, _META_BIBLIOTHEEK_ID, ident)
        notes.append(f"bibliotheek-id in colofon/meta={ident}")
    mscx = _insert_colophon_after_staff1(mscx, full)
    notes.append(f"copyright footer={short!r}")
    notes.append("colofon na laatste maat (zelfde pagina als er ruimte is)")
    return mscx, notes


def read_mscx_from_mscz(path: Path) -> str:
    """Lees de score-.mscx uit een .mscz-archief."""
    with zipfile.ZipFile(path, "r") as zin:
        mscx_name = _pick_mscx_name(zin.namelist())
        return zin.read(mscx_name).decode("utf-8")


def bibliotheek_id_status(path: Path, expected: str) -> tuple[bool, str]:
    """Of basispartituur-meta + colofon het verwachte bibliotheek-id hebben.

    Returns (ok, detail).
    """
    expected = (expected or "").strip()
    if not expected:
        return False, "geen verwacht bibliotheek-id"
    try:
        mscx = read_mscx_from_mscz(path)
    except (OSError, zipfile.BadZipFile, FileNotFoundError, KeyError) as exc:
        return False, f"kan .mscz niet lezen: {exc}"
    got_meta = _meta(mscx, _META_BIBLIOTHEEK_ID).strip()
    full = _meta(mscx, _META_COPYRIGHT_FULL)
    line_re = re.compile(
        rf"(?im)^\s*{re.escape(_BIB_ID_LABEL)}\s*{re.escape(expected)}\s*$"
    )
    has_line = bool(line_re.search(full)) or bool(line_re.search(mscx))
    if not has_line:
        # MuseScore/PDF mag tab i.p.v. spatie; accepteer ook inline.
        loose = re.compile(
            rf"{re.escape(_BIB_ID_LABEL)}\s*{re.escape(expected)}",
            re.I,
        )
        has_line = bool(loose.search(full)) or bool(loose.search(mscx))
    if got_meta == expected and has_line:
        return True, "ok"
    parts: list[str] = []
    if got_meta != expected:
        parts.append(f"meta={got_meta!r} (verwacht {expected!r})")
    if not has_line:
        parts.append("colofon mist Bibliotheek-id-regel")
    return False, "; ".join(parts)

def _has_tempo(mscx: str) -> bool:
    return bool(re.search(r"<Tempo\b", mscx))


def ensure_tempo(mscx: str, bpm: int = _DEFAULT_TEMPO_BPM) -> tuple[str, list[str]]:
    """Verplicht onzichtbaar tempo (BPM) voor Coria; default 120."""
    notes: list[str] = []
    if _has_tempo(mscx):
        notes.append("tempo aanwezig")
        return mscx, notes
    # MuseScore: <tempo> = kwartnoten per seconde
    bps = bpm / 60.0
    tempo_xml = (
        f"<Tempo>\n"
        f"            <tempo>{bps:.6f}</tempo>\n"
        f"            <followText>1</followText>\n"
        f"            <visible>0</visible>\n"
        f"            <text>&lt;sym&gt;metNoteQuarterUp&lt;/sym&gt; = {bpm}</text>\n"
        f"            </Tempo>\n          "
    )
    # Plaats vóór eerste Chord in Staff 1-matenblok
    staff = _measure_staff(mscx, "1")
    if staff is None:
        notes.append("tempo niet gezet: geen Staff 1")
        return mscx, notes
    body = staff.group(0)
    m = re.search(r"<Chord\b", body)
    if not m:
        notes.append("tempo niet gezet: geen Chord in Staff 1")
        return mscx, notes
    insert_at = staff.start() + m.start()
    mscx = mscx[:insert_at] + tempo_xml + mscx[insert_at:]
    notes.append(f"tempo ontbrak: onzichtbaar {bpm} BPM gezet")
    return mscx, notes


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


def copyright_footer_overrides(short: str) -> dict[str, str]:
    """Letterlijke korte notice in odd/even footer (zichtbaar op alle pagina's)."""
    esc = _xml_text((short or "").strip())
    return {"oddFooterC": esc, "evenFooterC": esc}


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
            # lambda: $ in copyright-tekst mag geen re.sub-backref worden
            mss = re.sub(pat, lambda _m, r=repl: r, mss, count=1, flags=re.S)
        else:
            mss = mss.replace(
                "</Style>",
                f"    <{tag}>{value}</{tag}>\n    </Style>",
                1,
            )
    return mss


def write_mscz_with_all_pages_footer(src: Path, dest: Path) -> str:
    """Kopieer .mscz naar dest met letterlijke copyright-footer op alle pagina's.

    Laat de bron-basispartituur ongemoeid (handig voor PDF-export). Returns de footertekst.
    """
    with zipfile.ZipFile(src, "r") as zin:
        names = zin.namelist()
        mscx_name = _pick_mscx_name(names)
        mscx = zin.read(mscx_name).decode("utf-8")
        mss = (
            zin.read("score_style.mss").decode("utf-8")
            if "score_style.mss" in names
            else ""
        )
        others = {
            n: zin.read(n)
            for n in names
            if n != mscx_name and n != "score_style.mss"
        }
    short = _meta(mscx, "copyright").strip()
    if not short:
        short = _VOW_SHORT
    new_mss = overlay_style(mss, copyright_footer_overrides(short))
    dest.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        zout.writestr(mscx_name, mscx.encode("utf-8"))
        zout.writestr("score_style.mss", new_mss.encode("utf-8"))
        for n, data in others.items():
            zout.writestr(n, data)
    dest.write_bytes(buf.getvalue())
    return short


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
        elif total <= 0:
            ticks = 0
        elif same:
            # Zelfde toon na de lettergreep: geen underline (Capella-padding;
            # frase-slurs zijn geen melisma).
            ticks = 0
        else:
            # Kale noten op andere toonhoogte = echte melisma.
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


def _frac_attr(fr: Fraction) -> str:
    return f"{fr.numerator}/{fr.denominator}"


def _event_quarters(block: str) -> Fraction:
    dt = re.search(r"<durationType>(.*?)</durationType>", block)
    if not dt:
        return Fraction(0)
    base = _QUARTERS.get(dt.group(1).strip())
    if base is None:
        return Fraction(0)
    dots_m = re.search(r"<dots>(\d+)</dots>", block)
    dots = int(dots_m.group(1)) if dots_m else 0
    add = base
    extra = Fraction(0)
    for _ in range(dots):
        add /= 2
        extra += add
    return base + extra


def _encode_duration(quarters: Fraction) -> tuple[str, int] | None:
    """(durationType, dots) of None als geen enkele MuseScore-duur past."""
    if quarters <= 0:
        return None
    for dots in (0, 1, 2):
        for name, base in _QUARTERS.items():
            total = base
            add = base
            for _ in range(dots):
                add /= 2
                total += add
            if total == quarters:
                return name, dots
    return None


def _set_event_duration(block: str, quarters: Fraction) -> str:
    enc = _encode_duration(quarters)
    if enc is None:
        raise ValueError(f"geen durationType voor {quarters} kwarten")
    name, dots = enc
    out = re.sub(
        r"<durationType>.*?</durationType>",
        f"<durationType>{name}</durationType>",
        block,
        count=1,
    )
    out = re.sub(r"\s*<dots>.*?</dots>", "", out)
    if dots:
        out = re.sub(
            r"(<durationType>.*?</durationType>)",
            rf"\1\n            <dots>{dots}</dots>",
            out,
            count=1,
        )
    return out


def _lyric_onset_times(voice: str) -> list[Fraction]:
    """Starttijden (in kwarten) van lettergreep-noten in een stem."""
    t = Fraction(0)
    onsets: list[Fraction] = []
    for ev in CHORD_REST_RE.finditer(voice):
        if ev.group(1) == "Chord" and _chord_lyric_plain(ev.group(0)):
            if not _in_tuplet(voice, ev.start()):
                onsets.append(t)
        t += _event_quarters(ev.group(0))
    return onsets


def _split_event_at_cuts(block: str, start: Fraction, end: Fraction, cuts: list[Fraction]) -> list[str]:
    points = [start, *cuts, end]
    pieces: list[str] = []
    for i, (a, b) in enumerate(zip(points, points[1:])):
        dur = b - a
        if dur <= 0:
            continue
        piece = block if i == 0 else _strip_eids(block)
        # Nooit feathered glyph vermenigvuldigen bij knippen
        piece = re.sub(r"\s*<headType>\w+</headType>", "", piece)
        piece = re.sub(r"\s*<noStem>[^<]*</noStem>", "", piece)
        piece = _set_event_duration(piece, dur)
        if i > 0:
            piece = LYRICS_RE.sub("", piece)
        pieces.append(piece)
    return pieces


def _split_voice_at_lyric_onsets(voice: str, onsets: list[Fraction]) -> tuple[str, int]:
    """Knip noten/rusten die over een lettergreep-inzet heen liggen."""
    if not onsets:
        return voice, 0
    onset_set = set(onsets)
    events = list(CHORD_REST_RE.finditer(voice))
    if not events:
        return voice, 0
    n_split = 0
    # Van achter naar voren, zodat indices geldig blijven.
    for ev in reversed(events):
        if _in_tuplet(voice, ev.start()):
            continue
        start = Fraction(0)
        for prev in events:
            if prev.start() >= ev.start():
                break
            start += _event_quarters(prev.group(0))
        dur = _event_quarters(ev.group(0))
        end = start + dur
        cuts = sorted(t for t in onset_set if start < t < end)
        if not cuts:
            continue
        try:
            pieces = _split_event_at_cuts(ev.group(0), start, end, cuts)
        except ValueError:
            continue
        if len(pieces) <= 1:
            continue
        voice = voice[: ev.start()] + "".join(pieces) + voice[ev.end() :]
        n_split += 1
    return voice, n_split


def _ensure_note_per_syllable(mscx: str) -> tuple[str, int]:
    """Elke partij: minstens een noot-inzet per lettergreep van de lead-stem.

    Lead = eerste stem van de bovenste muziekbalk (lyrics). Langere noten in
    andere stemmen die over zo'n inzet heen liggen, worden geknipt (zelfde
    toon; som van duren blijft gelijk). Idempotent.
    """
    staff_pat = re.compile(r'(<Staff id="\d+">)(.*?)(</Staff>)', re.S)
    staffs = [
        m
        for m in staff_pat.finditer(mscx)
        if MEASURE_RE.search(m.group(2))
    ]
    if not staffs:
        return mscx, 0

    inners = [list(MEASURE_RE.finditer(m.group(2))) for m in staffs]
    nmeas = min(len(x) for x in inners)
    total = 0

    new_inners: list[str] = []
    for si, sm in enumerate(staffs):
        body = sm.group(2)
        pieces: list[str] = []
        pos = 0
        for mi, mm in enumerate(inners[si]):
            pieces.append(body[pos : mm.start()])
            meas = mm.group(0)
            if mi < nmeas:
                lead = inners[0][mi].group(0)
                lead_voices = list(VOICE_RE.finditer(lead))
                onsets: list[Fraction] = []
                if lead_voices:
                    onsets = _lyric_onset_times(lead_voices[0].group(0))
                if onsets:
                    def fix_voice(vm: re.Match[str]) -> str:
                        nonlocal total
                        new_v, n = _split_voice_at_lyric_onsets(vm.group(0), onsets)
                        total += n
                        return new_v

                    meas = VOICE_RE.sub(fix_voice, meas)
            pieces.append(meas)
            pos = mm.end()
        pieces.append(body[pos:])
        new_inners.append("".join(pieces))

    out = mscx
    for sm, inner in zip(reversed(staffs), reversed(new_inners)):
        out = out[: sm.start()] + sm.group(1) + inner + sm.group(3) + out[sm.end() :]
    return out, total


def _in_tuplet(voice: str, pos: int) -> bool:
    before = voice[:pos]
    return before.count("<Tuplet>") > before.count("<endTuplet/>")


def _strip_eids(xml: str) -> str:
    return re.sub(r"\s*<eid>.*?</eid>", "", xml)


def _set_chord_lyric(chord: str, text: str, syllabic: str) -> str:
    ly_m = LYRICS_RE.search(chord)
    if ly_m is None:
        insert = (
            "            <Lyrics>\n"
            f"              <syllabic>{syllabic}</syllabic>\n"
            f"              <text>{_xml_text(text)}</text>\n"
            "              </Lyrics>\n"
        )
        return re.sub(r"<Note>", insert + "            <Note>", chord, count=1)
    block = ly_m.group(0)
    if "<syllabic>" in block:
        block = re.sub(
            r"<syllabic>.*?</syllabic>",
            f"<syllabic>{syllabic}</syllabic>",
            block,
            count=1,
        )
    else:
        block = block.replace(
            "<Lyrics>",
            f"<Lyrics>\n              <syllabic>{syllabic}</syllabic>",
            1,
        )
    block = re.sub(
        r"<text>.*?</text>",
        f"<text>{_xml_text(text)}</text>",
        block,
        count=1,
        flags=re.S,
    )
    return chord[: ly_m.start()] + block + chord[ly_m.end() :]


def _rewrite_measure_len(meas: str, wholes: Fraction) -> str:
    attr = _frac_attr(wholes)
    if re.match(r"<Measure\b[^>]*\blen=", meas):
        return re.sub(r'\blen="[^"]*"', f'len="{attr}"', meas, count=1)
    return re.sub(r"<Measure\b", f'<Measure len="{attr}"', meas, count=1)


def _split_voice_lyrics(
    voice: str,
    ops: list[tuple[int, list[str], str]],
    *,
    with_lyrics: bool,
) -> str:
    """Voeg kopie-akkoorden in; ops van achter naar voren (index blijft geldig)."""
    for idx, parts, orig_syll in reversed(ops):
        items = list(CHORD_REST_RE.finditer(voice))
        if idx >= len(items):
            continue
        hit = items[idx]
        if hit.group(1) != "Chord" or _in_tuplet(voice, hit.start()):
            continue
        src = hit.group(0)
        n = len(parts)
        first = src
        extras: list[str] = []
        if with_lyrics:
            first = _set_chord_lyric(
                src, parts[0], split_syllabic(orig_syll, 0, n)
            )
            for i in range(1, n):
                copy = _strip_eids(src)
                copy = _set_chord_lyric(
                    copy, parts[i], split_syllabic(orig_syll, i, n)
                )
                extras.append(copy)
        else:
            for _ in range(n - 1):
                extras.append(_strip_eids(src))
        voice = voice[: hit.start()] + first + "".join(extras) + voice[hit.end() :]
    return voice


def _split_undersplit_lyrics(mscx: str) -> tuple[str, int]:
    """Tokens met meerdere klinkergroepen -> extra noten (zelfde duur), SATB."""
    staff_pat = re.compile(r'(<Staff id="\d+">)(.*?)(</Staff>)', re.S)
    staffs = [
        m
        for m in staff_pat.finditer(mscx)
        if MEASURE_RE.search(m.group(2))
    ]
    if not staffs:
        return mscx, 0

    inners = [list(MEASURE_RE.finditer(m.group(2))) for m in staffs]
    nmeas = min(len(x) for x in inners)
    splits = 0

    new_inners: list[str] = []
    for si, sm in enumerate(staffs):
        body = sm.group(2)
        pieces: list[str] = []
        pos = 0
        for mi, mm in enumerate(inners[si]):
            pieces.append(body[pos : mm.start()])
            meas = mm.group(0)
            if mi < nmeas:
                lead = inners[0][mi].group(0)
                lead_voices = list(VOICE_RE.finditer(lead))
                ops: list[tuple[int, list[str], str]] = []
                if lead_voices:
                    v0 = lead_voices[0].group(0)
                    events = list(CHORD_REST_RE.finditer(v0))
                    for i, ev in enumerate(events):
                        if ev.group(1) != "Chord" or _in_tuplet(v0, ev.start()):
                            continue
                        chord = ev.group(0)
                        # Basispartituur ||O|| niet splitsen — recite-collaps beheert die tekst.
                        if "<headType>breve</headType>" in chord and (
                            "<noStem>1</noStem>" in chord or "<noStem>true</noStem>" in chord
                        ):
                            continue
                        raw = _chord_lyric_plain(chord)
                        if not raw:
                            continue
                        # Multi-woord recite-tekst niet via hyphenate_token uit elkaar trekken
                        if " " in raw.strip():
                            continue
                        parts = hyphenate_token(raw)
                        if len(parts) <= 1:
                            continue
                        ops.append((i, parts, _chord_syllabic(chord)))
                if ops:
                    vi = 0

                    def fix_voice(vm: re.Match[str]) -> str:
                        nonlocal vi
                        with_ly = si == 0 and vi == 0
                        vi += 1
                        return _split_voice_lyrics(
                            vm.group(0), ops, with_lyrics=with_ly
                        )

                    meas = VOICE_RE.sub(fix_voice, meas)
                    v1 = VOICE_RE.search(meas)
                    if v1 is not None:
                        q = sum(
                            _event_quarters(ev.group(0))
                            for ev in CHORD_REST_RE.finditer(v1.group(0))
                        )
                        if q > 0:
                            meas = _rewrite_measure_len(meas, q / 4)
                    if si == 0:
                        splits += len(ops)
            pieces.append(meas)
            pos = mm.end()
        pieces.append(body[pos:])
        new_inners.append("".join(pieces))

    out = mscx
    for sm, inner in zip(reversed(staffs), reversed(new_inners)):
        out = out[: sm.start()] + sm.group(1) + inner + sm.group(3) + out[sm.end() :]
    return out, splits


def apply_mscx(
    mscx: str,
    rights_hint: str = "",
    bibliotheek_id: str = "",
) -> tuple[str, list[str]]:
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
        # Alleen het eerste (titel-)VBox; colofon volgt later opnieuw
        mscx = VBOX_RE.sub(new_vbox, mscx, count=1)
    else:
        staff = _measure_staff(mscx, "1")
        if staff:
            open_end = mscx.find(">", staff.start()) + 1
            mscx = mscx[:open_end] + "\n" + new_vbox + mscx[open_end:]
    notes.append(f"VBox title={title!r} composer={composer!r}")

    mscx = _strip_arial_on_stafftext(mscx)
    mscx, n_restore, n_gap = _fix_leading_rest_spacing(mscx)
    if n_restore:
        notes.append(f"leidende rust terug voor de noten: {n_restore} maten")
    if n_gap:
        notes.append(f"leidende rusten na dubbele streep/start: gap (geen kolom): {n_gap}")

    # Reciteer eerst; lyric-underlines daarna. Capella-slurs zijn frasen, geen
    # melisma — default: ticks wissen, niet opnieuw zetten (voorkomt God,/ke,-lijnen).
    mscx, n_recite = collapse_recite_mscx(mscx)
    if n_recite:
        notes.append(f"reciteer-collaps (eerste+||O||+laatste): {n_recite} reeksen")

    mscx, n_trim = sync_measures_no_filler_rests(mscx)
    if n_trim:
        notes.append(f"opvulrusten verwijderd: {n_trim}")

    mscx, n_bar = _ensure_visible_system_barlines(mscx)
    if n_bar:
        notes.append(f"maatstrepen zichtbaar gemaakt: {n_bar}")

    mscx, n_strip = _strip_lyric_ticks(mscx)
    no_ext = bool(_meta(mscx, "vsaNoLyricExtenders"))
    want_ext = bool(_meta(mscx, "vsaLyricExtenders")) and not no_ext
    if want_ext:
        mscx, n_mel = _apply_melisma_extenders(mscx)
        notes.append(f"melisma-extenders (ticks): {n_mel}")
    elif n_strip:
        notes.append(f"lyric-underlines (ticks) verwijderd: {n_strip}")

    if cue:
        mscx = _ensure_first_measure_stafftext(mscx, cue)

    mscx, tnotes = ensure_tempo(mscx)
    notes.extend(tnotes)

    mscx, cnotes = apply_copyright_notices(
        mscx, rights_hint=rights_hint, bibliotheek_id=bibliotheek_id
    )
    notes.extend(cnotes)

    mscx = _set_meta(mscx, _CONTRACT_META, _CONTRACT_VERSION)
    notes.append(f"partituur-contract {_CONTRACT_VERSION}")

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


def _strip_empty_staves(mscx: str) -> tuple[str, int]:
    """Verwijder maat-balken zonder noten (Capella SAT+B -> SA/TB + lege 3e balk).

    Part-definities (`<Staff id>` zonder `<Measure>`) zijn geen lege balken:
    die mogen nooit de reden zijn om een id te droppen, anders verdwijnt de
    hele partituur (VOW e.d.).
    """
    score_pat = re.compile(r'<Staff id="(\d+)">.*?</Staff>', re.S)
    hits = list(score_pat.finditer(mscx))
    measure_hits = [m for m in hits if "<Measure" in m.group(0)]
    if len(measure_hits) < 2:
        return mscx, 0
    drop_ids: set[int] = set()
    keep: list[tuple[int, str]] = []
    for m in measure_hits:
        sid = int(m.group(1))
        block = m.group(0)
        empty = "<Chord" not in block and "<Note" not in block
        if empty:
            drop_ids.add(sid)
        else:
            keep.append((sid, block))
    if not drop_ids or not keep:
        return mscx, 0

    mapping = {old: i + 1 for i, (old, _) in enumerate(keep)}
    n_keep = len(keep)
    pieces: list[str] = []
    pos = 0
    for m in hits:
        pieces.append(mscx[pos : m.start()])
        sid = int(m.group(1))
        if sid not in drop_ids:
            block = m.group(0)
            new_id = mapping.get(sid, sid)
            if new_id != sid:
                block = re.sub(
                    rf'<Staff id="{sid}">',
                    f'<Staff id="{new_id}">',
                    block,
                    count=1,
                )
            pieces.append(block)
        pos = m.end()
    pieces.append(mscx[pos:])
    out = "".join(pieces)

    def fix_part(pm: re.Match[str]) -> str:
        head, inner, tail = pm.group(1), pm.group(2), pm.group(3)
        defs = list(re.finditer(r"<Staff>.*?</Staff>\s*", inner, re.S))
        if not defs:
            return pm.group(0)
        buf: list[str] = []
        p0 = 0
        for i, d in enumerate(defs):
            buf.append(inner[p0 : d.start()])
            if (i + 1) not in drop_ids:
                buf.append(d.group(0))
            p0 = d.end()
        buf.append(inner[p0:])
        inner = "".join(buf)
        inner = re.sub(
            r'(<bracket\b[^>]*\bspan=")(\d+)(")',
            lambda bm: f"{bm.group(1)}{n_keep}{bm.group(3)}",
            inner,
            count=1,
        )
        return head + inner + tail

    out = re.sub(
        r"(<Part(?:\s[^>]*)?>)(.*?)(</Part>)",
        fix_part,
        out,
        count=1,
        flags=re.S,
    )
    return out, len(drop_ids)


def process_mscz(
    path: Path,
    *,
    extra_style: dict[str, str] | None = None,
    no_extenders: bool = False,
    rights_hint: str = "",
    bibliotheek_id: str = "",
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
    mscx, n_empty = _strip_empty_staves(mscx)
    mscx, n_split = _split_undersplit_lyrics(mscx)
    mscx, n_syll = _ensure_note_per_syllable(mscx)
    ident = (bibliotheek_id or "").strip() or (id_from_path(path) or "")
    new_mscx, mscx_notes = apply_mscx(
        mscx, rights_hint=rights_hint, bibliotheek_id=ident
    )
    if n_syll:
        mscx_notes.insert(0, f"noten per lettergreep geknipt: {n_syll}")
    if n_split:
        mscx_notes.insert(0, f"lettergrepen gesplitst: {n_split}")
    if n_empty:
        mscx_notes.insert(0, f"lege notenbalken verwijderd: {n_empty}")
    notes.extend(mscx_notes)
    short = _meta(new_mscx, "copyright").strip()
    style_extra = dict(extra_style or {})
    if short:
        style_extra.update(copyright_footer_overrides(short))
    new_mss = overlay_style(mss, style_extra)
    notes.append("score_style.mss overlays toegepast")
    if short:
        notes.append(f"footer alle pagina's (letterlijk)={short!r}")

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
    p.add_argument(
        "--id",
        dest="bibliotheek_id",
        default="",
        help="Bibliotheek-id (zangstuk/variant/uitvoeringsvorm); "
        "default: afleiden uit pad onder bibliotheek/",
    )
    args = p.parse_args()
    src = args.mscz
    if not src.is_file():
        raise SystemExit(f"niet gevonden: {src}")
    if is_print_mscz(src):
        raise SystemExit(
            f"print-.mscz hoort niet in apply_mscz_layout: {src.name}\n"
            r"Hernoem naar gewone .mscz (basispartituur) of bewerk alleen in MuseScore; "
            r"zie handleiding partituur/7-print-mscz."
        )
    suffix = src.suffix.lower()
    rights_hint = ""
    if suffix == ".mxl":
        rights_hint = extract_rights_from_mxl(src)
        dest = args.output if args.output is not None else src.with_suffix(".mscz")
        if dest.suffix.lower() != ".mscz":
            dest = dest / published_path(src.with_suffix(".mscz")).name
        dest = published_path(dest)
        require_no_spaces(dest)
        if is_print_mscz(dest):
            raise SystemExit(
                f"doel mag geen print-.mscz zijn: {dest.name}"
            )
        print(f"mxl -> mscz via MuseScore: {dest}")
        musescore_convert(src, dest)
        path = dest
    elif suffix == ".mscz":
        path = published_path(args.output) if args.output is not None else src
        require_no_spaces(path)
        if is_print_mscz(path):
            raise SystemExit(
                f"doel mag geen print-.mscz zijn: {path.name}"
            )
        if path != src:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(src.read_bytes())
    else:
        raise SystemExit("verwacht een .mscz of .mxl")
    if " " in src.name and suffix == ".mscz" and args.output is None:
        raise SystemExit(f"bestandsnaam mag geen spaties hebben: {src.name}")
    ident = (args.bibliotheek_id or "").strip() or (id_from_path(path) or "")
    if ident:
        expected = f"{bibliotheek_stem(ident)}.mscz"
        if path.name != expected:
            print(
                f"waarschuwing: bibliotheek-map {ident} verwacht bestandsnaam "
                f"{expected}, kreeg {path.name}",
                flush=True,
            )
    notes = process_mscz(
        path,
        no_extenders=args.no_extenders,
        rights_hint=rights_hint,
        bibliotheek_id=ident,
    )
    if ident:
        notes.append(f"bibliotheek-id={ident}")
    print(f"ok {path}")
    for n in notes:
        print(f"  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
