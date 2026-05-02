import aiohttp
import asyncio
import json
import logging
from datetime import datetime
from strategies.kemendikdasmen import KemendikdasmenStrategy
from strategies.kemdiktisaintek import KemendiktisaintekStrategy
from strategies.kemensos import KemensosStrategy

logger = logging.getLogger("scraper")

class Scraper:
    def __init__(self, db_manager, output_path="data/raw/dataset_raw.jsonl"):
        self.db = db_manager
        self.output_path = output_path
        self.strategy_map = {
            "kemendikdasmen.go.id": KemendikdasmenStrategy(),
            "kemdiktisaintek.go.id": KemendiktisaintekStrategy(),
            "kemensos.go.id": KemensosStrategy()
        }

    async def process_url(self, session, row):
        url, url_hash = row['url'], row['url_hash']
        strategy = next((s for d, s in self.strategy_map.items() if d in url), None)
        if not strategy: return False

        try:
            await asyncio.sleep(1) # Jeda sopan
            async with session.get(url, timeout=25) as response:
                if response.status != 200: return False
                
                ctype = response.headers.get('Content-Type', '').lower()
                if 'text/html' not in ctype: # Filter file binary
                    await self.db.update_status(url_hash, 'failed_not_html')
                    return False

                clean_text = strategy.scrape(url, await response.text())
                if clean_text and len(clean_text) > 250:
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
        pending_jobs = await self.db.get_pending_batch(limit=batch_size)
        if not pending_jobs: return 0
        
        # Cegah Error 400 dengan menaikkan limit header ke 32KB
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers={"User-Agent": "AITF-SR-02-Crawler/4.0"},
            max_field_size=32768, 
            max_line_size=32768
        ) as session:
            tasks = [self.process_url(session, job) for job in pending_jobs]
            results = await asyncio.gather(*tasks)
            return sum(1 for r in results if r)