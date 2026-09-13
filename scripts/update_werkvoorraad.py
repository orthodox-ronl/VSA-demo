"""Vul de tabel in oefenhoek/input/werkvoorraad.md vanuit de dumps op schijf.

Draait in check/build/serve (generate). Handmatige notities, doel-id en
koormap in een bestaande rij blijven staan; stap/volgende worden opnieuw
afgeleid.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from repertoire import folder, leaf_folders, parse_id
from score_filenames import published_stem

REPO = Path(__file__).resolve().parents[1]
OEFENHOEK = REPO / "content-source" / "praktijk" / "oefenhoek"
INPUT = OEFENHOEK / "input"
DOC = INPUT / "werkvoorraad.md"
HERKOMST = ("capella", "vow", "musescore", "musicxml", "pdf")
DUMP_EXT = {".mxl", ".xml", ".musicxml", ".mscz", ".cap", ".capx", ".pdf", ".vsa"}
SCORE_EXT = {".mscz", ".mxl", ".pdf", ".vsa"}
BEGIN = "<!-- werkvoorraad-tabel:begin -->"
END = "<!-- werkvoorraad-tabel:einde -->"

# Oude mapnaam (Hemelum-slot) -> repertoire-id
_SLOT_TO_ID = {
    "15c-cherubijnenhymne-kastorski": "cherubijnenhymne/15c-kastorski/hemelum",
    "8a-trisagion": "trisagion/8a/hemelum",
    "8a-trisagion-slav": "trisagion/8a-slav/hemelum",
    "19a-eucharistische-kanon": "eucharistische-kanon/19a-feofan/hemelum",
    "20d-in-waarheid-moeder-godslied": "moeder-godslied/20d-in-waarheid/hemelum",
    "28-wij-hebben-het-ware-licht": "28-wij-hebben-het-ware-licht/vokn/hemelum",
    "29-de-naam-des-heren-zij-gezegend": "29-de-naam-des-heren-zij-gezegend/vokn/groningen",
    "2-eerste-antifoon": "2-eerste-antifoon/vokn/hemelum",
    "4-tweede-antifoon": "4-tweede-antifoon/vokn/hemelum",
    "6-derde-antifoon-zaligsprekingen": "6-derde-antifoon-zaligsprekingen/vokn/hemelum",
    "7-kleine-intocht": "7-kleine-intocht/vokn/hemelum",
}


def _cell(value: str) -> str:
    return (value or "").replace("|", "\\|")


def _parse_rows(markdown: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in markdown.splitlines():
        if not line.startswith("| `"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 7:
            continue
        dump = parts[0].strip().strip("`")
        rows[dump] = {
            "doel_id": parts[1].strip().strip("`"),
            "koormap": parts[2].strip().strip("`"),
            "doelvorm": parts[3].strip().strip("`"),
            "stap": parts[4].strip(),
            "volgende": parts[5].strip(),
            "notitie": parts[6].strip(),
        }
    return rows


def _has_score(path: Path) -> bool:
    if not path.is_dir():
        return False
    return any(p.is_file() and p.suffix.lower() in SCORE_EXT for p in path.iterdir())


def _normalize_id(old_id: str) -> str:
    if not old_id:
        return ""
    if old_id in _SLOT_TO_ID:
        return _SLOT_TO_ID[old_id]
    try:
        parse_id(old_id)
        return old_id
    except ValueError:
        return old_id


def _match_doel(dump_name: str, old_id: str) -> tuple[str, Path | None]:
    ident = _normalize_id(old_id)
    leaves = {i: p for i, p in leaf_folders()}
    if ident in leaves:
        return ident, leaves[ident]
    if ident:
        dest = folder(ident) if "/" in ident and ident.count("/") == 2 else None
        if dest is not None:
            try:
                parse_id(ident)
            except ValueError:
                dest = None
        if dest is not None:
            return ident, dest if dest.is_dir() else None
        return ident, None
    stem = published_stem(dump_name)
    hits = [i for i in leaves if i.endswith("/" + stem) or stem in i]
    if len(hits) == 1:
        return hits[0], leaves[hits[0]]
    return "", None


def _koormap(prev: dict[str, str], ident: str) -> str:
    old = prev.get("koormap") or prev.get("deelrubriek", "")
    if old == "liturgiemap-hemelum":
        slot = prev.get("doel_id", "").strip("`")
        if slot and "/" not in slot:
            return slot
        if ident:
            return ident.split("/")[0]
        return ""
    if old in ("overig",):
        return ""
    return old


def _doelvorm(dump: Path, old: str) -> str:
    if old:
        return f"`{old}`" if not old.startswith("`") else old
    if dump.suffix.lower() == ".vsa":
        return "`.vsa`"
    return "`.mscz`"


def _stap(path: Path | None, dump: Path) -> tuple[str, str]:
    if path is None:
        return "ontvangen", "doel-id"
    if _has_score(path):
        return "gepubliceerd", "—"
    if dump.suffix.lower() == ".mscz":
        return "ontvangen", "layout"
    return "ontvangen", "opkuisen"


def _dumps() -> list[Path]:
    out: list[Path] = []
    for herkomst in HERKOMST:
        folder_h = INPUT / herkomst
        if not folder_h.is_dir():
            continue
        for path in folder_h.iterdir():
            if not path.is_file() or path.name.startswith("."):
                continue
            if path.name == ".gitkeep":
                continue
            if path.suffix.lower() not in DUMP_EXT:
                continue
            out.append(path)
    return sorted(out, key=lambda p: p.relative_to(INPUT).as_posix().lower())


def _table(old: dict[str, dict[str, str]]) -> str:
    lines = [
        "| Dump | Doel-id | Koormap | Doelvorm | Stap | Volgende | Notitie |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for dump in _dumps():
        rel = dump.relative_to(INPUT).as_posix()
        prev = old.get(rel, {})
        raw_id = prev.get("doel_id", "")
        if rel.endswith("15e Cherubijnenhymne Bortnjanski no.5.mxl"):
            raw_id = raw_id or "cherubijnenhymne/15e-bortnjanski-no5/vokn"
        doel_id, path = _match_doel(dump.name, raw_id)
        koormap = _koormap(prev, doel_id)
        if rel.endswith("15e Cherubijnenhymne Bortnjanski no.5.mxl"):
            koormap = ""
        vorm = _doelvorm(dump, prev.get("doelvorm", ""))
        stap, volgende = _stap(path, dump)
        notitie = prev.get("notitie", "")
        doel_cell = f"`{doel_id}`" if doel_id else ""
        koor_cell = f"`{koormap}`" if koormap else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{rel}`",
                    doel_cell,
                    koor_cell,
                    vorm,
                    _cell(stap),
                    _cell(volgende),
                    _cell(notitie),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _replace_table(doc: str, table: str) -> str:
    if BEGIN not in doc or END not in doc:
        raise SystemExit(f"FAIL: {DOC} mist {BEGIN} / {END}")
    before, rest = doc.split(BEGIN, 1)
    _, after = rest.split(END, 1)
    return f"{before}{BEGIN}\n\n{table}\n{END}{after}"


def main() -> int:
    if not DOC.is_file():
        print(f"FAIL: {DOC} ontbreekt.", flush=True)
        return 1
    text = DOC.read_text(encoding="utf-8")
    old = _parse_rows(text)
    updated = _replace_table(text, _table(old))
    if updated != text:
        DOC.write_text(updated, encoding="utf-8", newline="\n")
        print("Werkvoorraad-tabel bijgewerkt.", flush=True)
    else:
        print("Werkvoorraad-tabel ongewijzigd.", flush=True)
    generated = REPO / "generated" / "content" / "praktijk" / "oefenhoek" / "input"
    if generated.is_dir():
        shutil.rmtree(generated)
        print(
            "generated/content/.../oefenhoek/input verwijderd (geen Hugo-pagina's).",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
