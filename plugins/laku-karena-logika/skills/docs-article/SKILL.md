---
name: docs-article
description: Mengubah folder dokumentasi/panduan aplikasi SaaS (halaman HTML/Markdown + screenshot) menjadi seri artikel tutorial yang mudah dipahami tamu website, menyamarkan data pribadi di screenshot (nama → nama dummy, 4 digit akhir nomor telepon di-blur, foto profil tetap), lalu memposting otomatis ke CMS api.lakukan.id — kategori Docs › kelompok tutorial, gambar isi, sampul, dan status terbit — sehingga langsung tampil di menu Panduan website. Gunakan saat pengguna berkata "pelajari folder panduan ini lalu posting", "posting panduan ke CMS", "upload dokumentasi ke lakukan", "buat artikel tutorial dari dokumentasi", "jadikan panduan ini artikel di website", atau memberi folder panduan + API key Lakukan.
---

# Docs Article – Dokumentasi ke CMS Lakukan

Ubah dokumentasi aplikasi menjadi artikel tutorial di CMS `api.lakukan.id`. Artikel ini menjadi sumber menu **Panduan** yang dibangun skill `website-seo`, sehingga tamu website bisa memahami cara aplikasi SaaS bekerja.

Urutan WAJIB: input → pelajari sumber → samarkan screenshot → periksa visual → susun `artikel.json` → `cek` → posting → verifikasi publik → laporan.

Skrip ada di `scripts/`, sedangkan aturan dan detail API ada di `references/`:
- `aturan-konten.md`: judul, kategori, HTML, gambar.
- `api-lakukan.md`: endpoint dan perilaku server.
- `contoh-timebase.json`: contoh 12 artikel yang sudah disetujui user.

## 0. Input
- **Folder sumber**: halaman panduan (HTML/MD) dan folder gambarnya. Bisa juga dokumen lain yang berisi langkah pemakaian aplikasi.
- **Nama produk** (merek publik) dan **company slug publik** (header `X-Company-Slug`, mis. `timebase`). Slug ini dipakai untuk verifikasi akhir dan sebagai awalan slug kategori.
- **API key Lakukan**: minta ke user bila belum ada di percakapan. Simpan hanya di env untuk perintah yang berjalan (`export LAKUKAN_API_KEY=…`). JANGAN tulis key ke file, memori, skrip, atau commit, dan jangan ulangi key di chat.
- Alat: macOS (`swiftc` untuk OCR Vision) dan Python Pillow untuk penyamaran. Bila Pillow belum ada, buat venv di folder kerja (`python3 -m venv <kerja>/venv && <kerja>/venv/bin/pip install pillow`). `posting.py` hanya memakai Python standar.

## 1. Pelajari sumber
- Baca semua halaman. Catat struktur navigasinya, karena grup sidebar akan menjadi kelompok kategori. Catat juga urutan belajar dan gambar yang dipakai tiap bagian.
- Pisahkan bagian internal (catatan audit, tautan Drive, tanggal audit) yang **tidak** ikut diterbitkan.

## 2. Samarkan screenshot
Aturan privasi (dari user, berlaku untuk semua produk):

| Data di gambar | Perlakuan |
|---|---|
| Nama orang | Diganti **nama dummy** yang wajar dan konsisten. Nama asli yang sama selalu menjadi dummy yang sama di semua gambar, dengan panjang yang mirip. |
| Nomor telepon | **4 digit terakhir di-blur** |
| Email berisi nama | Diganti email dummy (`nama.dummy@contoh.id`) |
| Foto profil / avatar | **Tetap**: jangan diblur |

Langkah:
1. `python3 scripts/samarkan.py ocr --src <folder gambar> --kerja <folder kerja>`. Perintah ini menandai gambar placeholder di `placeholder.txt` dan menulis semua teks per gambar ke `teks.txt`, termasuk baris `!! nomor telepon terbaca`.
2. Baca `teks.txt` dan **lihat gambarnya**, lalu susun `<kerja>/peta.json` (format ada di docstring skrip):
   - `nama`: setiap nama orang beserta dummy-nya. Nama yang terpotong ("Muhammad Zain Iqbal Muza…") ditulis lengkap sebisanya; skrip mencocokkan awalan dan salah baca ringan.
   - `alias_ocr`: teks salah baca OCR yang tidak tertangkap (mis. "Rati ritra Alamsvan" → "Rafi Fitra Alamsyah").
   - `email`: email asli → dummy.
   - `blur`: kotak `[x0,y0,x1,y1]` per file untuk data yang tidak terbaca OCR tapi masih bocor. Misalnya kolom No HP yang sudah setengah diblur tapi digit akhirnya terlihat, atau baris nama yang terpotong dropdown.
3. `python3 scripts/samarkan.py terapkan --src … --kerja … --peta …/peta.json --out <folder hasil>`
4. **Periksa visual SETIAP gambar hasil** (baca gambarnya, crop/zoom bila perlu). Pastikan tidak ada nama asli tersisa (header akun, dropdown, daftar, tooltip, email), semua nomor telepon tertutup 4 digit akhirnya, dan teks dummy rapi (ukuran setara, tidak menimpa angka atau ikon). Kalau ada yang lolos, tambahkan ke peta lalu ulangi langkah 3.
5. Simpan salinan hasil ke `<folder sumber>/assets/img-anonim/` agar user punya versi aman. File asli tidak diubah.

## 3. Susun `artikel.json`
Ikuti `references/aturan-konten.md`. Ringkasnya:
- Satu halaman sumber biasanya menjadi satu artikel. Kategori **level 0 = `docs`**, **level 1 = kelompok tutorial** (slug `<produk>-<kelompok>`).
- Judul cukup nama tutorialnya, tanpa nomor seri. Slug bersih tanpa nomor.
- Tulis ulang isi sebagai tutorial untuk tamu: langkah bernomor, label UI tebal, kotak tips, dan `{{img:file|keterangan}}` memakai gambar tersamar. Tanpa tautan Sebelumnya/Selanjutnya.
- Urutan array `artikel` adalah urutan baca.

## 4. Cek lalu posting
1. `python3 scripts/posting.py cek --data artikel.json --gambar <folder hasil>`. Perintah ini memvalidasi aturan (judul bernomor, slug, panjang, gambar hilang, script) dan menampilkan rencana: kategori baru/ada/dipindah, artikel baru/update.
2. Posting menerbitkan konten publik. Bila user **sudah** meminta posting otomatis, lanjutkan. Bila belum, tampilkan ringkasan rencana dan minta satu konfirmasi.
3. `python3 scripts/posting.py posting --data artikel.json --gambar <folder hasil>` (tambahkan `--draft` bila user minta draft). Perintah ini membuat atau memperbarui kategori di bawah Docs, lalu memproses artikel dari belakang ke depan: buat draft, unggah gambar isi, unggah sampul, lalu terbitkan. Menjalankan ulang aman, karena artikel yang sudah ada diperbarui, bukan diduplikasi.
4. `python3 scripts/posting.py publik --data artikel.json --company-slug <slug>`. Perintah ini memastikan setiap kelompok tampil di API publik dengan jumlah artikel yang benar dan gambarnya HTTP 200.

### Revisi setelah terbit
- Isi, judul, ringkasan, atau kelompok berubah: ubah `artikel.json`, lalu jalankan `posting` lagi.
- Slug harus berubah (mis. dulu bernomor): buat artikel dengan slug baru, lalu `DELETE /core/v1/admin/articles/<slug lama>`. Hapus hanya artikel yang dibuat untuk seri ini.
- Struktur kategori salah: `PUT …/article-categories/<slug>` dengan `parent_id` untuk memindahkan, lalu hapus kategori perantara yang sudah kosong.

## 5. Laporan
- Pohon kategori (Docs › kelompok, beserta jumlah artikel) dan daftar judul per kelompok.
- Peta penyamaran (jumlah nama → dummy, nomor yang diblur, area manual) dan lokasi `img-anonim/`.
- Gambar placeholder yang dilewati (sebutkan namanya agar user bisa menggantinya) dan bagian sumber yang sengaja tidak diterbitkan.
- Hasil verifikasi publik. Artikel baru tampil di website setelah `website-seo` dibuild ulang dan dideploy.
