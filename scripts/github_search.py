import urllib.request
import json

url = "https://api.github.com/search/repositories?q=disk+analyzer+windows&per_page=10"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
data = json.loads(r.read())

for i in data.get('items', [])[:8]:
    print(f"{i['full_name']} Stars:{i['stargazers_count']}")
    print(f"  {i.get('description', 'No description')[:80]}")
    print()
