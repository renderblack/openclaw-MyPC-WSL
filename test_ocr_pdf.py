from paddleocr import PaddleOCR
import sys
import os

# 初始化 OCR (中文支持)
ocr = PaddleOCR(use_angle_cls=True, lang='chinese', use_gpu=True)

file_path = r"G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf"

print(f"文件存在: {os.path.exists(file_path)}")
print(f"开始 OCR 识别...")

# OCR 识别
result = ocr.ocr(file_path, cls=True)

# 输出结果
if result and result[0]:
    print(f"\n识别到 {len(result[0])} 个文本区域:")
    for line in result[0]:
        text = line[1][0]
        confidence = line[1][1]
        print(f"  - {text} (置信度: {confidence:.2f})")
else:
    print("未识别到文本")