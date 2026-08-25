import json
import os

def generate_html_from_db(db_file='content-database.json'):
    """خواندن دیتابیس و ساخت فایل‌های HTML برای هر مقاله"""
    
    # خواندن دیتابیس
    with open(db_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ساخت پوشه blog اگر وجود نداشت
    if not os.path.exists('blog'):
        os.makedirs('blog')

    print(f"🏗️ شروع ساخت صفحات برای {len(data['articles'])} مقاله...\n")

    for article in data['articles']:
        # استخراج نام پوشه از path (مثلاً blog/my-article/ -> my-article)
        path = article.get('path', '').strip('/')
        slug = path.split('/')[-1] if '/' in path else path
        
        if not slug: 
            continue

        # ساخت مسیر پوشه مقاله
        article_dir = os.path.join('blog', slug)
        if not os.path.exists(article_dir):
            os.makedirs(article_dir)

        # ساخت محتوای HTML پایه
        html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <link rel="stylesheet" href="/parsang.css">
</head>
<body>
    <header>
        <h1>{article['title']}</h1>
        <p class="meta">خوشه: {article.get('cluster', 'عمومی')} | تاریخ: {article.get('publish_date', '')}</p>
    </header>
    
    <main>
        <div class="content">
            <p>محتوای اصلی مقاله اینجا قرار می‌گیرد...</p>
        </div>

        <!-- بخش لینک‌های مرتبط که توسط auto_linker پر می‌شود -->
        <section class="related-articles">
            <h3>مقالات مرتبط</h3>
            <ul>
"""
        # اضافه کردن لینک‌های مرتبط
        related_ids = article.get('auto_related', [])
        if related_ids:
            for rel_id in related_ids:
                # پیدا کردن مقاله مرتبط برای گرفتن عنوان و مسیر
                rel_article = next((a for a in data['articles'] if a['id'] == rel_id), None)
                if rel_article:
                    html_content += f'                <li><a href="{rel_article["path"]}">{rel_article["title"]}</a></li>\n'
        else:
            html_content += '                <li>مقاله مرتبطی یافت نشد.</li>\n'

        html_content += """            </ul>
        </section>
    </main>
</body>
</html>"""

        # ذخیره فایل HTML
        file_path = os.path.join(article_dir, 'index.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ ساخته شد: {file_path}")

if __name__ == "__main__":
    generate_html_from_db()
