"""Publicatie-bestandsnamen voor de oefenhoek-conversiestraat.

Geen spaties in de bestandsnaam (Coria/GitHub weigeren of miscoderen die).
Map- en stamnamen: [a-z0-9_-]+ (` - ` en spaties -> '-'; overige leestekens -> '-').

Print-`.mscz` (naam eindigt op `.print.mscz`): koormap-/PDF-vel buiten de
hub-pijplijn. Geen apply_mscz_layout, geen mscz-products, geen hub-product-gate.
"""
from __future__ import annotations

import re
from pathlib import Path

_UNSAFE = re.compile(r"[^a-zA-Z0-9_-]+")
PRINT_MSCZ_SUFFIX = ".print.mscz"


def require_no_spaces(path: Path) -> None:
    if " " in path.name:
        raise SystemExit(f"bestandsnaam mag geen spaties hebben: {path.name}")


def is_print_mscz(path: Path | str) -> bool:
    """True als dit een print-vel is (scripts moeten ervan afblijven)."""
    name = path.name if isinstance(path, Path) else Path(path).name
    return name.lower().endswith(PRINT_MSCZ_SUFFIX)


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
