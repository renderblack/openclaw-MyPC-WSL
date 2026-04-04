#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""使用 Chrome 露头模式下载磁盘分析工具"""

import requests
import time
import os

def main():
    print("=" * 50)
    print("Chrome 露头模式下载工具")
    print("=" * 50)
    
    # 检查 Chrome 是否以调试模式运行
    try:
        resp = requests.get('http://127.0.0.1:9222/json', timeout=10)
        tabs_data = resp.json()
        print("[+] 发现 {} 个 Chrome 标签页".format(len(tabs_data)))
        for i, t in enumerate(tabs_data):
            title = t.get('title', '无标题')
            url = t.get('url', '无 URL')
            if 'chrome://' not in url:
                print("    {}. {} (可用)".format(i+1, title[:30]))
            else:
                print("    {}. {} (系统页)".format(i+1, title[:30]))
    except Exception as e:
        print("[-] 无法连接到 Chrome 调试端口: {}".format(e))
        return
    
    # 选择第一个非系统标签页
    target_tab = None
    for t in tabs_data:
        url = t.get('url', '')
        if 'chrome://' not in url:
            target_tab = t
            break
    
    if not target_tab:
        # 使用第一个标签页
        target_tab = tabs_data[0]
    
    tab_id = target_tab['id']
    ws_url = target_tab['webSocketDebuggerUrl']
    
    download_url = "https://github.com/Bill2-Software/WinDirStatPortable/releases/tag/v1.1.2"
    
    print("\n[*] 正在使用标签页：{}".format(target_tab.get('title', '无标题')[:30]))
    print("[*] 正在导航到下载页面...")
    
    # 使用 WebSocket 调用 CDP
    import websocket
    import json
    
    ws = websocket.create_connection(ws_url)
    
    # 发送 Page.navigate 命令
    cmd = {
        "id": 1,
        "method": "Page.navigate",
        "params": {"url": download_url}
    }
    ws.send(json.dumps(cmd))
    
    # 等待响应
    result = ws.recv()
    print("[+] 导航命令已发送: {}".format(result[:100]))
    
    ws.close()
    
    time.sleep(5)
    
    print("\n" + "=" * 50)
    print("请在 Chrome 窗口中手动点击 Download 按钮")
    print("下载完成后告诉我，我会帮你安装")
    print("=" * 50)
    
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    print("\n[*] 默认下载目录: {}".format(download_dir))

if __name__ == "__main__":
    main()
