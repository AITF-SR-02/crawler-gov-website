import aiohttp, asyncio, re
from bs4 import BeautifulSoup

async def investigate_brin_js():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with aiohttp.ClientSession(headers=hdrs, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get("https://brin.go.id/news") as r:
            html = await r.text()
            soup = BeautifulSoup(html, 'lxml')
            
            js_files = [script['src'] for script in soup.find_all('script', src=True)]
            print(f"Found {len(js_files)} JS files")
            
            for js in js_files:
                js_url = f"https://brin.go.id{js}" if js.startswith('/') else js
                print(f"Checking {js_url}")
                try:
                    async with session.get(js_url) as js_r:
                        js_code = await js_r.text()
                        apis = re.findall(r'https?://[^\s\"\']+/api/[^\s\"\']+', js_code)
                        cms_links = re.findall(r'https?://[^\s\"\']+cms[^\s\"\']+', js_code)
                        both = set(apis + cms_links)
                        if both:
                            print(f"  Found APIs: {both}")
                except Exception as e:
                    pass

asyncio.run(investigate_brin_js())
