"""Neem een partituur op in de Oefenhoek-bibliotheek.

Maakt (indien nodig) zangstuk/variant-_index.md en leaf-index.md met bieb,
kopieert of verplaatst bestanden naar de publicatiestam, en weigert formats
die niet in de bibliotheek horen.

Niet in check. Geen volledige muzikale opkuis; wel poorten (id, formaat,
vsa validate). Zie scripts/h.cmd bieb-accepteer en de handleiding
publiceren/1-opnemen-in-bibliotheek.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bibliotheek import (  # noqa: E402
    BIBLIOTHEEK_ROOT,
    REPO_ROOT,
    folder,
    parse_id,
    stem,
    under_alias_variant,
)
from score_filenames import is_print_mscz  # noqa: E402

ALLOWED_STATUS = frozenset({"voorzien", "concept", "reviewable", "productie"})
SCORE_SUFFIXES = frozenset({".mscz", ".vsa"})
COMPANION_SUFFIXES = frozenset({".pdf", ".mxl"})


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _write(path: Path, text: str, *, dry_run: bool) -> None:
    if dry_run:
        print(f"  would write {_rel(path)}", flush=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _fm_value(text: str, key: str) -> str | None:
    in_fm = False
    prefix = f"{key.lower()}:"
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm and line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def default_title(ident: str) -> str:
    zangstuk, _variant, _uv = parse_id(ident)
    return zangstuk.replace("-", " ")


def classify_source(path: Path) -> str:
    """Geef soort: hub_mscz | print_mscz | vsa | pdf | mxl | refuse:..."""
    if not path.is_file():
        return f"refuse:bestaat niet ({path})"
    name = path.name.lower()
    if is_print_mscz(path):
        return "print_mscz"
    suffix = path.suffix.lower()
    if suffix == ".mscz":
        return "hub_mscz"
    if suffix == ".vsa":
        return "vsa"
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".mxl":
        # Ruwe Capella-MXL hoort via opkuisen; alleen siblings (producten) ok.
        return "mxl"
    if suffix in {".musicxml", ".xml", ".cap", ".capx"}:
        return (
            "refuse:dit formaat hoort niet rechtstreeks in de bibliotheek "
            "(eerst opkuisen / normaliseren; zie handleiding partituur)"
        )
    return f"refuse:onbekende extensie {path.suffix!r}"


def target_name(kind: str, ident: str, *, with_vsa: bool) -> str:
    stam = stem(ident)
    if kind == "hub_mscz":
        return f"{stam}.mscz"
    if kind == "print_mscz":
        return f"{stam}.print.mscz"
    if kind == "vsa":
        return f"{stam}.vsa"
    if kind == "pdf":
        return f"{stam}.pdf"
    if kind == "mxl":
        if with_vsa:
            return f"{stam}.vsa.mxl"
        return f"{stam}.mxl"
    raise ValueError(kind)


def section_index_text(title: str) -> str:
    return (
        f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
        "nav_sort: weight\npublicatiestatus: concept\n"
        "automatische_inhoud: true\n---\n"
    )


def leaf_index_text(
    ident: str,
    title: str,
    status: str,
    *,
    artefacten_handmatig: bool,
) -> str:
    handmatig = "artefacten_handmatig: true\n" if artefacten_handmatig else ""
    return (
        f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
        f"publicatiestatus: {status}\n"
        f"{handmatig}"
        "automatische_inhoud: false\n---\n\n"
        f"# {title}\n\n"
        f"{{{{< bieb id=\"{ident}\" >}}}}\n"
    )


def ensure_sections(ident: str, *, dry_run: bool) -> None:
    zangstuk, variant, _uv = parse_id(ident)
    zdir = BIBLIOTHEEK_ROOT / zangstuk
    zindex = zdir / "_index.md"
    if not zindex.is_file():
        _write(zindex, section_index_text(zangstuk.replace("-", " ")), dry_run=dry_run)
        print(f"  section {_rel(zindex)}", flush=True)
    vdir = zdir / variant
    vindex = vdir / "_index.md"
    if not vindex.is_file():
        _write(vindex, section_index_text(variant.replace("-", " ")), dry_run=dry_run)
        print(f"  section {_rel(vindex)}", flush=True)


def validate_vsa(path: Path) -> list[str]:
    """Lege lijst = ok; anders foutregels."""
    try:
        proc = subprocess.run(
            ["vsa", "validate", str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return [
            "vsa staat niet op PATH; installeer vsa-tool of draai scripts\\check.cmd "
            "eerst (bootstrap)"
        ]
    if proc.returncode == 0:
        return []
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    detail = out or err or f"exit {proc.returncode}"
    return [f"vsa validate faalde voor {path.name}: {detail}"]


def place_file(
    src: Path,
    dest: Path,
    *,
    move: bool,
    force: bool,
    dry_run: bool,
) -> None:
    if dest.exists() and not force:
        raise SystemExit(
            f"doel bestaat al: {_rel(dest)}\n"
            "Oplossing: gebruik --force om te overschrijven, of kies een ander id."
        )
    if dry_run:
        action = "move" if move else "copy"
        print(f"  would {action} {_rel(src)} -> {_rel(dest)}", flush=True)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if move:
        if dest.exists():
            dest.unlink()
        shutil.move(str(src), str(dest))
    else:
        shutil.copy2(src, dest)
    print(f"  {'moved' if move else 'copied'} {_rel(dest)}", flush=True)


def accept(
    ident: str,
    sources: list[Path],
    *,
    title: str | None,
    status: str | None,
    stub: bool,
    move: bool,
    force: bool,
    dry_run: bool,
    skip_vsa_validate: bool,
    artefacten_handmatig: bool,
) -> int:
    try:
        parse_id(ident)
    except ValueError as exc:
        print(f"FAIL: ongeldig bibliotheek-id ({exc})", flush=True)
        print(
            "Oplossing: gebruik zangstuk/variant/uitvoeringsvorm "
            "(alleen a-z, 0-9, -, _). Zie Id-register.",
            flush=True,
        )
        return 1

    dest_dir = folder(ident)
    if under_alias_variant(dest_dir):
        print(
            f"FAIL: {ident} valt onder een alias-variant "
            "(daar horen geen partituren)",
            flush=True,
        )
        print(
            "Oplossing: plaats op de canonieke variant, of maak alleen "
            "alias_van op de variant-_index.",
            flush=True,
        )
        return 1

    if stub and sources:
        print("FAIL: --stub samen met bestanden mag niet", flush=True)
        return 1
    if not stub and not sources:
        print(
            "FAIL: geef minstens een bestand, of --stub voor een lege leaf",
            flush=True,
        )
        return 1

    classified: list[tuple[Path, str]] = []
    errors: list[str] = []
    for raw in sources:
        src = raw.expanduser().resolve()
        kind = classify_source(src)
        if kind.startswith("refuse:"):
            errors.append(f"{src.name}: {kind.removeprefix('refuse:')}")
            continue
        classified.append((src, kind))

    kinds = {k for _, k in classified}
    if "mxl" in kinds and "hub_mscz" not in kinds and "vsa" not in kinds:
        errors.append(
            "alleen een .mxl: dat is meestal een Capella- of productbestand. "
            "Accepteer eerst een .mscz of .vsa, of leg de .mxl ernaast als "
            "sibling. Ruwe Capella: zie handleiding opkuisen."
        )

    has_score = bool(kinds & {"hub_mscz", "print_mscz", "vsa"}) or stub
    if not has_score and classified:
        errors.append(
            "geen hub-.mscz, .print.mscz of .vsa: de bibliotheek-leaf heeft "
            "dan niets oefenbaars. Gebruik --stub voor een lege placeholder."
        )

    if not skip_vsa_validate:
        for src, kind in classified:
            if kind == "vsa":
                errors.extend(validate_vsa(src))

    if errors:
        for line in errors:
            print(f"FAIL: {line}", flush=True)
        return 1

    resolved_title = title or default_title(ident)
    if status is None:
        resolved_status = "voorzien" if stub else "reviewable"
    else:
        resolved_status = status
    if resolved_status not in ALLOWED_STATUS:
        print(
            f"FAIL: onbekende publicatiestatus {resolved_status!r} "
            f"(verwacht: {', '.join(sorted(ALLOWED_STATUS))})",
            flush=True,
        )
        return 1
    if resolved_status == "productie" and not force:
        print(
            "FAIL: publicatiestatus productie niet automatisch zetten",
            flush=True,
        )
        print(
            "Oplossing: kies reviewable/concept/voorzien, of --force als "
            "een beheerder productie bewust wil.",
            flush=True,
        )
        return 1

    with_vsa = "vsa" in kinds
    handmatig = artefacten_handmatig or ("print_mscz" in kinds)

    print(f"Bibliotheek-id: {ident}", flush=True)
    print(f"Doelmap: {_rel(dest_dir)}", flush=True)
    if dry_run:
        print("(dry-run: niets geschreven)", flush=True)

    ensure_sections(ident, dry_run=dry_run)

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    for src, kind in classified:
        name = target_name(kind, ident, with_vsa=with_vsa)
        if " " in name:
            print(f"FAIL: doelnaam mag geen spaties hebben: {name}", flush=True)
            return 1
        place_file(
            src,
            dest_dir / name,
            move=move,
            force=force,
            dry_run=dry_run,
        )

    index_path = dest_dir / "index.md"
    if index_path.is_file() and not force and not dry_run:
        existing = index_path.read_text(encoding="utf-8")
        bieb_ok = f'bieb id="{ident}"' in existing or f"bieb id='{ident}'" in existing
        if not bieb_ok:
            print(
                f"FAIL: bestaande {_rel(index_path)} heeft geen matching bieb id",
                flush=True,
            )
            print(
                "Oplossing: corrigeer de shortcode, of --force om index.md "
                "opnieuw te schrijven.",
                flush=True,
            )
            return 1
        print(f"  kept {_rel(index_path)}", flush=True)
    else:
        _write(
            index_path,
            leaf_index_text(
                ident,
                resolved_title,
                resolved_status,
                artefacten_handmatig=handmatig,
            ),
            dry_run=dry_run,
        )
        print(f"  index {_rel(index_path)} ({resolved_status})", flush=True)

    print("OK: opgenomen in de bibliotheek", flush=True)
    if dry_run:
        print("(dry-run: herhaal zonder --dry-run om echt te schrijven)", flush=True)
    if not stub and "hub_mscz" in kinds:
        print(
            "Volgende (hub): normaliseren/layouten indien nog niet gedaan, "
            "daarna scripts\\mscz-products.cmd",
            flush=True,
        )
    if "vsa" in kinds:
        print(
            "Volgende (VSA): scripts\\vsa-products.cmd of check "
            "(Coria-.vsa.mxl)",
            flush=True,
        )
    print(
        "Daarna: koormap-slot met bieb (handleiding publiceren) en "
        "scripts\\check.cmd --strict",
        flush=True,
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Neem .mscz / .vsa / .print.mscz (en optioneel PDF/MXL) op in "
            "oefenhoek/bibliotheek onder een bibliotheek-id."
        )
    )
    p.add_argument(
        "ident",
        help="bibliotheek-id: zangstuk/variant/uitvoeringsvorm",
    )
    p.add_argument(
        "bestanden",
        nargs="*",
        type=Path,
        help="een of meer bronbestanden",
    )
    p.add_argument(
        "--title",
        help="paginatitel (default: zangstuk-id met spaties i.p.v. streepjes)",
    )
    p.add_argument(
        "--status",
        choices=sorted(ALLOWED_STATUS),
        help="publicatiestatus (default: reviewable, of voorzien bij --stub)",
    )
    p.add_argument(
        "--stub",
        action="store_true",
        help="alleen leaf + index.md, zonder partituurbestand",
    )
    p.add_argument(
        "--move",
        action="store_true",
        help="verplaats bronbestanden (default: kopieer)",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="overschrijf bestaande doelen / herschrijf index.md",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="toon acties zonder te schrijven",
    )
    p.add_argument(
        "--skip-vsa-validate",
        action="store_true",
        help="sla vsa validate over (niet aanbevolen)",
    )
    p.add_argument(
        "--artefacten-handmatig",
        action="store_true",
        help="zet artefacten_handmatig: true (ook auto bij .print.mscz)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return accept(
        args.ident.strip(),
        list(args.bestanden),
        title=args.title,
        status=args.status,
        stub=args.stub,
        move=args.move,
        force=args.force,
        dry_run=args.dry_run,
        skip_vsa_validate=args.skip_vsa_validate,
        artefacten_handmatig=args.artefacten_handmatig,
    )


if __name__ == "__main__":
    raise SystemExit(main())
