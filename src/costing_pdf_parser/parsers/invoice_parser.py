import logging
from typing import Dict, List
from .base_parser import BaseParser

logger = logging.getLogger(__name__)

class InvoiceParser(BaseParser):
    @property
    def doc_type(self):
        return "invoice"
    
    def _extract_fields(self, ocr_results: List[Dict]) -> Dict:
        fields = {
            'invoice_number': '',
            'company': '',
            'tax_id': '',
            'date': '',
            'total_amount': '',
            'tax_amount': ''
        }
        
        all_text = ' '.join([item['text'] for item in ocr_results])
        
        keywords = {
            'invoice_number': ['发票号码', '发票号', 'Invoice No'],
            'company': ['公司名称', '开票方', 'Company'],
            'tax_id': ['税号', '纳税人识别号', 'Tax ID'],
            'date': ['开票日期', '日期', 'Date'],
            'total_amount': ['价税合计', '总金额', 'Total'],
            'tax_amount': ['税额', 'Tax Amount']
        }
        
        for field, keys in keywords.items():
            for key in keys:
                if key in all_text:
                    fields[field] = f'需根据实际格式提取: {key}'
                    break
        
        logger.info(f"Invoice字段提取: {fields}")
        return fields
