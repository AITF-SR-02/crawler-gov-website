import aiohttp, asyncio
from bs4 import BeautifulSoup

async def main():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with aiohttp.ClientSession(headers=hdrs, connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Check listing page
        url_listing = "https://brin.go.id/news"
        print(f"=== LISTING: {url_listing} ===")
        async with session.get(url_listing) as r:
            html = await r.text()
            soup = BeautifulSoup(html, "lxml")
            links = []
            for a in soup.find_all('a', href=True):
                h = a['href']
                if '/news/' in h and len(h) > 30:
                    links.append(h)
            links = list(set(links))
            print(f"Status: {r.status}")
            print(f"HTML length: {len(html)}")
            print(f"Article links: {len(links)}")
            for l in links[:5]:
                print(f"  {l}")
            
            # Check for SPA indicators
            if len(links) == 0:
                print("Checking for SPA...")
                scripts = soup.find_all('script')
                for s in scripts:
                    if s.string and ('news' in s.string or 'api' in s.string):
                        print(f"Found script: {s.string[:200]}")
                print(f"App div: {soup.select_one('#__nuxt, #app, #root')}")
                
        # Check article page
        url_article = "https://brin.go.id/news/127906/brin-pt-cosmax-kembangkan-kosmetik-alami-berbasis-mangga-dan-temulawak"
        print(f"\n=== ARTICLE: {url_article} ===")
        async with session.get(url_article) as r:
            html = await r.text()
            soup = BeautifulSoup(html, "lxml")
            content = soup.select_one("div.news-content")
            print(f"Status: {r.status}")
            print(f"Content found: {content is not None}")
            if content:
                print(f"Text preview: {content.get_text(strip=True)[:200]}")
            else:
                print(f"App div: {soup.select_one('#__nuxt, #app, #root')}")

asyncio.run(main())
