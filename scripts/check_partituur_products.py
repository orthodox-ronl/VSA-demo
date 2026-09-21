"""Controleer basispartituur-.mscz vs PDF/Coria-MXL via embedded partituur-sha256.

Schrijft data/partituur-product-status.json voor Hugo-banners.
Exit 1 bij problemen tenzij --warn-only (preview).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from export_mscz_coria_mxl import expand_mscz
from partituur_product_meta import (
    FIELD_GENERATED_AT,
    partituur_sha256,
    read_mxl_stamp,
    read_pdf_stamp,
    stamp_sha_from_dict,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "content-source"
STATUS_PATH = REPO_ROOT / "data" / "partituur-product-status.json"
FIX_PAGE = "/praktijk/handleiding/partituur/6-afgeleiden/"


@dataclass
class Issue:
    kind: str  # missing_pdf | missing_mxl | stale_pdf | stale_mxl | unstamped_pdf | unstamped_mxl
    file: str
    detail: str


@dataclass
class FolderStatus:
    dir: str
    mscz: str
    ok: bool
    issues: list[Issue]
    fix_cmd: str


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _bladermap_key(mscz: Path) -> str:
    """Pad relatief t.o.v. content-source, met trailing slash-achtige dir."""
    rel = mscz.parent.relative_to(REPO_ROOT / "content-source")
    return rel.as_posix()


def check_one(mscz: Path) -> FolderStatus:
    pdf = mscz.with_suffix(".pdf")
    mxl = mscz.with_suffix(".mxl")
    issues: list[Issue] = []
    digest = partituur_sha256(mscz)
    rel_mscz = _rel(mscz)
    fix = (
        f'scripts\\mscz-products.cmd "{mscz.parent.relative_to(REPO_ROOT)}"'
    )

    if not pdf.is_file():
        issues.append(
            Issue(
                "missing_pdf",
                _rel(pdf),
                "PDF ontbreekt naast de basispartituur-.mscz",
            )
        )
    else:
        stamp = read_pdf_stamp(pdf)
        got = stamp_sha_from_dict(stamp)
        if not got:
            issues.append(
                Issue(
                    "unstamped_pdf",
                    _rel(pdf),
                    "PDF heeft geen VSAPartituurSHA256-metadata (opnieuw genereren)",
                )
            )
        elif got != digest:
            when = stamp.get(FIELD_GENERATED_AT, "?")
            issues.append(
                Issue(
                    "stale_pdf",
                    _rel(pdf),
                    f"PDF-partituur-hash wijkt af (gegenereerd {when}); "
                    f"basispartituur is gewijzigd",
                )
            )

    if not mxl.is_file():
        issues.append(
            Issue(
                "missing_mxl",
                _rel(mxl),
                "Coria-.mxl ontbreekt naast de basispartituur-.mscz",
            )
        )
    else:
        stamp = read_mxl_stamp(mxl)
        got = stamp_sha_from_dict(stamp)
        if not got:
            issues.append(
                Issue(
                    "unstamped_mxl",
                    _rel(mxl),
                    "MXL heeft geen vsa-partituur-sha256 (opnieuw genereren)",
                )
            )
        elif got != digest:
            when = stamp.get(FIELD_GENERATED_AT, "?")
            issues.append(
                Issue(
                    "stale_mxl",
                    _rel(mxl),
                    f"MXL-partituur-hash wijkt af (gegenereerd {when}); "
                    f"basispartituur is gewijzigd",
                )
            )

    return FolderStatus(
        dir=_bladermap_key(mscz),
        mscz=rel_mscz,
        ok=not issues,
        issues=issues,
        fix_cmd=fix,
    )


def collect_statuses(root: Path) -> list[FolderStatus]:
    out: list[FolderStatus] = []
    for mscz in expand_mscz([root]):
        out.append(check_one(mscz))
    out.sort(key=lambda s: s.dir)
    return out


def write_status_json(statuses: list[FolderStatus], path: Path = STATUS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fix_page": FIX_PAGE,
        "folders": {
            s.dir: {
                "mscz": s.mscz,
                "ok": s.ok,
                "fix_cmd": s.fix_cmd,
                "issues": [asdict(i) for i in s.issues],
            }
            for s in statuses
        },
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _strict_env() -> bool:
    for key in ("VSA_PARTITUUR_PRODUCTS_STRICT", "VSA_PARTITUUR_PRODUCTS_STRICT"):
        if os.environ.get(key, "").strip().lower() in {"1", "true", "yes"}:
            return True
    return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="Zoekroot (default: content-source)",
    )
    p.add_argument(
        "--warn-only",
        action="store_true",
        help="Schrijf status-JSON maar exit altijd 0 (preview/lokaal)",
    )
    p.add_argument(
        "--fail",
        action="store_true",
        help="Non-zero bij problemen (productie / main)",
    )
    args = p.parse_args()
    root = args.root if args.root.is_absolute() else REPO_ROOT / args.root
    statuses = collect_statuses(root)
    write_status_json(statuses)
    bad = [s for s in statuses if not s.ok]
    print(
        f"Basispartituur-producten: {len(statuses) - len(bad)} ok, {len(bad)} probleem "
        f"({STATUS_PATH.relative_to(REPO_ROOT).as_posix()})",
        flush=True,
    )
    for s in bad:
        print(f"  {s.dir}:", flush=True)
        for issue in s.issues:
            print(f"    - [{issue.kind}] {issue.file}: {issue.detail}", flush=True)
        print(f"    Fix: {s.fix_cmd}", flush=True)
        print(f"    Zie: {FIX_PAGE}", flush=True)

    if not bad:
        return 0
    if args.warn_only:
        return 0
    if args.fail:
        return 1
    # Productie op GitHub main: streng. Elders (lokaal/preview): banner only.
    ref = (
        os.environ.get("GITHUB_REF", "")
        or os.environ.get("GITHUB_REF_NAME", "")
        or ""
    )
    if ref in {"main", "refs/heads/main"}:
        return 1
    if _strict_env():
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
