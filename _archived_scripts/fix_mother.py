import re, pathlib

p = pathlib.Path("blog/mother-daughter-marriage-resistance/index.html")
html = p.read_text(encoding="utf-8")
html = re.sub(r'<meta name="robots" content="noindex">\s*', '', html)
p.write_text(html, encoding="utf-8")
print("noindex removed")

slugs = ["abandoning-mother-psychoanalysis","deformation-male-personality",
"false-confidence-relationships","infidelity-mental-pit",
"long-distance-marriage-reality","masculine-husband-dynamic",
"mother-daughter-marriage-resistance","shabgoft-03",
"toxic-mother-sensitive-daughter-psychoanalysis"]

arc_p = pathlib.Path("archive.html")
arc = arc_p.read_text(encoding="utf-8")
added = 0
for s in slugs:
    if f'href="/blog/{s}/"' in arc:
        continue
    hp = pathlib.Path("blog") / s / "index.html"
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', hp.read_text(encoding="utf-8"), flags=re.S)
    title = h1.group(1).strip() if h1 else s
    i = arc.rfind('</ul>')
    arc = arc[:i] + f'<li><a href="/blog/{s}/">{title}</a></li>\n' + arc[i:]
    added += 1
    print("archive +", s)
arc_p.write_text(arc, encoding="utf-8")
print("archive links added:", added)