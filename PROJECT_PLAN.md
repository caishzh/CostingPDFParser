# Costing PDF Parser 项目计划

## 项目概述
为公司成本组开发的Python模块化PDF解析工具，支持采购订单、发票、对账单等业务PDF文档的自动解析。

## 技术栈
- **OCR引擎**: PaddleOCR + PP-OCRv4_mobile (CPU版)
- **版面分析**: PP-StructureV2
- **图像处理**: OpenCV
- **PDF处理**: PyMuPDF (fitz)
- **运行环境**: Windows + i3 CPU + 无GPU

## 项目目录结构
```
CostingPDFParser/
├── config.py                    # 全局配置文件
├── requirements.txt             # Python依赖
├── main.py                      # 示例入口
├── core/                        # 核心模块
│   ├── __init__.py
│   ├── ocr_processor.py         # OCR封装类
│   └── seal_extractor.py        # 独立印章提取类
├── parsers/                     # 单据解析模块
│   ├── __init__.py
│   ├── base_parser.py           # 解析基类
│   ├── po_parser.py             # 采购订单解析
│   ├── invoice_parser.py        # 发票解析
│   └── statement_parser.py      # 对账单解析
├── utils/                       # 工具模块
│   ├── __init__.py
│   ├── pdf_utils.py
│   └── image_utils.py
└── parser.py                    # 统一调度入口
```

## 核心模块设计

### 1. config.py - 配置文件
- OCR模型路径配置
- 印章提取参数配置
- 日志配置

### 2. core/ocr_processor.py - OCR封装类
```python
class OCRProcessor:
    def pdf_to_images(self, pdf_path):
        # PDF转图像
    def ocr_text(self, img):
        # OCR文字识别
    def layout_analysis(self, img):
        # 版面分析
    def parse_table(self, img):
        # 表格解析
```

### 3. core/seal_extractor.py - 印章提取类
```python
class SealExtractor:
    def extract(self, pdf_path):
        # 主入口：提取印章
    def _pdf_to_cv2(self, pdf_path):
        # PDF转OpenCV图像
    def _extract_red_seal(self, img):
        # HSV红色范围提取
    def _remove_black_text(self, mask, gray_img):
        # 去除黑字
    def _morphology_close(self, mask):
        # 闭运算修补
    def _find_contours(self, mask):
        # 轮廓检测
    def _crop_seal(self, img, contour):
        # 裁剪印章
    def _ocr_seal_text(self, seal_img):
        # 印章文字识别
```

### 4. parsers/base_parser.py - 解析基类
```python
class BaseParser:
    def parse(self, pdf_path):
        # 统一解析流程
    def _extract_fields(self, ocr_result):
        # 提取字段（子类实现）
    def _clean_table(self, table_data):
        # 清洗表格
```

### 5. parser.py - 统一调度入口
```python
class Parser:
    def parse(self, file_path, doc_type="po"):
        # 自动分发到对应解析类
```

## 开发步骤
1. 创建项目目录结构
2. 创建依赖文件requirements.txt
3. 实现配置文件config.py
4. 实现底层OCR封装类
5. 实现独立印章提取类
6. 实现单据解析基类
7. 实现PO/Invoice/Statement解析子类
8. 实现统一调度入口
9. 创建示例代码

## 性能目标
- 单页全流程 ≤8秒
- 纯CPU i3流畅运行
- 无GPU依赖
