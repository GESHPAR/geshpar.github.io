import re, pathlib

slugs = ["abandoning-mother-psychoanalysis","deformation-male-personality",
"false-confidence-relationships","infidelity-mental-pit",
"long-distance-marriage-reality","masculine-husband-dynamic",
"mother-daughter-marriage-resistance","shabgoft-03",
"toxic-mother-sensitive-daughter-psychoanalysis"]

PH = ["محتوای اصلی مقاله اینجا قرار می‌گیرد", "در حال انتقال"]
tag = '<meta name="robots" content="noindex">'
n = 0
for s in slugs:
    p = pathlib.Path("blog") / s / "index.html"
    if not p.exists():
        print(s, ": file not found"); continue
    html = p.read_text(encoding="utf-8")
    if not any(x in html for x in PH):
        print(s, ": not placeholder, skipped"); continue
    if 'name="robots"' in html:
        print(s, ": robots tag already there"); continue
    html = re.sub(r'(<head[^>]*>)', r'\1\n' + tag, html, count=1)
    p.write_text(html, encoding="utf-8")
    n += 1
    print(s, ": noindex added")
print("TOTAL noindex:", n)