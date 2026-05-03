import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class IndonesiaGoStrategy(BaseStrategy):
    """Strategi scraping untuk indonesia.go.id
    
    CATATAN: Website ini adalah SPA (Vue/Nuxt) dan mengembalikan 
    <div id="app"></div> kosong saat di-fetch tanpa JavaScript.
    Jika content ditemukan (misalnya via SSR), gunakan selector quill-content.
    """
    def __init__(self):
        super().__init__()
        self.selector = "div.quill-content"

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')

        # Try primary selector
        container = soup.select_one(self.selector)
        if not container:
            # Fallback: try any prose-like container
            container = soup.select_one("div.prose") or soup.select_one("article")
        
        if not container:
            return None

        text_blocks = []
        for i, el in enumerate(container.find_all('p')):
            txt = el.get_text(strip=True)
            if not txt or len(txt) < 5:
                continue
            if self.is_junk(txt):
                continue

            # Start marker: "JAKARTA -" style uppercase location
            if i == 0:
                txt = re.sub(r'^[A-Z\s]+?\s?[\-—–]\s*', '', txt)
                if not txt:
                    continue

            text_blocks.append(txt)

        return "\n\n".join(text_blocks) if text_blocks else None
