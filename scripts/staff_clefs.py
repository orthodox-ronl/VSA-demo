"""Twee-balks sleutelbeleid: balk 1 = G, balk 2 = F (inclusief mid-score).

Gebruikt door cleanup_capella_mxl (MusicXML) en apply_mscz_layout (MSCX).
Toonsoorten blijven buiten scope. Alleen bij precies twee niet-lege balken.
"""
from __future__ import annotations

import base64
import os
import re
import xml.etree.ElementTree as ET

STAFF1_MUSICXML = ("G", "2")
STAFF2_MUSICXML = ("F", "4")
STAFF1_MSCX = "G"
STAFF2_MSCX = "F"

_STAFF_BLOCK_RE = re.compile(r'(<Staff id="(\d+)">)(.*?)(</Staff>)', re.S)
_MEASURE_RE = re.compile(r"<Measure\b[^>]*>.*?</Measure>", re.S)
_CLEF_RE = re.compile(r"<Clef>.*?</Clef>", re.S)
_VOICE_OPEN_RE = re.compile(r"<voice>")


def new_eid() -> str:
    return base64.urlsafe_b64encode(os.urandom(16)).decode("ascii").rstrip("=")[:22]


def _local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def _child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _children(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if _local(c.tag) == name]


def count_nonempty_score_staves_mscx(mscx: str) -> int:
    """Aantal score-Staff-blokken met maten en noten/akkoorden."""
    n = 0
    for m in _STAFF_BLOCK_RE.finditer(mscx):
        body = m.group(3)
        if "<Measure" not in body:
            continue
        if "<Chord" in body or "<Note" in body:
            n += 1
    return n


def _mscx_clef_xml(clef_type: str, *, header: bool) -> str:
    header_xml = "\n            <isHeader>1</isHeader>" if header else ""
    return (
        f"<Clef>\n"
        f"            <concertClefType>{clef_type}</concertClefType>\n"
        f"            <transposingClefType>{clef_type}</transposingClefType>"
        f"{header_xml}\n"
        f"            <eid>{new_eid()}</eid>\n"
        f"            </Clef>"
    )


def _rewrite_clef_block(block: str, clef_type: str) -> str:
    """Zet concert/transposing clef-types; mid-score verliest isHeader niet verplicht."""
    out = re.sub(
        r"<concertClefType>[^<]*</concertClefType>",
        f"<concertClefType>{clef_type}</concertClefType>",
        block,
        count=1,
    )
    out = re.sub(
        r"<transposingClefType>[^<]*</transposingClefType>",
        f"<transposingClefType>{clef_type}</transposingClefType>",
        out,
        count=1,
    )
    return out


def _desired_mscx_type(staff_index: int) -> str:
    return STAFF1_MSCX if staff_index == 0 else STAFF2_MSCX


def ensure_two_staff_header_clefs_mscx(mscx: str) -> tuple[str, list[str]]:
    """Forceer G op balk 1 en F op balk 2 (alle Clefs, inclusief mid-score)."""
    notes: list[str] = []
    measure_staffs = [
        m
        for m in _STAFF_BLOCK_RE.finditer(mscx)
        if "<Measure" in m.group(3)
        and ("<Chord" in m.group(3) or "<Note" in m.group(3))
    ]
    if len(measure_staffs) != 2:
        return mscx, notes

    changed = 0
    inserted = 0
    pieces: list[str] = []
    pos = 0
    for staff_i, sm in enumerate(measure_staffs):
        pieces.append(mscx[pos : sm.start()])
        head, sid, body, tail = sm.group(1), sm.group(2), sm.group(3), sm.group(4)
        want = _desired_mscx_type(staff_i)

        def fix_clef(cm: re.Match[str]) -> str:
            nonlocal changed
            old = cm.group(0)
            new = _rewrite_clef_block(old, want)
            if new != old:
                changed += 1
            return new

        new_body = _CLEF_RE.sub(fix_clef, body)
        if not _CLEF_RE.search(new_body):
            # Geen clef: header-clef vooraan in de eerste voice van maat 1.
            meas = _MEASURE_RE.search(new_body)
            if meas is not None:
                voice = _VOICE_OPEN_RE.search(meas.group(0))
                if voice is not None:
                    insert_at = meas.start() + voice.end()
                    clef = "\n          " + _mscx_clef_xml(want, header=True)
                    new_body = new_body[:insert_at] + clef + new_body[insert_at:]
                    inserted += 1
                    notes.append(f"Staff {sid}: ontbrekende {want}-sleutel gezet")
        pieces.append(head + new_body + tail)
        pos = sm.end()
    pieces.append(mscx[pos:])
    if changed:
        notes.append(f"sleutels genormaliseerd naar G/F: {changed} Clef-blok(ken)")
    if not notes and not changed and not inserted:
        # Idempotent: al goed, geen log
        return mscx, notes
    return "".join(pieces), notes


def _part_staff_count(part: ET.Element) -> int:
    max_staves = 1
    for measure in _children(part, "measure"):
        attrs = _child(measure, "attributes")
        if attrs is None:
            continue
        st = _child(attrs, "staves")
        if st is not None and st.text and st.text.isdigit():
            max_staves = max(max_staves, int(st.text))
        for cl in _children(attrs, "clef"):
            num = cl.get("number")
            if num and num.isdigit():
                max_staves = max(max_staves, int(num))
    return max_staves


def _set_clef_sign_line(clef: ET.Element, sign: str, line: str) -> bool:
    changed = False
    s = _child(clef, "sign")
    if s is None:
        s = ET.SubElement(clef, "sign")
        changed = True
    if s.text != sign:
        s.text = sign
        changed = True
    ln = _child(clef, "line")
    if ln is None:
        ln = ET.SubElement(clef, "line")
        changed = True
    if ln.text != line:
        ln.text = line
        changed = True
    octv = _child(clef, "clef-octave-change")
    if octv is not None:
        clef.remove(octv)
        changed = True
    return changed


def _ensure_clef_in_attrs(
    attrs: ET.Element, number: str | None, sign: str, line: str
) -> bool:
    """Zorg dat attributes een clef met dit number (of zonder number) heeft."""
    changed = False
    target: ET.Element | None = None
    for cl in _children(attrs, "clef"):
        num = cl.get("number")
        if number is None:
            if num is None or num == "1":
                target = cl
                break
        elif num == number:
            target = cl
            break
    if target is None:
        attrib = {"number": number} if number is not None else {}
        target = ET.Element("clef", attrib)
        attrs.append(target)
        ET.SubElement(target, "sign").text = sign
        ET.SubElement(target, "line").text = line
        return True
    if number is not None and target.get("number") != number:
        target.set("number", number)
        changed = True
    if _set_clef_sign_line(target, sign, line):
        changed = True
    return changed


def _rewrite_all_clefs_in_part(
    part: ET.Element, staff_map: dict[str | None, tuple[str, str]]
) -> int:
    """staff_map: clef number (of None) -> (sign, line)."""
    n = 0
    for measure in _children(part, "measure"):
        attrs = _child(measure, "attributes")
        if attrs is None:
            continue
        for cl in list(_children(attrs, "clef")):
            num = cl.get("number")
            key = num if num in staff_map else (None if None in staff_map else num)
            if key not in staff_map and num is not None and "1" in staff_map and num == "1":
                key = "1"
            if key not in staff_map:
                # Onbekend staff-nummer op 2-balks: map 1->G, 2->F als die keys bestaan
                if num == "1" and "1" in staff_map:
                    key = "1"
                elif num == "2" and "2" in staff_map:
                    key = "2"
                elif None in staff_map:
                    key = None
                else:
                    continue
            sign, line = staff_map[key]
            if _set_clef_sign_line(cl, sign, line):
                n += 1
    return n


def ensure_two_staff_clefs_musicxml(root: ET.Element) -> list[str]:
    """Forceer G/F op twee-balks MusicXML (alle clefs, inclusief mid-score)."""
    notes: list[str] = []
    parts = [c for c in root if _local(c.tag) == "part"]
    if not parts:
        return notes

    if len(parts) == 1:
        n_staves = _part_staff_count(parts[0])
        if n_staves != 2:
            return notes
        staff_map = {
            "1": STAFF1_MUSICXML,
            "2": STAFF2_MUSICXML,
            None: STAFF1_MUSICXML,
        }
        changed = _rewrite_all_clefs_in_part(parts[0], staff_map)
        # Eerste attributes: beide clefs aanwezig
        for measure in _children(parts[0], "measure"):
            attrs = _child(measure, "attributes")
            if attrs is None:
                continue
            if _ensure_clef_in_attrs(attrs, "1", *STAFF1_MUSICXML):
                changed += 1
            if _ensure_clef_in_attrs(attrs, "2", *STAFF2_MUSICXML):
                changed += 1
            break
        if changed:
            notes.append(f"MusicXML sleutels G/F (1 part, 2 balken): {changed} wijzigingen")
        return notes

    if len(parts) == 2:
        # Twee parts = twee balken (Women/Men, Voice 1/2, …).
        if any(_part_staff_count(p) > 1 for p in parts):
            return notes
        total = 0
        for part, pair in zip(parts, (STAFF1_MUSICXML, STAFF2_MUSICXML)):
            staff_map = {None: pair, "1": pair}
            total += _rewrite_all_clefs_in_part(part, staff_map)
            for measure in _children(part, "measure"):
                attrs = _child(measure, "attributes")
                if attrs is None:
                    continue
                if _ensure_clef_in_attrs(attrs, None, *pair):
                    total += 1
                break
        if total:
            notes.append(f"MusicXML sleutels G/F (2 parts): {total} wijzigingen")
        return notes

    return notes
