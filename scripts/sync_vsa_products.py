"""Maak Coria-.mxl bij bibliotheek-.vsa (eenstemmig, representatie vsa).

Doelbestand: `{stam}.vsa.mxl` naast de `.vsa` (oefenhoek-product-contract).
Slaat `oefenhoek/input/` en mappen met `artefacten_handmatig: true` over.

Coria-export gebruikt een kortstondige syllabified kopie (Pyphen) zodat de
canonieke `.vsa` zonder lettergreepstreepjes op de site-SVG blijft.

Lokaal (pipeline): stale producten vernieuwen. CI: niet aanroepen vóór check
(productie faalt bij missing/stale committed producten).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from bibliotheek import under_alias_variant
from export_mscz_coria_mxl import load_score_xml, process_existing_mxl, write_mxl
from partituur_product_meta import (
    FIELD_PARTITUUR_SHA,
    FIELD_PARTITUUR_SHA_LEGACY,
    FIELD_SOURCE_KIND,
    FIELD_SOURCE_SHA,
    GENERATOR_VSA,
    SOURCE_KIND_VSA,
    read_mxl_stamp,
    source_sha256,
    stamp_mxl_source,
    utc_now_iso,
)
from score_filenames import is_bibliotheek_vsa_source, require_no_spaces
from vsa.syllabify import syllabify_vsa_source

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


def product_path_for_vsa(vsa: Path) -> Path:
    """`naam.vsa` -> `naam.vsa.mxl`."""
    return vsa.with_suffix(".vsa.mxl")


def collect_vsa(root: Path) -> list[Path]:
    out: list[Path] = []
    if not root.is_dir():
        return out
    for path in sorted(root.rglob("*.vsa")):
        if not is_bibliotheek_vsa_source(path):
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


@dataclass
class PlaybackVsaSource:
    """Pad voor ``vsa musicxml``; optioneel temp-bestand om daarna te verwijderen."""

    path: Path
    _temp: Path | None = None

    def cleanup(self) -> None:
        if self._temp is not None and self._temp.is_file():
            self._temp.unlink(missing_ok=True)


def playback_vsa_for_export(canonical: Path) -> PlaybackVsaSource:
    """Syllabify ongescoopte tekst voor Coria; canonieke bron blijft ongewijzigd."""
    text = canonical.read_text(encoding="utf-8")
    result = syllabify_vsa_source(text)
    if not result.changed:
        return PlaybackVsaSource(path=canonical)
    handle, tmp_name = tempfile.mkstemp(suffix=".vsa", prefix="vsa-coria-")
    tmp_path = Path(tmp_name)
    try:
        with open(handle, "w", encoding="utf-8", closefd=True) as fh:
            fh.write(result.text)
    except OSError:
        tmp_path.unlink(missing_ok=True)
        raise
    return PlaybackVsaSource(path=tmp_path, _temp=tmp_path)


def _stamp_ok(mxl: Path, source_hash: str) -> bool:
    if not mxl.is_file():
        return False
    stamp = read_mxl_stamp(mxl)
    if stamp.get(FIELD_SOURCE_KIND, "") not in {"", SOURCE_KIND_VSA}:
        # Ander productiespoor op dit pad: niet overschrijven via deze sync.
        if stamp.get(FIELD_SOURCE_KIND):
            return stamp.get(FIELD_SOURCE_SHA, "") == source_hash
    return stamp.get(FIELD_SOURCE_SHA, "") == source_hash


def is_stale(vsa: Path, mxl: Path) -> bool:
    return not _stamp_ok(mxl, source_sha256(vsa))


def _run_vsa_musicxml(vsa: Path, mxl: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "vsa.cli",
        "musicxml",
        "--musicxml-profile",
        "playback",
        str(vsa),
        str(mxl),
    ]
    subprocess.check_call(cmd, cwd=str(REPO_ROOT))


def sync_one(vsa: Path, mxl: Path, *, dry_run: bool) -> None:
    rel = vsa.relative_to(REPO_ROOT)
    source_hash = source_sha256(vsa)
    generated_at = utc_now_iso()
    print(f"  MXL  {rel} -> {mxl.name}", flush=True)
    if dry_run:
        return
    require_no_spaces(mxl)
    playback = playback_vsa_for_export(vsa)
    try:
        _run_vsa_musicxml(playback.path, mxl)
    finally:
        playback.cleanup()
    process_existing_mxl(mxl)
    root = load_score_xml(mxl)
    stamp_mxl_source(
        root,
        source_hash=source_hash,
        source_kind=SOURCE_KIND_VSA,
        generated_at=generated_at,
        generator=GENERATOR_VSA,
    )
    write_mxl(mxl, root)
    # Legacy korte naam naast alleen-vsa: weg om dubbele Coria-knoppen te vermijden.
    legacy = vsa.with_suffix(".mxl")
    if legacy.is_file() and legacy.resolve() != mxl.resolve():
        stamp = read_mxl_stamp(legacy)
        if stamp.get(FIELD_SOURCE_KIND, SOURCE_KIND_VSA) in {"", SOURCE_KIND_VSA}:
            # Geen partituur-stamp: mag legacy VSA-mxl zijn.
            if not stamp.get(FIELD_PARTITUUR_SHA) and not stamp.get(
                FIELD_PARTITUUR_SHA_LEGACY
            ):
                print(f"  remove legacy {legacy.name}", flush=True)
                legacy.unlink()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Exporteer stale Coria-.mxl vanuit bibliotheek-.vsa."
    )
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="Zoekroot (default: oefenhoek/bibliotheek)",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--force",
        action="store_true",
        help="Ook exporteren als producten al bij de bron passen",
    )
    args = p.parse_args()
    root = args.root if args.root.is_absolute() else REPO_ROOT / args.root
    vsas = collect_vsa(root)
    todo: list[tuple[Path, Path]] = []
    for vsa in vsas:
        mxl = product_path_for_vsa(vsa)
        if args.force or is_stale(vsa, mxl):
            todo.append((vsa, mxl))
    if not todo:
        print(f"VSA-producten up-to-date ({len(vsas)} .vsa)", flush=True)
        return 0
    print(f"VSA-producten bijwerken: {len(todo)} van {len(vsas)}", flush=True)
    failed = 0
    for vsa, mxl in todo:
        print(f"== {vsa.relative_to(REPO_ROOT)}", flush=True)
        try:
            sync_one(vsa, mxl, dry_run=args.dry_run)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED {exc}", flush=True)
            failed += 1
    if failed:
        print(f"{failed} mislukt van {len(todo)}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
