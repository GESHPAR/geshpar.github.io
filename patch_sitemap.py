import pathlib

p = pathlib.Path("make_sitemap.py")
t = p.read_text(encoding="utf-8")
old = "    return any(p in html for p in PLACEHOLDERS)"
new = '''    import re as _re
    return bool(_re.search(r'<p[^>]*>\\s*(?:محتوای اصلی مقاله اینجا قرار می‌گیرد|در حال انتقال)[^<]*</p>', html))'''
if old in t:
    t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
    print("patched OK")
else:
    print("pattern not found! show me make_sitemap.py lines around is_ph")
    