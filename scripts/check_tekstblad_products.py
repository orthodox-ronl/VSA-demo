"""Controleer bibliotheek-`.tekstblad.md` vs sibling `{stam}.tekstblad.pdf`.

Schrijft data/tekstblad-product-status.json voor Hugo-banners.
Slaat artefacten_handmatig over. Exit 1 bij problemen tenzij --warn-only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from partituur_product_meta import (
    FIELD_SOURCE_KIND,
    FIELD_SOURCE_SHA,
    SOURCE_KIND_TEKSTBLAD,
    read_pdf_stamp,
    source_sha256,
)
from score_filenames import tekstblad_pdf_for_md
from sync_tekstblad_products import DEFAULT_ROOT, collect_tekstblad

REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = REPO_ROOT / "data" / "tekstblad-product-status.json"
FIX_PAGE = "/praktijk/handleiding/werktrajecten/tekstblad/"


@dataclass
class Issue:
    kind: str  # missing_pdf | stale_pdf | unstamped_pdf | wrong_kind
    file: str
    detail: str


@dataclass
class FolderStatus:
    dir: str
    source: str
    ok: bool
    issues: list[Issue]
    fix_cmd: str


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _bladermap_key(md: Path) -> str:
    rel = md.parent.relative_to(REPO_ROOT / "content-source")
    return rel.as_posix()


def check_one(md: Path) -> FolderStatus:
    pdf = tekstblad_pdf_for_md(md)
    issues: list[Issue] = []
    src_hash = source_sha256(md)
    fix = r"scripts\tekstblad-products.cmd"
    if not pdf.is_file():
        issues.append(
            Issue(
                "missing_pdf",
                _rel(pdf),
                "tekstblad-PDF ontbreekt naast de .tekstblad.md",
            )
        )
    else:
        stamp = read_pdf_stamp(pdf)
        kind = stamp.get(FIELD_SOURCE_KIND, "")
        got = stamp.get(FIELD_SOURCE_SHA, "")
        if not got:
            issues.append(
                Issue(
                    "unstamped_pdf",
                    _rel(pdf),
                    "PDF mist vsa-source-sha256 (opnieuw tekstblad-products)",
                )
            )
        elif got != src_hash:
            issues.append(
                Issue(
                    "stale_pdf",
                    _rel(pdf),
                    "PDF hoort niet bij de huidige .tekstblad.md",
                )
            )
        if kind and kind != SOURCE_KIND_TEKSTBLAD:
            issues.append(
                Issue(
                    "wrong_kind",
                    _rel(pdf),
                    f"vsa-source-kind={kind!r}, verwacht {SOURCE_KIND_TEKSTBLAD!r}",
                )
            )
    return FolderStatus(
        dir=_bladermap_key(md),
        source=_rel(md),
        ok=not issues,
        issues=issues,
        fix_cmd=fix,
    )


def write_status(folders: list[FolderStatus]) -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "folders": [
            {
                **asdict(f),
                "issues": [asdict(i) for i in f.issues],
            }
            for f in folders
        ],
        "fix_page": FIX_PAGE,
    }
    STATUS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check tekstblad-PDF's tegen .tekstblad.md"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help="zoekroot (default: oefenhoek/bibliotheek)",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="schrijf status, exit 0 ook bij problemen",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_absolute():
        root = (REPO_ROOT / root).resolve()

    folders = [check_one(md) for md in collect_tekstblad(root)]
    write_status(folders)

    bad = [f for f in folders if not f.ok]
    if not bad:
        print(f"OK: {len(folders)} tekstblad-map(pen)", flush=True)
        return 0

    for f in bad:
        print(f"FAIL: {f.dir}", flush=True)
        for issue in f.issues:
            print(f"  {issue.kind}: {issue.file} — {issue.detail}", flush=True)
        print(f"  Herstel: {f.fix_cmd}", flush=True)
        print(f"  Handleiding: {FIX_PAGE}", flush=True)

    if args.warn_only or os.environ.get("TEKSTBLAD_PRODUCTS_WARN_ONLY") == "1":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
