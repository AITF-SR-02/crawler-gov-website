import re
from bs4 import BeautifulSoup

class BaseStrategy:
    def __init__(self):
        # Kata kunci untuk menghentikan pengambilan teks
        self.stop_words = ["Biro Komunikasi", "Sekretariat Jenderal", "Laman:", "X:", "Instagram:", "Foto:", "Sumber:"]
        # Regex untuk menghapus lokasi & tanggal hingga tanda pisah
        self.dash_pattern = re.compile(r'^.*?[ \-\u2013\u2014]\s*')

    def clean_first_paragraph(self, text):
        """Menghapus metadata lokasi/tanggal di awal narasi[cite: 1]."""
        if not text:
            return ""
        if len(text.split(' ')[0]) < 100 or len(text.split('-')[0]) < 100:
            return self.dash_pattern.sub('', text, count=1).strip()
        return text.strip()

    def is_junk(self, text):
        """Mengecek apakah paragraf berisi teks sampah[cite: 1]."""
        p_text = text.strip()
        if not p_text or len(p_text) < 10:
            return True
        return any(word in p_text for word in self.stop_words)

    def extract_clean_text(self, html_content, selector, tags=['p', 'li', 'blockquote']):
        """Template ekstraksi universal[cite: 1]."""
        soup = BeautifulSoup(html_content, "lxml")
        container = soup.select_one(selector)
        if not container:
            return None
        paragraphs = []
        for element in container.find_all(tags):
            text = element.get_text(strip=True)
            if self.is_junk(text):
                if any(word in text for word in self.stop_words if word != "#"):
                    break
                continue
            paragraphs.append(text)
        if not paragraphs:
            return None
        paragraphs[0] = self.clean_first_paragraph(paragraphs[0])
        return "\n\n".join(paragraphs)