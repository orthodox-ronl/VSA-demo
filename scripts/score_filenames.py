"""Publicatie-bestandsnamen voor de oefenhoek-conversiestraat.

Geen spaties in de bestandsnaam (Coria/GitHub weigeren of miscoderen die).
Map- en stamnamen: [a-z0-9_-]+ (` - ` en spaties -> '-'; overige leestekens -> '-').
"""
from __future__ import annotations

import re
from pathlib import Path

_UNSAFE = re.compile(r"[^a-zA-Z0-9_-]+")


def require_no_spaces(path: Path) -> None:
    if " " in path.name:
        raise SystemExit(f"bestandsnaam mag geen spaties hebben: {path.name}")


def published_stem(name: str) -> str:
    stem = Path(name).stem.replace(" - ", "-").replace(" ", "-")
    stem = _UNSAFE.sub("-", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("-")
    if not stem:
        raise SystemExit(f"geen geldige stam uit {name!r}")
    return stem


def published_path(path: Path) -> Path:
    """Zelfde map, gepubliceerde stam, zelfde suffix."""
    return path.with_name(published_stem(path.name) + path.suffix)
