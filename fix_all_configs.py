import json

# Fix models.json
with open('C:/Users/Administrator/.openclaw/agents/main/agent/models.json', 'r', encoding='utf-8') as f:
    models_config = json.load(f)

print('=== Fixing models.json ===')
providers = models_config.get('providers', {})
print('Providers before:', list(providers.keys()))

if 'minimax' in providers:
    del providers['minimax']
    print('  Deleted: minimax')
if 'minimax-portal' in providers:
    del providers['minimax-portal']
    print('  Deleted: minimax-portal')

print('Providers after:', list(providers.keys()))

with open('C:/Users/Administrator/.openclaw/agents/main/agent/models.json', 'w', encoding='utf-8') as f:
    json.dump(models_config, f, indent=2, ensure_ascii=False)

print('models.json saved')
print()

# Fix openclaw.json
with open('C:/Users/Administrator/.openclaw/openclaw.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print('=== Fixing openclaw.json ===')
config['agents']['defaults']['model']['primary'] = 'custom-newapi/MiniMax-M2.5'
config['agents']['defaults']['model']['fallbacks'] = ['custom-newapi/MiniMax-M2.5', 'deepseek/deepseek-chat']

providers = config.get('models', {}).get('providers', {})
if 'minimax' in providers:
    del providers['minimax']
    print('  Deleted provider: minimax')

auth = config.get('auth', {})
profiles = auth.get('profiles', {})
if 'minimax:cn' in profiles:
    del profiles['minimax:cn']
    print('  Deleted auth: minimax:cn')

plugins = config.get('plugins', {})
entries = plugins.get('entries', {})
if 'minimax' in entries:
    del entries['minimax']
    print('  Deleted plugin: minimax')

with open('C:/Users/Administrator/.openclaw/openclaw.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print()
print('AFTER:')
print('  Primary:', config['agents']['defaults']['model']['primary'])
print('  Providers:', list(config.get('models', {}).get('providers', {}).keys()))
print()
print('=== All Fixed ===')
