"""Publish Coria scores as /mxl/c/<md5>.musicxml (uncompressed XML).

Coria play_from_url rejects URLs that do not end in .xml/.mxl/.musicxml
(query strings) and cannot fetch GitHub paths with spaces or %2520.
A single ASCII filename under /mxl/c/ avoids all of that; the hash
changes when file bytes change, so Coria loads fresh lyrics.

Coria's importer ("translation failed") is unreliable on compressed
.mxl ZIP for some scores (Cherubijnenhymne Kastorski). Uncompressed
MusicXML 3.1 from the same payload loads. We always serve that.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
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


def _fingerprint(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()[:12]


def _payload_for_coria(path: Path) -> bytes:
    if path.suffix.lower() != ".mxl":
        return path.read_bytes()
    try:
        with zipfile.ZipFile(path) as z:
            names = [
                n
                for n in z.namelist()
                if n.endswith((".xml", ".musicxml")) and not n.startswith("META")
            ]
            if not names:
                raise ValueError(f"geen MusicXML in {path}")
            return z.read(names[0])
    except zipfile.BadZipFile:
        return path.read_bytes()


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
        payload = _payload_for_coria(path)
        fp = _fingerprint(payload)
        target = DEST_ROOT / f"{fp}.musicxml"
        if not target.exists():
            target.write_bytes(payload)
        mapping[key] = f"{URL_PREFIX}/{fp}.musicxml"

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(mapping, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Coria MusicXML fingerprints: {len(mapping)} bestand(en)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
