import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Deep dive into gdu - the most promising CLI disk analyzer
print("=" * 60)
print("深度分析: dundee/gdu (CLI 磁盘分析器)")
print("=" * 60)

# 1. Get repo details
url = "https://api.github.com/repos/dundee/gdu"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = urllib.request.urlopen(req)
repo = json.loads(r.read())

print(f"\n仓库: {repo['full_name']}")
print(f"Stars: {repo['stargazers_count']}")
print(f"语言: {repo.get('language', 'N/A')}")
print(f"问题数: {repo.get('open_issues_count', 'N/A')}")
print(f"最后提交: {repo.get('pushed_at', 'N/A')[:10]}")
print(f"描述: {repo.get('description', 'N/A')}")
print(f"\n主页: {repo.get('homepage', 'N/A')}")

# 2. Get releases to find prebuilt binaries
print("\n" + "=" * 60)
print("最新版本及下载")
print("=" * 60)
url2 = "https://api.github.com/repos/dundee/gdu/releases/latest"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
r2 = urllib.request.urlopen(req2)
release = json.loads(r2.read())

print(f"\n版本: {release.get('tag_name', 'Unknown')}")
print(f"发布名称: {release.get('name', '')}")
print(f"预编译二进制文件:")

for asset in release.get('assets', []):
    name = asset['name']
    dl_count = asset.get('download_count', 0)
    browser_url = asset.get('browser_download_url', '')
    print(f"  - {name} (下载: {dl_count})")
    # Check if Windows binary
    if 'windows' in name.lower() or 'amd64' in name.lower() or '386' in name.lower():
        print(f"    → Windows 版本! URL: {browser_url[:60]}...")

# 3. Check README for CLI usage
print("\n" + "=" * 60)
print("CLI 使用方式")
print("=" * 60)
readme_url = "https://raw.githubusercontent.com/dundee/gdu/main/README.md"
try:
    req3 = urllib.request.Request(readme_url, headers={"User-Agent": "Mozilla/5.0"})
    r3 = urllib.request.urlopen(req3)
    readme = r3.read().decode('utf-8')[:2000]
    print(readme[:1500])
except Exception as e:
    print(f"读取失败: {e}")

print("\n" + "=" * 60)
print("结论")
print("=" * 60)
print("""
✅ gdu 非常适合 CLI-Anything 方案：

优点:
1. 天生 CLI 工具，有console界面
2. 5505 stars，非常活跃
3. Go语言写的，跨平台编译简单
4. 有预编译的 Windows 二进制文件
5. 输出可以重定向到文件
6. 可以指定目录扫描

可能的自动化方式:
- 直接调用 gdu 命令，解析输出
- gdu -o output.json (如果支持JSON输出)
- 或者 gdu 2>&1 | 管道传输

下一步:
1. 下载 Windows 版本
2. 测试 CLI 参数
3. 看能否输出 JSON 格式
""")
