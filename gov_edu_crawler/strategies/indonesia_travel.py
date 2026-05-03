import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class IndonesiaTravelStrategy(BaseStrategy):
    """Strategi scraping untuk www.indonesia.travel (Wonderful Indonesia official)"""
    def __init__(self):
        super().__init__()
        self.selector = "div#article-content"

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        if not container:
            return None

        # Remove media elements
        for tag in container.select('div.tambah-video, img, figure'):
            tag.decompose()

        text_blocks = []
        for el in container.find_all('p'):
            txt = el.get_text(strip=True)
            # Skip empty paragraphs and &nbsp;
            if not txt or txt == '\xa0' or len(txt) < 5:
                continue
            if self.is_junk(txt):
                continue
            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
