1. INDONESIA GO

main domain:
https://indonesia.go.id

sub domain:
https://indonesia.go.id/informasi/nasional

example:
https://indonesia.go.id/informasi/nasional/detail/revitalisasi-sekolah-dari-tembok-retak-ke-ekosistem-belajar-berkualitas


strategy:
1. Root Selector UtamaSelector: div.quill-content.proseTarget Elemen: Tag p yang berada di dalamnya.Selector Lengkap: div.quill-content.prose p2. Karakteristik KontenSitus ini menggunakan framework (kemungkinan Vue.js/Nuxt.js) yang terlihat dari atribut data-v-xxxx. Jangan gunakan atribut tersebut sebagai selector karena kodenya dinamis (bisa berubah tiap build). Gunakan class quill-content karena itu adalah standar container dari editor yang mereka pakai.3. Pembersihan Data (Logic)Start Marker: Walaupun di contoh gambar teks langsung mulai ke narasi, portal resmi pemerintah sering mengawali paragraf pertama dengan lokasi (contoh: JAKARTA -).Regex Fallback: ^[A-Z\s]+?\s?[\-—–]\s* (untuk membuang "JAKARTA - " jika ada).Empty Nodes: Quill sering menghasilkan tag <p><br></p> untuk spasi antar paragraf. Pastikan script kamu mengabaikan elemen p yang tidak memiliki teks murni.Ringkasan KonfigurasiKomponenAturan / SelectorJangkar Utamadiv.quill-content.proseElemen TargetpFrameworkVue/Nuxt (berdasarkan atribut data-v)MetodePlain Text (Looping tag p)