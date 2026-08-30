import json
import os

# خواندن قالب مادر
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# خواندن داده‌های مقاله
with open('article-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# تولید FAQ Schema
faq_schema = ''
if data.get('faq'):
    faq_schema = f'''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {json.dumps([
    {{
      "@type": "Question",
      "name": item["question"],
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": item["answer"]
      }}
    }} for item in data['faq']
  ], ensure_ascii=False, indent=4)}
}}
</script>
'''

# تولید بخش FAQ در HTML
faq_section = ''
if data.get('faq'):
    faq_items = ''.join([
        f'''
    <div class="faq-item">
        <div class="faq-question">{item['question']}</div>
        <div class="faq-answer">{item['answer']}</div>
    </div>
''' for item in data['faq']
    ])
    faq_section = f'''
<section class="faq-section">
    <h2>❓ سوالات متداول</h2>
    {faq_items}
</section>
'''

# جایگزینی متغیرها در قالب
final_html = template
final_html = final_html.replace('{{TITLE}}', data['title'])
final_html = final_html.replace('{{SUBTITLE}}', data.get('subtitle', ''))
final_html = final_html.replace('{{DESCRIPTION}}', data['description'])
final_html = final_html.replace('{{KEYWORDS}}', data['keywords'])
final_html = final_html.replace('{{PUBLISH_DATE}}', data['publish_date'])
final_html = final_html.replace('{{MODIFIED_DATE}}', data.get('modified_date', data['publish_date']))
final_html = final_html.replace('{{OG_IMAGE}}', data.get('og_image', ''))
final_html = final_html.replace('{{CANONICAL_URL}}', data['canonical_url'])
final_html = final_html.replace('{{OG_TITLE}}', data['title'])
final_html = final_html.replace('{{OG_DESCRIPTION}}', data['description'])
final_html = final_html.replace('{{OG_URL}}', data['canonical_url'])
final_html = final_html.replace('{{TWITTER_TITLE}}', data['title'])
final_html = final_html.replace('{{TWITTER_DESCRIPTION}}', data['description'])
final_html = final_html.replace('{{TWITTER_IMAGE}}', data.get('og_image', ''))
final_html = final_html.replace('{{BREADCRUMB_TITLE}}', data['title'].split(':')[0])
final_html = final_html.replace('{{FAQ_SCHEMA}}', faq_schema)
final_html = final_html.replace('{{FAQ_SECTION}}', faq_section)
final_html = final_html.replace('{{CONTENT}}', data['content'])

# ذخیره فایل نهایی
output_dir = 'blog'
os.makedirs(output_dir, exist_ok=True)

slug = data['canonical_url'].rstrip('/').split('/')[-1]
output_path = os.path.join(output_dir, f'{slug}.html')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f'✅ مقاله با موفقیت تولید شد: {output_path}')
print(f'📊 تعداد سوالات متداول: {len(data.get("faq", []))}')