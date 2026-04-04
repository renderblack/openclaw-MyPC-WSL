import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Search PyPI for disk analyzer tools
print("=== 搜索 PyPI 磁盘分析工具 ===\n")

# Try to access PyPI JSON API
pypi_urls = [
    "https://pypi.org/pypi/qd/json",
    "https://pypi.org/pypi/ncdu/json",
    "https://pypi.org/pypi/disk_analyzer/json",
    "https://pypi.org/pypi/duc/json",
]

for pypi_url in pypi_urls:
    pkg_name = pypi_url.split("/pypi/")[1].split("/")[0]
    req = urllib.request.Request(pypi_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=10)
        data = json.loads(r.read())
        info = data.get('info', {})
        print(f"✅ {info.get('name', pkg_name)}")
        print(f"   版本: {info.get('version', 'N/A')}")
        print(f"   描述: {info.get('summary', 'N/A')[:80]}")
        print()
    except Exception as e:
        print(f"❌ {pkg_name}: {str(e)[:50]}")
        print()

# Also check what CLI tools we have available
print("\n=== 检查系统已有的磁盘工具 ===\n")
import subprocess

tools = ["df", "dir", "Get-PSDrive", "wmic"]
for tool in tools:
    try:
        result = subprocess.run(
            tool.split() if " " not in tool else ["powershell", "-Command", tool],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"✅ {tool} 可用")
    except:
        print(f"❌ {tool} 不可用")
