import os
import sys

# اضافه کردن مسیر فعلی برای شناسایی فایل‌های هم‌پوشه
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_linker import ContentAutomation
from html_generator import generate_html_from_db

def main():
    print("🚀 شروع فرآیند اتوماسیون گشپار...")
    print("=" * 50)

    # مرحله ۱: تحلیل و لینک‌دهی خودکار
    print("\n1️⃣ مرحله اول: تحلیل و لینک‌دهی خودکار...")
    try:
        bot = ContentAutomation()
        bot.update_all_related_links()
    except Exception as e:
        print(f"❌ خطا در مرحله لینک‌دهی: {e}")
        return

    # مرحله ۲: تولید فایل‌های HTML
    print("\n2️⃣ مرحله دوم: تولید صفحات HTML...")
    try:
        generate_html_from_db()
    except Exception as e:
        print(f"❌ خطا در مرحله تولید HTML: {e}")
        return

    print("\n" + "=" * 50)
    print(" فرآیند اتوماسیون با موفقیت تمام شد!")

if __name__ == "__main__":
    main()
