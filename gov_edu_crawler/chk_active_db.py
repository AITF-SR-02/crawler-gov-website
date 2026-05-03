import sqlite3

conn = sqlite3.connect('data/dedupe.sqlite3')
cur = conn.cursor()

print("=== DOMAIN STATUS (Total URLs) ===")
cur.execute("""
    SELECT domain, status, COUNT(*) 
    FROM url_jobs 
    WHERE domain IN ('indonesiakaya.com', 'lpdp.kemenkeu.go.id', 'indonesia.travel', 'wonderfulindonesia.co.id', 'pusatprestasinasional.kemendikdasmen.go.id')
    GROUP BY domain, status
    ORDER BY domain, COUNT(*) DESC
""")
for domain, status, count in cur.fetchall():
    print(f"{domain} - {status}: {count}")

conn.close()
