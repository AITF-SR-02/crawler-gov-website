1. Puspresnas

main domain:
https://pusatprestasinasional.kemendikdasmen.go.id

sub domain:
https://pusatprestasinasional.kemendikdasmen.go.id/wara-wara

example:
https://pusatprestasinasional.kemendikdasmen.go.id/wara-wara/detail/menuju-international-geography-olympiad-igeo-2026-kemendikdasmen-matangkan-dan-seleksi-murid-di-pembinaan-tahap-ii-2026-smp

strategy:
Strategi Crawler: Svelte/Inertia (JSON Extraction)1. Root SelectorSelector: div#appTarget: Atribut data-page2. Data Path (Inside JSON)Setelah string JSON di-parse, navigasikan ke path berikut untuk mendapatkan isi berita:props -> data -> detail3. Workflow Pembersihan DataExtract: Ambil atribut data-page dari div#app.Parse: Ubah string tersebut menjadi objek JSON.Decode: Konten pada kunci detail berisi HTML terenkode (contoh: &lt;p&gt;, &quot;). Lakukan HTML Unescape untuk mengembalikan tag asli.Strip Tags: Buang semua tag HTML hasil decode untuk mendapatkan narasi teks murni (Plain Text).Clean Metadata: Terapkan pola Start Marker (tanda pisah) untuk membuang metadata lokasi/tanggal (seperti "Depok, 25 November 2025") yang ada di awal teks.Ringkasan Teknis EkstraksiKomponenAturan / LangkahAnchor Elementdiv#appSource Attributedata-pageTarget Keyprops.data.detailProcessingJSON.parse -> HTML Unescape -> Strip TagsStart CleanHapus teks hingga tanda pisah (- atau –) pertama.Catatan Khusus: Pola ini jauh lebih stabil daripada mencari CSS class visual, karena data pada props.data.detail adalah data mentah yang dikirim langsung dari server sebelum di-render oleh Svelte.


