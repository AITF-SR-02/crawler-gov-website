from .base_strategy import BaseStrategy

class KemendiktisaintekStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Target kontainer utama sesuai pola strategi
        self.selector = "article.rich-content"

    def scrape(self, url, html_content):
        """Ekstraksi dengan pengecekan Start Marker yang lebih longgar[cite: 4]."""
        # Kemendiktisaintek sering punya gambar Base64 yang sangat panjang, 
        # extract_clean_text otomatis membuangnya[cite: 4].
        return self.extract_clean_text(html_content, self.selector)