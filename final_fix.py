import os, shutil

moves = []

# ۱) blog/blog/x.html -> blog/x.html
src = os.path.join('blog', 'blog')
if os.path.isdir(src):
    for f in os.listdir(src):
        s, d = os.path.join(src, f), os.path.join('blog', f)
        if os.path.isfile(s) and not os.path.exists(d):
            shutil.move(s, d); moves.append(f'blog/blog/{f} -> blog/{f}')
    if not os.listdir(src): os.rmdir(src)

# ۲) blog/cases/x.html -> cases/x.html
src = os.path.join('blog', 'cases')
if os.path.isdir(src):
    os.makedirs('cases', exist_ok=True)
    for f in os.listdir(src):
        s, d = os.path.join(src, f), os.path.join('cases', f)
        if os.path.isfile(s) and not os.path.exists(d):
            shutil.move(s, d); moves.append(f'blog/cases/{f} -> cases/{f}')
    if not os.listdir(src): os.rmdir(src)

# ۳) blog/index/index.html -> blog/index.html
src = os.path.join('blog', 'index')
if os.path.isdir(src):
    inner, dst = os.path.join(src, 'index.html'), os.path.join('blog', 'index.html')
    if os.path.exists(inner):
        if not os.path.exists(dst):
            shutil.move(inner, dst); moves.append('blog/index/index.html -> blog/index.html')
        else:
            os.remove(inner); moves.append('حذف تکراری: blog/index/index.html')
    if not os.listdir(src): os.rmdir(src)

print('--- جابه‌جایی‌ها ---')
for m in moves: print('📦', m)
if not moves: print('(چیزی جابه‌جا نشد)')

# ۴) ساخت sitemap تمیز
BASE = 'https://geshpar.com'
SKIP_DIRS = {'.git', '.github', 'backup_cleanup', 'node_modules', 'css'}
SKIP_FILES = {'google9869e7a22ec28571.html', 'googledb6df8098a4bbafc.html', 'template.html'}

urls, seen = [], set()
def add(u):
    if u not in seen:
        seen.add(u); urls.append(u)

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS
               and not d.startswith('.') and not d.endswith('.html')]
    rel = os.path.relpath(root, '.').replace('\\', '/')
    rel = '' if rel == '.' else rel
    for f in sorted(files):
        if f in SKIP_FILES: continue
        if f == 'index.html':
            add(f'{BASE}/{rel}/' if rel else f'{BASE}/')
        elif f.endswith('.html'):
            if os.path.isdir(os.path.join(root, f[:-5])): continue
            add(f'{BASE}/{rel}/{f}' if rel else f'{BASE}/{f}')

with open('sitemap.xml', 'w', encoding='utf-8') as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        out.write(f'  <url><loc>{u}</loc></url>\n')
    out.write('</urlset>\n')

# ۵) چک نهایی خودکار
print('--- چک نهایی sitemap ---')
s = open('sitemap.xml', encoding='utf-8').read()
for bad in ['.html/', '/blog/blog/', '/blog/cases/', '/blog/index/']:
    print('❌ پیدا شد: ' + bad if bad in s else '✅ تمیز: ' + bad)
print(f'✅ تعداد آدرس یکتا: {len(urls)}')
