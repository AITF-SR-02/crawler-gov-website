import asyncio
import logging
from core.db_manager import DatabaseManager
from core.discovery import Discovery
from core.scraper import Scraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main")

async def run_prod(db, discovery, scraper):
    while True:
        try:
            logger.info("🔍 Tahap Discovery: Mencari URL baru...")
            found = await discovery.find_new_links(target_batch=150)
            
            logger.info(f"🚜 Tahap Scraping: Memproses {found} URL baru...")
            success_count = await scraper.run_batch(batch_size=30)
            
            stats = await db.get_stats()
            logger.info(f"📊 Hasil batch: {success_count} disimpan. Total Global: {stats.get('completed', 0)}")

            # Logic Smart Sleep
            if success_count == 0 and found > 0:
                logger.warning("⚠️ Batch berisi duplikat. Lanjut cari lagi...")
                await asyncio.sleep(5)
            elif success_count == 0 and found == 0:
                logger.warning("😴 Arsip atau Sitemap habis. Istirahat 5 menit...")
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(15)

        except Exception as e:
            logger.error(f"🔥 Error loop utama: {e}")
            await asyncio.sleep(60)

async def main():
    db = DatabaseManager()
    await db.init_db()
    await run_prod(db, Discovery(db), Scraper(db))

if __name__ == "__main__":
    asyncio.run(main())