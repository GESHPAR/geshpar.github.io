import json, pathlib

slugs = ["abandoning-mother-psychoanalysis","deformation-male-personality",
"false-confidence-relationships","infidelity-mental-pit",
"long-distance-marriage-reality","masculine-husband-dynamic",
"mother-daughter-marriage-resistance","shabgoft-03",
"toxic-mother-sensitive-daughter-psychoanalysis"]

def load(fn):
    p = pathlib.Path(fn)
    if not p.exists():
        print(f"== {fn}: FILE MISSING")
        return {}
    txt = p.read_text(encoding="utf-8")
    if not txt.strip():
        print(f"== {fn}: EMPTY FILE")
        return {}
    try:
        return json.loads(txt)
    except Exception as e:
        print(f"== {fn}: BROKEN JSON -> {e}")
        print("   first 80 chars:", repr(txt[:80]))
        return {}

def find(node, slug):
    if isinstance(node, dict):
        if node.get("slug") == slug or node.get("id") == slug:
            return node
        for v in node.values():
            r = find(v, slug)
            if r: return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, slug)
            if r: return r
    return None

def slen(node):
    if isinstance(node, str): return len(node)
    if isinstance(node, dict): return sum(slen(v) for v in node.values())
    if isinstance(node, list): return sum(slen(v) for v in node)
    return 0

for fn in ("content-database.json","article-data.json"):
    db = load(fn)
    if not db:
        continue
    print("==", fn, "OK")
    for s in slugs:
        rec = find(db, s)
        print(f"  {s}: " + (f"found, text size {slen(rec)}" if rec else "NOT FOUND"))