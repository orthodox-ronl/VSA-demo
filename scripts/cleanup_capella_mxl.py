"""Proefscript: Capella/CapToMusic-MXL opkuisen voor oefengebruik.

Doel (homofone recitatief-scores zoals 7 / 6b):
- titel uit staff-tekst naar work-title + credit
- boekpagina-cijfers als losse words verwijderen
- print-object=no klinkende noten zichtbaar maken
- meerlettergrepige lyric-tokens splitsen (1 lettergreep per noot)
- lyrics van stem 1 naar stem 2-4 kopieren (zelfde nootindex per maat)

Geen extra Python-pakketten. Hyphenatie: uitzonderingenlijst + eenvoudige
Nederlandse regels. Polyfone stukken (cherubijnenhymne) vragen meer werk.

Gebruik:
  python scripts/cleanup_capella_mxl.py pad\\naar\\file.mxl
"""
from __future__ import annotations

import argparse
import copy
import io
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

# Handmatige splitsing voor liturgische woorden die de naive regel mist
# of verkeerd zou doen. Alleen de stam, zonder leestekens.
HYPHEN_EXCEPTIONS: dict[str, str] = {
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
    "hongeren": "hon-ge-ren",
    "kinderen": "kin-de-ren",
    "koninkrijk": "ko-nink-rijk",
    "lasterlijk": "las-ter-lijk",
    "nedervallen": "ne-der-val-len",
    "opgestaan": "op-ge-staan",
    "treurenden": "treu-ren-den",
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


def naive_hyphen(stem: str) -> list[str]:
    """Eenvoudige NL-splitsing: dubbele medeklinker, V-CV, prefixen."""
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

    # V-CV: za-lig (niet in diphthong)
    diph = ("aa", "ee", "oo", "uu", "ie", "ei", "ij", "ou", "au", "ui", "eu", "oe")
    i = 1
    while i < len(w) - 1:
        a, b, c = w[i - 1], w[i], w[i + 1]
        if a in VOWELS and b not in VOWELS and c in VOWELS:
            pair = (w[i - 1 : i + 1] if i >= 1 else "")
            if w[max(0, i - 2) : i] not in diph:
                return _restore_case(stem[:i], stem) + naive_hyphen(stem[i:])
        i += 1
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


def set_note_type(note: ET.Element, dur: int, divisions: int) -> None:
    type_el = child(note, "type")
    tm = child(note, "time-modification")
    if tm is not None:
        note.remove(tm)
    q = divisions
    mapping = [
        (q * 8, "breve"),
        (q * 4, "whole"),
        (q * 2, "half"),
        (q, "quarter"),
        (q // 2, "eighth"),
        (q // 4, "16th"),
        (q // 8, "32nd"),
    ]
    name = None
    for d, n in mapping:
        if d and dur == d:
            name = n
            break
    if name is None and q and 3 * dur == q:
        name = "eighth"
        _add_time_mod(note, type_el, 3, 2)
    elif name is None and q and 3 * dur == 2 * q:
        name = "quarter"
        _add_time_mod(note, type_el, 3, 2)
    if name is None:
        return
    if type_el is None:
        type_el = ET.Element("type")
        dur_el = child(note, "duration")
        idx = list(note).index(dur_el) + 1 if dur_el is not None else 0
        note.insert(idx, type_el)
    type_el.text = name


def _add_time_mod(note: ET.Element, type_el: ET.Element | None, actual: int, normal: int) -> None:
    tm = ET.Element("time-modification")
    ET.SubElement(tm, "actual-notes").text = str(actual)
    ET.SubElement(tm, "normal-notes").text = str(normal)
    if type_el is not None:
        idx = list(note).index(type_el) + 1
        note.insert(idx, tm)
    else:
        note.append(tm)


def set_lyric_syllables(note: ET.Element, text: str, syllabic: str) -> None:
    lys = lyric_elements(note)
    if not lys:
        ly = ET.Element("lyric", {"number": "1"})
        ET.SubElement(ly, "syllabic").text = syllabic
        ET.SubElement(ly, "text").text = text
        note.append(ly)
        return
    ly = lys[0]
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


def split_note(
    note: ET.Element,
    n: int,
    divisions: int,
    parts: list[str] | None = None,
) -> list[ET.Element]:
    if n <= 1:
        if parts:
            set_lyric_syllables(note, parts[0], "single")
        return [note]
    total = note_duration(note)
    base = total // n
    rem = total % n
    durs = [base] * n
    durs[-1] += rem
    out = [note]
    for _ in range(n - 1):
        out.append(copy.deepcopy(note))
    for i, (el, dur) in enumerate(zip(out, durs)):
        set_text(child(el, "duration"), str(dur))
        set_note_type(el, dur, divisions)
        el.attrib.pop("print-object", None)
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


def measure_divisions(measure: ET.Element, current: int) -> int:
    attrs = child(measure, "attributes")
    if attrs is None:
        return current
    div = child(attrs, "divisions")
    if div is not None and div.text:
        return int(float(div.text))
    return current


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


def set_part_name(root: ET.Element) -> None:
    for sp in findall(root, "score-part"):
        pn = child(sp, "part-name")
        if pn is not None and not (pn.text or "").strip():
            pn.text = "SATB"
        pa = child(sp, "part-abbreviation")
        if pa is not None and not (pa.text or "").strip():
            pa.text = "SATB"


def voice_timeline(measure: ET.Element, vid: str) -> list[tuple[int, int, ET.Element]]:
    out: list[tuple[int, int, ET.Element]] = []
    t = 0
    for note in notes_by_voice(measure).get(vid, []):
        d = note_duration(note)
        out.append((t, d, note))
        t += d
    return out


def split_note_to_durs(note: ET.Element, durs: list[int], divisions: int) -> list[ET.Element]:
    if len(durs) <= 1:
        return [note]
    out = [note]
    for _ in range(len(durs) - 1):
        out.append(copy.deepcopy(note))
    for i, (el, dur) in enumerate(zip(out, durs)):
        set_text(child(el, "duration"), str(dur))
        set_note_type(el, dur, divisions)
        el.attrib.pop("print-object", None)
        for beam in children(el, "beam"):
            el.remove(beam)
        if i > 0:
            clear_lyrics(el)
            notations = child(el, "notations")
            if notations is not None:
                for sl in [s for s in list(notations) if local(s.tag) == "slur"]:
                    notations.remove(sl)
                if len(list(notations)) == 0:
                    el.remove(notations)
    return out


def copy_lyric(src: ET.Element, dst: ET.Element) -> None:
    clear_lyrics(dst)
    for ly in lyric_elements(src):
        dst.append(copy.deepcopy(ly))


def add_extend(note: ET.Element) -> None:
    """Melismanoot: geen nieuwe lettergreep, wel verbinding."""
    clear_lyrics(note)
    ly = ET.Element("lyric", {"number": "1"})
    ext = ET.SubElement(ly, "extend")
    ext.set("type", "stop")
    note.append(ly)
    # vorige noot met tekst: extend start
    # (wordt in een tweede pass gezet)


def mark_extend_starts(measure: ET.Element) -> None:
    for vid in notes_by_voice(measure):
        seq = notes_by_voice(measure)[vid]
        for i, note in enumerate(seq):
            lys = lyric_elements(note)
            if not lys:
                continue
            ext = child(lys[0], "extend")
            if ext is None or ext.get("type") != "stop":
                continue
            if i == 0:
                continue
            prev = seq[i - 1]
            ply = lyric_elements(prev)
            if not ply:
                continue
            if child(ply[0], "extend") is None:
                e = ET.SubElement(ply[0], "extend")
                e.set("type", "start")


def split_lyrics_homophonic(root: ET.Element) -> int:
    """Split meerlettergrepige tokens alleen op stem 1."""
    splits = 0
    for part in [c for c in root if local(c.tag) == "part"]:
        divisions = 480
        for measure in children(part, "measure"):
            divisions = measure_divisions(measure, divisions)
            v1 = notes_by_voice(measure).get("1", [])
            for i in range(len(v1) - 1, -1, -1):
                note = v1[i]
                lys = lyric_elements(note)
                if not lys:
                    continue
                syll = child(lys[0], "syllabic")
                txt_el = child(lys[0], "text")
                syll_v = (syll.text or "single") if syll is not None else "single"
                raw = (txt_el.text or "") if txt_el is not None else ""
                raw = raw.replace("\xa0", " ")
                if syll_v in ("begin", "middle", "end"):
                    if txt_el is not None:
                        txt_el.text = raw.strip()
                    continue
                parts = hyphenate_token(raw)
                if len(parts) <= 1:
                    if txt_el is not None:
                        txt_el.text = raw.strip()
                    continue
                new_v1 = split_note(note, len(parts), divisions, parts)
                replace_note_with_sequence(measure, note, new_v1)
                splits += 1
    return splits


def match_other_voices_to_soprano(root: ET.Element) -> tuple[int, int]:
    """Onderverdeel stem 2-4 waar ze meerdere sopraannoten overspannen; kopieer lyrics."""
    splits = 0
    copied = 0
    for part in [c for c in root if local(c.tag) == "part"]:
        divisions = 480
        for measure in children(part, "measure"):
            divisions = measure_divisions(measure, divisions)
            src = voice_timeline(measure, "1")
            other_ids = [v for v in notes_by_voice(measure) if v != "1"]
            for vid in other_ids:
                dst = voice_timeline(measure, vid)
                for t, d, note in reversed(dst):
                    covering = [(st, sd, sn) for st, sd, sn in src if t <= st < t + d]
                    if not covering:
                        continue
                    cover_durs = [sd for _, sd, _ in covering]
                    if sum(cover_durs) != d:
                        continue
                    if len(covering) > 1:
                        new_notes = split_note_to_durs(note, cover_durs, divisions)
                        replace_note_with_sequence(measure, note, new_notes)
                        splits += 1
                        pairs = list(zip(new_notes, covering))
                    else:
                        pairs = [(note, covering[0])]
                    for dst_note, (_st, _sd, src_note) in pairs:
                        if lyric_elements(src_note):
                            copy_lyric(src_note, dst_note)
                            copied += 1
                        elif is_pitched(dst_note) and not is_rest(dst_note):
                            add_extend(dst_note)
                            copied += 1
            mark_extend_starts(measure)
            # ook sopranen-melisma's (noot zonder tekst)
            for _t, _d, sn in voice_timeline(measure, "1"):
                if not lyric_elements(sn) and is_pitched(sn) and not is_rest(sn):
                    add_extend(sn)
            mark_extend_starts(measure)
    return splits, copied


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
    set_part_name(root)
    n_split = split_lyrics_homophonic(root)
    n_match, n_copy = match_other_voices_to_soprano(root)
    print(
        f"  unhide={n_unhide} page-words={n_pages} title={title!r} "
        f"subtitle={subtitle!r} splits_v1={n_split} splits_other={n_match} "
        f"lyrics_copied={n_copy}"
    )
    print(f"  {summarize(root)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Capella-MXL opkuisen (proef).")
    parser.add_argument("paths", nargs="+", type=Path, help="Een of meer .mxl-bestanden")
    args = parser.parse_args()
    for path in args.paths:
        print(f"== {path}")
        root, xml_name, extras = load_mxl(path)
        cleanup(root)
        write_mxl(path, root, xml_name, extras)
        print(f"  geschreven: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
