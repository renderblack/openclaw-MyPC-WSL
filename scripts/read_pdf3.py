# -*- coding: utf-8 -*-
import subprocess
import os
import sys

# 先用cmd找到PDF的准确路径
result = subprocess.run(
    ['cmd', '/c', 'dir G:\\*合同*.pdf /s /b'],
    capture_output=True
)

# 解码输出（GBK编码）
output = result.stdout.decode('gbk', errors='ignore')
print("CMD输出:")
print(output)

# 找到包含"沪昆"和"合同"的行
pdf_path = None
for line in output.split('\n'):
    if '沪昆' in line and '合同' in line and line.strip():
        pdf_path = line.strip()
        break

if not pdf_path:
    # 备用：找2023年的合同
    for line in output.split('\n'):
        if '2023' in line and '合同' in line and '.pdf' in line and line.strip():
            pdf_path = line.strip()
            break

print(f"\n找到PDF: {pdf_path}")

if pdf_path and os.path.exists(pdf_path):
    print(f"文件大小: {os.path.getsize(pdf_path)} bytes")
    
    # 读取PDF
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            print(f"总页数: {len(pdf.pages)}")
            print("=" * 60)
            
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    print(f"\n【第 {i} 页】")
                    print(text)
                    print("-" * 40)
                    
    except Exception as e:
        print(f"pdfplumber错误: {e}")
        
        # 备用方案
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(pdf_path)
            print("【PDF内容 (pdfminer)】")
            print(text)
        except Exception as e2:
            print(f"pdfminer错误: {e2}")
else:
    print("PDF文件不存在或路径解析失败")