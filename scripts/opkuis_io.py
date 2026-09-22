"""MusicXML- en MuseScore-I/O voor opkuisen."""
from __future__ import annotations

import io
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cleanup_capella_mxl import load_mxl, write_mxl
from score_filenames import is_print_mscz


def load_musicxml(path: Path) -> tuple[ET.Element, str, dict[str, bytes]]:
    """Laad .mxl (zip) of plain .musicxml/.xml.

    Returns: (root, xml_member_name, extras_for_mxl).
    """
    suf = path.suffix.lower()
    if suf == ".mxl":
        return load_mxl(path)
    if suf in (".musicxml", ".xml"):
        text = path.read_text(encoding="utf-8")
        root = ET.fromstring(text)
        return root, path.name, {}
    raise ValueError(f"geen MusicXML-extensie: {path}")


def write_musicxml(
    path: Path,
    root: ET.Element,
    xml_name: str,
    extras: dict[str, bytes],
) -> None:
    """Schrijf naar .mxl of plain .musicxml/.xml."""
    suf = path.suffix.lower()
    if suf == ".mxl":
        write_mxl(path, root, xml_name, extras)
        return
    if suf in (".musicxml", ".xml"):
        ET.indent(root, space="\t")
        body = ET.tostring(root, encoding="unicode")
        if not body.startswith("<?xml"):
            body = (
                '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
                "<!-- opgekuist door scripts/opkuisen.py -->\n"
                + body
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8", newline="\n")
        return
    raise ValueError(f"geen MusicXML-doel-extensie: {path}")


def pick_mscx_name(names: list[str]) -> str:
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


def read_mscz(path: Path) -> tuple[str, str, dict[str, bytes], str]:
    """Return (mscx_text, mscx_name, others, mss_text)."""
    if is_print_mscz(path):
        raise ValueError(f"print-.mscz geweigerd: {path.name}")
    with zipfile.ZipFile(path, "r") as zin:
        names = zin.namelist()
        mscx_name = pick_mscx_name(names)
        mscx = zin.read(mscx_name).decode("utf-8")
        mss_name = "score_style.mss" if "score_style.mss" in names else None
        mss = zin.read(mss_name).decode("utf-8") if mss_name else ""
        others = {
            n: zin.read(n)
            for n in names
            if n != mscx_name and n != mss_name
        }
    return mscx, mscx_name, others, mss


def write_mscz(
    path: Path,
    mscx: str,
    mscx_name: str,
    others: dict[str, bytes],
    mss: str = "",
) -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        zout.writestr(mscx_name, mscx.encode("utf-8"))
        if mss:
            zout.writestr("score_style.mss", mss.encode("utf-8"))
        for n, data in others.items():
            zout.writestr(n, data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(buf.getvalue())


def read_mscx_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_mscx_file(path: Path, mscx: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(mscx, encoding="utf-8", newline="\n")
