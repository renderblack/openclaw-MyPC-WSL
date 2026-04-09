# -*- coding: utf-8 -*-
import os, sys
os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient

with QuarkClient() as client:
    files = client.list_files('0', page=1, size=50)
    print('Files in root:')
    for f in files.get('data', {}).get('list', []):
        name = f.get('name', 'unknown')
        size = f.get('size', 0)
        ftype = f.get('type', 'unknown')
        print(f'  [{ftype}] {name} - {size/(1024**3):.2f} GB' if size else f'  [{ftype}] {name}')
