"""Capella/CapToMusic-.mxl map -> standaard-layout .mscz.

Laag 1-3: cleanup_capella_mxl.py. Laag 4: apply_mscz_layout.py (MuseScore 4).
Niet in check. Geen PDF of Coria-.mxl.

  python scripts/batch_capella_mxl_to_mscz.py
  python scripts/batch_capella_mxl_to_mscz.py --dry-run
  python scripts/batch_capella_mxl_to_mscz.py --limit 3

Bestaande .mscz die niet ouder zijn dan de bron worden overgeslagen
(hervatten). MuseScore sluiten voor je start.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apply_mscz_layout import find_musescore, musescore_convert, process_mscz, extract_rights_from_mxl
from cleanup_capella_mxl import cleanup, load_mxl, write_mxl
from score_filenames import published_stem, require_no_spaces

DEFAULT_SRC = Path(r"C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mxl")
DEFAULT_DST = Path(r"C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mscz")
_TIMEOUT_FILE = 180


def collect_mxl(src_root: Path) -> list[Path]:
    return sorted(p for p in src_root.rglob("*.mxl") if p.is_file())


def unique_dest(dest: Path, taken: set[Path]) -> Path:
    if dest not in taken:
        return dest
    stem, suffix = dest.stem, dest.suffix
    n = 2
    while True:
        cand = dest.with_name(f"{stem}-{n}{suffix}")
        if cand not in taken:
            return cand
        n += 1


def plan_jobs(src_root: Path, dst_root: Path) -> list[tuple[Path, Path]]:
    taken: set[Path] = set()
    jobs: list[tuple[Path, Path]] = []
    for src in collect_mxl(src_root):
        rel_parent = src.relative_to(src_root).parent
        dest = dst_root / rel_parent / (published_stem(src.name) + ".mscz")
        dest = unique_dest(dest, taken)
        require_no_spaces(dest)
        taken.add(dest)
        jobs.append((src, dest))
    return jobs


def _is_fresh(dest: Path, src: Path) -> bool:
    return dest.is_file() and dest.stat().st_mtime >= src.stat().st_mtime


def cleanup_to(src: Path, dest_mxl: Path) -> None:
    dest_mxl.parent.mkdir(parents=True, exist_ok=True)
    root, xml_name, extras = load_mxl(src)
    cleanup(root)
    write_mxl(dest_mxl, root, xml_name, extras)


def musescore_convert_batch(pairs: list[tuple[Path, Path]], timeout: int) -> bool:
    if not pairs:
        return True
    for _src, dest in pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            dest.unlink()
    job = [{"in": str(s.resolve()), "out": [str(d.resolve())]} for s, d in pairs]
    musescore = find_musescore()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump(job, fh)
        job_path = Path(fh.name)
    try:
        proc = subprocess.run(
            [str(musescore), "-j", str(job_path)],
            timeout=timeout,
        )
        if proc.returncode != 0:
            return False
        return all(dest.is_file() for _src, dest in pairs)
    except (subprocess.TimeoutExpired, OSError):
        return False
    finally:
        job_path.unlink(missing_ok=True)


def finish_mscz(clean_mxl: Path, tmp_mscz: Path, dest: Path) -> None:
    if not tmp_mscz.is_file():
        musescore_convert(clean_mxl, tmp_mscz)
    process_mscz(tmp_mscz, rights_hint=extract_rights_from_mxl(clean_mxl))
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tmp_mscz, dest)


def convert_chunk(
    chunk: list[tuple[Path, Path, Path]],
    work: Path,
) -> list[tuple[Path, Path, str]]:
    """chunk items: (src, dest, rel_stem). Returns failures."""
    failed: list[tuple[Path, Path, str]] = []
    prepared: list[tuple[Path, Path, Path, Path]] = []
    for src, dest, rel_stem in chunk:
        clean = work / rel_stem.with_suffix(".mxl")
        tmp_mscz = work / rel_stem.with_suffix(".mscz")
        try:
            cleanup_to(src, clean)
            prepared.append((src, dest, clean, tmp_mscz))
        except Exception as exc:
            failed.append((src, dest, f"opkuisen: {exc}"))

    pairs = [(clean, tmp) for _src, _dest, clean, tmp in prepared]
    timeout = _TIMEOUT_FILE * max(len(pairs), 1) + 120
    if pairs:
        musescore_convert_batch(pairs, timeout)

    for src, dest, clean, tmp_mscz in prepared:
        try:
            finish_mscz(clean, tmp_mscz, dest)
        except Exception as exc:
            try:
                musescore_convert(clean, tmp_mscz)
                finish_mscz(clean, tmp_mscz, dest)
            except Exception as exc2:
                failed.append((src, dest, f"layout/mscz: {exc2}"))
    return failed


def main() -> int:
    p = argparse.ArgumentParser(
        description="Capella-.mxl map opkuisen en naar standaard-.mscz zetten."
    )
    p.add_argument(
        "src",
        nargs="?",
        type=Path,
        default=DEFAULT_SRC,
        help=f"Bronmap met .mxl (default: {DEFAULT_SRC})",
    )
    p.add_argument(
        "dst",
        nargs="?",
        type=Path,
        default=DEFAULT_DST,
        help=f"Doelmap voor .mscz (default: {DEFAULT_DST})",
    )
    p.add_argument("--force", action="store_true", help="Bestaande .mscz overschrijven")
    p.add_argument("--dry-run", action="store_true", help="Alleen de planning tonen")
    p.add_argument("--limit", type=int, default=0, help="Stop na N conversies (niet skips)")
    p.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="MuseScore-jobgrootte (default 10)",
    )
    args = p.parse_args()
    src_root = args.src.resolve()
    dst_root = args.dst.resolve()
    if not src_root.is_dir():
        print(f"bronmap ontbreekt: {src_root}", flush=True)
        return 1
    jobs = plan_jobs(src_root, dst_root)
    if not jobs:
        print("Geen .mxl-bestanden gevonden.", flush=True)
        return 1

    todo: list[tuple[Path, Path]] = []
    skipped = 0
    for src, dest in jobs:
        if not args.force and _is_fresh(dest, src):
            skipped += 1
            continue
        todo.append((src, dest))
    if args.limit > 0:
        todo = todo[: args.limit]

    print(f"bron:  {src_root}", flush=True)
    print(f"doel:  {dst_root}", flush=True)
    print(
        f"totaal {len(jobs)} .mxl, skip {skipped}, te doen {len(todo)}",
        flush=True,
    )
    if args.dry_run:
        for src, dest in todo:
            print(f"  {src.relative_to(src_root)} -> {dest.relative_to(dst_root)}", flush=True)
        return 0
    if not todo:
        print("Niets te doen.", flush=True)
        return 0

    find_musescore()
    dst_root.mkdir(parents=True, exist_ok=True)
    log_path = dst_root / "_batch-log.txt"
    failures: list[tuple[Path, Path, str]] = []
    ok = 0
    work_jobs = [
        (src, dest, src.relative_to(src_root).with_suffix(""))
        for src, dest in todo
    ]
    batch_size = max(args.batch_size, 1)

    with tempfile.TemporaryDirectory(prefix="capella-mxl-") as tmp:
        work = Path(tmp)
        for i in range(0, len(work_jobs), batch_size):
            chunk = work_jobs[i : i + batch_size]
            n0 = i + 1
            n1 = i + len(chunk)
            print(f"-- {n0}-{n1}/{len(work_jobs)}", flush=True)
            for src, _dest, _rel in chunk:
                print(f"== {src.relative_to(src_root)}", flush=True)
            chunk_fail = convert_chunk(chunk, work)
            failures.extend(chunk_fail)
            failed_dests = {dest for _src, dest, _err in chunk_fail}
            ok += sum(1 for _src, dest, _rel in chunk if dest not in failed_dests)

    lines = [
        f"ok {ok}",
        f"skip {skipped}",
        f"fail {len(failures)}",
        f"bron {src_root}",
        f"doel {dst_root}",
        "",
    ]
    for src, dest, err in failures:
        lines.append(f"FAIL {src}")
        lines.append(f"  -> {dest}")
        lines.append(f"  {err}")
        print(f"FAIL {src}: {err}", flush=True)
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"log: {log_path}", flush=True)
    print(f"klaar: ok={ok} skip={skipped} fail={len(failures)}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
