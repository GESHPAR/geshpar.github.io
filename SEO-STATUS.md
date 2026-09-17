# حافظه‌ی ثابت پارسنگ — اولِ هر جلسه خوانده شود
- قرارداد: فایل blog/<slug>/index.html ؛ canonical و og:url همیشه با /blog/ یعنی https://geshpar.com/blog/<slug>/
- 2026-09-15: اصلاح سراسری canonical انجام شد؛ fear-of-abandonment به healing-old-wounds ریدایرکت شد؛ سایت‌مپ تمیز شد؛ پوشه‌ی مزاحم blog/blog و مورد rushed-families تعیین‌تکلیف شد.
- قانون شب‌ها: هیچ جلسه‌ای بدون خواندن این فایل شروع نشود؛ هیچ وعده‌ای بدون اجرای همان شب بسته نشود.
- کار هفتگی: بررسی گزارش Pages کنسول + Request Indexing برای مقاله‌های جدید.## برنامه جلسه فردا — 2026-09-17

### فاز ۰ — آیین شروع (۵ دقیقه)
- [ ] خواندن CONTRACT.md از اول تا آخر
- [ ] خواندن SEO-STATUS.md از اول تا آخر
- [ ] اعلام شروع جلسه به دستیار و گفتن شماره فازی که آخرین بار جا ماندیم

### فاز ۱ — بستن چک‌لیست امشب (۱۵ دقیقه)
- [ ] خط `tools/` در .gitignore + ذخیره → خاکستری شدن seo-checks.http
- [ ] دستور تأیید: git check-ignore -v tools/seo-checks.http
- [ ] ساخت tools/status.ps1 با محتوای تأییدشده
- [ ] اجرای status.ps1 و ثبت خروجی در همین فایل
- [ ] سه دستور git (add / commit / push)
- معیار بسته شدن: push بدون خطا + tools خاکستری

### فاز ۲ — تأیید زنده stubها (۱۰ دقیقه + انتظار احتمالی)
- [ ] اجرای status.ps1
- [ ] اگر سبز: علامت‌زدن «پرونده مهاجرت URL بسته شد» در بخش اقدام‌ها
- [ ] اگر زرد: repo در گیتهاب → تب Actions/Deployments → دیدن وضعیت آخرین دیپلوی → ۱۰ دقیقه صبر → تکرار
- معیار بسته شدن: خط سبز «STUB زنده است»

### فاز ۳ — سرچ کنسول، فقط رابط کاربری (۲۰ دقیقه)
- [ ] Sitemaps → Submit مجدد sitemap.xml
- [ ] Request Indexing برای ۱۰ URL اولویت‌دار:
      /  |  /blog/  |  betrayal-doubt-loneliness-mask  |  control-for-survival-closed-community
      healthy-boundaries-tolerating-ambiguity  |  married-but-single-paradox
      pathological-loyalty-happiness-as-betrayal  |  temporary-bridges-relationships-as-tools
      khastegari-complete-guide  |  online-counseling
- معیار بسته شدن: نوشتن تاریخ درخواست‌ها در همین فایل

### فاز ۴ — یک کیس جدید، اختیاری (۶۰ دقیقه)
- [ ] دریافت کیس → تولید فقط طبق قالب §3 قرارداد
- [ ] خروجی مجاز من: کد HTML کامل + slug + سه دستور git، نه بیشتر نه کمتر
- [ ] ساخت blog/<slug>/index.html طبق §1 (پوشه اول، بعد فایل)
- [ ] به‌روزرسانی sitemap + Request Indexing برای آدرس جدید (§7)

### فاز ۵ — آیین پایان (۱۰ دقیقه)
- [ ] تیک‌خوردن همه چک‌باکس‌های امروز در همین فایل
- [ ] به‌روزرسانی خط «آخرین به‌روزرسانی» به تاریخ فردا
- [ ] قانون طلایی: هیچ وعده باز نماند؛ هر چه ماند، دقیقاً قید شود به کدام فازِ جلسه بعد می‌رود