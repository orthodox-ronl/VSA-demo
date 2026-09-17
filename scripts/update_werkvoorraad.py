"""Vul de tabel in oefenhoek/input/werkvoorraad.md vanuit de inputs op schijf.

Draait in check/build/serve (generate). Handmatige notities, doel-id en
koormap in een bestaande rij blijven staan; stap/volgende worden opnieuw
afgeleid.

Doel-id is bij voorkeur een bibliotheek-id (zangstuk/variant/uitvoeringsvorm).
Oude bladermap-namen worden via _SLOT_TO_ID genormaliseerd.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from bibliotheek import folder, leaf_folders, parse_id
from score_filenames import published_stem

REPO = Path(__file__).resolve().parents[1]
OEFENHOEK = REPO / "content-source" / "praktijk" / "oefenhoek"
INPUT = OEFENHOEK / "input"
DOC = INPUT / "werkvoorraad.md"
HERKOMST = ("capella", "vow", "musescore", "musicxml", "pdf")
INPUT_EXT = {".mxl", ".xml", ".musicxml", ".mscz", ".cap", ".capx", ".pdf", ".vsa"}
SCORE_EXT = {".mscz", ".mxl", ".pdf", ".vsa"}
BEGIN = "<!-- werkvoorraad-tabel:begin -->"
END = "<!-- werkvoorraad-tabel:einde -->"

# Oude mapnaam (Hemelum-slot of leaf) -> bibliotheek-id (koormap-aligned)
_SLOT_TO_ID = {
    "15c-cherubijnenhymne-kastorski": "15-cherubijnenhymne/15c-kastorski/hemelum",
    "15-cherubijnenhymne/15c-kastorski": "15-cherubijnenhymne/15c-kastorski/hemelum",
    "15e-cherubijnenhymne-bortnjanski": "15-cherubijnenhymne/15e-bortnjanski/hemelum",
    "15-cherubijnenhymne/15e-bortnjanski": "15-cherubijnenhymne/15e-bortnjanski/hemelum",
    "15b-fatejev": "15-cherubijnenhymne/15b-fatejev/hemelum",
    "15d-kastorski": "15-cherubijnenhymne/15d-kastorski/hemelum",
    "15c-cherubijnenhymne-kastorski-ksl-trlat": (
        "15-cherubijnenhymne/15c-kastorski/hemelum-ksl-trlat"
    ),
    "8a-trisagion": "8-trisagion/8a-nederlands/hemelum",
    "8a-trisagion-slav": "8-trisagion/8a-slav/hemelum",
    "19a-eucharistische-kanon": "19-eucharistische-canon/19a-feofan/hemelum",
    "19-eucharistische-canon-rostov": "19-eucharistische-canon/rostov/hemelum",
    "20d-in-waarheid-moeder-godslied": "20-moeder-godslied/20d-in-waarheid/hemelum",
    "20-moeder-godslied-ontslapen-mgods": "20-moeder-godslied/ontslapen-moeder-gods/hemelum",
    "25-communievers-onthoofding-johannes-de-doper": (
        "25-communievers/onthoofding-johannes-de-doper/hemelum"
    ),
    "tropaar-nikolaas-van-myra": "tropaar/nikolaas-van-myra-toon-4/hemelum",
    "2-eerste-antifoon": "2-eerste-antifoon/zondag/hemelum",
    "4-tweede-antifoon": "4-tweede-antifoon/zondag/hemelum",
    "5-eniggeboren-zoon": "5-eniggeboren-zoon/default/hemelum",
    "6-derde-antifoon-zaligsprekingen": (
        "6-derde-antifoon/zondag/hemelum"
    ),
    "6-derde-antifoon": "6-derde-antifoon/zondag/hemelum",
    "7-kleine-intocht": "7-kleine-intocht/zondag/hemelum",
    "7-kleine-intocht/weekdagen/hemelum": "7-kleine-intocht/weekdagen/hemelum",
    "7-kleine-intocht/moeder-gods/hemelum": "7-kleine-intocht/moeder-gods/hemelum",
    "7-kleine-intocht/zo-wk-mg/hemelum": "7-kleine-intocht/zo-wk-mg/hemelum",
    "zo-wk-mg": "7-kleine-intocht/zo-wk-mg/hemelum",
    "28-wij-hebben-het-ware-licht": "28-wij-hebben-het-ware-licht/default/hemelum",
    "29-de-naam-des-heren-zij-gezegend": (
        "29-de-naam-des-heren-zij-gezegend/default/hemelum"
    ),
}
_ID_TO_SLOT = {v: k for k, v in _SLOT_TO_ID.items()}


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
        key = parts[0].strip().strip("`")
        rows[key] = {
            "doel_id": parts[1].strip().strip("`"),
            "koormap": parts[2].strip().strip("`"),
            "doelvorm": parts[3].strip().strip("`"),
            "stap": parts[4].strip(),
            "volgende": parts[5].strip(),
            "notitie": parts[6].strip(),
        }
        # Oude kolom "Deelrubriek" (liturgiemap-hemelum / overig)
        if parts[2].strip() in ("liturgiemap-hemelum", "overig", "bibliotheek"):
            rows[key]["deelrubriek"] = parts[2].strip()
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


def _legacy_bladermappen() -> dict[str, Path]:
    """Leaf-mappen onder liturgiemap/overig (nog niet gemigreerd)."""
    found: dict[str, Path] = {}
    for index in OEFENHOEK.rglob("index.md"):
        rel = index.relative_to(OEFENHOEK)
        if "input" in rel.parts or "bibliotheek" in rel.parts:
            continue
        folder_name = index.parent.name
        found[folder_name] = index.parent
    return found


def _match_doel(dump_name: str, old_id: str) -> tuple[str, Path | None]:
    # Capella 7b deelde vroeger doel-id met 7 (zondag).
    lower = dump_name.lower()
    if "7b" in lower and "weekdagen" in lower:
        old_id = "7-kleine-intocht/weekdagen/hemelum"
    elif "moedergods" in lower.replace("-", "").replace("_", "") or (
        "moeder" in lower and "gods" in lower and "intocht" in lower
    ):
        if not old_id or old_id == "7-kleine-intocht":
            old_id = "7-kleine-intocht/moeder-gods/hemelum"
    ident = _normalize_id(old_id)
    leaves = {i: p for i, p in leaf_folders()}
    if ident in leaves:
        return ident, leaves[ident]
    legacy = _legacy_bladermappen()
    if ident:
        try:
            parse_id(ident)
            dest = folder(ident)
            if dest.is_dir():
                return ident, dest
            # Bibliotheek-id bekend, map nog niet: kijk oude bladermap.
            slot = _ID_TO_SLOT.get(ident, "")
            for key in (slot, old_id, Path(old_id).name if old_id else ""):
                if key and key in legacy:
                    return ident, legacy[key]
            return ident, None
        except ValueError:
            if ident in legacy:
                return ident, legacy[ident]
            if old_id in legacy:
                return old_id, legacy[old_id]
            return ident, None
    stem = published_stem(dump_name)
    hits = [i for i in leaves if i.endswith("/" + stem) or stem in i]
    if len(hits) == 1:
        return hits[0], leaves[hits[0]]
    if stem in legacy:
        return _normalize_id(stem) or stem, legacy[stem]
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
    if old in ("overig", "bibliotheek"):
        return ""
    return old


def _doelvorm(src: Path, old: str) -> str:
    if old:
        return f"`{old}`" if not old.startswith("`") else old
    if src.suffix.lower() == ".vsa":
        return "`.vsa`"
    return "`.mscz`"


def _stap(path: Path | None, src: Path, *, ident: str = "") -> tuple[str, str]:
    if path is None:
        if ident:
            try:
                parse_id(ident)
                return "ontvangen", "migratie"
            except ValueError:
                pass
        return "ontvangen", "doel-id"
    if _has_score(path):
        return "gepubliceerd", "—"
    if src.suffix.lower() == ".mscz":
        return "ontvangen", "layout"
    return "ontvangen", "opkuisen"


def _inputs() -> list[Path]:
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
            if path.suffix.lower() not in INPUT_EXT:
                continue
            out.append(path)
    return sorted(out, key=lambda p: p.relative_to(INPUT).as_posix().lower())


def _table(old: dict[str, dict[str, str]]) -> str:
    lines = [
        "| Input | Doel-id | Koormap | Doelvorm | Stap | Volgende | Notitie |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for src in _inputs():
        rel = src.relative_to(INPUT).as_posix()
        prev = old.get(rel, {})
        raw_id = prev.get("doel_id", "")
        doel_id, path = _match_doel(src.name, raw_id)
        koormap = _koormap(prev, doel_id)
        vorm = _doelvorm(src, prev.get("doelvorm", ""))
        stap, volgende = _stap(path, src, ident=doel_id)
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
