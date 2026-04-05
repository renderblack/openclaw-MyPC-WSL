import pdfplumber
import os

pdf_path = r'G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf'

# 获取文件信息
file_size = os.path.getsize(pdf_path) / 1024  # KB
print(f'文件大小: {file_size:.1f} KB')
print('---')

# 提取所有文本
with pdfplumber.open(pdf_path) as pdf:
    print(f'总页数: {len(pdf.pages)}')
    print('---')
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        if text:
            print(f'=== 第 {i} 页 ===')
            print(text[:2500] if len(text) > 2500 else text)
            print()