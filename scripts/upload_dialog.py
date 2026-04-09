# -*- coding: utf-8 -*-
"""
夸克网盘上传 - 使用 pywinauto 处理文件对话框
"""
import os
import sys
import time
import subprocess

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FILE_PATH = r"G:\动画组共享\动画项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁24局沪昆铁路抬升改建项目演示动画(无水印)20231205.mp4"

print("="*60)
print("夸克网盘上传 - 文件对话框自动化")
print("="*60)
print(f"文件: {FILE_PATH}")
print(f"大小: {os.path.getsize(FILE_PATH) / (1024**3):.2f} GB")
print()

if not os.path.exists(FILE_PATH):
    print(f"ERROR: 文件不存在!")
    sys.exit(1)

print("[提示]")
print("请在夸克网盘网页版中:")
print("1. 点击右上角'上传'按钮")
print("2. 选择'上传文件'")
print("3. 当文件对话框打开时，立即告诉我")
print()
input("准备好后按回车键继续...")

print("\n等待文件对话框出现...")

try:
    from pywinauto import Application
    
    # Wait for file dialog to appear (max 30 seconds)
    app = None
    for i in range(30):
        try:
            app = Application(backend="win32").connect(title_re=".*打开.*|.*Open.*")
            print("检测到文件对话框!")
            break
        except:
            time.sleep(1)
            print(f"等待中... ({i+1}/30)")
    
    if app:
        # Get the dialog
        dialog = app.window(title_re=".*打开.*|.*Open.*")
        
        # Find the file name input field and type the path
        print("\n输入文件路径...")
        
        # Type the full path
        dialog.type_keys(FILE_PATH)
        time.sleep(0.5)
        
        # Press Enter to confirm
        print("按回车键...")
        dialog.type_keys("{ENTER}")
        
        print("\n文件选择完成!")
        print("请在浏览器中确认上传状态...")
    else:
        print("未检测到文件对话框，超时退出")
        
except ImportError as e:
    print(f"pywinauto 导入失败: {e}")
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
