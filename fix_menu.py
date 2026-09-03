# -*- coding: utf-8 -*-
from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

# تغییر ۱: اضافه کردن لینک فهرست مقالات به منو
old_nav = '<li><a href="#articles">وبلاگ</a></li>'
new_nav = '<li><a href="#articles">وبلاگ</a></li>\n      <li><a href="/archive.html">فهرست مقالات</a></li>'
html = html.replace(old_nav, new_nav)

# تغییر ۲: اصلاح لینک کارت آرشیو کیس‌ها
old_card = '<a href="#cluster-clinical" style="background: var(--card); border-radius: 20px; padding: 26px; box-shadow: 0 6px 20px rgba(0,0,0,.05); transition: .25s; border-top: 4px solid var(--ink); display: block; text-decoration: none; color: inherit;">'
new_card = '<a href="/archive.html" style="background: var(--card); border-radius: 20px; padding: 26px; box-shadow: 0 6px 20px rgba(0,0,0,.05); transition: .25s; border-top: 4px solid var(--ink); display: block; text-decoration: none; color: inherit;">'
html = html.replace(old_card, new_card)

p.write_text(html, encoding='utf-8')
print("✅ منو و کارت آرشیو آپدیت شدند")