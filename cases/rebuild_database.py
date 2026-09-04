# -*- coding: utf-8 -*-
# rebuild_database.py
# بازسازی کامل دیتابیس از صفر

import json
import os
from pathlib import Path
from datetime import datetime

def scan_all_content():
    """اسکن تمام محتوای سایت"""
    content_items = []
    
    # اسکن پوشه‌های مختلف
    directories = ['cases', 'blog', 'guides', 'contact']
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            continue
            
        for html_file in dir_path.glob('**/*.html'):
            item = process_content_file(html_file, dir_name)
            if item:
                content_items.append(item)
    
    return content_items

def process_content_file(file_path, category):
    """پردازش یک فایل محتوا"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "slug": file_path.stem,
            "path": str(file_path.relative_to(Path.cwd())),
            "title": extract_title(content),
            "description": extract_description(content),
            "category": category,
            "tags": extract_tags(content),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "internal_links": extract_internal_links(content),
            "status": "published",
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
    except Exception as e:
        print(f"خطا در پردازش {file_path}: {e}")
        return None

def extract_title(content):
    import re
    match = re.search(r'<title>(.*?)</title>', content)
    return match.group(1) if match else "عنوان نامشخص"

def extract_description(content):
    import re
    match = re.search(r'<meta name="description" content="(.*?)"', content)
    return match.group(1) if match else ""

def extract_tags(content):
    import re
    match = re.search(r'"tags":\s*\[(.*?)\]', content)
    if match:
        tags_str = match.group(1)
        return [tag.strip().strip('"\'') for tag in tags_str.split(',')]
    return []

def extract_internal_links(content):
    import re
    links = re.findall(r'href=["\'](/[^"\']+?)["\']', content)
    return list(set(links))

def main():
    print("🔄 شروع بازسازی کامل دیتابیس...")
    
    content_items = scan_all_content()
    
    # ذخیره دیتابیس
    db_path = Path('content-database.json')
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(content_items, f, ensure_ascii=False, indent=2)
    
    print(f"✅ دیتابیس با موفقیت بازسازی شد")
    print(f"📊 تعداد کل آیتم‌ها: {len(content_items)}")
    
    # نمایش آمار بر اساس دسته‌بندی
    categories = {}
    for item in content_items:
        cat = item.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📈 آمار بر اساس دسته‌بندی:")
    for cat, count in categories.items():
        print(f"   {cat}: {count}")

if __name__ == "__main__":
    main()