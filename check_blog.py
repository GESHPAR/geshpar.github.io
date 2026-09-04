import os

print("=== پوشه‌های داخل blog ===")
for name in sorted(os.listdir('blog')):
    path = os.path.join('blog', name)
    if os.path.isdir(path):
        type_mark = "📁 پوشه"
        if name.endswith('.html'):
            type_mark = "⚠️ پوشه با .html"
        print(f"{type_mark}: {name}")
    else:
        print(f"📄 فایل: {name}")