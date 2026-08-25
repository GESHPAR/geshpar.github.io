import json
import os

class ContentAutomation:
    def __init__(self):
        self.db_file = 'content-database.json'
        self.load_database()
    
    def load_database(self):
        if not os.path.exists(self.db_file):
            print(" فایل دیتابیس پیدا نشد!")
            self.data = {"articles": [], "clusters": {}, "linking_rules": {}}
            return
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ دیتابیس بارگذاری شد: {len(self.data['articles'])} مقاله")
        except Exception as e:
            print(f"❌ خطا: {e}")
            self.data = {"articles": [], "clusters": {}, "linking_rules": {}}

    def find_related_articles(self, article_id):
        """پیدا کردن مقالات مرتبط بر اساس خوشه و کلمات کلیدی"""
        current = next((a for a in self.data['articles'] if a['id'] == article_id), None)
        if not current:
            return []
        
        related = []
        current_cluster = current.get('cluster', '')
        current_keywords = set(current.get('keywords', []))
        rules = self.data.get('linking_rules', {})
        
        for article in self.data['articles']:
            if article['id'] == article_id:
                continue
            
            score = 0
            
            # امتیاز خوشه مشترک
            if article.get('cluster') == current_cluster:
                score += rules.get('same_cluster_priority', 0.8)
            
            # امتیاز کلمات کلیدی مشترک
            article_keywords = set(article.get('keywords', []))
            overlap = len(current_keywords & article_keywords)
            if overlap >= rules.get('keyword_overlap_min', 1):
                score += overlap * 0.3
            
            if score >= rules.get('min_similarity_score', 0.5):
                related.append((article['id'], score))
        
        related.sort(key=lambda x: x[1], reverse=True)
        max_links = rules.get('max_links_per_article', 3)
        return [r[0] for r in related[:max_links]]

    def update_all_related_links(self):
        """آپدیت لینک‌های مرتبط برای همه مقالات"""
        print("\n🔄 آپدیت لینک‌های مرتبط برای همه مقالات...\n")
        
        for article in self.data['articles']:
            related = self.find_related_articles(article['id'])
            article['auto_related'] = related
            
            print(f"📄 {article['title']}")
            if related:
                for rel_id in related:
                    rel_art = next((a for a in self.data['articles'] if a['id'] == rel_id), None)
                    if rel_art:
                        print(f"   🔗 {rel_art['title']}")
            else:
                print("   (بدون مقاله مرتبط)")
            print()
        
        # ذخیره
        self.data['meta']['total_articles'] = len(self.data['articles'])
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print("✅ دیتابیس ذخیره شد!")

    def show_all_articles(self):
        print(f"\n📊 لیست تمام مقالات ({len(self.data['articles'])} مقاله):")
        for i, article in enumerate(self.data['articles'], 1):
            print(f"{i}. {article['title']}")
            print(f"   خوشه: {article.get('cluster', 'نامشخص')}")
            print(f"   کلمات کلیدی: {', '.join(article.get('keywords', []))}")

if __name__ == "__main__":
    bot = ContentAutomation()
    bot.show_all_articles()
    print("\n" + "="*60)
    bot.update_all_related_links()
    
