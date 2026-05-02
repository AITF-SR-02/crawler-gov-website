import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

class KemdiktisaintekStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Selector khusus untuk kemdiktisaintek
        self.selector = "div.entry-content" # Sesuaikan jika berbeda di lapangan

    def scrape(self, url, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        # Mencari container utama berita
        container = soup.select_one(self.selector) or soup.select_one('article')
        
        if not container:
            return None

        text_blocks = []
        # Ambil semua tag p
        elements = container.find_all('p')
        
        for i, el in enumerate(elements):
            txt = el.get_text(strip=True)
            
            # Start Marker: Hapus lokasi di awal jika ada dash
            if i == 0:
                txt = re.sub(r'^.*?[—–-]\s*', '', txt)
                txt = re.sub(r'^[–\-\s]+', '', txt)

            # Threshold 20 karakter sesuai request lu tadi
            if len(txt) > 20:
                text_blocks.append(txt)

        return "\n\n".join(text_blocks)