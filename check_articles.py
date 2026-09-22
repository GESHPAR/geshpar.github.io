import os

# تنظیم مسیر هوشمند
if os.path.exists("blog"):
    blog_path = "blog"
elif os.path.exists("../blog"):
    blog_path = "../blog"
else:
    blog_path = None

results = []

if not blog_path:
    print("❌ خطا: پوشه 'blog' یافت نشد.")
else:
    print(f"✅ اسکن شروع شد...\n")
    
    for root, dirs, files in os.walk(blog_path):
        for file in files:
            if file == "index.html":
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        char_count = len(content)
                        slug = os.path.basename(root)
                        
                        status = "✅ OK"
                        if char_count == 0:
                            status = "❌ EMPTY"
                        elif char_count < 1500:
                            status = "⚠️ SHORT"
                        
                        results.append({"slug": slug, "chars": char_count, "status": status})
                except Exception as e:
                    results.append({"slug": os.path.basename(root), "chars": 0, "status": "ERROR"})

    # مرتب‌سازی
    results.sort(key=lambda x: (x["status"] != "❌ EMPTY", x["status"] != "⚠️ SHORT", -x["chars"]))

    print(f"{'وضعیت':<10} | {'کاراکتر':<8} | {'نام مقاله'}")
    print("-" * 60)
    
    empty_count = short_count = ok_count = 0
    
    for item in results:
        print(f"{item['status']:<10} | {item['chars']:<8} | {item['slug']}")
        if "EMPTY" in item['status']: empty_count += 1
        elif "SHORT" in item['status']: short_count += 1
        else: ok_count += 1

    print("-" * 60)
    print(f"\n📊 آمار نهایی:")
    print(f"✅ استاندارد: {ok_count}")
    print(f"⚠️ کوتاه: {short_count}")
    print(f"❌ خالی: {empty_count}")