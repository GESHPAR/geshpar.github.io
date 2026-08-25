import json
import os

class ContentAutomation:
    def __init__(self):
        self.db_file = 'content-database.json'
        self.load_database()
    
    def load_database(self):
        if not os.path.exists(self.db_file):
            print("❌ فایل دیتابیس پیدا نشد!")
            self.data = {"articles": [], "linking_rules": {"max_internal_links": 6}}
            return
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ دیتابیس بارگذاری شد: {len(self.data['articles'])} مقاله")
        except Exception as e:
            print(f"❌ خطا: {e}")
            self.data = {"articles": [], "linking_rules": {"max_internal_links": 6}}

    def add_article(self, article_data):
        article_id = article_data['id']
        
        # بررسی تکراری نبودن
        if any(a['id'] == article_id for a in self.data['articles']):
            print(f"⚠️ مقاله {article_id} قبلاً وجود دارد!")
            return False
        
        # یافتن مقالات مرتبط
        related_articles = self.find_related_articles(article_data)
        
        self.data['articles'].append(article_data)
        self.save_database()
        
        print(f"\n✅ مقاله '{article_data['title']}' اضافه شد!")
        print(f"🔗 {len(related_articles)} مقاله مرتبط پیدا شد:")
        for rel_id in related_articles:
            rel_art = next((a for a in self.data['articles'] if a['id'] == rel_id), None)
            if rel_art:
                print(f"   - {rel_art['title']}")
        
        return True

    def find_related_articles(self, new_article):
        related = []
        new_tags = set(new_article.get('tags', []))
        
        for article in self.data['articles']:
            if article['id'] == new_article['id']:
                continue
            
            article_tags = set(article.get('tags', []))
            overlap = len(new_tags & article_tags)
            
            if overlap > 0:
                related.append((article['id'], overlap))
        
        related.sort(key=lambda x: x[1], reverse=True)
        max_links = self.data.get('linking_rules', {}).get('max_internal_links', 6)
        return [r[0] for r in related[:max_links]]

    def save_database(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def show_all_articles(self):
        print(f"\n📊 لیست تمام مقالات ({len(self.data['articles'])} مقاله):")
        for i, article in enumerate(self.data['articles'], 1):
            print(f"{i}. {article['title']}")
            print(f"   تگ‌ها: {', '.join(article.get('tags', []))}")

if __name__ == "__main__":
    bot = ContentAutomation()
    bot.show_all_articles()
