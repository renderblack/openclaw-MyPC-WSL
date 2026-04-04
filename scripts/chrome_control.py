#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chrome CDP 控制脚本
使用 Python + pychrome 库控制 Chrome 浏览器
"""

import pychrome
import base64
import time
import os
import sys
import requests

# Chrome 调试地址
CHROME_DEBUG_URL = "http://localhost:9222"

def get_tabs():
    """获取所有标签页"""
    try:
        response = requests.get(f"{CHROME_DEBUG_URL}/json")
        tabs = response.json()
        return tabs
    except Exception as e:
        print(f"[ERROR] Cannot get tabs: {e}")
        return []

def main():
    """主函数"""
    print("=== Chrome CDP Control Script ===")
    print(f"Debug URL: {CHROME_DEBUG_URL}")
    print()
    
    # 获取标签页
    tabs = get_tabs()
    if not tabs:
        print("[ERROR] Cannot connect to Chrome. Make sure Chrome is started with:")
        print("   chrome.exe --remote-debugging-port=9222")
        return
    
    print(f"[OK] Found {len(tabs)} tabs")
    for i, tab_info in enumerate(tabs):
        title = tab_info.get('title', 'No title')
        url = tab_info.get('url', 'No URL')
        ws_url = tab_info.get('webSocketDebuggerUrl', '')
        print(f"  {i+1}. {title}")
        print(f"     URL: {url}")
        print(f"     WS: {ws_url[:50]}...")
    print()
    
    # 选择第一个标签页
    tab_info = tabs[0]
    tab_id = tab_info['id']
    ws_url = tab_info['webSocketDebuggerUrl']
    
    print(f"[INFO] Using tab: {tab_info['title']}")
    print(f"[INFO] Tab ID: {tab_id}")
    print()
    
    # 创建浏览器和标签页
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    
    # 启动标签页
    tab.start()
    
    try:
        print("[DEMO] Performing demo operations:")
        print("-" * 40)
        
        # 1. 导航到 Bing
        print("[NAVIGATE] To: https://www.bing.com")
        tab.call_method("Page.navigate", url="https://www.bing.com")
        time.sleep(3)  # 等待页面加载
        
        # 2. 获取页面标题
        result = tab.call_method("Runtime.evaluate", expression="document.title")
        title = result['result']['value']
        print(f"[PAGE TITLE] {title}")
        
        # 3. 截图
        print("[SCREENSHOT] Capturing...")
        result = tab.call_method("Page.captureScreenshot", format="png")
        screenshot_data = base64.b64decode(result['data'])
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_path = os.path.join(script_dir, "bing_screenshot.png")
        
        with open(screenshot_path, 'wb') as f:
            f.write(screenshot_data)
        
        print(f"[OK] Screenshot saved to: {screenshot_path}")
        print(f"[OK] File size: {os.path.getsize(screenshot_path)} bytes")
        
        # 4. 获取页面内容（前 500 字符）
        result = tab.call_method("Runtime.evaluate", expression="document.documentElement.outerHTML.substring(0, 500)")
        html_preview = result['result']['value']
        print(f"[HTML PREVIEW] {html_preview[:200]}...")
        
        print("-" * 40)
        print("[OK] Demo completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] Operation failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        tab.stop()
        print("[INFO] Tab stopped.")

if __name__ == "__main__":
    main()
