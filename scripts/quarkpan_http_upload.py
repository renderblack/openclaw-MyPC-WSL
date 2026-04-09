# -*- coding: utf-8 -*-
"""
夸克网盘上传 - 使用 HTTP 直传（非 OSS）
"""
import os
import sys
import json
import hashlib
import httpx
from pathlib import Path
from urllib.parse import urlencode

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 读取保存的 cookies
from quark_client.config import get_config_dir

CONFIG_DIR = get_config_dir()
COOKIES_FILE = CONFIG_DIR / "cookies.json"

with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
    cookie_data = json.load(f)

cookies = cookie_data['cookies']
cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

# 文件信息
FILE_PATH = r"G:\动画组共享\动画项目\2020\09-外部-上海机场线\06-成片\中铁二十四局集团上海机场联络线1标 项目介绍（20201223最终版修改）.mp4"
file_size = Path(FILE_PATH).stat().st_size
file_name = Path(FILE_PATH).name

print(f"文件: {file_name}")
print(f"大小: {file_size / (1024**3):.2f} GB")
print()

# 使用 drive-pc API (类似 PC 客户端)
pre_url = "https://drive-pc.quark.cn/1/clouddrive/file/upload/pre"

headers = {
    'Cookie': cookie_string,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Referer': 'https://pan.quark.cn/',
    'Origin': 'https://pan.quark.cn'
}

pre_data = {
    "ccp_hash_update": True,
    "parallel_upload": True,
    "pdir_fid": "0",
    "dir_name": "",
    "size": file_size,
    "file_name": file_name,
    "format_type": "video/mp4",
    "l_updated_at": 1775520000000,
    "l_created_at": 1775520000000
}

print("[1/5] 发起预上传请求...")
try:
    response = httpx.post(pre_url, json=pre_data, headers=headers, timeout=30)
    print(f"响应状态: {response.status_code}")
    
    if response.status_code == 200:
        pre_result = response.json()
        print(f"Status: {pre_result.get('status')}")
        
        if pre_result.get('status') == 200:
            data = pre_result.get('data', {})
            task_id = data.get('task_id', '')
            upload_id = data.get('upload_id', '')
            obj_key = data.get('obj_key', '')
            bucket = data.get('bucket', '')
            auth_info = data.get('auth_info', '')
            upload_url_returned = data.get('upload_url', '')
            
            print(f"  task_id: {task_id}")
            print(f"  bucket: {bucket}")
            print(f"  upload_url returned: {upload_url_returned}")
            
            if not task_id:
                print("ERROR: No task_id returned")
                sys.exit(1)
            
            # Step 2: 计算文件哈希
            print("\n[2/5] 计算文件哈希...")
            with open(FILE_PATH, 'rb') as f:
                content = f.read()
            sha1 = hashlib.sha1(content).hexdigest()
            print(f"  SHA1: {sha1}")
            
            # Step 3: 更新文件哈希
            print("\n[3/5] 更新文件哈希...")
            hash_url = "https://drive-pc.quark.cn/1/clouddrive/file/hash"
            hash_data = {
                "task_id": task_id,
                "content_hash": sha1,
                "hash_name": "sha1"
            }
            hash_resp = httpx.post(hash_url, json=hash_data, headers=headers, timeout=30)
            print(f"  响应状态: {hash_resp.status_code}")
            
            # Step 4: 分片上传
            print("\n[4/5] 分片上传...")
            
            # 尝试使用返回的 upload_url 而非构造的 OSS URL
            if upload_url_returned and upload_url_returned != 'http://pds.quark.cn':
                print(f"  使用返回的上传URL: {upload_url_returned}")
                upload_host = upload_url_returned
            else:
                # 使用 callback 中的 URL
                callback = data.get('callback', {})
                callback_url = callback.get('callbackUrl', '')
                print(f"  使用 callback URL: {callback_url}")
                upload_host = f"https://{callback_url}"
            
            # 分片上传
            part_size = 20 * 1024 * 1024  # 20MB
            total_parts = (file_size + part_size - 1) // part_size
            print(f"  总分片数: {total_parts}")
            
            etags = []
            with open(FILE_PATH, 'rb') as f:
                for part_num in range(1, total_parts + 1):
                    chunk = f.read(part_size)
                    chunk_size = len(chunk)
                    
                    # 尝试直接 POST 到 callback URL
                    print(f"  上传分片 {part_num}/{total_parts} ({chunk_size/(1024**2):.1f} MB)...")
                    
                    # 使用 multipart form data 上传
                    files = {'file': (f'part_{part_num}', chunk, 'video/mp4')}
                    data_multipart = {
                        'task_id': task_id,
                        'upload_id': upload_id,
                        'part_number': part_num
                    }
                    
                    try:
                        # 尝试使用 multipart 上传
                        part_resp = httpx.post(
                            f"https://{callback_url}",
                            files=files,
                            data=data_multipart,
                            headers={
                                'Cookie': cookie_string,
                                'Referer': 'https://pan.quark.cn/'
                            },
                            timeout=120
                        )
                        print(f"    响应: {part_resp.status_code}")
                        
                        if part_resp.status_code == 200:
                            etags.append(f"etag_for_part_{part_num}")
                    except Exception as e:
                        print(f"    错误: {e}")
                        # 尝试另一种方式
                        break
            
            # Step 5: 完成上传
            print("\n[5/5] 完成上传...")
            finish_url = "https://drive-pc.quark.cn/1/clouddrive/file/upload/finish"
            finish_data = {
                "task_id": task_id
            }
            finish_resp = httpx.post(finish_url, json=finish_data, headers=headers, timeout=30)
            print(f"  响应状态: {finish_resp.status_code}")
            print(f"  响应: {finish_resp.text[:200]}")
            
            if finish_resp.status_code == 200:
                result = finish_resp.json()
                print(f"\n结果: {result}")
                
        else:
            print(f"API错误: {pre_result}")
    else:
        print(f"HTTP错误: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
