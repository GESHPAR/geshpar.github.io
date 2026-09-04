# -*- coding: utf-8 -*-
# validate_database.py
# اعتبارسنجی دیتابیس پس از اضافه کردن کیس‌ها

import json
from pathlib import Path

def validate_database():
    """اعتبارسنجی کامل دیتابیس"""
    db_path = Path('content-database.json')
    
    if not db_path.exists():
        print("❌ دیتابیس یافت نشد!")
        return False
    
    with open(db_path, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    errors = []
    warnings = []
    
    required_fields = ['slug', 'path', 'title', 'category', 'date']
    
    for i, entry in enumerate(database):
        # بررسی فیلدهای الزامی
        for field in required_fields:
            if field not in entry:
                errors.append(f"ورودی {i+1}: فیلد '{field}' مفقود است")
        
        # بررسی وجود فایل
        if 'path' in entry:
            file_path = Path(entry['path'])
            if not file_path.exists():
                errors.append(f"ورودی {entry.get('slug', i+1)}: فایل '{entry['path']}' یافت نشد")
        
        # بررسی یکتایی slug
        slug = entry.get('slug')
        if slug:
            count = sum(1 for e in database if e.get('slug') == slug)
            if count > 1:
                warnings.append(f"Slug تکراری: '{slug}' ({count} بار)")
    
    # گزارش نتایج
    print("🔍 گزارش اعتبارسنجی دیتابیس:")
    print("="*50)
    
    if errors:
        print(f"❌ {len(errors)} خطا یافت شد:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ هیچ خطایی یافت نشد")
    
    if warnings:
        print(f"⚠️ {len(warnings)} هشدار یافت شد:")
        for warning in warnings:
            print(f"   - {warning}")
    else:
        print("✅ هیچ هشداری یافت نشد")
    
    print(f"📊 کل ورودی‌ها: {len(database)}")
    print("="*50)
    
    return len(errors) == 0

if __name__ == "__main__":
    is_valid = validate_database()
    exit(0 if is_valid else 1)