import aiosqlite
import hashlib
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/dedupe.sqlite3"):
        self.db_path = db_path

    async def init_db(self):
        """Inisialisasi tabel url_jobs jika belum ada."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS url_jobs (
                    url_hash TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    batch_id INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Index untuk mempercepat pencarian status
            await db.execute("CREATE INDEX IF NOT EXISTS idx_status ON url_jobs(status)")
            await db.commit()

    def generate_hash(self, url):
        """Bikin MD5 hash unik dari URL untuk deduplikasi."""
        return hashlib.md5(url.encode()).hexdigest()

    async def add_urls(self, urls_with_domains):
        """
        Input: list of tuple (url, domain)
        Tugas: Masukin URL baru ke antrean kalau belum ada (deduplikasi).
        """
        async with aiosqlite.connect(self.db_path) as db:
            count = 0
            for url, domain in urls_with_domains:
                url_hash = self.generate_hash(url)
                try:
                    await db.execute(
                        "INSERT INTO url_jobs (url_hash, url, domain) VALUES (?, ?, ?)",
                        (url_hash, url, domain)
                    )
                    count += 1
                except aiosqlite.IntegrityError:
                    # Lewati kalau URL sudah ada di database (duplikat)
                    continue
            await db.commit()
            return count

    async def get_pending_batch(self, limit=100):
        """Ambil batch URL yang berstatus 'pending'[cite: 7]."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM url_jobs WHERE status = 'pending' LIMIT ?", 
                (limit,)
            ) as cursor:
                return await cursor.fetchall()

    async def update_status(self, url_hash, status):
        """Update status pekerjaan (completed/failed)."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE url_jobs SET status = ?, updated_at = ? WHERE url_hash = ?",
                (status, datetime.now(), url_hash)
            )
            await db.commit()

    async def get_stats(self):
        """Cek perolehan sementara."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT status, COUNT(*) FROM url_jobs GROUP BY status") as cursor:
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows}