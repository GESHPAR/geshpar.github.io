import os

AUTHOR_BOX_HTML = '''
<aside class="author-box" id="author-box">
  <div class="author-avatar">م‌م</div>
  <div class="author-info">
    <h3>مفید مقصودی</h3>
    <p class="author-title">کارشناس ارشد روانشناسی بالینی | شمارهٔ نظام: ۲۱۶۸</p>
    <p class="author-bio">بیش از ۳۰ سال تجربه و ۱۰,۰۰۰ جلسه مشاوره با رویکرد کل‌نگر. عضو سازمان نظام روانشناسی و مشاوره ایران.</p>
    <a href="/about.html" class="author-link">دربارهٔ درمانگر ←</a>
  </div>
</aside>
'''

AUTHOR_BOX_CSS = '''
<style>
.author-box {
  max-width: 760px;
  margin: 40px auto 30px;
  padding: 24px;
  background: #faf6ee;
  border: 2px solid #b98a2f;
  border-radius: 16px;
  display: flex;
  gap: 20px;
  align-items: center;
  direction: rtl;
  font-family: 'Vazirmatn', Tahoma, sans-serif;
}
.author-avatar {
  width: 90px; height: 90px; min-width: 90px;
  border-radius: 50%;
  background: #2f4a3e; color: #f4efe6;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; font-weight: 800;
  border: 3px solid #b98a2f;
}
.author-info h3 { color: #2f4a3e; font-size: 1.15rem; margin: 0 0 6px; }
.author-title { color: #b98a2f; font-size: .9rem; margin: 0 0 10px; font-weight: 600; }
.author-bio { color: #4a443d; font-size: .9rem; line-height: 1.8; margin: 0 0 10px; }
.author-link { color: #4a6b5d; font-weight: 700; text-decoration: none; font-size: .9rem; }
.author-link:hover { color: #b98a2f; }
@media (max-width: 600px) { .author-box { flex-direction: column; text-align: center; } }
</style>
'''

AUTHOR_SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "مفید مقصودی",
    "jobTitle": "روانشناس بالینی",
    "url": "https://geshpar.com/about.html",
    "identifier": {
      "@type": "PropertyValue",
      "name": "شماره پروانه نظام روانشناسی",
      "value": "2168"
    },
    "memberOf": {
      "@type": "Organization",
      "name": "سازمان نظام روانشناسی و مشاوره ایران"
    },
    "worksFor": {
      "@type": "MedicalBusiness",
      "name": "کلینیک روانشناسی پارسنگ"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "کلینیک روانشناسی پارسنگ",
    "url": "https://geshpar.com"
  }
}
</script>
'''

blog_dir = 'blog'
n = 0
for article_dir in os.listdir(blog_dir):
    idx = os.path.join(blog_dir, article_dir, 'index.html')
    if not os.path.isfile(idx):
        continue

    with open(idx, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'id="author-box"' in html:
        continue

    if AUTHOR_BOX_CSS.strip() not in html:
        html = html.replace('</head>', AUTHOR_BOX_CSS + '\n</head>')

    if '"@type": "Article"' not in html:
        html = html.replace('</head>', AUTHOR_SCHEMA + '\n</head>')

    if '</main>' in html:
        html = html.replace('</main>', AUTHOR_BOX_HTML + '\n</main>', 1)
    else:
        html = html.replace('</body>', AUTHOR_BOX_HTML + '\n</body>')

    with open(idx, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print('✍️', article_dir)

print(f'✅ مهر اعتبار روی {n} مقاله نشست')