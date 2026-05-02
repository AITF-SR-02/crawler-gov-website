1. Kemensos

Berikut adalah strategi **CSS Selector** gabungan (merged) khusus untuk **Portal Kemensos**:

### **Pattern Berita Kemensos (Merged)**

*   **Root Selector:** `h5.text-content`.
*   **Child Selector:** `div` atau `p`.
    *   *Tips:* Gunakan `h5.text-content > *` untuk menangkap keduanya secara fleksibel.
*   **Start Marker:** Cari tanda pisah **"—"** (em-dash) atau **"-"** (strip) pada elemen pertama.
    *   **Aksi:** Hapus semua teks sebelum tanda tersebut (Lokasi & Nama Menteri/Wamen).
    *   **Regex:** `^.*?[—-]\s*`.
*   **Stop Marker:** (Sesuai pola umum Kemendikdasmen) Berhenti jika menemukan kata kunci: `Biro Komunikasi`, `Laman:`, atau `Instagram:`.
*   **Cleanup Logic:**
    *   **Wajib:** Gunakan `.get_text()` atau `.innerText` untuk menyatukan teks dari dalam tag `<span>` atau `<b>`.
    *   **Filter:** Abaikan elemen yang hanya berisi `<br />` atau spasi kosong (`&nbsp;`).

---

### **Ringkasan Teknis Konfigurasi**

| Komponen | Aturan / Selector |
| :--- | :--- |
| **Anchor** | `h5.text-content` |
| **Target** | `div` atau `p` |
| **Start Clean** | Regex `^.*?[—-]\s*` |
| **Method** | Plain Text (Stripping HTML) |

**Catatan Khusus:** Portal ini unik karena menggunakan tag **`h5`** sebagai pembungkus utama seluruh tubuh berita, bukan `div` atau `article` seperti subdomain pendidikan.


