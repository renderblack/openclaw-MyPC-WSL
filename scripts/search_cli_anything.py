import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Search for CLI-Anything related repos
print("Searching GitHub for CLI-Anything repos...")

url = "https://api.github.com/search/repositories?q=cli-anything+OR+claw-cli-anything&per_page=10"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    r = urllib.request.urlopen(req, timeout=15)
    data = json.loads(r.read())
    total = data.get('total_count', 0)
    print(f"Found {total} repos\n")
    
    for item in data.get('items', []):
        stars = item.get('stargazers_count', 0)
        name = item.get('full_name', '')
        desc = item.get('description', 'N/A') or 'N/A'
        html_url = item.get('html_url', '')
        
        # Remove emoji to avoid encoding issues
        desc_clean = desc.encode('utf-8', errors='replace').decode('utf-8')
        
        print(f"[{stars}] {name}")
        print(f"    {desc_clean[:80]}")
        print(f"    {html_url}")
        print()
except Exception as e:
    print(f"Search failed: {e}")
