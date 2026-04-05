# -*- coding: utf-8 -*-
import subprocess
import os

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

if pdf_path and os.path.exists(pdf_path):
    # 读取PDF
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        print(f"总页数: {len(pdf.pages)}")
        print("=" * 60)
        
        all_text = []
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            all_text.append(f"=== 第 {i} 页 ===\n{text}\n")
        
        # 保存到文件
        output_file = r"C:\Users\Administrator\.openclaw\workspace\scripts\pdf_content.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        print(f"已保存到: {output_file}")
        
        # 打印内容
        for t in all_text:
            print(t)