import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

try:
    from ..core.ocr_processor import OCRProcessor
    from ..core.seal_extractor import SealExtractor
except ImportError:
    from core.ocr_processor import OCRProcessor
    from core.seal_extractor import SealExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseParser(ABC):
    def __init__(self):
        self.ocr_processor = OCRProcessor()
        self.seal_extractor = SealExtractor()
    
    def parse(self, pdf_path):
        result = {
            'success': False,
            'doc_type': self.doc_type,
            'fields': {},
            'tables': [],
            'seal': None,
            'raw_ocr': []
        }
        
        try:
            logger.info(f"开始解析{self.doc_type}文档: {pdf_path}")
            
            seal_result = self.seal_extractor.extract(pdf_path)
            result['seal'] = seal_result
            
            images = self.ocr_processor.pdf_to_images(pdf_path)
            if not images:
                logger.error("PDF转图像失败")
                return result
            
            ocr_results = []
            for img in images:
                ocr_text = self.ocr_processor.ocr_text(img)
                ocr_results.extend(ocr_text)
            
            result['raw_ocr'] = ocr_results
            
            result['fields'] = self._extract_fields(ocr_results)
            result['tables'] = self._extract_tables(images)
            
            result['success'] = True
            logger.info(f"{self.doc_type}文档解析成功")
            
        except Exception as e:
            logger.error(f"{self.doc_type}文档解析失败: {e}")
        
        return result
    
    @property
    @abstractmethod
    def doc_type(self):
        pass
    
    @abstractmethod
    def _extract_fields(self, ocr_results: List[Dict]) -> Dict:
        pass
    
    def _extract_tables(self, images):
        tables = []
        for img in images:
            table_results = self.ocr_processor.parse_table(img)
            tables.extend(table_results)
        return tables
    
    def _clean_table(self, table_data):
        return table_data
