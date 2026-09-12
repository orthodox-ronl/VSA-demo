"""Faal als een publicatie-.mxl markup heeft waar Coria op crasht.

Coria meldt dan 'Fout: translation failed'. Ruwe dumps in oefenhoek/input/
worden overgeslagen. Zie export_mscz_coria_mxl.sanitize_coria_importer.
"""
from __future__ import annotations

import sys
from pathlib import Path

from export_mscz_coria_mxl import (
    coria_importer_violations,
    expand_score_files,
    load_score_xml,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "content-source"


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    files = expand_score_files([root], ".mxl")
    failed = 0
    for path in files:
        try:
            violations = coria_importer_violations(load_score_xml(path))
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {path}: {exc}")
            failed += 1
            continue
        if violations:
            print(f"FAIL {path}: Coria-onveilige markup: {', '.join(violations)}")
            failed += 1
    if failed:
        print(
            f"{failed} onveilige .mxl. Maak schoon met: "
            "python scripts/export_mscz_coria_mxl.py --sanitize-mxl content-source"
        )
        return 1
    print(f"Coria-MXL check OK ({len(files)} bestand(en))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
