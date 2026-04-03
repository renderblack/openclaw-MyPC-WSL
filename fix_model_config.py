import json

# Read config
with open('C:/Users/Administrator/.openclaw/openclaw.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print('=== Fixing Model Configuration ===')
print()
print('BEFORE:')
print('  Primary:', config['agents']['defaults']['model']['primary'])
print('  Fallbacks:', config['agents']['defaults']['model']['fallbacks'])
print('  Providers:', list(config.get('models', {}).get('providers', {}).keys()))
print('  Auth:', list(config.get('auth', {}).get('profiles', {}).keys()))
print('  Plugins:', list(config.get('plugins', {}).get('entries', {}).keys()))

# 1. Fix primary model
config['agents']['defaults']['model']['primary'] = 'custom-newapi/MiniMax-M2.5'

# 2. Fix fallbacks - remove minimax
fallbacks = config['agents']['defaults']['model']['fallbacks']
new_fallbacks = ['custom-newapi/MiniMax-M2.5', 'deepseek/deepseek-chat']
config['agents']['defaults']['model']['fallbacks'] = new_fallbacks

# 3. Remove minimax provider
providers = config.get('models', {}).get('providers', {})
if 'minimax' in providers:
    del providers['minimax']
    print()
    print('  Deleted provider: minimax')

# 4. Remove minimax auth
auth = config.get('auth', {})
profiles = auth.get('profiles', {})
if 'minimax:cn' in profiles:
    del profiles['minimax:cn']
    print('  Deleted auth profile: minimax:cn')

# 5. Remove minimax plugin
plugins = config.get('plugins', {})
entries = plugins.get('entries', {})
if 'minimax' in entries:
    del entries['minimax']
    print('  Deleted plugin entry: minimax')

# Save
with open('C:/Users/Administrator/.openclaw/openclaw.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print()
print('AFTER:')
print('  Primary:', config['agents']['defaults']['model']['primary'])
print('  Fallbacks:', config['agents']['defaults']['model']['fallbacks'])
print('  Providers:', list(config.get('models', {}).get('providers', {}).keys()))
print('  Auth:', list(config.get('auth', {}).get('profiles', {}).keys()))
print('  Plugins:', list(config.get('plugins', {}).get('entries', {}).keys()))
print()
print('=== Configuration Fixed ===')
