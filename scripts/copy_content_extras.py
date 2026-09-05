"""Copy page-bundle extras that vsa build-markdown does not copy (e.g. .mxl)."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "content-source"
DEST = REPO_ROOT / "generated" / "content"
EXTRA_SUFFIXES = {".mxl"}


def main() -> int:
    if not SOURCE.is_dir() or not DEST.is_dir():
        print("FAIL: content-source of generated/content ontbreekt.", flush=True)
        return 1
    copied = 0
    for path in SOURCE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTRA_SUFFIXES:
            continue
        target = DEST / path.relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1
    print(f"Page-bundle extras: {copied} bestand(en)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
