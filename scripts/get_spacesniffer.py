import urllib.request
import json

# Get latest release info for SpaceSniffer
url = "https://api.github.com/repos/redtrillix/SpaceSniffer/releases/latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
data = json.loads(r.read())

print(f"版本: {data.get('tag_name', 'Unknown')}")
print(f"发布名称: {data.get('name', '')}")
print()

for asset in data.get('assets', []):
    print(f"附件: {asset['name']}")
    print(f"  下载次数: {asset.get('download_count', 0)}")
    print(f"  浏览器下载: {asset.get('browser_download_url', '')}")
    print()
