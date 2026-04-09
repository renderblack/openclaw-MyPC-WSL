# -*- coding: utf-8 -*-
"""
Combined Status Check for Telegram - Chinese Version
"""
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import os
import re
import time
import subprocess
import json
import urllib.request
import urllib.parse

# Telegram config
TELEGRAM_TOKEN = "8717931087:AAERcQmiIpkMB0VcpHVMfjKEyhPa7fYq0_M"
CHAT_ID = "1022202630"
PROXY = "http://127.0.0.1:7890"

def run_ps(script):
    """Run PowerShell script and return output"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except:
        return "N/A"

def get_gateway_status():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:18789", timeout=3)
        return "ON" if req.status == 200 else "OFF"
    except:
        return "OFF"

def get_disk_usage():
    # Get disk usage percentage and free space
    ps = """
    $d = Get-PSDrive -Name C
    $pct = [math]::Round($d.Used / ($d.Used + $d.Free) * 100, 1)
    $free = [math]::Round($d.Free / 1GB, 1)
    Write-Output "$pct% ($free GB free)"
    """
    result = run_ps(ps)
    return result if result else "N/A"

def get_memory():
    ps = """
    $os = Get-CimInstance Win32_OperatingSystem
    $free = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
    $total = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
    Write-Output "$free GB free / $total GB"
    """
    result = run_ps(ps)
    return result if result else "N/A"

def get_cpu():
    ps = """
    $cpu = Get-CimInstance Win32_Processor
    $load = $cpu.LoadPercentage
    if ($load -is [array]) { $load = $load[0] }
    Write-Output "$load%"
    """
    result = run_ps(ps)
    return result if result else "N/A"

def get_uptime():
    ps = """
    $os = Get-CimInstance Win32_OperatingSystem
    $span = (Get-Date) - $os.LastBootUpTime
    Write-Output "$($span.Days)天 $($span.Hours)小时"
    """
    result = run_ps(ps)
    return result if result else "N/A"

def get_weather():
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
        opener = urllib.request.build_opener(proxy_handler)
        url = "https://wttr.in/Jiaxing?format=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = opener.open(req, timeout=10)
        return response.read().decode('utf-8').strip()
    except:
        return "N/A"

def search_news():
    keywords = ["桥梁事故", "施工坍塌", "工程事故", "脚手架倒塌", "塔吊事故"]
    all_results = []
    
    for keyword in keywords:
        try:
            encoded = urllib.parse.quote(keyword)
            url = f"https://www.baidu.com/s?wd={encoded}&rn=5"
            
            proxy_handler = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
            opener = urllib.request.build_opener(proxy_handler)
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response = opener.open(req, timeout=15)
            html = response.read().decode('utf-8', errors='ignore')
            
            pattern = r'<h3 class="c-title t"><a[^>]*href="[^"]*"[^>]*aria-label="([^"]*)"'
            matches = re.findall(pattern, html)
            
            for title in matches[:3]:
                if title and len(title) > 5:
                    all_results.append(title.strip())
            
            time.sleep(0.3)
        except:
            continue
    
    seen = set()
    unique = []
    for r in all_results:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    
    return unique[:5]

def get_processes():
    ps = "(Get-Process).Count"
    result = run_ps(ps)
    return result if result else "N/A"

def send_telegram(message):
    for attempt in range(3):
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})
            opener = urllib.request.build_opener(proxy_handler)
            
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            req = urllib.request.Request(url, 
                                        data=json.dumps(data).encode('utf-8'),
                                        headers={'Content-Type': 'application/json'})
            response = opener.open(req, timeout=15)
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('ok'):
                print(f"[{time.strftime('%Y-%m-%d %H:%M')}] Telegram sent OK")
                return True
            else:
                print(f"Telegram failed: {result}")
        except Exception as e:
            print(f"Telegram attempt {attempt+1} error: {e}")
            time.sleep(2)
    return False

def main():
    print("Gathering info...")
    
    gateway = get_gateway_status()
    disk = get_disk_usage()
    memory = get_memory()
    cpu = get_cpu()
    uptime = get_uptime()
    weather = get_weather()
    news = search_news()
    processes = get_processes()
    
    print(f"Gateway: {gateway}")
    print(f"Disk: {disk}")
    print(f"Memory: {memory}")
    print(f"CPU: {cpu}")
    print(f"Uptime: {uptime}")
    print(f"Weather: {weather}")
    print(f"News: {len(news)} items")
    
    # Build message
    lines = []
    lines.append("=" * 40)
    lines.append("皮皮虾 定时推送")
    lines.append("=" * 40)
    lines.append("")
    
    lines.append("【系统状态】")
    lines.append(f"  网关: {gateway}")
    lines.append(f"  磁盘: {disk}")
    lines.append(f"  内存: {memory}")
    lines.append(f"  CPU: {cpu}")
    lines.append(f"  进程: {processes}")
    lines.append(f"  运行: {uptime}")
    lines.append("")
    
    lines.append("【天气预报】")
    lines.append(f"  {weather}")
    lines.append("")
    
    lines.append(f"【工程安全新闻】 ({len(news)}条)")
    if news:
        for i, item in enumerate(news, 1):
            title = item[:50] + "..." if len(item) > 50 else item
            lines.append(f"  {i}. {title}")
    else:
        lines.append("  暂无新闻")
    lines.append("")
    
    lines.append("=" * 40)
    lines.append(f"推送: {time.strftime('%Y-%m-%d %H:%M')}")
    
    message = "\n".join(lines)
    print("\n" + message + "\n")
    
    # Send to Telegram
    send_telegram(message)

if __name__ == "__main__":
    main()
