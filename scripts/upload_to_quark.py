# -*- coding: utf-8 -*-
"""
夸克网盘上传 - Selenium 浏览器自动化
"""
import os
import sys
import time
import subprocess

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# File to upload
FILE_PATH = r"G:\动画组共享\动画项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁24局沪昆铁路抬升改建项目演示动画(无水印)20231205.mp4"

print("="*60)
print("夸克网盘上传 - Selenium 自动化")
print("="*60)
print(f"文件: {FILE_PATH}")
print(f"大小: {os.path.getsize(FILE_PATH) / (1024**3):.2f} GB")
print()

# Check if file exists
if not os.path.exists(FILE_PATH):
    print(f"ERROR: 文件不存在: {FILE_PATH}")
    sys.exit(1)

print("[1/5] 启动 Chrome 浏览器...")
# Use Chrome remote debugging mode
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"

# Check if Chrome is running in debug mode
try:
    import requests
    response = requests.get("http://localhost:9222/json", timeout=5)
    print("  发现 Chrome 调试模式运行中")
    use_existing = True
except:
    print("  Chrome 未在调试模式，启动新窗口...")
    use_existing = False

# Try to connect to existing Chrome or start new one
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
    print("  成功连接到 Chrome")
except Exception as e:
    print(f"  连接失败: {e}")
    print("  尝试启动新 Chrome...")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    
    # Start Chrome
    subprocess.Popen([chrome_path, "--remote-debugging-port=9222"], 
                     executable=chrome_path)
    time.sleep(3)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

print("\n[2/5] 打开夸克网盘...")
driver.get("https://pan.quark.cn")
time.sleep(5)

print("\n[3/5] 检查登录状态...")
try:
    # Check if logged in
    current_url = driver.current_url
    print(f"  当前URL: {current_url}")
    
    if "login" in current_url.lower():
        print("  未登录，请手动登录...")
        input("  登录后按回车继续...")
    else:
        print("  已登录")
except Exception as e:
    print(f"  检查登录状态失败: {e}")

print("\n[4/5] 查找上传按钮...")
# Look for upload button
try:
    # Try to find the upload button or drag-drop area
    upload_area = driver.find_element(By.CSS_SELECTOR, ".upload-area, .drop-zone, #uploadBtn, [class*='upload']")
    print(f"  找到上传区域: {upload_area}")
except:
    print("  未找到标准上传按钮，尝试点击上传...")
    
    # Try clicking on the upload button in the toolbar
    try:
        upload_btn = driver.find_element(By.XPATH, "//span[contains(text(),'上传')]")
        upload_btn.click()
        print("  点击上传按钮")
        time.sleep(2)
    except Exception as e:
        print(f"  点击上传按钮失败: {e}")

# Find file input element
print("\n[5/5] 上传文件...")
try:
    #夸克网盘的文件上传通常是一个隐藏的input元素
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    print(f"  找到文件输入框: {file_input}")
    
    # Send file path
    file_input.send_keys(FILE_PATH)
    print(f"  文件路径已发送")
    
    print("  等待上传完成...")
    # Wait for upload progress to complete
    time.sleep(10)
    
    # Check if upload completed
    print("\n  上传可能已开始，请在浏览器中确认...")
    
except Exception as e:
    print(f"  上传失败: {e}")
    print("\n  请手动操作:")
    print("  1. 在浏览器中点击'上传'按钮")
    print("  2. 选择文件:", FILE_PATH)

print("\n" + "="*60)
print("脚本执行完成，请在浏览器中确认上传状态")
print("="*60)

# Keep browser open
input("\n按回车键关闭浏览器...")
driver.quit()
