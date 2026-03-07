import logging
from typing import Dict, List

from .base_parser import BaseParser

logger = logging.getLogger(__name__)


class POParser(BaseParser):
    @property
    def doc_type(self):
        return "po"

    def _extract_fields(self, ocr_results: List[Dict]) -> Dict:
        fields = {
            "po_number": "",
            "supplier": "",
            "date": "",
            "total_amount": "",
        }

        all_text = " ".join([item["text"] for item in ocr_results])

        keywords = {
            "po_number": ["PO号", "采购订单号", "订单号", "PO No"],
            "supplier": ["供应商", "供货方", "Supplier"],
            "date": ["日期", "Date", "下单日期"],
            "total_amount": ["总金额", "合计", "Total", "金额"],
        }

        for field, keys in keywords.items():
            for key in keys:
                if key in all_text:
                    fields[field] = f"需根据实际格式提取: {key}"
                    break

        logger.info(f"PO字段提取: {fields}")
        return fields
