import websocket
import json
import time

# Chrome CDP WebSocket connection
ws_url = "ws://127.0.0.1:9222/devtools/page/D72FD29EF1EC04BC4977643B6E72FEC8"

try:
    print("Connecting to Chrome tab...")
    ws = websocket.create_connection(ws_url, timeout=10)
    print("Connected!\n")
    
    # First check current URL
    ws.send(json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {"expression": "window.location.href"}
    }))
    result = ws.recv()
    print(f"Current URL: {result}\n")
    
    # Navigate to gdu releases page
    print("Navigating to gdu releases page...")
    ws.send(json.dumps({
        "id": 2,
        "method": "Page.navigate",
        "params": {"url": "https://github.com/dundee/gdu/releases/expanded_assets/v5.35.0"}
    }))
    time.sleep(4)
    
    # Get page title
    ws.send(json.dumps({
        "id": 3,
        "method": "Runtime.evaluate",
        "params": {"expression": "document.title"}
    }))
    result = ws.recv()
    print(f"Page title: {result}\n")
    
    # Get all download links
    ws.send(json.dumps({
        "id": 4,
        "method": "Runtime.evaluate",
        "params": {"expression": """
            JSON.stringify(
                Array.from(document.querySelectorAll('a[href*="windows"]'))
                .map(a => ({text: a.textContent.trim(), href: a.href}))
            )
        """}
    }))
    result = ws.recv()
    print(f"Download links: {result}\n")
    
    ws.close()
    print("Done!")
    
except Exception as e:
    print(f"Error: {e}")
