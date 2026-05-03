1. BRIN

main domain:
https://brin.go.id/
sub domain:
https://brin.go.id/news
example:
https://brin.go.id/news/127906/brin-pt-cosmax-kembangkan-kosmetik-alami-berbasis-mangga-dan-temulawak

strategy:
1. Root Selector & Konten UtamaContainer Teks Berita: div.news-content.Target Elemen: Tag p yang berada langsung di bawah container tersebut.Selector Gabungan: div.news-content > p.2. Metadata BeritaJudul Berita: div.news-title.Waktu Publikasi: div.news-time.Gambar Utama: div.news-image img.3. Pembersihan Data (Logic)Start Marker (Pembersihan Awal):Karakteristik: Paragraf pertama dimulai dengan lokasi dan atribusi humas yang dipisahkan oleh tanda pisah tunggal. Contoh: "Tangerang Selatan-Humas BRIN. Badan Riset dan Inovasi Nasional (BRIN)..."Tindakan: Hapus teks dari awal hingga tanda pisah (-) pertama.Regex: ^.*?\-\s*Humas BRIN,\s* (Sesuaikan jika teks spesifik "Humas BRIN" bervariasi).Inline Styling: Elemen <p> pada situs ini sering membawa atribut inline style seperti dir="ltr" dan style="text-align: justify; ...". Gunakan metode .get_text() untuk mengambil narasi bersih.Ringkasan Konfigurasi TeknisKomponenAturan / SelectorJangkar Utamadiv.news-contentElemen Narasip (Abaikan yang hanya berisi spasi/kosong)Juduldiv.news-titlePembersihanRegex untuk menghapus metadata lokasi di paragraf pertama.
