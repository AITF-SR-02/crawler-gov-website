import aiohttp, asyncio, re

async def investigate_brin_js3():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with aiohttp.ClientSession(headers=hdrs, connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = "https://brin.go.id/_next/static/chunks/pages/news-4c36f3af73feedef.js"
        async with session.get(url) as r:
            code = await r.text()
            # Find the get block
            match = re.search(r'params:\{(.{1,100}?)\}', code)
            if match:
                print(f"Params: {match.group(0)}")
                
            match = re.search(r'get\("".concat\("https://api-web.brin.go.id/webapi/v1"\),\{params:\{(.*?)\}\}\)', code)
            if match:
                print(f"Full GET call: {match.group(0)}")

asyncio.run(investigate_brin_js3())
