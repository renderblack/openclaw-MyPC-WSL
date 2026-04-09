# -*- coding: utf-8 -*-
import os, sys
import json
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient

with QuarkClient() as client:
    # Search for the file we tried to upload
    print('Searching for the uploaded file...')
    results = client.search_files('中铁二十四局集团上海机场联络线1标')
    
    file_list = results.get('data', {}).get('list', [])
    print(f'Found {len(file_list)} files:')
    
    for f in file_list:
        name = f.get('file_name', 'unknown')
        size = f.get('size', 0)
        fid = f.get('fid', '')
        print(f'  {name}')
        print(f'    Size: {size/(1024**3):.2f} GB' if size else '    Size: 0')
        print(f'    FID: {fid}')
        print()
    
    # Also check recent files
    print('\nRecent files:')
    files = client.list_files('0', page=1, size=20)
    for f in files.get('data', {}).get('list', []):
        name = f.get('file_name', 'unknown')
        size = f.get('size', 0)
        updated = f.get('l_updated_at', 0)
        print(f'  {name} - {size/(1024**2):.2f} MB' if size else f'  {name}')
