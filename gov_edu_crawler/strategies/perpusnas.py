import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class PerpusnasStrategy(BaseStrategy):
    """Strategi scraping untuk perpusnas.go.id"""
    def __init__(self):
        super().__init__()
        self.selector = "div.entry-content"
        # Start marker: "[Daerah] - Humas Perpusnas,"
        self.start_pattern = re.compile(r'^.*?\-\s*Humas Perpusnas,\s*', re.IGNORECASE)
        # End marker: "*** (AKN/Ed:DRS/Dok:PHP)"
        self.end_pattern = re.compile(r'\s*\*{3}\s*\(.*?\)\s*$')

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        if not container:
            return None

        text_blocks = []
        elements = container.find_all('p')
        for i, el in enumerate(elements):
            txt = el.get_text(strip=True)
            if not txt or self.is_junk(txt):
                continue

            # Clean start marker on first paragraph
            if i == 0:
                txt = self.start_pattern.sub('', txt)
                if not txt:
                    continue

            if len(txt) > 5:
                text_blocks.append(txt)

        if not text_blocks:
            return None

        # Clean end marker on last paragraph
        text_blocks[-1] = self.end_pattern.sub('', text_blocks[-1])
        if not text_blocks[-1]:
            text_blocks.pop()

        return "\n\n".join(text_blocks) if text_blocks else None
