# -*- coding: utf-8 -*-
"""
夸克网盘登录 - 手动轮询版本（无倒计时线程）
"""
import os
import sys
import time

# Set UTF-8 encoding
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client.auth.api_login import APILogin
from quark_client import QuarkClient
import qrcode
import threading

def generate_qr_image(qr_url, save_path):
    """生成二维码图片"""
    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    img.add_data(qr_url)
    img.make(fit=True)
    img_qr = img.make_image(fill_color="black", back_color="white")
    img_qr.save(save_path)

def login():
    print("正在获取二维码...")
    
    try:
        # Get QR code
        login_api = APILogin(timeout=600)
        token, qr_url = login_api.get_qr_code()
        
        # Save QR to Desktop
        save_path = 'C:/Users/Administrator/Desktop/quark_login_qr.png'
        generate_qr_image(qr_url, save_path)
        print(f"二维码已保存: {save_path}")
        print("请用夸克APP扫描二维码...")
        print("等待扫码中... (每2秒检查一次)")
        
        # Poll manually without countdown thread
        start_time = time.time()
        max_wait = 300  # 5 minutes
        
        while time.time() - start_time < max_wait:
            result = login_api.check_login_status(token)
            
            if result is not None:
                if login_api._is_login_success(result):
                    print("\n扫码成功！正在保存登录信息...")
                    login_api._save_login_result(result)
                    
                    # Verify
                    try:
                        client = QuarkClient()
                        if client.is_logged_in():
                            storage = client.get_storage_info()
                            total_gb = storage['data']['total'] / (1024**3)
                            used_gb = storage['data']['used'] / (1024**3)
                            print(f"\n=== 登录成功！===")
                            print(f"网盘容量: {used_gb:.2f} GB / {total_gb:.2f} GB")
                        else:
                            print("\n登录状态验证失败")
                    except Exception as e:
                        print(f"验证登录状态时出错: {e}")
                    return True
                elif login_api._is_login_failed(result):
                    print("\n扫码失败或已过期，请重新生成二维码")
                    return False
            
            elapsed = int(time.time() - start_time)
            print(f"\r已等待 {elapsed} 秒...", end='', flush=True)
            time.sleep(2)
        
        print("\n等待超时，二维码可能已过期")
        return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = login()
    sys.exit(0 if success else 1)
