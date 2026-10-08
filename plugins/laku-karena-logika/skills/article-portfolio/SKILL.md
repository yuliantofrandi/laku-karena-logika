---
name: article-portfolio
description: Menulis artikel studi kasus PORTFOLIO Venturo untuk satu proyek software (website, web app/sistem internal, mobile app, dashboard, chatbot/AI, integrasi/API, desktop/POS) lengkap dengan tantangan, solusi, keunggulan, hasil, screenshot per aktor yang disamarkan, cover mockup, dan SEO, lalu memposting ke kategori Portfolio di CMS api.lakukan.id. Bisa juga mengupdate portfolio yang sudah terbit. Gunakan saat pengguna berkata "buat portfolio", "tulis studi kasus proyek X", "posting portfolio", "tambah proyek ke portfolio", atau "update portfolio X".
---

# Article Portfolio – Studi Kasus Proyek ke CMS Lakukan

Satu proyek = satu artikel studi kasus di kategori **Portfolio** website Venturo (CMS `api.lakukan.id`). Tujuannya meyakinkan calon klien bahwa Venturo paham masalah bisnis mereka, bukan sekadar pamer tampilan.

Skill ini **memakai ulang skrip skill lain di plugin yang sama**:
- `../article-docs/scripts/posting.py` untuk `cek`, `posting`, `ambil`, dan `publik` (detail API: `../article-docs/references/api-lakukan.md`)
- `../article-docs/scripts/samarkan.py` untuk menyamarkan screenshot
- `../article-blog/scripts/render_infografis.py` + `../article-blog/assets/infografis/` (base.css + font) untuk merender cover mockup dan diagram

Aset milik skill ini: `assets/logo-venturo.png` — **logo resmi Venturo** (PNG transparan, sudah dipotong rapat).

Dua mode:

| Mode | Kapan | Alur |
|---|---|---|
| **Portfolio baru** | "buat/posting portfolio proyek X" | Langkah 0–7 |
| **Update portfolio** | "update/revisi portfolio X", "ganti screenshot X" | `posting.py ambil --slug X --out artikel.json` → edit yang diminta → `cek` → `posting` (tanpa duplikat; field yang tidak ditulis tetap) |

Urutan WAJIB: brief → aktor & daftar visual → ambil screenshot → samarkan → cover & diagram → tulis artikel → `cek` → posting → verifikasi publik → laporan.

## 0. Brief (tanya sekali di awal, satu pesan)
- **Nama proyek** dan **jenis proyek** (lihat tabel di langkah 1; boleh lebih dari satu, mis. Website + CMS + Mobile).
- **Klien boleh disebut?** Ya → nama & logo klien. Tidak (NDA) → mode anonim: "sebuah media berita nasional", logo dan nama di screenshot disamarkan. Default: anonim bila user tidak menjawab.
- **Sumber visual**: URL frontend, URL admin (user login SENDIRI di browser; Claude tidak pernah mengetik password), link/folder screenshot mobile app, atau folder screenshot yang sudah ada.
- **Cerita proyek**: masalah awal klien, apa yang dibangun, fitur andalan, tech stack, durasi, peran Venturo (Dedicated Team / Managed Services / project).
- **Hasil nyata** bila ada: angka trafik, kecepatan, efisiensi proses, jumlah pengguna, skor PageSpeed.
- **Keyword target** (opsional; bila kosong, skill mengusulkan dari pola di langkah 6).
- **API key Lakukan**: minta bila belum ada. Pakai hanya lewat env `LAKUKAN_API_KEY`. Jangan tulis ke file atau memori, dan jangan ulangi di chat. **Company slug publik** website Venturo untuk verifikasi.

## 1. Aktor & daftar visual
Susun daftar screenshot **per aktor**: siapa saja pengguna sistem ini dan di perangkat apa. 1 aktor = 1–2 layar utamanya, sehingga gambar menceritakan alur kerja bisnis (mis. portal berita: pembaca di web publik → redaksi di CMS; HRIS: karyawan absen di HP → HRD rekap → manajer approval).

Paket visual per jenis proyek:

| Jenis proyek | Visual utama |
|---|---|
| Website (company profile, berita, e-commerce) | Homepage desktop + mobile, 1–2 halaman inti, CMS/admin, skor PageSpeed |
| Web app / sistem internal (ERP, HRIS, invoice) | Dashboard, 2–3 form/fitur andalan per aktor, laporan |
| Mobile app | 3–4 layar dalam frame HP: login → home → fitur inti → notifikasi |
| Dashboard / BI | Grafik utama, filter/drill-down, ekspor laporan |
| Chatbot / AI / WhatsApp | Screenshot percakapan, diagram alur bot, tampilan admin-nya |
| Integrasi / API / otomasi (tanpa UI) | Diagram alur sistem, sebelum vs sesudah proses, potongan log/hasil tersamar |
| Desktop / POS / IoT | Foto perangkat di lokasi (bila ada), layar kasir/kontrol |

Aturan visual:
- Total **6–10 gambar** termasuk cover. Wajib: cover mockup + minimal 1 visual per aktor utama.
- **Bukti hasil** (PageSpeed, grafik Search Console/analytics) sangat disarankan; angka sensitif klien di-blur bila klien anonim.
- Proyek tanpa UI diganti **diagram** yang dirender (langkah 4), bukan dibiarkan tanpa gambar.
- Tampilkan daftar visual ini ke user dalam satu pesan sebelum mengambil screenshot.

## 2. Ambil screenshot
- Lewat browser Chrome: desktop **1440×900**, mobile **390×844** (resize window). Tutup pop-up/cookie banner dulu dan scroll ke bagian yang paling mewakili.
- Admin area: minta user login sendiri, lalu ambil layar sesuai daftar aktor. Hindari layar yang memuat data keuangan atau kredensial.
- Mobile app: pakai screenshot dari user (atau emulator bila tersedia).
- Simpan ke `<kerja>/asli/` dengan nama berkata kunci: `<proyek>-<aktor>-<layar>.jpg`, mis. `bolong-redaksi-editor-artikel.jpg`.

## 3. Samarkan
Ikuti aturan privasi `article-docs` langkah 2 (`samarkan.py ocr` → `peta.json` → `terapkan` → **periksa visual setiap gambar**): nama orang → dummy konsisten, 4 digit akhir telepon di-blur, email → dummy, foto profil tetap. Tambahan untuk portfolio:
- Mode anonim: nama/logo klien, domain, dan nama perusahaan di header ikut diblur atau diganti lewat `blur`/`nama` di peta.
- Data finansial, token, URL internal, dan IP server selalu di-blur.
- Simpan hasil ke `<kerja>/tersamar/`.

## 4. Cover mockup & diagram
1. Salin `../article-blog/assets/infografis/*` **dan `assets/logo-venturo.png`** ke `<kerja>/render/`, lalu ganti token warna/font di `base.css` sesuai **design system Venturo** (warna logo: teal ±`#26A0AF` dan hijau ±`#93CD7A`).
2. **Cover (1600×900)**: buat `cover.html` berisi frame laptop (CSS) memuat screenshot desktop tersamar + frame HP di depannya memuat screenshot mobile, judul proyek singkat, chip jenis proyek, dan **logo Venturo** (`<img src="logo-venturo.png" alt="Venturo">`, lebar ±220–320 px). Proyek tanpa UI: cover = diagram alur yang paling mewakili.

**Aturan logo (WAJIB, semua cover & diagram):**
- Selalu pakai `assets/logo-venturo.png`. Jangan menulis "Venturo" sebagai logo teks (`.brand`), jangan menggambar ulang, dan jangan memakai logo Venturo dari sumber lain.
- Jangan mengubah warna, rasio, atau memotong bagian "EXPERT PROGRAMMERS"; ubah ukurannya hanya lewat `width`.
- Taruh di latar terang. Di latar gelap atau gradasi, letakkan logo di atas chip putih (`background:#fff;border-radius:16px;padding:14px 20px`) agar tulisan abu-abunya tetap terbaca.
- Footer infografis bawaan `article-blog` (`<span class="brand">…</span>`) diganti dengan `<img>` logo ini.
- Logo klien (bila klien boleh disebut) tampil terpisah dan lebih kecil dari logo Venturo; di mode anonim, logo klien tidak dipakai.
3. **Diagram** (bila perlu): alur sistem/integrasi atau alur bot, memakai pola `contoh-alur-keputusan.html` / `contoh-siklus.html` sebagai titik awal.
4. `python3 ../article-blog/scripts/render_infografis.py --src <kerja>/render --out <kerja>/tersamar --nama cover.html=<proyek>-cover.jpg …`
5. **Lihat setiap JPG.** Perbaiki bila screenshot terpotong janggal, teks bertumpuk, atau frame tidak proporsional.

## 5. Tulis artikel (±800–1.300 kata, HTML)
Struktur tetap untuk semua jenis proyek:
1. **Pembuka** 1–2 paragraf: siapa klien (atau anonim) dan inti solusinya. Keyword utama di paragraf pertama.
2. **Kotak ringkasan** (`<table>`): Klien · Industri · Layanan · Platform · Tech stack · Durasi.
3. `<h2>Tantangan</h2>`: masalah **bisnis** klien (bukan teknis), 2–4 poin konkret.
4. `<h2>Solusi</h2>`: dibagi `<h3>` per aktor/platform (mis. "Website untuk pembaca", "CMS untuk redaksi", "Aplikasi mobile"), masing-masing dengan screenshot-nya.
5. `<h2>Keunggulan</h2>`: 3–5 fitur pembeda, tiap poin = manfaat bagi klien + bukti visual.
6. `<h2>Hasil</h2>`: angka nyata dari user. **Jangan mengarang angka dan jangan menerbitkan placeholder**: bila angka tidak ada, tulis hasil kualitatif yang dikonfirmasi user (mis. "redaksi kini menerbitkan artikel tanpa bantuan programmer").
7. **Penutup + CTA lembut** ke halaman layanan (Dedicated Team / Managed Services) atau konsultasi. Tanpa harga, tanpa klaim superlatif, tanpa nama kompetitor.

- Gambar: `{{img:nama-file.jpg|Keterangan satu kalimat.}}` setelah paragraf yang menjelaskannya; tambahkan "Data pribadi pada gambar disamarkan" bila relevan.
- Tag yang dipakai: `h2 h3 p ul ol li strong em blockquote table tr th td img`. Tanpa `h1`, `script`, `iframe`, `style`, `on*`.
- Bahasa Indonesia profesional dan hangat, menyapa "Anda" di penutup.

## 6. SEO
- **Keyword** mengikuti jenis proyek: "jasa pembuatan [jenis aplikasi]" + industri, mis. "jasa pembuatan website berita", "jasa pembuatan aplikasi HRIS", "jasa pembuatan chatbot WhatsApp".
- **Judul** 40–60 karakter, pola *"[Jenis Solusi] untuk [Industri/Klien]: [Hasil utama]"*.
- **Slug** = nama proyek + jenis, huruf kecil, tanpa tanggal (mis. `portal-berita-bolong-cms`). Slug tidak bisa diubah setelah terbit.
- **Ringkasan** 120–160 karakter: masalah klien + hasil.
- Nama file dan keterangan gambar berkata kunci (keterangan = alt text).
- **Internal link**: 1 ke halaman layanan terkait, 1–2 ke portfolio sejenis (rujuk dengan judulnya; ambil URL dari user atau API publik).
- JSON-LD tidak ditulis di isi (CMS menolak `script`); schema `Article` + `BreadcrumbList` dibuat oleh website saat build.

## 7. `artikel.json`, cek, posting
1. Cek pohon kategori: `cek` menampilkan kategori yang ada. Rujuk kategori Portfolio yang sudah ada **tanpa mengubahnya**. Bila Portfolio punya anak kategori per jenis proyek, rujuk anak yang cocok. Jangan membuat kategori baru kecuali diminta user.
```json
{"kelompok": [{"slug": "portfolio"}],
 "artikel": [{"slug": "...", "judul": "...", "ringkasan": "...", "kelompok": "portfolio",
   "sampul": "<proyek>-cover.jpg", "status": "published", "isi": "<p>…</p>{{img:…|…}}"}]}
```
2. `python3 ../article-docs/scripts/posting.py cek --data artikel.json --gambar <kerja>/tersamar`
3. Bila user meminta "posting portfolio", langsung terbitkan. Bila user hanya minta draf atau masih ragu, pakai `--draft` atau tanyakan sekali.
4. `python3 ../article-docs/scripts/posting.py posting --data artikel.json --gambar <kerja>/tersamar`
5. `python3 ../article-docs/scripts/posting.py publik --data artikel.json --company-slug <slug>`

## 8. Laporan
- Judul, slug, kategori, panjang (kata), keyword utama, dan status terbit beserta hasil verifikasi publik.
- Daftar aktor dan gambar (nama file + isinya), termasuk apa saja yang disamarkan dan mode klien (disebut/anonim).
- Bagian yang masih lemah, mis. "Hasil" tanpa angka, dan saran data apa yang bisa ditambahkan nanti lewat mode update.
- Pengingat bahwa portfolio tampil di website setelah dibuild ulang dan dideploy.
