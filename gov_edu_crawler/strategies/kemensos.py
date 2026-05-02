import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class KemensosStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Root selector unik Kemensos menggunakan h5
        self.selector = "h5.text-content"

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        container = soup.select_one(self.selector)
        
        if not container: return None

        text_blocks = []
        # Target elemen div atau p di dalam h5.text-content
        elements = container.find_all(['div', 'p'])
        junk_keywords = ["Biro Komunikasi", "Laman:", "Instagram:"]

        for i, el in enumerate(elements):
            txt = el.get_text(strip=True)
            if any(junk in txt for junk in junk_keywords) or not txt: continue

            # Start Marker Kemensos: Hapus lokasi/nama menteri
            if i == 0:
                txt = re.sub(r'^.*?[—-]\s*', '', txt)
                txt = re.sub(r'^[–\-\s]+', '', txt)

            # Threshold paragraf minimal 5 karakter
            if len(txt) > 5: 
                text_blocks.append(txt)

        return "\n\n".join(text_blocks)