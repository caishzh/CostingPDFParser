# Costing PDF Parser

为公司成本组开发的模块化PDF解析工具，支持采购订单、发票、对账单等业务PDF文档的自动解析。

## 特性

- 🚀 **模块化架构**：可轻松扩展新的单据类型
- 🔍 **独立印章提取**：基于OpenCV+PP-OCR的印章识别模块
- 📄 **PP-StructureV2**：版面分析和表格识别
- 💻 **纯CPU运行**：优化的i3笔记本性能
- 📦 **一行调用**：简单易用的API接口

## 项目结构

```
CostingPDFParser/
├── config.py                    # 全局配置
├── requirements.txt             # Python依赖
├── main.py                      # 示例入口
├── parser.py                    # 统一调度入口
├── core/                        # 核心模块
│   ├── ocr_processor.py         # OCR封装类
│   └── seal_extractor.py        # 独立印章提取类
├── parsers/                     # 单据解析模块
│   ├── base_parser.py           # 解析基类
│   ├── po_parser.py             # 采购订单解析
│   ├── invoice_parser.py        # 发票解析
│   └── statement_parser.py      # 对账单解析
└── utils/                       # 工具模块
    ├── pdf_utils.py
    └── image_utils.py
```

## 快速开始

### 1. 克隆仓库

```bash
git clone <your-github-repo-url>
cd CostingPDFParser
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 一行代码使用

```python
from parser import Parser

parser = Parser()
result = parser.parse("your_file.pdf", doc_type="po")
print(result)
```

## 支持的单据类型

| 类型 | doc_type | 说明 |
|------|----------|------|
| 采购订单 | po | Purchase Order |
| 发票 | invoice | 增值税发票等 |
| 对账单 | statement | 往来对账单 |

## 扩展新的单据类型

只需三步即可添加新的单据解析器：

1. 在 `parsers/` 目录下创建新文件，继承 `BaseParser`
2. 实现 `doc_type` 属性和 `_extract_fields` 方法
3. 注册到 `Parser` 类

```python
from parsers.base_parser import BaseParser

class ContractParser(BaseParser):
    @property
    def doc_type(self):
        return "contract"
    
    def _extract_fields(self, ocr_results):
        return {"field1": "value1"}

# 注册新解析器
from parser import Parser
Parser.register_parser("contract", ContractParser)
```

## 配置说明

编辑 `config.py` 调整参数：

```python
# OCR配置
OCR_USE_GPU = False  # 强制CPU
OCR_LANG = "ch"

# 印章提取配置
SEAL_HSV_LOWER1 = (0, 70, 70)
SEAL_HSV_UPPER1 = (10, 255, 255)
# ... 更多配置
```

## 印章提取模块输出

```python
{
    'pdf2img_status': True,
    'seal_crop_img': <numpy.ndarray>,
    'seal_text': 'XX有限公司公章',
    'confidence': 0.95,
    'detail': {
        'circular_text': 'XX有限公司',
        'center_text': '公章',
        'number': '123456',
        'confidences': [0.98, 0.92, 0.95]
    }
}
```

## 性能指标

- 纯CPU i3笔记本流畅运行
- 单页全流程 ≤8秒
- 无GPU依赖

## 系统要求

- Windows / Linux / macOS
- Python 3.8+
- i3或以上CPU
- 4GB+ RAM

## 许可证

MIT License
