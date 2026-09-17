"""Eenmalig: liturgiemap-hemelum score-bundles -> bibliotheek (drie lagen).

Niet in check. Opnieuw draaien is veilig als doel al bestaat (overschrijft
index.md, kopieert bestanden).

Id's zijn koormap-aligned (geen vokn-placeholders). Zie
`content-source/praktijk/oefenhoek/bibliotheek/ID-REGISTER.md` en de lijsten
SCORE_MOVES / PRINT_MOVES / STUB_SLOTS hieronder.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bibliotheek import BIBLIOTHEEK_ROOT, REPO_ROOT, folder, parse_id, stem

MAP = REPO_ROOT / "content-source" / "praktijk" / "oefenhoek" / "liturgiemap-hemelum"
SCORE_EXT = {".mscz", ".mxl", ".pdf", ".vsa"}

# (bron-relatief t.o.v. liturgiemap-hemelum, bibliotheek-id)
SCORE_MOVES: list[tuple[str, str]] = [
    ("15-cherubijnenhymne/15c-kastorski", "15-cherubijnenhymne/15c-kastorski/hemelum"),
    ("15c-cherubijnenhymne-kastorski", "15-cherubijnenhymne/15c-kastorski/hemelum"),  # legacy
    ("8-trisagion/8a-trisagion", "8-trisagion/8a-nederlands/hemelum"),
    ("8-trisagion/8a-trisagion-slav", "8-trisagion/8a-slav/hemelum"),
    ("19a-eucharistische-kanon", "19-eucharistische-canon/19a-feofan/hemelum"),
    (
        "20-moeder-godslied/20d-in-waarheid-moeder-godslied",
        "20-moeder-godslied/20d-in-waarheid/hemelum",
    ),
    (
        "20-moeder-godslied/20-moeder-godslied-ontslapen-mgods",
        "20-moeder-godslied/ontslapen-moeder-gods/hemelum",
    ),
    (
        "25-communievers/25-communievers-onthoofding-johannes-de-doper",
        "25-communievers/onthoofding-johannes-de-doper/hemelum",
    ),
    (
        "troparen-en-kondaken/tropaar-nikolaas-van-myra",
        "tropaar/nikolaas-van-myra-toon-4/hemelum",
    ),
    (
        "2-eerste-antifoon/weekdagen/hemelum",
        "2-eerste-antifoon/weekdagen-hemelum/hemelum",
    ),
    (
        "2-eerste-antifoon/weekdagen/liturgikon",
        "2-eerste-antifoon/weekdagen-liturgikon/hemelum",
    ),
    ("2-eerste-antifoon/zondag", "2-eerste-antifoon/zondag/hemelum"),
    (
        "4-tweede-antifoon/weekdagen/hemelum",
        "4-tweede-antifoon/weekdagen-hemelum/hemelum",
    ),
    ("4-tweede-antifoon/zondag", "4-tweede-antifoon/zondag/hemelum"),
    (
        "6-derde-antifoon/weekdagen/hemelum",
        "6-derde-antifoon/weekdagen-hemelum/hemelum",
    ),
    (
        "6-derde-antifoon/zondag",
        "6-derde-antifoon/zondag/hemelum",
    ),
    ("5-eniggeboren-zoon", "5-eniggeboren-zoon/default/hemelum"),
    ("7-kleine-intocht/zondag", "7-kleine-intocht/zondag/hemelum"),
    ("7-kleine-intocht/weekdagen", "7-kleine-intocht/weekdagen/hemelum"),
    ("7-kleine-intocht/moeder-gods", "7-kleine-intocht/moeder-gods/hemelum"),
    (
        "28-wij-hebben-het-ware-licht",
        "28-wij-hebben-het-ware-licht/default/hemelum",
    ),
    (
        "29-de-naam-des-heren-zij-gezegend",
        "29-de-naam-des-heren-zij-gezegend/default/hemelum",
    ),
]

# Print-vel: *.print.mscz + PDF (geen hub-pijplijn / geen Coria).
PRINT_MOVES: list[tuple[str, str]] = [
    ("7-kleine-intocht/zo-wk-mg", "7-kleine-intocht/zo-wk-mg/hemelum"),
]

# Map-slots zonder partituur: bibliotheek-stub + shortcode-verwijzing.
STUB_SLOTS: list[tuple[str, str]] = [
    ("1-vredeslitanie", "1-vredeslitanie/default/hemelum"),
    ("3-eerste-kleine-litanie", "3-eerste-kleine-litanie/default/hemelum"),
    ("9a-prokimen/weekdagen", "9-prokimen/9a-maandag/groningen"),  # compositieblad; leaf-voorbeeld
    ("9b-alleluia", "9-alleluia/9a-toon-1/groningen"),
    ("10-evangelielezing", "10-evangelielezing/default/hemelum"),
    ("11-dringende-litanie", "11-dringende-litanie/default/hemelum"),
    ("12-ontslapenen-litanie", "12-ontslapenen-litanie/default/hemelum"),
    ("13-catechumenen-litanie", "13-catechumenen-litanie/default/hemelum"),
    ("14-gelovigen-litanie", "14-gelovigen-litanie/default/hemelum"),
    ("16-vragende-litanie", "16-vragende-litanie/default/hemelum"),
    ("17-vredeswens", "17-vredeswens/default/hemelum"),
    ("18-geloofsbelijdenis", "18-geloofsbelijdenis/default/hemelum"),
    ("21-en-allen", "21-en-allen/default/hemelum"),
    ("22-vragende-litanie", "22-vragende-litanie/default/hemelum"),
    ("23-onze-vader", "23-onze-vader/default/hemelum"),
    ("24-een-is-heilig", "24-een-is-heilig/default/hemelum"),
    ("26-gezegend-hij-die-komt", "26-gezegend-hij-die-komt/default/hemelum"),
    ("27-communiezang", "27-communiezang/default/hemelum"),
    ("7d-dialoog-met-diaken", "7d-dialoog-met-diaken/default/hemelum"),
]

# Koormap-slots met catalogus-include (geen lokale hub): niet via migrate_stub.
# Zie ID-REGISTER.md (CATALOGUS_KOORMAP).

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
    zdir = BIBLIOTHEEK_ROOT / zangstuk
    zindex = zdir / "_index.md"
    if not zindex.is_file():
        _write(
            zindex,
            (
                f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
                "nav_sort: weight\npublicatiestatus: concept\n"
                "automatische_inhoud: true\n---\n"
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
                    "nav_sort: weight\npublicatiestatus: concept\n"
                    "automatische_inhoud: true\n---\n"
                ),
            )


def _bibliotheek_index(ident: str, title: str, status: str) -> str:
    return (
        f"---\ntitle: \"{title}\"\nlinkTitle: \"{title}\"\n"
        f"publicatiestatus: {status}\nautomatische_inhoud: false\n---\n\n"
        f"# {title}\n\n"
        f"{{{{< bieb id=\"{ident}\" >}}}}\n"
    )


def _map_slot(title: str, link: str, weight: str, status: str, ident: str) -> str:
    w = f"weight: {weight}\n" if weight else ""
    lt = f"linkTitle: \"{link}\"\n" if link else ""
    return (
        f"---\ntitle: \"{title}\"\n{lt}{w}"
        f"publicatiestatus: {status}\nautomatische_inhoud: false\n---\n\n"
        f"# {title}\n\n"
        f"{{{{< bieb id=\"{ident}\" >}}}}\n"
    )


def _move_scores(src: Path, dest: Path, ident: str) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    stam = stem(ident)
    for path in list(src.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SCORE_EXT:
            continue
        if path.name.lower().endswith(".print.mscz"):
            continue
        target = dest / f"{stam}{path.suffix.lower()}"
        if path.resolve() != target.resolve():
            shutil.copy2(path, target)
            path.unlink()


def _move_print_bundle(src: Path, dest: Path, ident: str) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    stam = stem(ident)
    for path in list(src.iterdir()):
        if not path.is_file():
            continue
        low = path.name.lower()
        if low.endswith(".print.mscz"):
            target = dest / f"{stam}.print.mscz"
        elif path.suffix.lower() == ".pdf":
            target = dest / f"{stam}.pdf"
        else:
            continue
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
    _write(dest / "index.md", _bibliotheek_index(ident, title, status))
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
    _write(dest / "index.md", _bibliotheek_index(ident, title, status))
    _write(index, _map_slot(title, link, weight, status, ident))
    print(f"stub {rel} -> {ident}")


def migrate_print(rel: str, ident: str) -> None:
    src = MAP / rel
    index = src / "index.md"
    text = index.read_text(encoding="utf-8") if index.is_file() else ""
    title = _fm_field(text, "title") or ident.split("/")[-1]
    link = _fm_field(text, "linkTitle") or title
    weight = _fm_field(text, "weight")
    status = _fm_field(text, "publicatiestatus") or "concept"
    zangstuk, variant, _uv = parse_id(ident)
    dest = folder(ident)
    _ensure_section(zangstuk, variant, zangstuk)
    if src.is_dir():
        _move_print_bundle(src, dest, ident)
    body = (
        f"# {title}\n\n"
        "Print-vel (geen Coria-hub). PDF via de knoppen hieronder.\n\n"
        f"{{{{< bieb id=\"{ident}\" >}}}}\n"
    )
    _write(
        dest / "index.md",
        (
            f"---\ntitle: \"{title}\"\nlinkTitle: \"{link}\"\n"
            f"publicatiestatus: {status}\nautomatische_inhoud: false\n---\n\n"
            f"{body}"
        ),
    )
    koormap_body = (
        f"# {title}\n\n"
        "Print-vel voor de koormap (zondag / weekdagen / Moeder Gods). "
        "Canonieke hubs: [Zondag](../zondag/), [Weekdagen](../weekdagen/), "
        "[Moeder Gods](../moeder-gods/).\n\n"
        f"{{{{< bieb id=\"{ident}\" >}}}}\n"
    )
    w = f"weight: {weight}\n" if weight else ""
    _write(
        index,
        (
            f"---\ntitle: \"{title}\"\nlinkTitle: \"{link}\"\n{w}"
            f"publicatiestatus: {status}\nautomatische_inhoud: false\n---\n\n"
            f"{koormap_body}"
        ),
    )
    print(f"print {rel} -> {ident}")


def main() -> int:
    BIBLIOTHEEK_ROOT.mkdir(parents=True, exist_ok=True)
    root_index = BIBLIOTHEEK_ROOT / "_index.md"
    if not root_index.is_file():
        _write(
            root_index,
            (
                "---\n"
                'title: "Bibliotheek"\n'
                'linkTitle: "Bibliotheek"\n'
                "weight: 5\n"
                "nav_sort: weight\n"
                "publicatiestatus: concept\n"
                "automatische_inhoud: true\n"
                "---\n\n"
                "Oefenbare uitvoeringsvormen (partituur). Koormappen elders "
                "verwijzen hierheen via een id, zonder het bestand te kopieren.\n"
            ),
        )
    for rel, ident in SCORE_MOVES:
        migrate_score(rel, ident)
    for rel, ident in PRINT_MOVES:
        migrate_print(rel, ident)
    for rel, ident in STUB_SLOTS:
        migrate_stub(rel, ident)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
