import os, re, shutil

BLOG = 'blog'

# پشتیبانِ طرح فعلی
src = os.path.join(BLOG, 'index.html')
if os.path.exists(src) and not os.path.exists(src + '.backup'):
    shutil.copy2(src, src + '.backup')
    print('📦 پشتیبان ساخته شد: blog/index.html.backup')

def title_of(path, fallback):
    try:
        with open(path, encoding='utf-8') as f:
            m = re.search(r'<title>(.*?)</title>', f.read(), re.S)
        return m.group(1).strip() if m else fallback
    except Exception:
        return fallback

items = []
# نسل جدید: پوشه‌هایی که index.html دارن
for name in sorted(os.listdir(BLOG)):
    d = os.path.join(BLOG, name)
    idx = os.path.join(d, 'index.html')
    if os.path.isdir(d) and os.path.exists(idx):
        items.append((f'/blog/{name}/', title_of(idx, name)))

# نسل قدیم: فایل‌های .html که نسخه پوشه‌ای ندارن
for f in sorted(os.listdir(BLOG)):
    if f.endswith('.html') and f != 'index.html':
        slug = f[:-5]
        if not os.path.isdir(os.path.join(BLOG, slug)):
            items.append((f'/blog/{f}', title_of(os.path.join(BLOG, f), slug)))

rows = '\n'.join(f'    <li><a href="{u}">{t}</a></li>' for u, t in items)

html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>وبلاگ پارسنگ | همهٔ مقالات</title>
<link rel="stylesheet" href="/parsang.css">
</head>
<body>
<header><h1>همهٔ مقالات وبلاگ ({len(items)})</h1>
<p><a href="/">بازگشت به صفحه اصلی</a></p></header>
<main><ul>
{rows}
</ul></main>
</body>
</html>
"""

with open(src, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ blog/index.html بازسازی شد با {len(items)} مقاله')