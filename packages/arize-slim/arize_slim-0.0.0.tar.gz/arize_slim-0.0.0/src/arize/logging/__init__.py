import logging
import sys

from .formatter import CustomLogFormatter

logger = logging.getLogger("arize")
logger.propagate = False
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.INFO)
fmt = "  %(name)s | %(levelname)s | %(message)s"
if hasattr(sys, "ps1"):  # for python interactive mode
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(CustomLogFormatter(fmt))
    logger.addHandler(handler)
