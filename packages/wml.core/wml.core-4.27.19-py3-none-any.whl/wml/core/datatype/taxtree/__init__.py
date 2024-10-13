"""Package managing taxtrees.

A taxcodeset is defined as a set of taxcodes. It is represented as (a json string of) a list of
taxcodes.
"""

from ..taxcode import valid_taxcode
from .base import Taxtree, load_taxtree
from .extra import (
    LeafsetMapper,
    check_disjoint,
    merge2base_taxtree_df,
    merge2sealed_taxtree_df,
)


__all__ = [
    "valid_taxcode",
    "Taxtree",
    "load_taxtree",
    "LeafsetMapper",
    "check_disjoint",
    "merge2base_taxtree_df",
    "merge2sealed_taxtree_df",
]
