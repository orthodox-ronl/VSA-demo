"""Eenmalig: liturgiemap-hemelum score-bundles -> repertoire (drie lagen).

Niet in check. Opnieuw draaien is veilig als doel al bestaat (overschrijft
index.md, kopieert bestanden).
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repertoire import REPERTOIRE_ROOT, REPO_ROOT, folder, parse_id, stem

MAP = REPO_ROOT / "content-source" / "praktijk" / "oefenhoek" / "liturgiemap-hemelum"
SCORE_EXT = {".mscz", ".mxl", ".pdf", ".vsa"}

# (bron-relatief t.o.v. liturgiemap-hemelum, repertoire-id)
SCORE_MOVES: list[tuple[str, str]] = [
    ("15c-cherubijnenhymne-kastorski", "cherubijnenhymne/15c-kastorski/hemelum"),
    ("8a-trisagion", "trisagion/8a/hemelum"),
    ("8a-trisagion-slav", "trisagion/8a-slav/hemelum"),
    ("19a-eucharistische-kanon", "eucharistische-kanon/19a-feofan/hemelum"),
    ("20-moeder-godslied/20d-in-waarheid-moeder-godslied", "moeder-godslied/20d-in-waarheid/hemelum"),
    (
        "20-moeder-godslied/moeder-godslied-ontslapen-mgods",
        "moeder-godslied/ontslapen-moeder-gods/hemelum",
    ),
    (
        "25-communievers/communievers-onthoofding-johannes-de-doper",
        "communievers/onthoofding-johannes-de-doper/hemelum",
    ),
    (
        "troparen-en-kondaken/troparion-nikolaas-van-myra",
        "troparion-nikolaas-van-myra/liturgikon/hemelum",
    ),
]

# Map-slots zonder partituur: repertoire-stub + include.
STUB_SLOTS: list[tuple[str, str]] = [
    ("1-vredeslitanie", "1-vredeslitanie/vokn/hemelum"),
    ("2-eerste-antifoon", "2-eerste-antifoon/vokn/hemelum"),
    ("3-eerste-kleine-litanie", "3-eerste-kleine-litanie/vokn/hemelum"),
    ("4-tweede-antifoon", "4-tweede-antifoon/vokn/hemelum"),
    ("5-eniggeboren-zoon", "5-eniggeboren-zoon/vokn/hemelum"),
    ("6-derde-antifoon-zaligsprekingen", "6-derde-antifoon-zaligsprekingen/vokn/hemelum"),
    ("7-kleine-intocht", "7-kleine-intocht/vokn/hemelum"),
    ("9-prokimens", "9-prokimens/vokn/hemelum"),
    ("9b-alleluja", "9b-alleluja/vokn/hemelum"),
    ("10-evangelielezing", "10-evangelielezing/vokn/hemelum"),
    ("11-dringende-litanie", "11-dringende-litanie/vokn/hemelum"),
    ("12-ontslapenen-litanie", "12-ontslapenen-litanie/vokn/hemelum"),
    ("13-catehumenen-litanie", "13-catehumenen-litanie/vokn/hemelum"),
    ("14-gelovigen-litanie", "14-gelovigen-litanie/vokn/hemelum"),
    ("16-vragende-litanie", "16-vragende-litanie/vokn/hemelum"),
    ("17-vredeswens", "17-vredeswens/vokn/hemelum"),
    ("18-geloofsbelijdenis", "18-geloofsbelijdenis/vokn/hemelum"),
    ("21-en-allen", "21-en-allen/vokn/hemelum"),
    ("22-vragende-litanie", "22-vragende-litanie/vokn/hemelum"),
    ("23-onze-vader", "23-onze-vader/vokn/hemelum"),
    ("24-een-is-heilig", "24-een-is-heilig/vokn/hemelum"),
    ("26-gezegend-hij-die-komt", "26-gezegend-hij-die-komt/vokn/hemelum"),
    ("27-communiezang", "27-communiezang/vokn/hemelum"),
    ("28-wij-hebben-het-ware-licht", "28-wij-hebben-het-ware-licht/vokn/hemelum"),
    ("29-de-naam-des-heren-zij-gezegend", "29-de-naam-des-heren-zij-gezegend/vokn/hemelum"),
    ("dialoog-met-diaken", "dialoog-met-diaken/vokn/hemelum"),
]

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def _fm_field(text: str, name: str) -> str:
    m = FM_RE.match(text)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        if line.lower().startswith(name + ":"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _ensure_section(zangstuk: str, variant: str | None, title: str) -> None:
    zdir = REPERTOIRE_ROOT / zangstuk
    zindex = zdir / "_index.md"
    if not zindex.is_file():
        _write(
            zindex,
            (
                f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
                "nav_sort: weight\npublicatiestatus: concept\n---\n"
            ),
        )
    if variant:
        vdir = zdir / variant
        vindex = vdir / "_index.md"
        if not vindex.is_file():
            _write(
                vindex,
                (
                    f"---\ntitle: \"{variant}\"\nlinkTitle: \"{variant}\"\n"
                    "nav_sort: weight\npublicatiestatus: concept\n---\n"
                ),
            )


def _repertoire_index(ident: str, title: str, status: str) -> str:
    return (
        f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
        f"publicatiestatus: {status}\n---\n\n"
        f"# {title}\n\n"
        f"{{{{< repertoire-score id=\"{ident}\" >}}}}\n"
    )


def _map_slot(title: str, link: str, weight: str, status: str, ident: str) -> str:
    w = f"weight: {weight}\n" if weight else ""
    lt = f"linkTitle: \"{link}\"\n" if link else ""
    return (
        f"---\ntitle: \"{title}\"\n{lt}{w}"
        f"publicatiestatus: {status}\n---\n\n"
        f"# {title}\n\n"
        f"{{{{< repertoire-score id=\"{ident}\" >}}}}\n"
    )


def _move_scores(src: Path, dest: Path, ident: str) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    stam = stem(ident)
    for path in list(src.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SCORE_EXT:
            continue
        target = dest / f"{stam}{path.suffix.lower()}"
        if path.resolve() != target.resolve():
            shutil.copy2(path, target)
            path.unlink()


def migrate_score(rel: str, ident: str) -> None:
    src = MAP / rel
    index = src / "index.md"
    text = index.read_text(encoding="utf-8") if index.is_file() else ""
    title = _fm_field(text, "title") or ident.split("/")[-1]
    link = _fm_field(text, "linkTitle") or title
    weight = _fm_field(text, "weight")
    status = _fm_field(text, "publicatiestatus") or "voorzien"
    zangstuk, variant, _uv = parse_id(ident)
    dest = folder(ident)
    _ensure_section(zangstuk, variant, zangstuk)
    if src.is_dir():
        _move_scores(src, dest, ident)
    _write(dest / "index.md", _repertoire_index(ident, title, status))
    _write(index, _map_slot(title, link, weight, status, ident))
    print(f"score {rel} -> {ident}")


def migrate_stub(rel: str, ident: str) -> None:
    src = MAP / rel
    index = src / "index.md"
    text = index.read_text(encoding="utf-8") if index.is_file() else ""
    title = _fm_field(text, "title") or rel
    link = _fm_field(text, "linkTitle") or title
    weight = _fm_field(text, "weight")
    status = _fm_field(text, "publicatiestatus") or "voorzien"
    zangstuk, variant, _uv = parse_id(ident)
    dest = folder(ident)
    _ensure_section(zangstuk, variant, title)
    dest.mkdir(parents=True, exist_ok=True)
    _write(dest / "index.md", _repertoire_index(ident, title, status))
    _write(index, _map_slot(title, link, weight, status, ident))
    print(f"stub {rel} -> {ident}")


def main() -> int:
    REPERTOIRE_ROOT.mkdir(parents=True, exist_ok=True)
    root_index = REPERTOIRE_ROOT / "_index.md"
    if not root_index.is_file():
        _write(
            root_index,
            (
                "---\n"
                'title: "Repertoire"\n'
                'linkTitle: "Repertoire"\n'
                "weight: 5\n"
                "nav_sort: weight\n"
                "publicatiestatus: concept\n"
                "---\n\n"
                "Oefenbare uitvoeringsvormen (partituur). Koormappen elders "
                "verwijzen hierheen via een id, zonder het bestand te kopieren.\n"
            ),
        )
    for rel, ident in SCORE_MOVES:
        migrate_score(rel, ident)
    for rel, ident in STUB_SLOTS:
        migrate_stub(rel, ident)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
