"""Export een layout-.mscz naar playback-MXL voor Coria.

SATB in MuseScore is meestal 1 part / 2 balken / 4 stemmen. Coria kiest een
partij op score-part, niet op voice: dit script explodeert naar S/A/T/B,
kopieert lyrics, zet melisma-extenders, en schrijft .mxl zonder DOCTYPE
(DTD-fetch laat Coria falen). Coria vertaalt MusicXML intern (foutmelding
"translation failed"); layout-only markup (balken, stokken, slur-notations,
toonvoortekens, default-x/y, movement-title) gaat eraf. Versie wordt 3.1.
Pitch/alter, duur en lyrics blijven. Coria krijgt uncompressed `.musicxml`
via fingerprint_coria_mxl.py (ZIP-.mxl faalt op o.a. Kastorski).

Leidende rusten na een dubbele streep (print: gap/onzichtbaar) gaan eraf;
de maat wordt korter. Daarna een extra maat: 4 kwarten rust, lyric
[PAUZE], P:/D:/K:-cue van de volgende koormaat erboven. Gebogen cesuur:
1 kwart rust na die noot, geen lyric. Onzichtbare BPM-marker in de `.mscz`
wordt `<sound tempo>` + metronoom op alle parts. Overige print-object=no-rusten
worden zichtbaar. Time: senza-misura.

Geen roundtrip terug naar .mscz. Publicatie-.mxl: check_coria_mxl.py in check. Later: VSA-tooling.
Bestandsnamen: geen spaties (`scripts/score_filenames.py`).

  python scripts/export_mscz_coria_mxl.py pad\\naar\\file.mscz
  python scripts/export_mscz_coria_mxl.py pad\\naar\\file.mscz -o uit.mxl
  python scripts/export_mscz_coria_mxl.py content-source\\praktijk
  python scripts/export_mscz_coria_mxl.py --sanitize-mxl content-source\\praktijk
"""
from __future__ import annotations

import argparse
import copy
import io
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from score_filenames import published_path, require_no_spaces

CUE_RE = re.compile(r"^\s*[PDK]\s*[:;]", re.I)
PAUSE_LYRIC = "[PAUZE]"

MUSESCORE_CANDIDATES = (
    Path(r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe"),
    Path(r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"),
)

PART_META = (
    {"id": "P1", "name": "Soprano", "abbr": "S", "clef_sign": "G", "clef_line": "2"},
    {"id": "P2", "name": "Alto", "abbr": "A", "clef_sign": "G", "clef_line": "2"},
    {"id": "P3", "name": "Tenor", "abbr": "T", "clef_sign": "F", "clef_line": "4"},
    {"id": "P4", "name": "Bass", "abbr": "B", "clef_sign": "F", "clef_line": "4"},
)

_MXL_CONTAINER = """\
<?xml version="1.0" encoding="UTF-8"?>
<container>
  <rootfiles>
    <rootfile full-path="score.xml"/>
  </rootfiles>
</container>
"""


def local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if local(c.tag) == name:
            return c
    return None


def children(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if local(c.tag) == name]


def text(el: ET.Element | None) -> str:
    return (el.text or "").strip() if el is not None else ""


def is_rest(note: ET.Element) -> bool:
    return child(note, "rest") is not None


def is_chord(note: ET.Element) -> bool:
    return child(note, "chord") is not None


def is_pitched(note: ET.Element) -> bool:
    return child(note, "pitch") is not None or child(note, "unpitched") is not None


def lyric_elements(note: ET.Element) -> list[ET.Element]:
    return children(note, "lyric")


def note_duration(note: ET.Element) -> int:
    d = child(note, "duration")
    if d is None or not text(d):
        return 0
    return int(text(d))


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


def musescore_export(mscz: Path, dest: Path, musescore: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    job = [{"in": str(mscz.resolve()), "out": [str(dest.resolve())]}]
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
                [str(musescore), "-f", "-o", str(dest), str(mscz)],
                check=True,
                timeout=180,
            )
    finally:
        job_path.unlink(missing_ok=True)
    if not dest.is_file():
        raise RuntimeError(f"MuseScore schreef geen {dest}")


_DOCTYPE_RE = re.compile(rb"<!DOCTYPE[\s\S]*?>", re.IGNORECASE)


def parse_score_xml(raw: bytes) -> ET.Element:
    """Parse MusicXML; strip DOCTYPE (vsa-export) so ElementTree niet weigert."""
    return ET.fromstring(_DOCTYPE_RE.sub(b"", raw, count=1))


def load_score_xml(path: Path) -> ET.Element:
    if path.suffix.lower() == ".mxl":
        with zipfile.ZipFile(path) as z:
            names = [
                n
                for n in z.namelist()
                if n.endswith((".xml", ".musicxml")) and not n.startswith("META")
            ]
            if not names:
                raise ValueError(f"geen MusicXML in {path}")
            raw = z.read(names[0])
    else:
        raw = path.read_bytes()
    return parse_score_xml(raw)


def write_mxl(path: Path, root: ET.Element) -> None:
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    xml_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + body
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/container.xml", _MXL_CONTAINER)
        z.writestr("score.xml", xml_text.encode("utf-8"))
    path.write_bytes(buf.getvalue())


def score_parts(root: ET.Element) -> list[ET.Element]:
    plist = next(c for c in root if local(c.tag) == "part-list")
    return [c for c in plist if local(c.tag) == "score-part"]


def music_parts(root: ET.Element) -> list[ET.Element]:
    return [c for c in root if local(c.tag) == "part"]


def satb_voice_map(part: ET.Element) -> list[tuple[str, str]] | None:
    """[(staff, voice), ...] in S/A/T/B-volgorde, of None."""
    by_staff: dict[str, set[str]] = {}
    for measure in children(part, "measure"):
        for note in children(measure, "note"):
            staff = text(child(note, "staff")) or "1"
            voice = text(child(note, "voice")) or "1"
            by_staff.setdefault(staff, set()).add(voice)
    staves = sorted(by_staff, key=lambda s: int(s) if s.isdigit() else s)
    if len(staves) != 2:
        return None
    voices = [sorted(by_staff[s], key=lambda v: int(v) if v.isdigit() else v) for s in staves]
    if any(len(v) != 2 for v in voices):
        return None
    return [
        (staves[0], voices[0][0]),
        (staves[0], voices[0][1]),
        (staves[1], voices[1][0]),
        (staves[1], voices[1][1]),
    ]


_NOTE_MARKUP = frozenset({"beam", "stem", "notations", "accidental"})
_LAYOUT_ATTR_PREFIXES = ("default-", "relative-")
_LAYOUT_ATTRS = frozenset({"width", "print-object", "color"})
CORIA_FORBIDDEN_TAGS = _NOTE_MARKUP | frozenset({"part-group", "movement-title", "supports", "tie"})


def sanitize_coria_importer(root: ET.Element) -> None:
    """Strip visuele MusicXML die Coria's vertaler laat crashen.

    Playback blijft pitch+alter+duration+lyric. Getest tegen Coria:
    Cherubijnenhymne Kastorski faalt tot deze markup weg is, versie 3.1,
    geen movement-title. (Feofan werkte toevallig al zonder deze strip.)
    """
    root.set("version", "3.1")
    for el in list(root):
        if local(el.tag) == "movement-title":
            root.remove(el)
    ident = child(root, "identification")
    if ident is not None:
        enc = child(ident, "encoding")
        if enc is not None:
            for el in list(enc):
                if local(el.tag) == "supports":
                    enc.remove(el)
    for el in list(root.iter()):
        for attr in list(el.attrib):
            if attr.startswith(_LAYOUT_ATTR_PREFIXES) or attr in _LAYOUT_ATTRS:
                del el.attrib[attr]
        if local(el.tag) != "note":
            continue
        for child_el in list(el):
            ctag = local(child_el.tag)
            if ctag in _NOTE_MARKUP or ctag == "tie":
                el.remove(child_el)
                continue
            if ctag != "lyric":
                continue
            for grand in list(child_el):
                if local(grand.tag) == "extend":
                    child_el.remove(grand)
    plist = child(root, "part-list")
    if plist is not None:
        for el in list(plist):
            if local(el.tag) == "part-group":
                plist.remove(el)


def strip_layout(root: ET.Element) -> None:
    for tag in ("defaults", "credit"):
        for el in list(root):
            if local(el.tag) == tag:
                root.remove(el)
    ident = child(root, "identification")
    if ident is not None:
        enc = child(ident, "encoding")
        if enc is None:
            enc = ET.SubElement(ident, "encoding")
        sw = ET.Element("software")
        sw.text = "export_mscz_coria_mxl.py"
        enc.append(sw)


def make_score_part(meta: dict[str, str], channel: int) -> ET.Element:
    sp = ET.Element("score-part", id=meta["id"])
    ET.SubElement(sp, "part-name").text = meta["name"]
    ET.SubElement(sp, "part-abbreviation").text = meta["abbr"]
    iid = f"{meta['id']}-I1"
    inst = ET.SubElement(sp, "score-instrument", id=iid)
    ET.SubElement(inst, "instrument-name").text = meta["name"]
    ET.SubElement(inst, "instrument-sound").text = "keyboard.piano.grand"
    ET.SubElement(sp, "midi-device", id=iid, port="1")
    midi = ET.SubElement(sp, "midi-instrument", id=iid)
    ET.SubElement(midi, "midi-channel").text = str(channel)
    ET.SubElement(midi, "midi-program").text = "1"
    ET.SubElement(midi, "volume").text = "78.7402"
    ET.SubElement(midi, "pan").text = "0"
    return sp


def rewrite_attributes(attrs: ET.Element, *, clef_sign: str, clef_line: str) -> ET.Element:
    new = copy.deepcopy(attrs)
    for el in list(new):
        tag = local(el.tag)
        if tag in {"staves", "clef", "staff-details", "staff-layout"}:
            new.remove(el)
    clef = ET.SubElement(new, "clef")
    ET.SubElement(clef, "sign").text = clef_sign
    ET.SubElement(clef, "line").text = clef_line
    return new


def note_matches(note: ET.Element, staff: str, voice: str) -> bool:
    st = text(child(note, "staff")) or "1"
    vo = text(child(note, "voice")) or "1"
    return st == staff and vo == voice


def prepare_note(note: ET.Element) -> ET.Element:
    n = copy.deepcopy(note)
    for el in list(n):
        if local(el.tag) == "staff":
            n.remove(el)
    vo = child(n, "voice")
    if vo is not None:
        vo.text = "1"
    else:
        vo = ET.Element("voice")
        vo.text = "1"
        n.append(vo)
    if is_pitched(n) and n.get("print-object") == "no":
        del n.attrib["print-object"]
    return n


def tempo_direction(bpm: str) -> ET.Element:
    """Zichtbare metronoom + sound tempo (Coria-test; in .mscz mag die onzichtbaar zijn)."""
    try:
        shown = str(int(float(bpm)))
    except ValueError:
        shown = bpm
    direction = ET.Element("direction", placement="above")
    dt = ET.SubElement(direction, "direction-type")
    metro = ET.SubElement(dt, "metronome", parentheses="no")
    ET.SubElement(metro, "beat-unit").text = "quarter"
    ET.SubElement(metro, "per-minute").text = shown
    ET.SubElement(direction, "sound", tempo=shown)
    return direction


def extract_measure(
    src: ET.Element,
    *,
    staff: str,
    voice: str,
    meta: dict[str, str],
    keep_direction: bool,
    first_part: bool,
) -> ET.Element:
    out = ET.Element("measure", number=src.get("number") or "1")
    for el in src:
        tag = local(el.tag)
        if tag == "print":
            continue
        if tag == "backup" or tag == "forward":
            continue
        if tag == "attributes":
            if first_part or child(el, "clef") is not None or child(el, "key") is not None:
                out.append(
                    rewrite_attributes(
                        el, clef_sign=meta["clef_sign"], clef_line=meta["clef_line"]
                    )
                )
            continue
        if tag == "direction":
            if keep_direction:
                d = copy.deepcopy(el)
                for st in children(d, "staff"):
                    d.remove(st)
                out.append(d)
            continue
        if tag == "sound":
            tempo = el.get("tempo")
            if tempo:
                out.append(tempo_direction(tempo))
            continue
        if tag == "note":
            if note_matches(el, staff, voice):
                out.append(prepare_note(el))
            continue
        if tag == "barline":
            out.append(copy.deepcopy(el))
            continue
        if tag in {"harmony", "listening"}:
            continue
        if keep_direction:
            out.append(copy.deepcopy(el))
    return out


def pitched_timeline(measure: ET.Element) -> list[tuple[int, ET.Element]]:
    t = 0
    out: list[tuple[int, ET.Element]] = []
    for note in children(measure, "note"):
        if is_chord(note):
            continue
        if not is_rest(note):
            out.append((t, note))
        t += note_duration(note)
    return out


def copy_lyrics_from_soprano(parts: list[ET.Element]) -> int:
    if len(parts) < 2:
        return 0
    soprano = parts[0]
    n = 0
    sop_measures = children(soprano, "measure")
    for pi, part in enumerate(parts[1:], start=2):
        for sm, tm in zip(sop_measures, children(part, "measure")):
            src = pitched_timeline(sm)
            dst = pitched_timeline(tm)
            by_time = {t: note for t, note in src if lyric_elements(note)}
            used_index = False
            if len(src) == len(dst):
                used_index = True
            for i, (t, note) in enumerate(dst):
                if lyric_elements(note):
                    continue
                donor = None
                if t in by_time:
                    donor = by_time[t]
                elif used_index:
                    donor = src[i][1]
                if donor is None or not lyric_elements(donor):
                    continue
                for ly in lyric_elements(donor):
                    note.append(copy.deepcopy(ly))
                n += 1
    return n


def has_double_bar(measure: ET.Element) -> bool:
    for bar in children(measure, "barline"):
        if text(child(bar, "bar-style")) == "light-light":
            return True
    return False


def note_has_caesura(note: ET.Element) -> bool:
    return any(local(el.tag) == "caesura" for el in note.iter())


def direction_is_cue(direction: ET.Element) -> bool:
    words = " ".join(
        (el.text or "") for el in direction.iter() if local(el.tag) == "words"
    )
    return bool(CUE_RE.search(words.strip()))


def steal_cue_directions(measure: ET.Element) -> list[ET.Element]:
    stolen: list[ET.Element] = []
    for el in list(measure):
        if local(el.tag) == "direction" and direction_is_cue(el):
            measure.remove(el)
            stolen.append(el)
    return stolen


def divisions_of(root: ET.Element) -> int:
    for part in music_parts(root):
        for measure in children(part, "measure"):
            attrs = child(measure, "attributes")
            if attrs is None:
                continue
            div = child(attrs, "divisions")
            if div is not None and text(div).isdigit():
                return int(text(div))
    return 2


def make_rest_note(
    duration: int, *, type_name: str, lyric: str | None = None
) -> ET.Element:
    note = ET.Element("note")
    ET.SubElement(note, "rest")
    ET.SubElement(note, "duration").text = str(duration)
    ET.SubElement(note, "voice").text = "1"
    ET.SubElement(note, "type").text = type_name
    if lyric:
        ly = ET.SubElement(note, "lyric", number="1")
        ET.SubElement(ly, "syllabic").text = "single"
        ET.SubElement(ly, "text").text = lyric
    return note


def make_pause_measure(
    number: str, *, rest_dur: int, cues: list[ET.Element]
) -> ET.Element:
    measure = ET.Element("measure", number=number)
    for cue in cues:
        measure.append(copy.deepcopy(cue))
    measure.append(make_rest_note(rest_dur, type_name="whole", lyric=PAUSE_LYRIC))
    bar = ET.SubElement(measure, "barline", location="right")
    ET.SubElement(bar, "bar-style").text = "light-light"
    return measure


def insert_pause_measures(parts: list[ET.Element], whole_dur: int) -> int:
    """Na elke dubbele streep: 4-kwart rust + [PAUZE]; cue van de volgende maat."""
    if not parts:
        return 0
    n = 0
    soprano = children(parts[0], "measure")
    insert_after = [
        i
        for i in range(len(soprano) - 1)
        if has_double_bar(soprano[i])
    ]
    for i in reversed(insert_after):
        next_measures = [children(p, "measure")[i + 1] for p in parts]
        cues = steal_cue_directions(next_measures[0])
        for extra in next_measures[1:]:
            steal_cue_directions(extra)
        number = f"{next_measures[0].get('number', i + 2)}p"
        for part, nxt in zip(parts, next_measures):
            pause = make_pause_measure(number, rest_dur=whole_dur, cues=cues)
            part.insert(list(part).index(nxt), pause)
        n += 1
    return n


def insert_rest_after_time(measure: ET.Element, t_cut: int, duration: int) -> bool:
    t = 0
    for el in list(measure):
        if local(el.tag) != "note" or is_chord(el):
            continue
        t += note_duration(el)
        if t == t_cut:
            rest = make_rest_note(duration, type_name="quarter")
            measure.insert(list(measure).index(el) + 1, rest)
            return True
    return False


def insert_caesura_quarter_rests(parts: list[ET.Element], quarter: int) -> int:
    """Gebogen cesuur: 1 kwart rust op hetzelfde moment in alle parts, geen lyric."""
    if not parts:
        return 0
    n = 0
    n_meas = len(children(parts[0], "measure"))
    for mi in range(n_meas):
        group = [children(p, "measure")[mi] for p in parts]
        cuts: set[int] = set()
        for m in group:
            t = 0
            for note in children(m, "note"):
                if is_chord(note):
                    continue
                t += note_duration(note)
                if note_has_caesura(note):
                    cuts.add(t)
        for t_cut in sorted(cuts, reverse=True):
            for m in group:
                if insert_rest_after_time(m, t_cut, quarter):
                    n += 1
    return n


def renumber_measures(root: ET.Element) -> None:
    for part in music_parts(root):
        for i, measure in enumerate(children(part, "measure"), start=1):
            measure.set("number", str(i))


def measure_duration(measure: ET.Element) -> int:
    t = 0
    for note in children(measure, "note"):
        if is_chord(note):
            continue
        t += note_duration(note)
    return t


def strip_leading_rests(measure: ET.Element) -> int:
    n = 0
    for el in list(measure):
        if local(el.tag) != "note":
            continue
        if is_chord(el) or not is_rest(el):
            break
        measure.remove(el)
        n += 1
    return n


def unhide_notes(root: ET.Element) -> int:
    n = 0
    for part in music_parts(root):
        for el in part.iter():
            if local(el.tag) != "note":
                continue
            if el.get("print-object") == "no":
                del el.attrib["print-object"]
                n += 1
    return n


def equalize_measure_durations(parts: list[ET.Element]) -> int:
    """Kortere stem in een maat: rust achteraan, zodat Coria per maat gelijk blijft."""
    n = 0
    groups = list(zip(*(children(p, "measure") for p in parts)))
    for group in groups:
        durs = [measure_duration(m) for m in group]
        target = max(durs) if durs else 0
        for measure, dur in zip(group, durs):
            gap = target - dur
            if gap <= 0:
                continue
            rest = ET.Element("note")
            ET.SubElement(rest, "rest")
            ET.SubElement(rest, "duration").text = str(gap)
            ET.SubElement(rest, "voice").text = "1"
            bar = child(measure, "barline")
            if bar is not None:
                measure.insert(list(measure).index(bar), rest)
            else:
                measure.append(rest)
            n += 1
    return n


def set_senza_misura(root: ET.Element) -> None:
    for part in music_parts(root):
        for mi, measure in enumerate(children(part, "measure")):
            attrs = child(measure, "attributes")
            if attrs is None:
                continue
            tm = child(attrs, "time")
            if tm is None:
                continue
            attrs.remove(tm)
            if mi != 0:
                continue
            new = ET.Element("time")
            ET.SubElement(new, "senza-misura")
            key = child(attrs, "key")
            div = child(attrs, "divisions")
            if key is not None:
                attrs.insert(list(attrs).index(key) + 1, new)
            elif div is not None:
                attrs.insert(list(attrs).index(div) + 1, new)
            else:
                attrs.insert(0, new)


def apply_coria_timing(root: ET.Element) -> None:
    """Print-pickups weg; [PAUZE] na dubbele streep; kwart na cesuur; geen hidden rusten."""
    parts = music_parts(root)
    if not parts:
        return
    measures = [children(p, "measure") for p in parts]
    n_lead = 0
    prev_double = False
    for mi in range(len(measures[0])):
        if mi == 0 or prev_double:
            for ms in measures:
                n_lead += strip_leading_rests(ms[mi])
        prev_double = has_double_bar(measures[0][mi])
    div = divisions_of(root)
    n_pause = insert_pause_measures(parts, whole_dur=4 * div)
    n_caes = insert_caesura_quarter_rests(parts, quarter=div)
    n_hide = unhide_notes(root)
    n_pad = equalize_measure_durations(parts)
    set_senza_misura(root)
    renumber_measures(root)
    n_tempo = 0
    for part in parts:
        for measure in children(part, "measure"):
            for d in children(measure, "direction"):
                snd = child(d, "sound")
                if snd is not None and snd.get("tempo"):
                    n_tempo += 1
    print(
        f"  sectie-pickup rusten weg={n_lead} pauze-maten={n_pause} "
        f"cesuur-kwarten={n_caes} unhide={n_hide} duur-pad={n_pad} "
        f"tempo-markers={n_tempo}"
    )


def apply_melisma_extenders(root: ET.Element) -> int:
    n = 0
    for part in music_parts(root):
        notes: list[ET.Element] = []
        for measure in children(part, "measure"):
            for el in children(measure, "note"):
                if is_chord(el):
                    continue
                notes.append(el)
        i = 0
        while i < len(notes):
            note = notes[i]
            if is_rest(note) or not lyric_elements(note):
                i += 1
                continue
            j = i + 1
            while j < len(notes) and not is_rest(notes[j]) and not lyric_elements(notes[j]):
                j += 1
            ly = lyric_elements(note)[0]
            ext = child(ly, "extend")
            if j > i + 1:
                if ext is None:
                    ET.SubElement(ly, "extend")
                    n += 1
            elif ext is not None:
                ly.remove(ext)
            i += 1
    return n


def explode_satb(root: ET.Element, voice_map: list[tuple[str, str]]) -> ET.Element:
    src_part = music_parts(root)[0]
    measures = children(src_part, "measure")
    new = ET.Element(root.tag, attrib=root.attrib)
    work = child(root, "work")
    if work is not None:
        new.append(copy.deepcopy(work))
    ident = child(root, "identification")
    if ident is not None:
        new.append(copy.deepcopy(ident))
    movement = child(root, "movement-title")
    if movement is not None:
        new.append(copy.deepcopy(movement))
    plist = ET.SubElement(new, "part-list")
    pg = ET.SubElement(plist, "part-group", type="start", number="1")
    ET.SubElement(pg, "group-symbol").text = "bracket"
    for i, meta in enumerate(PART_META):
        plist.append(make_score_part(meta, channel=i + 1))
    ET.SubElement(plist, "part-group", type="stop", number="1")
    built: list[ET.Element] = []
    for i, ((staff, voice), meta) in enumerate(zip(voice_map, PART_META)):
        part = ET.SubElement(new, "part", id=meta["id"])
        for mi, src in enumerate(measures):
            part.append(
                extract_measure(
                    src,
                    staff=staff,
                    voice=voice,
                    meta=meta,
                    keep_direction=True,
                    first_part=(mi == 0),
                )
            )
        built.append(part)
    n_ly = copy_lyrics_from_soprano(built)
    print(f"  SATB explode S/A/T/B, lyrics gekopieerd={n_ly}")
    return new


def sanitize_existing_parts(root: ET.Element) -> ET.Element:
    """Al 4 parts: layout weg, lyrics aanvullen, MIDI als die ontbreekt."""
    strip_layout(root)
    parts = music_parts(root)
    if len(parts) == 4:
        n_ly = copy_lyrics_from_soprano(parts)
        if n_ly:
            print(f"  lyrics gekopieerd naar lagere parts={n_ly}")
    return root


def convert_root(root: ET.Element) -> ET.Element:
    parts = music_parts(root)
    if len(parts) == 1:
        voice_map = satb_voice_map(parts[0])
        if voice_map is not None:
            new = explode_satb(root, voice_map)
            strip_layout(new)
            return new
    return sanitize_existing_parts(root)


def summarize(root: ET.Element) -> str:
    bits = []
    for part in music_parts(root):
        lyr = sum(
            1
            for n in children(part, "measure")
            for note in children(n, "note")
            if lyric_elements(note)
        )
        bits.append(f"{part.get('id')}:lyrics={lyr}")
    work = child(root, "work")
    title = text(child(work, "work-title")) if work is not None else ""
    return f"title={title!r} parts={len(music_parts(root))} {', '.join(bits)}"


def process(mscz: Path, out: Path) -> None:
    musescore = find_musescore()
    print(f"using {musescore}")
    with tempfile.TemporaryDirectory() as tmp:
        raw_mxl = Path(tmp) / "export.mxl"
        musescore_export(mscz, raw_mxl, musescore)
        root = load_score_xml(raw_mxl)
    root = convert_root(root)
    apply_coria_timing(root)
    n_ext = apply_melisma_extenders(root)
    print(f"  melisma-extend={n_ext}")
    print(f"  {summarize(root)}")
    parts = music_parts(root)
    if len(parts) >= 2:
        bad = []
        for mi, group in enumerate(
            zip(*(children(p, "measure") for p in parts)), start=1
        ):
            durs = [measure_duration(m) for m in group]
            if len(set(durs)) > 1:
                bad.append(f"m{mi}:{durs}")
        if bad:
            print(f"  WAARSCHUWING maatduur verschilt: {', '.join(bad)}")
    sanitize_coria_importer(root)
    write_mxl(out, root)
    print(f"geschreven: {out}")


def process_existing_mxl(path: Path) -> None:
    require_no_spaces(path)
    root = load_score_xml(path)
    sanitize_coria_importer(root)
    write_mxl(path, root)
    print(f"  {summarize(root)}")
    print(f"gesaneerd: {path}")


def coria_importer_violations(root: ET.Element) -> list[str]:
    found: set[str] = set()
    for el in root.iter():
        tag = local(el.tag)
        if tag in CORIA_FORBIDDEN_TAGS:
            found.add(tag)
    if root.attrib.get("version") not in {"3.0", "3.1"}:
        found.add(f"version:{root.attrib.get('version')}")
    return sorted(found)


def expand_score_files(paths: list[Path], suffix: str) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if path.is_dir():
            found = sorted(p for p in path.rglob(f"*{suffix}") if p.is_file())
            if path.name != "input" and "input" not in path.parts:
                found = [p for p in found if "input" not in p.parts]
            out.extend(found)
        else:
            out.append(path)
    return out


def expand_mscz(paths: list[Path]) -> list[Path]:
    return expand_score_files(paths, ".mscz")


def main() -> int:
    p = argparse.ArgumentParser(description="Layout-.mscz naar Coria-MXL.")
    p.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Een of meer .mscz/.mxl, of een map (recursief; sla input\\ over)",
    )
    p.add_argument("-o", "--output", type=Path, help="Doel-.mxl (alleen bij een .mscz)")
    p.add_argument(
        "--sanitize-mxl",
        action="store_true",
        help="Bestaande publicatie-.mxl in-place Coria-veilig maken (geen MuseScore)",
    )
    args = p.parse_args()
    if args.sanitize_mxl:
        files = expand_score_files(args.paths, ".mxl")
        if not files:
            print("Geen .mxl-bestanden gevonden.", flush=True)
            return 0
        if args.output is not None:
            raise SystemExit("-o niet samen met --sanitize-mxl")
        failed = 0
        for path in files:
            print(f"== {path}", flush=True)
            if not path.is_file() or path.suffix.lower() != ".mxl":
                print(f"  overgeslagen: {path}", flush=True)
                failed += 1
                continue
            try:
                process_existing_mxl(path)
            except Exception as exc:  # noqa: BLE001
                print(f"  FAILED {exc}", flush=True)
                failed += 1
        if failed:
            print(f"{failed} mislukt van {len(files)}", flush=True)
            return 1
        return 0

    files = expand_mscz(args.paths)
    if not files:
        print("Geen .mscz-bestanden gevonden.", flush=True)
        return 1
    if args.output is not None and len(files) != 1:
        raise SystemExit("-o alleen bij precies een .mscz")
    failed = 0
    for path in files:
        print(f"== {path}", flush=True)
        if not path.is_file():
            print(f"  niet gevonden: {path}", flush=True)
            failed += 1
            continue
        if path.suffix.lower() != ".mscz":
            print(f"  geen .mscz: {path}", flush=True)
            failed += 1
            continue
        try:
            require_no_spaces(path)
            out = args.output if args.output is not None else path.with_suffix(".mxl")
            out = published_path(out)
            require_no_spaces(out)
            process(path, out)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED {exc}", flush=True)
            failed += 1
    if failed:
        print(f"{failed} mislukt van {len(files)}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
