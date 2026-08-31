# -*- coding: utf-8 -*-
# rebuild_database.py
# اضافه کردن خودکار مقاله‌های جدید به دیتابیس سایت
# طرز کار: باز کردن در VS Code و زدن دکمه Run (مثلث بالا سمت راست)

import json, re
from pathlib import Path

ROOT = Path(__file__).parent
BLOG = ROOT / "blog"

DB = None
for name in ["article-data.json", "content-database.json", "inventory.json"]:
    p = ROOT / name
    if p.exists() and "total_articles" in p.read_text(encoding="utf-8"):
        DB = p
        break
if DB is None:
    print("فایل دیتابیس پیدا نشد!")
    input("برای خروج Enter بزن...")
    exit()

DEFAULTS = {
    "weekend-alone": {
        "title": "آخر هفته‌های تنها: چرا همسرم وقت نمی‌ذاره؟",
        "keywords": ["خستگی شوهر", "تنهایی زن", "تعامل زناشویی", "فرسودگی شغلی"],
        "cluster": "روابط و خانواده",
        "auto_related": ["family-boundaries", "long-distance-marriage-reality", "masculine-husband-dynamic"],
    },
    "betrayal-systemic-analysis": {
        "title": "وقتی اعتماد ترک برمی‌دارد: ماندن یا رفتن بعد از خیانت؟",
        "keywords": ["خیانت", "تروما", "بازسازی اعتماد", "بحران زناشویی"],
        "cluster": "تروما و اضطراب",
        "auto_related": ["infidelity-mental-pit", "affair-crisis-pregnancy", "collapsed-family-boundaries"],
    },
    "dependency-narcissism-cycle": {
        "title": "وقتی وابستگی می‌کُشد: تحلیل یک رابطه سمی | اختلال شخصیت وابسته",
        "keywords": ["اختلال شخصیت وابسته", "نارسیسیسم", "تحقیر", "طرحواره رهاشدگی"],
        "cluster": "روابط و خانواده",
        "auto_related": ["codependency-marriage", "false-confidence-relationships", "deformation-male-personality"],
    },
    "displaced-grief-silent-aggression": {
        "title": "دو زبان، یک دعوا: وقتی سوگ با خشم حرف می‌زند و سکوت با پرخاشگری",
        "keywords": ["سوگ", "پرخاشگری", "جابه‌جایی", "ارتباط غیرموثر"],
        "cluster": "تروما و اضطراب",
        "auto_related": ["pregnancy-rage-guilt", "untreated-mood-disorder-marriage", "collapsed-family-boundaries"],
    },
    "push-out-pull-in-paradox": {
        "title": "دو زن، یک در: فرمان «برو» و فرمان «نرو» چه چیزی را پنهان می‌کنند؟",
        "keywords": ["کنترل", "خودمختاری", "پیام دوگانه", "مرزهای زناشویی"],
        "cluster": "روابط و خانواده",
        "auto_related": ["family-boundaries", "collapsed-family-boundaries", "ideological-family-conflict"],
    },
}

db = json.loads(DB.read_text(encoding="utf-8"))
ids = {a["id"] for a in db["articles"]}

def parse_html(p):
    t = p.read_text(encoding="utf-8")
    tt = re.search(r"<title>(.*?)</title>", t, re.S)
    title = tt.group(1).split("|")[0].strip() if tt else p.stem
    cluster, date, kws = "", "", []
    m = re.search(r'class="meta"[^>]*>(.*?)</p>', t, re.S)
    if m:
        c = re.search(r"خوشه:\s*([^|<]+)", m.group(1))
        cluster = c.group(1).strip() if c else ""
        d = re.search(r"تاریخ:\s*([0-9-]+)", m.group(1))
        date = d.group(1) if d else ""
    cmt = re.search(r"<!--\s*DB:(.*?)-->", t, re.S)
    if cmt:
        kk = re.search(r"keywords=(.*?)(;|$)", cmt.group(1))
        if kk:
            kws = [x.strip() for x in re.split("[،,]", kk.group(1)) if x.strip()]
        cc = re.search(r"cluster=(.*?)(;|$)", cmt.group(1))
        if cc:
            cluster = cc.group(1).strip()
    return title, cluster, date, kws

new_ids = []
for p in sorted(BLOG.glob("*.html")):
    fid = p.stem
    if fid in ids or fid == "template":
        continue
    info = DEFAULTS.get(fid)
    if info:
        title, cluster, kws = info["title"], info["cluster"], info["keywords"]
        rel, date = info["auto_related"], "2026-08-31"
    else:
        title, cluster, date, kws = parse_html(p)
        rel = []
    db["articles"].append({
        "id": fid,
        "title": title,
        "path": "blog/%s.html" % fid,
        "keywords": kws,
        "cluster": cluster or "روابط و خانواده",
        "publish_date": date or "2026-08-31",
        "status": "published",
        "auto_related": rel,
    })
    ids.add(fid)
    new_ids.append(fid)

for a in db["articles"]:
    if a["id"] in new_ids and not a["auto_related"]:
        same = [x["id"] for x in db["articles"] if x["cluster"] == a["cluster"] and x["id"] != a["id"]]
        a["auto_related"] = same[:3]

cl = db.setdefault("clusters", {})
for a in db["articles"]:
    cl.setdefault(a["cluster"], [])
    if a["id"] not in cl[a["cluster"]]:
        cl[a["cluster"]].append(a["id"])

db["meta"]["total_articles"] = len(db["articles"])
db["meta"]["last_updated"] = "2026-08-31"

DB.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
print("انجام شد! %d مقاله جدید ثبت شد: %s" % (len(new_ids), new_ids))
input("برای خروج Enter بزن...")