#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 Chrome 当前页面状态"""

import requests
import time

def main():
    print("=" * 50)
    print("检查 Chrome 页面状态")
    print("=" * 50)
    
    try:
        resp = requests.get('http://127.0.0.1:9222/json', timeout=10)
        tabs_data = resp.json()
        
        for i, t in enumerate(tabs_data):
            title = t.get('title', '无标题')
            url = t.get('url', '无 URL')
            print("{}. {}".format(i+1, title[:50]))
            print("   URL: {}".format(url[:60]))
            print()
        
        # 检查是否有 GitHub 页面
        for t in tabs_data:
            url = t.get('url', '')
            if 'github.com' in url:
                print("[+] 发现 GitHub 页面!")
                print("    请在 Chrome 窗口中点击下载按钮")
                return
        
        print("[-] 未发现 GitHub 页面，可能还在加载中...")
        
    except Exception as e:
        print("[-] 错误: {}".format(e))

if __name__ == "__main__":
    main()
