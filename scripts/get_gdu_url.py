import urllib.request
import os
import json

# Get exact download URL for Windows binary
url = "https://api.github.com/repos/dundee/gdu/releases/latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
release = json.loads(r.read())

windows_url = None
for asset in release.get('assets', []):
    if 'windows_amd64.exe.zip' in asset['name']:
        windows_url = asset['browser_download_url']
        print(f"Found: {asset['name']}")
        print(f"URL: {windows_url}")
        break

if windows_url:
    print("\nTrying direct download...")
    output_path = "C:\\Users\\Administrator\\Downloads\\gdu.exe.zip"
    
    proxy = urllib.request.ProxyHandler({
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    })
    opener = urllib.request.build_opener(proxy)
    
    req2 = urllib.request.Request(windows_url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/octet-stream"
    })
    
    try:
        response = opener.open(req2, timeout=30)
        with open(output_path, 'wb') as f:
            f.write(response.read())
        size = os.path.getsize(output_path)
        print(f"Downloaded! Size: {size / 1024:.1f} KB")
    except Exception as e:
        print(f"Failed: {e}")
        
        # Try without proxy
        print("\nTrying without proxy...")
        try:
            req3 = urllib.request.Request(windows_url, headers={
                "User-Agent": "Mozilla/5.0"
            })
            response = urllib.request.urlopen(req3, timeout=30)
            with open(output_path, 'wb') as f:
                f.write(response.read())
            size = os.path.getsize(output_path)
            print(f"Downloaded without proxy! Size: {size / 1024:.1f} KB")
        except Exception as e2:
            print(f"Also failed: {e2}")
