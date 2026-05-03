import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import math
import os
import random
import asyncio
from playwright.async_api import async_playwright

logger = logging.getLogger("discovery")

class Discovery:
    def __init__(self, db_manager):
        self.db = db_manager
        self.focus = (os.getenv("CRAWLER_FOCUS") or "kemendikdasmen").strip().lower()
        self.forbidden_ext = (
            ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", 
            ".zip", ".rar", ".css", ".js",
        )
        self.junk_keywords = [
            "/author/", "mailto:", "tel:", "whatsapp:", 
            "/galeri"
        ]
        self._odoo_cursor = {}
        self.seeds_config = self._build_seeds_config(self.focus)

    def _build_seeds_config(self, focus: str):
        all_seeds = [
            {
                "type": "odoo_search",
                "name": "kemendikdasmen_siaran_pers",
                "group": "kemendikdasmen",
                "base_url": "https://www.kemendikdasmen.go.id",
                "section": "siaran-pers",
                "domain": "kemendikdasmen.go.id",
                "max_p": 468,
                "limit": 10,
                "pages_per_run": 3,
            },
            {
                "type": "odoo_search",
                "name": "kemendikdasmen_pengumuman",
                "group": "kemendikdasmen",
                "base_url": "https://www.kemendikdasmen.go.id",
                "section": "pengumuman",
                "domain": "kemendikdasmen.go.id",
                "max_p": 36,
                "limit": 10,
                "pages_per_run": 2,
            },
            {
                "type": "html",
                "name": "vokasi_berita",
                "group": "kemendikdasmen",
                "url": "https://vokasi.kemendikdasmen.go.id/Publikasi/Berita",
                "domain": "vokasi.kemendikdasmen.go.id",
                "max_p": 150,
                "page_format": "{base}/{page}",
            },
            {
                "type": "html",
                "name": "itjen_berita",
                "group": "kemendikdasmen",
                "url": "https://itjen.kemendikdasmen.go.id/web/berita",
                "domain": "itjen.kemendikdasmen.go.id",
                "max_p": 100,
                "page_format": "{base}/page/{page}/",
            },
            {
                "type": "html",
                "name": "bskap_publikasi",
                "group": "kemendikdasmen",
                "url": "https://bskap.kemendikdasmen.go.id/publikasi",
                "domain": "bskap.kemendikdasmen.go.id",
                "max_p": 50,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "rumahpusbin_berita",
                "group": "kemendikdasmen",
                "url": "https://rumahpusbin.kemendikdasmen.go.id/berita.php",
                "domain": "rumahpusbin.kemendikdasmen.go.id",
                "max_p": 20,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "badanbahasa_berita",
                "group": "kemendikdasmen",
                "url": "https://badanbahasa.kemendikdasmen.go.id/berita",
                "domain": "badanbahasa.kemendikdasmen.go.id",
                "max_p": 1,
                "page_format": "{base}",
            },
            {
                "type": "html",
                "name": "kemdiktisaintek_news",
                "group": "kemdiktisaintek",
                "url": "https://kemdiktisaintek.go.id/news",
                "domain": "kemdiktisaintek.go.id",
                "max_p": 1000,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "kemensos_berita",
                "group": "kemensos",
                "url": "https://kemensos.go.id/berita-terkini",
                "domain": "kemensos.go.id",
                "max_p": 300,
                "page_format": "{base}/Sekolah-Rakyat/{page}",
            },
            {
                "type": "api_json",
                "name": "puspresnas_wara_wara",
                "group": "puspresnas",
                "url": "https://pusatprestasinasional.kemendikdasmen.go.id/api/news",
                "domain": "pusatprestasinasional.kemendikdasmen.go.id",
                "max_p": 145,
                "page_format": "{base}?page={page}",
                "route_key": "route",
            },
            {
                "type": "html",
                "name": "kemenag_search",
                "group": "kemenag",
                "url": "https://kemenag.go.id/search",
                "domain": "kemenag.go.id",
                "max_p": 900,
                "page_format": "{base}?q=&page={page}",
            },
            {
                "type": "html",
                "name": "indonesiakaya_kesenian",
                "group": "indonesiakaya",
                "url": "https://indonesiakaya.com/pustaka-indonesia-category/kesenian",
                "domain": "indonesiakaya.com",
                "max_p": 50,
                "page_format": "{base}/page/{page}/",
            },
            {
                "type": "html",
                "name": "indonesiakaya_tradisi",
                "group": "indonesiakaya",
                "url": "https://indonesiakaya.com/pustaka-indonesia-category/tradisi",
                "domain": "indonesiakaya.com",
                "max_p": 50,
                "page_format": "{base}/page/{page}/",
            },
            {
                "type": "html",
                "name": "indonesiakaya_pariwisata",
                "group": "indonesiakaya",
                "url": "https://indonesiakaya.com/pustaka-indonesia-category/pariwisata",
                "domain": "indonesiakaya.com",
                "max_p": 50,
                "page_format": "{base}/page/{page}/",
            },
            {
                "type": "html",
                "name": "indonesiakaya_kuliner",
                "group": "indonesiakaya",
                "url": "https://indonesiakaya.com/pustaka-indonesia-category/kuliner",
                "domain": "indonesiakaya.com",
                "max_p": 50,
                "page_format": "{base}/page/{page}/",
            },
            {
                "type": "html",
                "name": "perpusnas_berita",
                "group": "perpusnas",
                "url": "https://perpusnas.go.id/berita",
                "domain": "perpusnas.go.id",
                "max_p": 100,
                "page_format": "{base}/page/{page}",
            },
            # --- LPDP MODIFIED FOR PLAYWRIGHT ---
            {
                "type": "playwright",
                "name": "lpdp_berita",
                "group": "lpdp",
                "url": "https://lpdp.kemenkeu.go.id/informasi/berita",
                "domain": "lpdp.kemenkeu.go.id",
                "max_p": 50,
                "page_format": "{base}/?page={page}",
            },
            {
                "type": "html",
                "name": "indonesiagoid_nasional",
                "group": "indonesiagoid",
                "url": "https://indonesia.go.id/informasi/nasional",
                "domain": "indonesia.go.id",
                "max_p": 1000,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "indotravel_culture",
                "group": "wonderful",
                "url": "https://www.indonesia.travel/id/id/travel-ideas/culture",
                "domain": "indonesia.travel",
                "max_p": 50,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "indotravel_nature",
                "group": "wonderful",
                "url": "https://www.indonesia.travel/id/id/travel-ideas/nature-adventure",
                "domain": "indonesia.travel",
                "max_p": 50,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "indotravel_culinary",
                "group": "wonderful",
                "url": "https://www.indonesia.travel/id/id/travel-ideas/culinary-shopping",
                "domain": "indonesia.travel",
                "max_p": 50,
                "page_format": "{base}?page={page}",
            },
            {
                "type": "html",
                "name": "wonderfulcoid_all",
                "group": "wonderful",
                "url": "https://wonderfulindonesia.co.id/all-posts",
                "domain": "wonderfulindonesia.co.id",
                "max_p": 14,
                "page_format": "{base}/page/{page}/",
            },
            # --- BRIN (SPA) MODIFIED FOR PLAYWRIGHT ---
            {
                "type": "playwright",
                "name": "brin_news",
                "group": "brin",
                "url": "https://brin.go.id/news",
                "domain": "brin.go.id",
                "max_p": 1,
                "page_format": "{base}",
            },
        ]

        if focus in {"all", "*"}:
            return all_seeds

        selected_seeds = []
        focus_parts = [p.strip() for p in focus.replace(",", " ").split()]
        
        for p in focus_parts:
            if p in {"kemdikdasmen", "kemendikdasmen", "dikdasmen"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "kemendikdasmen"])
            elif p in {"kemdiktisaintek", "saintek", "diktisaintek", "kemendiktisanitek"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "kemdiktisaintek"])
            elif p in {"kemensos"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "kemensos"])
            elif p in {"puspresnas", "pusatprestasinasional"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "puspresnas"])
            elif p in {"kemenag"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "kemenag"])
            elif p in {"indonesiakaya", "indonesia_kaya"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "indonesiakaya"])
            elif p in {"perpusnas"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "perpusnas"])
            elif p in {"lpdp"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "lpdp"])
            elif p in {"indonesiagoid", "indonesia_go", "indonesia.go.id"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "indonesiagoid"])
            elif p in {"wonderful", "wonderfulindonesia", "indonesia_travel"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "wonderful"])
            elif p in {"brin"}:
                selected_seeds.extend([s for s in all_seeds if s.get("group") == "brin"])

        unique_seeds = []
        for s in selected_seeds:
            if s not in unique_seeds:
                unique_seeds.append(s)

        if unique_seeds:
            return unique_seeds

        logger.warning(f"⚠️ CRAWLER_FOCUS='{focus}' tidak dikenal. Fallback ke 'all'.")
        return all_seeds

    def _is_allowed(self, url: str, domain: str) -> bool:
        url_low = url.lower()
        return (
            url_low.startswith("http")
            and domain in url_low
            and not url_low.endswith(self.forbidden_ext)
            and not any(k in url_low for k in self.junk_keywords)
        )

    async def _discover_odoo_search(self, session: aiohttp.ClientSession, seed: dict, quota: int) -> int:
        key = seed["name"]
        base_url = seed["base_url"].rstrip("/")
        section = seed["section"]
        api_url = f"{base_url}/pencarian/{section}/search"

        limit = int(seed.get("limit") or 10)
        max_p = int(seed.get("max_p") or 1)
        pages_per_run = int(seed.get("pages_per_run") or 1)

        start_page = int(self._odoo_cursor.get(key, 1))
        if start_page < 1 or start_page > max_p:
            start_page = 1

        added = 0
        for offset in range(pages_per_run):
            if added >= quota:
                break

            page = start_page + offset
            if page > max_p:
                break

            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "keyword": "",
                    "sort_order": "terbaru",
                    "kategori": [],
                    "kelompok": [],
                    "tagging": "",
                    "pengguna": [],
                    "tahun": [],
                    "page": page,
                    "limit": limit,
                    "csrf_token": "",
                },
                "id": 1,
            }

            try:
                async with session.post(
                    api_url,
                    json=payload,
                    timeout=35,
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                ) as response:
                    if response.status != 200:
                        break
                    data = await response.json(content_type=None)
            except Exception:
                break

            result = data.get("result") or {}
            results = result.get("results") or []
            if not results:
                break

            total_count = result.get("total_count")
            if isinstance(total_count, int) and total_count > 0:
                computed_max = max(1, math.ceil(total_count / limit))
                seed["max_p"] = max(seed.get("max_p", 1), computed_max)
                max_p = seed["max_p"]

            urls_to_add = []
            for item in results:
                path = item.get("url")
                if not path:
                    continue
                full_url = urljoin(base_url + "/", path)
                if self._is_allowed(full_url, seed["domain"]):
                    urls_to_add.append((full_url, seed["domain"]))

            if not urls_to_add:
                continue

            inserted = await self.db.add_urls(urls_to_add)
            added += inserted

        next_page = start_page + pages_per_run
        if next_page > max_p:
            next_page = 1
        self._odoo_cursor[key] = next_page
        return added

    async def _discover_html(self, session: aiohttp.ClientSession, seed: dict, quota: int) -> int:
        base_url = seed["url"]
        domain = seed["domain"]
        max_p = int(seed.get("max_p") or 1)
        page_format = seed.get("page_format") or "{base}?page={page}"

        added = 0
        start_page = 1 if max_p <= 1 else random.randint(1, max_p)

        for page in range(start_page, start_page + 10):
            if added >= quota:
                break
            if page > max_p:
                break

            current_seed = page_format.format(base=base_url, page=page)
            try:
                async with session.get(current_seed, timeout=20) as response:
                    if response.status != 200:
                        break
                    soup = BeautifulSoup(await response.text(), "lxml")
            except Exception:
                continue

            candidates = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("#") or href.startswith("javascript:"):
                    continue

                if any(x in href for x in ["?p=", "?id=", "berita_detail", "?page="]):
                    full_url = urljoin(base_url, href).split("#")[0]
                else:
                    full_url = urljoin(base_url, href).split("#")[0].split("?")[0]

                if self._is_allowed(full_url, domain):
                    candidates.append((full_url, domain))

            if not candidates:
                if page >= start_page + 2:
                    break
                continue

            inserted = await self.db.add_urls(candidates)
            added += inserted

        return added

    async def _discover_playwright(self, seed: dict, quota: int) -> int:
        """Fungsi baru: Menarik link dari website SPA seperti LPDP & BRIN"""
        base_url = seed["url"]
        domain = seed["domain"]
        max_p = int(seed.get("max_p") or 1)
        page_format = seed.get("page_format") or "{base}?page={page}"

        added = 0
        start_page = 1 if max_p <= 1 else random.randint(1, max_p)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent="AITF-SR-02-DeepScout/12.0")
                page_instance = await context.new_page()

                for page_num in range(start_page, start_page + 10):
                    if added >= quota or page_num > max_p:
                        break

                    current_seed = page_format.format(base=base_url, page=page_num)
                    logger.info(f"🎭 [DISCOVERY] Playwright fetching SPA seed: {current_seed}")
                    
                    try:
                        await page_instance.goto(current_seed, wait_until="networkidle", timeout=45000)
                        await asyncio.sleep(3) # Tunggu rendering selesai
                        html = await page_instance.content()
                        soup = BeautifulSoup(html, "lxml")
                    except Exception as e:
                        logger.error(f"🎭 Playwright error di {current_seed}: {str(e)[:50]}")
                        continue

                    candidates = []
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        if href.startswith("#") or href.startswith("javascript:"):
                            continue
                        if any(x in href for x in ["?p=", "?id=", "berita_detail", "?page="]):
                            full_url = urljoin(base_url, href).split("#")[0]
                        else:
                            full_url = urljoin(base_url, href).split("#")[0].split("?")[0]

                        if self._is_allowed(full_url, domain):
                            candidates.append((full_url, domain))

                    if not candidates:
                        if page_num >= start_page + 2:
                            break
                        continue

                    inserted = await self.db.add_urls(candidates)
                    added += inserted

                await browser.close()
        except Exception as e:
            logger.error(f"Gagal inisiasi Playwright di Discovery: {e}")
            
        return added

    async def _discover_api(self, session, seed, quota):
        """Discovery via paginated JSON API (Puspresnas)."""
        base_url = seed["url"]
        domain = seed["domain"]
        max_p = seed.get("max_p", 50)
        page_format = seed.get("page_format", "{base}?page={page}")
        route_key = seed.get("route_key", "route")
        added = 0
        start_page = random.randint(1, max_p)

        for page in range(start_page, start_page + 10):
            if added >= quota or page > max_p:
                break

            api_url = page_format.format(base=base_url, page=page)
            try:
                async with session.get(api_url, timeout=20) as response:
                    if response.status != 200:
                        break
                    data = await response.json(content_type=None)
            except Exception:
                continue

            items = data.get("data", data) if isinstance(data, dict) else data
            if not isinstance(items, list):
                continue

            candidates = []
            for item in items:
                route = item.get(route_key, "")
                if route and domain in route:
                    candidates.append((route.split("#")[0].split("?")[0], domain))

            if not candidates:
                if page >= start_page + 2:
                    break
                continue

            inserted = await self.db.add_urls(candidates)
            added += inserted

        return added

    async def find_new_links(self, target_batch: int = 150) -> int:
        if not self.seeds_config:
            return 0

        groups = []
        for s in self.seeds_config:
            g = s.get("group")
            if g and g not in groups:
                groups.append(g)

        if not hasattr(self, 'current_group_idx'):
            self.current_group_idx = 0
            
        if groups:
            current_group = groups[self.current_group_idx % len(groups)]
            self.current_group_idx += 1
            active_seeds = [s for s in self.seeds_config if s.get("group") == current_group]
        else:
            current_group = "unknown"
            active_seeds = self.seeds_config

        total_added = 0
        quota_per_seed = max(1, target_batch // len(active_seeds))

        async with aiohttp.ClientSession(headers={"User-Agent": "AITF-SR-02-DeepScout/12.0"}) as session:
            logger.info(f"🔍 Discovery start (focus={self.focus}, active_group={current_group}, seeds={len(active_seeds)})")

            if self.focus in {"all", "*"}:
                random.shuffle(active_seeds)

            for seed in active_seeds:
                if total_added >= target_batch:
                    break

                quota = min(quota_per_seed, target_batch - total_added)
                try:
                    if seed.get("type") == "odoo_search":
                        added = await self._discover_odoo_search(session, seed, quota)
                        label = f"{seed['base_url']}/pencarian/{seed['section']}"
                    elif seed.get("type") == "api_json":
                        added = await self._discover_api(session, seed, quota)
                        label = seed.get("url")
                    elif seed.get("type") == "playwright":
                        # ROUTING BARU UNTUK SPA (LPDP, BRIN)
                        added = await self._discover_playwright(seed, quota)
                        label = seed.get("url")
                    else:
                        added = await self._discover_html(session, seed, quota)
                        label = seed.get("url")
                except Exception:
                    added = 0
                    label = seed.get("url") or seed.get("name")

                total_added += added
                logger.info(f"✨ {label}: Dapet {added} URL baru.")

        return total_added