"""Controleer dat gecommitte demo-PDF's niet ouder zijn dan hun bronnen.

Faalt met het precieze regeneratiecommando (scripts\\demo-pdf.cmd).
Wordt aangeroepen vanuit scripts\\_pipeline.cmd (check / build / serve).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DemoPdf:
    pdf: Path
    sources: tuple[Path, ...]
    fix_cmd: str


# Bekende handmatige PDF-demo's: pipeline bouwt ze niet, checkt wel freshness.
DEMO_PDFS: tuple[DemoPdf, ...] = (
    DemoPdf(
        pdf=Path("static/demo/voorbeeld-blad.pdf"),
        sources=(
            Path("content-source/praktijk/demo/assets/voorbeeld-blad.md"),
            Path("content-source/praktijk/demo/assets/voorbeeld.vsa"),
        ),
        fix_cmd="scripts\\demo-pdf.cmd",
    ),
)


def _rel(path: Path) -> str:
    return str(path).replace("/", "\\")


def check_one(entry: DemoPdf) -> list[str]:
    errors: list[str] = []
    pdf = REPO_ROOT / entry.pdf
    if not pdf.is_file():
        errors.append(f"Ontbreekt: {_rel(entry.pdf)}")
        errors.append(f"Bouw met: {entry.fix_cmd}")
        return errors

    pdf_mtime = pdf.stat().st_mtime
    newer: list[Path] = []
    missing: list[Path] = []
    for src in entry.sources:
        full = REPO_ROOT / src
        if not full.is_file():
            missing.append(src)
            continue
        if full.stat().st_mtime > pdf_mtime:
            newer.append(src)

    if missing:
        errors.append(f"Bronbestanden ontbreken voor {_rel(entry.pdf)}:")
        for src in missing:
            errors.append(f"  - {_rel(src)}")
    if newer:
        errors.append(f"Verouderd: {_rel(entry.pdf)}")
        errors.append("Nieuwer dan de PDF:")
        for src in newer:
            errors.append(f"  - {_rel(src)}")
        errors.append(f"Bouw opnieuw met: {entry.fix_cmd}")
    return errors


def main() -> int:
    all_errors: list[str] = []
    for entry in DEMO_PDFS:
        all_errors.extend(check_one(entry))

    if all_errors:
        print("ERROR: demo-PDF niet up-to-date.", file=sys.stderr)
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1

    for entry in DEMO_PDFS:
        print(f"OK: {_rel(entry.pdf)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
