import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class WonderfulIndonesiaStrategy(BaseStrategy):
    """Strategi scraping untuk wonderfulindonesia.co.id"""
    def __init__(self):
        super().__init__()
        self.selector = "div.post_content.entry-content"

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        if not container:
            return None

        # CRITICAL: Remove hidden spam elements (gambling links etc.)
        for hidden in container.select('div[style*="display:none"], div[style*="display: none"]'):
            hidden.decompose()

        # Remove sidebar and widget elements
        for junk in container.select('div.sidebar, aside.widget, hr.wp-block-separator'):
            junk.decompose()

        text_blocks = []
        for el in container.find_all(['p', 'h2', 'blockquote']):
            txt = el.get_text(strip=True)
            if not txt or txt == '\xa0' or len(txt) < 5:
                continue
            if self.is_junk(txt):
                continue
            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
