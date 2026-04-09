# -*- coding: utf-8 -*-
import os, sys
import json
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient

with QuarkClient() as client:
    files = client.list_files('0', page=1, size=5)
    print('Status:', files.get('status'))
    print('Code:', files.get('code'))
    print('Raw data keys:', list(files.get('data', {}).keys()) if isinstance(files.get('data'), dict) else type(files.get('data')))
    
    # Get the list
    file_list = files.get('data', {}).get('list', [])
    print('Number of files:', len(file_list))
    
    if file_list:
        print('\nFirst file structure:')
        print(json.dumps(file_list[0], indent=2, ensure_ascii=False))
