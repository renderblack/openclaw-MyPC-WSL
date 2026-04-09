# -*- coding: utf-8 -*-
import requests
import json

# Test Quark PC client local API
port = 9128
base_url = f"http://127.0.0.1:{port}"

endpoints = [
    "/",
    "/api",
    "/api/v1",
    "/api/v1/file",
    "/api/v1/file/upload",
    "/upload",
    "/file",
    "/quark",
    "/pcs",
    "/drive",
    "/sync"
]

print(f"Testing Quark local API on port {port}...")
print()

for endpoint in endpoints:
    url = base_url + endpoint
    try:
        r = requests.get(url, timeout=3)
        print(f"{endpoint} -> {r.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"{endpoint} -> Connection refused")
    except Exception as e:
        print(f"{endpoint} -> Error: {e}")
