import logging
from typing import Dict, Any
from parsers.po_parser import POParser
from parsers.invoice_parser import InvoiceParser
from parsers.statement_parser import StatementParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Parser:
    _PARSERS = {
        'po': POParser,
        'invoice': InvoiceParser,
        'statement': StatementParser
    }
    
    def __init__(self):
        self._parser_instances = {}
    
    def parse(self, file_path: str, doc_type: str = "po") -> Dict[str, Any]:
        if doc_type not in self._PARSERS:
            raise ValueError(f"不支持的单据类型: {doc_type}，支持的类型: {list(self._PARSERS.keys())}")
        
        if doc_type not in self._parser_instances:
            self._parser_instances[doc_type] = self._PARSERS[doc_type]()
        
        parser = self._parser_instances[doc_type]
        return parser.parse(file_path)
    
    @classmethod
    def register_parser(cls, doc_type: str, parser_class):
        cls._PARSERS[doc_type] = parser_class
        logger.info(f"已注册新的单据解析器: {doc_type}")
