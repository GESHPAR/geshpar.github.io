import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(ROOT, "blog")

# اسلاگ‌های معتبر = پوشه‌هایی که index.html دارند
valid = sorted(
    (d for d in os.listdir(BLOG) if os.path.isfile(os.path.join(BLOG, d, "index.html"))),
    key=len, reverse=True
)
alt = "|".join(map(re.escape, valid))

re_root   = re.compile(r'(href=")/(' + alt + r')/"')          # href="/slug/"  ->  href="/blog/slug/"
re_canon  = re.compile(r'(https://geshpar\.com)/(' + alt + r')/')  # canonical/og بدون blog
re_nested = re.compile(r'(href="/blog/)([a-z0-9-]+)/([a-z0-9-]+)\.html"')  # ساختار قدیمی تودرتو

fixed = []
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d != ".git"]
    for fn in files:
        if not fn.endswith(".html"):
            continue
        p = os.path.join(dirpath, fn)
        src = open(p, encoding="utf-8").read()
        out = re_root.sub(r'\1/blog/\2/"', src)
        out = re_canon.sub(r'\1/blog/\2/', out)
        out = re_nested.sub(
            lambda m: f'{m.group(1)}{m.group(3)}/"' if m.group(3) in valid else m.group(0),
            out
        )
        if out != src:
            open(p, "w", encoding="utf-8").write(out)
            fixed.append(os.path.relpath(p, ROOT))

print(f"{len(fixed)} فایل اصلاح شد:")
for f in fixed:
    print("  ", f)