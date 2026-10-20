# Portfolio & Blog dari CMS Lakukan

## API publik (tanpa API key)

```
GET https://api.lakukan.id/api/articles?category=<slug>&limit=100&page=<n>
Header: X-Company-Slug: <company-slug>     (contoh: venturo-web)
        User-Agent: <nama website>
```

- Filter `status === 'published'` dilakukan di kode (`cms.js`), bukan lewat parameter.
- Dipanggil **di server** (Pages Functions), karena API menolak permintaan langsung dari browser (CORS) dan supaya HTML bisa diindeks.
- **Jangan pernah** menaruh API key admin di website/repo. Kalau butuh menulis ke CMS (membuat kategori, posting), itu tugas skill `article-portfolio` / `article-blog` dengan key dari environment dan izin pengguna, atau pengguna melakukannya sendiri di dashboard.
- Hasil di-cache edge 600 detik → artikel baru tampil ≤10 menit.

## Kategori

- `portfolio`: semua studi kasus.
- `portfolio-ai`: proyek yang mengandung AI. Artikel AI diberi **dua** kategori (`portfolio` dan `portfolio-ai`).
- `cms.js`: `inPortfolio` menganggap semua kategori berawalan `portfolio-` sebagai portfolio; `listPortfolio` mengambil `[cat, cat + '-ai']` lalu menggabungkan dan menghapus duplikat.
- Blog = semua artikel published **selain** kategori portfolio, dengan filter `?kategori=<slug>`.

## Route

| URL | Isi |
|---|---|
| `/portfolio/` | Semua portfolio + chip filter (Semua / AI) |
| `/portfolio/ai/` | Hanya portfolio AI, badge "AI" di kartu |
| `/portfolio/<slug>/` | Detail: Article + BreadcrumbList JSON-LD, CTA WA menyebut judul proyek, related 4 kartu |
| `/blog/`, `/blog/<slug>/` | Daftar & detail (BlogPosting JSON-LD) |
| `/sitemap.xml` | Halaman statis + `/portfolio/ai/` + semua artikel |

Halaman dirender dari `website/_templates/portfolio.html` (header/footer sama dengan halaman statis, noindex untuk template itu sendiri).

## Ukuran gambar otomatis (anti-CLS)

`functions/_lib/image-size.js` membaca beberapa byte awal gambar CMS (Range request), mengurai dimensi PNG/JPEG/GIF/WebP, lalu menambahkan `width`/`height` ke `<img>` di isi artikel. Dipakai di detail portfolio dan blog.

## Menampilkan portfolio di halaman statis

Untuk kartu portfolio di halaman layanan (bukan halaman CMS), ambil daftar artikel dari API, pilih yang relevan per halaman (AI → halaman AI, web → halaman website, dsb.), lalu tulis kartunya statis di HTML dengan link ke `/portfolio/<slug>/`. Simpan script generatornya di `tools/` proyek supaya bisa dijalankan ulang.

## Isi artikel yang baik

Judul berisi keyword, excerpt ≤280 karakter (jadi meta description), cover 1200×675, subjudul Tantangan → Solusi → Teknologi → Hasil. Penulisan pakai skill `article-portfolio`.
