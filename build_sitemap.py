import os
import fnmatch
from datetime import datetime, timezone

BASE = "https://geshpar.com"
OUTPUT = "sitemap.xml"

# حداقل حجم برای قبول یک مقاله بلاگ
# فایل‌های خیلی کوچک/stub وارد sitemap نمی‌شوند
MIN_ARTICLE_BYTES = 1000

# حداقل حجم برای صفحات HTML ریشه مثل about.html
MIN_ROOT_HTML_BYTES = 200

# پوشه‌هایی که هرگز نباید در sitemap باشند
SKIP_DIRS = {
    ".git",
    ".github",
    ".vscode",
    "node_modules",
    "css",
    "js",
    "assets",
    "images",
    "fonts",
    "backup_cleanup",
    "_quarantine",
    "quarantine",
    "tools",
    "scripts",
    "tests",
    "cases",
    "archive",
    "index",
}

# فایل‌هایی که هرگز نباید در sitemap باشند
SKIP_FILES = {
    "template.html",
    "archive.html",
    "sitemap.xml",
    "robots.txt",
    "favicon.ico",
}

# فایل‌های تأیید گوگل
GOOGLE_FILE_PATTERNS = (
    "google*.html",
)

# کیس‌های شاهکاری که می‌خواهیم priority بالاتر بگیرند
FEATURED_SLUGS = {
    "post-divorce-return-security-fear",
    "survivors-guilt-mother-death-anger-projection",
    "paranoid-husband-evidence-collection-trap",
    "perfectionism-body-image-oabandonment-cycle",
    "rumination-cycle-couples-therapy-focus-shift",
    "enmeshment-separation-individuation-failure-mother-daughter",
    "projective-identification-jealousy-pregnancy-narcissistic-injury",
}

urls = []
seen = set()


def file_lastmod(path):
    """تاریخ آخرین تغییر فایل را به فرمت YYYY-MM-DD برمی‌گرداند."""
    try:
        ts = os.path.getmtime(path)
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return None


def add(url, lastmod=None, priority=None):
    """افزودن URL یکتا به sitemap."""
    if url in seen:
        return
    seen.add(url)
    urls.append((url, lastmod, priority))


for root, dirs, files in os.walk("."):
    rel = os.path.relpath(root, ".").replace("\\", "/")
    rel = "" if rel == "." else rel

    # جلوگیری از blog/blog/...
    if rel == "blog/blog" or rel.startswith("blog/blog/"):
        dirs[:] = []
        continue

    # prune پوشه‌های غیرمجاز
    dirs[:] = sorted(
        d for d in dirs
        if d not in SKIP_DIRS
        and not d.startswith(".")
        and not d.startswith("_")
        and not d.endswith(".html")
    )

    for filename in sorted(files):
        if filename in SKIP_FILES:
            continue

        if any(fnmatch.fnmatch(filename, pattern) for pattern in GOOGLE_FILE_PATTERNS):
            continue

        if not filename.endswith(".html"):
            continue

        path = os.path.join(root, filename)

        try:
            size = os.path.getsize(path)
        except OSError:
            continue

        lastmod = file_lastmod(path)

        # صفحه اصلی
        if rel == "" and filename == "index.html":
            add(f"{BASE}/", lastmod, 1.0)
            continue

        # هاب بلاگ
        if rel == "blog" and filename == "index.html":
            add(f"{BASE}/blog/", lastmod, 0.9)
            continue

        # مقالات بلاگ: فقط blog/<slug>/index.html
        if rel.startswith("blog/") and filename == "index.html":
            slug = rel.split("/", 1)[1]

            # هر چیز تودرتوتر از blog/<slug>/ مجاز نیست
            if "/" in slug:
                continue

            # stubهای خیلی کوچک حذف می‌شوند
            if size < MIN_ARTICLE_BYTES:
                continue

            priority = 0.9 if slug in FEATURED_SLUGS else 0.8
            add(f"{BASE}/{rel}/", lastmod, priority)
            continue

        # صفحات HTML ریشه، مثلاً about.html
        if rel == "" and filename.endswith(".html"):
            if size >= MIN_ROOT_HTML_BYTES:
                add(f"{BASE}/{filename}", lastmod, 0.7)
            continue

        # سایر بخش‌های مجاز مثل contact/ یا guides/marriage-therapy-guide/
        # به‌شرطی که داخل blog نباشند
        if filename == "index.html" and rel and not rel.startswith("blog/"):
            add(f"{BASE}/{rel}/", lastmod, 0.7)
            continue

        # بقیه چیزها نادیده گرفته می‌شوند:
        # - .html های سرگردان داخل blog
        # - cases
        # - archive
        # - quarantine
        # - nested blog paths
        # - هر فایل غیرمجاز دیگر


# مرتب‌سازی نهایی برای خروجی پایدار
urls.sort(key=lambda item: item[0])

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    for url, lastmod, priority in urls:
        out.write("  <url>\n")
        out.write(f"    <loc>{url}</loc>\n")

        if lastmod:
            out.write(f"    <lastmod>{lastmod}</lastmod>\n")

        if priority is not None:
            out.write(f"    <priority>{priority:.1f}</priority>\n")

        out.write("  </url>\n")

    out.write("</urlset>\n")

print(f"✅ {OUTPUT} ساخته شد؛ {len(urls)} آدرس یکتا")