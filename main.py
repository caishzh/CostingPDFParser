#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Costing PDF Parser - 示例使用代码
"""

from parser import Parser
import json

def main():
    print("=" * 60)
    print("Costing PDF Parser - 示例")
    print("=" * 60)
    
    parser = Parser()
    
    pdf_path = "your_document.pdf"
    
    print(f"\n1. 解析采购订单 (PO):")
    try:
        result_po = parser.parse(pdf_path, doc_type="po")
        print(f"解析结果: {json.dumps(result_po, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"PO解析失败 (示例): {e}")
    
    print(f"\n2. 解析发票 (Invoice):")
    try:
        result_invoice = parser.parse(pdf_path, doc_type="invoice")
        print(f"解析结果: {json.dumps(result_invoice, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Invoice解析失败 (示例): {e}")
    
    print(f"\n3. 解析对账单 (Statement):")
    try:
        result_statement = parser.parse(pdf_path, doc_type="statement")
        print(f"解析结果: {json.dumps(result_statement, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Statement解析失败 (示例): {e}")
    
    print("\n" + "=" * 60)
    print("使用方式:")
    print("  from parser import Parser")
    print("  parser = Parser()")
    print("  result = parser.parse('your_file.pdf', doc_type='po')")
    print("=" * 60)

if __name__ == "__main__":
    main()
