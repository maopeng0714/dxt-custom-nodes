"""Top-level package for dxt custom nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS"
]

__authors__ = ["MaoPeng <weizhishu007@gmail.com>"]
__author__ = ", ".join(__authors__)

__emails__ = ["weizhishu007@gmail.com"]
__email__ = ", ".join(__emails__)

__version__ = "1.0.0"

from .src.nodes import (NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS)
