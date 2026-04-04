import websocket
import json
import time
import os

# Chrome CDP WebSocket connection
ws_url = "ws://127.0.0.1:9222/devtools/page/D72FD29EF1EC04BC4977643B6E72FEC8"

try:
    print("=" * 60)
    print("步骤 1: 连接 Chrome 并导航到 gdu 下载页面")
    print("=" * 60)
    
    ws = websocket.create_connection(ws_url, timeout=10)
    print("[OK] Chrome 已连接")
    
    # Navigate to gdu Windows download directly
    download_url = "https://github.com/dundee/gdu/releases/download/v5.35.0/gdu_windows_amd64.exe.zip"
    
    print(f"正在导航到: {download_url}")
    ws.send(json.dumps({
        "id": 1,
        "method": "Page.navigate",
        "params": {"url": download_url}
    }))
    
    # Wait for navigation
    time.sleep(5)
    
    # Check if download started
    ws.send(json.dumps({
        "id": 2,
        "method": "Page.getNavigationHistory"
    }))
    
    result = ws.recv()
    print(f"导航结果：{result[:200]}...")
    
    # Wait a bit for download to start
    print("等待下载开始...")
    time.sleep(5)
    
    # Check Downloads folder
    downloads_path = "C:\\Users\\Administrator\\Downloads"
    files = os.listdir(downloads_path)
    gdu_files = [f for f in files if 'gdu' in f.lower()]
    
    print(f"\nDownloads 文件夹中的 gdu 相关文件:")
    for f in gdu_files:
        full_path = os.path.join(downloads_path, f)
        size = os.path.getsize(full_path)
        print(f"  - {f} ({size / 1024:.1f} KB)")
    
    if gdu_files:
        print("[OK] gdu 下载成功！")
    else:
        print("[!] 未检测到下载，可能需要手动确认或等待更长时间")
    
    ws.close()
    
except Exception as e:
    print(f"错误：{e}")
