# -*- coding: utf-8 -*-
import os, sys
import json
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient
from pathlib import Path

FILE_PATH = r"G:\动画组共享\动画项目\2020\09-外部-上海机场线\06-成片\中铁二十四局集团上海机场联络线1标 项目介绍（20201223最终版修改）.mp4"

with QuarkClient() as client:
    file_size = Path(FILE_PATH).stat().st_size
    
    # Call pre_upload directly
    print(f"文件: {Path(FILE_PATH).name}")
    print(f"大小: {file_size / (1024**3):.2f} GB")
    print()
    
    # Check the pre_upload response
    result = client.api_client.post(
        "file/upload/pre",
        json_data={
            "ccp_hash_update": True,
            "parallel_upload": True,
            "pdir_fid": "0",
            "dir_name": "",
            "size": file_size,
            "file_name": Path(FILE_PATH).name,
            "format_type": "video/mp4",
            "l_updated_at": int(1775519812000),
            "l_created_at": int(1775519812000)
        },
        params={'pr': 'ucpro', 'fr': 'pc', 'uc_param_str': ''}
    )
    
    print("Pre-upload response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get('status') == 2000000:
        data = result.get('data', {})
        print(f"\n返回的bucket: {data.get('bucket')}")
        print(f"返回的upload_url: {data.get('upload_url', 'N/A')[:100]}...")
