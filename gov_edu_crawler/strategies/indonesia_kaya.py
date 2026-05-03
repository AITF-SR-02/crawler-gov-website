import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class IndonesiaKayaStrategy(BaseStrategy):
    """Strategi scraping untuk indonesiakaya.com"""
    def __init__(self):
        super().__init__()
        self.selector = "div#main-content"
        self.junk_selectors = [
            "div#main-gallery",
            "div.baca-juga",
            "div.artikel-terkait",
            "div.infoMore",
        ]

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        if not container:
            return None

        # Remove junk elements before extracting text
        for sel in self.junk_selectors:
            for junk in container.select(sel):
                junk.decompose()

        text_blocks = []
        for el in container.find_all(['p', 'blockquote']):
            if el.find('img'):
                continue
            txt = el.get_text(strip=True)
            if not txt or self.is_junk(txt) or len(txt) < 10:
                continue
            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
