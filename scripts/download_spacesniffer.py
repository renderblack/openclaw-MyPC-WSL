import urllib.request
import urllib.error
import os

url = "https://github.com/redtrillix/SpaceSniffer/releases/download/v1.3.0.2/spacesniffer_1_3_0_2.zip"
output_path = "C:\\Users\\Administrator\\Downloads\\spacesniffer_1_3_0_2.zip"

proxy = urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
})
opener = urllib.request.build_opener(proxy)

req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/octet-stream"
})

print(f"正在下载: {url}")
print(f"保存到: {output_path}")

try:
    response = opener.open(req)
    with open(output_path, 'wb') as f:
        f.write(response.read())
    size = os.path.getsize(output_path)
    print(f"下载完成! 大小: {size / 1024:.1f} KB")
except Exception as e:
    print(f"下载失败: {e}")
