"""Maak PDF en Coria-MXL in bladermappen gelijk aan hun .mscz.

Per publicatie-.mscz (niet oefenhoek/input/): bestaande sibling-.pdf /
sibling-.mxl opnieuw exporteren als ze ontbreken of ouder zijn dan de .mscz.
Zonder MuseScore: op CI overslaan; lokaal falen als er stale producten zijn.

Aangeroepen vanuit scripts\\_pipeline.cmd (check / build / serve).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from export_mscz_coria_mxl import (
    expand_score_files,
    find_musescore,
    musescore_export,
    process,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "content-source"


def _running_in_ci() -> bool:
    return os.environ.get("CI", "").strip().lower() in {"1", "true", "yes"}


def _find_musescore() -> Path | None:
    try:
        return find_musescore()
    except SystemExit:
        return None


def _sibling_product(mscz: Path, suffix: str) -> Path | None:
    same = mscz.with_suffix(suffix)
    if same.is_file():
        return same
    found = sorted(p for p in mscz.parent.glob(f"*{suffix}") if p.is_file())
    if len(found) == 1:
        return found[0]
    if found:
        return None
    return same


def _is_stale(product: Path, mscz: Path) -> bool:
    if not product.is_file():
        return True
    return product.stat().st_mtime < mscz.stat().st_mtime


def collect_jobs(root: Path) -> list[tuple[Path, Path | None, Path | None]]:
    jobs: list[tuple[Path, Path | None, Path | None]] = []
    for mscz in expand_score_files([root], ".mscz"):
        pdf = _sibling_product(mscz, ".pdf")
        mxl = _sibling_product(mscz, ".mxl")
        if pdf is None and mxl is None:
            continue
        jobs.append((mscz, pdf, mxl))
    return jobs


def stale_jobs(
    jobs: list[tuple[Path, Path | None, Path | None]],
) -> list[tuple[Path, Path | None, Path | None]]:
    out: list[tuple[Path, Path | None, Path | None]] = []
    for mscz, pdf, mxl in jobs:
        need_pdf = pdf is not None and _is_stale(pdf, mscz)
        need_mxl = mxl is not None and _is_stale(mxl, mscz)
        if need_pdf or need_mxl:
            out.append(
                (
                    mscz,
                    pdf if need_pdf else None,
                    mxl if need_mxl else None,
                )
            )
    return out


def sync_one(
    mscz: Path,
    pdf: Path | None,
    mxl: Path | None,
    musescore: Path,
    *,
    dry_run: bool,
) -> None:
    rel = mscz.relative_to(REPO_ROOT)
    if pdf is not None:
        print(f"  PDF  {rel} -> {pdf.name}", flush=True)
        if not dry_run:
            musescore_export(mscz, pdf, musescore)
    if mxl is not None:
        print(f"  MXL  {rel} -> {mxl.name}", flush=True)
        if not dry_run:
            process(mscz, mxl)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Exporteer stale PDF/Coria-MXL vanuit publicatie-.mscz."
    )
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="Zoekroot (default: content-source)",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--force",
        action="store_true",
        help="Ook exporteren als producten nieuwer zijn",
    )
    args = p.parse_args()
    root = args.root if args.root.is_absolute() else REPO_ROOT / args.root
    jobs = collect_jobs(root)
    todo = jobs if args.force else stale_jobs(jobs)
    if not todo:
        print(f"MSCZ-producten up-to-date ({len(jobs)} .mscz)", flush=True)
        return 0

    musescore = _find_musescore()
    if musescore is None:
        print(f"{len(todo)} stale PDF/MXL t.o.v. .mscz, MuseScore ontbreekt.", flush=True)
        if _running_in_ci():
            print("CI: sla lokale MuseScore-export over.", flush=True)
            return 0
        print(
            r"Installeer MuseScore 4 of regenereer met "
            r"python scripts\sync_mscz_products.py",
            flush=True,
        )
        for mscz, pdf, mxl in todo:
            bits = [mscz.name]
            if pdf is not None:
                bits.append(pdf.name)
            if mxl is not None:
                bits.append(mxl.name)
            print(f"  - {' / '.join(bits)}", flush=True)
        return 1

    print(f"using {musescore}", flush=True)
    print(f"MSCZ-producten bijwerken: {len(todo)} van {len(jobs)}", flush=True)
    failed = 0
    for mscz, pdf, mxl in todo:
        print(f"== {mscz.relative_to(REPO_ROOT)}", flush=True)
        try:
            sync_one(mscz, pdf, mxl, musescore, dry_run=args.dry_run)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED {exc}", flush=True)
            failed += 1
    if failed:
        print(f"{failed} mislukt van {len(todo)}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
