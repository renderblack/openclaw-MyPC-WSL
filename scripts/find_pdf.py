# -*- coding: utf-8 -*-
import subprocess
import os

# 查找PDF文件
result = subprocess.run(
    ['powershell', '-Command', 
     "Get-ChildItem -Path G:\\ -Recurse -ErrorAction SilentlyContinue | Where-Object {$_.Name -like '*沪昆铁路施工演示动画合同*'} | Select-Object -ExpandProperty FullName"],
    capture_output=True, text=True, encoding='utf-8'
)

print("PowerShell output:")
print(result.stdout)
print(result.stderr)

# 尝试直接访问
possible_paths = [
    r"G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf",
    r"G:\桥梁项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf",
]

for p in possible_paths:
    if os.path.exists(p):
        print(f"\n找到文件: {p}")
        print(f"文件大小: {os.path.getsize(p)} bytes")