# -*- coding: utf-8 -*-
"""
使用 pypdf 直接提取 PDF 文本
"""
import fitz  # PyMuPDF for PDF to image conversion
from pypdf import PdfReader
import os

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"

print("=" * 60)
print("PDF 文本提取")
print("=" * 60)
print()

# 方法1: 直接使用 pypdf 提取嵌入文本
print("方法1: 使用 pypdf 提取嵌入文本...")
try:
    reader = PdfReader(pdf_path)
    print(f"PDF 页数: {len(reader.pages)}")
    print()
    
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text.append(f"=== 第 {i+1} 页 ===")
            all_text.append(text)
            print(f"第 {i+1} 页: 提取到 {len(text)} 字符")
        else:
            print(f"第 {i+1} 页: 无嵌入文本")
    
    if all_text:
        print()
        print("=" * 60)
        print("提取结果:")
        print("=" * 60)
        full_text = "\n\n".join(all_text)
        print(full_text[:3000])
        if len(full_text) > 3000:
            print(f"\n... 共 {len(full_text)} 字符 ...")
        
        output_txt = r"C:\Users\Administrator\.openclaw\workspace\pdf_text_extract.txt"
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(full_text)
        print()
        print(f"结果已保存到: {output_txt}")
    else:
        print()
        print("PDF 无嵌入文本，需要使用 OCR")
except Exception as e:
    print(f"pypdf 错误: {e}")

print()
print("=" * 60)
print("PDF 文件信息:")
print("=" * 60)
doc = fitz.open(pdf_path)
print(f"页数: {len(doc)}")
print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
for i in range(len(doc)):
    page = doc[i]
    print(f"第 {i+1} 页: {page.rect.width:.0f} x {page.rect.height:.0f} pt")