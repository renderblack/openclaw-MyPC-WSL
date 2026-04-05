# -*- coding: utf-8 -*-
# 从PDF提取图片
import subprocess
import os

# 找到PDF
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

print(f"PDF: {pdf_path}")

# 用pdf2image提取图片
try:
    from pdf2image import convert_from_path
    
    # 需要安装poppler
    images = convert_from_path(pdf_path)
    print(f"提取到 {len(images)} 页")
    
    # 保存图片
    output_dir = r"C:\Users\Administrator\.openclaw\workspace\scripts\pdf_images"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, img in enumerate(images):
        img.save(f"{output_dir}\\page_{i+1}.png", "PNG")
        print(f"保存: page_{i+1}.png")
        
except Exception as e:
    print(f"pdf2image错误: {e}")
    print("需要安装 poppler")