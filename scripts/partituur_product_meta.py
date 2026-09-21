"""Provenance in afgeleiden: source-sha256 + generated-at.

Basispartituur (representatie-id ``partituur``) zet
``vsa-partituur-sha256`` (en legacy ``vsa-hub-sha256``) als bron-hash van de
basispartituur-``.mscz``.
VSA-producten zetten ``vsa-source-sha256`` + ``vsa-source-kind=vsa``.

MXL: MusicXML identification / miscellaneous-field.
PDF: Info-dict via pypdf (napoststampen na MuseScore-export).
"""

from __future__ import annotations

import hashlib
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

FIELD_PARTITUUR_SHA = "vsa-partituur-sha256"
FIELD_PARTITUUR_SHA_LEGACY = "vsa-hub-sha256"
# Alias voor bestaande imports / docs die de oude naam noemen.
FIELD_HUB_SHA = FIELD_PARTITUUR_SHA
FIELD_SOURCE_SHA = "vsa-source-sha256"
FIELD_SOURCE_KIND = "vsa-source-kind"
FIELD_GENERATED_AT = "vsa-generated-at"
FIELD_GENERATOR = "vsa-generator"
GENERATOR_ID = "mscz-products"
GENERATOR_VSA = "vsa-musicxml"
SOURCE_KIND_PARTITUUR = "partituur"
SOURCE_KIND_HUB = SOURCE_KIND_PARTITUUR  # legacy alias
SOURCE_KIND_VSA = "vsa"
PDF_KEY_PARTITUUR = "/VSAPartituurSHA256"
PDF_KEY_PARTITUUR_LEGACY = "/VSAHubSHA256"
PDF_KEY_HUB = PDF_KEY_PARTITUUR
PDF_KEY_GENERATED = "/VSAGeneratedAt"
PDF_KEY_GENERATOR = "/VSAGenerator"


def partituur_sha256(mscz: Path) -> str:
    return hashlib.sha256(mscz.read_bytes()).hexdigest()


def hub_sha256(mscz: Path) -> str:
    """Legacy alias van ``partituur_sha256``."""
    return partituur_sha256(mscz)


def source_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stamp_sha_from_dict(stamp: dict[str, str]) -> str:
    """Lees partituur-hash uit stamp-dict (nieuw of legacy veld)."""
    return (
        stamp.get(FIELD_PARTITUUR_SHA, "")
        or stamp.get(FIELD_PARTITUUR_SHA_LEGACY, "")
        or ""
    )


def _local(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _child(el: ET.Element, name: str) -> ET.Element | None:
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _children(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if _local(c.tag) == name]


def _ensure_identification(root: ET.Element) -> ET.Element:
    ident = _child(root, "identification")
    if ident is None:
        ident = ET.Element("identification")
        insert_at = 0
        for i, c in enumerate(list(root)):
            if _local(c.tag) in {"work", "movement-number", "movement-title"}:
                insert_at = i + 1
        root.insert(insert_at, ident)
    return ident


def _set_misc_field(ident: ET.Element, name: str, value: str) -> None:
    misc = _child(ident, "miscellaneous")
    if misc is None:
        misc = ET.SubElement(ident, "miscellaneous")
    for field in _children(misc, "miscellaneous-field"):
        if field.get("name") == name:
            field.text = value
            return
    field = ET.SubElement(misc, "miscellaneous-field", name=name)
    field.text = value


def stamp_mxl_source(
    root: ET.Element,
    *,
    source_hash: str,
    source_kind: str,
    generated_at: str,
    generator: str,
    also_partituur_sha: bool = False,
    also_hub_sha: bool | None = None,
) -> None:
    if also_hub_sha is not None:
        also_partituur_sha = also_hub_sha
    ident = _ensure_identification(root)
    enc = _child(ident, "encoding")
    if enc is None:
        enc = ET.SubElement(ident, "encoding")
    date_el = _child(enc, "encoding-date")
    if date_el is None:
        date_el = ET.Element("encoding-date")
        enc.insert(0, date_el)
    date_el.text = generated_at[:10]
    sw = ET.Element("software")
    sw.text = f"{generator} {source_kind}={source_hash[:12]}"
    enc.append(sw)
    _set_misc_field(ident, FIELD_SOURCE_SHA, source_hash)
    _set_misc_field(ident, FIELD_SOURCE_KIND, source_kind)
    _set_misc_field(ident, FIELD_GENERATED_AT, generated_at)
    _set_misc_field(ident, FIELD_GENERATOR, generator)
    if also_partituur_sha:
        _set_misc_field(ident, FIELD_PARTITUUR_SHA, source_hash)
        _set_misc_field(ident, FIELD_PARTITUUR_SHA_LEGACY, source_hash)


def stamp_mxl_tree(
    root: ET.Element,
    *,
    partituur_hash: str | None = None,
    hub_hash: str | None = None,
    generated_at: str,
    generator: str = GENERATOR_ID,
) -> None:
    """Basispartituur-product stamp (nieuw + legacy hash-velden)."""
    digest = partituur_hash if partituur_hash is not None else hub_hash
    if not digest:
        raise ValueError("partituur_hash of hub_hash verplicht")
    stamp_mxl_source(
        root,
        source_hash=digest,
        source_kind=SOURCE_KIND_PARTITUUR,
        generated_at=generated_at,
        generator=generator,
        also_partituur_sha=True,
    )


def read_mxl_stamp(path: Path) -> dict[str, str]:
    """Lees stamp uit .mxl of .musicxml/.xml."""
    if path.suffix.lower() == ".mxl":
        with zipfile.ZipFile(path) as z:
            names = [
                n
                for n in z.namelist()
                if n.endswith((".xml", ".musicxml")) and not n.startswith("META")
            ]
            if not names:
                return {}
            raw = z.read(names[0])
    else:
        raw = path.read_bytes()
    raw = re.sub(rb"<!DOCTYPE[\s\S]*?>", b"", raw, count=1, flags=re.I)
    root = ET.fromstring(raw)
    ident = _child(root, "identification")
    if ident is None:
        return {}
    out: dict[str, str] = {}
    misc = _child(ident, "miscellaneous")
    if misc is not None:
        for field in _children(misc, "miscellaneous-field"):
            name = field.get("name") or ""
            if name and (field.text or "").strip():
                out[name] = (field.text or "").strip()
    return out


def stamp_pdf(
    path: Path,
    *,
    partituur_hash: str | None = None,
    hub_hash: str | None = None,
    generated_at: str,
    generator: str = GENERATOR_ID,
) -> None:
    digest = partituur_hash if partituur_hash is not None else hub_hash
    if not digest:
        raise ValueError("partituur_hash of hub_hash verplicht")
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        import subprocess
        import sys

        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(Path(__file__).with_name("requirements-partituur.txt")),
            ],
        )
        from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(path))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata(
        {
            PDF_KEY_PARTITUUR: digest,
            PDF_KEY_PARTITUUR_LEGACY: digest,
            "/VSAGeneratedAt": generated_at,
            "/VSAGenerator": generator,
        }
    )
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(path)


def read_pdf_stamp(path: Path) -> dict[str, str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return {}
    try:
        reader = PdfReader(str(path))
    except Exception:  # noqa: BLE001
        return {}
    meta = reader.metadata
    if meta is None:
        return {}
    raw = {str(k): str(v) for k, v in dict(meta).items() if v is not None}
    out: dict[str, str] = {}
    mapping = {
        PDF_KEY_PARTITUUR: FIELD_PARTITUUR_SHA,
        "VSAPartituurSHA256": FIELD_PARTITUUR_SHA,
        PDF_KEY_PARTITUUR_LEGACY: FIELD_PARTITUUR_SHA_LEGACY,
        "VSAHubSHA256": FIELD_PARTITUUR_SHA_LEGACY,
        "/VSAGeneratedAt": FIELD_GENERATED_AT,
        "VSAGeneratedAt": FIELD_GENERATED_AT,
        "/VSAGenerator": FIELD_GENERATOR,
        "VSAGenerator": FIELD_GENERATOR,
    }
    for key, field in mapping.items():
        if key in raw and raw[key].strip():
            out[field] = raw[key].strip()
    return out
