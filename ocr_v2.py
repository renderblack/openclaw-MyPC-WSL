# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import os

# 设置环境变量跳过模型检查
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

print("正在初始化 PaddleOCR (lang='ch')...")

# 尝试 ch 而不是 chinese_chinese
ocr = PaddleOCR(use_textline_orientation=True, lang='ch', use_gpu=True)

pdf_path = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"
output_file = r"C:\Users\Administrator\.openclaw\workspace\ocr_result.txt"

print(f"OCR 识别文件: {pdf_path}")
print(f"文件大小: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB")
print()
print("开始 OCR 识别...")
print("=" * 50)

# 执行 OCR
result = ocr.ocr(pdf_path)

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
            print(f"[置信度:{confidence:.2f}] {text}")
            f.write(f"{text}\n")
    else:
        print("未识别到文本")
        f.write("未识别到文本\n")

print()
print("=" * 50)
print(f"结果已保存到: {output_file}")