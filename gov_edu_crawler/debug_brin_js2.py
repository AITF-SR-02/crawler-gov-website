import aiohttp, asyncio, re

async def investigate_brin_js2():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with aiohttp.ClientSession(headers=hdrs, connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = "https://brin.go.id/_next/static/chunks/pages/news-4c36f3af73feedef.js"
        async with session.get(url) as r:
            code = await r.text()
            # find strings starting with http
            urls = re.findall(r'https?://[^\s\"\',]+', code)
            print(f"Found URLs in news.js:")
            for u in set(urls):
                print(u)
                
            # print surrounding text for brin domains
            for match in re.finditer(r'.{0,50}brin\.go\.id.{0,50}', code):
                print(match.group(0))

asyncio.run(investigate_brin_js2())
