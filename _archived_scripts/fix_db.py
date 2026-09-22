import json

with open('content-database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

n = 0
for a in data['articles']:
    p = a.get('path', '')
    core = p.strip('/')
    parts = core.split('/')
    if parts and parts[-1].endswith('.html'):
        parts[-1] = parts[-1][:-5]
        a['path'] = '/'.join(parts) + '/'
        n += 1
        print('🔧', a['path'])

with open('content-database.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✅ تمام؛ {n} آدرس تمیز شد')