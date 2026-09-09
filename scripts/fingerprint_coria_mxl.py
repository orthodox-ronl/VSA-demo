"""Copy native/generated MXL under a content-hash path for Coria.

Coria play_from_url requires the URL to end in .mxl/.xml/.musicxml, so a
query-string cache buster is rejected. A path segment /c/<hash>/ keeps the
suffix and still changes the URL when lyrics change.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "coria-fp.json"
SUFFIXES = {".mxl", ".musicxml"}
TREES = (
    (REPO_ROOT / "static" / "mxl", "mxl"),
    (REPO_ROOT / "static" / "vsa" / "mxl", "vsa/mxl"),
)


def _fingerprint(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


def _copy_tree(root: Path, url_prefix: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    cache_root = root / "c"
    if cache_root.exists():
        shutil.rmtree(cache_root)
    if not root.is_dir():
        return mapping
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] == "c":
            continue
        fp = _fingerprint(path)
        target = cache_root / fp / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        key = f"{url_prefix}/{relative.as_posix()}".replace("/", "__")
        mapping[key] = fp
    return mapping


def main() -> int:
    mapping: dict[str, str] = {}
    for root, url_prefix in TREES:
        mapping.update(_copy_tree(root, url_prefix))
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(mapping, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Coria MXL fingerprints: {len(mapping)} bestand(en)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
