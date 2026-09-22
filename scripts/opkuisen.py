"""Generieke opkuiser: herkomstanalyse + inhoudelijke fixes (+ optioneel layout).

Zie handleiding scripts/opkuisen.md en scripts\\h.cmd opkuisen.
Niet in check/build/serve.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from apply_mscz_layout import (  # noqa: E402
    extract_rights_from_mxl,
    musescore_convert,
    process_mscz,
    process_mscz_content_only,
)
from cleanup_capella_mxl import cleanup, cleanup_generic  # noqa: E402
from opkuis_detect import (  # noqa: E402
    HOEK_CAPELLA,
    HOEK_MUSICXML_GENERIC,
    HOEK_MUSESCORE,
    HOEK_MVSA,
    HOEK_VSA,
    KNOWN_HOEKEN,
    MUSICXML_SUFFIXES,
    REFUSED_SUFFIXES,
    SUPPORTED_SUFFIXES,
    DetectResult,
    detect_path,
)
from opkuis_io import (  # noqa: E402
    load_musicxml,
    read_mscx_file,
    write_mscx_file,
    write_musicxml,
)
from score_filenames import (  # noqa: E402
    is_print_mscz,
    published_path,
    published_stem,
    require_no_spaces,
)

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_REFUSED = 2


def expand_opkuis_paths(paths: list[Path]) -> list[Path]:
    """Recursief bestanden met ondersteunde extensies.

    Bij een mapscan: sla ``*.print.mscz`` over. Als de scan-root zelf geen
    ``input``-segment is, sla paden onder ``input\\`` over (ruwe dumps niet
    per ongeluk meenemen vanuit content-source). Een expliciet bestandspad
    blijft altijd in de lijst.
    """
    out: list[Path] = []
    for path in paths:
        if path.is_dir():
            found: list[Path] = []
            for p in sorted(path.rglob("*")):
                if not p.is_file():
                    continue
                suf = p.suffix.lower()
                if suf not in SUPPORTED_SUFFIXES and suf not in REFUSED_SUFFIXES:
                    continue
                if is_print_mscz(p):
                    continue
                found.append(p)
            if path.name != "input" and "input" not in path.parts:
                found = [p for p in found if "input" not in p.parts]
            out.extend(found)
        else:
            out.append(path)
    # unique preserve order
    seen: set[Path] = set()
    uniq: list[Path] = []
    for p in out:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(p)
    return uniq


def _is_protected_input_path(path: Path) -> bool:
    """Ruwe oefenhoek-input (niet _werk / _inbox): niet stil overschrijven."""
    parts_l = [p.lower() for p in path.parts]
    try:
        i = parts_l.index("input")
    except ValueError:
        return False
    if i + 1 >= len(parts_l):
        return False
    herkomst = parts_l[i + 1]
    if herkomst.startswith("_"):
        return False
    return True


def resolve_dest(
    src: Path,
    *,
    output: Path | None,
    in_place: bool,
    ext: str | None,
    n_inputs: int,
) -> Path:
    """Bepaal schrijfdoel. Raises SystemExit bij weigering."""
    if ext:
        if not ext.startswith("."):
            ext = f".{ext}"
        ext = ext.lower()

    def with_ext(p: Path) -> Path:
        if ext:
            return p.with_suffix(ext)
        return p

    if output is not None:
        as_file = (
            n_inputs == 1
            and output.suffix.lower() in SUPPORTED_SUFFIXES
            and not output.is_dir()
        )
        if as_file:
            dest = with_ext(output)
            return published_path(dest) if " " in dest.name else dest
        # doelmap
        rel_name = published_stem(src.name) + (ext or src.suffix.lower())
        return published_path(output / rel_name)

    if ext:
        dest = src.with_name(published_stem(src.name) + ext)
        return dest

    if in_place or " " not in src.name:
        if " " in src.name:
            raise SystemExit(
                f"in-place geweigerd (spaties in de naam): {src.name}\n"
                f"Oplossing: gebruik -o, bijv. -o {published_path(src).name}"
            )
        return src

    raise SystemExit(
        f"in-place geweigerd (spaties in de naam): {src.name}\n"
        f"Oplossing: gebruik -o naar _werk\\STAM\\, bijv. {published_path(src).name}"
    )


def _format_detect(det: DetectResult) -> list[str]:
    lines = [
        f"  hoek={det.hoek} confidence={det.confidence:.2f}",
        f"  passes={','.join(det.suggested_passes) or '(geen)'}",
    ]
    for s in det.signals:
        lines.append(f"  signaal: {s}")
    for w in det.warnings:
        lines.append(f"  waarschuwing: {w}")
    if det.error:
        lines.append(f"  fout: {det.error}")
    return lines


def _run_vsa_validate(path: Path) -> tuple[bool, str]:
    which = shutil.which("vsa")
    if not which:
        return False, "vsa niet op PATH (installeer vsa-tool)"
    try:
        proc = subprocess.run(
            [which, "validate", str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, str(e)
    out = (proc.stdout or "") + (proc.stderr or "")
    ok = proc.returncode == 0
    return ok, out.strip() or f"exit {proc.returncode}"


def apply_content(path: Path, det: DetectResult, dest: Path) -> list[str]:
    """Voer inhoudsfixes uit en schrijf naar dest. Return notities."""
    notes: list[str] = []
    hoek = det.hoek

    if hoek == HOEK_VSA:
        raise SystemExit(
            f"geen automatische VSA-inhoudsopkuis voor {path.name}. "
            r"Gebruik: scripts\opkuisen.cmd ... --analyze  (of vsa validate). "
            r"Zie handleiding praktijk/handleiding/vsa/1-vsa-schrijven."
        )
    if hoek == HOEK_MVSA:
        raise SystemExit(
            f"mvsa is voorzien, nog geen opkuis: {path.name}. "
            r"Zie handleiding werktrajecten/mvsa."
        )

    if hoek in (HOEK_CAPELLA, HOEK_MUSICXML_GENERIC):
        if path.suffix.lower() not in MUSICXML_SUFFIXES:
            raise SystemExit(
                f"hoek {hoek} verwacht MusicXML-extensie, kreeg {path.suffix}: {path}"
            )
        root, xml_name, extras = load_musicxml(path)
        if hoek == HOEK_CAPELLA:
            cleanup(root)
            notes.append("capella-musicxml (lagen 1-3)")
        else:
            cleanup_generic(root)
            notes.append("generic-musicxml (twee-balks sleutels)")
        if dest != path:
            dest.parent.mkdir(parents=True, exist_ok=True)
        write_musicxml(dest, root, xml_name, extras)
        notes.append(f"geschreven: {dest}")
        return notes

    if hoek == HOEK_MUSESCORE:
        suf = path.suffix.lower()
        if suf == ".mscz":
            if dest != path:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(path.read_bytes())
                work = dest
            else:
                work = path
            notes.extend(process_mscz_content_only(work))
            notes.append(f"geschreven: {work}")
            return notes
        if suf == ".mscx":
            from apply_mscz_layout import content_cleanup_mscx

            text = read_mscx_file(path)
            new_text, cnotes = content_cleanup_mscx(text)
            notes.extend(cnotes)
            write_mscx_file(dest if dest != path else path, new_text)
            notes.append(f"geschreven: {dest if dest != path else path}")
            return notes
        raise SystemExit(f"hoek musescore verwacht .mscz/.mscx: {path}")

    raise SystemExit(
        f"geen inhoudspass voor hoek={hoek} ({path}). "
        "Gebruik --assume of --analyze."
    )


def apply_layout_after_content(work: Path, *, bibliotheek_id: str = "") -> list[str]:
    """Normaliseer basispartituur (apply_mscz_layout)."""
    notes: list[str] = []
    suf = work.suffix.lower()
    if suf in MUSICXML_SUFFIXES:
        rights = ""
        if suf == ".mxl":
            rights = extract_rights_from_mxl(work)
        dest = work.with_suffix(".mscz")
        dest = published_path(dest)
        require_no_spaces(dest)
        notes.append(f"mxl/xml -> mscz via MuseScore: {dest}")
        musescore_convert(work, dest)
        notes.extend(
            process_mscz(dest, rights_hint=rights, bibliotheek_id=bibliotheek_id)
        )
        notes.append(f"layout geschreven: {dest}")
        return notes
    if suf == ".mscz":
        notes.extend(process_mscz(work, bibliotheek_id=bibliotheek_id))
        notes.append(f"layout geschreven: {work}")
        return notes
    if suf == ".mscx":
        raise SystemExit(
            "layout op losse .mscx wordt niet ondersteund; "
            "sla eerst op als .mscz in MuseScore 4."
        )
    raise SystemExit(f"layout niet van toepassing op {work.suffix}: {work}")


def process_one(
    path: Path,
    *,
    analyze: bool,
    do_layout: bool,
    assume: str | None,
    force: bool,
    output: Path | None,
    in_place: bool,
    ext: str | None,
    n_inputs: int,
    bibliotheek_id: str = "",
) -> int:
    """Verwerk een pad. Return exitcode 0/1/2."""
    print(f"== {path}")
    det = detect_path(path, assume=assume)
    for line in _format_detect(det):
        print(line)

    if det.error:
        print(f"  WEIGERING: {det.error}")
        return EXIT_ERROR

    if analyze:
        if det.hoek == HOEK_VSA:
            ok, msg = _run_vsa_validate(path)
            print(f"  vsa validate: {'OK' if ok else 'FAIL'}")
            for line in (msg.splitlines() or ["(geen output)"])[:40]:
                print(f"    {line}")
            return EXIT_OK if ok else EXIT_ERROR
        if det.hoek == HOEK_MVSA:
            print("  mvsa: voorzien - geen validate/opkuis in v1")
            return EXIT_OK
        if do_layout:
            print("  --layout + --analyze/--dry-run: zou na content ook layout doen (geen schrijven)")
        print("  analyze/dry-run: geen schrijfactie")
        return EXIT_OK

    if det.low_confidence and not force and not assume:
        print(
            "  WEIGERING: lage confidence - geef --assume <hoek> of --force "
            f"(hoek={det.hoek}, confidence={det.confidence:.2f})"
        )
        return EXIT_REFUSED

    if det.hoek in (HOEK_VSA, HOEK_MVSA):
        try:
            apply_content(path, det, path)
        except SystemExit as e:
            print(f"  WEIGERING: {e}")
            return EXIT_REFUSED
        return EXIT_REFUSED

    try:
        dest = resolve_dest(
            path,
            output=output,
            in_place=in_place,
            ext=ext,
            n_inputs=n_inputs,
        )
    except SystemExit as e:
        print(f"  WEIGERING: {e}")
        return EXIT_REFUSED

    require_no_spaces(dest)

    if _is_protected_input_path(dest) and not in_place:
        print(
            f"  WEIGERING: schrijven naar ruwe input geweigerd: {dest}\n"
            "  Oplossing: -o naar input\\_werk\\STAM\\ of --in-place (overschrijft de bron)."
        )
        return EXIT_REFUSED

    try:
        notes = apply_content(path, det, dest)
        for n in notes:
            print(f"  {n}")
        work = dest
        if do_layout:
            # Layout expects mscz; if we wrote musicxml, convert from dest
            layout_notes = apply_layout_after_content(
                work, bibliotheek_id=bibliotheek_id
            )
            for n in layout_notes:
                print(f"  {n}")
    except SystemExit as e:
        print(f"  FOUT: {e}")
        return EXIT_ERROR
    except Exception as e:
        print(f"  FOUT: {e}")
        return EXIT_ERROR
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Opkuisen: herkomstanalyse en inhoudelijke opschoning van "
            "MusicXML/MuseScore (optioneel layout). Zie h.cmd opkuisen."
        )
    )
    p.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Bestand of map (recursief; ondersteunde score-extensies)",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Doelbestand of doelmap",
    )
    p.add_argument(
        "--in-place",
        action="store_true",
        help="Overschrijf de bron (nodig voor ruwe oefenhoek/input/...)",
    )
    p.add_argument(
        "--ext",
        help="Doel-extensie (bijv. .mxl of .mscz)",
    )
    p.add_argument(
        "--analyze",
        action="store_true",
        dest="analyze",
        help="Alleen herkomst + rapport; geen schrijven (synoniem: --dry-run)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        dest="analyze",
        help="Synoniem van --analyze: geen schrijven",
    )
    p.add_argument(
        "--layout",
        action="store_true",
        help="Na content ook basispartituur-layout (apply_mscz_layout)",
    )
    p.add_argument(
        "--assume",
        choices=sorted(KNOWN_HOEKEN),
        help="Overschrijf herkomstdetectie",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Ga door bij lage confidence (zonder --assume)",
    )
    p.add_argument(
        "--id",
        dest="bibliotheek_id",
        default="",
        help="Bibliotheek-id voor layout-diepte (optioneel)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    files = expand_opkuis_paths(args.paths)
    if not files:
        print("Geen ondersteunde score-bestanden gevonden.", flush=True)
        return EXIT_ERROR

    if args.output is not None and len(files) > 1:
        out = args.output
        # allow non-existing path as directory
        if out.suffix.lower() in SUPPORTED_SUFFIXES and (out.is_file() or not out.exists()):
            # ambiguous: if exists as file or looks like file with suffix
            if out.exists() and out.is_file():
                print("Bij meerdere invoerbestanden moet -o een map zijn.", flush=True)
                return EXIT_ERROR
            if not out.exists() and out.suffix.lower() in SUPPORTED_SUFFIXES:
                print(
                    "Bij meerdere invoerbestanden moet -o een map zijn "
                    f"(geen enkel bestand {out.name}).",
                    flush=True,
                )
                return EXIT_ERROR

    worst = EXIT_OK
    n_ok = n_err = n_ref = 0
    for path in files:
        suf = path.suffix.lower()
        if suf in REFUSED_SUFFIXES and not args.analyze:
            print(f"== {path}")
            print(
                f"  WEIGERING: {suf} - eerst CapToMusic naar .mxl, daarna opkuisen."
            )
            n_ref += 1
            worst = max(worst, EXIT_REFUSED)
            continue
        code = process_one(
            path,
            analyze=bool(args.analyze),
            do_layout=bool(args.layout),
            assume=args.assume,
            force=bool(args.force),
            output=args.output,
            in_place=bool(args.in_place),
            ext=args.ext,
            n_inputs=len(files),
            bibliotheek_id=args.bibliotheek_id or "",
        )
        if code == EXIT_OK:
            n_ok += 1
        elif code == EXIT_REFUSED:
            n_ref += 1
            worst = max(worst, EXIT_REFUSED)
        else:
            n_err += 1
            worst = max(worst, EXIT_ERROR)

    print(
        f"-- samenvatting: ok={n_ok} geweigerd={n_ref} fout={n_err} totaal={len(files)}"
    )
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
