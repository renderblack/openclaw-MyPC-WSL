# -*- coding: utf-8 -*-
import os
import glob

# 尝试不同的路径模式
patterns = [
    r"G:\桥梁项目\2023\*抬升*\*.pdf",
    r"G:\桥梁项目\2023\202312*\*.pdf", 
    r"G:\桥梁项目\2023\*\*.pdf",
    r"G:\**\*合同*.pdf",
]

for pattern in patterns:
    files = glob.glob(pattern, recursive=True)
    if files:
        print(f"模式: {pattern}")
        for f in files:
            print(f"  {f}")
            print(f"  大小: {os.path.getsize(f)} bytes")
        print()