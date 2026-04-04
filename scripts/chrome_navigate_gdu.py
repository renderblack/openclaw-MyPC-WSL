import websocket
import json
import time

# Chrome CDP WebSocket connection
ws_url = "ws://127.0.0.1:9222/devtools/page/D72FD29EF1EC04BC4977643B6E72FEC8"

try:
    print("Connecting to Chrome tab...")
    ws = websocket.create_connection(ws_url, timeout=10)
    print("Connected!\n")
    
    # Navigate to gdu releases page
    cmd_id = 1
    ws.send(json.dumps({
        "id": cmd_id,
        "method": "Page.navigate",
        "params": {"url": "https://github.com/dundee/gdu/releases/latest"}
    }))
    print("Navigating to gdu releases page...")
    time.sleep(3)
    
    # Check if page loaded
    ws.send(json.dumps({"id": 2, "method": "Page.getNavigationHistory"}))
    
    ws.close()
    print("Done!")
    
except Exception as e:
    print(f"Error: {e}")
