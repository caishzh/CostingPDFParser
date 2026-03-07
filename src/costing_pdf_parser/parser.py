import logging
from typing import Any, Dict

from .parsers.invoice_parser import InvoiceParser
from .parsers.po_parser import POParser
from .parsers.statement_parser import StatementParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parser:
    """统一调度入口类，负责根据单据类型分发到对应的解析器。

    示例用法:
        >>> from costing_pdf_parser import Parser
        >>> parser = Parser()
        >>> result = parser.parse("po.pdf", doc_type="po")
    """

    _PARSERS = {
        "po": POParser,
        "invoice": InvoiceParser,
        "statement": StatementParser,
    }

    def __init__(self):
        self._parser_instances = {}

    def parse(self, file_path: str, doc_type: str = "po") -> Dict[str, Any]:
        """解析PDF文档。

        Args:
            file_path: PDF文件路径。
            doc_type: 单据类型，可选值: "po", "invoice", "statement"。

        Returns:
            包含解析结果的字典。

        Raises:
            ValueError: 当doc_type不支持时抛出。
        """
        if doc_type not in self._PARSERS:
            raise ValueError(
                f"不支持的单据类型: {doc_type}，支持的类型: {list(self._PARSERS.keys())}"
            )

        if doc_type not in self._parser_instances:
            self._parser_instances[doc_type] = self._PARSERS[doc_type]()

        parser = self._parser_instances[doc_type]
        return parser.parse(file_path)

    @classmethod
    def register_parser(cls, doc_type: str, parser_class):
        """注册新的单据解析器。

        Args:
            doc_type: 单据类型标识。
            parser_class: 解析器类，需继承自BaseParser。
        """
        cls._PARSERS[doc_type] = parser_class
        logger.info(f"已注册新的单据解析器: {doc_type}")
