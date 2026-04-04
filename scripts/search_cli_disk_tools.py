import urllib.request
import json

# Search for disk analyzers with CLI potential
queries = [
    "disk usage analyzer cli windows",
    "treemap disk analyzer open source",
    "ncdu windows port",
    "rust disk analyzer cli"
]

for query in queries:
    print(f"\n=== 搜索: {query} ===")
    url = f"https://api.github.com/search/repositories?q={query.replace(' ', '+')}&per_page=5&sort=stars"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req)
        data = json.loads(r.read())
        print(f"找到 {data.get('total_count', 0)} 个项目")
        for item in data.get('items', [])[:3]:
            print(f"\n{item['full_name']} ⭐{item['stargazers_count']}")
            print(f"描述: {item.get('description', 'N/A')[:80]}")
            print(f"语言: {item.get('language', 'N/A')} | 更新: {item.get('pushed_at', 'N/A')[:10]}")
            # Check if has CLI
            if 'cli' in item.get('description', '').lower() or 'cli' in item.get('name', '').lower():
                print("  → 有 CLI 特性!")
    except Exception as e:
        print(f"搜索失败: {e}")
