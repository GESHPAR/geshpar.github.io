# Article SOP — پارسنگ/گشپار

## هدف
هر مقاله باید بالینی، ناشناس‌شده، دارای رضایت، حداقل ۱۵۰۰ کاراکتر متن دیده‌شده، و دارای SEO استاندارد باشد.

## ورودی اجباری
- slug
- consent: verified-anonymized
- cluster
- pillar
- related links
- transcript

## انتشار بدون این‌ها ممنوع
- رضایت تأییدشده
- ناشناس‌سازی
- حداقل ۱۵۰ کاراکتر متن دیده‌شده
- canonical درست
- title یکتا
- description یکتا
- JSON-LD معتبر
- حداقل ۳ لینک داخلی معتبر
- absence of placeholders
- author: مفید مقصودی

## مسیر فایل
blog/<slug>/index.html

## sitemap
هر مقاله جدید باید در sitemap.xml وجود داشته باشد.

## چک محلی
.\scripts\check-article.ps1 -Path blog\<slug>\index.html -Slug <slug>

## گیت
git add blog/<slug>/index.html sitemap.xml inventory.json
git commit -m "blog: add <slug>"
git push origin main