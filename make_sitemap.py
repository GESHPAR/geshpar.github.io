import re, pathlib, datetime

ROOT = pathlib.Path(".")
SITE = "https://geshpar.com"
BLOG = ROOT / "blog"
PLACEHOLDERS = ["محتوای اصلی مقاله اینجا قرار می‌گیرد", "در حال انتقال"]

def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""

def is_ph(html):
    return any(p in html for p in PLACEHOLDERS)

def set_canonical(html, url):
    tag = f'<link rel="canonical" href="{url}">'
    if re.search(r'<link[^>]+rel=["\']canonical["\']', html):
        return re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', tag, html, count=1)
    return re.sub(r'(<head[^>]*>)', r'\1\n' + tag, html, count=1)

urls = [SITE + "/", SITE + "/about.html", SITE + "/archive.html",
        SITE + "/contact/", SITE + "/blog/"]
missing = []

RED = r'http-equiv="refresh"\s+content="0;\s*url=([^"]+)"'
top_slugs = set()
for f in sorted(BLOG.glob("*.html")):
    if f.stem in ("index", "template"):
        continue
    top_slugs.add(f.stem)
    m = re.search(RED, read(f))
    if m:
        urls.append(m.group(1)); continue
    d = BLOG / f.stem / "index.html"
    m2 = re.search(RED, read(d))
    if m2:
        urls.append(m2.group(1)); continue
    urls.append(f"{SITE}/blog/{f.stem}.html")

for d in sorted(BLOG.iterdir()):
    if not d.is_dir() or d.name in top_slugs or d.name == "PPPPPPP":
        continue
    idx = d / "index.html"
    html = read(idx)
    if not html:
        continue
    if is_ph(html):
        missing.append(d.name); continue
    url = f"{SITE}/blog/{d.name}/"
    idx.write_text(set_canonical(html, url), encoding="utf-8")
    urls.append(url)

for p in sorted((ROOT / "cases").glob("*.html")):
    urls.append(f"{SITE}/cases/{p.name}")
urls.append(SITE + "/guides/marriage-therapy-guide/")

urls = list(dict.fromkeys(urls))
today = datetime.date.today().isoformat()
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    xml += ["  <url>", f"    <loc>{u}</loc>",
            f"    <lastmod>{today}</lastmod>", "  </url>"]
xml.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
print("URLs in sitemap:", len(urls))
print("Incomplete (not in sitemap):", missing)