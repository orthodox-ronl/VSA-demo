"""Oefenhoek: elk _index.md en index.md (niet input/) heeft publicatiestatus."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OEFENHOEK = REPO_ROOT / "content-source" / "praktijk" / "oefenhoek"
VALID = frozenset({"voorzien", "concept", "reviewable", "productie"})
NAMES = frozenset({"_index.md", "index.md"})


def _status(text: str) -> str | None:
    in_fm = False
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm and line.lower().startswith("publicatiestatus:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def main() -> int:
    if not OEFENHOEK.is_dir():
        print("FAIL: oefenhoek ontbreekt.", flush=True)
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
        status = _status(path.read_text(encoding="utf-8"))
        if not status:
            errors.append(f"{rel}: publicatiestatus ontbreekt")
        elif status not in VALID:
            errors.append(f"{rel}: onbekende publicatiestatus {status!r}")
    if errors:
        for line in errors:
            print(f"FAIL: {line}", flush=True)
        return 1
    print(f"Oefenhoek publicatiestatus: {checked} pagina('s) OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
