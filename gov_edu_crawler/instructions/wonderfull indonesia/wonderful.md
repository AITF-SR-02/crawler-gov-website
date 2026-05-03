1. wonderfull indonesia 1

main domain:
https://www.indonesia.travel/

sub domain:
https://www.indonesia.travel/id/id/travel-ideas/

example:
https://www.indonesia.travel/id/id/travel-ideas/culture/7-spot-cantik-untuk-melihat-panorama-danau-toba-yang-lebih-estetik/

strategy:
1. Root Selector UtamaKontainer Inti: div#article-content (Selector paling akurat untuk isi tubuh artikel).Target Elemen Narasi: Tag p yang berada di dalam kontainer tersebut.Selector Gabungan: div#article-content p2. Metadata & JudulJudul Utama: h1#article-title atau h1.title-section.Sub-Header (List Poin): p strong atau p[style*="font-size: 22.0px"] strong.Detail: Situs ini sering menggunakan tag paragraf dengan inline style ukuran font besar untuk menandai poin-poin lokasi (contoh: "1 | Bukit Holbung").3. Data Cleanup (Pembersihan)Empty Paragraphs: Abaikan elemen <p>&nbsp;</p> atau <p><br /></p> yang sering muncul sebagai pemberi jarak antar paragraf.Media Elements: Jika hanya butuh teks, abaikan div.tambah-video dan tag img.Start/End Marker: Situs ini biasanya ramah SEO, teks langsung dimulai dengan sapaan khas (seperti "Sobat Pesona"). Tidak ada pola lokasi/tanggal berita kaku di awal paragraf seperti situs kementerian.Ringkasan Teknis KonfigurasiKomponenAturan / SelectorJangkar Utamadiv#article-contentElemen TekspJudulh1#article-titlePoin Pentingp strong (untuk poin lokasi/sub-topik)MetodePlain Text (Ambil .get_text() dari tiap paragraf)


2. wonderfull indonesia 2:
 
 main domain: 
 https://wonderfulindonesia.co.id/

 sub domain:
 https://wonderfulindonesia.co.id/all-posts/

 example:
 https://wonderfulindonesia.co.id/pantai-base-g-tanjung-ria-dekat-kota/


strategy:
1. Root Selector UtamaKontainer Inti: div.post_content.entry-contentTarget Elemen Narasi: Tag p, h2, dan blockquote yang berada langsung di dalam kontainer tersebut.Selector Gabungan: div.post_content.entry-content > *2. Metadata & JudulJudul Utama: h1.post_titleTanggal Terbit: span.post_meta_item.post_date atau meta[property="article:published_time"]Kategori: div.post_meta_categories a (Contoh: "Maluku & Papua")Penulis: a.post_author_name3. Pembersihan Data & Proteksi Spam (Wajib)Situs ini memiliki elemen tersembunyi yang berisi teks sampah (tapi terdeteksi sebagai teks oleh parser standar). Anda harus melakukan hal berikut:Exclude Hidden Spam: Abaikan/Hapus div[style*="display:none"]. Di dalam contoh kode Anda, terdapat banyak link judi/spam yang disembunyikan menggunakan atribut ini.Exclude Sidebar: Jangan mengambil data dari div.sidebar atau aside.widget.Clean Separator: Abaikan atau gunakan sebagai pemisah elemen hr.wp-block-separator.4. Strategi JSON-LD (Jalur Alternatif)Situs ini menggunakan Rank Math, sehingga data terstruktur sangat lengkap.Selector: script.rank-math-schemaData yang didapat: BlogPosting (Headline, Keywords, datePublished, Image).Ringkasan Teknis KonfigurasiKomponenAturan / SelectorJangkar Utamadiv.post_content.entry-contentElemen Narasip, h2.wp-block-heading, blockquotePembersihan WajibHapus div[style*="display:none"] (Anti-Spam)Metadatascript[type="application/ld+json"]Karakteristik TeksNarasi panjang, deskriptif, dan informatif (Travel Guide).