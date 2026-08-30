import os, json

FAQ = {
 'spouse-neglect': [
   ('همسرم به من توجه نمی‌کند؛ چه کنم؟', 'بی‌توجهی همیشه به معنای بی‌علاقگی نیست؛ گاهی تفاوتِ «زبانِ محبت» است. اول نیازت را بدون سرزنش و با پیامِ «من» بیان کن و به تغییر فرصت بده؛ اگر الگو ادامه یافت، زوج‌درمانی مسیر گفت‌وگو را باز می‌کند.'),
   ('چرا همسرم نسبت به من بی‌تفاوت شده است؟', 'بی‌تفاوتی معمولاً یک‌شبه نمی‌شود؛ انبارِ کوچکی‌های نگفته است. به جای متهم کردن، گفت‌وگویی آرام دربارهٔ نیازهای دوطرفه شروع کن؛ و یادت باشد تو مسئولِ تنهاییِ دونفره نیستی.'),
 ],
 'husband-sulking': [
   ('همسرم کم‌حرف است؛ چه کنم؟', 'بعضی مردان سکوت را از کودکی به‌عنوان پناهگاه آموخته‌اند، نه به‌عنوان تنبیهِ تو. به‌جای اصرار به حرف، فضای امنِ بدون قضاوت بساز؛ اما اگر سکوت ابزارِ تنبیه شده، این الگو نیاز به بررسی تخصصی دارد.'),
   ('چرا همسرم قهر می‌کند و حرف نمی‌زند؟', 'قهر، زبانِ کسی است که گفت‌وگو را ناامن تجربه کرده. چرخهٔ «قهر–ناز» را با گفت‌وگوی بالغانه جایگزین کن؛ مرز بگذار ولی تحقیر نکن.'),
 ],
 'spouse-family-dependency': [
   ('وابستگی همسرم به خانواده‌اش؛ چه کنم؟', 'مرزِ «احترام به خانواده» و «وابستگی» همان‌جاست که زندگیِ دونفره‌تان تصمیم گرفته می‌شود. آرام، قاطع و بدون توهین به خانواده‌اش، حریمِ خصوصیِ زوجی را مرزبندی کن؛ این فرایند تدریجی است و گاهی کمکِ حرفه‌ای می‌خواهد.'),
 ],
 'spousal-infidelity': [
   ('چطور بفهمم همسرم خیانت می‌کند؟', 'تغییرِ ناگهانی رفتار (پنهان‌کاریِ گوشی، غیبتِ بی‌دلیل، اتهامِ بی‌سند به تو) می‌تواند هشدار باشد، اما «شک» به‌تنهایی سند نیست. پیش از هر تصمیم، اول آرامشِ خودت، بعد گفت‌وگوی صریح — و در صورت نیاز همراهیِ تخصصی.'),
   ('نشانه‌های خیانت همسر چیست؟', 'هیچ نشانهٔ تنها کافی نیست؛ مجموعهٔ تغییرات مهم است. اما مراقب باش: سوءظنِ بی‌پایه هم به‌اندازهٔ خیانت ویرانگر است. اگر شک زندگی‌ات را فلج کرده، پیش از جمع‌آوری «سند»، کمکِ حرفه‌ای بگیر.'),
 ],
 'diagnosing-pathological-lying': [
   ('همسرم دروغ می‌گوید؛ چرا؟', 'دروغ گاهی دفاعِ آموخته‌شده در برابر ترسِ قضاوت است و گاهی الگوی شخصیتی. دروغِ موردی، گفت‌وگوی امن و اعتمادسازی می‌خواهد؛ اما دروغ‌گوییِ بیمارگونه ارزیابی تخصصی دارد — تو به‌تنهایی مسئولِ «درمانش» نیستی.'),
 ],
}

def faq_block(items):
    h = '\n<section class="faq-section" id="faq-section">\n<h2>پرسش‌های پرتکرار شما</h2>\n'
    for q, a in items:
        h += f'<h3>{q}</h3>\n<p>{a}</p>\n'
    h += '</section>\n'
    return h

FAQ_CSS = '''
<style>
.faq-section { max-width: 760px; margin: 30px auto; padding: 20px 24px; background: #f2ede1; border-right: 4px solid #b98a2f; border-radius: 12px; direction: rtl; font-family: 'Vazirmatn', Tahoma, sans-serif; }
.faq-section h2 { color: #2f4a3e; font-size: 1.2rem; margin-bottom: 14px; }
.faq-section h3 { color: #4a6b5d; font-size: 1rem; margin: 14px 0 6px; }
.faq-section p { color: #4a443d; font-size: .92rem; line-height: 1.9; margin: 0; }
</style>
'''

n = 0
for slug, items in FAQ.items():
    idx = os.path.join('blog', slug, 'index.html')
    if not os.path.isfile(idx):
        print('⚠️ پیدا نشد:', slug)
        continue
    with open(idx, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'id="faq-section"' in html:
        continue

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ]
    }
    schema_tag = '\n<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n</script>\n'

    html = html.replace('</head>', FAQ_CSS + schema_tag + '</head>', 1)

    block = faq_block(items)
    if '<aside class="author-box"' in html:
        html = html.replace('<aside class="author-box"', block + '<aside class="author-box"', 1)
    elif '</main>' in html:
        html = html.replace('</main>', block + '</main>', 1)
    else:
        html = html.replace('</body>', block + '</body>', 1)

    with open(idx, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print('❓', slug)

print(f'✅ FAQ روی {n} مقاله نشست')