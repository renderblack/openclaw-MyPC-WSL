# -*- coding: utf-8 -*-
"""
夸克网盘登录脚本
使用简单登录方式，引导用户输入Cookie
"""
import os
import sys
import subprocess

# Set console encoding to UTF-8
os.system('chcp 65001 > nul 2>&1')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Try to import and run the simple login
try:
    from quark_client.auth.simple_login import SimpleLogin
    
    login_manager = SimpleLogin()
    
    # Check if already logged in
    saved = login_manager.load_saved_cookies()
    if saved:
        print("\n[OK] Found saved login session!")
        print("[OK] Cookie is still valid.")
        sys.exit(0)
    
    print("\n" + "=" * 60)
    print("Quark Pan Login - Simple Method")
    print("=" * 60)
    print("\nYou need to login to Quark Pan to upload files.")
    print("\nSteps:")
    print("1. Open https://pan.quark.cn in your browser")
    print("2. Login with your Quark account")
    print("3. Press F12 -> Application -> Cookies -> https://pan.quark.cn")
    print("4. Copy all cookies as name=value; name=value format")
    print("\nRequired cookies: __kps, __uid (at minimum)")
    print("\n" + "=" * 60)
    
    # Get cookie input from user
    cookie_input = input("\nPaste your Cookie string here: ").strip()
    
    if not cookie_input:
        print("[ERROR] Empty cookie input")
        sys.exit(1)
    
    # Validate and save
    if login_manager._validate_cookie_format(cookie_input):
        login_manager._save_cookies(cookie_input)
        print("\n[OK] Cookie saved successfully!")
        
        # Verify it works
        from quark_client import QuarkClient
        with QuarkClient() as client:
            storage = client.get_storage_info()
            total_gb = storage['data']['total'] / (1024**3)
            used_gb = storage['data']['used'] / (1024**3)
            print(f"\n[OK] Login verified!")
            print(f"     Storage: {used_gb:.2f} GB / {total_gb:.2f} GB")
    else:
        print("\n[ERROR] Cookie format invalid. Missing required fields (__kps, __uid)")
        sys.exit(1)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
