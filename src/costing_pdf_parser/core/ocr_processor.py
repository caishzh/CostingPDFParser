import logging
import os
import sys

os.environ["FLAGS_use_mkldnn"] = "False"
os.environ["FLAGS_use_ngraph"] = "False"

from typing import Any, Dict, List

from paddleocr import PaddleOCR

from ..config import Config
from ..utils.image_utils import preprocess_image, resize_image
from ..utils.pdf_utils import pdf_to_images

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class OCRProcessor:
    """OCR处理器，封装PaddleOCR和PP-StructureV2的功能。"""

    def __init__(self):
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=False,
                lang=Config.OCR_LANG,
            )
            logger.info("OCR初始化成功")
        except Exception as e:
            try:
                self.ocr = PaddleOCR(lang=Config.OCR_LANG)
                logger.info("OCR初始化成功（最简参数）")
            except Exception as e2:
                logger.error(f"OCR初始化失败: {e2}")
                raise

    def pdf_to_images(self, pdf_path, dpi=200):
        try:
            images = pdf_to_images(pdf_path, dpi)
            logger.info(f"PDF转图像成功，共{len(images)}页")
            return images
        except Exception as e:
            logger.error(f"PDF转图像失败: {e}")
            raise

    def ocr_text(self, img):
        try:
            img = preprocess_image(img)
            img = resize_image(img)
            
            import os
            old_mkldnn = os.environ.get("FLAGS_use_mkldnn")
            os.environ["FLAGS_use_mkldnn"] = "False"
            
            result = self.ocr.ocr(img)
            
            if old_mkldnn is not None:
                os.environ["FLAGS_use_mkldnn"] = old_mkldnn
            else:
                os.environ.pop("FLAGS_use_mkldnn", None)
                
            if result and result[0]:
                texts = []
                for line in result[0]:
                    texts.append(
                        {
                            "bbox": line[0],
                            "text": line[1][0],
                            "confidence": line[1][1],
                        }
                    )
                return texts
            return []
        except Exception as e:
            logger.error(f"OCR文字识别失败: {e}")
            return []

    def layout_analysis(self, img):
        try:
            img = preprocess_image(img)
            logger.info("版面分析功能暂时跳过")
            return []
        except Exception as e:
            logger.error(f"版面分析失败: {e}")
            return []

    def parse_table(self, img):
        try:
            img = preprocess_image(img)
            logger.info("表格解析功能暂时跳过")
            return []
        except Exception as e:
            logger.error(f"表格解析失败: {e}")
            return []
