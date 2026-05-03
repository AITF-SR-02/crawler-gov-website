import aiohttp, asyncio

async def test_brin_auth_api():
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    auth = aiohttp.BasicAuth("superadmin@mail.com", "teTEMx-tdfGG-yfveDj-HPCqS")
    async with aiohttp.ClientSession(headers=hdrs, auth=auth, connector=aiohttp.TCPConnector(ssl=False)) as session:
        # 1. Test listing API
        url_listing = "https://api-web.brin.go.id/webapi/v1?module=posts&path=Core&paginate=true&limit=11&sort=publish_date,desc&in=cid,5&page=1"
        print(f"=== LISTING API: {url_listing} ===")
        async with session.get(url_listing) as r:
            print(f"Status: {r.status}")
            if r.status == 200:
                data = await r.json()
                print(f"Items found: {len(data.get('data', []))}")
                for item in data.get('data', [])[:3]:
                    print(f"  Title: {item.get('title')}")
                    print(f"  Slug: {item.get('slug')}")
                    print(f"  ID: {item.get('id')}")
        
        # 2. Test article API (we might need to query by ID or Slug)
        url_article = "https://api-web.brin.go.id/webapi/v1?module=posts&path=Core&slug=brin-pt-cosmax-kembangkan-kosmetik-alami-berbasis-mangga-dan-temulawak"
        print(f"\n=== ARTICLE API: {url_article} ===")
        async with session.get(url_article) as r:
            print(f"Status: {r.status}")
            if r.status == 200:
                data = await r.json()
                item = data.get('data', [{}])[0] if data.get('data') else {}
                content = item.get('content', '')
                print(f"Content length: {len(content)}")
                print(f"Content preview: {content[:200]}")
                print(f"Item Keys: {item.keys()}")

asyncio.run(test_brin_auth_api())
