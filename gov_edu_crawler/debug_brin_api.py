import aiohttp, asyncio, re
from bs4 import BeautifulSoup

async def investigate_brin_api():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with aiohttp.ClientSession(headers=hdrs, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get("https://brin.go.id/news") as r:
            html = await r.text()
            soup = BeautifulSoup(html, 'lxml')
            
            # Find NextJS build id
            script = soup.find('script', id='__NEXT_DATA__')
            if script:
                print("NEXT_DATA script:")
                print(script.string[:500])
                
            # Find any API links
            apis = re.findall(r'https?://[^\s\"\']+/api/[^\s\"\']+', html)
            if apis:
                print("\nFound APIs in HTML:")
                for a in set(apis):
                    print(a)
                    
        # Let's try to query the NextJS API for the article directly using the known build ID
        build_id = "r9J2a8qkevCyqWJiaAsfw" # from earlier script
        print("\nTesting NextJS API for article...")
        url = f"https://brin.go.id/_next/data/{build_id}/id/news/127906/brin-pt-cosmax-kembangkan-kosmetik-alami-berbasis-mangga-dan-temulawak.json"
        async with session.get(url) as r:
            print(f"Status: {r.status}")
            if r.status == 200:
                text = await r.text()
                print(f"Content length: {len(text)}")
                print(text[:500].encode('ascii', 'replace').decode())

asyncio.run(investigate_brin_api())
