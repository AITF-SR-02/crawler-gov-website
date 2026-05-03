import aiohttp
import asyncio
import json
import logging
import os
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

from strategies.kemendikdasmen import KemendikdasmenStrategy
from strategies.kemdiktisaintek import KemdiktisaintekStrategy
from strategies.kemensos import KemensosStrategy
from strategies.inertia_engine import InertiaEngineStrategy
from strategies.kemenag import KemenagStrategy
from strategies.indonesia_kaya import IndonesiaKayaStrategy
from strategies.perpusnas import PerpusnasStrategy
from strategies.lpdp import LpdpStrategy
from strategies.indonesia_go import IndonesiaGoStrategy
from strategies.indonesia_travel import IndonesiaTravelStrategy
from strategies.wonderful_indonesia import WonderfulIndonesiaStrategy
from strategies.brin import BrinStrategy

logger = logging.getLogger("scraper")

class Scraper:
    def __init__(self, db_manager, output_path="data/raw/dataset_raw.jsonl"):
        self.db = db_manager
        self.output_path = output_path
        self.focus = (os.getenv("CRAWLER_FOCUS") or "kemendikdasmen").strip().lower()
        self.strategy_map = {
            "pusatprestasinasional.kemendikdasmen.go.id": InertiaEngineStrategy(),
            "kemendikdasmen.go.id": KemendikdasmenStrategy(),
            "kemdiktisaintek.go.id": KemdiktisaintekStrategy(),
            "kemensos.go.id": KemensosStrategy(),
            "kemenag.go.id": KemenagStrategy(),
            "indonesiakaya.com": IndonesiaKayaStrategy(),
            "perpusnas.go.id": PerpusnasStrategy(),
            "lpdp.kemenkeu.go.id": LpdpStrategy(),
            "indonesia.go.id": IndonesiaGoStrategy(),
            "indonesia.travel": IndonesiaTravelStrategy(),
            "wonderfulindonesia.co.id": WonderfulIndonesiaStrategy(),
            "brin.go.id": BrinStrategy(),
        }

    def _domain_filter(self):
        if self.focus in {"all", "*"}: return None
        if "," in self.focus: return None
        # Mapping fokus ke domain asli
        focus_map = {
            "lpdp": "lpdp.kemenkeu.go.id",
            "brin": "brin.go.id",
            "kemenag": "kemenag.go.id",
            "indonesiagoid": "indonesia.go.id"
        }
        return focus_map.get(self.focus, self.focus)

    async def _fetch_with_crawl4ai(self, url):
        """Engine Baru: Menggunakan Crawl4AI untuk handling SPA/JS secara otomatis."""
        logger.info(f"🚀 [Crawl4AI] Processing: {url}")
        async with AsyncWebCrawler() as crawler:
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                wait_for="body", # Menunggu elemen body render
                page_timeout=60000,
                js_code="window.scrollTo(0, document.body.scrollHeight);", # Auto-scroll
            )
            result = await crawler.arun(url=url, config=config)
            
            if result.success:
                return result.html
            else:
                logger.error(f"❌ Crawl4AI failed: {result.error_message}")
                return None

    async def process_url(self, session, row):
        url, url_hash = row['url'], row['url_hash']
        logger.info(f"🚜 Scraping Target: {url}") 
        
        strategy = next((s for d, s in sorted(self.strategy_map.items(), key=lambda x: -len(x[0])) if d in url), None)
        if not strategy: 
            await self.db.update_status(url_hash, 'err_no_strategy')
            return False

        # Identifikasi domain yang butuh Engine Dinamis
        js_domains = ["lpdp.kemenkeu.go.id", "brin.go.id", "kemenag.go.id", "indonesia.go.id"]
        use_dynamic = any(domain in url for domain in js_domains)

        try:
            html_content = ""
            if use_dynamic:
                html_content = await self._fetch_with_crawl4ai(url)
            else:
                # Tetap gunakan aiohttp untuk situs statis (jauh lebih cepat)
                async with session.get(url, timeout=60) as response:
                    if response.status == 200:
                        html_content = await response.text()

            if not html_content:
                await self.db.update_status(url_hash, 'err_fetch_failed')
                return False

            # Ekstraksi menggunakan Strategy
            clean_text = strategy.scrape(url, html_content)
            
            if clean_text and len(clean_text) > 50: # Naikkan threshold sedikit agar kualitas bagus
                data = {"url": url, "content": clean_text, "scraped_at": datetime.now().isoformat()}
                with open(self.output_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
                await self.db.update_status(url_hash, 'completed')
                return True
            else:
                await self.db.update_status(url_hash, 'failed_content_empty_or_short')
                return False

        except Exception as e:
            logger.error(f"💥 Critical Error on {url}: {str(e)[:50]}")
            await self.db.update_status(url_hash, f'err_{str(e)[:15]}')
            return False

    async def run_batch(self, batch_size=5):
        pending_jobs = await self.db.get_pending_batch(limit=batch_size, domain_contains=self._domain_filter())
        if not pending_jobs: 
            logger.info("✅ Tidak ada antrean pending.")
            return 0
            
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers={"User-Agent": "AITF-SR-02-Crawler/13.0"}
        ) as session:
            tasks = [self.process_url(session, job) for job in pending_jobs]
            results = await asyncio.gather(*tasks)
            return sum(1 for r in results if r)