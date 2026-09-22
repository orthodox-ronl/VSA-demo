"""Maak `{stam}.tekstblad.pdf` bij bibliotheek-`{stam}.tekstblad.md`.

Representatie-id: tekstblad. Renderer: ``vsa pdf`` (zelfde als pdf.cmd).
Slaat ``oefenhoek/input/`` en mappen met ``artefacten_handmatig: true`` over.

Lokaal (pipeline): stale producten vernieuwen. CI: niet regenereren; gate via
``check_tekstblad_products.py``. Commit bron + PDF samen.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from bibliotheek import under_alias_variant
from partituur_product_meta import (
    FIELD_SOURCE_KIND,
    FIELD_SOURCE_SHA,
    GENERATOR_TEKSTBLAD,
    SOURCE_KIND_TEKSTBLAD,
    read_pdf_stamp,
    source_sha256,
    stamp_pdf,
    utc_now_iso,
)
from score_filenames import (
    is_tekstblad_md,
    require_no_spaces,
    tekstblad_pdf_for_md,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = (
    REPO_ROOT / "content-source" / "praktijk" / "oefenhoek" / "bibliotheek"
)


def _fm_bool(text: str, key: str) -> bool:
    in_fm = False
    prefix = f"{key.lower()}:"
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm and line.lower().startswith(prefix):
            val = line.split(":", 1)[1].strip().strip("\"'").lower()
            return val in {"true", "1", "yes"}
    return False


def folder_is_handmatig(folder: Path) -> bool:
    index = folder / "index.md"
    if not index.is_file():
        return False
    try:
        return _fm_bool(index.read_text(encoding="utf-8"), "artefacten_handmatig")
    except OSError:
        return False


def collect_tekstblad(root: Path) -> list[Path]:
    out: list[Path] = []
    if not root.is_dir():
        return out
    for path in sorted(root.rglob("*")):
        if not path.is_file() or not is_tekstblad_md(path):
            continue
        if "input" in path.parts:
            continue
        if folder_is_handmatig(path.parent):
            continue
        if under_alias_variant(path):
            continue
        require_no_spaces(path)
        out.append(path)
    return out


def needs_rebuild(md: Path, pdf: Path) -> bool:
    if not pdf.is_file():
        return True
    expected = source_sha256(md)
    stamp = read_pdf_stamp(pdf)
    if stamp.get(FIELD_SOURCE_KIND) != SOURCE_KIND_TEKSTBLAD:
        return True
    if stamp.get(FIELD_SOURCE_SHA) != expected:
        return True
    return False


def build_one(md: Path, *, force: bool, dry_run: bool) -> str:
    pdf = tekstblad_pdf_for_md(md)
    if not force and not needs_rebuild(md, pdf):
        return f"skip {pdf.name} (up-to-date)"
    if dry_run:
        return f"would build {pdf.name} from {md.name}"
    cmd = [
        sys.executable,
        "-m",
        "vsa.cli",
        "pdf",
        str(md),
        "-o",
        str(pdf),
        "--content-root",
        str(REPO_ROOT / "content-source"),
    ]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    if proc.returncode != 0:
        raise SystemExit(
            f"vsa pdf faalde voor {md.as_posix()} (exit {proc.returncode})"
        )
    if not pdf.is_file():
        raise SystemExit(f"PDF ontbreekt na vsa pdf: {pdf.as_posix()}")
    stamp_pdf(
        pdf,
        source_hash=source_sha256(md),
        source_kind=SOURCE_KIND_TEKSTBLAD,
        generated_at=utc_now_iso(),
        generator=GENERATOR_TEKSTBLAD,
    )
    return f"ok {pdf.name}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tekstblad-PDF's bij bibliotheek-.tekstblad.md vernieuwen."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help="zoekroot (default: oefenhoek/bibliotheek)",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_absolute():
        root = (REPO_ROOT / root).resolve()
    sources = collect_tekstblad(root)
    if not sources:
        print(f"Geen .tekstblad.md onder {root}", flush=True)
        return 0
    for md in sources:
        try:
            msg = build_one(md, force=args.force, dry_run=args.dry_run)
        except SystemExit as exc:
            print(f"FAIL: {exc}", flush=True)
            return 1
        print(msg, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
