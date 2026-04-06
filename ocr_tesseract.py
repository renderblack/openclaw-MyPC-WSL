# -*- coding: utf-8 -*-
"""
使用 Tesseract OCR 识别 PDF 图片
Tesseract 5.5.0 + chi_sim 语言包
"""
import fitz
import pytesseract
from PIL import Image
import os

# 配置 Tesseract 路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("Tesseract OCR PDF 识别")
print("=" * 60)
print()

# 1. 将 PDF 转换为图片
print("第1步: 将 PDF 转换为图片...")
doc = fitz.open(pdf_path)
print(f"PDF 共 {len(doc)} 页")

image_paths = []
for page_num in range(len(doc)):
    page = doc[page_num]
    mat = fitz.Matrix(2, 2)  # 2x scale for better OCR
    pix = page.get_pixmap(matrix=mat)
    image_path = os.path.join(output_dir, f"page_{page_num+1}.png")
    pix.save(image_path)
    image_paths.append(image_path)
    print(f"  第 {page_num+1} 页已保存")

doc.close()
print()

# 2. 使用 Tesseract OCR 识别
print("第2步: OCR 识别...")
print(f"语言: eng+chi_sim")
print()

all_results = []
for i, img_path in enumerate(image_paths):
    print(f"  识别第 {i+1} 页...", end="", flush=True)
    
    # 读取图片
    img = Image.open(img_path)
    
    # Tesseract OCR - 使用英文+中文
    text = pytesseract.image_to_string(
        img,
        lang='eng+chi_sim',
        config='--psm 6'
    )
    
    if text.strip():
        all_results.append(f"=== 第 {i+1} 页 ===")
        all_results.append(text.strip())
        print(f" 识别到 {len(text)} 字符")
    else:
        print("  未识别到文本")

# 3. 保存结果
print()
print("=" * 60)
print("OCR 结果:")
print("=" * 60)

full_text = "\n\n".join(all_results)
print(full_text)

output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_tesseract.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write(full_text)

print()
print("=" * 60)
print(f"结果已保存到: {output_txt}")
print(f"总字符数: {len(full_text)}")