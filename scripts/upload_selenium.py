# -*- coding: utf-8 -*-
"""
夸克网盘上传 - Selenium 完整流程
"""
import os
import sys
import json
import time

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

FILE_PATH = r"G:\动画组共享\动画项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画\中铁24局沪昆铁路抬升改建项目演示动画(无水印)20231205.mp4"
FILE_NAME = "中铁24局沪昆铁路抬升改建项目演示动画(无水印)20231205.mp4"

print("="*60)
print("夸克网盘上传 - Selenium 自动化")
print("="*60)
print(f"文件: {FILE_NAME}")
print(f"大小: {os.path.getsize(FILE_PATH) / (1024**3):.2f} GB")
print()

# Check file exists
if not os.path.exists(FILE_PATH):
    print(f"ERROR: 文件不存在!")
    sys.exit(1)

# Load saved cookies from quarkpan
COOKIES_FILE = r"C:\Users\Administrator\.openclaw\workspace\config\cookies.json"
with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
    cookie_data = json.load(f)

print("[1/4] 配置 Chrome 浏览器...")
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
# Use a clean profile to avoid conflicts
chrome_options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\SeleniumTemp")

print("[2/4] 启动 Chrome...")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
wait = WebDriverWait(driver, 20)

print("[3/4] 访问夸克网盘并注入 Cookie...")
driver.get("https://pan.quark.cn")
time.sleep(2)

# Inject cookies
for cookie in cookie_data['cookies']:
    try:
        driver.add_cookie({
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain'],
            'path': cookie.get('path', '/')
        })
    except Exception as e:
        print(f"  添加 cookie {cookie['name']} 失败: {e}")

# Refresh to apply cookies
driver.get("https://pan.quark.cn")
time.sleep(5)

# Check if logged in
print("检查登录状态...")
if "login" in driver.current_url.lower():
    print("Cookie 登录失败，请在浏览器中手动登录...")
    input("登录后按回车继续...")
else:
    print("登录成功!")

print("\n[4/4] 上传文件...")
try:
    # Look for upload button
    print("查找上传按钮...")
    
    # Try different selectors for upload
    selectors = [
        "//span[contains(text(),'上传')]",
        "//button[contains(text(),'上传')]",
        "//div[contains(@class,'upload')]",
        "//span[contains(text(),'新建')]"
    ]
    
    upload_btn = None
    for selector in selectors:
        try:
            upload_btn = driver.find_element(By.XPATH, selector)
            if upload_btn:
                print(f"找到上传按钮: {selector}")
                break
        except:
            continue
    
    if upload_btn:
        upload_btn.click()
        time.sleep(2)
        
        # Look for file input
        print("查找文件输入框...")
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            print("找到文件输入框，发送文件路径...")
            file_input.send_keys(FILE_PATH)
            print("文件路径已发送!")
            print("\n请在浏览器中确认上传状态...")
        except Exception as e:
            print(f"未找到文件输入框: {e}")
            print("\n请手动操作:")
            print("1. 点击上传按钮")
            print("2. 选择文件:", FILE_PATH)
    else:
        print("未找到上传按钮，请在浏览器中手动上传")
        
except Exception as e:
    print(f"上传过程出错: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("上传任务已触发，请在浏览器中确认上传状态")
print("="*60)

input("\n按回车键关闭浏览器...")
driver.quit()
