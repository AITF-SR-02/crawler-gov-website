import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import asyncio
import random

logger = logging.getLogger("discovery")

class Discovery:
    def __init__(self, db_manager):
        self.db = db_manager
        # Daftar benih (seeds) utama untuk project Sekolah Rakyat
        self.base_seeds = [
            ("https://www.kemendikdasmen.go.id/berita", "kemendikdasmen.go.id"),
            ("https://vokasi.kemendikdasmen.go.id/Publikasi/Berita", "kemendikdasmen.go.id"),
            ("https://itjen.kemendikdasmen.go.id/web/berita", "kemendikdasmen.go.id"),
            ("https://badanbahasa.kemendikdasmen.go.id/berita", "kemendikdasmen.go.id"),
            ("https://bskap.kemendikdasmen.go.id/publikasi", "kemendikdasmen.go.id"),
            ("https://kemdiktisaintek.go.id/news", "kemdiktisaintek.go.id")
        ]
        self.forbidden_ext = ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.zip', '.rar', '.css', '.js')
        self.junk_keywords = ['/category/', '/tag/', '/search/', '/author/', 'mailto:', 'tel:', 'whatsapp:']

    async def find_new_links(self, target_batch=150):
        new_urls_found = []
        # Jatah per domain agar semua kebagian (Fairness)
        quota_per_domain = target_batch // len(self.base_seeds)

        async with aiohttp.ClientSession(headers={"User-Agent": "AITF-SR-02-DeepScout/9.0"}) as session:
            logger.info("🔍 Memulai pencarian di 'Lahan Baru' (Arsip Page 100+)...")
            
            # Acak urutan domain biar gak bosen di satu tempat
            random.shuffle(self.base_seeds)
            
            for base_url, domain in self.base_seeds:
                if len(new_urls_found) >= target_batch: break
                
                domain_count = 0
                # LONCAT JAUH: Kita cari dari halaman 100 sampai 1000 untuk bongkar arsip lama
                start_page = random.randint(100, 1000) 
                logger.info(f"🔎 {domain}: Membongkar arsip mulai dari Page {start_page}...")

                for page in range(start_page, start_page + 20):
                    if domain_count >= quota_per_domain: break
                    
                    # Kalibrasi parameter pagination sesuai struktur web masing-masing
                    if "vokasi" in base_url: 
                        current_seed = f"{base_url}/{page}"
                    elif "itjen" in base_url: 
                        current_seed = f"{base_url}/page/{page}/"
                    elif "kemdiktisaintek" in base_url or "badanbahasa" in base_url:
                        current_seed = f"{base_url}?page={page}"
                    else: 
                        # Default untuk kemendikdasmen.go.id
                        current_seed = f"{base_url}?p={page}"

                    try:
                        async with session.get(current_seed, timeout=15) as response:
                            # Jika 404, berarti halaman arsip sudah mentok, pindah domain
                            if response.status == 404: 
                                logger.info(f"⏹️ {domain} mentok di Page {page}.")
                                break
                            if response.status != 200: continue
                            
                            soup = BeautifulSoup(await response.text(), "lxml")
                            found_in_page = 0
                            
                            for a in soup.find_all('a', href=True):
                                # Bersihkan URL dari fragment (#) dan query string (?)
                                full_url = urljoin(base_url, a['href']).split('#')[0].split('?')[0]
                                url_low = full_url.lower()
                                
                                # Filter domain dan ekstensi file sampah
                                if (url_low.startswith('http') and domain in url_low and 
                                    not url_low.endswith(self.forbidden_ext) and
                                    not any(k in url_low for k in self.junk_keywords)):
                                    
                                    # Simpan ke database dan cek apakah ini barang baru
                                    is_new = await self.db.add_urls([(full_url, domain)])
                                    if is_new > 0:
                                        new_urls_found.append(full_url)
                                        domain_count += 1
                                        found_in_page += 1
                                        if domain_count >= quota_per_domain: break
                            
                            # Smart Break: Jika satu halaman isinya duplikat semua, jangan dipaksa lanjut
                            if found_in_page == 0 and page > start_page + 3: 
                                break 
                    except Exception as e:
                        continue
                
                logger.info(f"✨ {domain}: Berhasil dapet {domain_count} URL baru.")

        return len(new_urls_found)