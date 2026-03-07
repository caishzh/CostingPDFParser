import os

os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")

from .parser import Parser

__version__ = "0.1.0"
__all__ = ["Parser"]
