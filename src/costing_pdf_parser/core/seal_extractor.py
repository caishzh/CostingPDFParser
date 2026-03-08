import logging
import os

os.environ["FLAGS_use_mkldnn"] = "False"
os.environ["FLAGS_use_ngraph"] = "False"

from typing import Any, Dict, Optional

import cv2
import numpy as np
from paddleocr import PaddleOCR

from ..config import Config
from ..utils.pdf_utils import pdf_to_cv2

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class SealExtractor:
    """印章提取器，基于OpenCV和PP-OCR提取红色印章。"""

    def __init__(self):
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=False,
                lang="ch",
            )
            logger.info("印章OCR初始化成功")
        except Exception as e:
            try:
                self.ocr = PaddleOCR(lang="ch")
                logger.info("印章OCR初始化成功（最简参数）")
            except Exception as e2:
                logger.error(f"印章OCR初始化失败: {e2}")
                raise

    def extract(self, pdf_path):
        result = {
            "pdf2img_status": False,
            "seal_crop_img": None,
            "seal_text": "",
            "confidence": 0.0,
            "detail": {
                "circular_text": "",
                "center_text": "",
                "number": "",
                "confidences": [],
            },
        }

        try:
            img = self._pdf_to_cv2(pdf_path)
            if img is None:
                logger.error("PDF转图像失败")
                return result

            result["pdf2img_status"] = True

            seal_mask = self._extract_red_seal(img)
            if seal_mask is None:
                logger.warning("未检测到红色印章")
                return result

            seal_mask = self._remove_black_text(seal_mask, img)
            seal_mask = self._morphology_close(seal_mask)

            contour = self._find_contours(seal_mask)
            if contour is None:
                logger.warning("未找到有效印章轮廓")
                return result

            seal_img, seal_bbox = self._crop_seal(img, contour)
            if seal_img is None:
                logger.warning("印章裁剪失败")
                return result

            result["seal_crop_img"] = seal_img

            ocr_result = self._ocr_seal_text(seal_img)
            result["seal_text"] = ocr_result["text"]
            result["confidence"] = ocr_result["confidence"]
            result["detail"] = ocr_result["detail"]

            logger.info("印章提取成功")

        except Exception as e:
            logger.error(f"印章提取失败: {e}")

        return result

    def _pdf_to_cv2(self, pdf_path):
        try:
            return pdf_to_cv2(pdf_path, dpi=200)
        except Exception as e:
            logger.error(f"PDF转CV2图像失败: {e}")
            return None

    def _extract_red_seal(self, img):
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower1 = np.array(Config.SEAL_HSV_LOWER1)
            upper1 = np.array(Config.SEAL_HSV_UPPER1)
            mask1 = cv2.inRange(hsv, lower1, upper1)

            lower2 = np.array(Config.SEAL_HSV_LOWER2)
            upper2 = np.array(Config.SEAL_HSV_UPPER2)
            mask2 = cv2.inRange(hsv, lower2, upper2)

            mask = cv2.bitwise_or(mask1, mask2)
            return mask
        except Exception as e:
            logger.error(f"红色印章提取失败: {e}")
            return None

    def _remove_black_text(self, mask, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            black_mask = gray < Config.SEAL_BLACK_THRESHOLD
            mask[black_mask] = 0
            return mask
        except Exception as e:
            logger.error(f"黑字消除失败: {e}")
            return mask

    def _morphology_close(self, mask):
        try:
            kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, Config.SEAL_KERNEL_SIZE
            )
            return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        except Exception as e:
            logger.error(f"闭运算失败: {e}")
            return mask

    def _find_contours(self, mask):
        try:
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            valid_contours = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area >= Config.SEAL_MIN_AREA:
                    valid_contours.append((area, cnt))

            if not valid_contours:
                return None

            valid_contours.sort(key=lambda x: x[0], reverse=True)
            return valid_contours[0][1]
        except Exception as e:
            logger.error(f"轮廓检测失败: {e}")
            return None

    def _crop_seal(self, img, contour):
        try:
            x, y, w, h = cv2.boundingRect(contour)

            size = max(w, h)
            size = max(size, Config.SEAL_MIN_CROP_SIZE)
            size = min(size, Config.SEAL_MAX_CROP_SIZE)

            center_x = x + w // 2
            center_y = y + h // 2

            x1 = max(0, center_x - size // 2)
            y1 = max(0, center_y - size // 2)
            x2 = min(img.shape[1], x1 + size)
            y2 = min(img.shape[0], y1 + size)

            seal_img = img[y1:y2, x1:x2]
            return seal_img, (x1, y1, x2, y2)
        except Exception as e:
            logger.error(f"印章裁剪失败: {e}")
            return None, None

    def _ocr_seal_text(self, seal_img):
        result = {
            "text": "",
            "confidence": 0.0,
            "detail": {
                "circular_text": "",
                "center_text": "",
                "number": "",
                "confidences": [],
            },
        }

        try:
            ocr_output = self.ocr.ocr(seal_img)

            if ocr_output and ocr_output[0]:
                texts = []
                confidences = []

                for line in ocr_output[0]:
                    text = line[1][0]
                    conf = line[1][1]
                    texts.append(text)
                    confidences.append(conf)

                result["text"] = "".join(texts)
                if confidences:
                    result["confidence"] = sum(confidences) / len(confidences)
                result["detail"]["confidences"] = confidences

                for text in texts:
                    if any(c.isdigit() for c in text) and len(text) <= 10:
                        result["detail"]["number"] = text
                    elif len(text) > 5:
                        result["detail"]["circular_text"] += text
                    else:
                        result["detail"]["center_text"] += text

            logger.info(f"印章文字识别: {result['text']}")

        except Exception as e:
            logger.error(f"印章文字识别失败: {e}")

        return result
