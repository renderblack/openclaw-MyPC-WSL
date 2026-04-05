# -*- coding: utf-8 -*-
import os

# PDF路径 - 使用原始字符串
pdf_path = r"G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf"

print(f"文件存在: {os.path.exists(pdf_path)}")
print(f"文件大小: {os.path.getsize(pdf_path)} bytes")

# 尝试使用pdfplumber
try:
    import pdfplumber
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"\n总页数: {len(pdf.pages)}")
        print("=" * 50)
        
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                print(f"\n【第 {i} 页】")
                print(text)
                print("-" * 30)
                
except Exception as e:
    print(f"pdfplumber错误: {e}")
    
    # 备用方案：用pdfminer
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(pdf_path)
        print("【PDF内容 (pdfminer)】")
        print(text)
    except Exception as e2:
        print(f"pdfminer也失败: {e2}")