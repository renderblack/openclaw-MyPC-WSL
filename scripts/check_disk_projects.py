import urllib.request
import json

# Known disk analyzer projects to investigate
projects = [
    (" Analyzer", "ncdu/ncdu", "NCurses Disk Usage - classic CLI analyzer"),
    ("", "BrettCleary/Spearmint", "Simple CLI disk analyzer in Python"),
    ("", "bytesssocker/ncdu-windows", "NCurses Disk Usage for Windows"),
    ("", "gnualmalki/udu", "Ultra fast disk usage analyzer"),
    ("", "dundee/gdu", "Fast CLI disk utility written in Go"),
    ("", "OneMoreHeroic/rdisk", "Rust disk analyzer with treemap"),
    ("", "iprt/types.h", ""),  # placeholder to test
]

# Fix encoding issue
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=== 磁盘分析开源项目 CLI 能力调查 ===\n")

for name, repo, desc in projects[:6]:
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        r = urllib.request.urlopen(req, timeout=10)
        data = json.loads(r.read())
        
        has_cli = False
        # Check for CLI indicators
        desc_lower = (data.get('description', '') + ' ' + desc).lower()
        if 'cli' in desc_lower or 'command' in desc_lower or 'terminal' in desc_lower:
            has_cli = True
        
        stars = data.get('stargazers_count', 0)
        lang = data.get('language', 'N/A')
        topics = data.get('topics', [])
        
        cli_mark = "[CLI]" if has_cli else "[GUI]"
        print(f"{cli_mark} {data.get('full_name', repo)} Stars:{stars}")
        print(f"     语言: {lang} | Topic: {', '.join(topics[:3]) if topics else 'None'}")
        print(f"     描述: {data.get('description', desc or 'N/A')[:70]}")
        print()
    except Exception as e:
        print(f"  获取失败: {repo} - {e}\n")
