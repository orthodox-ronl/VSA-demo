"""Compatibility shim: gebruik ``check_partituur_products``."""

from check_partituur_products import *  # noqa: F403
from check_partituur_products import main

if __name__ == "__main__":
    raise SystemExit(main())
