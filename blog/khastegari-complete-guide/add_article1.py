import json

entry = {
  "id": "khastegari-complete-guide",
  "title": "راهنمای کامل خواستگاری: چه بپرسیم، کی بپرسیم، چه بگوییم؟",
  "path": "/blog/khastegari-complete-guide/",
  "keywords": ["خواستگاری", "آشنایی قبل از ازدواج", "پسر بگیر", "قرار اول", "عقد قبلی"],
  "cluster": "ازدواج و آشنایی",
  "publish_date": "2026-08-30",
  "status": "published",
  "auto_related": []
}

with open('content-database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if not any(a.get('id') == entry['id'] for a in data['articles']):
    data['articles'].append(entry)
    with open('content-database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('✅ به دیتابیس اضافه شد')
else:
    print('⏭️ قبلاً در دیتابیس بود')

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    s = f.read()

if 'khastegari-complete-guide' not in s:
    block = '''  <url>
    <loc>https://geshpar.com/blog/khastegari-complete-guide/</loc>
    <lastmod>2026-08-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>'''
    s = s.replace('</urlset>', block)
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(s)
    print('✅ به نقشهٔ سایت اضافه شد')
else:
    print('⏭️ قبلاً در نقشه بود')