import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class LpdpStrategy(BaseStrategy):
    """Strategi scraping untuk lpdp.kemenkeu.go.id"""
    def __init__(self):
        super().__init__()

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')

        # Content is inside <article> tag
        container = soup.find('article')
        if not container:
            return None

        text_blocks = []
        junk_keywords = ["Nikmati berbagai konten", "inbox kamu", "Selengkapnya",
                         "Gedung Danadyaksa", "Website Kementerian", "bantuan.lpdp",
                         "Customer Service", "Pengaduan"]

        for i, el in enumerate(container.find_all('p')):
            txt = el.get_text(strip=True)
            if not txt or len(txt) < 10:
                continue
            if any(junk in txt for junk in junk_keywords):
                continue
            if self.is_junk(txt):
                continue

            # Start marker: "Cikarang, 14 April 2026 -"
            if i == 0:
                txt = re.sub(r'^.*?[\-\u2013\u2014]\s*', '', txt)
                if not txt:
                    continue

            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
