"""Maak PDF en Coria-MXL bij een basispartituur-.mscz (na de editslag).

Wrapper: `scripts\\mscz-products.cmd`. Wordt ook vanuit de pipeline
aangeroepen (lokaal, met MuseScore). Op CI zonder MuseScore: overslaan.

Per basispartituur-`.mscz` onder content-source (niet `oefenhoek/input/`, niet
`*.print.mscz`): sibling-.pdf en Coria-.mxl. Na bibliotheek-migratie liggen
basispartituren onder
`oefenhoek/bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/`.
Freshness voor de gate zit in embedded partituur-sha256
(zie partituur_product_meta.py); lokaal skip gebruikt FS-mtime of
ontbrekende/verkeerde stamp.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from export_mscz_coria_mxl import (
    expand_mscz,
    find_musescore,
    load_score_xml,
    musescore_export,
    process,
    write_mxl,
)
from apply_mscz_layout import write_mscz_with_all_pages_footer
from partituur_product_meta import (
    partituur_sha256,
    read_mxl_stamp,
    read_pdf_stamp,
    stamp_mxl_tree,
    stamp_pdf,
    stamp_sha_from_dict,
    utc_now_iso,
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


def _sibling_product(mscz: Path, suffix: str) -> Path:
    """Zelfde stam als de .mscz (aanmaken mag)."""
    return mscz.with_suffix(suffix)


def _stamp_matches(product: Path, digest: str, *, kind: str) -> bool:
    if not product.is_file():
        return False
    if kind == "pdf":
        stamp = read_pdf_stamp(product)
    else:
        stamp = read_mxl_stamp(product)
    return stamp_sha_from_dict(stamp) == digest


def _is_stale(product: Path, mscz: Path, digest: str, *, kind: str) -> bool:
    if not product.is_file():
        return True
    if _stamp_matches(product, digest, kind=kind):
        return False
    # Geen/verkeerde stamp: regenerate. Mtime alleen als hint dat het
    # sowieso ouder is; mismatch stamp wint altijd.
    return True


def collect_jobs(root: Path) -> list[tuple[Path, Path, Path]]:
    jobs: list[tuple[Path, Path, Path]] = []
    for mscz in expand_mscz([root]):
        jobs.append(
            (
                mscz,
                _sibling_product(mscz, ".pdf"),
                _sibling_product(mscz, ".mxl"),
            )
        )
    return jobs


def stale_jobs(
    jobs: list[tuple[Path, Path | None, Path | None]],
) -> list[tuple[Path, Path | None, Path | None]]:
    out: list[tuple[Path, Path | None, Path | None]] = []
    for mscz, pdf, mxl in jobs:
        digest = partituur_sha256(mscz)
        need_pdf = pdf is not None and _is_stale(pdf, mscz, digest, kind="pdf")
        need_mxl = mxl is not None and _is_stale(mxl, mscz, digest, kind="mxl")
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
    digest = partituur_sha256(mscz)
    generated_at = utc_now_iso()
    if pdf is not None:
        print(f"  PDF  {rel} -> {pdf.name}", flush=True)
        if not dry_run:
            # Temp-kopie: letterlijke copyright-footer op alle pagina's ($C = alleen p.1).
            with tempfile.TemporaryDirectory(prefix="vsa-pdf-") as td:
                tmp = Path(td) / mscz.name
                write_mscz_with_all_pages_footer(mscz, tmp)
                musescore_export(tmp, pdf, musescore)
            stamp_pdf(pdf, partituur_hash=digest, generated_at=generated_at)
    if mxl is not None:
        print(f"  MXL  {rel} -> {mxl.name}", flush=True)
        if not dry_run:
            process(mscz, mxl)
            root = load_score_xml(mxl)
            stamp_mxl_tree(root, partituur_hash=digest, generated_at=generated_at)
            write_mxl(mxl, root)


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
            r"scripts\mscz-products.cmd",
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
