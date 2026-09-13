import os
import shutil
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(ROOT, "blog")

print("=== مرحله ۱: شناسایی duplicate ها ===")

# پیدا کردن پوشه‌های تکراری (slug/ و slug.html/)
duplicates_to_delete = []
for item in os.listdir(BLOG):
    if item.endswith('.html') and not item.endswith('.html.html'):
        # مثلاً family-boundaries.html
        base_name = item.replace('.html', '')
        # بررسی آیا پوشه بدون .html وجود دارد؟
        folder_path = os.path.join(BLOG, base_name)
        if os.path.isdir(folder_path):
            print(f"  ✓ Duplicate یافت شد: {item} ← حذف می‌شود (نسخه صحیح: {base_name}/)")
            duplicates_to_delete.append(item)

print(f"\n=== مرحله ۲: شناسایی صفحات 'در حال انتقال' ===")

thin_pages_to_delete = []
for item in os.listdir(BLOG):
    item_path = os.path.join(BLOG, item)
    
    # اگر پوشه است و index.html دارد
    if os.path.isdir(item_path):
        index_path = os.path.join(item_path, "index.html")
        if os.path.isfile(index_path):
            content = open(index_path, encoding='utf-8').read()
            # بررسی آیا محتوای واقعی دارد یا فقط redirect است
            if "در حال انتقال" in content or "انتقال به نشانی جدید" in content:
                # بررسی اینکه آیا نسخه اصلی بدون redirect وجود دارد
                # اگر این خودش redirect است و محتوای واقعی ندارد → حذف
                if len(content) < 500:  # صفحات redirect معمولاً کوچک هستند
                    print(f"  ✓ Thin page: {item}/ ← حذف می‌شود")
                    thin_pages_to_delete.append(item)

print(f"\n=== مرحله ۳: حذف فایل‌ها ===")

# حذف duplicate های .html/
for dup in duplicates_to_delete:
    dup_path = os.path.join(BLOG, dup)
    if os.path.isfile(dup_path):
        os.remove(dup_path)
        print(f"  ✓ حذف شد: {dup}")

# حذف thin pages
for thin in thin_pages_to_delete:
    thin_path = os.path.join(BLOG, thin)
    if os.path.isdir(thin_path):
        shutil.rmtree(thin_path)
        print(f"  ✓ حذف شد: {thin}/")

print(f"\n=== خلاصه ===")
print(f"  Duplicate های حذف‌شده: {len(duplicates_to_delete)}")
print(f"  Thin pages حذف‌شده: {len(thin_pages_to_delete)}")
print(f"\n⚠️  حالا باید sitemap.xml را دستی ویرایش کنی و این آدرس‌ها را حذف کنی")