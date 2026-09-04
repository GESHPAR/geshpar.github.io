# -*- coding: utf-8 -*-
# batch_add_cases.py
# اسکریپت اضافه کردن همه کیس‌ها به دیتابیس به صورت دسته‌ای

import json
import os
from pathlib import Path
from datetime import datetime

def load_existing_database():
    """بارگذاری دیتابیس موجود"""
    db_path = Path('content-database.json')
    if db_path.exists():
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_database(database):
    """ذخیره دیتابیس"""
    db_path = Path('content-database.json')
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

def process_case_file(case_file):
    """پردازش یک فایل کیس و استخراج اطلاعات"""
    try:
        with open(case_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # استخراج اطلاعات از فایل HTML
        title = extract_title(content)
        description = extract_description(content)
        tags = extract_tags(content)
        category = extract_category(case_file)
        
        return {
            "slug": case_file.stem,
            "path": str(case_file.relative_to(Path.cwd())),
            "title": title,
            "description": description,
            "category": category,
            "tags": tags,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "internal_links": extract_internal_links(content),
            "status": "published"
        }
    except Exception as e:
        print(f"❌ خطا در پردازش {case_file}: {e}")
        return None

def extract_title(content):
    """استخراج عنوان از محتوا"""
    import re
    match = re.search(r'<title>(.*?)</title>', content)
    return match.group(1) if match else "عنوان نامشخص"

def extract_description(content):
    """استخراج توضیحات از متاتگ"""
    import re
    match = re.search(r'<meta name="description" content="(.*?)"', content)
    return match.group(1) if match else ""

def extract_tags(content):
    """استخراج تگ‌ها از محتوا"""
    import re
    match = re.search(r'"tags":\s*\[(.*?)\]', content)
    if match:
        tags_str = match.group(1)
        return [tag.strip().strip('"\'') for tag in tags_str.split(',')]
    return []

def extract_category(file_path):
    """استخراج دسته‌بندی از مسیر فایل"""
    parts = file_path.parts
    if 'cases' in parts:
        return 'cases'
    elif 'blog' in parts:
        return 'blog'
    elif 'guides' in parts:
        return 'guides'
    return 'general'

def extract_internal_links(content):
    """استخراج لینک‌های داخلی از محتوا"""
    import re
    links = re.findall(r'href=["\'](/[^"\']+?)["\']', content)
    return list(set(links))  # حذف تکراری‌ها

def main():
    print("🚀 شروع پردازش دسته‌ای کیس‌ها...")
    
    # بارگذاری دیتابیس موجود
    database = load_existing_database()
    existing_slugs = {item['slug'] for item in database}
    
    # پیدا کردن تمام فایل‌های HTML در پوشه cases
    cases_dir = Path('cases')
    if not cases_dir.exists():
        print("❌ پوشه cases یافت نشد!")
        return
    
    html_files = list(cases_dir.glob('*.html'))
    print(f"📁 {len(html_files)} فایل کیس یافت شد")
    
    new_entries = 0
    updated_entries = 0
    
    for case_file in html_files:
        print(f"🔄 پردازش: {case_file.name}")
        
        case_data = process_case_file(case_file)
        if not case_data:
            continue
        
        slug = case_data['slug']
        
        # بررسی وجود قبلی
        existing_entry = next((item for item in database if item['slug'] == slug), None)
        
        if existing_entry:
            # آپدیت ورودی موجود
            existing_entry.update(case_data)
            updated_entries += 1
            print(f"✅ آپدیت شد: {slug}")
        else:
            # افزودن ورودی جدید
            database.append(case_data)
            new_entries += 1
            print(f"✅ اضافه شد: {slug}")
    
    # ذخیره دیتابیس
    save_database(database)
    
    print("\n" + "="*50)
    print(f"📊 آمار نهایی:")
    print(f"   ✅ موارد جدید: {new_entries}")
    print(f"   🔄 موارد آپدیت شده: {updated_entries}")
    print(f"   📈 کل موارد در دیتابیس: {len(database)}")
    print("="*50)

if __name__ == "__main__":
    main()