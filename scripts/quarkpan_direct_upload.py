# -*- coding: utf-8 -*-
"""
夸克网盘上传 - 使用直传方式
"""
import os
import sys
import json
import base64
import hashlib
import httpx
from pathlib import Path

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

print("Cookie string:", cookie_string[:50], "...")

# 文件信息
FILE_PATH = r"G:\动画组共享\动画项目\2020\09-外部-上海机场线\06-成片\中铁二十四局集团上海机场联络线1标 项目介绍（20201223最终版修改）.mp4"
file_size = Path(FILE_PATH).stat().st_size
file_name = Path(FILE_PATH).name

print(f"\n文件: {file_name}")
print(f"大小: {file_size / (1024**3):.2f} GB")

# Step 1: Pre-upload
print("\n[1/4] 发起预上传请求...")

pre_url = "https://drive-pc.quark.cn/1/clouddrive/file/upload/pre"

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

headers = {
    'Cookie': cookie_string,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Referer': 'https://pan.quark.cn/'
}

response = httpx.post(pre_url, json=pre_data, headers=headers, timeout=30)
print(f"预上传响应状态: {response.status_code}")
pre_result = response.json()
print(json.dumps(pre_result, indent=2, ensure_ascii=False)[:500])

if pre_result.get('status') == 200:
    data = pre_result.get('data', {})
    task_id = data.get('task_id', '')
    upload_id = data.get('upload_id', '')
    obj_key = data.get('obj_key', '')
    bucket = data.get('bucket', '')
    auth_info = data.get('auth_info', '')
    
    print(f"\n获取到:")
    print(f"  task_id: {task_id}")
    print(f"  bucket: {bucket}")
    print(f"  upload_id: {upload_id}")
    print(f"  obj_key: {obj_key[:50]}...")
    
    # Step 2: 计算文件 hash
    print("\n[2/4] 计算文件哈希...")
    with open(FILE_PATH, 'rb') as f:
        content = f.read()
    md5 = hashlib.md5(content).hexdigest()
    sha1 = hashlib.sha1(content).hexdigest()
    print(f"  MD5: {md5}")
    print(f"  SHA1: {sha1}")
    
    # Step 3: 获取上传授权
    print("\n[3/4] 获取上传授权...")
    
    oss_date = 'Tue, 07 Apr 2026 00:00:00 GMT'
    
    auth_meta = f"""PUT

video/mp4
{oss_date}
x-oss-date:{oss_date}
x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)
/{bucket}/{obj_key}?partNumber=1&uploadId={upload_id}"""
    
    auth_url = "https://drive-pc.quark.cn/1/clouddrive/file/upload/auth"
    auth_data = {
        "task_id": task_id,
        "auth_info": auth_info,
        "auth_meta": auth_meta
    }
    
    auth_response = httpx.post(auth_url, json=auth_data, headers=headers, timeout=30)
    print(f"授权响应状态: {auth_response.status_code}")
    auth_result = auth_response.json()
    print(json.dumps(auth_result, indent=2, ensure_ascii=False)[:500])
    
    if auth_result.get('status') == 200:
        auth_data_response = auth_result.get('data', {})
        upload_url = f"https://{bucket}.oss-cn-shenzhen.aliyuncs.com/{obj_key}?partNumber=1&uploadId={upload_id}"
        auth_key = auth_data_response.get('auth_key', '')
        
        print(f"\n上传URL: {upload_url[:80]}...")
        
        # Step 4: 上传到 OSS
        print("\n[4/4] 上传文件到OSS...")
        
        upload_headers = {
            'Content-Type': 'video/mp4',
            'x-oss-date': oss_date,
            'x-oss-user-agent': 'aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)',
            'authorization': auth_key
        }
        
        # 分片上传（20MB per part）
        part_size = 20 * 1024 * 1024
        total_parts = (file_size + part_size - 1) // part_size
        print(f"总分片数: {total_parts}")
        
        with open(FILE_PATH, 'rb') as f:
            for part_num in range(1, total_parts + 1):
                chunk = f.read(part_size)
                chunk_size = len(chunk)
                
                # 构建当前分片的 auth_meta
                part_auth_meta = f"""PUT

video/mp4
{oss_date}
x-oss-date:{oss_date}
x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)
/{bucket}/{obj_key}?partNumber={part_num}&uploadId={upload_id}"""
                
                # 获取当前分片授权
                part_auth_data = {
                    "task_id": task_id,
                    "auth_info": auth_info,
                    "auth_meta": part_auth_meta
                }
                
                part_auth_resp = httpx.post(auth_url, json=part_auth_data, headers=headers, timeout=30)
                part_auth = part_auth_resp.json()
                
                if part_auth.get('status') == 200:
                    part_auth_key = part_auth.get('data', {}).get('auth_key', '')
                    part_upload_url = f"https://{bucket}.oss-cn-shenzhen.aliyuncs.com/{obj_key}?partNumber={part_num}&uploadId={upload_id}"
                    
                    part_headers = {
                        'Content-Type': 'video/mp4',
                        'x-oss-date': oss_date,
                        'x-oss-user-agent': 'aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)',
                        'authorization': part_auth_key
                    }
                    
                    print(f"上传分片 {part_num}/{total_parts} ({chunk_size/(1024**2):.1f} MB)...")
                    
                    part_resp = httpx.put(part_upload_url, content=chunk, headers=part_headers, timeout=120)
                    print(f"  响应状态: {part_resp.status_code}")
                    
                    if part_resp.status_code != 200:
                        print(f"  错误: {part_resp.text[:200]}")
                        break
                else:
                    print(f"分片 {part_num} 授权失败")
                    break
        
        print("\n上传完成!")
        
    else:
        print("授权获取失败")
else:
    print("预上传请求失败")
