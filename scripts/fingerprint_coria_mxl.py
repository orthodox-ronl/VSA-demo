"""Publish Coria MXL as /mxl/c/<md5>.mxl (URL always ends with .mxl).

Coria play_from_url rejects URLs that do not end in .xml/.mxl/.musicxml
(query strings) and cannot fetch GitHub paths with spaces or %2520.
A single ASCII filename under /mxl/c/ avoids all of that; the hash
changes when file bytes change, so Coria loads fresh lyrics.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "coria-fp.json"
DEST_ROOT = REPO_ROOT / "static" / "mxl" / "c"
URL_PREFIX = "mxl/c"
SUFFIXES = {".mxl", ".musicxml"}
SOURCE_TREES = (
    REPO_ROOT / "static" / "mxl",
    REPO_ROOT / "static" / "vsa" / "mxl",
)


def _fingerprint(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


def _iter_source_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for root in SOURCE_TREES:
        if not root.is_dir():
            continue
        prefix = "mxl" if root == SOURCE_TREES[0] else "vsa/mxl"
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUFFIXES:
                continue
            relative = path.relative_to(root)
            if relative.parts and relative.parts[0] == "c":
                continue
            key = f"{prefix}/{relative.as_posix()}".replace("/", "__")
            files.append((key, path))
    return files


def main() -> int:
    if DEST_ROOT.exists():
        shutil.rmtree(DEST_ROOT)
    DEST_ROOT.mkdir(parents=True, exist_ok=True)

    mapping: dict[str, str] = {}
    for key, path in _iter_source_files():
        fp = _fingerprint(path)
        target = DEST_ROOT / f"{fp}.mxl"
        if not target.exists():
            shutil.copy2(path, target)
        mapping[key] = f"{URL_PREFIX}/{fp}.mxl"

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(mapping, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Coria MXL fingerprints: {len(mapping)} bestand(en)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
