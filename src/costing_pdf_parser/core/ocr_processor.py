import logging
import os
import sys
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
                use_angle_cls=True,
                lang=Config.OCR_LANG,
                use_gpu=Config.OCR_USE_GPU,
                show_log=Config.OCR_SHOW_LOG,
                det_model_dir=Config.OCR_DET_MODEL_DIR,
                rec_model_dir=Config.OCR_REC_MODEL_DIR,
                cls_model_dir=Config.OCR_CLS_MODEL_DIR,
            )
            logger.info("OCR初始化成功")
        except Exception as e:
            logger.error(f"OCR初始化失败: {e}")
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
            result = self.ocr.ocr(img, cls=True)
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
            from paddleocr import PPStructure

            table_engine = PPStructure(
                show_log=Config.OCR_SHOW_LOG, use_gpu=Config.OCR_USE_GPU
            )
            img = preprocess_image(img)
            result = table_engine(img)
            logger.info("版面分析成功")
            return result
        except Exception as e:
            logger.error(f"版面分析失败: {e}")
            return []

    def parse_table(self, img):
        try:
            from paddleocr import PPStructure

            table_engine = PPStructure(
                show_log=Config.OCR_SHOW_LOG,
                use_gpu=Config.OCR_USE_GPU,
                structure_version="PP-StructureV2",
            )
            img = preprocess_image(img)
            result = table_engine(img)
            tables = []
            for res in result:
                if res["type"] == "table":
                    tables.append(res)
            logger.info(f"表格解析成功，共{len(tables)}个表格")
            return tables
        except Exception as e:
            logger.error(f"表格解析失败: {e}")
            return []
