import urllib.request
import json

# Search for CLI alternatives and SpaceSniffer details
print("=== SpaceSniffer 源码分析 ===")

# Get repo content
url = "https://api.github.com/repos/redtrillix/SpaceSniffer/contents"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
contents = json.loads(r.read())

for item in contents:
    print(f"{item['type']}: {item['name']}")

print()

# Check if there's any CLI or output specification
print("=== 查找 CLI 模式或输出格式 ===")

# Search for disk usage CLI tools
url2 = "https://api.github.com/search/repositories?q=ncdu+windows+disk+usage"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
r2 = urllib.request.urlopen(req2)
data2 = json.loads(r2.read())
print(f"ncdu 相关项目: {data2.get('total_count', 0)} 个")

for item in data2.get('items', [])[:3]:
    print(f"  {item['full_name']} Stars:{item['stargazers_count']}")
    print(f"    {item.get('description', '')[:60]}")
