# -*- coding: utf-8 -*-
"""
夸克网盘登录 - 无阻塞版本
"""
import os
import sys
import time
import threading

# Set UTF-8 encoding
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from quark_client.auth.api_login import APILogin
from quark_client import QuarkClient
import qrcode

def generate_qr_image(token, qr_url, save_path):
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

def login_with_qr():
    print("正在获取二维码...")
    
    try:
        # Get QR code
        login_api = APILogin(timeout=600)  # 10 minutes timeout
        token, qr_url = login_api.get_qr_code()
        
        print("QR URL:", qr_url[:50], "...")
        
        # Save QR to Desktop
        save_path = 'C:/Users/Administrator/Desktop/quark_login_qr.png'
        generate_qr_image(token, qr_url, save_path)
        print(f"二维码已保存: {save_path}")
        print("请用夸克APP扫描二维码...")
        
        # Start polling in background
        result = login_api.poll_scan_result(token)
        
        if result:
            print("\n=== 扫码成功！===")
            # Save cookies
            login_api.save_auth_data(result)
            print("登录凭证已保存!")
            
            # Verify
            client = QuarkClient()
            if client.is_logged_in():
                storage = client.get_storage_info()
                total_gb = storage['data']['total'] / (1024**3)
                used_gb = storage['data']['used'] / (1024**3)
                print(f"\n登录验证成功!")
                print(f"网盘容量: {used_gb:.2f} GB / {total_gb:.2f} GB")
            return True
        else:
            print("\n扫码超时或失败，请重试")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    login_with_qr()
