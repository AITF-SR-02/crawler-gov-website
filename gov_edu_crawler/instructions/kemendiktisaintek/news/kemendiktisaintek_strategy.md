1. Kemendiktisaintek

Pattern Crawler: Kemendiktisaintek (Merged)
Root Selector

Container Utama: article.rich-content atau kontainer utama di dalam div dengan kelas latar belakang bg-[#E7EDFA].

Target Elemen: Tag p untuk mengambil narasi secara berurutan.

Start Marker (Pembersihan Awal)

Tipe Siaran Pers: Hapus teks di paragraf pertama hingga tanda pisah pertama (— atau –).

Tipe Artikel/Cerita Kita: Langsung ambil teks tanpa pemotongan. Pada pola terbaru, narasi sering kali dimulai langsung dengan deskripsi (contoh: "licin dan batu-batu besar yang menyulitkan langkah...") tanpa awalan lokasi dan tanda pisah.

Logika Crawler: Jika tanda pisah tidak ditemukan dalam 50 karakter pertama pada paragraf teks pertama, maka paragraf tersebut diambil secara utuh.

Stop Marker (Batasan Akhir)

Abaikan atau hentikan pengambilan jika paragraf mengandung kata kunci: Biro Komunikasi, Sekretariat Jenderal, Laman:, atau tanda pagar (#).

Pembersihan Data (Wajib)

Metode: Gunakan fungsi .get_text() atau .innerText.

Alasan: Berdasarkan kode pada baris 79 dan 104, terdapat tag <img> yang berisi data Gambar Base64 sangat panjang yang disisipkan di antara paragraf. Mengambil teks murni akan otomatis membuang sampah kode gambar tersebut.

Optimasi Ekstraksi

Pastikan skrip ekstraksi memproses seluruh file yang tersedia dalam jalur direktori yang ditentukan tanpa memprioritaskan kurikulum tertentu.

Catatan: Pola ini sangat bergantung pada penggunaan metode pengambilan teks bersih untuk menghindari ribuan karakter kode Base64 yang muncul di tengah-tengah paragraf narasi.


