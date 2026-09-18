# قرارداد ثابت پارسنگ — اولِ هر جلسه، قبل از هر کاری خوانده شود

## ۱. ساختار فایل‌ها (بدون استثنا)
- مسیر مقاله در ریپو: `blog/<slug>/index.html`
- روش ساخت در VS Code: راست‌کلیک روی `blog` → New Folder → نام slug → راست‌کلیک روی پوشه‌ی جدید → New File → نام `index.html`
- هرگز از New File با مسیر `slug/index.html` استفاده نکن
- هرگز پوشه‌ی تودرتو نساز (`blog/blog/...` ممنوع)

## ۲. آدرس واقعی سایت (بدون استثنا)
- URL واقعی: `https://geshpar.com/blog/<slug>/`
- تگ `<link rel="canonical">` دقیقاً همین URL باشد
- تگ `<meta property="og:url">` دقیقاً همین URL باشد
- هرگز بدون `/blog/` ننویس

## ۳. قالب HTML ثابت (بدون استثنا)
- topbar، back-link، H1، meta-line (شماره نظام ۲۱۶۸)، story-box، H2 تحلیل روانکاوانه با سه H3، blockquote جمله مراجع، hr، H2 سوپرویژن تحلیلی با سه H3، blockquote جمله درمانگر، H3 بینش نهایی، related-posts فقط از slugهای موجود، CTA با /contact/، footer، author-box، اسکریپت copy-guard
- هیچ استایل، کلاس یا بخش جدید اضافه نکن
- فقط محتوای کیس را در همین قالب بگذار

## ۴. تحلیل روانکاوانه (بدون استثنا)
- تحلیل فقط از دینامیک درونی خود مراجع
- روایت او از دیگران واقعیت مطلق نیست
- از نظریات بزرگان روانکاوی استفاده کن (فروید، کلاین، بالبی، وینی‌کات)

## ۵. خروجی پایان هر کیس (بدون استثنا)
- کد HTML کامل
- slug
- سه دستور git (add، commit، push)
- نه بیشتر، نه کمتر

## ۶. روش کار در ترمینال (بدون استثنا)
- کد HTML فقط داخل فایل index.html پیست شود
- به ترمینال فقط سه دستور git داده شود
- هرگز HTML را در ترمینال پیست نکن
- هرگز چند دستور را یک‌جا پیست نکن (مگر بلوک‌های تأییدشده)

## ۷. سایت‌مپ و کنسول (بدون استثنا)
- بعد از هر مقاله، سایت‌مپ به‌روز شود
- در کنسول، Request Indexing برای آدرس جدید
- Submit دوباره‌ی سایت‌مپ اگر لازم است

## ۸. فایل‌های حافظه (بدون استثنا)
- `CONTRACT.md` اولِ هر جلسه خوانده شود
- `SEO-STATUS.md` برای پیگیری وضعیت فنی
- هیچ جلسه‌ای بدون خواندن این دو شروع نشود

## ۹. قانون طلایی (بدون استثنا)
- هیچ وعده‌ای بدون اجرای همان شب بسته نشود
- هیچ تغییری بدون تأیید کاربر اعمال نشود
- هیچ فرضی بدون تست زنده پذیرفته نشود

---
**امضا:** این قرارداد از تاریخ 2026-09-15 لازم‌الاجراست و هرگز تغییر نمی‌کند.### لاگ جلسه — 2026-09-17
- فاز ۱: tools/ در .gitignore ✔ | check-ignore ✔ | push: 4137b09..ca8e176 ✔ | tools خاکستری ✔
- فاز ۲: status.ps1 → ۱۱ سبز + STUB زنده است ✔ | پرونده مهاجرت URL: بسته
- اقدام واقعی پیدا شده: canonical و og:url صفحه /blog/ نداشت → اضافه و push شد
- بازمانده‌های دست‌نخورده: inventory.json (۱۱۸+/۱۱۸-) | پوشه blog/blog | فایل‌های "index html" و index.html.backup### فاز ۳ — 2026-09-17
- sitemap.xml: resubmit شد
- Request Indexing: ۱۰ URL اولویت‌دار، تاریخ 2026-09-17
- دلایل Not indexed: Discovered 95 | Crawled 21 | Redirect 2 | Duplicate 1 | Alternate 1
- نمونه Discovered: forty-two-years-silence, healing-old-wounds, displaced-jealousy-family-conflict,
  codependency-success-fear.html, modern-tragedy-mother-shadow, untreated-mood-disorder-marriage,
  marital-paranoia, case-safe-cage.html, addictive-mother-controlling-son, triangulation-parentification-child-mediator
- آخرین به‌روزرسانی: 2026-09-17- بنر Validation failed (شروع 9/7، شکست 9/15): مربوط به پیش از اصلاحات امروز؛ اقدام نمی‌خواهد.
- بررسی بعدی گزارش Pages: 2026-09-24 | معیار: کاهش عدد Discovered از 95- قانون تشخیص (افزوده 2026-09-17): «گوگل کارش زمان‌بر است» توضیحِ آخر است، نه اول.
  ترتیب مجاز: ۱) چک‌لیست ایراد خودمان (canonical، ریدایرکت، sitemap، لینک داخلی، duplicate)
  ۲) شمارش‌های گزارش Pages  ۳) تازه بعد «صف/زمان» — آن هم با تاریخ و معیارِ بازبررسی.
  هر «صبر کن» بدون تاریخ و معیار = وعده‌ی شکسته.
- درس ۲۴→۹۵ (به قول مراجع: «اگر به گوگل گوش بدیم زود ایندکس میکنه»):
  پس از اصلاح canonical/ریدایرکت/sitemap در 2026-09، ایندکس از ۲۴ به ۹۵ رسید.
  سرعت، پاداشِ گوش‌دادن به گوگل است، نه پاداشِ شانس.## لاگ جلسه — 2026-09-17 (روز کامل)
- فاز ۱: tools/ در .gitignore ✔ | check-ignore ✔ | status.ps1 v2 ✔ | push ✔
- فاز ۲: ۱۱ سبز + STUB زنده است ✔ | پرونده مهاجرت URL: بسته
- اقدام واقعی: canonical+og:url صفحه /blog/ غایب بود → اضافه و push شد
- فاز ۳: sitemap resubmit ✔ | Request Indexing ده URL ✔ |
  دلایل Not indexed: Discovered 95 | Crawled 21 | Redirect 2 | Duplicate 1 | Alternate 1
- یافته‌ی رأس: صفحات یتیم (Referring page=None)؛ فهرست وبلاگ ۳۰ مقاله را نداشت
- فاز ۴ اجرانشده در برنامه: بازسازی فهرست به ۱۷۷ ورودی (f08c844) +
  پختن canonical در قالب build_blog_index.py | وصله KeyError meta در auto_linker |
  commit ef60706 + push ✔
- بنر Validation failed (شکست 9/15): مربوط به پیش از اصلاحات؛ بدون اقدام
- Request Indexing پنج صفحه‌ی تازه‌لینک‌گرفته: 2026-09-17

## صف وعده‌های جلسه‌ی بعد
- فاز ۰: paste کردن CONTRACT.md و SEO-STATUS.md در چت
- فاز ۱: اجرای status.ps1 (چک سلامت)
- فاز ۲: مسیر نوشتن auto_linker: چرا مقاله‌ها را بازنویسی نکرد؟
  معیار: بعد از اجرا، git status باید M روی blog/*/index.html نشان دهد |
  ممیزی canonical هجده URL با پسوند .html | پوشه blog/blog | آن ۱ URL Duplicate
- فاز ۳: چک هفتگی Pages (معیار: Discovered کمتر از ۹۵) |
  برای پنج URL بالا Referring page = /blog/ (تاریخ معیار: 2026-09-24؛ وگرنه افزودن دستی به sitemap) |
  Request Indexing پنج URL جدید
- فاز ۴: اسکریپت meta description برای همه‌ی کیس‌ها | تنوع اسکلت برای ۲۱ Crawled-not-indexed (دسته‌های ۵-۷)
- آخرین به‌روزرسانی: 2026-09-17