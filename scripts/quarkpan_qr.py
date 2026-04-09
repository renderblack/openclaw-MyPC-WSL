# -*- coding: utf-8 -*-
"""
夸克网盘登录 - 生成二维码图片
"""
import os
os.system('chcp 65001 > nul 2>&1')

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client.auth.api_login import APILogin
import qrcode
from PIL import Image

print("正在获取二维码...")

try:
    # Get QR code URL
    login = APILogin()
    token, qr_url = login.get_qr_code()
    
    print(f"QR URL: {qr_url}")
    
    # Generate QR code image
    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    img.add_data(qr_url)
    img.make(fit=True)
    
    # Create image
    img_qr = img.make_image(fill_color="black", back_color="white")
    
    # Save to Desktop
    save_path = 'C:/Users/Administrator/Desktop/quark_login_qr.png'
    img_qr.save(save_path)
    
    print(f"二维码已保存到: {save_path}")
    print("请用夸克APP扫描二维码登录")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
