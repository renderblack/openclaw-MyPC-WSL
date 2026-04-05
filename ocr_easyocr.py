# -*- coding: utf-8 -*-
"""
使用 EasyOCR 识别 PDF 图片
"""
import easyocr
import fitz
import os

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("EasyOCR PDF 识别")
print("=" * 60)
print()

# 1. 将 PDF 转换为图片
print("第1步: PDF 转图片 (2x zoom)...")
doc = fitz.open(pdf_path)
image_paths = []
for i in range(len(doc)):
    page = doc[i]
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(output_dir, f"page_{i+1}.png")
    pix.save(img_path)
    image_paths.append(img_path)
    print(f"  第{i+1}页: {img_path}")
doc.close()
print()

# 2. 初始化 EasyOCR
print("第2步: 初始化 EasyOCR (中文+英文)...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
print()

# 3. 逐页识别
print("第3步: OCR 识别...")
all_text = []

for i, img_path in enumerate(image_paths):
    print(f"\n  识别第 {i+1} 页...")
    result = reader.readtext(img_path)
    
    page_text = []
    for detection in result:
        text = detection[1]
        all_text.append(text)
        page_text.append(text)
    
    if page_text:
        print(f"    识别到 {len(page_text)} 个文本区域")
    else:
        print(f"    未识别到文本")

# 4. 保存结果
output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_easyocr.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print()
print("=" * 60)
print("OCR 结果预览:")
print("=" * 60)
preview = "\n".join(all_text)
print(preview[:3000])
if len(preview) > 3000:
    print(f"\n... 共 {len(preview)} 字符 ...")
print()
print(f"结果已保存到: {output_txt}")