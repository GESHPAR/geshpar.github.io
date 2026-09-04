# -*- coding: utf-8 -*-
import json
from pathlib import Path

db = json.loads(Path('content-database.json').read_text(encoding='utf-8'))
items = sorted(db, key=lambda e: e.get('date',''), reverse=True)

rows = "\n".join(
    f'<li><a href="/{e["path"]}">{e["title"]}</a></li>' for e in items
)

html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>فهرست کامل مقالات و کیس‌ها | پارسنگ</title>
<meta name="description" content="آرشیو همهٔ مقالات، کیس‌ها و راهنماهای کلینیک پارسنگ - {len(items)} مطلب.">
<link rel="stylesheet" href="/css/parsang.css">
</head>
<body>
<main>
<h1>فهرست کامل مقالات ({len(items)} مطلب)</h1>
<ul class="archive-list">
{rows}
</ul>
</main>
</body>
</html>"""

Path('archive.html').write_text(html, encoding='utf-8')
print(f"✅ archive.html با {len(items)} مطلب ساخته شد")