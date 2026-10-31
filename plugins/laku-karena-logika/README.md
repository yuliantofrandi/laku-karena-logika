# Laku karena logika — AI Marketing OS

Rangkaian skill Claude yang mengubah **pengetahuan produk** jadi **output marketing** untuk bisnis SaaS. Dibangun berlapis: dari mendokumentasikan strategi bisnis, sampai memproduksi materi marketing yang konsisten dengannya.

Semua skill di sini berbahasa Indonesia, berbasis pola yang sudah divalidasi lewat produk nyata (Timelog, Humanis).

## Install

```
/plugin marketplace add yuliantofrandi/laku-karena-logika
/plugin install laku-karena-logika@laku-karena-logika
```

## Skill di dalamnya

### `business-knowledge`
Menyusun, mengisi, merevisi, dan mengaudit **Business Knowledge Base (BKB)** satu produk SaaS — dokumen strategi bisnis yang jadi sumber kebenaran untuk semua materi marketing di hilir.

Struktur BKB (5 section):
1. **Business Overview** — identitas, vision, mission
2. **Brand Strategy** — category, DNA & pembeda berlevel, positioning, tagline, opportunity
3. **Pricing Plan** — tier, diskon volume, add-on
4. **Product-to-Value Mapping** — problem → benefit → business outcome
5. **Target Customer Profile** — segmen + buyer persona

Prinsip yang dijaga: satu fakta satu rumah (anti-duplikasi), tidak mengarang fakta (`[INPUT-NEEDED]` hanya untuk fakta yang belum ada; tanpa penanda ragu `[?]`), keputusan strategis diisi rekomendasi terbaik agar produk laris, dan keputusan strategis (positioning, target) disertai alasannya — harga tidak wajib beralasan karena kelayakannya diuji `business-reviewer`.

### `business-reviewer`
Menilai dan memberi **skor** pada BKB, lalu menguji strateginya lawan lanskap kompetitor nyata (**competitive analysis**) — semuanya sebagai satu laporan review, **read-only** (tidak mengedit BKB). Sementara `business-knowledge` menulis & merapikan dokumen, skill ini berdiri di luar sebagai kritikus: skor 100 poin per dimensi, temuan (cacat penulisan vs celah strategis), dan analisis kompetitor. BKB sengaja tidak memuat kompetitor (tanpa merek, harga, atau fitur); seluruh data & analisis kompetitor tinggal di laporan review bertanggal ini.

### `keyword-research`
Riset buying keyword di Google Ads Keyword Planner (lewat browser), lalu susun jadi Excel siap eksekusi: keyword plan, page brief (title/meta/H1/slug), dan negative keyword. Skill hilir — Langkah 0-nya membaca brief/BKB produk untuk menilai relevansi keyword, jadi melanjutkan rantai dari `business-knowledge`.

> **Catatan lingkungan:** skill ini butuh **Claude-in-Chrome** (otomasi browser) dan skill **`anthropic-skills:xlsx`**, serta menyimpan hasil ke `/mnt/user-data/outputs/` — jadi ditujukan untuk lingkungan **claude.ai/Chat**, bukan alur file lokal Cowork seperti dua skill di atas.

### `website-seo`
Membangun website marketing statis dari **BKB + keyword plan**: beranda sebagai **sales page** (AIDA + PAS), halaman Prioritas 1 sebagai landing Ads + SEO, halaman panduan untuk keyword informasional. `scripts/build.py` (Python standar) merakit halaman statis dengan CSS inline tanpa JavaScript (target hijau PageSpeed), sedangkan Blog & Panduan dirender **Cloudflare Pages Functions** dari CMS Lakukan (artikel baru tampil ≤ 10 menit tanpa build ulang; teknologi sama dengan `website-service`). Build juga **memeriksa aturan**: title 40–60, meta 120–155, primary keyword di paragraf pertama, 1.000–1.500 kata, link internal wajib, tanpa nama kompetitor, tanpa klaim "satu-satunya/termurah". Social proof boleh berupa data contoh untuk preview, tapi build publish menolaknya dan rating bintang hanya dibuat dari ulasan asli. Halaman hukum `noindex` sampai direview. Setiap produk wajib punya menu & halaman **White Label** dengan copy global yang terisi otomatis per produk. Setiap halaman wajib diberi ilustrasi per section (SVG mockup UI/konsep bergaya brand, dengan brief untuk diganti gambar asli) tanpa mengorbankan SEO & PageSpeed. Skill ini dirancang dipakai berulang untuk banyak produk SaaS/GaaS. Untuk website **jasa** (software house, outsourcing) pakai `website-service`.

### `sosmed-desain`
Ide → brief (disetujui di chat) → pilih gaya → carousel 5–7 frame atau satu gambar di kanvas Design Claude dengan design system Venturo. Tiga gaya bergantian agar feed tidak monoton: **Style 1 – kartu miring**, **Style 2 – blok warna lembut**, dan **Style 3 – satu gambar padat** (mis. tabel "tanpa vs dengan AI"; detail di `references/gaya.md`). Kanvas 9:16 (1080 × 1920) dengan semua isi di **zona aman 4:5** (y = 285–1635).

### `sosmed-caption`
Menulis judul + dua versi caption dari desain final: ber-enter untuk Instagram & Threads, satu paragraf untuk TikTok (TikTok membuang enter pada posting foto). Tanpa hashtag nama perusahaan, ≤ 500 karakter. Disimpan sebagai `caption.md` di folder Google Drive posting.

### `sosmed-posting`
Satu konfirmasi di awal, lalu: `scripts/render.py` merender frame terpilih jadi JPEG 9:16 (`9x16-tiktok-threads/`) dan crop 4:5 (`4x5-instagram/`) dalam hitungan detik (font & logo/latar Venturo dibundel di `assets/`), simpan ke `Sosmed/<judul>/` di Google Drive, lalu jadwalkan tiga posting di Metricool: TikTok (9:16, musik otomatis), Threads (9:16), Instagram (carousel/gambar 4:5). Selesai begitu terjadwal, dengan estimasi waktu tayang dan durasi tiap langkah. Batasan platform yang sudah terbukti ada di `references/teknis.md`.

### `motion-graphic`
Mengubah aplikasi SaaS pengguna jadi **video motion graphic MP4**. Bahannya **screenshot asli** dari layar browser pengguna (lewat Claude-in-Chrome) yang disamarkan dulu — nama & jabatan diganti dummy, 4 digit terakhir nomor telepon di-blur, foto profil tetap — lalu dianimasikan dengan kursor, klik, dan zoom kamera, dan dirender frame-per-frame. Tiga gaya: **Style 1 – promo fitur 9:16**, **Style 2 – walkthrough 16:9**, **Style 3 – walkthrough 9:16** (detail di `references/gaya.md`). Hasil: **satu** MP4 kecil (≤ 3 MB, 720p) dengan nama file berkata kunci untuk SEO, siap dipasang di website + snippet embed yang lolos PageSpeed (Performance ≥ 90, CLS 0, 0 byte video sebelum diklik).

> **Catatan lingkungan:** butuh **Claude-in-Chrome**, **macOS** (screenshot ditangkap dengan `screencapture`, perlu izin Screen Recording), serta `ffmpeg`, Python `playwright` + Chromium, Pillow, dan `lighthouse` di komputer — skill mengecek dan menawarkan pemasangannya di langkah awal. Hasil disimpan di folder pilihan pengguna (default `motion-graphic/<produk>/` di working directory).

### `article-docs`
Mengubah folder **dokumentasi/panduan aplikasi** (halaman HTML/Markdown + screenshot) jadi **seri artikel tutorial** untuk tamu website, lalu memposting otomatis ke CMS **api.lakukan.id**. Screenshot disamarkan dulu dengan OCR Vision (`scripts/samarkan.py`): nama orang → nama dummy yang konsisten, email → dummy, 4 digit terakhir nomor telepon di-blur, foto profil tetap; gambar placeholder dilewati. Kategori selalu dua level — **Docs › kelompok tutorial** — dan judul cukup nama tutorialnya (tanpa nomor seri; urutan diatur frontend). `scripts/posting.py` (Python standar) memvalidasi, membuat/memperbarui kategori & artikel, mengunggah gambar isi + sampul, menerbitkan berurutan, dan memverifikasi API publik. Bisa juga untuk **satu artikel** saja atau **mengupdate artikel** yang sudah terbit (`posting.py ambil` → edit → `posting`). Field yang tidak diubah tetap seperti semula, tanpa duplikat, dan posisi artikel di daftar tidak bergeser. Hasilnya langsung menjadi isi menu **Panduan** yang dibangun `website-seo`.

> **Catatan lingkungan (article-docs):** butuh **macOS** (`swiftc` untuk OCR Vision), Python **Pillow** untuk penyamaran, dan **API key Lakukan** dari user (dipakai lewat env `LAKUKAN_API_KEY`, tidak pernah disimpan ke file).

### `article-blog`
Menulis **satu artikel blog edukatif** untuk produk SaaS dari topik atau materi user (kebijakan internal, SOP, data), misalnya "agar karyawan profesional bekerja WFA" dari aturan WFA perusahaan. Artikel dilengkapi **3 infografis bermerek** yang dirender dari template HTML 16:9 lewat Chrome headless — **9 pola** (kartu pilar, pernyataan, siklus, timeline, tangga level, hindari vs lakukan, alur keputusan, angka besar, checklist) dan **4 tema latar** (terang, lembut, gelap, gradasi), dipilih bervariasi per artikel agar pembaca tidak bosan (`scripts/render_infografis.py`), serta 1–2 screenshot produk yang disamarkan. Artikel langsung terbit di kategori **Blog** CMS Lakukan dan tampil di /blog website. Materi internal disajikan sebagai "contoh kebijakan" tanpa nama perusahaan, tanpa harga, dan tanpa nama kompetitor. Untuk posting, update, dan penyamaran, skill ini memakai skrip `article-docs`.

> **Catatan lingkungan (article-blog):** butuh **Google Chrome/Chromium**, Python (Pillow opsional; `sips` di macOS sebagai cadangan), dan **API key Lakukan** lewat env `LAKUKAN_API_KEY`.

### `article-portfolio`
Menulis **artikel studi kasus portfolio** untuk satu proyek software Venturo, apa pun jenisnya (website, web app/sistem internal, mobile app, dashboard, chatbot/AI, integrasi/API, desktop/POS). Struktur tetap: ringkasan proyek, **tantangan**, **solusi per aktor/platform**, **keunggulan**, hasil, dan CTA ke layanan. Screenshot disusun **per aktor** (1 aktor = 1–2 layar utama) dan disamarkan; proyek tanpa UI memakai diagram. Ada cover mockup laptop + HP (selalu memakai logo resmi Venturo yang dibundel di `assets/logo-venturo.png`), mode klien anonim (NDA), SEO (keyword "jasa pembuatan [jenis]", judul, slug, alt text, internal link), dan mode update. Terbit ke kategori **Portfolio** CMS Lakukan. Memakai skrip `article-docs` (posting & penyamaran) dan `article-blog` (render cover/diagram).

> **Catatan lingkungan (article-portfolio):** sama dengan `article-docs` + `article-blog`: Chrome/Chromium, Python Pillow, dan **API key Lakukan** lewat env `LAKUKAN_API_KEY`. Admin area proyek di-login sendiri oleh user.

### `proposal-managed`
Dari satu **System Requirement Brief** klien (txt/pdf/docx), membuat **tiga PDF langsung jadi** dengan satu nomor dokumen dan revisi: (1) **Penawaran Layanan** Managed Service sekaligus form persetujuan (tanda tangan + stempel CEO, pilihan Layanan Lanjutan setelah go-live), (2) **Lampiran Estimasi Delivery Point** (ringkasan Poin per modul, rincian per item, pengembangan tahap berikutnya, asumsi), dan (3) **Service Agreement** 23 pasal. Estimasi dihitung per tugas (1 Poin ≈ 1 jam kerja senior, bobot 0,25–1), paket bulanan 50–250 Poin (Rp150.000/Poin, Setup Awal Rp10.000.000) dengan cadangan UAT, termin per bulan, dan Layanan Lanjutan 50 Poin/bulan di luar Total Investasi. Dirender A4 lewat Playwright Chromium.

> **Catatan lingkungan (proposal-managed):** butuh Python **Playwright** + Chromium dan `pdftoppm` (poppler) untuk verifikasi.

### `proposal-dedicated`
Turunan `proposal-managed` untuk model **Dedicated Team (man power based)**: menghitung **berapa orang di setiap bulan** plus fitur yang dikerjakan. Dari brief/RFI/tender, skill menyusun penawaran **per fase** (Requirement → Fondasi → Fitur Utama → SIT → UAT & Pentest → Go-Live → Hypercare 3 bln → Annual Support 12 bln) dengan alokasi pecahan (1, ½, ¼ orang; satuan waktu ¼ bulan), tarif **Long Term** (≥ 2 bulan, dengan Engineering Kick-off proporsional) dan **Short Term** (< 2 bulan, tanpa Kick-off), perjalanan dinas, serta termin per bulan. Generator `scripts/build.py` membangun ketiga dokumen dari satu file data dan memastikan Total Investasi = Σ termin. Hasil: Penawaran Dedicated Team, **Lampiran Rincian Biaya & Rencana Kerja**, dan Service Agreement Dedicated. Harga nett (Venturo belum PKP). Untuk RFI/tender, skill juga memetakan struktur respons yang diminta.

> **Catatan lingkungan (proposal-dedicated):** Python **Playwright** + Chromium dan `pdftoppm` (poppler); jalankan skrip tanpa flag `-I`.

### `proposal-upload`
Lanjutan `proposal-managed`: mengunggah 3 PDF penawaran satu set langsung dari folder hasil `proposal-managed` ke bucket **R2 Cloudflare** di **proposal.venturo.id** (terpisah dari website company profile) langsung tanpa konfirmasi dengan URL sesuai nama file (`https://proposal.venturo.id/VEN-<Project>-<Tahun>-<Rev>.pdf`), hanya revisi terbaru per project; memverifikasi ketiga link, lalu menyusun **pesan WhatsApp pengantar 2 bubble** berisi link (Penawaran sebagai dokumen utama), masa berlaku 14 hari dari tanggal dokumen, dan ajakan review — diskon hanya disebut bila ada di PDF. Input = 3 PDF hasil `proposal-managed` dari sesi chat sebelumnya (folder dan/atau file).

> **Catatan lingkungan (proposal-upload):** butuh `npx wrangler@4` dengan auth Cloudflare (`wrangler login`, atau API token izin *Workers R2 Storage: Edit* di env `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`), bucket R2 `proposal`, dan custom domain `proposal.venturo.id` yang tersambung ke bucket (setup sekali, lihat SKILL.md). Skill hanya menyusun pesan WA; pengguna yang mengirimkannya.

### `website-profile`
**Gabungan `website-seo` + `website-service` dalam satu skill**, dengan dua preset di `site.json`: **`produk`** (website produk SaaS: sales page, landing SEO/Ads, Harga, White Label, modal langganan) dan **`jasa`** (website bisnis jasa software: tanpa harga yang dijaga build, semua tombol ke WhatsApp, menu Layanan · Portfolio · Blog, schema ProfessionalService). Satu `build.py` (perakit + pemeriksa aturan) dan satu set **Cloudflare Pages Functions** untuk Blog, Panduan, dan **Portfolio + filter AI** dari CMS Lakukan. Preset produk menghasilkan output identik dengan `website-seo`. `website-seo` dan `website-service` tetap tersedia untuk perbandingan.

### `website-service`
Membangun dan merawat **website lini bisnis jasa software** (software house, IT outsourcing, Dedicated Team, Managed Services, jasa pembuatan aplikasi/website/AI) seperti **venturo.id**: HTML statis + **Cloudflare Pages Functions**, portfolio & blog dari CMS Lakukan (termasuk filter Portfolio AI), **tanpa harga**, CTA WhatsApp berkonteks dengan event `generate_lead`, 1 keyword = 1 halaman, klaim sekali per halaman, GA4/Ads tertunda, dan PageSpeed mobile 90+. Berisi kode starter, standar UI, aturan konten jasa, checklist prapublish & pasca-launch, script audit, serta log keputusan venturo.id. Untuk website **produk SaaS** pakai `website-seo`.

> **Catatan lingkungan (website-service):** Node.js (`npx wrangler@4`, `npx lighthouse@12`), Python 3, Chrome untuk screenshot, dan akun **Cloudflare** (login wrangler) untuk deploy. CMS dibaca lewat API publik, tanpa API key.

> **Catatan lingkungan:** tiga skill sosmed butuh Claude desktop yang terhubung ke komputer (folder Google Drive lokal), konektor **Google Drive** dan **Metricool**, serta tipe artifact **Design** di claude.ai.

## Pakai

```
/business-knowledge
/business-reviewer
/keyword-research
/website-seo
/sosmed-desain
/sosmed-caption
/sosmed-posting
/motion-graphic
/article-docs
/article-blog
/article-portfolio
/proposal-managed
/proposal-dedicated
/proposal-upload
/website-service
/website-profile
```

Atau cukup minta dengan bahasa biasa: *"buat BKB untuk produk baru X"*, *"isi positioning dan pricing"*, *"audit BKB, cek duplikasi"* (→ `business-knowledge`); *"review BKB, berapa skornya"*, *"analisa kompetitor"*, *"stress test positioning kami"* (→ `business-reviewer`); *"cari kata kunci"*, *"riset keyword"*, *"bikin rencana Google Ads/SEO"* (→ `keyword-research`); *"buat website dari BKB dan keyword plan"*, *"buat sales page/landing page"* (→ `website-seo`); *"buat carousel tentang X"* (→ `sosmed-desain`), *"buat caption"* (→ `sosmed-caption`), *"ekspor dan posting ke TikTok, IG, Threads"* (→ `sosmed-posting`); *"buat motion graphic"*, *"video demo aplikasi"*, *"walkthrough aplikasi untuk landing page"* (→ `motion-graphic`); *"pelajari folder panduan ini lalu posting ke CMS"*, *"jadikan dokumentasi ini artikel di website"*, *"update artikel X"* (→ `article-docs`); *"buatkan blog tentang X"*, *"input aturan ini ke blog dengan infografis"* (→ `article-blog`); *"buat portfolio proyek X"*, *"tulis studi kasus proyek ini"*, *"update portfolio X"* (→ `article-portfolio`); *"buat PDF penawaran"*, *"buat penawaran dari brief/requirement ini"*, *"estimasi delivery point"*, *"lampiran estimasi"*, *"service agreement"* (→ `proposal-managed`); *"penawaran dedicated team"*, *"proposal man power"* (→ `proposal-dedicated`); *"upload penawaran"*, *"buat link dan pesan WA penawaran"* (→ `proposal-upload`); *"buat website jasa"*, *"tambah halaman layanan"*, *"audit website venturo"*, *"deploy website ke Cloudflare"* (→ `website-service`); *"buat website profile"*, *"website company profile dengan preset jasa/produk"* (→ `website-profile`). Skill aktif otomatis saat tugasnya cocok.

## Roadmap skill berikutnya

Plugin ini dirancang menampung banyak skill AI Marketing OS: brand-story-writer, company-profile-writer, content-ideator, blog writer — masing-masing membaca output skill sebelumnya.
