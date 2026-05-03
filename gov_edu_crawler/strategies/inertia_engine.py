import json
import html
import logging
import re
from bs4 import BeautifulSoup
from .base_strategy import BaseStrategy

logger = logging.getLogger("inertia_engine")

class InertiaEngineStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Regex to extract data-page attribute directly from raw HTML
        # This bypasses BeautifulSoup which truncates massive attributes
        self._data_page_re = re.compile(r'<div\s+id="app"\s+data-page="(.*?)"', re.DOTALL)

    def scrape(self, url, html_content):
        """
        Strategi Khusus Puspresnas & BBGTK Berbasis Inertia.js.
        Data ditemukan di div#app atribut data-page.
        Uses regex extraction to handle massive (8MB+) data-page attributes
        that BeautifulSoup/lxml would truncate.
        """
        try:
            # 1. Extract data-page using regex (bypass BeautifulSoup for huge attributes)
            match = self._data_page_re.search(html_content)
            if not match:
                return None

            raw_json = match.group(1)
            if not raw_json:
                return None

            # 2. Decode HTML entities in JSON (&quot; -> ", &amp; -> &, etc.)
            decoded_json = html.unescape(raw_json)

            # 3. Parse JSON
            page_data = json.loads(decoded_json)
            props = page_data.get('props', {})
            
            raw_html = ""
            # 4. Navigate structure based on domain
            if "pusatprestasinasional" in url:
                # Struktur: props -> data -> detail
                raw_html = props.get('data', {}).get('detail', "")
            elif "bbgtkjatim" in url:
                # Struktur: props -> result -> content
                raw_html = props.get('result', {}).get('content', "")
            
            if not raw_html:
                return None

            # 5. Decode HTML Entity (<p> -> <p>)
            decoded_html = html.unescape(raw_html)
            
            # 6. Extract and clean text
            return self.extract_and_clean(decoded_html)

        except Exception as e:
            logger.error(f"Error parsing Inertia JSON: {e}")
            return None

    def extract_and_clean(self, html_fragment):
        """Membersihkan tag dan membuang sampah Base64[cite: 1]."""
        soup = BeautifulSoup(html_fragment, "lxml")
        
        # BUANG SEMUA GAMBAR (Mencegah teks Base64 masuk ke dataset)[cite: 1]
        for img in soup.find_all('img'):
            img.decompose()

        paragraphs = []
        for element in soup.find_all(['p', 'li']):
            # Jangan ambil teks dari elemen yang punya anak (hindari duplikasi)
            if element.find(['p', 'li']):
                continue
                
            text = element.get_text(strip=True)
            if text and len(text) > 10 and not self.is_junk(text):
                paragraphs.append(text)
        
        if not paragraphs:
            return None

        # Terapkan Start Marker (Tanda Pisah) pada paragraf pertama[cite: 1]
        # Contoh: "Bandung, 27 April 2026 — " akan dibuang[cite: 1]
        paragraphs[0] = self.clean_first_paragraph(paragraphs[0])
        
        return "\n\n".join(paragraphs)