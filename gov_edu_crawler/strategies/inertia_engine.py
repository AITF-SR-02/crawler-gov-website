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

    def scrape(self, url, html_content):
        """
        Strategi Khusus Puspresnas & BBGTK Berbasis Inertia.js.
        Data ditemukan di div#app atribut data-page.
        """
        soup = BeautifulSoup(html_content, "lxml")
        app_div = soup.select_one("div#app")
        
        if not app_div or not app_div.has_attr('data-page'):
            return None

        try:
            # 1. Ambil JSON mentah
            # BeautifulSoup otomatis men-decode &quot; menjadi "
            page_data = json.loads(app_div['data-page'])
            props = page_data.get('props', {})
            
            raw_html = ""
            # 2. Navigasi Path Sesuai Struktur HTML Puspresnas
            if "pusatprestasinasional" in url:
                # Struktur: props -> data -> detail
                raw_html = props.get('data', {}).get('detail', "")
            elif "bbgtkjatim" in url:
                # Struktur: props -> result -> content
                raw_html = props.get('result', {}).get('content', "")
            
            if not raw_html:
                return None

            # 3. Decode HTML Entity (&lt;p&gt; -> <p>)
            decoded_html = html.unescape(raw_html)
            
            # 4. Ekstraksi dan Pembersihan Teks
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
        # Ambil teks dari p, li, dan span[cite: 1]
        for element in soup.find_all(['p', 'li', 'span']):
            # Jangan ambil teks dari elemen yang punya anak (hindari duplikasi)
            if element.find(['p', 'li']):
                continue
                
            text = element.get_text(strip=True)
            if text and not self.is_junk(text):
                paragraphs.append(text)
        
        if not paragraphs:
            return None

        # 5. Terapkan Start Marker (Tanda Pisah) pada paragraf pertama[cite: 1]
        # Contoh: "Bandung, 27 April 2026 — " akan dibuang[cite: 1]
        paragraphs[0] = self.clean_first_paragraph(paragraphs[0])
        
        return "\n\n".join(paragraphs)