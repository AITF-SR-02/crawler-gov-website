1. Puspresnas

main domain:
https://pusatprestasinasional.kemendikdasmen.go.id

sub domain:
https://pusatprestasinasional.kemendikdasmen.go.id/wara-wara

example:
https://pusatprestasinasional.kemendikdasmen.go.id/wara-wara/detail/menuju-international-geography-olympiad-igeo-2026-kemendikdasmen-matangkan-dan-seleksi-murid-di-pembinaan-tahap-ii-2026-smp

strategy:
Strategi Crawler: Svelte/Inertia (JSON Extraction)1. Root SelectorSelector: div#appTarget: Atribut data-page2. Data Path (Inside JSON)Setelah string JSON di-parse, navigasikan ke path berikut untuk mendapatkan isi berita:props -> data -> detail3. Workflow Pembersihan DataExtract: Ambil atribut data-page dari div#app.Parse: Ubah string tersebut menjadi objek JSON.Decode: Konten pada kunci detail berisi HTML terenkode (contoh: &lt;p&gt;, &quot;). Lakukan HTML Unescape untuk mengembalikan tag asli.Strip Tags: Buang semua tag HTML hasil decode untuk mendapatkan narasi teks murni (Plain Text).Clean Metadata: Terapkan pola Start Marker (tanda pisah) untuk membuang metadata lokasi/tanggal (seperti "Depok, 25 November 2025") yang ada di awal teks.Ringkasan Teknis EkstraksiKomponenAturan / LangkahAnchor Elementdiv#appSource Attributedata-pageTarget Keyprops.data.detailProcessingJSON.parse -> HTML Unescape -> Strip TagsStart CleanHapus teks hingga tanda pisah (- atau –) pertama.Catatan Khusus: Pola ini jauh lebih stabil daripada mencari CSS class visual, karena data pada props.data.detail adalah data mentah yang dikirim langsung dari server sebelum di-render oleh Svelte.


2. BBGTJATIM

main domain:
https://bbgtkjatim.kemendikdasmen.go.id

sub domain:
https://bbgtkjatim.kemendikdasmen.go.id/news/


example:
https://bbgtkjatim.kemendikdasmen.go.id/news/buku-saku-7-kaih-dan-lagu-kicau-bantu-guru-paud-dan-pnf-perkuat-karakter-dan-numerasi-anak#body


Strategi Crawler: BBGTK Jatim (Data-Driven)Root SelectorSelector: div#appTarget: Atribut data-pageData Path (JSON)Setelah melakukan JSON.parse pada atribut tersebut, navigasikan ke:props $\rightarrow$ result $\rightarrow$ contentLangkah Ekstraksi & PembersihanParse & Decode: Ambil isi props.result.content yang berisi HTML terenkode (misal: &lt;div&gt;, &quot;).Strip Tags: Gunakan parser untuk membuang tag HTML dan mengambil narasi teks murni.Start Marker: Hapus metadata lokasi di awal paragraf pertama hingga tanda pisah.Contoh pada gambar: Teks dimulai dengan "Batu, BBGTK Jatim —".Regex: ^.*?\u2013\s* (menggunakan kode Unicode untuk en-dash yang terlihat di JSON).Junk Filter (Base64): Pada gambar terlihat kode Base64 Gambar (data:image/jpeg;base64...) yang sangat panjang terselip di dalam string konten. Ekstraksi teks murni (Plain Text) secara otomatis akan membuang sampah kode ini.Ringkasan Teknis KonfigurasiKomponenAturan / LangkahAnchor Elementdiv#appSource Attributedata-pageTarget Data Pathprops.result.contentProcessingJSON.parse $\rightarrow$ HTML Unescape $\rightarrow$ Strip TagsStart CleanHapus hingga tanda pisah (\u2013)Kelebihan Strategi: Karena data diambil langsung dari state aplikasi (props), Anda tidak akan terganggu oleh perubahan tata letak visual (layout) selama struktur pengiriman data dari backend tetap sama.

