import os

BASE = 'https://geshpar.com'

# پوشه‌هایی که نباید در sitemap باشند
SKIP_DIRS = {'.git', '.github', 'backup_cleanup', 'node_modules', 'css'}
# فایل‌هایی که نباید در sitemap باشند (فایل‌های تأیید گوگل و قالب خالی)
SKIP_FILES = {
    'google9869e7a22ec28571.html', 
    'googledb6df8098a4bbafc.html',
    'template.html'
}

urls = []
seen = set()

def add(url):
    if url not in seen:          # ضد تکراری
        seen.add(url)
        urls.append(url)

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]

    rel = os.path.relpath(root, '.').replace('\\', '/')
    rel = '' if rel == '.' else rel

    for f in sorted(files):
        if f in SKIP_FILES:
            continue

        if f == 'index.html':
            # پوشه‌ای که index.html داره → آدرس با اسلش آخر
            add(f'{BASE}/{rel}/' if rel else f'{BASE}/')

        elif f.endswith('.html'):
            slug = f[:-5]
            # اگه نسخه پوشه‌ایِ همین مقاله وجود داره، فایل قدیمی رو ثبت نکن
            if os.path.isdir(os.path.join(root, slug)):
                continue
            add(f'{BASE}/{rel}/{f}' if rel else f'{BASE}/{f}')

with open('sitemap.xml', 'w', encoding='utf-8') as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        out.write(f'  <url><loc>{u}</loc></url>\n')
    out.write('</urlset>\n')

print(f'✅ sitemap.xml ساخته شد با {len(urls)} آدرس یکتا')