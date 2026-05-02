from .base_strategy import BaseStrategy

class KemensosStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        # Root selector unik menggunakan h5
        self.selector = "h5.text-content"

    def scrape(self, url, html_content):
        """Ekstraksi khusus menggunakan child selector dari h5[cite: 6]."""
        # Mengambil div atau p di dalam h5.text-content[cite: 6]
        return self.extract_clean_text(html_content, self.selector, tags=['div', 'p'])