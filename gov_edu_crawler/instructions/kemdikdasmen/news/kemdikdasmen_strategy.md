1. Kemdikdasmen

Pattern Berita Kemendikdasmen
Anchor Container: div.col-12.col-md-8

Text Selector: p (Ambil semua tag p di dalam kontainer di atas).

Cleaning Logic (Urutan Eksekusi):

Hapus Elemen: strong (Menghapus otomatis Lokasi di awal dan Penulis di akhir).

Filter Junk: Abaikan paragraf yang mengandung kata:

Biro Komunikasi

Laman: atau X:

# (Hashtag)

Regex Clean: Hapus karakter sisa di awal teks: ^[–\-\s]+ (menghapus tanda strip/spasi yang tertinggal setelah lokasi dibuang).

Anti-Junk: Gunakan .text atau .innerText, jangan .html untuk menghindari kode gambar Base64.

Cara Cepat Analisis Website Lain (Tips):
Start Point: Cari div atau article yang membungkus seluruh tulisan.

Body Pattern: Biasanya teks bersih ada di tag p yang merupakan anak langsung dari kontainer utama.

Junk Pattern: Cari kata kunci statis di bagian bawah (seperti: "Editor", "Source", "Sosial Media") sebagai Stop-Word)

2. Vokasi Kemdikdasmen

Pattern Berita Vokasi
Anchor Container: div.entry-content

Text Selector: p (Ambil teks dari semua tag p).

Cleaning Logic (Urutan Eksekusi):

P1 (Start): Hapus teks hingga tanda pisah pertama (- atau –).

Contoh: Menghapus "Jakarta, Ditjen Vokasi PKPLK - ".

P-Last (End): Hapus kode inisial di dalam kurung di akhir paragraf terakhir.

Contoh: Menghapus "(Nan/NA/AS)".

Empty Tags: Abaikan paragraf yang hanya berisi <br> atau spasi kosong.

Anti-Junk: Gunakan .get_text() untuk mengabaikan tag <span> dan style yang sangat banyak di website ini.

Panduan Pembersihan (Regex):
Awal: ^.*?[-–]\s* (Hapus lokasi/instansi).

Akhir: \s*\([^)]*\)$ (Hapus inisial penulis).

Tips Cepat Analisis:
Website tipe CMS ini sering memiliki teks "tersembunyi" di dalam span. Selama Anda menargetkan div.entry-content dan mengambil elemen p di dalamnya, teks narasi akan didapat secara urut. Tutup ekstraksi sebelum atau tepat pada paragraf yang mengandung kode inisial penulis.


3. Inspektorat Jenderal
Pattern Berita Itjen (Merged)
Root Container: div.entry-content

Target Elements: p, li, blockquote (Ambil semua agar daftar/kutipan tidak hilang).

Start Marker: Cari paragraf teks pertama, hapus semua karakter hingga tanda pisah pertama (—, –, atau -).

Regex: ^.*?[—–-]\s*

Stop Marker: Abaikan teks jika menemukan kata kunci: Penulis:, Editor:, Foto:, atau Sumber:.

Media Filter: Lewati (skip) tag p yang berisi elemen img.

Extraction: Gunakan .get_text() atau .innerText untuk mendapatkan teks bersih dari sisa tag HTML (seperti span, em, strong).

Kunci Keberhasilan: Gunakan tanda pisah sebagai patokan awal teks, bukan tag gaya (bold/italic), karena Itjen sering mengganti-ganti format gaya di awal berita.


4. Badan Bahasa
Pattern Berita Badan Bahasa (Merged & Updated)
Root Container: div.article_body_wrap

Target Elements: p

Start Marker (Pembersihan Awal):

Pola Umum: Narasi utama selalu dimulai setelah tanda pisah "–" (en-dash) atau "—" (em-dash).

Aksi: Cari tanda pisah pertama tersebut pada paragraf-paragraf awal. Hapus semua teks di depan tanda tersebut (untuk membuang Lokasi, Tanggal, atau Header "Siaran Pers").

Regex: ^.*?–\s* atau ^.*?—\s*

Stop Marker (Pembersihan Akhir):

Hentikan pengambilan teks jika bertemu paragraf yang mengandung kata kunci:

Biro Komunikasi dan Hubungan Masyarakat

Laman:

X: atau Instagram:

# (Hashtag)

Skip Elements (Anti-Junk):

Abaikan paragraf yang hanya berisi gambar (img).

Abaikan paragraf kosong (hanya berisi &nbsp; atau <br>).

Abaikan paragraf yang isinya sangat pendek (di bawah 10 karakter) sebelum narasi utama dimulai.

Metode Ekstraksi:

Wajib menggunakan .get_text() atau .innerText.

Alasan: Badan Bahasa sering menyisipkan gambar di bagian paling bawah artikel dalam format tag <p><img></p>. Mengambil teks saja akan otomatis mengabaikan elemen visual tersebut.

Perbandingan dengan Pola Sebelumnya:
Update: Berita di Badan Bahasa tidak selalu memiliki 3 baris header "Siaran Pers". Beberapa langsung dimulai dengan "Jakarta, [Tanggal] – ".

Solusi Gabungan: Gunakan tanda pisah "–" sebagai patokan universal untuk memulai narasi berita, terlepas dari ada atau tidaknya header "Siaran Pers".

Tips Singkat untuk Semua Website Kemendikdasmen:
Hampir semua subdomain (Vokasi, Itjen, Badan Bahasa) menggunakan Tanda Pisah (Dash) di paragraf awal sebagai pemisah antara metadata lokasi/instansi dengan isi berita. Ini adalah Start Marker yang paling stabil.


5. Pusat Perlindungan Bahasa
Pattern Crawler: Rumah Pusbin
1. Root Selector

Container: main#main .container

Element: p (Ambil semua teks di dalam tag p).

2. Start Marker (Pembersihan Awal)

Kondisi: Jika di paragraf pertama terdapat tanda pisah (—, –, atau -).

Aksi: Hapus teks dari awal hingga tanda pisah tersebut.

Regex: ^.*?[—–-]\s*

Note: Jika tidak ada tanda pisah dalam 50 karakter pertama, jangan dipotong (berarti langsung narasi).

3. Stop Marker (Batasan Akhir)

Aksi: Berhenti atau hapus paragraf jika mengandung kata kunci:

Biro Komunikasi

Sekretariat Jenderal

Laman:

# (Hashtag)

4. Data Cleanup (Wajib)

Method: Gunakan .get_text() atau .innerText untuk mengekstrak teks saja.

Tujuan:

Menghapus nested tags (Pusbin sering pakai <p><p>teks</p></p>).

Membuang sampah kode Microsoft Word (mso-fareast, dll).

Mengabaikan gambar (Base64) dan tombol "Kembali".

5. Filter Junk

Abaikan elemen p yang hanya berisi spasi kosong (&nbsp;) atau elemen yang membungkus gambar (img).


5. Badan Standar, Kurikulum, dan Asesmen Pendidikan
Kementerian Pendidikan Dasar dan Menengah

Pattern Crawler: BSKAP Kemendikdasmen (Merged)
1. Root Selector

Container: div.col-xl-6 div[style*="word-break: break-word"]

Element: p (Ambil semua elemen paragraf di dalam kontainer tersebut).

2. Start Marker (Pembersihan Awal)

Aksi: Hapus teks di paragraf pertama hingga tanda pisah pertama (– atau -).

Karakteristik: Lokasi dan tanggal biasanya dibungkus tag <strong> atau <b> tepat sebelum tanda pisah.

Regex: ^.*?[–-]\s*

3. Stop Marker (Batasan Akhir)

Aksi: Berhenti mengambil teks jika paragraf mengandung kata kunci berikut:

Biro Komunikasi

Sekretariat Jenderal

Laman:

# (Hashtag)

4. Data Cleanup

Method: Gunakan .get_text() atau .innerText.

Filter:

Abaikan paragraf yang hanya berisi spasi kosong atau &nbsp;.

Abaikan elemen gambar atau metadata di luar kontainer utama.

Pastikan entitas HTML seperti &#039; (kutipan) terkonversi dengan benar menjadi teks biasa.

5. Identifikasi Khusus
Website BSKAP menggunakan atribut word-break: break-word pada pembungkus teks narasinya. Ini adalah kunci selector yang paling stabil untuk membedakan antara konten berita dengan elemen UI lainnya.