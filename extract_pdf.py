# -*- coding: utf-8 -*-
import pypdf
import os

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_file = r"C:\Users\Administrator\.openclaw\workspace\pdf_text.txt"

print("使用 pypdf 提取 PDF 文本...")
print(f"文件: {pdf_path}")
print(f"大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
print()

reader = pypdf.PdfReader(pdf_path)
print(f"PDF 页数: {len(reader.pages)}")
print()

text_content = []
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        text_content.append(f"--- 第 {i+1} 页 ---")
        text_content.append(text)

result = "\n".join(text_content)

print("提取的文本内容:")
print("=" * 50)
print(result[:2000])  # 打印前2000字符
print("..." if len(result) > 2000 else "")
print("=" * 50)

# 保存结果
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)

print(f"\n结果已保存到: {output_file}")