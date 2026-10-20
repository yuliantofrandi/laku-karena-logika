---
name: article-blog
description: Menulis satu artikel BLOG edukatif untuk produk SaaS (mis. TimeBase) dari topik atau materi user — kebijakan internal, SOP, aturan perusahaan, data — lengkap dengan 3 infografis bermerek (dirender dari template HTML lewat Chrome headless) dan screenshot produk yang disamarkan, lalu memposting otomatis ke kategori Blog di CMS api.lakukan.id sehingga tampil di menu /blog website. Bisa juga mengupdate artikel blog yang sudah terbit. Gunakan saat pengguna berkata "buatkan blog", "tulis artikel blog tentang X", "input ke blog", "posting artikel blog", "buat blog dari aturan/SOP ini", "artikel edukasi untuk karyawan/pelanggan", atau "update artikel blog X".
---

# Article Blog – Artikel Edukatif ke Blog CMS Lakukan

Tulis satu artikel blog yang mengedukasi pembaca, misalnya "agar karyawan profesional bekerja WFA", lengkapi dengan infografis bermerek yang informatif, lalu terbitkan ke kategori **Blog** di CMS `api.lakukan.id`. Website produk (`website-seo`) menampilkannya di /blog setelah dibuild ulang.

Skill ini **memakai ulang skrip dari skill `article-docs`** di plugin yang sama:
- `../article-docs/scripts/posting.py` untuk `cek`, `posting`, `ambil`, dan `publik`
- `../article-docs/scripts/samarkan.py` untuk menyamarkan screenshot

Skrip milik skill ini sendiri: `scripts/render_infografis.py` dan template `assets/infografis/`. Aturan lengkap ada di `references/aturan-blog.md`, dan contoh yang sudah disetujui di `references/contoh-blog-timebase.json`.

Urutan WAJIB: input → kerangka & sudut pandang → tulis isi → infografis → screenshot tersamar → `artikel.json` → `cek` → posting → verifikasi publik → laporan.

## 0. Input
- **Topik/tujuan** artikel dan **materi** dari user (aturan, SOP, data) bila ada.
- **Produk**: nama merek, company slug publik (mis. `timebase`), dan folder website bila ada (untuk warna/font dari `static/style.css` + `static/fonts/`).
- **API key Lakukan**: minta bila belum ada di percakapan. Pakai hanya lewat env `LAKUKAN_API_KEY`. Jangan tulis ke file atau memori, dan jangan ulangi di chat.
- Alat: Google Chrome/Chromium (render infografis) dan Python. Pillow opsional; di macOS ada `sips` sebagai cadangan.

## 1. Kerangka & sudut pandang
- Tentukan kata kunci utama, judul (40–60 karakter), slug, dan ringkasan (120–160 karakter) sesuai `aturan-blog.md`.
- Susun 4–6 bagian `<h2>`. Pola yang sudah disetujui untuk materi kebijakan: *apa arti X* → *contoh kebijakan* → *ritme/langkah praktis* → *buktikan dengan data (produk)* → *peran atasan/pihak lain* → *checklist* → *kesimpulan + CTA lembut*.
- Materi internal user disajikan sebagai **contoh kebijakan** tanpa nama perusahaan atau sistem internal (kecuali user meminta), dengan angka dan syarat tetap persis.

## 2. Tulis isi
- Bahasa Indonesia yang hangat dan menyapa "Anda", sekitar 900–1.500 kata. Kata kunci ada di paragraf pertama.
- Produk tampil di satu bagian sebagai bukti nyata, misalnya data Active/Idle/Distraction di TimeBase. Tanpa harga, tanpa klaim superlatif, tanpa nama kompetitor.
- Tandai posisi gambar dengan `{{img:nama-file.jpg|Keterangan satu kalimat.}}`.

## 3. Infografis (3 buah, WAJIB bervariasi)
1. Salin `assets/infografis/*` ke folder kerja. Ganti token warna dan font di `base.css` sesuai merek produk; bila produknya TimeBase, biarkan default.
2. **Pilih 3 pola yang berbeda** dari katalog 9 pola di `references/aturan-blog.md` (bagian "Variasi infografis"), sesuai isi tiap bagian artikel — bukan selalu kartu pilar + timeline + hindari/lakukan. Aturannya:
   - 3 pola dari **kelompok yang berbeda** (ringkasan, proses, perbandingan/keputusan, data/checklist).
   - Minimal **2 tema latar berbeda** (terang, `tema-lembut`, `tema-gelap`, `tema-gradasi`) lewat kelas di `<body>`.
   - **Sampul dirotasi**: jangan selalu kartu pilar. Bila artikel blog sebelumnya diketahui (folder kerja lama, `posting.py ambil`, atau halaman /blog), hindari pola sampul dan kombinasi 3 pola yang sama dengan artikel terakhir.
   Ganti isinya sesuai artikel dengan teks singkat dan footer logo teks + tagline merek.
3. `python3 scripts/render_infografis.py --src <kerja> --out <folder gambar> --nama a.html=infografis-<kata-kunci>.jpg …`
4. **Lihat setiap JPG**. Perbaiki HTML lalu render ulang bila ada teks terpotong, judul dua baris yang mendesak isi, atau ruang kosong janggal.

## 4. Screenshot produk (1–2 buah)
- Pakai screenshot yang relevan dengan bagian produk. Bila sudah ada versi tersamar (mis. `assets/img-anonim/` dari `article-docs`), salin dan beri nama berkata kunci.
- Screenshot baru wajib disamarkan dengan `../article-docs/scripts/samarkan.py` (nama → dummy, 4 digit akhir telepon di-blur, foto profil tetap), lalu diperiksa visual.

## 5. `artikel.json`, cek, posting
```json
{"kelompok": [{"slug": "blog"}],
 "artikel": [{"slug": "...", "judul": "...", "ringkasan": "...", "kelompok": "blog",
   "sampul": "infografis-....jpg", "status": "published", "isi": "<p>…</p>{{img:…|…}}"}]}
```
- `{"slug": "blog"}` tanpa `nama` berarti rujukan, sehingga kategori Blog tidak diubah.
- `python3 ../article-docs/scripts/posting.py cek --data artikel.json --gambar <folder gambar>`
- Bila user meminta "buatkan/input/posting blog", langsung terbitkan (`status: published`). Bila user hanya minta draf atau masih ragu, pakai `--draft` atau tanyakan sekali.
- `python3 ../article-docs/scripts/posting.py posting --data artikel.json --gambar <folder gambar>`
- `python3 ../article-docs/scripts/posting.py publik --data artikel.json --company-slug <slug>`

### Update artikel blog
`posting.py ambil --slug <slug> --out artikel.json` → edit bagian yang diminta (gambar baru via `{{img:…}}`, `sampul` hanya bila diganti) → `cek` → `posting`. Artikel diperbarui tanpa duplikat, dan field yang tidak ditulis tetap.

## 6. Laporan
- Judul, slug, kategori, panjang (kata), dan status terbit beserta hasil verifikasi publik.
- Alur bagian (`h2`) dan daftar gambar (3 infografis + screenshot) beserta isinya, termasuk **pola + tema** tiap infografis.
- Penyesuaian dari materi user, misalnya nama internal yang disamarkan menjadi "contoh kebijakan", dan tawarkan opsi menyebut nama perusahaan bila user mau.
- Pengingat bahwa artikel tampil di /blog setelah website dibuild ulang dan dideploy.
