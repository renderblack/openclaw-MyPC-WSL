import websocket
import json
import time

ws_url = "ws://127.0.0.1:9222/devtools/page/D72FD29EF1EC04BC4977643B6E72FEC8"

try:
    print("=== 用 Chrome 搜索 CLI-Anything 仓库 ===\n")
    ws = websocket.create_connection(ws_url, timeout=10)
    
    # Navigate to GitHub search
    ws.send(json.dumps({
        "id": 1,
        "method": "Page.navigate",
        "params": {"url": "https://github.com/search?q=cli-anything+disk+analyzer&type=repositories"}
    }))
    time.sleep(3)
    
    # Get search results
    ws.send(json.dumps({
        "id": 2,
        "method": "Runtime.evaluate",
        "params": {"expression": """
            Array.from(document.querySelectorAll('.repo-name a'))
            .slice(0, 5)
            .map(a => ({
                name: a.textContent.trim(),
                href: a.href,
                stars: a.closest('.d-flex').querySelector('.color-fg-muted')?.textContent?.trim() || ''
            }))
        """}
    }))
    
    result = ws.recv()
    print(f"搜索结果:\n{result}\n")
    
    ws.close()
    print("完成！")
    
except Exception as e:
    print(f"错误：{e}")
