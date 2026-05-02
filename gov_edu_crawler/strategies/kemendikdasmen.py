import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class KemendikdasmenStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.selectors = {
            "vokasi": "div.entry-content",
            "itjen": "div.entry-content",
            "badanbahasa": "div.article_body_wrap",
            "rumahpusbin": "main#main .container",
            "bskap": 'div.col-xl-6 div[style*="word-break: break-word"]',
            "main": "div.col-12.col-md-8"
        }

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        
        if "vokasi." in url: container = soup.select_one(self.selectors["vokasi"])
        elif "itjen." in url: container = soup.select_one(self.selectors["itjen"])
        elif "badanbahasa." in url: container = soup.select_one(self.selectors["badanbahasa"])
        elif "rumahpusbin." in url: container = soup.select_one(self.selectors["rumahpusbin"])
        elif "bskap." in url: container = soup.select_one(self.selectors["bskap"])
        else: container = soup.select_one(self.selectors["main"])

        if not container: return None

        text_blocks = []
        is_main = not any(sub in url for sub in ["vokasi.", "itjen.", "badanbahasa.", "rumahpusbin.", "bskap."])
        
        if is_main:
            for s in container.find_all('strong'):
                s.decompose()
            elements_text = container.get_text(separator='\n', strip=True).split('\n')
        else:
            tags = ['p', 'li', 'blockquote'] if "itjen." in url else ['p']
            elements_text = [el.get_text(strip=True) for el in container.find_all(tags) if not el.find('img')]
            
        junk_keywords = ["Biro Komunikasi", "Laman:", "X:", "Instagram:", "#"]

        for i, txt in enumerate(elements_text):
            txt = txt.strip()
            # Better footer filtering
            if any(txt.startswith(x) for x in ["Sumber:", "Penulis:", "Editor:"]): continue
            if "BKHM" in txt or any(junk in txt for junk in junk_keywords) or not txt: continue
            
            if i <= 1: 
                txt = re.sub(r'^.*?[—–-]\s*', '', txt)
                txt = re.sub(r'^[–\-\s]+', '', txt)

            if not is_main and i == len(elements_text) - 1 and "vokasi." in url:
                txt = re.sub(r'\s*\([^)]*\)$', '', txt)

            if len(txt) > 5: text_blocks.append(txt)

        return "\n\n".join(text_blocks)