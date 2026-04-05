# -*- coding: utf-8 -*-
import subprocess
import os
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# 找到PDF路径
result = subprocess.run(
    ['cmd', '/c', 'dir G:\\*沪昆*合同*.pdf /s /b'],
    capture_output=True
)
output = result.stdout.decode('gbk', errors='ignore')

pdf_path = None
for line in output.split('\n'):
    if '沪昆' in line and '合同' in line and line.strip():
        pdf_path = line.strip()
        break

print(f"PDF路径: {pdf_path}")

if pdf_path and os.path.exists(pdf_path):
    # 方法1: pdfminer
    try:
        text = extract_text(pdf_path)
        if text.strip():
            print("【pdfminer 提取结果】")
            print(text[:3000])
        else:
            print("pdfminer 提取为空，可能是扫描件")
    except Exception as e:
        print(f"pdfminer错误: {e}")
    
    # 方法2: 检查PDF是否包含图片（扫描件特征）
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\n=== PDF 详细信息 ===")
            print(f"总页数: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                print(f"\n--- 第 {i+1} 页 ---")
                print(f"  宽度: {page.width}, 高度: {page.height}")
                
                # 检查是否有文字
                chars = page.chars
                print(f"  字符数: {len(chars) if chars else 0}")
                
                # 检查是否有图片
                images = page.images
                print(f"  图片数: {len(images) if images else 0}")
                
                if not chars or len(chars) < 10:
                    print(f"  ⚠️ 可能为扫描件（无文字）")
                    
    except Exception as e:
        print(f"pdfplumber详细检查错误: {e}")