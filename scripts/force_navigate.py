#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""强制导航到下载页面"""

import requests
import time
import json

def main():
    print("=" * 50)
    print("强制导航到下载页面")
    print("=" * 50)
    
    download_url = "https://github.com/Bill2-Software/WinDirStatPortable/releases/tag/v1.1.2"
    
    try:
        resp = requests.get('http://127.0.0.1:9222/json', timeout=10)
        tabs_data = resp.json()
        
        print("[+] 发现 {} 个标签页".format(len(tabs_data)))
        
        # 找一个可用的标签页（非 chrome:// 开头）
        target_tab = None
        for t in tabs_data:
            url = t.get('url', '')
            if 'chrome://' not in url and 'chrome-untrusted://' not in url:
                target_tab = t
                break
        
        if not target_tab and tabs_data:
            target_tab = tabs_data[0]
        
        if not target_tab:
            print("[-] 没有可用的标签页")
            return
        
        tab_id = target_tab['id']
        tab_title = target_tab.get('title', '无标题')
        print("[*] 使用标签页: {} ({})".format(tab_id[:8], tab_title[:30]))
        
        # 使用 CDP 导航
        ws_url = target_tab['webSocketDebuggerUrl']
        print("[*] WebSocket URL: {}".format(ws_url[:50] + "..."))
        
        import websocket
        ws = websocket.create_connection(ws_url)
        
        # 发送 Page.navigate
        cmd = {"id": 1, "method": "Page.navigate", "params": {"url": download_url}}
        ws.send(json.dumps(cmd))
        result = ws.recv()
        print("[+] 导航结果: {}".format(result[:100]))
        
        # 等待加载
        time.sleep(3)
        
        # 获取页面标题
        cmd = {"id": 2, "method": "Page.getTitle"}
        ws.send(json.dumps(cmd))
        result = ws.recv()
        print("[+] 页面标题: {}".format(result))
        
        ws.close()
        
        print("\n" + "=" * 50)
        print("页面已打开！请在 Chrome 中点击下载按钮")
        print("下载文件将保存到: C:\\Users\\Administrator\\Downloads")
        print("=" * 50)
        
    except Exception as e:
        print("[-] 错误: {}".format(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
