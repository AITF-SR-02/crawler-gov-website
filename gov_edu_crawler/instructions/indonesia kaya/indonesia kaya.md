1. Indonesia Kaya

main domain:
https://indonesiakaya.com


sub domain:
https://indonesiakaya.com/pustaka-indonesia/

https://indonesiakaya.com/pustaka-indonesia-category/kuliner/
https://indonesiakaya.com/pustaka-indonesia-category/kesenian/
https://indonesiakaya.com/pustaka-indonesia-category/pariwisata/
https://indonesiakaya.com/pustaka-indonesia-category/tradisi/



example:
https://indonesiakaya.com/pustaka-indonesia/legenda-batu-bagga/

strategy:
1. Target Utama (Content)Root Selector: div#main-content.Elemen Narasi: Semua tag p dan blockquote yang merupakan anak langsung dari root.Metode Ekstraksi: Ambil teks murni (plain text) dari elemen-elemen tersebut dan gabungkan.2. Elemen yang Harus Dibuang (Exclusion)Situs ini menyisipkan elemen promosi di tengah konten. Untuk mendapatkan data yang "bersih" bagi LLM, Anda harus mengabaikan/menghapus selector berikut sebelum mengambil teks:div#main-gallery : Berisi slider gambar yang tidak memiliki narasi panjang.div.baca-juga : Kotak rekomendasi artikel yang sering terselip di paragraf ke-2 atau ke-3.div.artikel-terkait : Daftar artikel di bagian bawah teks.div.infoMore : Informasi teknis penulis, fotografer, dan sumber referensi.3. Metadata (Data Pendukung)Judul: div.section__text--head h3.Deskripsi Singkat: p.text-italic yang berada tepat di bawah judul.Kategori Utama: small.text-underline-none a (misal: "Kesenian").Tagar (Keywords): div.tag a (untuk klasifikasi topik tambahan).Ringkasan Strategi TeknisKomponenSelector / AturanKontainer Intidiv#main-contentAksi PembersihanHapus div#main-gallery, div.baca-juga, div.infoMoreAksi EkstraksiAmbil .get_text() dari semua p dan blockquote yang tersisaPenanganan LinkBuang tag <a> tapi simpan teks di dalamnya (misal: <a href="...">Malin Kundang</a> menjadi "Malin Kundang").

