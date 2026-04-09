# -*- coding: utf-8 -*-
import os, sys
import json
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient

with QuarkClient() as client:
    # Search for any file with "中铁" in the name
    print('Searching for "中铁"...')
    results = client.search_files('中铁', size=20)
    print('Status:', results.get('status'))
    print('Code:', results.get('code'))
    
    file_list = results.get('data', {}).get('list', [])
    print(f'Found {len(file_list)} files:')
    for f in file_list:
        name = f.get('file_name', 'unknown')
        size = f.get('size', 0)
        fid = f.get('fid', '')
        print(f'  {name} - {size/(1024**3):.2f} GB' if size else f'  {name}')
        print(f'    FID: {fid}')
    
    # Also list root to check for large files
    print('\n\nListing root directory (looking for large files):')
    files = client.list_files('0', page=1, size=100)
    for f in files.get('data', {}).get('list', []):
        name = f.get('file_name', 'unknown')
        size = f.get('size', 0)
        is_dir = f.get('dir', False)
        if size > 1024*1024*1024:  # Files larger than 1GB
            print(f'  [LARGE] {name} - {size/(1024**3):.2f} GB')
        elif not is_dir:
            print(f'  {name} - {size/(1024**2):.2f} MB' if size else f'  {name}')
