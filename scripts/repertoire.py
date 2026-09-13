"""Repertoire-root: uitvoeringsvorm-id <-> pad (verhuisbare boom).

Id: zangstuk-id/variant-id/uitvoeringsvorm-id  ([a-z0-9_-]+, drie lagen).
Publicatiestam: zangstuk-id-variant-id-uitvoeringsvorm-id
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REPERTOIRE_ROOT = (
    REPO_ROOT / "content-source" / "praktijk" / "oefenhoek" / "repertoire"
)
HUGO_SECTION = "praktijk/oefenhoek/repertoire"
_ID_PART = re.compile(r"^[a-z0-9_-]+$")


def parse_id(value: str) -> tuple[str, str, str]:
    parts = value.strip().strip("/").split("/")
    if len(parts) != 3:
        raise ValueError(
            f"verwacht zangstuk/variant/uitvoeringsvorm, kreeg {value!r}"
        )
    for part in parts:
        if not _ID_PART.fullmatch(part):
            raise ValueError(f"ongeldig id-segment {part!r} in {value!r}")
    return parts[0], parts[1], parts[2]


def folder(value: str) -> Path:
    zangstuk, variant, uitvoeringsvorm = parse_id(value)
    return REPERTOIRE_ROOT / zangstuk / variant / uitvoeringsvorm


def stem(value: str) -> str:
    zangstuk, variant, uitvoeringsvorm = parse_id(value)
    return f"{zangstuk}-{variant}-{uitvoeringsvorm}"


def id_from_path(path: Path) -> str | None:
    try:
        rel = path.resolve().relative_to(REPERTOIRE_ROOT.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if len(parts) < 3:
        return None
    candidate = "/".join(parts[:3])
    try:
        parse_id(candidate)
    except ValueError:
        return None
    return candidate


def leaf_folders() -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    if not REPERTOIRE_ROOT.is_dir():
        return found
    for index in REPERTOIRE_ROOT.rglob("index.md"):
        ident = id_from_path(index.parent)
        if ident:
            found.append((ident, index.parent))
    return sorted(found, key=lambda item: item[0])
