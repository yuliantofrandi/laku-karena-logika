# Standar artikel Blog (CMS Lakukan)

Acuannya artikel pertama user di Blog Timebase: `/blog/kerja-wfa-profesional`. User (4 Okt 2026) membandingkan artikel hasil ekspor halaman "(SEO saja)" dengan acuan ini: "susunan dari 4 artikel yang dibuat tidak sebagus artikel pertama… pelajari pattern-nya dan terapkan, termasuk gambarnya, buat jadi lebih bagus seperti infografis". Setiap artikel Blog yang ditulis atau diekspor wajib mengikuti pola ini. Contohnya ada di `references/contoh-artikel-blog/`.

## Susunan teks (±900–1.100 kata)
1. **Dua paragraf pembuka.** Paragraf pertama berisi hook masalah nyata pembaca dengan keyword utama ditebalkan. Paragraf kedua berbunyi "Artikel ini membahas …" sebagai daftar isi singkat dalam kalimat.
2. **6–8 H2** berbentuk pertanyaan atau pernyataan jelas. Tiap section berisi:
   - 1–2 paragraf pendek;
   - **infografis** `<img alt="…">`, langsung diikuti **keterangan miring** `<p><em>…</em></p>` (satu kalimat yang merangkum gambar);
   - daftar `<ol>`/`<ul>` dengan **lead tebal** (`<li><strong>Poin.</strong> penjelasan</li>`), atau tabel.
3. **Kotak** `<blockquote>`, minimal satu dari masing-masing:
   - `💡 <strong>Tips:</strong> …` untuk saran praktis;
   - `ℹ️ <strong>Catatan:</strong> …` untuk batasan atau kejujuran produk (mis. "bukan nasihat hukum", "Idle bisa berarti membaca").
4. **Tabel checklist** "Pertanyaan | Kenapa penting" menjelang akhir.
5. **"Pertanyaan yang sering diajukan"** (opsional, H3 + jawaban singkat) untuk keyword long-tail.
6. **"Kesimpulan"**: satu paragraf rangkuman dan satu paragraf ajakan lembut dengan link ke halaman produk, Harga, atau menu Panduan. Tidak memakai tombol, karena CTA penutup sudah dipasang oleh halaman blog.
7. Fakta hanya dari BKB atau isi website. Jangan mengarang angka atau fitur.

## Infografis (3 per artikel, 1600×900 PNG) — `scripts/infografis.py`
- **Gaya:**
  - latar putih dengan gradasi lembut ungu (kanan atas) dan peach (kiri bawah);
  - label ungu kapital dengan garis gradasi;
  - judul Montserrat 800, dengan bagian `sorot` memakai gradasi brand;
  - footer: logo + "ACCOUNTABILITY EVERYWHERE" di kiri, keterangan kecil di kanan.
- **Tipe:**
  - `kartu`: 3–5 kartu berikon bulat gradasi + label + judul + isi + pill tag;
  - `banding`: dua kolom ✗/✓ atau netral/plus dengan baris bernomor;
  - `alur`: langkah bernomor di garis gradasi, kartu dengan poin, satu langkah bisa diberi badge "Wajib/Penting";
  - `dua`: tabel dua kolom sejajar (mis. HRIS vs monitoring).
- **Spesifikasinya JSON** (`infografis-contoh.json`), dirender lewat Chrome headless:
  ```bash
  python3 tools/infografis.py export/blog-v2/infografis.json export/blog-v2/gambar
  ```
- **Infografis pertama = sampul** (`cover`). Seperti artikel acuan, sampul **juga tampil di section-nya** (`"sampul_di_isi": true`).
- Periksa setiap PNG secara visual: tidak ada teks terpotong, tidak ada ruang kosong besar, dan kolom seimbang (tambah baris bila satu kolom lebih pendek).

## Unggah / perbarui
```bash
LAKUKAN_API_KEY=… python3 tools/unggah_blog.py --sumber=export/blog-v2 --perbarui [slug…]
```
Folder sumber berisi `<slug>.json` (title, slug, excerpt, content, cover, images, sampul_di_isi) + `gambar/*.png`. File `infografis.json` otomatis dilewati.
