# Standar menu Panduan (artikel dari API Lakukan)

Disetujui user pada 4 Okt 2026 untuk website Timebase. Instruksi user: "tambahkan menu panduan, artikelnya diambil dari api.lakukan.id … ada kategorinya juga, pastikan tampilannya memuat per kategori juga".

## Sumber data
- API publik: `https://api.lakukan.id/api`, dengan header `X-Company-Slug: <slug produk>` (contoh: `timebase`). Company id (mis. `venturo`) tidak dipakai di header; slug produk yang menentukan marketplace.
- Endpoint yang dipakai:
  - `GET /article-categories` → pohon kategori (`children`, `sort_order`, `description`).
  - `GET /articles?limit=100&page=N` → daftar artikel (`meta.pagination`).
  - `GET /articles/<slug>` → isi HTML lengkap (`content`, `cover_url`, `author`, `updated_at`).
- Hanya **kategori anak dari `kategori_induk`** (default `docs`) yang ditampilkan. Artikel di kategori induk itu sendiri atau di kategori lain (mis. Blog, artikel uji "aaa"/"ccc") dilewati.
- Konfigurasi di `site.json`: `"panduan": {"api": …, "company_slug": "<slug>", "kategori_induk": "docs"}`. Bila `company_slug` kosong, fitur dilewati. Tambahkan `["/panduan", "Panduan"]` sebagai menu utama terakhir di `nav`.
- Build menyimpan data ke `data/panduan-cache.json`. Bila API gagal, build memakai cache (WARNING).
- Artikel baru di CMS baru tampil setelah build ulang dan deploy.

## Struktur halaman (`scripts/panduan.py`)
- **`/panduan` (hub):**
  - Hero ringkas: badge "Pusat bantuan", H1 "Panduan <Brand>", dan satu kalimat pembuka.
  - Chip kategori dengan jumlah artikel.
  - **Satu kartu per kategori**: ikon bulat gradasi, nama kategori, deskripsi, daftar judul artikel (baris bergaris + ›), dan link "N panduan →".
  - 5 kategori disusun 3 + 2.
  - Bukan grid sampul per kategori: kategori yang hanya berisi 1 artikel akan menyisakan ruang kosong. User menolak ruang kosong.
- **`/panduan/<kategori>`:**
  - Chip kategori, dengan chip aktif berwarna gelap.
  - Grid kartu artikel: sampul 16:9, judul, ringkasan maksimal 3 baris.
- **`/panduan/<kategori>/<artikel>`:**
  - Layout dokumen seperti halaman legal: navigasi kiri per kategori (grup aktif terbuka, artikel aktif disorot) dan "Daftar panduan" tertutup di mobile.
  - Isi artikel: penulis · tanggal diperbarui → sampul → isi HTML (dibersihkan dari script/iframe/on*).
  - Gambar isi memakai lazy load. Blockquote tampil sebagai kotak tips.
  - Di bawah artikel ada tombol Sebelumnya/Berikutnya dalam kategori yang sama.
- **URL kategori** membuang awalan slug produk: `timebase-memulai` → `/panduan/memulai`.
- **Menu "Panduan"** tetap aktif di semua sub-halaman.
- **Footer:**
  - Kolom tambahan "Panduan" berisi daftar kategori + "Semua panduan".
  - Kolom artikel SEO berganti nama menjadi "Artikel".
- **SEO:** semua halaman panduan index dan masuk sitemap. JSON-LD berisi BreadcrumbList bertingkat, dan halaman artikel juga memakai `Article`.
- **Di mobile:** chip kategori satu baris yang bisa digeser, dan chip aktif otomatis digeser ke dalam layar.

## Tidak boleh
- Mengedit isi artikel dari CMS di build. Penulisan merek seperti "TimeBase" diikuti apa adanya; perbaikan dilakukan di CMS.
- Menjalankan cek kata minimum atau ilustrasi wajib halaman SEO pada halaman panduan.
