#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chrome Control Skill - OpenClaw 可调用的 Chrome 浏览器控制脚本
用法:
    python chrome_skill.py tabs
    python chrome_skill.py navigate <url>
    python chrome_skill.py screenshot [output_path]
    python chrome_skill.py title
    python chrome_skill.py content [length]
    python chrome_skill.py click <css_selector>
    python chrome_skill.py type <css_selector> <text>
"""

import pychrome
import base64
import time
import os
import sys
import requests
import json
from urllib.parse import urlparse

# Chrome 调试地址
CHROME_DEBUG_URL = "http://localhost:9222"

def get_tabs():
    """获取所有标签页"""
    try:
        response = requests.get(f"{CHROME_DEBUG_URL}/json", timeout=5)
        return response.json()
    except Exception as e:
        print(f"ERROR: Cannot connect to Chrome: {e}")
        return None

def cmd_tabs():
    """列出所有标签页"""
    tabs = get_tabs()
    if not tabs:
        print("No tabs found or Chrome not running in debug mode")
        return
    
    print(f"Found {len(tabs)} tabs:")
    for i, tab in enumerate(tabs):
        title = tab.get('title', 'No title')
        url = tab.get('url', 'No URL')
        print(f"  {i+1}. {title}")
        print(f"     {url}")
        print()

def cmd_navigate(url):
    """导航到指定 URL"""
    if not url:
        print("ERROR: URL is required")
        return
    
    # 验证 URL
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    
    print(f"Navigating to: {url}")
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: Chrome not available")
        return
    
    # 使用第一个标签页导航
    tab_info = tabs[0]
    ws_url = tab_info['webSocketDebuggerUrl']
    
    # 创建标签页连接
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        # 导航
        tab.call_method("Page.navigate", url=url)
        print(f"SUCCESS: Navigating to {url}")
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取新标题
        result = tab.call_method("Runtime.evaluate", expression="document.title")
        print(f"Page title: {result['result']['value']}")
    except Exception as e:
        print(f"ERROR: Navigation failed: {e}")
    finally:
        tab.stop()

def cmd_screenshot(output_path=None):
    """截取页面截图"""
    if not output_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "screenshot.png")
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: No tabs available")
        return
    
    tab_info = tabs[0]
    
    # 创建浏览器连接
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        print(f"Capturing screenshot from: {tab_info.get('title', 'New Tab')}")
        
        # 截图
        result = tab.call_method("Page.captureScreenshot", format="png")
        screenshot_data = base64.b64decode(result['data'])
        
        with open(output_path, 'wb') as f:
            f.write(screenshot_data)
        
        print(f"SUCCESS: Screenshot saved to {output_path}")
        print(f"Size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"ERROR: Screenshot failed: {e}")
    finally:
        tab.stop()

def cmd_title():
    """获取页面标题"""
    tabs = get_tabs()
    if not tabs:
        print("ERROR: No tabs available")
        return
    
    tab_info = tabs[0]
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        result = tab.call_method("Runtime.evaluate", expression="document.title")
        title = result['result']['value']
        print(f"TITLE: {title}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        tab.stop()

def cmd_content(length=1000):
    """获取页面 HTML 内容"""
    tabs = get_tabs()
    if not tabs:
        print("ERROR: No tabs available")
        return
    
    tab_info = tabs[0]
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        script = f"document.documentElement.outerHTML.substring(0, {length})"
        result = tab.call_method("Runtime.evaluate", expression=script)
        content = result['result']['value']
        print(content)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        tab.stop()

def cmd_click(selector):
    """点击元素"""
    if not selector:
        print("ERROR: CSS selector is required")
        return
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: No tabs available")
        return
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        script = f"""
        (function() {{
            var elem = document.querySelector('{selector}');
            if (elem) {{
                elem.click();
                return 'CLICKED: ' + elem.tagName;
            }}
            return 'NOT FOUND';
        }})();
        """
        result = tab.call_method("Runtime.evaluate", expression=script)
        print(result['result']['value'])
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        tab.stop()

def cmd_type(selector, text):
    """向输入框填写文本"""
    if not selector or not text:
        print("ERROR: Both selector and text are required")
        return
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: No tabs available")
        return
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    try:
        # 先聚焦元素并清空
        focus_script = f"""
        (function() {{
            var elem = document.querySelector('{selector}');
            if (elem) {{
                elem.focus();
                elem.value = '';
                return 'READY';
            }}
            return 'NOT FOUND';
        }})();
        """
        result = tab.call_method("Runtime.evaluate", expression=focus_script)
        print(result['result']['value'])
        
        if result['result']['value'] == 'READY':
            # 输入文本
            for char in text:
                tab.call_method("Input.dispatchKeyEvent", type="keyDown", text=char)
                tab.call_method("Input.dispatchKeyEvent", type="keyUp", text=char)
                time.sleep(0.01)
            print(f"TYPED: {text}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        tab.stop()

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  tabs                       - List all tabs")
        print("  navigate <url>              - Navigate to URL")
        print("  screenshot [path]          - Take screenshot")
        print("  title                      - Get page title")
        print("  content [length]           - Get page HTML")
        print("  click <selector>           - Click element")
        print("  type <selector> <text>     - Type into element")
        return
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if command == "tabs":
        cmd_tabs()
    elif command == "navigate":
        cmd_navigate(args[0] if args else None)
    elif command == "screenshot":
        cmd_screenshot(args[0] if args else None)
    elif command == "title":
        cmd_title()
    elif command == "content":
        length = int(args[0]) if args else 1000
        cmd_content(length)
    elif command == "click":
        cmd_click(args[0] if args else None)
    elif command == "type":
        if len(args) >= 2:
            cmd_type(args[0], args[1])
        else:
            print("ERROR: type requires <selector> and <text>")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
