import websocket
import json

# Connect to Chrome debugging port
ws_url = "ws://127.0.0.1:9222/devtools/page"

try:
    ws = websocket.create_connection("ws://127.0.0.1:9222/devtools/browser", timeout=10)
    print("Connected to Chrome!")
    
    # Get list of tabs
    ws.send(json.dumps({"id": 1, "method": "targets.getTargets"}))
    result = ws.recv()
    print(f"Targets: {result}")
    
    ws.close()
except Exception as e:
    print(f"Error: {e}")
