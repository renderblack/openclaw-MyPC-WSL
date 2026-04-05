# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import os

# 初始化 OCR - 使用 GPU 加速
print("初始化 PaddleOCR (GPU 模式)...")
ocr = PaddleOCR(use_angle_cls=True, lang='chinese', use_gpu=True)

# PDF 文件路径
pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_result.txt"

print(f"OCR 识别文件: {pdf_path}")
print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
print()
print("开始 OCR 识别，请稍候...")
print("=" * 50)

# 执行 OCR
result = ocr.ocr(pdf_path, cls=True)

print(f"识别完成！共找到 {len(result[0]) if result and result[0] else 0} 个文本区域")
print()
print("=" * 50)
print("OCR 结果:")
print("=" * 50)

# 保存结果到文件
with open(output_file, "w", encoding="utf-8") as f:
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            confidence = line[1][1]
            print(f"{text}")
            f.write(f"{text}\n")
    else:
        print("未识别到文本")
        f.write("未识别到文本\n")

print()
print("=" * 50)
print(f"结果已保存到: {output_file}")