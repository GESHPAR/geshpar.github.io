import re, pathlib, glob

slugs = {"abandoning-mother-psychoanalysis","deformation-male-personality",
"false-confidence-relationships","infidelity-mental-pit",
"long-distance-marriage-reality","masculine-husband-dynamic",
"mother-daughter-marriage-resistance","shabgoft-03",
"toxic-mother-sensitive-daughter-psychoanalysis"}

files = glob.glob("**/*.html", recursive=True)
changes = 0
for fp in files:
    if "\\blog\\" in fp and any(s in fp for s in slugs):
        continue
    try:
        txt = pathlib.Path(fp).read_text(encoding="utf-8")
    except: continue
    before = txt
    for s in slugs:
        pat1 = rf'<li[^>]*>.*?/blog/{s}/?.*?</li>'
        pat2 = rf'<a[^>]*href="[^"]*{s}[^"]*"[^>]*>.*?</a>'
        txt = re.sub(pat1, "", txt, flags=re.S|re.I)
        txt = re.sub(pat2, "", txt, flags=re.S|re.I)
    if txt != before:
        pathlib.Path(fp).write_text(txt, encoding="utf-8")
        changes += 1
        print("cleaned:", fp)
print("TOTAL files cleaned:", changes)