# -*- coding: utf-8 -*-
# fix_paths.py
import json, shutil
from pathlib import Path

ROOT = Path(__file__).parent
BLOG = ROOT / "blog"

moved = []
for p in sorted(BLOG.glob("*.html")):
    if p.stem == "template" or p.name == "index.html":
        continue
    folder = BLOG / p.stem
    if not folder.exists():
        folder.mkdir()
        shutil.move(str(p), str(folder / "index.html"))
        moved.append(p.stem)

for name in ["inventory.json", "article-data.json", "content-database.json"]:
    f = ROOT / name
    if not f.exists():
        continue
    try:
        db = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue
    ch = False
    for a in db.get("articles", []):
        if not isinstance(a, dict):
            continue
        fid = a.get("id") or a.get("slug") or ""
        if not fid:
            continue
        if a.get("path") == "blog/%s.html" % fid:
            a["path"] = "blog/%s/" % fid
            ch = True
    if ch:
        f.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")

print("منتقل شد:", moved)
print("تمام شد.")
input("برای خروج Enter بزن...")