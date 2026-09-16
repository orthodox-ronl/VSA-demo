"""Controleer bibliotheek-.vsa vs sibling `{stam}.vsa.mxl` via source-sha256.

Schrijft data/vsa-product-status.json voor Hugo-banners.
Slaat artefacten_handmatig over. Exit 1 bij problemen tenzij --warn-only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from hub_product_meta import (
    FIELD_GENERATED_AT,
    FIELD_SOURCE_KIND,
    FIELD_SOURCE_SHA,
    SOURCE_KIND_VSA,
    read_mxl_stamp,
    source_sha256,
)
from sync_vsa_products import (
    DEFAULT_ROOT,
    collect_vsa,
    product_path_for_vsa,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = REPO_ROOT / "data" / "vsa-product-status.json"
FIX_PAGE = "/praktijk/handleiding/vsa/1-vsa-schrijven/"


@dataclass
class Issue:
    kind: str  # missing_mxl | stale_mxl | unstamped_mxl | wrong_kind
    file: str
    detail: str


@dataclass
class FolderStatus:
    dir: str
    vsa: str
    ok: bool
    issues: list[Issue]
    fix_cmd: str


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _bladermap_key(vsa: Path) -> str:
    rel = vsa.parent.relative_to(REPO_ROOT / "content-source")
    return rel.as_posix()


def check_one(vsa: Path) -> FolderStatus:
    mxl = product_path_for_vsa(vsa)
    issues: list[Issue] = []
    src_hash = source_sha256(vsa)
    fix = r'scripts\vsa-products.cmd'
    if not mxl.is_file():
        issues.append(
            Issue(
                "missing_mxl",
                _rel(mxl),
                "Coria-.vsa.mxl ontbreekt naast de bibliotheek-.vsa",
            )
        )
    else:
        stamp = read_mxl_stamp(mxl)
        kind = stamp.get(FIELD_SOURCE_KIND, "")
        got = stamp.get(FIELD_SOURCE_SHA, "")
        if not got:
            issues.append(
                Issue(
                    "unstamped_mxl",
                    _rel(mxl),
                    "MXL heeft geen vsa-source-sha256 (opnieuw genereren)",
                )
            )
        elif kind and kind != SOURCE_KIND_VSA:
            issues.append(
                Issue(
                    "wrong_kind",
                    _rel(mxl),
                    f"MXL source-kind is {kind!r}, verwacht {SOURCE_KIND_VSA!r}",
                )
            )
        elif got != src_hash:
            when = stamp.get(FIELD_GENERATED_AT, "?")
            issues.append(
                Issue(
                    "stale_mxl",
                    _rel(mxl),
                    f"MXL-source-hash wijkt af (gegenereerd {when}); .vsa is gewijzigd",
                )
            )
    return FolderStatus(
        dir=_bladermap_key(vsa),
        vsa=_rel(vsa),
        ok=not issues,
        issues=issues,
        fix_cmd=fix,
    )


def collect_statuses(root: Path) -> list[FolderStatus]:
    # Eén status per bladermap (meerdere .vsa zeldzaam; dan laatste wint + issues mergen)
    by_dir: dict[str, FolderStatus] = {}
    for vsa in collect_vsa(root):
        status = check_one(vsa)
        prev = by_dir.get(status.dir)
        if prev is None:
            by_dir[status.dir] = status
            continue
        merged_issues = list(prev.issues) + list(status.issues)
        by_dir[status.dir] = FolderStatus(
            dir=status.dir,
            vsa=prev.vsa + "; " + status.vsa,
            ok=not merged_issues,
            issues=merged_issues,
            fix_cmd=status.fix_cmd,
        )
    return sorted(by_dir.values(), key=lambda s: s.dir)


def write_status_json(statuses: list[FolderStatus], path: Path = STATUS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fix_page": FIX_PAGE,
        "folders": {
            s.dir: {
                "vsa": s.vsa,
                "ok": s.ok,
                "fix_cmd": s.fix_cmd,
                "issues": [asdict(i) for i in s.issues],
            }
            for s in statuses
        },
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="Zoekroot (default: oefenhoek/bibliotheek)",
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
        f"VSA-producten: {len(statuses) - len(bad)} ok, {len(bad)} probleem "
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
    ref = (
        os.environ.get("GITHUB_REF", "")
        or os.environ.get("GITHUB_REF_NAME", "")
        or ""
    )
    if ref in {"main", "refs/heads/main"}:
        return 1
    if os.environ.get("VSA_HUB_PRODUCTS_STRICT", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
