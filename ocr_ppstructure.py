# -*- coding: utf-8 -*-
"""
使用 PaddleOCR PP-OCRv4 pipeline 直接识别 PDF 图片
"""
import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

from paddleocr import PPStructure
import fitz
import time

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_dir = r"C:\Users\Administrator\.openclaw\workspace\pdf_images"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("PaddleOCR PP-STRUCTURE 识别")
print("=" * 60)
print()

# 1. 将 PDF 转换为图片
print("第1步: PDF 转图片...")
doc = fitz.open(pdf_path)
image_paths = []
for i in range(len(doc)):
    page = doc[i]
    mat = fitz.Matrix(2, 2)  # 2x scale for better OCR
    pix = page.get_pixmap(matrix=mat)
    img_path = os.path.join(output_dir, f"page_{i+1}.png")
    pix.save(img_path)
    image_paths.append(img_path)
    print(f"  第{i+1}页: {img_path}")
doc.close()
print()

# 2. 使用 PaddleOCR PP-STRUCTURE
print("第2步: 初始化 PP-STRUCTURE...")
table_engine = PPStructure(table=False, ocr=True, show_log=True)
print()

# 3. 逐页识别
print("第3步: OCR 识别...")
all_results = []

for i, img_path in enumerate(image_paths):
    print(f"\n  识别第 {i+1} 页...")
    start = time.time()
    result = table_engine(img_path)
    elapsed = time.time() - start
    print(f"  完成，耗时 {elapsed:.1f}s")
    all_results.extend(result)

# 4. 提取文本
print("\n第4步: 提取文本...")
full_text = []
for res in all_results:
    if 'res' in res:
        for line in res['res']:
            if 'text' in line:
                full_text.append(line['text'])

# 5. 保存结果
output_txt = r"C:\Users\Administrator\.openclaw\workspace\ocr_result_paddle.txt"
with open(output_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(full_text))

print()
print("=" * 60)
print("OCR 结果预览:")
print("=" * 60)
print("\n".join(full_text[:50]))
if len(full_text) > 50:
    print(f"\n... 共 {len(full_text)} 行 ...")
print()
print(f"结果已保存到: {output_txt}")