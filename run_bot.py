from auto_linker import ContentAutomation
import json

def main():
    bot = ContentAutomation()
    
    print("\n" + "="*40)
    print("🆕 افزودن مقاله جدید به سیستم گشپار")
    print("="*40)
    
    # دریافت اطلاعات از کاربر
    file_name = input("1. نام پوشه مقاله (مثلاً new-case-6): ").strip()
    title = input("2. عنوان کامل مقاله: ").strip()
    
    if not file_name or not title:
        print("❌ خطا: نام و عنوان الزامی است.")
        return

    article_data = {
        "id": file_name,
        "title": title,
        "path": f"/blog/{file_name}/",
        "publish_date": "2026-08-25", # تاریخ امروز
        "status": "draft",
        "keywords": [], # خالی بگذار تا خودش حدس بزند
        "cluster": ""   # خالی بگذار تا خودش حدس بزند
    }
    
    success = bot.add_article(article_data)
    
    if success:
        print("\n" + "="*40)
        print("✅ عملیات موفقیت‌آمیز بود!")
        print("💡 حالا می‌توانید فایل HTML را در پوشه blog بسازید.")
        print("💡 لینک‌های پیشنهادی در دیتابیس ذخیره شدند.")
        print("="*40)
    else:
        print("\n❌ مشکلی پیش آمد.")

if __name__ == "__main__":
    main()
