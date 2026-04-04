import urllib.request
import json

# Get Chrome debugging info via HTTP
url = "http://127.0.0.1:9222/json"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    r = urllib.request.urlopen(req, timeout=10)
    data = json.loads(r.read())
    
    print(f"Found {len(data)} Chrome tabs/pages:\n")
    for tab in data:
        print(f"ID: {tab.get('id', 'N/A')}")
        print(f"  Type: {tab.get('type', 'N/A')}")
        print(f"  Title: {tab.get('title', 'N/A')}")
        print(f"  URL: {tab.get('url', 'N/A')}")
        print(f"  WebSocket URL: {tab.get('webSocketDebuggerUrl', 'N/A')}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
