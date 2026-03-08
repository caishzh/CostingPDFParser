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
├── pyproject.toml               # 项目配置
├── requirements.txt             # Python依赖
├── README.md                    # 项目说明
├── src/
│   └── costing_pdf_parser/      # 核心包
│       ├── __init__.py
│       ├── config.py            # 全局配置
│       ├── parser.py            # 统一调度入口
│       ├── core/                # 核心模块
│       │   ├── ocr_processor.py # OCR封装类
│       │   └── seal_extractor.py # 独立印章提取类
│       ├── parsers/             # 单据解析模块
│       │   ├── base_parser.py   # 解析基类
│       │   ├── po_parser.py     # 采购订单解析
│       │   ├── invoice_parser.py # 发票解析
│       │   └── statement_parser.py # 对账单解析
│       └── utils/               # 工具模块
│           ├── pdf_utils.py
│           └── image_utils.py
└── test/                        # 测试文件（gitignore）
```

## 快速开始

### 前置条件（新手必读）

在开始之前，请确保你的电脑上已经安装了：

1. **Python 3.8 或更高版本**
   - 下载地址：https://www.python.org/downloads/
   - 安装时请勾选 "Add Python to PATH"
   - 验证安装：打开终端（Windows 按 Win+R，输入 cmd），输入 `python --version` 或 `python3 --version`

2. **Git**
   - 下载地址：https://git-scm.com/downloads
   - 验证安装：打开终端，输入 `git --version`

---

### 步骤 1：克隆项目代码

打开终端，输入以下命令：

```bash
git clone https://github.com/caishzh/CostingPDFParser.git
cd CostingPDFParser
```

> 说明：
> - `git clone` 会把代码下载到你的电脑上
> - `cd CostingPDFParser` 会进入项目文件夹

---

### 步骤 2：创建虚拟环境（推荐，新手友好）

虚拟环境可以避免依赖冲突，建议新手使用：

**Windows 用户：**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux 用户：**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 成功激活后，终端前面会显示 `(venv)` 字样

---

### 步骤 3：安装依赖（推荐方法）

```bash
pip install -e .
```

> 说明：
> - `-e` 表示可编辑模式，修改代码后不需要重新安装
> - `.` 表示当前目录（即 pyproject.toml 所在目录）
> - 安装过程中会自动下载所有需要的库（包括 PaddleOCR）

**如果上面的方法失败，使用备选方法：**
```bash
pip install -r requirements.txt
```

---

### 步骤 4：运行测试

#### 4.1 测试安装是否成功

在终端中输入：
```bash
python -c "from costing_pdf_parser import Parser; print('安装成功！')"
```

如果看到 "安装成功！"，说明安装没问题。

#### 4.2 解析你的第一个 PDF

在项目根目录下创建一个名为 `test_my_pdf.py` 的文件，内容如下：

```python
from costing_pdf_parser import Parser

def main():
    print("开始解析 PDF...")
    
    parser = Parser()
    
    pdf_path = "你的PDF文件路径.pdf"
    doc_type = "po"
    
    result = parser.parse(pdf_path, doc_type=doc_type)
    
    print("\n解析结果：")
    print(result)

if __name__ == "__main__":
    main()
```

然后运行：
```bash
python test_my_pdf.py
```

---

### 常见问题（新手必看）

**Q: 提示 "python 不是内部或外部命令" 怎么办？**
A: 说明 Python 没有添加到 PATH，请重新安装 Python 并勾选 "Add Python to PATH"。

**Q: 安装 PaddleOCR 很慢怎么办？**
A: 使用国内镜像源加速：
```bash
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 提示 "ModuleNotFoundError"？**
A: 确保虚拟环境已激活（终端前有 `(venv)`），然后重新运行安装命令。

**Q: Windows 下激活虚拟环境报错？**
A: 打开 PowerShell（管理员），输入：
```powershell
Set-ExecutionPolicy RemoteSigned
```
然后重新尝试激活。

## 支持的单据类型

| 类型 | doc_type | 说明 |
|------|----------|------|
| 采购订单 | po | Purchase Order |
| 发票 | invoice | 增值税发票等 |
| 对账单 | statement | 往来对账单 |

## 扩展新的单据类型

只需三步即可添加新的单据解析器：

1. 在 `src/costing_pdf_parser/parsers/` 目录下创建新文件，继承 `BaseParser`
2. 实现 `doc_type` 属性和 `_extract_fields` 方法
3. 注册到 `Parser` 类

```python
from costing_pdf_parser.parsers.base_parser import BaseParser

class ContractParser(BaseParser):
    @property
    def doc_type(self):
        return "contract"
    
    def _extract_fields(self, ocr_results):
        return {"field1": "value1"}

# 注册新解析器
from costing_pdf_parser import Parser
Parser.register_parser("contract", ContractParser)
```

## 配置说明

编辑 `src/costing_pdf_parser/config.py` 调整参数：

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
