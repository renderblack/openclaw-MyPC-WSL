import json
with open('C:/Users/Administrator/.openclaw/openclaw.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print('=== Model Configuration Report ===')
print()
print('Primary Model:', config['agents']['defaults']['model']['primary'])
print('Fallback Models:', config['agents']['defaults']['model']['fallbacks'])
print()
print('Providers:')
providers = config.get('models', {}).get('providers', {})
for name, prov in providers.items():
    base_url = prov.get('baseUrl', 'no url')
    models = [m['id'] for m in prov.get('models', [])]
    print(f'  - {name}: {base_url}')
    print(f'    Models: {models}')
print()
print('Auth Profiles:', list(config.get('auth', {}).get('profiles', {}).keys()))
print()
print('Plugins:', list(config.get('plugins', {}).get('entries', {}).keys()))
