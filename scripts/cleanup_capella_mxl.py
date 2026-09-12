"""Capella/CapToMusic-MXL: inhoudelijke opkuis naar een MuseScore-uitgangspunt.

Dit is geen alles-in-een 'maak het mooi in MuseScore'. Er zijn lagen.
Zie ook VSA `reciting-mode: quarters` en MusicXML-profielen playback/engraving
in VSA-tooling (docs/specification/rendering.md).

----------------------------------------------------------------------
Laag 1 - Capella-semantiek (wat de XML bedoelde)
----------------------------------------------------------------------
Onzichtbare klinkende noten (`print-object=no`) zijn reciteerkwarten: extra
lettergrepen op dezelfde toon, al als kwart gecodeerd. Zichtbaar maken
zonder de duur of het noottype te veranderen.

Een maat is hier geen metrische waarheid (`senza-misura`). Maatlengte mag
groeien als er lettergrepen bijkomen. Halve/hele noten op cadensen blijven
halve/hele noten (echte melodische lengte, geen recitatief-dummy).

----------------------------------------------------------------------
Laag 2 - Tekst-noot-binding
----------------------------------------------------------------------
- Een lettergreep <-> een noot (recitatief: een kwart).
- Meerdere lettergrepen op een token (`koninkrijk`, `aanbidden`): extra
  noten INVOEGEN met dezelfde duur als het origineel (blijven kwarten),
  niet de originele kwart in triolen/achten/16en knippen.
- Melisma: bestaande langere noten of noten zonder tekst houden.
  Lyric-extender (`<extend/>`) alleen als die extra noten niet onder een
  slur vanaf de lettergreep vallen (Capella-slur = frase/doorgangsnoot;
  een underline onder Hei-li-ge hoort daar niet). Geen extender op
  begin/middle (koppelteken bindt het woord al).
- Recitatief: hele woorden (`altijd`, `eeuwen`) in lettergrepen hakken
  en per lettergreep een noot (zelfde duur, geen triolen).
- Lyrics alleen op stem 1, tussen de twee notenbalken (niet onder de bas,
  niet per stem herhaald). SATB blijft homofoon in de noten.
- Extra noten op alle stemmen op dezelfde index; daarna ``<backup>``
  bijwerken (anders start A/T/B in MuseScore 2/4/6 noten te laat).
- Geen partijnamen (SATB) op elk systeem.
- Titels uit staff-tekst naar work-title/credit; boekpagina-cijfers weg.
- Geen maten die alleen rusten of helemaal leeg zijn (Capella-maat 0).

----------------------------------------------------------------------
Laag 3 - Partituurhint (MXL als start voor .mscz)
----------------------------------------------------------------------
Compacte systeem- en balkafstand; geen extra eerste-systeem-inspring in de
XML. 'Laatste pagina niet uitzetten' is grotendeels MuseScore-stijl
(last-system-fill / max system distance), niet betrouwbaar in MusicXML.

----------------------------------------------------------------------
Laag 4 - .mscz -> PDF en later MXL voor Coria
----------------------------------------------------------------------
`scripts/apply_mscz_layout.py` + `scripts/mscz-layout-contract.md`.
Het opgekuiste MXL is het importbestand; daarna A4-layout op het .mscz.
Coria-MXL vanuit dat .mscz: `scripts/export_mscz_coria_mxl.py`
(`[PAUZE]` na dubbele streep, kwart-rust na gebogen cesuur).

Publicatiebestanden: geen spaties in de naam (`scripts/score_filenames.py`).
Capella-input in `oefenhoek/input/` mag spaties houden; schrijf opgekuiste
uitvoer met `-o` naar een naam zonder spaties. In-place op een naam mét
spaties is geweigerd.

Gebruik:
  python scripts/cleanup_capella_mxl.py pad\\naar\\file.mxl
  python scripts/cleanup_capella_mxl.py pad\\naar\\file.mxl -o uit.mxl
"""
from __future__ import annotations

import argparse
import copy
import io
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

from score_filenames import published_path, require_no_spaces

# Handmatige splitsing voor liturgische woorden die de naive regel mist
# of verkeerd zou doen. Alleen de stam, zonder leestekens.
HYPHEN_EXCEPTIONS: dict[str, str] = {
    "altijd": "al-tijd",
    "eeuwen": "eeuw-en",
    "aanbidden": "aan-bid-den",
    "aanschouwen": "aan-schou-wen",
    "aarde": "aar-de",
    "allerlei": "al-ler-lei",
    "barmhartigheid": "barm-har-tig-heid",
    "barmhartigen": "barm-har-ti-gen",
    "dorsten": "dors-ten",
    "gedenk": "ge-denk",
    "gekomen": "ge-ko-men",
    "geschieden": "ge-schie-den",
    "heilige": "hei-li-ge",
    "hongeren": "hon-ge-ren",
    "kinderen": "kin-de-ren",
    "koninkrijk": "ko-nink-rijk",
    "lasterlijk": "las-ter-lijk",
    "nedervallen": "ne-der-val-len",
    "opgestaan": "op-ge-staan",
    "treurenden": "treu-ren-den",
    "vader": "va-der",
    "verheugt": "ver-heugt",
    "vervolgd": "ver-volgd",
    "vredestichters": "vre-de-stich-ters",
    "wanneer": "wan-neer",
    "wonderbaar": "won-der-baar",
    "worden": "wor-den",
    "zachtmoedigen": "zacht-moe-di-gen",
    "zalig": "za-lig",
    "zingen": "zin-gen",
    "zullen": "zul-len",
}

VOWELS = "aeiouyáéíóúàèëïöü"
DIPHTHONGS = (
    "aa", "ee", "oo", "uu", "ie", "ei", "ij", "ou", "au", "ui", "eu", "oe",
)
# Niet splitsen midden in deze clusters (VC-CV zou ch/ng stukmaken).
_CONS_KEEP = ("sch", "ch", "ng", "nk")


def local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if local(c.tag) == name:
            return c
    return None


def children(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if local(c.tag) == name]


def findall(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el.iter() if local(c.tag) == name]


def strip_punct(token: str) -> tuple[str, str, str]:
    m = re.match(r"^(\W*)(.*?)(\W*)$", token, flags=re.U)
    if not m:
        return "", token, ""
    return m.group(1), m.group(2), m.group(3)


def _letter_units(stem: str) -> list[tuple[str, int, int]]:
    """('v'|'c', start, end) met tweeklanken als een klinker."""
    w = stem.lower()
    units: list[tuple[str, int, int]] = []
    i = 0
    while i < len(w):
        if w[i : i + 2] in DIPHTHONGS:
            units.append(("v", i, i + 2))
            i += 2
        elif w[i] in VOWELS:
            units.append(("v", i, i + 1))
            i += 1
        else:
            j = i
            while (
                j < len(w)
                and w[j] not in VOWELS
                and w[j : j + 2] not in DIPHTHONGS
            ):
                j += 1
            units.append(("c", i, j))
            i = j
    return units


def naive_hyphen(stem: str) -> list[str]:
    """Eenvoudige NL-splitsing: prefix, dubbele cons, V-CV / VC-CV."""
    w = stem.lower()
    if len(w) < 4:
        return [stem]
    prefixes = (
        "neder",
        "achter",
        "onder",
        "over",
        "voor",
        "aarts",
        "ge",
        "be",
        "ver",
        "ont",
        "aan",
        "her",
        "neer",
        "op",
        "uit",
        "toe",
        "mis",
        "wan",
    )
    for pref in prefixes:
        if w.startswith(pref) and len(w) - len(pref) >= 3:
            rest = stem[len(pref) :]
            return _restore_case(stem[: len(pref)], stem) + naive_hyphen(rest)

    # identieke medeklinkers: zul-len, bid-den
    m = re.search(r"([^aeiouyáéíóúàèëïöü])\1", w)
    if m and 0 < m.start() < len(w) - 1:
        i = m.start() + 1
        return _restore_case(stem[:i], stem) + naive_hyphen(stem[i:])

    units = _letter_units(stem)
    for i in range(len(units) - 2):
        kind0, _, _ = units[i]
        kind1, c0, c1 = units[i + 1]
        kind2, _, _ = units[i + 2]
        if kind0 != "v" or kind1 != "c" or kind2 != "v":
            continue
        cluster = w[c0:c1]
        if cluster in _CONS_KEEP or len(cluster) == 1:
            cut = c0
        else:
            cut = c0 + 1
        if 0 < cut < len(stem):
            return _restore_case(stem[:cut], stem) + naive_hyphen(stem[cut:])
    return [stem]


def _restore_case(part: str, original: str) -> list[str]:
    if original.isupper():
        return [part.upper()]
    if original[:1].isupper():
        return [part[:1].upper() + part[1:].lower()]
    return [part]


def hyphenate_token(token: str) -> list[str]:
    raw = (token or "").replace("\xa0", " ").strip()
    if not raw:
        return []
    lead, stem, trail = strip_punct(raw)
    if not stem:
        return [raw]
    key = stem.lower()
    if key in HYPHEN_EXCEPTIONS:
        parts = HYPHEN_EXCEPTIONS[key].split("-")
        parts = _apply_case(parts, stem)
    else:
        groups = re.findall(rf"[{VOWELS}]+", stem, flags=re.I)
        if len(groups) < 2 or len(stem) < 4:
            return [raw]
        parts = naive_hyphen(stem)
        if len(parts) == 1:
            return [raw]
    if lead:
        parts[0] = lead + parts[0]
    if trail:
        parts[-1] = parts[-1] + trail
    return parts


def _apply_case(parts: list[str], stem: str) -> list[str]:
    if stem.isupper():
        return [p.upper() for p in parts]
    if stem[:1].isupper():
        out = [p.lower() for p in parts]
        out[0] = out[0][:1].upper() + out[0][1:]
        return out
    return [p.lower() for p in parts]


def set_text(el: ET.Element | None, value: str) -> None:
    if el is not None:
        el.text = value


def note_duration(note: ET.Element) -> int:
    d = child(note, "duration")
    return int(d.text) if d is not None and d.text else 0


def is_rest(note: ET.Element) -> bool:
    return child(note, "rest") is not None


def is_chord(note: ET.Element) -> bool:
    return child(note, "chord") is not None


def is_pitched(note: ET.Element) -> bool:
    return child(note, "pitch") is not None


def lyric_elements(note: ET.Element) -> list[ET.Element]:
    return children(note, "lyric")


def set_lyric_syllables(note: ET.Element, text: str, syllabic: str) -> None:
    lys = lyric_elements(note)
    if not lys:
        ly = ET.Element("lyric", {"number": "1", "default-y": "-80"})
        ET.SubElement(ly, "syllabic").text = syllabic
        ET.SubElement(ly, "text").text = text
        note.append(ly)
        return
    ly = lys[0]
    ly.set("default-y", "-80")
    syll = child(ly, "syllabic")
    txt = child(ly, "text")
    if syll is None:
        syll = ET.Element("syllabic")
        ly.insert(0, syll)
    syll.text = syllabic
    if txt is None:
        txt = ET.SubElement(ly, "text")
    txt.text = text


def clear_lyrics(note: ET.Element) -> None:
    for ly in lyric_elements(note):
        note.remove(ly)


def replicate_note(
    note: ET.Element,
    n: int,
    parts: list[str] | None = None,
) -> list[ET.Element]:
    """N kopieen van dezelfde noot (zelfde duur en type). Geen triolen."""
    if n <= 1:
        if parts:
            set_lyric_syllables(note, parts[0], "single")
        return [note]
    out = [note]
    for _ in range(n - 1):
        out.append(copy.deepcopy(note))
    for i, el in enumerate(out):
        el.attrib.pop("print-object", None)
        tm = child(el, "time-modification")
        if tm is not None:
            el.remove(tm)
        for beam in children(el, "beam"):
            el.remove(beam)
        if parts:
            if i == 0:
                syll = "begin"
            elif i == n - 1:
                syll = "end"
            else:
                syll = "middle"
            set_lyric_syllables(el, parts[i], syll)
        else:
            clear_lyrics(el)
        if i > 0:
            notations = child(el, "notations")
            if notations is not None:
                for sl in [s for s in list(notations) if local(s.tag) == "slur"]:
                    notations.remove(sl)
                if len(list(notations)) == 0:
                    el.remove(notations)
    return out


def notes_by_voice(measure: ET.Element) -> dict[str, list[ET.Element]]:
    voices: dict[str, list[ET.Element]] = {}
    for el in measure:
        if local(el.tag) != "note" or is_chord(el):
            continue
        v = child(el, "voice")
        vid = v.text if v is not None and v.text else "1"
        voices.setdefault(vid, []).append(el)
    return voices


def replace_note_with_sequence(measure: ET.Element, old: ET.Element, new_notes: list[ET.Element]) -> None:
    kids = list(measure)
    idx = kids.index(old)
    measure.remove(old)
    for i, n in enumerate(new_notes):
        measure.insert(idx + i, n)


def fix_backups_in_measure(measure: ET.Element) -> None:
    """Zet backup-duur op de som van de noten sinds de vorige backup/maatstart."""
    chunk = 0
    for el in measure:
        ln = local(el.tag)
        if ln == "note" and child(el, "chord") is None:
            chunk += note_duration(el)
        elif ln == "backup":
            d = child(el, "duration")
            if d is not None:
                d.text = str(chunk)
            chunk = 0
        elif ln == "forward":
            d = child(el, "duration")
            if d is not None and d.text:
                chunk += int(d.text)


def unhide_pitched_notes(root: ET.Element) -> int:
    n = 0
    for note in findall(root, "note"):
        if note.get("print-object") == "no" and is_pitched(note):
            del note.attrib["print-object"]
            n += 1
    return n


def remove_page_number_directions(root: ET.Element) -> int:
    removed = 0
    for parent in root.iter():
        for el in list(parent):
            if local(el.tag) != "direction":
                continue
            words = [w for w in findall(el, "words") if (w.text or "").strip()]
            if not words:
                continue
            if all(re.fullmatch(r"\d+", (w.text or "").strip()) for w in words):
                parent.remove(el)
                removed += 1
    return removed


def promote_titles(root: ET.Element) -> tuple[str | None, str | None]:
    title = None
    subtitle = None
    title_dirs: list[tuple[ET.Element, ET.Element]] = []
    sub_dirs: list[tuple[ET.Element, ET.Element]] = []
    for parent in root.iter():
        for el in list(parent):
            if local(el.tag) != "direction":
                continue
            for w in findall(el, "words"):
                text = (w.text or "").strip()
                if not text:
                    continue
                size = float(w.get("font-size") or "0")
                if size >= 18 and title is None:
                    title = re.sub(r"\s+", " ", text)
                    title_dirs.append((parent, el))
                elif 12 <= size < 18 and subtitle is None and not re.fullmatch(r"\d+", text):
                    # korte ondertitel / toon / (zondag)
                    if len(text) <= 80:
                        subtitle = re.sub(r"\s+", " ", text)
                        sub_dirs.append((parent, el))
    for parent, el in title_dirs + sub_dirs:
        if el in list(parent):
            parent.remove(el)

    if title:
        work = child(root, "work")
        if work is None:
            work = ET.Element("work")
            root.insert(0, work)
        wt = child(work, "work-title")
        if wt is None:
            wt = ET.SubElement(work, "work-title")
        wt.text = title
        if subtitle:
            mt = child(root, "movement-title")
            if mt is None:
                ident = child(root, "identification")
                idx = list(root).index(ident) + 1 if ident is not None else 1
                mt = ET.Element("movement-title")
                mt.text = subtitle
                root.insert(idx, mt)
            else:
                mt.text = subtitle

        # vervang lege credits
        for cr in list(children(root, "credit")):
            words = "".join((w.text or "") for w in findall(cr, "credit-words")).strip()
            if not words:
                root.remove(cr)
        credit = ET.Element("credit", {"page": "1"})
        ET.SubElement(credit, "credit-type").text = "title"
        cw = ET.SubElement(
            credit,
            "credit-words",
            {
                "default-x": "590",
                "default-y": "1600",
                "justify": "center",
                "valign": "top",
                "font-size": "22",
                "font-family": "Arial",
            },
        )
        cw.text = title
        ident = child(root, "identification")
        defaults = child(root, "defaults")
        if defaults is not None:
            idx = list(root).index(defaults) + 1
        elif ident is not None:
            idx = list(root).index(ident) + 1
        else:
            idx = 1
        root.insert(idx, credit)
        if subtitle:
            credit2 = ET.Element("credit", {"page": "1"})
            ET.SubElement(credit2, "credit-type").text = "subtitle"
            cw2 = ET.SubElement(
                credit2,
                "credit-words",
                {
                    "default-x": "590",
                    "default-y": "1550",
                    "justify": "center",
                    "valign": "top",
                    "font-size": "14",
                    "font-family": "Arial",
                    "font-style": "italic",
                },
            )
            cw2.text = subtitle
            root.insert(idx + 1, credit2)
    return title, subtitle


def hide_part_name(root: ET.Element) -> None:
    for sp in findall(root, "score-part"):
        pn = child(sp, "part-name")
        if pn is not None:
            pn.text = None
            pn.set("print-object", "no")
        pa = child(sp, "part-abbreviation")
        if pa is not None:
            pa.text = None
            pa.set("print-object", "no")


def split_lyrics_keep_quarters(root: ET.Element) -> int:
    """Split tokens op stem 1; zelfde extra noten op dezelfde index in A/T/B."""
    splits = 0
    for part in [c for c in root if local(c.tag) == "part"]:
        for measure in children(part, "measure"):
            voices = notes_by_voice(measure)
            v1 = voices.get("1", [])
            ops: list[tuple[int, list[str]]] = []
            for i, note in enumerate(v1):
                lys = lyric_elements(note)
                if not lys:
                    continue
                syll = child(lys[0], "syllabic")
                txt_el = child(lys[0], "text")
                syll_v = (syll.text or "single") if syll is not None else "single"
                raw = (txt_el.text or "") if txt_el is not None else ""
                raw = raw.replace("\xa0", " ").strip()
                if syll_v in ("begin", "middle", "end"):
                    if txt_el is not None:
                        txt_el.text = raw
                    continue
                parts = hyphenate_token(raw)
                if len(parts) <= 1:
                    if txt_el is not None:
                        txt_el.text = raw
                    continue
                ops.append((i, parts))
            for i, parts in reversed(ops):
                n = len(parts)
                for vid, vnotes in voices.items():
                    if i >= len(vnotes):
                        continue
                    note = vnotes[i]
                    replicas = replicate_note(
                        note, n, parts if vid == "1" else None
                    )
                    replace_note_with_sequence(measure, note, replicas)
                splits += 1
            fix_backups_in_measure(measure)
    return splits


def _lyric_plain(note: ET.Element) -> str:
    lys = lyric_elements(note)
    if not lys:
        return ""
    txt = child(lys[0], "text")
    return (txt.text or "").replace("\xa0", " ").strip() if txt is not None else ""


def _lyric_syllabic(note: ET.Element) -> str:
    lys = lyric_elements(note)
    if not lys:
        return "single"
    syll = child(lys[0], "syllabic")
    return (syll.text or "single") if syll is not None else "single"


def _slur_starts(note: ET.Element) -> bool:
    notations = child(note, "notations")
    if notations is None:
        return False
    return any(sl.get("type") == "start" for sl in children(notations, "slur"))


def _pitch_key(note: ET.Element) -> tuple[str, str, str] | None:
    p = child(note, "pitch")
    if p is None:
        return None
    step = child(p, "step")
    alter = child(p, "alter")
    octv = child(p, "octave")
    return (
        (step.text or "") if step is not None else "",
        (alter.text or "0") if alter is not None else "0",
        (octv.text or "") if octv is not None else "",
    )


def apply_melisma_extenders(root: ET.Element) -> int:
    """Extender alleen bij kale noten op dezelfde toon (recitatief-rest).

    Doorgangsnoten (andere toon) en noten onder een slur krijgen geen
    underline. Begin/middle (koppelteken) ook niet. Idempotent.
    """
    n = 0
    for part in [c for c in root if local(c.tag) == "part"]:
        notes: list[ET.Element] = []
        for measure in children(part, "measure"):
            for el in measure:
                if local(el.tag) != "note" or is_chord(el):
                    continue
                v = child(el, "voice")
                vid = v.text if v is not None and v.text else "1"
                if vid != "1":
                    continue
                notes.append(el)
        i = 0
        while i < len(notes):
            note = notes[i]
            if is_rest(note) or not _lyric_plain(note):
                i += 1
                continue
            j = i + 1
            while j < len(notes) and not is_rest(notes[j]) and not _lyric_plain(notes[j]):
                j += 1
            ly = lyric_elements(note)[0]
            ext = child(ly, "extend")
            syll = _lyric_syllabic(note)
            key = _pitch_key(note)
            same = key is not None and all(
                _pitch_key(notes[k]) == key for k in range(i + 1, j)
            )
            want = (
                j > i + 1
                and same
                and syll not in ("begin", "middle")
                and not _slur_starts(note)
            )
            if want and ext is None:
                ET.SubElement(ly, "extend")
                n += 1
            elif not want and ext is not None:
                ly.remove(ext)
                n += 1
            i += 1
    return n


def strip_lyrics_from_lower_voices(root: ET.Element) -> int:
    """Lyrics alleen op stem 1, tussen de balken - niet onder het systeem."""
    n = 0
    for note in findall(root, "note"):
        v = child(note, "voice")
        vid = v.text if v is not None and v.text else "1"
        if vid == "1":
            for ly in lyric_elements(note):
                ly.set("number", "1")
                ly.set("default-y", "-80")
            continue
        if lyric_elements(note):
            clear_lyrics(note)
            n += 1
    return n


def merge_attributes(src: ET.Element, dst: ET.Element) -> None:
    src_attr = child(src, "attributes")
    if src_attr is None:
        return
    dst_attr = child(dst, "attributes")
    if dst_attr is None:
        dst.insert(0, copy.deepcopy(src_attr))
        return
    for field in ("divisions", "key", "time", "staves"):
        if child(dst_attr, field) is None:
            src_field = child(src_attr, field)
            if src_field is not None:
                dst_attr.insert(0, copy.deepcopy(src_field))
    dst_clef_nums = {c.get("number") for c in children(dst_attr, "clef")}
    for cl in children(src_attr, "clef"):
        if cl.get("number") not in dst_clef_nums:
            dst_attr.append(copy.deepcopy(cl))


def drop_empty_measures(root: ET.Element) -> int:
    dropped = 0
    for part in [c for c in root if local(c.tag) == "part"]:
        measures = children(part, "measure")
        for i, measure in enumerate(list(measures)):
            notes = [n for n in measure if local(n.tag) == "note"]
            empty = not notes or all(is_rest(n) for n in notes)
            if not empty:
                continue
            found_next = None
            seen = False
            for m in children(part, "measure"):
                if m is measure:
                    seen = True
                    continue
                if seen:
                    found_next = m
                    break
            if found_next is None:
                continue
            merge_attributes(measure, found_next)
            for el in list(measure):
                if local(el.tag) in ("direction",):
                    found_next.insert(0, copy.deepcopy(el))
            part.remove(measure)
            dropped += 1
        for i, measure in enumerate(children(part, "measure"), start=1):
            measure.set("number", str(i))
    return dropped


def compact_layout(root: ET.Element) -> None:
    for sl in findall(root, "staff-layout"):
        sd = child(sl, "staff-distance")
        if sd is None:
            continue
        if sl.get("number") == "2":
            sd.text = "70"
        else:
            sd.text = "40"
    for el in root.iter():
        ln = local(el.tag)
        if ln in ("system-distance", "top-system-distance"):
            try:
                if float(el.text or "0") > 50:
                    el.text = "50"
            except ValueError:
                pass
    for sl in findall(root, "system-layout"):
        for mar in children(sl, "system-margins"):
            lm = child(mar, "left-margin")
            if lm is not None:
                lm.text = "0"


def load_mxl(path: Path) -> tuple[ET.Element, str, dict[str, bytes]]:
    extras: dict[str, bytes] = {}
    xml_name = None
    xml_bytes = None
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            data = z.read(info.filename)
            if info.filename.endswith(".xml") and not info.filename.startswith("META"):
                xml_name = info.filename
                xml_bytes = data
            else:
                extras[info.filename] = data
    if xml_name is None or xml_bytes is None:
        raise ValueError(f"Geen MusicXML in {path}")
    root = ET.fromstring(xml_bytes)
    return root, xml_name, extras


def write_mxl(path: Path, root: ET.Element, xml_name: str, extras: dict[str, bytes]) -> None:
    ET.indent(root, space="\t")
    body = ET.tostring(root, encoding="unicode")
    if body.startswith("<?xml"):
        xml_text = body
    else:
        xml_text = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            "<!-- opgekuist door scripts/cleanup_capella_mxl.py -->\n"
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 2.0 Partwise//EN"'
            ' "http://www.musicxml.org/dtds/partwise.dtd">\n'
            + body
        )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in extras.items():
            z.writestr(name, data)
        if "META-INF/container.xml" not in extras:
            z.writestr(
                "META-INF/container.xml",
                (
                    '<?xml version="1.0" encoding="UTF-8"?>\n'
                    "<container>\n  <rootfiles>\n"
                    f'    <rootfile full-path="{xml_name}"'
                    ' media-type="application/vnd.recordare.musicxml+xml"/>\n'
                    "  </rootfiles>\n</container>\n"
                ),
            )
        z.writestr(xml_name, xml_text.encode("utf-8"))
    path.write_bytes(buf.getvalue())


def summarize(root: ET.Element) -> str:
    hidden = sum(
        1
        for n in findall(root, "note")
        if n.get("print-object") == "no" and is_pitched(n)
    )
    lyr = {}
    for n in findall(root, "note"):
        v = child(n, "voice")
        vid = v.text if v is not None else "?"
        if lyric_elements(n):
            lyr[vid] = lyr.get(vid, 0) + 1
    titles = findall(root, "work-title")
    title = titles[0].text if titles else "(geen)"
    return f"title={title!r} hidden_pitched={hidden} lyrics_by_voice={lyr}"


def cleanup(root: ET.Element) -> None:
    n_unhide = unhide_pitched_notes(root)
    n_pages = remove_page_number_directions(root)
    title, subtitle = promote_titles(root)
    hide_part_name(root)
    n_split = split_lyrics_keep_quarters(root)
    n_stripped = strip_lyrics_from_lower_voices(root)
    n_melisma = apply_melisma_extenders(root)
    n_empty = drop_empty_measures(root)
    for part in [c for c in root if local(c.tag) == "part"]:
        for measure in children(part, "measure"):
            fix_backups_in_measure(measure)
    compact_layout(root)
    print(
        f"  unhide={n_unhide} page-words={n_pages} title={title!r} "
        f"subtitle={subtitle!r} splits={n_split} lyrics_stripped={n_stripped} "
        f"melisma_extend={n_melisma} empty_measures={n_empty}"
    )
    print(f"  {summarize(root)}")


def expand_paths(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if path.is_dir():
            out.extend(sorted(p for p in path.glob("*.mxl") if p.is_file()))
        else:
            out.append(path)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Capella-MXL opkuisen (proef).")
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Een of meer .mxl-bestanden, of een map (alleen directe *.mxl, geen submappen)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Doel-.mxl of doelmap (default: in-place). Spaties/leestekens in de naam gaan eruit.",
    )
    args = parser.parse_args()
    files = expand_paths(args.paths)
    if not files:
        print("Geen .mxl-bestanden gevonden.", flush=True)
        return 1
    if args.output is not None and len(files) > 1 and not args.output.is_dir():
        print("Bij meerdere invoerbestanden moet -o een map zijn.", flush=True)
        return 1
    for path in files:
        print(f"== {path}")
        if args.output is None:
            dest = published_path(path) if " " in path.name else path
            if dest != path:
                raise SystemExit(
                    f"in-place geweigerd (spaties in de naam); gebruik -o, bijv. {dest.name}"
                )
        elif args.output.suffix.lower() == ".mxl":
            dest = published_path(args.output)
        else:
            dest = published_path(args.output / path.name)
        require_no_spaces(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        root, xml_name, extras = load_mxl(path)
        cleanup(root)
        write_mxl(dest, root, xml_name, extras)
        print(f"  geschreven: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
