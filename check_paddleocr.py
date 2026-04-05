# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import os
import shutil

# 检查模型目录
model_dir = os.path.expanduser("~/.paddleocr")
print(f"模型目录: {model_dir}")
print(f"模型目录存在: {os.path.exists(model_dir)}")

if os.path.exists(model_dir):
    print("模型目录内容:")
    for item in os.listdir(model_dir):
        print(f"  - {item}")

# 尝试下载模型
print("\n尝试使用中文简体模型...")
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, show_log=True)