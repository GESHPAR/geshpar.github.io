import re, pathlib

BLOG = pathlib.Path("blog")
SITE = "https://geshpar.com"
PLACEHOLDERS = ["محتوای اصلی مقاله اینجا قرار می‌گیرد", "در حال انتقال"]

def is_placeholder(html):
    return any(p in html for p in PLACEHOLDERS)

def set_canonical(html, url):
    tag = f'<link rel="canonical" href="{url}">'
    if re.search(r'<link[^>]+rel=["\']canonical["\']', html):
        return re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', tag, html, count=1)
    return re.sub(r'(<head[^>]*>)', r'\1\n' + tag, html, count=1)

def redirect_page(url):
    return f'''<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<title>انتقال به نشانی جدید</title>
<script>location.replace("{url}");</script>
</head>
<body>
<p>این مقاله منتقل شده است: <a href="{url}">{url}</a></p>
</body>
</html>'''

report = []
for f in sorted(BLOG.glob("*.html")):
    slug = f.stem
    if slug in ("index", "template"):
        continue
    d = BLOG / slug / "index.html"
    html_real = not is_placeholder(f.read_text(encoding="utf-8"))
    dir_real = d.exists() and not is_placeholder(d.read_text(encoding="utf-8"))

    if d.exists() and dir_real:
        url = f"{SITE}/blog/{slug}/"
        f.write_text(redirect_page(url), encoding="utf-8")
        d.write_text(set_canonical(d.read_text(encoding="utf-8"), url), encoding="utf-8")
        report.append(f"REDIRECT  {slug}.html  ->  {slug}/")
    elif d.exists() and not dir_real and html_real:
        url = f"{SITE}/blog/{slug}.html"
        d.write_text(redirect_page(url), encoding="utf-8")
        f.write_text(set_canonical(f.read_text(encoding="utf-8"), url), encoding="utf-8")
        report.append(f"REDIRECT  {slug}/  ->  {slug}.html  (نسخه پوشه خالی بود)")
    elif not d.exists() and html_real:
        url = f"{SITE}/blog/{slug}.html"
        f.write_text(set_canonical(f.read_text(encoding="utf-8"), url), encoding="utf-8")
        report.append(f"CANONICAL {slug}.html")
    else:
        report.append(f"CHECK     {slug}  (بررسی دستی)")

bi = BLOG / "index.html"
if bi.exists():
    bi.write_text(set_canonical(bi.read_text(encoding="utf-8"), f"{SITE}/blog/"), encoding="utf-8")

print("\n".join(report))
print("TOTAL:", len(report))