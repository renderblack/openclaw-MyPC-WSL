# -*- coding: utf-8 -*-
# 用Edge打开PDF，然后截图OCR
import subprocess
import os
import time

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

if pdf_path:
    # 用Edge打开PDF
    print("正在用Edge打开PDF...")
    subprocess.Popen(['msedge', pdf_path])
    print("请在Edge中打开PDF后告诉我，我来截图OCR")
    print("(或者你可以手动复制文字内容)")