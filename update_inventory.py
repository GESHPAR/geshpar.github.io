import os
import json
from datetime import datetime
from pathlib import Path

def update_inventory():
    blog_path = Path("blog")
    inventory_file = Path("inventory.json")
    
    all_files = []
    duplicates = []
    total_size = 0
    
    for file in blog_path.rglob("*.html"):
        file_size = file.stat().st_size
        total_size += file_size
        
        file_info = {
            "name": file.name,
            "path": str(file),
            "size": f"{file_size} bytes",
            "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "is_duplicate": "Copy" in file.name
        }
        
        all_files.append(file_info)
        
        if file_info["is_duplicate"]:
            duplicates.append(file.name)
    
    inventory = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totalArticles": len(all_files),
        "uniqueArticles": len([f for f in all_files if not f["is_duplicate"]]),
        "duplicateFiles": len(duplicates),
        "totalSize": f"{total_size / 1024:.2f} KB",
        "articles": all_files,
        "duplicates": duplicates,
        "warning": f"⚠️ {len(duplicates)} فایل تکراری پیدا شد!" if duplicates else "✅ هیچ فایل تکراری وجود ندارد"
    }
    
    with open(inventory_file, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(" آمار سایت گشپار")
    print("=" * 60)
    print(f"✅ آخرین به‌روزرسانی: {inventory['lastUpdated']}")
    print(f"📚 کل مقالات: {inventory['totalArticles']}")
    print(f"✨ مقالات یکتا: {inventory['uniqueArticles']}")
    print(f"🔄 فایل‌های تکراری: {inventory['duplicateFiles']}")
    print(f"💾 حجم کل: {inventory['totalSize']}")
    print("=" * 60)
    print(inventory['warning'])
    print("=" * 60)
    
    if duplicates:
        print("\n📋 لیست فایل‌های تکراری:")
        for dup in duplicates:
            print(f"  ❌ {dup}")
    
    print(f"\n✅ فایل inventory.json آپدیت شد!")
    print("=" * 60)

if __name__ == "__main__":
    update_inventory()
