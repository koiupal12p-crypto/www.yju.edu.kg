import os
import random
import string
import re
from datetime import datetime, timedelta

# ==============================================================================
# GENERATOR PRO - ADVANCED INTERNAL LINKING EDITION
# ==============================================================================
# - Absolute internal links (SEO safe)
# - Chain Linking Strategy: Connects Prev/Next pages
# - Cluster boost: Links within same folder
# - Domain auto-detected from CNAME
# - GitHub Actions optimized
# ==============================================================================

class ContinuousGenerator:
    def __init__(self):
        self.templates = {}
        self.template_names = ["test.html", "test1.html", "test2.html"]
        self.keywords_ar = []
        self.keywords_en = []
        self.max_files_per_folder = 500
        self.emojis = ["🔥", "🎥", "🔞", "😱", "✅", "🌟", "📺", "🎬", "✨", "💎", "⚡"]

        self.load_all_templates()
        self.load_keywords()
        self.domain = self.load_domain()

    def load_all_templates(self):
        for t_name in self.template_names:
            if os.path.exists(t_name):
                with open(t_name, "r", encoding="utf-8") as f:
                    self.templates[t_name] = f.read()
                print(f"[*] Template {t_name} loaded.")
            else:
                self.templates[t_name] = (
                    "<html><head>"
                    "<title>{{TITLE}}</title>"
                    "<link rel='canonical' href='{{CANONICAL_URL}}'>"
                    "</head><body>"
                    "<h1>{{TITLE}}</h1>"
                    "<p>{{DESCRIPTION}}</p>"
                    "{{INTERNAL_LINKS}}"
                    "</body></html>"
                )
                print(f"[!] {t_name} not found. Using fallback template.")

    def load_keywords(self):
        if os.path.exists("keywords_ar.txt"):
            with open("keywords_ar.txt", "r", encoding="utf-8") as f:
                self.keywords_ar = [l.strip() for l in f if l.strip()]
        if os.path.exists("keywords_en.txt"):
            with open("keywords_en.txt", "r", encoding="utf-8") as f:
                self.keywords_en = [l.strip() for l in f if l.strip()]

        if not self.keywords_ar: self.keywords_ar = ["محتوى", "تقني"]
        if not self.keywords_en: self.keywords_en = ["tech", "update"]

    def load_domain(self):
        if os.path.exists("CNAME"):
            with open("CNAME", "r", encoding="utf-8") as f:
                domain = f.read().strip()
                return domain.replace("https://", "").replace("http://", "")
        return "example.com"

    def build_text(self, min_words, max_words, mode="ar"):
        target_length = random.randint(min_words, max_words)
        source = self.keywords_ar if mode == "ar" else self.keywords_en
        words = []
        while len(words) < target_length:
            words.extend(random.choice(source).split())
        return " ".join(words[:target_length])

    def get_target_path(self, total_count):
        paths = []
        files_remaining = total_count
        while files_remaining > 0:
            d1 = ''.join(random.choices(string.ascii_lowercase, k=3))
            d2 = ''.join(random.choices(string.ascii_lowercase, k=3))
            full_path = os.path.join(d1, d2)
            os.makedirs(full_path, exist_ok=True)
            paths.append(full_path)
            files_remaining -= self.max_files_per_folder
        return paths

    def build_internal_links(self, current_index, generated_files):
        """
        تبني الروابط بنظام السلسلة (Chain) + العناقيد (Clusters)
        """
        current_file = generated_files[current_index]
        current_folder = current_file["folder"]
        
        selected_links = []
        
        # 1. نظام السلسلة: ربط بالصفحة السابقة والتالية
        if current_index > 0:
            selected_links.append(generated_files[current_index - 1])
        if current_index < len(generated_files) - 1:
            selected_links.append(generated_files[current_index + 1])

        # 2. روابط من نفس المجلد (تقوية السيو الموضعي)
        same_folder = [f for idx, f in enumerate(generated_files) 
                       if f["folder"] == current_folder and idx != current_index]
        random.shuffle(same_folder)
        selected_links.extend(same_folder[:5])

        # 3. روابط عشوائية من مجلدات أخرى (زيادة العمق)
        other_folders = [f for f in generated_files if f["folder"] != current_folder]
        random.shuffle(other_folders)
        selected_links.extend(other_folders[:3])

        links_html = (
            "<div class='internal-links' style='margin-top:40px; border-top:1px solid #ddd; padding-top:20px;'>"
            "<h3>مواضيع قد تهمك:</h3><ul>"
        )
        
        # إزالة التكرار والحفاظ على الترتيب
        seen_urls = set()
        for link in selected_links:
            url = f"https://{self.domain}/{link['folder']}/{link['filename']}"
            if url not in seen_urls:
                links_html += f"<li><a href='{url}'>{link['display_title']}</a></li>"
                seen_urls.add(url)

        links_html += "</ul></div>"
        return links_html

    def run_single_cycle(self, count=100):
        folder_paths = self.get_target_path(count)
        generated_files = []
        base_time = datetime.utcnow()

        # المرحلة الأولى: تجهيز البيانات في الذاكرة لتمكين الربط التبادلي
        files_to_create = []
        for folder in folder_paths:
            num_in_folder = min(count, self.max_files_per_folder)
            for _ in range(num_in_folder):
                title_text = self.build_text(5, 10)
                display_title = f"{random.choice(self.emojis)} {title_text} {random.choice(self.emojis)}"
                clean_name = re.sub(r'[^\w\s-]', '', title_text.lower())
                slug = re.sub(r'[-\s]+', '-', clean_name).strip('-')[:80]
                if not slug: slug = ''.join(random.choices(string.ascii_lowercase, k=10))

                files_to_create.append({
                    "display_title": display_title,
                    "filename": f"{slug}.html",
                    "desc": self.build_text(120, 220),
                    "folder": folder,
                    "date_iso": base_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "template": random.choice(self.template_names)
                })

        # المرحلة الثانية: الكتابة الفعلية مع بناء الروابط
        for i, file_data in enumerate(files_to_create):
            template_content = self.templates.get(file_data['template'], "")
            canonical_url = f"https://{self.domain}/{file_data['folder']}/{file_data['filename']}"
            
            # بناء الروابط الذكية
            internal_links = self.build_internal_links(i, files_to_create)

            content = template_content
            content = content.replace("{{TITLE}}", file_data['display_title'])
            content = content.replace("{{DESCRIPTION}}", file_data['desc'])
            content = content.replace("{{CANONICAL_URL}}", canonical_url)
            content = content.replace("{{INTERNAL_LINKS}}", internal_links)
            content = content.replace("{{DOMAIN_NAME}}", self.domain)
            # لدعم التنسيق في القوالب الطبية أو الفيديو
            content = content.replace("{{DATE}}", file_data['date_iso'])

            target_file = os.path.join(file_data['folder'], file_data['filename'])
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✅ Successfully generated {len(files_to_create)} pages with Chain Linking.")

if __name__ == "__main__":
    generator = ContinuousGenerator()
    generator.run_single_cycle(count=150) # عدد الصفحات في كل دورة (15 دقيقة)