# -*- coding: utf-8 -*-
"""
夸克网盘上传 - 使用 pds.quark.cn 直传
"""
import os
import sys
import json
import hashlib
import httpx
from pathlib import Path
from datetime import datetime, timezone

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

with QuarkClient() as client:
    # Pre-upload
    print("=== Step 1: Pre-upload ===")
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
    
    print(f"Status: {pre_result.get('status')}")
    
    if pre_result.get('status') != 200:
        print(f"Pre-upload failed: {pre_result}")
        sys.exit(1)
    
    data = pre_result.get('data', {})
    task_id = data.get('task_id')
    bucket = data.get('bucket', 'ul-zb')
    upload_url_base = data.get('upload_url', 'http://pds.quark.cn')
    obj_key = data.get('obj_key')
    upload_id = data.get('upload_id', '')
    auth_info = data.get('auth_info', '')
    
    print(f"Task ID: {task_id}")
    print(f"Bucket: {bucket}")
    print(f"Upload URL base: {upload_url_base}")
    print(f"Upload ID: {upload_id}")
    print(f"Obj Key: {obj_key[:50]}...")
    
    # Calculate hash
    print("\n=== Step 2: Calculate hash ===")
    with open(FILE_PATH, 'rb') as f:
        content = f.read()
    sha1 = hashlib.sha1(content).hexdigest()
    md5 = hashlib.md5(content).hexdigest()
    print(f"SHA1: {sha1}")
    print(f"MD5: {md5}")
    
    # Upload file directly to pds.quark.cn
    print("\n=== Step 3: Upload to pds.quark.cn ===")
    
    # Construct the full upload URL with upload_id
    upload_full_url = f"{upload_url_base}/{obj_key}?uploadId={upload_id}"
    print(f"Full upload URL: {upload_full_url[:80]}...")
    
    # Try PUT upload with auth headers
    oss_date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # First get auth - include uploadId in auth_meta
    auth_meta = f"""PUT

video/mp4
{oss_date}
x-oss-date:{oss_date}
x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)
/{bucket}/{obj_key}?uploadId={upload_id}"""
    
    auth_payload = {
        "task_id": task_id,
        "auth_info": auth_info,
        "auth_meta": auth_meta
    }
    
    print("\nGetting auth...")
    auth_result = client.api_client.post("file/upload/auth", json_data=auth_payload)
    print(f"Auth status: {auth_result.get('status')}")
    
    if auth_result.get('status') == 200:
        auth_key = auth_result.get('data', {}).get('auth_key', '')
        print(f"Got auth key: {auth_key[:30]}...")
        
        # Try PUT to pds.quark.cn
        headers = {
            'Content-Type': 'video/mp4',
            'x-oss-date': oss_date,
            'x-oss-user-agent': 'aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)',
            'authorization': auth_key,
            'Content-Length': str(file_size)
        }
        
        print(f"\nUploading {file_size/(1024**2):.1f} MB file...")
        
        # Open file and upload
        with open(FILE_PATH, 'rb') as f:
            resp = httpx.put(
                upload_full_url,
                content=f.read(),
                headers=headers,
                timeout=300
            )
        
        print(f"Response status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
        
        if resp.status_code in [200, 201, 204]:
            print("\n=== Upload successful! ===")
            
            # Now finish
            print("\n=== Step 4: Finish upload ===")
            finish_result = client.api_client.post(
                "file/upload/finish",
                json_data={"task_id": task_id}
            )
            print(f"Finish status: {finish_result.get('status')}")
            print(f"Finish result: {finish_result}")
        else:
            print(f"\nUpload failed with status {resp.status_code}")
    else:
        print(f"Auth failed: {auth_result}")
