import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class BrinStrategy(BaseStrategy):
    """Strategi scraping untuk brin.go.id"""
    def __init__(self):
        super().__init__()
        self.selector = "div.news-content"
        # Regex to remove location attribution in first paragraph:
        # e.g. "Tangerang Selatan-Humas BRIN." or "Jakarta-Humas BRIN. "
        self.brin_dash_pattern = re.compile(r'^.*?\-\s*Humas BRIN,?\s*', re.IGNORECASE)

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Target: div.news-content > p
        container = soup.select_one(self.selector)
        if not container:
            return None

        text_blocks = []
        for el in container.find_all('p', recursive=False):
            txt = el.get_text(strip=True)
            if not txt or len(txt) < 10:
                continue
            if self.is_junk(txt):
                continue
                
            # Clean first paragraph location marker
            if len(text_blocks) == 0:
                txt = self.brin_dash_pattern.sub('', txt, count=1).strip()
                
            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
