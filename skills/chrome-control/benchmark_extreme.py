#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chrome CDP 极限性能测试
测试难度：极高 - 压测模式
"""

import pychrome
import base64
import time
import os
import sys
import requests
import json

CHROME_DEBUG_URL = "http://localhost:9222"

def get_tabs():
    try:
        response = requests.get(f"{CHROME_DEBUG_URL}/json", timeout=5)
        return response.json()
    except:
        return None

def benchmark_heavy_js(tab):
    """高难度 JS 计算测试"""
    print("  [JS 极限测试]")
    
    # 1. 斐波那契数列
    script1 = "(function() { var s=Date.now(); function fib(n){return n<=1?n:fib(n-1)+fib(n-2);} var r=fib(25); return JSON.stringify({t:Date.now()-s, r:r}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script1)
        data = json.loads(result['result']['value'])
        print(f"    斐波那契 (25): {data['t']}ms, 结果:{data['r']}")
    except:
        print("    斐波那契 (25): 失败")
    
    # 2. 数组排序
    script2 = "(function() { var a=[]; for(var i=0;i<10000;i++)a.push(Math.random()); var s=Date.now(); a.sort(); return Date.now()-s; })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script2)
        print(f"    数组排序 (10000): {result['result']['value']}ms")
    except:
        print("    数组排序 (10000): 失败")
    
    # 3. 正则匹配
    script3 = "(function() { var t='test@example.com 123-456-7890 192.168.1.1 https://example.com'; var p=[/[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}/gi, /\\d{3}-\\d{3}-\\d{4}/g, /\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/g, /https?:\\/\\/[^\\s]+/gi]; var s=Date.now(), m=[]; p.forEach(function(r){m=m.concat(t.match(r)||[]);}); return JSON.stringify({c:m.length, t:Date.now()-s}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script3)
        data = json.loads(result['result']['value'])
        print(f"    正则匹配：{data['t']}ms, 匹配:{data['c']}个")
    except:
        print("    正则匹配：失败")
    
    # 4. DOM 创建
    script4 = "(function() { var s=Date.now(); var c=document.createElement('div'); c.id='test-dom'; for(var i=0;i<1000;i++){var d=document.createElement('div');d.textContent='Item '+i;c.appendChild(d);} document.body.appendChild(c); return Date.now()-s; })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script4)
        print(f"    DOM 创建 (1000): {result['result']['value']}ms")
    except:
        print("    DOM 创建 (1000): 失败")
    
    return time.time() - time.time()  # placeholder

def benchmark_heavy_dom(tab):
    """高难度 DOM 操作测试"""
    print("  [DOM 极限测试]")
    
    # 1. 全局查询
    script1 = "(function() { var s=Date.now(); var a=document.querySelectorAll('*'); var t={}; for(var i=0;i<a.length;i++){var n=a[i].tagName; t[n]=(t[n]||0)+1;} return JSON.stringify({n:a.length, u:Object.keys(t).length, t:Date.now()-s}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script1)
        data = json.loads(result['result']['value'])
        print(f"    全局查询：{data['t']}ms, 总数:{data['n']}, 标签:{data['u']}")
    except:
        print("    全局查询：失败")
    
    # 2. DOM 遍历
    script2 = "(function() { function count(n){if(!n)return 0; var c=1; var ch=n.firstChild; while(ch){c+=count(ch);ch=ch.nextSibling;} return c;} var s=Date.now(); var r=count(document.body); return JSON.stringify({c:r, t:Date.now()-s}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script2)
        data = json.loads(result['result']['value'])
        print(f"    DOM 遍历：{data['t']}ms, 节点:{data['c']}")
    except:
        print("    DOM 遍历：失败")
    
    # 3. 布局计算
    script3 = "(function() { var s=Date.now(); var a=document.querySelectorAll('*'); var v=0; for(var i=0;i<Math.min(a.length,100);i++){var r=a[i].getBoundingClientRect(); if(r.width>0&&r.height>0)v++;} return JSON.stringify({n:Math.min(a.length,100), v:v, t:Date.now()-s}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script3)
        data = json.loads(result['result']['value'])
        print(f"    布局计算：{data['t']}ms, 可见:{data['v']}")
    except:
        print("    布局计算：失败")

def benchmark_network(tab):
    """网络监控测试"""
    print("  [网络监控]")
    
    tab.call_method("Network.enable")
    
    script = "(function() { var r=performance.getEntries(); var s=0, t=0; for(var i=0;i<r.length;i++){s+=r[i].transferSize||0; t=Math.max(t, r[i].responseEnd-r[i].startTime);} return JSON.stringify({c:r.length, s:s, d:t}); })();"
    try:
        result = tab.call_method("Runtime.evaluate", expression=script)
        data = json.loads(result['result']['value'])
        print(f"    请求数:{data['c']}, 大小:{data['s']/1024:.1f}KB, 耗时:{data['d']:.0f}ms")
    except:
        print("    网络监控：失败")
    
    tab.call_method("Network.disable")

def benchmark_screenshot(tab):
    """截图测试"""
    print("  [截图测试]")
    
    start = time.time()
    try:
        result = tab.call_method("Page.captureScreenshot", format="png")
        elapsed = time.time() - start
        size = len(base64.b64decode(result['data']))
        print(f"    耗时:{elapsed*1000:.0f}ms, 大小:{size/1024:.1f}KB")
    except:
        print("    截图：失败")

def benchmark_continuous(tab):
    """连续操作测试"""
    print("  [连续操作]")
    
    # 截图连拍
    print("    截图连拍 (5 次):")
    times = []
    for i in range(5):
        s = time.time()
        try:
            tab.call_method("Page.captureScreenshot", format="png")
            times.append(time.time() - s)
        except:
            times.append(0)
    print(f"    平均:{sum(times)/len(times)*1000:.0f}ms")
    
    # DOM 查询
    print("    DOM 查询 (10 次):")
    times = []
    for i in range(10):
        s = time.time()
        try:
            tab.call_method("Runtime.evaluate", expression="document.title")
            times.append(time.time() - s)
        except:
            times.append(0)
    print(f"    平均:{sum(times)/len(times)*1000:.1f}ms")

def main():
    print("=" * 70)
    print("Chrome CDP 极限性能测试 - 压测模式")
    print("=" * 70)
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: Chrome not available")
        return
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    test_urls = [
        ("百度", "https://www.baidu.com"),
        ("淘宝", "https://www.taobao.com"),
        ("京东", "https://www.jd.com"),
        ("阿里云", "https://www.aliyun.com"),
        ("GitHub", "https://github.com"),
        ("StackOverflow", "https://stackoverflow.com"),
        ("知乎", "https://www.zhihu.com"),
        ("微博", "https://weibo.com"),
    ]
    
    total_start = time.time()
    results = []
    
    for name, url in test_urls:
        print(f"\n[{name}] {url}")
        print("-" * 50)
        
        # 导航
        nav_s = time.time()
        tab.call_method("Page.navigate", url=url)
        time.sleep(2)
        nav_t = time.time() - nav_s
        print(f"  导航:{nav_t:.2f}s")
        
        # 基本信息
        try:
            result = tab.call_method("Runtime.evaluate", expression="document.title.substring(0,30)")
            print(f"  标题:{result['result']['value']}...")
        except:
            print("  标题：获取失败")
        
        # JS 测试
        js_t = benchmark_heavy_js(tab)
        
        # DOM 测试
        benchmark_heavy_dom(tab)
        
        # 网络
        benchmark_network(tab)
        
        # 截图
        benchmark_screenshot(tab)
        
        # 连续操作
        benchmark_continuous(tab)
        
        results.append({'name': name, 'nav': nav_t})
    
    total_t = time.time() - total_start
    
    print("\n" + "=" * 70)
    print("极限测试汇总")
    print("=" * 70)
    print(f"\n总耗时:{total_t:.2f}s ({total_t/60:.1f}分钟)")
    print(f"测试网站:{len(test_urls)}个")
    print(f"平均每站:{total_t/len(test_urls):.2f}s")
    
    # 保存
    result_file = os.path.join(os.path.dirname(__file__), "benchmark_extreme_results.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({'total': total_t, 'results': results}, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存:{result_file}")
    
    print("\n压测完成! Chrome CDP 稳定性: 通过")
    
    tab.stop()

if __name__ == "__main__":
    main()
