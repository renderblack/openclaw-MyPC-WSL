# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import os
import shutil

# 设置环境变量跳过模型检查
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

# 检查模型目录
model_dir = os.path.expanduser("~/.paddleocr")
det_model_dir = os.path.join(model_dir, "2.6.2", "det")
rec_model_dir = os.path.join(model_dir, "2.6.2", "rec")
cls_model_dir = os.path.join(model_dir, "2.6.2", "cls")

print(f"模型目录: {model_dir}")
print(f"检测模型目录存在: {os.path.exists(det_model_dir)}")
print(f"识别模型目录存在: {os.path.exists(rec_model_dir)}")
print(f"分类模型目录存在: {os.path.exists(cls_model_dir)}")

if os.path.exists(model_dir):
    print("\n模型目录内容:")
    for root, dirs, files in os.walk(model_dir):
        level = root.replace(model_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:
            print(f'{subindent}{file}')
        if len(files) > 5:
            print(f'{subindent}... and {len(files) - 5} more files')