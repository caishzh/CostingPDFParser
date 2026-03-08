import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..core.ocr_processor import OCRProcessor
from ..core.seal_extractor import SealExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """单据解析器基类，所有具体单据解析器的父类。

    子类需要实现:
        - doc_type 属性: 返回单据类型字符串
        - _extract_fields() 方法: 从OCR结果中提取字段
    """

    def __init__(self, use_onednn: bool = None):
        self.use_onednn = use_onednn
        self._ocr_processor = None
        self._seal_extractor = None

    @property
    def ocr_processor(self):
        """OCR处理器实例（延迟初始化）。"""
        if self._ocr_processor is None:
            self._ocr_processor = OCRProcessor(use_onednn=self.use_onednn)
        return self._ocr_processor

    @property
    def seal_extractor(self):
        """印章提取器实例（延迟初始化）。"""
        if self._seal_extractor is None:
            self._seal_extractor = SealExtractor(use_onednn=self.use_onednn)
        return self._seal_extractor

    def parse(self, pdf_path):
        """解析PDF文档的完整流程。

        Args:
            pdf_path: PDF文件路径。

        Returns:
            包含解析结果的字典，结构如下:
                {
                    'success': bool,
                    'doc_type': str,
                    'fields': Dict,
                    'tables': List,
                    'seal': Dict,
                    'raw_ocr': List
                }
        """
        result = {
            "success": False,
            "doc_type": self.doc_type,
            "fields": {},
            "tables": [],
            "seal": None,
            "raw_ocr": [],
        }

        try:
            logger.info(f"开始解析{self.doc_type}文档: {pdf_path}")

            seal_result = self.seal_extractor.extract(pdf_path)
            result["seal"] = seal_result

            images = self.ocr_processor.pdf_to_images(pdf_path)
            if not images:
                logger.error("PDF转图像失败")
                return result

            ocr_results = []
            for img in images:
                ocr_text = self.ocr_processor.ocr_text(img)
                ocr_results.extend(ocr_text)

            result["raw_ocr"] = ocr_results

            result["fields"] = self._extract_fields(ocr_results)
            result["tables"] = self._extract_tables(images)

            result["success"] = True
            logger.info(f"{self.doc_type}文档解析成功")

        except Exception as e:
            logger.error(f"{self.doc_type}文档解析失败: {e}")

        return result

    @property
    @abstractmethod
    def doc_type(self):
        """返回单据类型标识字符串。"""
        pass

    @abstractmethod
    def _extract_fields(self, ocr_results: List[Dict]) -> Dict:
        """从OCR结果中提取业务字段。

        Args:
            ocr_results: OCR识别结果列表。

        Returns:
            包含提取字段的字典。
        """
        pass

    def _extract_tables(self, images):
        """从PDF页面中提取表格数据。

        Args:
            images: PDF页面图像列表。

        Returns:
            表格数据列表。
        """
        tables = []
        for img in images:
            table_results = self.ocr_processor.parse_table(img)
            tables.extend(table_results)
        return tables

    def _clean_table(self, table_data):
        """清洗表格数据（子类可覆盖）。

        Args:
            table_data: 原始表格数据。

        Returns:
            清洗后的表格数据。
        """
        return table_data
