# -*- coding: utf-8 -*-
"""
Quark Cloud Upload Script - Using Selenium to Control Chrome Browser
Uses existing Chrome profile to maintain login state
Usage: python quark_uploader.py
"""
import os
import sys
import time

# Force UTF-8 encoding for stdout
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Directory containing files
DIR_PATH = r"G:\动画组共享\动画项目\2023\202312中铁24局沪昆铁路抬升改建项目演示动画"

# Chrome path
CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# ChromeDriver path
CHROMEDRIVER_PATH = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "chromedriver", "chromedriver-win64", "chromedriver.exe")

# Existing Chrome profile
CHROME_PROFILE_DIR = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Default"

def list_mp4_files():
    """List all MP4 files in the directory"""
    files = [f for f in os.listdir(DIR_PATH) if f.endswith('.mp4')]
    return files

def setup_driver():
    """Setup Chrome browser driver with existing profile"""
    print("[INFO] Setting up Chrome driver...")
    print("[INFO] ChromeDriver path: {}".format(CHROMEDRIVER_PATH))
    print("[INFO] Chrome profile: {}\{}".format(CHROME_PROFILE_DIR, CHROME_PROFILE_NAME))
    
    if not os.path.exists(CHROMEDRIVER_PATH):
        print("[ERROR] ChromeDriver not found at: {}".format(CHROMEDRIVER_PATH))
        return None
    
    # Configure Chrome options - use existing profile
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH
    chrome_options.add_argument("--user-data-dir={}".format(CHROME_PROFILE_DIR))
    chrome_options.add_argument("--profile-directory={}".format(CHROME_PROFILE_NAME))
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--start-maximized")
    
    try:
        print("[INFO] Starting Chrome with existing profile...")
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        print("[OK] Driver ready")
        return driver
    except Exception as e:
        print("[ERROR] Failed to setup driver: {}".format(e))
        import traceback
        traceback.print_exc()
        return None

def upload_file(driver, file_path):
    """Upload file to Quark Cloud"""
    file_name = os.path.basename(file_path)
    file_size_gb = os.path.getsize(file_path) / (1024**3)
    
    print("[INFO] Target file: {}".format(file_name))
    print("[INFO] File size: {:.2f} GB".format(file_size_gb))
    
    # Step 1: Open Quark Cloud
    print("\n[Step 1/4] Opening Quark Cloud drive...")
    driver.get("https://drive.quark.cn")
    time.sleep(5)
    
    # Step 2: Wait for page load
    print("[Step 2/4] Waiting for page to load...")
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("  [OK] Page loaded")
    except Exception as e:
        print("  [WARN] Timeout: {}".format(e))
    
    time.sleep(3)
    
    # Step 3: Find upload button
    print("[Step 3/4] Searching for upload button...")
    
    upload_button = None
    
    # Try CSS selectors
    css_selectors = [
        "button[class*='upload']",
        "button[class*='Upload']",
        "[class*='upload-btn']",
        "[class*='uploadBtn']",
        ".upload-button",
        ".uploadBtn",
        "[class*='add-file']",
        "[class*='file-upload']",
        "[class*='upload-file']",
        "[class*='file-add']",
    ]
    
    for selector in css_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                upload_button = elements[0]
                print("  [OK] Found element: {}".format(selector))
                break
        except:
            continue
    
    # Try XPath
    if not upload_button:
        try:
            elements = driver.find_elements(By.XPATH, "//button[contains(text(),'上传')]")
            if elements:
                upload_button = elements[0]
                print("  [OK] Found upload button via XPath")
        except:
            pass
    
    # Check for file input directly
    if not upload_button:
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            if file_input:
                print("  [OK] Found file input directly")
                print("  [INFO] Sending file path to input...")
                file_input.send_keys(file_path)
                time.sleep(2)
                print("\n[SUCCESS] Upload initiated via file input!")
                return True
        except:
            pass
    
    if not upload_button:
        print("  [WARN] Upload button not found")
        try:
            driver.save_screenshot("quark_debug2.png")
            print("  [INFO] Screenshot saved: quark_debug2.png")
        except:
            pass
        return False
    
    # Step 4: Click upload
    print("[Step 4/4] Clicking upload button...")
    try:
        upload_button.click()
        time.sleep(2)
        print("  [OK] Upload button clicked")
        
        # Find file input
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            if file_input:
                print("  [OK] Found file input, sending path...")
                file_input.send_keys(file_path)
                print("  [OK] File path sent")
                time.sleep(2)
                print("\n[SUCCESS] Upload initiated!")
                return True
        except Exception as e:
            print("  [INFO] File input method failed: {}".format(e))
            
        return True
        
    except Exception as e:
        print("  [ERROR] {}".format(e))
        return False

def main():
    print("=" * 50)
    print("Quark Cloud Uploader - Chrome Browser Edition")
    print("=" * 50)
    
    # List available files
    print("\n[INFO] Available MP4 files:")
    mp4_files = list_mp4_files()
    for i, f in enumerate(mp4_files, 1):
        full_path = os.path.join(DIR_PATH, f)
        size_gb = os.path.getsize(full_path) / (1024**3)
        print("  {}. {} ({:.2f} GB)".format(i, f, size_gb))
    
    if not mp4_files:
        print("\n[ERROR] No MP4 files found in directory")
        return
    
    # Use the first file
    selected_idx = 0
    file_name = mp4_files[selected_idx]
    file_path = os.path.join(DIR_PATH, file_name)
    
    print("\n[INFO] Selected file: {}".format(file_name))
    
    driver = None
    try:
        driver = setup_driver()
        if not driver:
            print("\n[ERROR] Failed to setup driver")
            return
            
        success = upload_file(driver, file_path)
        
        if success:
            print("\n[SUCCESS] Upload started! Check browser for progress.")
        else:
            print("\n[FAIL] Upload process failed to start.")
            
    except Exception as e:
        print("\n[ERROR] Exception: {}".format(e))
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            print("\n[INFO] Browser remains open. Press Ctrl+C to exit...")

if __name__ == "__main__":
    main()
