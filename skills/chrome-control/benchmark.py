#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chrome CDP 性能测试脚本
测试难度：高
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

def benchmark_navigate(url, tab):
    """测试导航性能"""
    start = time.time()
    tab.call_method("Page.navigate", url=url)
    # 等待页面加载
    time.sleep(2)
    elapsed = time.time() - start
    return elapsed

def benchmark_screenshot(tab):
    """测试截图性能"""
    start = time.time()
    result = tab.call_method("Page.captureScreenshot", format="png")
    elapsed = time.time() - start
    size = len(base64.b64decode(result['data']))
    return elapsed, size

def benchmark_js(tab, script):
    """测试 JS 执行性能"""
    start = time.time()
    result = tab.call_method("Runtime.evaluate", expression=script)
    elapsed = time.time() - start
    return elapsed, result['result']['value']

def benchmark_dom_query(tab):
    """测试 DOM 查询性能"""
    start = time.time()
    script = """
    (function() {
        var links = document.querySelectorAll('a');
        var imgs = document.querySelectorAll('img');
        var forms = document.querySelectorAll('form');
        return JSON.stringify({
            links: links.length,
            images: imgs.length,
            forms: forms.length,
            title: document.title,
            readyState: document.readyState
        });
    })();
    """
    result = tab.call_method("Runtime.evaluate", expression=script)
    elapsed = time.time() - start
    return elapsed, json.loads(result['result']['value'])

def main():
    print("=" * 60)
    print("Chrome CDP 性能测试 - 高难度版")
    print("=" * 60)
    
    tabs = get_tabs()
    if not tabs:
        print("ERROR: Chrome not available")
        return
    
    browser = pychrome.Browser(url=CHROME_DEBUG_URL)
    tab = browser.new_tab()
    tab.start()
    
    # 测试网站列表
    test_urls = [
        "https://www.baidu.com",
        "https://www.taobao.com",
        "https://www.jd.com",
        "https://www.aliyun.com",
        "https://github.com",
    ]
    
    total_start = time.time()
    
    results = []
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n[{i}/5] 测试: {url}")
        print("-" * 40)
        
        # 1. 导航测试
        nav_start = time.time()
        tab.call_method("Page.navigate", url=url)
        time.sleep(2)  # 等待页面稳定
        nav_time = time.time() - nav_start
        print(f"  导航耗时: {nav_time:.2f}s")
        
        # 2. 获取页面标题
        title_start = time.time()
        result = tab.call_method("Runtime.evaluate", expression="document.title")
        title = result['result']['value']
        title_time = time.time() - title_start
        print(f"  标题获取: {title_time*1000:.1f}ms - {title[:30]}...")
        
        # 3. DOM 分析
        dom_start = time.time()
        script = """
        (function() {
            return JSON.stringify({
                links: document.querySelectorAll('a').length,
                images: document.querySelectorAll('img').length,
                scripts: document.querySelectorAll('script').length,
                title: document.title.substring(0, 50),
                url: window.location.href
            });
        })();
        """
        result = tab.call_method("Runtime.evaluate", expression=script)
        dom_time = time.time() - dom_start
        dom_info = json.loads(result['result']['value'])
        print(f"  DOM分析: {dom_time*1000:.1f}ms")
        print(f"    - 链接: {dom_info['links']}, 图片: {dom_info['images']}, 脚本: {dom_info['scripts']}")
        
        # 4. 截图测试
        screen_start = time.time()
        result = tab.call_method("Page.captureScreenshot", format="png")
        screen_time = time.time() - screen_start
        screen_size = len(base64.b64decode(result['data']))
        print(f"  截图耗时: {screen_time:.2f}s, 大小: {screen_size/1024:.1f}KB")
        
        # 5. JavaScript 计算测试
        js_start = time.time()
        script = """
        (function() {
            // 复杂计算：计算 10000 以内的质数
            var primes = [];
            for (var i = 2; i < 10000; i++) {
                var isPrime = true;
                for (var j = 2; j <= Math.sqrt(i); j++) {
                    if (i % j === 0) {
                        isPrime = false;
                        break;
                    }
                }
                if (isPrime) primes.push(i);
            }
            return primes.length;
        })();
        """
        result = tab.call_method("Runtime.evaluate", expression=script)
        js_time = time.time() - js_start
        prime_count = result['result']['value']
        print(f"  JS计算: {js_time*1000:.1f}ms (找到 {prime_count} 个质数)")
        
        # 记录结果
        results.append({
            'url': url,
            'nav': nav_time,
            'title': title_time,
            'dom': dom_time,
            'screenshot': screen_time,
            'screenshot_size': screen_size,
            'js': js_time,
            'primes': prime_count
        })
    
    # 总耗时
    total_time = time.time() - total_start
    
    # 输出汇总
    print("\n" + "=" * 60)
    print("性能测试汇总")
    print("=" * 60)
    
    print(f"\n总耗时: {total_time:.2f}s")
    print(f"平均每个网站: {total_time/len(test_urls):.2f}s")
    
    print("\n各指标平均耗时:")
    print(f"  导航: {sum(r['nav'] for r in results)/len(results):.2f}s")
    print(f"  标题: {sum(r['title'] for r in results)/len(results)*1000:.1f}ms")
    print(f"  DOM: {sum(r['dom'] for r in results)/len(results)*1000:.1f}ms")
    print(f"  截图: {sum(r['screenshot'] for r in results)/len(results):.2f}s")
    print(f"  JS计算: {sum(r['js'] for r in results)/len(results)*1000:.1f}ms")
    
    print("\n截图大小统计:")
    avg_size = sum(r['screenshot_size'] for r in results)/len(results)
    print(f"  平均: {avg_size/1024:.1f}KB")
    print(f"  最大: {max(r['screenshot_size'] for r in results)/1024:.1f}KB")
    print(f"  最小: {min(r['screenshot_size'] for r in results)/1024:.1f}KB")
    
    # 保存结果
    result_file = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_time': total_time,
            'results': results
        }, f, indent=2, ensure_ascii=False)
    print(f"\n详细结果已保存到: {result_file}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
    
    tab.stop()

if __name__ == "__main__":
    main()
