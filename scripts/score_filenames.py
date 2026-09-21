"""Publicatie-bestandsnamen voor de oefenhoek-conversiestraat.

Geen spaties in de bestandsnaam (Coria/GitHub weigeren of miscoderen die).
Map- en stamnamen: [a-z0-9_-]+ (` - ` en spaties -> '-'; overige leestekens -> '-').

Print-`.mscz` (naam eindigt op `.print.mscz`): koormap-/PDF-vel buiten de
basispartituur-pijplijn. Geen apply_mscz_layout, geen mscz-products, geen
partituur-product-gate.

Afgeleiden per representatie-id: zie scripts/oefenhoek-product-contract.md
(`{stam}.{representatie-id}.{ext}`).
"""
from __future__ import annotations

import re
from pathlib import Path

_UNSAFE = re.compile(r"[^a-zA-Z0-9_-]+")
PRINT_MSCZ_SUFFIX = ".print.mscz"
SYLLABIFY_VSA_SUFFIX = ".syl.vsa"
# Canonieke representatie-ids (contract). Uitbreiden alleen via contract-PR.
KNOWN_REPRESENTATIE_IDS = frozenset({"partituur", "vsa", "print"})
# Oude id in bestandsnamen / docs → canonieke id.
REPRESENTATIE_ID_ALIASES = {"hub": "partituur"}

def require_no_spaces(path: Path) -> None:
    if " " in path.name:
        raise SystemExit(f"bestandsnaam mag geen spaties hebben: {path.name}")


def is_print_mscz(path: Path | str) -> bool:
    """True als dit een print-vel is (scripts moeten ervan afblijven)."""
    name = path.name if isinstance(path, Path) else Path(path).name
    return name.lower().endswith(PRINT_MSCZ_SUFFIX)


def is_syllabify_sidecar_vsa(path: Path | str) -> bool:
    """Tussenvorm ``vsa syllabify --extension .syl.vsa``; geen canonieke bron."""
    name = path.name if isinstance(path, Path) else Path(path).name
    return name.lower().endswith(SYLLABIFY_VSA_SUFFIX.lower())


def is_bibliotheek_vsa_source(path: Path) -> bool:
    """Canonieke bibliotheek-``.vsa`` (geen syllabify-sidecar)."""
    return path.suffix.lower() == ".vsa" and not is_syllabify_sidecar_vsa(path)


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


def representatie_id_from_name(name: str) -> str | None:
    """Haal representatie-id uit `{stam}.{repr}.ext` of `{stam}.print.mscz`.

    Geeft None bij legacy korte naam (`{stam}.mxl` zonder representatie-segment).
    """
    lower = Path(name).name.lower()
    if lower.endswith(PRINT_MSCZ_SUFFIX):
        return "print"
    stem = Path(name).stem  # strips final suffix only (.mxl / .pdf / .mscz)
    if "." not in stem:
        return None
    maybe = stem.rsplit(".", 1)[-1].lower()
    maybe = REPRESENTATIE_ID_ALIASES.get(maybe, maybe)
    if maybe in KNOWN_REPRESENTATIE_IDS:
        return maybe
    return None


def canonicalize_representatie_id(representatie_id: str) -> str:
    rid = representatie_id.strip().lower()
    return REPRESENTATIE_ID_ALIASES.get(rid, rid)


def product_filename(stam: str, representatie_id: str, ext: str) -> str:
    """Bouw `{stam}.{representatie-id}.{ext}` (ext met of zonder punt)."""
    rid = canonicalize_representatie_id(representatie_id)
    if rid not in KNOWN_REPRESENTATIE_IDS:
        raise SystemExit(f"onbekende representatie-id: {representatie_id!r}")
    suffix = ext if ext.startswith(".") else f".{ext}"
    return f"{stam}.{rid}{suffix}"
