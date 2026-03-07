#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Costing PDF Parser - 示例使用代码
"""

import json


def main():
    print("=" * 60)
    print("Costing PDF Parser - 示例")
    print("=" * 60)

    print("\n方式一：作为包导入（安装后使用）")
    print("  from costing_pdf_parser import Parser")
    print("  parser = Parser()")
    print("  result = parser.parse('your_file.pdf', doc_type='po')")

    print("\n方式二：本地直接导入（开发时使用）")
    print("  from parser import Parser")
    print("  parser = Parser()")
    print("  result = parser.parse('your_file.pdf', doc_type='po')")

    print("\n" + "=" * 60)
    print("提示：先运行 'pip install -e .' 安装包")
    print("=" * 60)


if __name__ == "__main__":
    main()
