"""Costing PDF Parser - 模块化PDF解析工具。"""

import os
import sys

# 兼容 Python 3.13：imghdr 模块被移除，添加兼容层
try:
    import imghdr
except ImportError:
    class Imghdr:
        @staticmethod
        def what(file, h=None):
            if h is None:
                if isinstance(file, str):
                    with open(file, 'rb') as f:
                        h = f.read(32)
                else:
                    location = file.tell()
                    h = file.read(32)
                    file.seek(location)
            
            if h[6:10] in (b'JFIF', b'Exif'):
                return 'jpeg'
            if h.startswith(b'\211PNG\r\n\032\n'):
                return 'png'
            if h[:6] in (b'GIF87a', b'GIF89a'):
                return 'gif'
            if h.startswith(b'BM'):
                return 'bmp'
            if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
                return 'webp'
            return None
    
    sys.modules['imghdr'] = Imghdr()

os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("ONEDNN_VERBOSE", "0")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "True")
os.environ.setdefault("KMP_AFFINITY", "granularity=fine,compact,1,0")
os.environ.setdefault("FLAGS_use_mkldnn", "False")
os.environ.setdefault("FLAGS_use_ngraph", "False")
os.environ.setdefault("FLAGS_allocator_strategy", "naive_best_fit")
os.environ.setdefault("FLAGS_enable_onednn_ops", "False")
os.environ.setdefault("FLAGS_enable_onednn", "False")
os.environ.setdefault("FLAGS_onednn_ops_list", "")
os.environ.setdefault("DNNL_VERBOSE", "0")

from .parser import Parser

__version__ = "0.1.0"
__all__ = ["Parser"]
