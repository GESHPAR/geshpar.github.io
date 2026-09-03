# -*- coding: utf-8 -*-
import json, re
from pathlib import Path
from datetime import date

ROOT = Path('.')
SKIP_DIRS = {'.git', '.github', 'node_modules', 'backup_cleanup'}
cname = Path('CNAME')
BASE = ('https://' + cname.read_text(encoding='utf-8').strip()) if cname.exists() else 'https://geshpar.github.io'

def junk(p):
    return bool(set(p.parts) & SKIP_DIRS) or p.name == 'template.html' or p.name.startswith('google')

def main():
    files = [p for p in ROOT.rglob('*.html') if not junk(p) and p.is_file()]
    db, urls, rows = [], [], []
    for p in files:
        try:
            html = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            print('skip:', p.as_posix())
            continue
        rel = p.as_posix()
        url = rel[:-10] if rel.endswith('index.html') else rel
        t = re.search(r'<title>(.*?)</title>', html, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        links = sorted(set(re.findall(r'href="(/[^"#]+)"', html)))
        title = t.group(1).strip() if t else rel
        db.append({'slug': p.parent.name if p.name == 'index.html' else p.stem,
                   'path': rel, 'url': BASE + '/' + url, 'title': title,
                   'description': d.group(1).strip() if d else '',
                   'category': p.parts[0] if len(p.parts) > 1 else 'root',
                   'date': str(date.today()), 'internal_links': links, 'status': 'published'})
        rows.append(f'<li><a href="/{url}">{title}</a></li>')

    Path('archive.html').write_text(f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8">
<title>فهرست کامل مقالات | پارسنگ</title>
<meta name="description" content="آرشیو همهٔ مقالات و کیس‌های پارسنگ - {len(rows)} مطلب.">
<link rel="stylesheet" href="/css/parsang.css"></head>
<body><main><h1>فهرست کامل مقالات ({len(rows)} مطلب)</h1><ul>{chr(10).join(rows)}</ul></main></body></html>""", encoding='utf-8')
    urls = [BASE + '/' + ('' if e['path'].endswith('index.html') else e['path']) for e in db] + [BASE + '/archive.html']

    Path('sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(f'  <url><loc>{u}</loc></url>' for u in urls) + '\n</urlset>\n', encoding='utf-8')

    Path('content-database.json').write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"OK pages: {len(files)} | sitemap: {len(urls)} | db: {len(db)}")

if __name__ == '__main__':
    main()