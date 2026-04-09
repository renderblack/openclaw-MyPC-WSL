# -*- coding: utf-8 -*-
"""
Engineering Safety News Search Script
Uses Baidu search and returns results as JSON for QQ display
"""
import sys
import os
import re
import time
import json
import urllib.parse
import urllib.request

def search_baidu(keyword, count=5):
    """Search Baidu and return results"""
    results = []
    
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded_keyword}&rn=10&ie=utf-8"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    proxy = 'http://127.0.0.1:7890'
    
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        
        request = urllib.request.Request(url, headers=headers)
        response = opener.open(request, timeout=15)
        html = response.read().decode('utf-8', errors='ignore')
        
        # Pattern: <h3 class="c-title t"><a ... aria-label="Title">...</a></h3>
        pattern = r'<h3 class="c-title t"><a[^>]*href="([^"]*)"[^>]*aria-label="([^"]*)"[^>]*>'
        matches = re.findall(pattern, html)
        
        for link, title in matches[:count]:
            if title and len(title) > 3:
                results.append({
                    'title': title.strip(),
                    'link': link
                })
    except Exception as e:
        print(f"[WARN] Search failed for {keyword}: {e}", file=sys.stderr)
    
    return results

def format_output(results):
    """Format results for QQ display"""
    if not results:
        return "No news found"
    
    lines = []
    lines.append("=== Engineering Safety News ===")
    lines.append(f"Time: {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    for i, r in enumerate(results, 1):
        title = r['title'][:60] + "..." if len(r['title']) > 60 else r['title']
        lines.append(f"{i}. {title}")
        lines.append(f"   {r['link']}")
    
    lines.append("")
    lines.append(f"Found {len(results)} news items")
    
    return "\n".join(lines)

def main():
    keywords = [
        "桥梁事故",
        "施工坍塌", 
        "工程事故"
    ]
    
    all_results = []
    
    for keyword in keywords:
        results = search_baidu(keyword, count=5)
        all_results.extend(results)
        time.sleep(1)
    
    # Deduplicate by title
    seen = set()
    unique_results = []
    for r in all_results:
        title = r['title']
        if title not in seen:
            seen.add(title)
            unique_results.append(r)
    
    unique_results = unique_results[:5]
    
    # Output in UTF-8
    output = format_output(unique_results)
    print(output)

if __name__ == "__main__":
    main()
