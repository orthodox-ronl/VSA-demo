"""Vul de tabel in oefenhoek/input/werkvoorraad.md vanuit de dumps op schijf.

Draait in check/build/serve (generate). Handmatige notities en doel-id in een
bestaande rij blijven staan; stap/volgende worden opnieuw afgeleid.
"""

from __future__ import annotations

import shutil
from pathlib import Path

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
            "deelrubriek": parts[2].strip(),
            "doelvorm": parts[3].strip().strip("`"),
            "stap": parts[4].strip(),
            "volgende": parts[5].strip(),
            "notitie": parts[6].strip(),
        }
    return rows


def _bladermappen() -> list[tuple[str, str, Path]]:
    found: list[tuple[str, str, Path]] = []
    for index in OEFENHOEK.rglob("index.md"):
        rel = index.relative_to(OEFENHOEK)
        if "input" in rel.parts:
            continue
        folder = index.parent.name
        deel = rel.parts[0] if rel.parts else ""
        found.append((folder, deel, index.parent))
    return found


def _has_score(folder: Path) -> bool:
    return any(p.is_file() and p.suffix.lower() in SCORE_EXT for p in folder.iterdir())


def _match_doel(
    dump_name: str,
    maps: list[tuple[str, str, Path]],
    old_id: str,
) -> tuple[str, str, Path | None]:
    if old_id:
        for folder, deel, path in maps:
            if folder == old_id:
                return folder, deel, path
        return old_id, "", None
    stem = published_stem(dump_name)
    exact = [m for m in maps if m[0] == stem]
    if len(exact) == 1:
        folder, deel, path = exact[0]
        return folder, deel, path
    return "", "", None


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
        return "bladermap", "—"
    if dump.suffix.lower() == ".mscz":
        return "ontvangen", "layout"
    return "ontvangen", "opkuisen"


def _dumps() -> list[Path]:
    out: list[Path] = []
    for herkomst in HERKOMST:
        folder = INPUT / herkomst
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if not path.is_file() or path.name.startswith("."):
                continue
            if path.name == ".gitkeep":
                continue
            if path.suffix.lower() not in DUMP_EXT:
                continue
            out.append(path)
    return sorted(out, key=lambda p: p.relative_to(INPUT).as_posix().lower())


def _table(old: dict[str, dict[str, str]]) -> str:
    maps = _bladermappen()
    lines = [
        "| Dump | Doel-id | Deelrubriek | Doelvorm | Stap | Volgende | Notitie |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for dump in _dumps():
        rel = dump.relative_to(INPUT).as_posix()
        prev = old.get(rel, {})
        doel_id, deel, path = _match_doel(dump.name, maps, prev.get("doel_id", ""))
        if not deel:
            deel = prev.get("deelrubriek", "")
        vorm = _doelvorm(dump, prev.get("doelvorm", ""))
        stap, volgende = _stap(path, dump)
        notitie = prev.get("notitie", "")
        doel_cell = f"`{doel_id}`" if doel_id else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{rel}`",
                    doel_cell,
                    _cell(deel),
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
