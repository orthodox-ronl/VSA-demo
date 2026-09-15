"""Oefenhoek-index: widgets horen in de Hugo-layout, niet in de markdown.

- Zonder flags: haalt auto-includes/score-shortcodes uit bladermap-index.md
  (frontmatter + eigen tekst blijven). Catalogus-includes (id:/lokaal:/bron:)
  blijven. Draait in check/build/serve, voor vsa validate.
- --svg: schrijft SVG van lokale .vsa (geen sibling-.mscz) naar
  static/vsa/bladermap/, na vsa build-markdown (die static/vsa leegmaakt).

  python scripts/sync_oefenhoek_index.py
  python scripts/sync_oefenhoek_index.py --dry-run
  python scripts/sync_oefenhoek_index.py --svg
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OEFENHOEK = REPO / "content-source" / "praktijk" / "oefenhoek"
SVG_ROOT = REPO / "static" / "vsa" / "bladermap"

CATALOG_INCLUDE_RE = re.compile(
    r":::\s*include\s+\w+\s+(id|lokaal|bron):", re.I
)
LOCAL_INCLUDE_RE = re.compile(
    r'^\s*:::\s*include\s+(?:svg|coria|mxl)\s+"[^"]+".*:::\s*$', re.I
)
SCORE_OPEN_RE = re.compile(r"^\s*\{\{<\s*score-actions\b", re.I)
SCORE_CLOSE_RE = re.compile(r"^\s*\{\{<\s*/score-actions\s*>\}\}\s*$", re.I)
PDF_SHEET_RE = re.compile(r"^\s*\{\{<\s*pdf-sheet\b.*>\}\}\s*$", re.I)
STUB_COMMENT_RE = re.compile(
    r"^\s*<!--\s*(?::::include|score-actions|pdf-sheet)\b.*?-->\s*$",
    re.I,
)
AUTO_FALSE_RE = re.compile(
    r"^automatische_inhoud:\s*(false|0|nee|no)\s*$", re.I | re.M
)


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    rest = text[3:]
    end = rest.find("\n---")
    if end < 0:
        return "", text
    fm = rest[:end].strip("\n")
    body = rest[end + 4 :].lstrip("\n")
    return fm, body


def _strip_widgets(body: str) -> str:
    kept: list[str] = []
    skipping_score = False
    for line in body.splitlines():
        if skipping_score:
            if SCORE_CLOSE_RE.match(line):
                skipping_score = False
            continue
        if CATALOG_INCLUDE_RE.search(line):
            kept.append(line)
            continue
        if LOCAL_INCLUDE_RE.match(line):
            continue
        if SCORE_OPEN_RE.match(line):
            skipping_score = True
            continue
        if PDF_SHEET_RE.match(line):
            continue
        if STUB_COMMENT_RE.match(line):
            continue
        kept.append(line)
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return f"{text}\n" if text else ""


def _iter_indexes() -> list[Path]:
    out: list[Path] = []
    for path in sorted(OEFENHOEK.rglob("index.md")):
        if "input" in path.relative_to(OEFENHOEK).parts:
            continue
        out.append(path)
    return out


def strip_indexes(*, dry_run: bool) -> int:
    changed = 0
    skipped = 0
    for path in _iter_indexes():
        raw = path.read_text(encoding="utf-8")
        fm, body = _split_frontmatter(raw)
        if not fm:
            skipped += 1
            continue
        if AUTO_FALSE_RE.search(fm):
            skipped += 1
            continue
        if CATALOG_INCLUDE_RE.search(body):
            skipped += 1
            continue
        new_body = _strip_widgets(body)
        new = f"---\n{fm}\n---\n"
        if new_body:
            new += f"\n{new_body}"
        if new.replace("\r\n", "\n") == raw.replace("\r\n", "\n"):
            continue
        rel = path.relative_to(REPO).as_posix()
        if dry_run:
            print(f"would strip {rel}", flush=True)
        else:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(f"stripped {rel}", flush=True)
        changed += 1
    print(
        f"oefenhoek-index: {changed} gestript, {skipped} overgeslagen",
        flush=True,
    )
    return 0


def _render_one_vsa(src: Path, dest: Path) -> None:
    from vsa.include_vsa import IncludeVsaError, prepare_vsa_body
    from vsa.markdown_newline_policy import preserve_vsa_source_newlines
    from vsa.parser import Parser
    from vsa.svg_renderer import SVGRenderer

    text = src.read_text(encoding="utf-8")
    try:
        body, _ = prepare_vsa_body(text, src)
    except IncludeVsaError as exc:
        raise RuntimeError(f"{src}: {exc.message_nl}") from exc
    document = Parser(preserve_vsa_source_newlines(body)).parse()
    svg = SVGRenderer().render_document(document)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(svg, encoding="utf-8")


def render_svgs() -> int:
    source = REPO / "content-source"
    if SVG_ROOT.exists():
        for old in SVG_ROOT.rglob("*.svg"):
            old.unlink()
    written = 0
    for folder in sorted(OEFENHOEK.rglob("*")):
        if not folder.is_dir():
            continue
        if "input" in folder.relative_to(OEFENHOEK).parts:
            continue
        if not (folder / "index.md").is_file():
            continue
        msczs = list(folder.glob("*.mscz"))
        if msczs:
            continue
        for vsa in sorted(folder.glob("*.vsa")):
            rel = vsa.relative_to(source).with_suffix(".svg")
            dest = SVG_ROOT / rel
            _render_one_vsa(vsa, dest)
            written += 1
            print(f"svg {rel.as_posix()}", flush=True)
    print(f"oefenhoek-bladermap svg: {written} bestand(en)", flush=True)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Oefenhoek-index: strip markdown; optioneel SVG uit .vsa."
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--svg",
        action="store_true",
        help="Schrijf SVG van lokale .vsa naar static/vsa/bladermap/",
    )
    args = p.parse_args()
    if args.svg:
        return render_svgs()
    return strip_indexes(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
