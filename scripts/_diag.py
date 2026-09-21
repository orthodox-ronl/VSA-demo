"""Gedeelde formattering voor check-/pipeline-foutmeldingen."""

from __future__ import annotations

from pathlib import Path


def format_issue(
    path: str | Path,
    message: str,
    *,
    line: int | None = None,
    column: int | None = None,
    fix: str | None = None,
) -> str:
    """Bouw ``pad[:regel[:kolom]]: melding`` plus optionele ``Oplossing:``-regel."""
    loc = Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")
    if line is not None and line > 0:
        if column is not None and column > 0:
            loc = f"{loc}:{line}:{column}"
        else:
            loc = f"{loc}:{line}"
    text = f"{loc}: {message}"
    if fix:
        text = f"{text}\n  Oplossing: {fix}"
    return text


def frontmatter_key_line(text: str, key: str) -> int | None:
    """1-based regelnummer van ``key:`` in YAML-frontmatter, of None."""
    in_fm = False
    prefix = f"{key.lower()}:"
    for index, line in enumerate(text.splitlines(), start=1):
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm and line.lower().startswith(prefix):
            return index
    return None
