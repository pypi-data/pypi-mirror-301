"""Deprecated module."""

from mt.logg import logger

logger.warn_module_move("wml.core.datatype.code_mapping", "wml.core.code_mapping")

from ..code_mapping import *
