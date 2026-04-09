# -*- coding: utf-8 -*-
"""
夸克网盘登录 - 完整流程
"""
import os
import sys
import json
import time
import httpx

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client.config import get_config_dir

CONFIG_DIR = get_config_dir()
LOGIN_RESULT_FILE = CONFIG_DIR / "login_result.json"
COOKIES_FILE = CONFIG_DIR / "cookies.json"

def main():
    print("="*60)
    print("夸克网盘登录检查")
    print("="*60)
    
    # Step 1: Check if we have login_result
    if not LOGIN_RESULT_FILE.exists():
        print("未找到登录结果，请先扫码登录")
        return False
        
    with open(LOGIN_RESULT_FILE, 'r', encoding='utf-8') as f:
        login_result = json.load(f)
    
    if login_result.get('status') != 2000000:
        print(f"登录状态异常: {login_result.get('status')}")
        return False
    
    service_ticket = login_result.get('data', {}).get('members', {}).get('service_ticket')
    if not service_ticket:
        print("未找到service_ticket")
        return False
    
    print(f"找到service_ticket: {service_ticket[:20]}...")
    
    # Step 2: Use service_ticket to get cookies
    print("\n正在获取Cookie...")
    
    client = httpx.Client(timeout=30.0)
    client.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    })
    
    try:
        # Call account/info to get cookies set
        response = client.get(
            'https://pan.quark.cn/account/info',
            params={'st': service_ticket, 'lw': 'scan'}
        )
        
        print(f"API响应状态: {response.status_code}")
        
        # Check cookies from response
        cookies_list = []
        for cookie in client.cookies.jar:
            if cookie.domain and 'quark' in cookie.domain.lower():
                cookies_list.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path or '/',
                    'expires': cookie.expires or -1
                })
                print(f"  Cookie: {cookie.name}={cookie.value[:20]}...")
        
        if cookies_list:
            # Save cookies.json
            with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'cookies': cookies_list,
                    'timestamp': int(time.time()),
                    'expires_at': int(time.time()) + (7 * 24 * 3600)
                }, f, ensure_ascii=False, indent=2)
            print(f"\nCookie已保存到: {COOKIES_FILE}")
            
            # Verify login works
            print("\n验证登录...")
            from quark_client import QuarkClient
            with QuarkClient() as qc:
                if qc.is_logged_in():
                    storage = qc.get_storage_info()
                    total_gb = storage['data']['total'] / (1024**3)
                    used_gb = storage['data']['used'] / (1024**3)
                    print(f"=== 登录成功！===")
                    print(f"网盘容量: {used_gb:.2f} GB / {total_gb:.2f} GB")
                    return True
                else:
                    print("登录验证失败")
                    return False
        else:
            print("未获取到任何Cookie")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
