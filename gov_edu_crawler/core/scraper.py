import aiohttp
import asyncio
import json
import logging
import os
from datetime import datetime
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
        # Support comma-separated focus
        if self.focus in {"all", "*"}:
            return None
        # Return None to scrape all domains when multiple targets
        if "," in self.focus:
            return None
        if self.focus in {"kemdikdasmen", "kemendikdasmen", "dikdasmen"}:
            return "kemendikdasmen.go.id"
        if self.focus in {"kemdiktisaintek", "saintek", "diktisaintek"}:
            return "kemdiktisaintek.go.id"
        if self.focus in {"kemensos"}:
            return "kemensos.go.id"
        if self.focus in {"puspresnas", "pusatprestasinasional"}:
            return "pusatprestasinasional.kemendikdasmen.go.id"
        return None

    async def process_url(self, session, row):
        url, url_hash = row['url'], row['url_hash']
        # Biar lu bisa liat URL apa yang diproses[cite: 1]
        logger.info(f"🚜 Scraping: {url}") 
        
        # Sort by domain length (longest first) so subdomains match before parent
        strategy = next((s for d, s in sorted(self.strategy_map.items(), key=lambda x: -len(x[0])) if d in url), None)
        if not strategy: 
            await self.db.update_status(url_hash, 'err_no_strategy')
            return False

        try:
            async with session.get(url, timeout=60) as response:
                if response.status != 200: 
                    await self.db.update_status(url_hash, f'err_{response.status}')
                    return False
                ctype = response.headers.get('Content-Type', '').lower()
                if 'text/html' not in ctype: 
                    await self.db.update_status(url_hash, 'failed_not_html')
                    return False

                clean_text = strategy.scrape(url, await response.text())
                # Minimal 20 karakter biar berita pendek masuk
                if clean_text and len(clean_text) > 20: 
                    data = {"url": url, "content": clean_text, "scraped_at": datetime.now().isoformat()}
                    with open(self.output_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(data, ensure_ascii=False) + "\n")
                    await self.db.update_status(url_hash, 'completed')
                    return True
                else:
                    await self.db.update_status(url_hash, 'failed_too_short')
                    return False
        except Exception as e:
            await self.db.update_status(url_hash, f'err_{str(e)[:20]}')
            return False

    async def run_batch(self, batch_size=30):
        pending_jobs = await self.db.get_pending_batch(limit=batch_size, domain_contains=self._domain_filter())
        if not pending_jobs: return 0
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers={"User-Agent": "AITF-SR-02-Crawler/12.0"},
            max_field_size=16 * 1024 * 1024,  # 16MB - Puspresnas pages can be 8MB+
            max_line_size=16 * 1024 * 1024
        ) as session:
            tasks = [self.process_url(session, job) for job in pending_jobs]
            results = await asyncio.gather(*tasks)
            return sum(1 for r in results if r)