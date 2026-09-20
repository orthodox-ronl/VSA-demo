"""Bibliotheek-root: uitvoeringsvorm-id <-> pad (verhuisbare boom).

Id: zangstuk-id/variant-id/uitvoeringsvorm-id  ([a-z0-9_-]+, drie lagen).
Publicatiestam: zangstuk-id-variant-id-uitvoeringsvorm-id

Alias-variant: op de variant-_index (`zangstuk/variant/_index.md`) staat
`alias_van: zangstuk/canonieke-variant`. Geen uitvoeringsvorm-map, geen
partituur. Pipeline: `python scripts/bibliotheek.py` (in check).
"""

from __future__ import annotations

import re
from pathlib import Path

from _diag import format_issue, frontmatter_key_line

REPO_ROOT = Path(__file__).resolve().parents[1]
BIBLIOTHEEK_ROOT = (
    REPO_ROOT / "content-source" / "praktijk" / "oefenhoek" / "bibliotheek"
)
HUGO_SECTION = "praktijk/oefenhoek/bibliotheek"
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


def parse_variant_id(value: str) -> tuple[str, str]:
    parts = value.strip().strip("/").split("/")
    if len(parts) != 2:
        raise ValueError(
            f"verwacht zangstuk/variant, kreeg {value!r}"
        )
    for part in parts:
        if not _ID_PART.fullmatch(part):
            raise ValueError(f"ongeldig id-segment {part!r} in {value!r}")
    return parts[0], parts[1]


def folder(value: str) -> Path:
    zangstuk, variant, uitvoeringsvorm = parse_id(value)
    return BIBLIOTHEEK_ROOT / zangstuk / variant / uitvoeringsvorm


def variant_folder(value: str) -> Path:
    zangstuk, variant = parse_variant_id(value)
    return BIBLIOTHEEK_ROOT / zangstuk / variant


def stem(value: str) -> str:
    zangstuk, variant, uitvoeringsvorm = parse_id(value)
    return f"{zangstuk}-{variant}-{uitvoeringsvorm}"


def id_from_path(path: Path) -> str | None:
    try:
        rel = path.resolve().relative_to(BIBLIOTHEEK_ROOT.resolve())
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


def _fm_value(text: str, key: str) -> str | None:
    in_fm = False
    prefix = f"{key.lower()}:"
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm and line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def alias_van_of(variant_id: str) -> str | None:
    index = variant_folder(variant_id) / "_index.md"
    if not index.is_file():
        return None
    raw = _fm_value(index.read_text(encoding="utf-8"), "alias_van")
    return raw or None


def under_alias_variant(path: Path) -> bool:
    try:
        rel = path.resolve().relative_to(BIBLIOTHEEK_ROOT.resolve())
    except ValueError:
        return False
    if len(rel.parts) < 2:
        return False
    try:
        return bool(alias_van_of(f"{rel.parts[0]}/{rel.parts[1]}"))
    except ValueError:
        return False


def resolve_id(value: str) -> str:
    """Herschrijf een uitvoeringsvorm-id via de variant-alias, anders ongewijzigd."""
    zangstuk, variant, uitvoeringsvorm = parse_id(value)
    target = alias_van_of(f"{zangstuk}/{variant}")
    if not target:
        return value
    tz, tv = parse_variant_id(target)
    return f"{tz}/{tv}/{uitvoeringsvorm}"


def leaf_folders() -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    if not BIBLIOTHEEK_ROOT.is_dir():
        return found
    for index in BIBLIOTHEEK_ROOT.rglob("index.md"):
        ident = id_from_path(index.parent)
        if not ident:
            continue
        if under_alias_variant(index.parent):
            continue
        found.append((ident, index.parent))
    return sorted(found, key=lambda item: item[0])


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def check_alias_variants() -> list[str]:
    """Fouten: alias_van alleen op variant-_index; doel bestaat; geen extra bestanden."""
    errors: list[str] = []
    if not BIBLIOTHEEK_ROOT.is_dir():
        return errors
    for path in sorted(BIBLIOTHEEK_ROOT.rglob("*")):
        if path.name not in {"_index.md", "index.md"}:
            continue
        try:
            parent_rel = path.parent.resolve().relative_to(
                BIBLIOTHEEK_ROOT.resolve()
            )
        except ValueError:
            continue
        depth = len(parent_rel.parts)
        text = path.read_text(encoding="utf-8")
        alias = _fm_value(text, "alias_van")
        alias_line = frontmatter_key_line(text, "alias_van")
        rel = _rel(path)
        if path.name == "index.md":
            if alias:
                errors.append(
                    format_issue(
                        rel,
                        "alias_van hoort op de variant-_index, "
                        "niet op een uitvoeringsvorm-index",
                        line=alias_line,
                        fix=(
                            "verplaats alias_van naar "
                            "zangstuk/variant/_index.md en verwijder het "
                            "hier"
                        ),
                    )
                )
            continue
        if not alias:
            continue
        if depth != 2:
            errors.append(
                format_issue(
                    rel,
                    "alias_van alleen op variant-_index "
                    "(zangstuk/variant), niet op deze laag",
                    line=alias_line,
                    fix="zet alias_van alleen op zangstuk/variant/_index.md",
                )
            )
            continue
        try:
            parse_variant_id(alias)
        except ValueError as exc:
            errors.append(
                format_issue(
                    rel,
                    f"alias_van ongeldig ({exc})",
                    line=alias_line,
                    fix="gebruik het formaat zangstuk/variant (kleine letters, streepjes)",
                )
            )
            continue
        self_id = parent_rel.as_posix()
        if alias == self_id:
            errors.append(
                format_issue(
                    rel,
                    "alias_van wijst naar zichzelf",
                    line=alias_line,
                    fix="wijs alias_van naar de canonieke variant, niet naar deze map",
                )
            )
            continue
        target_index = variant_folder(alias) / "_index.md"
        if not target_index.is_file():
            errors.append(
                format_issue(
                    rel,
                    f"alias_van {alias!r} heeft geen variant-_index",
                    line=alias_line,
                    fix=(
                        f"maak {_rel(target_index)} of corrigeer alias_van "
                        "naar een bestaande variant"
                    ),
                )
            )
            continue
        nested = _fm_value(
            target_index.read_text(encoding="utf-8"), "alias_van"
        )
        if nested:
            errors.append(
                format_issue(
                    rel,
                    f"alias_van {alias!r} is zelf een alias ({nested}); "
                    "geen ketens",
                    line=alias_line,
                    fix="wijs rechtstreeks naar de canonieke variant",
                )
            )
        for child in sorted(path.parent.iterdir()):
            if child.name == "_index.md" and child.is_file():
                continue
            errors.append(
                format_issue(
                    rel,
                    "alias-variant mag alleen _index.md bevatten "
                    f"(geen uitvoeringsvorm), gevonden {child.name}",
                    line=alias_line,
                    fix=(
                        "verwijder of verplaats bestanden/mappen naast "
                        "_index.md in deze alias-variant"
                    ),
                )
            )
    return errors


def main() -> int:
    errors = check_alias_variants()
    aliases = 0
    if BIBLIOTHEEK_ROOT.is_dir():
        for index in BIBLIOTHEEK_ROOT.rglob("_index.md"):
            try:
                rel = index.parent.resolve().relative_to(
                    BIBLIOTHEEK_ROOT.resolve()
                )
            except ValueError:
                continue
            if len(rel.parts) != 2:
                continue
            if _fm_value(index.read_text(encoding="utf-8"), "alias_van"):
                aliases += 1
    if errors:
        for line in errors:
            print(f"FAIL: {line}", flush=True)
        return 1
    print(f"Bibliotheek alias-varianten: {aliases} OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
