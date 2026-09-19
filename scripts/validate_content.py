"""Runt vsa validate; optioneel falen op warnings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from vsa.validation_display import format_validation_message
from vsa.validation_runner import validate_path

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate content-source; optioneel fail-on-warnings.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(REPO_ROOT / "content-source"),
        help="Pad naar content (default: content-source).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Compacte validatie-output.",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Exit 1 ook bij warnings (zonder errors).",
    )
    return parser.parse_args()


def _validation_context_line(
    source: str,
    line_number: int,
    cache: dict[str, list[str]],
) -> str | None:
    if source not in cache:
        path = Path(source)
        if not path.is_file():
            return None
        cache[source] = path.read_text(encoding="utf-8").splitlines()

    lines = cache[source]
    if line_number < 1 or line_number > len(lines):
        return None
    return lines[line_number - 1]


def main() -> int:
    args = parse_args()
    result = validate_path(args.path)
    source_lines: dict[str, list[str]] = {}

    if result.messages:
        for message in result.messages:
            source_line = None
            if not args.summary:
                source_line = _validation_context_line(
                    message.source,
                    message.line,
                    source_lines,
                )
            for line in format_validation_message(
                message,
                summary=args.summary,
                source_line=source_line,
            ):
                print(line)
    else:
        print("OK")

    if not result.ok:
        return 1

    if args.fail_on_warnings and result.has_warnings():
        print(
            "FAIL: validatie-warnings aanwezig (--fail-on-warnings).",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
