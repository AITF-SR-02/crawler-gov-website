import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class KemenagStrategy(BaseStrategy):
    """Strategi scraping untuk kemenag.go.id"""
    def __init__(self):
        super().__init__()
        self.selector = "div.article-content"

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        if not container:
            return None

        text_blocks = []
        for i, el in enumerate(container.find_all('p')):
            txt = el.get_text(strip=True)
            if not txt or self.is_junk(txt):
                continue

            # Start marker: "Cirebon (Kemenag) ---" → hapus sampai ---
            if i == 0:
                txt = re.sub(r'^.*?-{2,}\s*', '', txt)
                if not txt:
                    continue

            if len(txt) > 5:
                text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
