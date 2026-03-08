"""Costing PDF Parser - 模块化PDF解析工具。"""

import os

os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("ONEDNN_VERBOSE", "0")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "True")
os.environ.setdefault("KMP_AFFINITY", "granularity=fine,compact,1,0")
os.environ.setdefault("FLAGS_use_mkldnn", "False")
os.environ.setdefault("FLAGS_use_ngraph", "False")

from .parser import Parser

__version__ = "0.1.0"
__all__ = ["Parser"]
