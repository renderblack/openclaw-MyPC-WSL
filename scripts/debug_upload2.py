# -*- coding: utf-8 -*-
"""
Debug: 完整的上传流程追踪
"""
import os
import sys
import json
import hashlib
import httpx
from pathlib import Path

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client.config import get_config_dir
from quark_client import QuarkClient

CONFIG_DIR = get_config_dir()
COOKIES_FILE = CONFIG_DIR / "cookies.json"

with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
    cookie_data = json.load(f)

cookies = cookie_data['cookies']
cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

# File info
FILE_PATH = r"G:\动画组共享\动画项目\2020\09-外部-上海机场线\06-成片\中铁二十四局集团上海机场联络线1标 项目介绍（20201223最终版修改）.mp4"
file_size = Path(FILE_PATH).stat().st_size
file_name = Path(FILE_PATH).name

print(f"文件: {file_name}")
print(f"大小: {file_size / (1024**3):.2f} GB")
print()

# First, let's check what API endpoints are available
print("=== Step 1: Pre-upload ===")

# Using quarkpan's API client
with QuarkClient() as client:
    # Pre-upload
    pre_result = client.api_client.post(
        "file/upload/pre",
        json_data={
            "ccp_hash_update": True,
            "parallel_upload": True,
            "pdir_fid": "0",
            "dir_name": "",
            "size": file_size,
            "file_name": file_name,
            "format_type": "video/mp4",
            "l_updated_at": 1775520000000,
            "l_created_at": 1775520000000
        },
        params={'pr': 'ucpro', 'fr': 'pc', 'uc_param_str': ''}
    )
    
    print(f"Pre-upload status: {pre_result.get('status')}")
    
    if pre_result.get('status') == 200:
        data = pre_result.get('data', {})
        print(f"Task ID: {data.get('task_id')}")
        print(f"Bucket: {data.get('bucket')}")
        print(f"Upload URL: {data.get('upload_url')}")
        print(f"Obj Key: {data.get('obj_key')[:50]}...")
        
        # Get upload auth to see what URL we should use
        task_id = data.get('task_id')
        auth_info = data.get('auth_info', '')
        upload_id = data.get('upload_id', '')
        obj_key = data.get('obj_key', '')
        bucket = data.get('bucket', 'ul-zb')
        
        # Calculate hash
        print("\n=== Step 2: Calculate hash ===")
        with open(FILE_PATH, 'rb') as f:
            content = f.read()
        sha1 = hashlib.sha1(content).hexdigest()
        print(f"SHA1: {sha1}")
        
        # Update hash
        print("\n=== Step 3: Update hash ===")
        hash_result = client.api_client.post(
            "file/update/sha1",
            json_data={
                "task_id": task_id,
                "content_hash": sha1
            }
        )
        print(f"Hash update status: {hash_result.get('status')}")
        
        # Get upload auth
        print("\n=== Step 4: Get upload auth ===")
        from datetime import datetime, timezone
        oss_date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        auth_meta = f"""PUT

video/mp4
{oss_date}
x-oss-date:{oss_date}
x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)
/{bucket}/{obj_key}?partNumber=1&uploadId={upload_id}"""
        
        auth_data = {
            "task_id": task_id,
            "auth_info": auth_info,
            "auth_meta": auth_meta
        }
        
        auth_result = client.api_client.post(
            "file/upload/auth",
            json_data=auth_data
        )
        
        print(f"Auth status: {auth_result.get('status')}")
        if auth_result.get('status') == 200:
            auth_key = auth_result.get('data', {}).get('auth_key', '')
            print(f"Auth key: {auth_key[:50]}...")
            
            # Construct the upload URL
            upload_url = f"https://{bucket}.oss-cn-shenzhen.aliyuncs.com/{obj_key}?partNumber=1&uploadId={upload_id}"
            print(f"\nConstructed upload URL: {upload_url}")
            
            # Now let's see if we can upload
            print("\n=== Step 5: Try upload ===")
            
            # First, let's check what headers are needed
            headers = {
                'Content-Type': 'video/mp4',
                'x-oss-date': oss_date,
                'x-oss-user-agent': 'aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)',
                'authorization': auth_key
            }
            
            # Read first 1MB as test
            with open(FILE_PATH, 'rb') as f:
                test_chunk = f.read(1024 * 1024)
            
            print(f"Uploading 1MB test chunk...")
            try:
                resp = httpx.put(upload_url, content=test_chunk, headers=headers, timeout=30)
                print(f"Response: {resp.status_code}")
                print(f"Response body: {resp.text[:200]}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Auth failed: {auth_result}")
