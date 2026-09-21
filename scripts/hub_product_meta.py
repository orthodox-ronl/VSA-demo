"""Compatibility shim: gebruik ``partituur_product_meta``."""

from partituur_product_meta import *  # noqa: F403
from partituur_product_meta import (  # noqa: F401
    FIELD_HUB_SHA,
    FIELD_PARTITUUR_SHA,
    FIELD_PARTITUUR_SHA_LEGACY,
    SOURCE_KIND_HUB,
    SOURCE_KIND_PARTITUUR,
    hub_sha256,
    partituur_sha256,
    stamp_sha_from_dict,
)
