import urllib.request
import os

# Download gdu Windows binary
url = "https://github.com/dundee/gdu/releases/download/v5.35.0/gdu_windows_amd64.exe.zip"
output_path = "C:\\Users\\Administrator\\Downloads\\gdu_windows_amd64.exe.zip"

proxy = urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
})
opener = urllib.request.build_opener(proxy)

req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/octet-stream"
})

print(f"Downloading: {url}")
print(f"To: {output_path}")

try:
    response = opener.open(req)
    with open(output_path, 'wb') as f:
        f.write(response.read())
    size = os.path.getsize(output_path)
    print(f"Downloaded! Size: {size / 1024:.1f} KB")
except Exception as e:
    print(f"Download failed: {e}")
