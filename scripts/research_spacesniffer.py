import urllib.request
import json

# Get SpaceSniffer repo content
url = "https://api.github.com/repos/redtrillix/SpaceSniffer/contents"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
contents = json.loads(r.read())

print("=== SpaceSniffer 仓库结构 ===")
for item in contents:
    print(f"{item['type']:5} {item['name']}")

# Check if there's a CLI or config file
print("\n=== 检查是否有 CLI 参数或配置文件 ===")
# Search for command line args in README
readme_url = "https://api.github.com/repos/redtrillix/SpaceSniffer/contents/README.md"
try:
    r_readme = urllib.request.urlopen(readme_url)
    readme_data = json.loads(r_readme.read())
    # Decode base64 content
    import base64
    content = base64.b64decode(readme_data['content']).decode('utf-8')
    print("README 内容摘要:")
    for line in content.split('\n')[:15]:
        if 'command' in line.lower() or 'arg' in line.lower() or 'cli' in line.lower():
            print(f"  {line.strip()}")
except Exception as e:
    print(f"无法读取 README: {e}")

# Search for CLI disk analyzers as alternatives
print("\n=== 寻找 CLI 替代方案 ===")
url2 = "https://api.github.com/search/repositories?q=cli+disk+usage+analyzer+windows&per_page=5"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
r2 = urllib.request.urlopen(req2)
data2 = json.loads(r2.read())
for item in data2.get('items', [])[:3]:
    print(f"{item['full_name']} Stars:{item['stargazers_count']}")
    print(f"  {item.get('description', '')[:70]}")
