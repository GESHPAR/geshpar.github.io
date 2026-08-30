import re
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    s = f.read()
s2 = re.sub(r'(https://geshpar\.com/blog/)([A-Za-z0-9\-]+)\.html', r'\1\2/', s)
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(s2)
print('✅ نقشهٔ سایت تمیز شد')