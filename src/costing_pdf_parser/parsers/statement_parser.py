import logging
from typing import Dict, List

from .base_parser import BaseParser

logger = logging.getLogger(__name__)


class StatementParser(BaseParser):
    """对账单解析器。"""

    @property
    def doc_type(self):
        return "statement"

    def _extract_fields(self, ocr_results: List[Dict]) -> Dict:
        fields = {
            "statement_number": "",
            "customer": "",
            "period": "",
            "opening_balance": "",
            "closing_balance": "",
        }

        all_text = " ".join([item["text"] for item in ocr_results])

        keywords = {
            "statement_number": ["对账单号", "Statement No"],
            "customer": ["客户", "Customer"],
            "period": ["期间", "Period", "对账周期"],
            "opening_balance": ["期初余额", "Opening Balance"],
            "closing_balance": ["期末余额", "Closing Balance"],
        }

        for field, keys in keywords.items():
            for key in keys:
                if key in all_text:
                    fields[field] = f"需根据实际格式提取: {key}"
                    break

        logger.info(f"Statement字段提取: {fields}")
        return fields
