"""Controleer bibliotheek-id in hub-.mscz (meta + colofon).

Dunne wrapper om `ensure_bibliotheek_id.py --check-only`.
"""
from __future__ import annotations

import sys

from ensure_bibliotheek_id import main as ensure_main


def main() -> int:
    argv = sys.argv[1:]
    if "--check-only" not in argv:
        argv = ["--check-only", *argv]
    sys.argv = [sys.argv[0], *argv]
    return ensure_main()


if __name__ == "__main__":
    raise SystemExit(main())
