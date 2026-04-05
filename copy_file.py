# -*- coding: utf-8 -*-
import shutil
import os

src = r"G:\动画组共享\动画项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁二十四局沪昆铁路施工演示动画合同.pdf"
dst = r"C:\Users\Administrator\.openclaw\workspace\合同_中铁二十四局沪昆铁路.pdf"

print(f"源文件存在: {os.path.exists(src)}")
print(f"源文件大小: {os.path.getsize(src) / 1024 / 1024:.2f} MB")

if os.path.exists(src):
    shutil.copy2(src, dst)
    print(f"复制成功: {dst}")
    print(f"目标文件大小: {os.path.getsize(dst) / 1024 / 1024:.2f} MB")
else:
    print("源文件不存在!")