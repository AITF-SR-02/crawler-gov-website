from .base_strategy import BaseStrategy

class KemendikdasmenStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Mapping selector berdasarkan subdomain agar efisien
        self.selectors = {
            "vokasi": "div.entry-content",
            "itjen": "div.entry-content",
            "badanbahasa": "div.article_body_wrap",
            "rumahpusbin": "main#main .container",
            "bskap": 'div[style*="word-break: break-word"]',
            "main": "div.col-12.col-md-8" # Default untuk kemendikdasmen.go.id
        }

    def scrape(self, url, html_content):
        """Menentukan selector berdasarkan subdomain dan mengekstraksi teks."""
        # 1. Identifikasi subdomain dari URL[cite: 1]
        target_selector = self.selectors["main"]
        
        if "vokasi." in url:
            target_selector = self.selectors["vokasi"]
        elif "itjen." in url:
            target_selector = self.selectors["itjen"]
        elif "badanbahasa." in url:
            target_selector = self.selectors["badanbahasa"]
        elif "rumahpusbin." in url:
            target_selector = self.selectors["rumahpusbin"]
        elif "bskap." in url:
            target_selector = self.selectors["bskap"]

        # 2. Ekstraksi teks menggunakan logic universal dari BaseStrategy
        # Itjen butuh elemen li dan blockquote juga
        tags = ['p', 'li', 'blockquote'] if "itjen." in url else ['p']
        
        content = self.extract_clean_text(html_content, target_selector, tags=tags)
        
        # 3. Logika khusus Vokasi: Hapus inisial penulis di akhir[cite: 2]
        if content and "vokasi." in url:
            import re
            content = re.sub(r'\s*\([^)]*\)$', '', content)
            
        return content