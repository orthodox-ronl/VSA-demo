"""Zet bibliotheek-id in hub-.mscz colofon/meta; optioneel alleen controleren.

Hubs onder `oefenhoek/bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/`.
Lokaal (niet-CI): ontbrekende/verkeerde id -> `process_mscz` (geen MuseScore).
CI / `--check-only`: alleen rapporteren. Exit 1 op main / `--fail` /
`VSA_BIBLIOTHEEK_ID_STRICT` als er nog problemen zijn.

Contract: scripts/mscz-hub-contract.md, scripts/oefenhoek-product-contract.md.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from apply_mscz_layout import bibliotheek_id_status, process_mscz
from bibliotheek import BIBLIOTHEEK_ROOT, id_from_path
from export_mscz_coria_mxl import expand_mscz
from score_filenames import is_print_mscz

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX_PAGE = "/praktijk/handleiding/partituur/3-standaard-mscz/"


def _running_in_ci() -> bool:
    return os.environ.get("CI", "").strip().lower() in {"1", "true", "yes"}


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def collect_hubs(root: Path) -> list[tuple[Path, str]]:
    """(hub-.mscz, expected bibliotheek-id) voor scores in de bibliotheekboom."""
    out: list[tuple[Path, str]] = []
    for mscz in expand_mscz([root]):
        if is_print_mscz(mscz):
            continue
        ident = id_from_path(mscz)
        if not ident:
            continue
        out.append((mscz, ident))
    out.sort(key=lambda item: item[1])
    return out


def _strict_exit() -> bool:
    ref = (
        os.environ.get("GITHUB_REF", "")
        or os.environ.get("GITHUB_REF_NAME", "")
        or ""
    )
    if ref in {"main", "refs/heads/main"}:
        return True
    if os.environ.get("VSA_BIBLIOTHEEK_ID_STRICT", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        return True
    if os.environ.get("PIPELINE_STRICT", "").strip():
        return True
    return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=BIBLIOTHEEK_ROOT,
        help="Zoekroot (default: oefenhoek/bibliotheek)",
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="Niet herschrijven; alleen controleren",
    )
    p.add_argument(
        "--fail",
        action="store_true",
        help="Non-zero bij problemen (naast main/strict)",
    )
    p.add_argument(
        "--warn-only",
        action="store_true",
        help="Altijd exit 0 (preview)",
    )
    args = p.parse_args()
    root = args.root if args.root.is_absolute() else REPO_ROOT / args.root
    hubs = collect_hubs(root)
    write = not args.check_only and not _running_in_ci()

    fixed = 0
    bad: list[tuple[Path, str, str]] = []
    for mscz, expected in hubs:
        ok, detail = bibliotheek_id_status(mscz, expected)
        if ok:
            continue
        if write:
            print(f"fix {_rel(mscz)} -> {expected}", flush=True)
            process_mscz(mscz, bibliotheek_id=expected)
            ok2, detail2 = bibliotheek_id_status(mscz, expected)
            if ok2:
                fixed += 1
                continue
            bad.append((mscz, expected, detail2))
        else:
            bad.append((mscz, expected, detail))

    print(
        f"Bibliotheek-id: {len(hubs) - len(bad)} ok, {fixed} hersteld, "
        f"{len(bad)} probleem",
        flush=True,
    )
    for mscz, expected, detail in bad:
        print(f"  [{expected}] {_rel(mscz)}: {detail}", flush=True)
        print(
            f"    Fix: python scripts\\apply_mscz_layout.py \"{_rel(mscz)}\"",
            flush=True,
        )
        print(f"    Zie: {FIX_PAGE}", flush=True)

    if not bad or args.warn_only:
        return 0
    if args.fail or _strict_exit():
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
