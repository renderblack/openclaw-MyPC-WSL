# -*- coding: utf-8 -*-
import os
os.system('chcp 65001 > nul')

from quark_client import QuarkClient

print("开始登录流程...")
with QuarkClient() as client:
    if not client.is_logged_in():
        print("需要登录，正在启动扫码登录...")
        client.login()
    else:
        print("已经登录成功！")
    
    # 获取存储信息
    storage = client.get_storage_info()
    total_gb = storage['data']['total'] / (1024**3)
    used_gb = storage['data']['used'] / (1024**3)
    print(f"网盘容量: {used_gb:.2f} GB / {total_gb:.2f} GB")
