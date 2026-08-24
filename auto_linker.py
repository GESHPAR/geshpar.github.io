import json
import re
from difflib import SequenceMatcher
from datetime import datetime
import os

class ContentAutomation:
    def __init__(self):
        self.db_file = 'content-database.json'
        self.load_database()
    
    def load_database(self):
        if not os.path.exists(self.db_file):
            print("❌ فایل دیتابیس پیدا نشد! لطفاً ابتدا content-database.json را بسازید.")
            return
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"❌ خطا در خواندن دیتابیس: {e}")
            self.data = {"articles": [], "clusters": {}, "linking_rules": {}}

    def add_article(self, article_data):
        article_id = article_data['id']
        
        # بررسی تکراری نبودن
        if any(a['id'] == article_id for a in self.data['articles']):
            print(f"⚠️ مقاله {article_id} قبلاً وجود دارد!")
            return False
        
        # تحلیل خودکار کلمات کلیدی اگر ارائه نشده
        if 'keywords' not in article_data or not article_data['keywords']:
            article_data['keywords'] = self.extract_keywords(article_data['title'])
            print(f"🔑 کلمات کلیدی پیشنهادی: {', '.join(article_data['keywords'])}")
        
        # تعیین خوشه
        if 'cluster' not in article_data:
            article_data['cluster'] = self.assign_cluster(article_data['keywords'])
            print(f" خوشه پیشنهادی: {article_data['cluster']}")
        
        # یافتن مقالات مرتبط
        related_articles = self.find_related_articles(article_data)
        article_data['auto_related'] = related_articles
        
        self.data['articles'].append(article_data)
        
        # آپدیت خوشه‌ها
        cluster = article_data['cluster']
        if cluster not in self.data['clusters']:
            self.data['clusters'][cluster] = []
        self.data['clusters'][cluster].append(article_id)
        
        self.save_database()
        
        print(f"\n✅ مقاله '{article_data['title']}' اضافه شد!")
        print(f"🔗 لینک‌های هوشمند پیشنهادی:")
        for rel_id in related_articles:
            rel_art = next((a for a in self.data['articles'] if a['id'] == rel_id), None)
            if rel_art:
                print(f"   - {rel_art['title']}")
        
        return True
    
    def extract_keywords(self, title):
        stop_words = ['وقتی', 'که', 'در', 'با', 'از', 'به', 'و', 'یا', 'اما', 'ولی', 'یک', 'را', 'می', 'است', 'شود']
        words = re.findall(r'[\u0600-\u06FF]+', title) # فقط حروف فارسی
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords[:5]
    
    def assign_cluster(self, keywords):
        cluster_mapping = {
            'تروما و اضطراب': ['خشونت', 'تروما', 'اضطراب', 'ترس', 'فرار', 'پارانویا'],
            'وسواس و اضطراب': ['وسواس', 'نشخوار', 'فکری', 'خیانت', 'شک', 'ذهن'],
            'روابط و خانواده': ['ازدواج', 'همسر', 'خانواده', 'رابطه', 'تحقیر', 'مرز', 'طلاق'],
            'رشد شخصی': ['رشد', 'توسعه', 'خودشناسی', 'اعتماد', 'موفقیت'],
            'سلامت روان': ['افسردگی', 'استرس', 'سلامت', 'روان', 'درمان']
        }
        
        scores = {}
        for cluster, c_keywords in cluster_mapping.items():
            score = sum(1 for kw in keywords if any(ckw in kw for ckw in c_keywords))
            scores[cluster] = score
        
        best_cluster = max(scores, key=scores.get)
        return best_cluster if scores[best_cluster] > 0 else 'عمومی'
    
    def find_related_articles(self, new_article):
        related = []
        rules = self.data.get('linking_rules', {})
        
        for article in self.data['articles']:
            if article['id'] == new_article['id']:
                continue
            
            score = 0
            
            # امتیاز خوشه مشترک
            if article.get('cluster') == new_article.get('cluster'):
                score += rules.get('same_cluster_priority', 0.8)
            
            # امتیاز کلمات کلیدی مشترک
            keyword_overlap = len(set(article.get('keywords', [])) & set(new_article.get('keywords', [])))
            if keyword_overlap >= rules.get('keyword_overlap_min', 1):
                score += (keyword_overlap / 5) * 0.5
            
            # امتیاز شباهت عنوان
            title_sim = SequenceMatcher(None, new_article['title'], article['title']).ratio()
            score += title_sim * 0.3
            
            if score >= rules.get('min_similarity_score', 0.5):
                related.append((article['id'], score))
        
        related.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in related[:rules.get('max_links_per_article', 3)]]
    
    def save_database(self):
        self.data['meta']['last_updated'] = datetime.now().isoformat()
        self.data['meta']['total_articles'] = len(self.data['articles'])
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    bot = ContentAutomation()
    print("🤖 سیستم اتوماسیون گشپار آماده است.")
    print("برای تست، یک مقاله جدید در فایل JSON اضافه کنید یا کد را توسعه دهید.")
