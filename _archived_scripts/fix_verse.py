import re, pathlib

p = pathlib.Path("blog/abandoning-mother-psychoanalysis/index.html")
html = p.read_text(encoding="utf-8")
html = html.replace("زد گردنی سر مسگری", "زدن گردن مسگری")
p.write_text(html, encoding="utf-8")
print("verse fixed")