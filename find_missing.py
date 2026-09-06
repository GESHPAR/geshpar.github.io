import json, os

# ۱) دیتابیس — این دفعه پسوند .html از اسلاگ جدا می‌شه
db = json.load(open('content-database.json', encoding='utf-8'))
articles = db if isinstance(db, list) else db.get('articles', [])

db_slugs = set()
for a in articles:
    if not isinstance(a, dict): continue
    p = a.get('path', '').strip('/')
    if not p.startswith('blog/'): continue
    s = p.split('/')[-1]
    if s.endswith('.html'): s = s[:-5]
    if s and s != 'index': db_slugs.add(s)

# ۲) دیسک
disk = set()
for name in os.listdir('blog'):
    if name == 'index.html': continue
    if name.endswith('.html'): disk.add(name[:-5])
    elif os.path.isdir(os.path.join('blog', name)): disk.add(name)

missing = sorted(db_slugs - disk)
print(f'دیتابیس: {len(db_slugs)} | دیسک: {len(disk)} | واقعا گمشده: {len(missing)}')

# ۳) جستجو در آخرین بکاپ
bk = os.path.join('backup_cleanup', '20260904_184205', 'blog')
if os.path.isdir(bk):
    names = set(os.listdir(bk))
    in_bk = [s for s in missing if s in names or s + '.html' in names]
    print(f'✅ در بکاپ موجوده: {len(in_bk)} از {len(missing)}')
else:
    print('⚠️ پوشه blog در بکاپ نیست')

# ۴) ذخیره لیست برای وارسی آرام
with open('missing_list.txt', 'w', encoding='utf-8') as f:
    for s in missing: f.write(s + '\n')
print('📄 لیست کامل در missing_list.txt ذخیره شد')