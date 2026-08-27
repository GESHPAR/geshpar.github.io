import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def create_backup():
    """ایجاد backup از فایل‌های تکراری قبل از حذف"""
    backup_dir = Path("backup_cleanup") / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"📦 پوشه backup ایجاد شد: {backup_dir}")
    return backup_dir

def find_duplicates():
    """پیدا کردن تمام فایل‌های تکراری"""
    blog_path = Path("blog")
    duplicates = []
    
    for file in blog_path.rglob("*.html"):
        if "Copy" in file.name or "copy" in file.name:
            duplicates.append(file)
    
    return duplicates

def cleanup_duplicates(backup_dir):
    """حذف فایل‌های تکراری با backup"""
    duplicates = find_duplicates()
    
    if not duplicates:
        print("✅ هیچ فایل تکراری پیدا نشد!")
        return 0, 0
    
    print(f"\n🔍 {len(duplicates)} فایل تکراری پیدا شد:")
    print("=" * 60)
    
    deleted_count = 0
    backup_count = 0
    
    for dup_file in duplicates:
        try:
            # کپی به backup
            backup_path = backup_dir / dup_file.name
            shutil.copy2(dup_file, backup_path)
            backup_count += 1
            
            # حذف فایل اصلی
            dup_file.unlink()
            deleted_count += 1
            
            print(f"✅ حذف شد: {dup_file.name}")
            
        except Exception as e:
            print(f"❌ خطا در حذف {dup_file.name}: {e}")
    
    return deleted_count, backup_count

def update_inventory_after_cleanup():
    """آپدیت inventory.json بعد از cleanup"""
    blog_path = Path("blog")
    inventory_file = Path("inventory.json")
    
    all_files = []
    total_size = 0
    
    for file in blog_path.rglob("*.html"):
        file_size = file.stat().st_size
        total_size += file_size
        
        file_info = {
            "name": file.name,
            "path": str(file),
            "size": f"{file_size} bytes",
            "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        }
        all_files.append(file_info)
    
    inventory = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totalArticles": len(all_files),
        "totalSize": f"{total_size / 1024:.2f} KB",
        "articles": all_files,
        "cleanupNote": "فایل‌های تکراری حذف شدند"
    }
    
    with open(inventory_file, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

def generate_report(deleted_count, backup_count, backup_dir):
    """تولید گزارش cleanup"""
    report_file = Path("cleanup_report.txt")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("📊 گزارش Cleanup فایل‌های تکراری\n")
        f.write("=" * 60 + "\n")
        f.write(f" تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f" فایل‌های حذف شده: {deleted_count}\n")
        f.write(f" فایل‌های backup شده: {backup_count}\n")
        f.write(f" مسیر backup: {backup_dir}\n")
        f.write("=" * 60 + "\n")
        f.write("✅ Cleanup با موفقیت انجام شد!\n")
    
    print(f"\n📄 گزارش در فایل {report_file} ذخیره شد")

def main():
    print("=" * 60)
    print("🧹 شروع Cleanup خودکار فایل‌های تکراری")
    print("=" * 60)
    
    # ایجاد backup
    backup_dir = create_backup()
    
    # حذف فایل‌های تکراری
    deleted_count, backup_count = cleanup_duplicates(backup_dir)
    
    # آپدیت inventory
    if deleted_count > 0:
        update_inventory_after_cleanup()
        print("\n✅ فایل inventory.json آپدیت شد")
    
    # تولید گزارش
    if deleted_count > 0:
        generate_report(deleted_count, backup_count, backup_dir)
    
    print("\n" + "=" * 60)
    print("✨ Cleanup با موفقیت انجام شد!")
    print("=" * 60)

if __name__ == "__main__":
    main()