"""Publish Coria scores as /mxl/c/<md5>.musicxml (uncompressed XML).

Coria play_from_url rejects URLs that do not end in .xml/.mxl/.musicxml
(query strings) and cannot fetch GitHub paths with spaces or %2520.
A single ASCII filename under /mxl/c/ avoids all of that; the hash
changes when file bytes change, so Coria loads fresh lyrics.

Coria's importer ("translation failed") is unreliable on compressed
.mxl ZIP for some scores (Cherubijnenhymne Kastorski). Uncompressed
MusicXML 3.1 from the same payload loads. We always serve that.

Coria haalt het bestand server-side op: de Oefenen-knop moet een
publieke https-URL zijn, niet /mxl/c/… of localhost. github.io is de
site voor mensen; Coria's server faalt daar regelmatig met
"failed to retrieve file". Oefenen gebruikt daarom raw.githubusercontent.com
op branch gh-pages (zelfde mappen als pages.yml: root / preview / slug).
Die fetch-root staat in data/coria-public-base.json.

Bronnen:
- content-source/**/*.mxl (niet oefenhoek/input/) — page-bundle Coria-.mxl
- static/mxl/** (legacy/extra)
- static/vsa/mxl/** (vsa musicxml)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_ROOT / "data" / "coria-fp.json"
PUBLIC_BASE_FILE = REPO_ROOT / "data" / "coria-public-base.json"
DEST_ROOT = REPO_ROOT / "static" / "mxl" / "c"
CONTENT_SOURCE = REPO_ROOT / "content-source"
URL_PREFIX = "mxl/c"
SUFFIXES = {".mxl", ".musicxml"}
# (root, url_prefix_for_key) — key wordt prefix/relpath met / -> __
SOURCE_TREES = (
    (REPO_ROOT / "static" / "mxl", "mxl"),
    (REPO_ROOT / "static" / "vsa" / "mxl", "vsa/mxl"),
)

# Keep in sync with .github/workflows/pages.yml (Determine deploy target).
PAGES_ROOT = "https://orthodox-ronl.github.io/VSA-demo"
RAW_ROOT = "https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages"
RESERVED_SLUGS = frozenset(
    {
        "preview",
        "main",
        "gh-pages",
        "development",
        "coria",
        "css",
        "demo",
        "images",
        "js",
        "mxl",
        "praktijk",
        "vsa",
    }
)


def _pages_subdir(branch: str) -> str:
    """Map onder gh-pages / github.io voor deze git-branch (leeg = site-root)."""
    branch = (branch or "").strip()
    if branch == "main":
        return ""
    if branch == "development":
        return "preview"
    slug = re.sub(r"[^a-z0-9_-]+", "-", branch.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError(f"Branchnaam {branch!r} levert geen URL-slug op.")
    if slug in RESERVED_SLUGS:
        slug = f"b-{slug}"
    return slug


def _join_root(root: str, subdir: str) -> str:
    root = root.rstrip("/")
    if subdir:
        return f"{root}/{subdir}/"
    return f"{root}/"


def github_pages_base_url(branch: str) -> str:
    """Publieke site-root voor mensen in de browser (trailing slash)."""
    return _join_root(PAGES_ROOT, _pages_subdir(branch))


def coria_fetch_base_url(branch: str) -> str:
    """Host die Coria server-side mag ophalen (trailing slash)."""
    return _join_root(RAW_ROOT, _pages_subdir(branch))


def detect_git_branch() -> str:
    """Branch voor Pages-URL: PR-head, GITHUB_REF, anders lokale git."""
    head_ref = os.environ.get("GITHUB_HEAD_REF", "").strip()
    if head_ref:
        return head_ref
    ref = os.environ.get("GITHUB_REF", "").strip()
    if ref.startswith("refs/heads/"):
        return ref[len("refs/heads/") :]
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    branch = (result.stdout or "").strip()
    if result.returncode == 0 and branch and branch != "HEAD":
        return branch
    raise SystemExit(
        "FAIL: git-branch onbekend; Coria-public-base kan niet bepaald worden."
    )


def write_public_base(branch: str | None = None) -> str:
    base = coria_fetch_base_url(branch or detect_git_branch())
    PUBLIC_BASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_BASE_FILE.write_text(
        json.dumps({"base": base}, indent=2) + "\n",
        encoding="utf-8",
    )
    return base


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
    seen_keys: set[str] = set()

    def add(key: str, path: Path) -> None:
        if key in seen_keys:
            return
        seen_keys.add(key)
        files.append((key, path))

    if CONTENT_SOURCE.is_dir():
        for path in sorted(CONTENT_SOURCE.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUFFIXES:
                continue
            relative = path.relative_to(CONTENT_SOURCE)
            if "input" in relative.parts:
                continue
            key = f"mxl/{relative.as_posix()}".replace("/", "__")
            add(key, path)

    for root, prefix in SOURCE_TREES:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUFFIXES:
                continue
            relative = path.relative_to(root)
            if relative.parts and relative.parts[0] == "c":
                continue
            key = f"{prefix}/{relative.as_posix()}".replace("/", "__")
            add(key, path)

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
    public_base = write_public_base()
    print(
        f"Coria MusicXML fingerprints: {len(mapping)} bestand(en); "
        f"public base {public_base}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
