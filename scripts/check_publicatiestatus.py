"""Oefenhoek: elk _index.md en index.md (niet input/) heeft
publicatiestatus en automatische_inhoud."""
from __future__ import annotations

from pathlib import Path

from _diag import format_issue, frontmatter_key_line

REPO_ROOT = Path(__file__).resolve().parents[1]
OEFENHOEK = REPO_ROOT / "content-source" / "praktijk" / "oefenhoek"
VALID = frozenset({"voorzien", "concept", "reviewable", "productie"})
AUTO_VALID = frozenset({"true", "false"})
NAMES = frozenset({"_index.md", "index.md"})


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


def main() -> int:
    if not OEFENHOEK.is_dir():
        print(
            format_issue(
                "content-source/praktijk/oefenhoek",
                "Oefenhoek-map ontbreekt",
                fix="controleer of content-source/praktijk/oefenhoek bestaat",
            ),
            flush=True,
        )
        return 1
    errors: list[str] = []
    checked = 0
    for path in sorted(OEFENHOEK.rglob("*.md")):
        if "input" in path.relative_to(OEFENHOEK).parts:
            continue
        if path.name not in NAMES:
            continue
        checked += 1
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        status = _fm_value(text, "publicatiestatus")
        status_line = frontmatter_key_line(text, "publicatiestatus")
        if not status:
            errors.append(
                format_issue(
                    rel,
                    "publicatiestatus ontbreekt in de frontmatter",
                    fix=(
                        "zet publicatiestatus op voorzien, concept, "
                        "reviewable of productie"
                    ),
                )
            )
        elif status not in VALID:
            errors.append(
                format_issue(
                    rel,
                    f"onbekende publicatiestatus {status!r}",
                    line=status_line,
                    fix=(
                        "gebruik precies: voorzien, concept, "
                        "reviewable of productie"
                    ),
                )
            )
        auto = (_fm_value(text, "automatische_inhoud") or "").lower()
        auto_line = frontmatter_key_line(text, "automatische_inhoud")
        if not auto:
            errors.append(
                format_issue(
                    rel,
                    "automatische_inhoud ontbreekt in de frontmatter",
                    fix="zet automatische_inhoud op true of false",
                )
            )
        elif auto not in AUTO_VALID:
            errors.append(
                format_issue(
                    rel,
                    f"onbekende automatische_inhoud {auto!r}",
                    line=auto_line,
                    fix="gebruik precies: true of false",
                )
            )
    if errors:
        for line in errors:
            print(f"FAIL: {line}", flush=True)
        return 1
    print(f"Oefenhoek frontmatter: {checked} pagina('s) OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
