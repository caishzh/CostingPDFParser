# 安装说明

## 方式一：开发模式安装（推荐用于开发）

在项目根目录下执行：

```bash
pip install -e .
```

这样安装后，你修改代码会立即生效，不需要重新安装。

## 方式二：标准安装

```bash
pip install .
```

## 使用方式

安装后，你可以在任何地方导入使用：

```python
from costing_pdf_parser import Parser

parser = Parser()
result = parser.parse("your_file.pdf", doc_type="po")
```

或者：

```python
import costing_pdf_parser

parser = costing_pdf_parser.Parser()
result = parser.parse("your_file.pdf", doc_type="po")
```

## 卸载

```bash
pip uninstall costing-pdf-parser
```
