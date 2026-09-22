#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_gate.py — فرمانده کل قوا
قبل از هر git push اجرا شود.
اگر حتی یک خطا پیدا شد، اجازه push نمی‌دهد.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BLOG = ROOT / "blog"
ERRORS = []
WARNINGS = []

def error(msg):
    ERRORS.append(msg)
    print(f"  ❌ {msg}")

def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠️  {msg}")

def check_file(filepath):
    # استثنا: blog/index.html صفحه فهرست است
    if filepath.parent.name == "blog" and filepath.name == "index.html":
        print("  ⏭️  (صفحه فهرست — صرف‌نظر)")
        return
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        error(f"خطا در خواندن {filepath.name}: {e}")
        return

    slug = filepath.parent.name

    # ۱. canonical
    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', content)
    if not canonical:
        error(f"{slug}: تگ canonical یافت نشد")
    else:
        expected = f"https://geshpar.com/blog/{slug}/"
        if canonical.group(1) != expected:
            error(f"{slug}: canonical اشتباه است → {canonical.group(1)} (باید: {expected})")

    # ۲. og:url
    og_url = re.search(r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', content)
    if not og_url:
        error(f"{slug}: تگ og:url یافت نشد")
    else:
        expected = f"https://geshpar.com/blog/{slug}/"
        if og_url.group(1) != expected:
            error(f"{slug}: og:url اشتباه است → {og_url.group(1)}")

    # ۳. meta description
    if not re.search(r'<meta[^>]+name=["\']description["\']', content):
        warn(f"{slug}: meta description یافت نشد")

    # ۴. شماره نظام (باید ۲۱۶ یا 2168 باشد)
    nums = re.findall(r'نظام روانشناسی[:::\s]+([۰-۹0-9]+)', content)
    for n in nums:
        if n not in ('۲۱۶۸', '2168'):
            error(f"{slug}: شماره نظام اشتباه ({n}) — باید ۲۱۶۸ باشد")

    # ۵. تاریخ نامعتبر
    if re.search(r'(?<!۲)۰۲۶', content) or re.search(r'(?<!۲)(?<!۰)۰۲(?!۶)(?![۰-۹])', content):
        error(f"{slug}: تاریخ نامعتبر یافت شد (۰۲۶ یا ۰۲۲)")

    # ۶. لینک‌های internal شکسته
    links = re.findall(r'href=["\']/blog/([^"\'/]+)/["\']', content)
    for link_slug in links:
        target = BLOG / link_slug / 'index.html'
        if not target.exists():
            error(f"{slug}: لینک شکسته → /blog/{link_slug}/")

def main():
    print("=" * 55)
    print("  🔍 QUALITY GATE — پارسنگ")
    print("=" * 55)

    if not BLOG.exists():
        error("پوشه blog/ یافت نشد!")
        sys.exit(1)

    files = sorted(BLOG.rglob('index.html'))
    print(f"\n  📄 تعداد مقالات: {len(files)}\n")

    for f in files:
        print(f"  بررسی: {f.parent.name} ...", end=" ")
        before = len(ERRORS)
        check_file(f)
        if len(ERRORS) == before:
            print("✅")
        else:
            print("")

    print("\n" + "=" * 55)
    print(f"  ❌ خطاها:    {len(ERRORS)}")
    print(f"  ⚠️  هشدارها: {len(WARNINGS)}")
    print("=" * 55)

    if ERRORS:
        print("\n  🚫 PUSH ممنوع — اول خطاها را اصلاح کنید.\n")
        sys.exit(1)
    else:
        print("\n  ✅ کیفیت تأیید شد — آماده push هستید.\n")
        sys.exit(0)

if __name__ == "__main__":
    main()