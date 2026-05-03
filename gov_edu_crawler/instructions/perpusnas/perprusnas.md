1. Perprusnas

main domain: https://perpusnas.go.id/berita

sub domain:
https://perpusnas.go.id/berita


example:
https://perpusnas.go.id/berita/peringatan-400-tahun-syekh-yusuf-al-makassari-perpusnas-tegaskan-komitmen-melestarikan-manuskrip-ulama-nusantara

strategy:
1. CSS Selector (Target Utama)

Selector Wajib: div.entry-content p

Alasan Detail: Di dalam halaman Perpusnas terdapat lebih dari satu div.entry-content (satu untuk teks berita, satu untuk galeri gambar). Dengan menargetkan langsung tag <p> di dalam entry-content, crawler Anda akan otomatis mengambil narasi teks dan mengabaikan bagian galeri (karena galeri menggunakan struktur div > img, bukan p).

2. Metode Pengambilan (Plain Text)

Metode: Loop setiap elemen <p>, ambil plain text-nya (.get_text() atau .innerText), lalu gabungkan dengan enter (\n).

Alasan Detail: CMS Perpusnas menghasilkan HTML kotor (WYSIWYG bawaan Microsoft Word) dengan ratusan tag <span> dan inline CSS (contoh: style="font-family: trebuchet ms; font-size: 12pt;"). Mengambil teks murni akan langsung merontokkan semua sampah kode visual ini.

3. Start Marker (Pembersihan Awal)

Pola Teks: Selalu diawali dengan [Nama Daerah] - Humas Perpusnas, (contoh: Banten - Humas Perpusnas, )

Tindakan: Hapus pola ini dari paragraf pertama agar teks langsung fokus ke inti berita.

Regex: ^.*?\-\s*Humas Perpusnas,\s*

4. End Marker (Pembersihan Akhir)

Pola Teks: Selalu diakhiri dengan tiga bintang dan inisial staf humas di dalam kurung (contoh: *** (AKN/Ed:DRS/Dok:PHP)).

Tindakan: Hapus dari akhir teks (paragraf terakhir).

Regex: \s*\*{3}\s*\(.*?\)$