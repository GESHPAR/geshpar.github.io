import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(ROOT, "blog")
DOMAIN = "https://geshpar.com"
SITEMAP_PATH = os.path.join(ROOT, "sitemap.xml")

# آستانه محتوای واقعی (حداقل کاراکتر)
MIN_CONTENT_LENGTH = 1500

# صفحات ثابت (دستی)
STATIC_PAGES = [
    {"loc": f"{DOMAIN}/", "priority": "1.0"},
    {"loc": f"{DOMAIN}/about.html", "priority": "0.7"},
    {"loc": f"{DOMAIN}/archive.html", "priority": "0.7"},
    {"loc": f"{DOMAIN}/contact/", "priority": "0.7"},
    {"loc": f"{DOMAIN}/blog/", "priority": "0.9"},
]

CASES_PAGES = [
    f"{DOMAIN}/cases/case-safe-cage.html",
    f"{DOMAIN}/cases/case-the-absent-voice.html",
    f"{DOMAIN}/cases/case-the-biology-excuse.html",
    f"{DOMAIN}/cases/case-the-dangerous-dream.html",
    f"{DOMAIN}/cases/case-the-guardian-paradox.html",
    f"{DOMAIN}/cases/case-the-impossible-request.html",
    f"{DOMAIN}/cases/case-the-role-reversal.html",
    f"{DOMAIN}/guides/marriage-therapy-guide/",
]

# الگوهای thin content
THIN_PATTERNS = [
    "در حال انتقال",
    "انتقال به نشانی جدید",
    "این صفحه منتقل شده",
    "meta http-equiv=\"refresh\"",
]

def get_file_date(path):
    """تاریخ آخرین تغییر فایل را برمی‌گرداند."""
    mtime = os.path.getmtime(path)
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

def is_real_content(html_content):
    """بررسی می‌کند آیا صفحه محتوای واقعی دارد یا thin/redirect است."""
    for pattern in THIN_PATTERNS:
        if pattern in html_content:
            return False
    
    # حذف تگ‌های HTML برای شمارش محتوای واقعی
    text = re.sub(r'<[^>]+>', '', html_content)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return len(text) >= MIN_CONTENT_LENGTH

def scan_blog_articles():
    """اسکن پوشه blog و یافتن مقالات با محتوای واقعی."""
    articles = []
    skipped = []
    
    for slug in sorted(os.listdir(BLOG)):
        slug_path = os.path.join(BLOG, slug)
        
        # فقط پوشه‌ها با index.html
        if not os.path.isdir(slug_path):
            continue
        
        index_path = os.path.join(slug_path, "index.html")
        if not os.path.isfile(index_path):
            continue
        
        try:
            content = open(index_path, encoding='utf-8').read()
        except:
            skipped.append((slug, "read error"))
            continue
        
        if is_real_content(content):
            articles.append({
                "loc": f"{DOMAIN}/blog/{slug}/",
                "lastmod": get_file_date(index_path),
                "priority": "0.8",
            })
        else:
            skipped.append((slug, "thin content"))
    
    return articles, skipped

def generate_sitemap():
    """تولید sitemap.xml نهایی."""
    articles, skipped = scan_blog_articles()
    
    print(f"=== نتیجه اسکن ===")
    print(f"  ✅ مقالات با محتوای واقعی: {len(articles)}")
    print(f"  ❌ صفحات thin/skipped: {len(skipped)}")
    
    if skipped:
        print(f"\n  صفحات حذف‌شده:")
        for slug, reason in skipped:
            print(f"    - {slug} ({reason})")
    
    # ساخت XML
    urls = []
    
    # صفحات ثابت
    for page in STATIC_PAGES:
        urls.append(f'  <url>\n    <loc>{page["loc"]}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <priority>{page["priority"]}</priority>\n  </url>')
    
    # مقالات جدید با اولویت بالا (۶ کیس عمیق)
    priority_slugs = [
        "married-but-single-paradox",
        "betrayal-doubt-loneliness-mask",
        "pathological-loyalty-happiness-as-betrayal",
        "temporary-bridges-relationships-as-tools",
        "healthy-boundaries-tolerating-ambiguity",
        "control-for-survival-closed-community",
    ]
    for art in articles:
        slug = art["loc"].split("/")[-2]
        priority = "0.9" if slug in priority_slugs else art["priority"]
        urls.append(f'  <url>\n    <loc>{art["loc"]}</loc>\n    <lastmod>{art["lastmod"]}</lastmod>\n    <priority>{priority}</priority>\n  </url>')
    
    # Cases & Guides
    for loc in CASES_PAGES:
        urls.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <priority>0.7</priority>\n  </url>')
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += '\n'.join(urls)
    xml += '\n</urlset>\n'
    
    with open(SITEMAP_PATH, "w", encoding='utf-8') as f:
        f.write(xml)
    
    print(f"\n✅ sitemap.xml تولید شد: {len(urls)} URL")

if __name__ == "__main__":
    generate_sitemap()