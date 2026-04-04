import urllib.request
import json

# Get SpaceSniffer repo info
url = "https://api.github.com/repos/redtrillix/SpaceSniffer"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
repo = json.loads(r.read())

print(f"仓库: {repo['full_name']}")
print(f"描述: {repo.get('description', '')}")
print(f"语言: {repo.get('language', '')}")
print(f"Stars: {repo['stargazers_count']}")
print()

# Get commits to understand recent activity
url2 = "https://api.github.com/repos/redtrillix/SpaceSniffer/commits?per_page=5"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
r2 = urllib.request.urlopen(req2)
commits = json.loads(r2.read())

print("最近提交:")
for c in commits[:3]:
    print(f"  {c['commit']['message'][:60]}")
