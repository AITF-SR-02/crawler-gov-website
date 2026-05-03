1. kemenag

main domain:

https://kemenag.go.id/

sub domain:

https://kemenag.go.id/search?q=&page=1


example:
https://kemenag.go.id/daerah/madrasah-jadi-pelopor-literasi-mendikdasmen-puji-tradisi-menulis-di-man-1-banyuwangi-sx1ea

strategy:
Pola Crawler Kemenag (Rendered DOM)
1. Root Selector Utama

Container: div.article-content

Target Elemen: Tag p yang berada langsung di dalam container tersebut.

2. Start Marker (Pembersihan Awal)

Karakteristik: Teks lokasi dan institusi di paragraf pertama dibungkus dengan tanda hubung panjang (contoh: "Cirebon (Kemenag) ---").

Aksi: Hapus semua teks di paragraf pertama hingga tanda --- (tiga buah strip).

Regex Rekomendasi: ^.*?\-{2,}\s* (akan menangkap 2 strip atau lebih, lalu menghapusnya).

3. Cleanup & Formatting

Gunakan .get_text() untuk mengambil teks murni dari masing-masing elemen <p>.

Gabungkan teks dari setiap paragraf dan abaikan <p> yang kosong jika ada.

Ringkasan CSS Selector
CSS
div.article-content > p