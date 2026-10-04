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

Prinsip yang dijaga: satu fakta satu rumah (anti-duplikasi), tidak mengarang fakta (`[INPUT-NEEDED]` / `[?]`), keputusan strategis diisi rekomendasi terbaik agar produk laris, dan keputusan strategis (positioning, target) disertai alasannya — harga tidak wajib beralasan karena kelayakannya diuji `business-reviewer`.

### `business-reviewer`
Menilai dan memberi **skor** pada BKB, lalu menguji strateginya lawan lanskap kompetitor nyata (**competitive analysis**) — semuanya sebagai satu laporan review, **read-only** (tidak mengedit BKB). Sementara `business-knowledge` menulis & merapikan dokumen, skill ini berdiri di luar sebagai kritikus: skor 100 poin per dimensi, temuan (cacat penulisan vs celah strategis), dan analisis kompetitor. BKB sengaja tidak memuat kompetitor (tanpa merek, harga, atau fitur); seluruh data & analisis kompetitor tinggal di laporan review bertanggal ini.

### `keyword-research`
Riset buying keyword di Google Ads Keyword Planner (lewat browser), lalu susun jadi Excel siap eksekusi: keyword plan, page brief (title/meta/H1/slug), dan negative keyword. Skill hilir — Langkah 0-nya membaca brief/BKB produk untuk menilai relevansi keyword, jadi melanjutkan rantai dari `business-knowledge`.

> **Catatan lingkungan:** skill ini butuh **Claude-in-Chrome** (otomasi browser) dan skill **`anthropic-skills:xlsx`**, serta menyimpan hasil ke `/mnt/user-data/outputs/` — jadi ditujukan untuk lingkungan **claude.ai/Chat**, bukan alur file lokal Cowork seperti dua skill di atas.

### `sosmed-desain`
Ide → brief (disetujui di chat) → pilih gaya → carousel 5–7 frame atau satu gambar di kanvas Design Claude dengan design system Venturo. Tiga gaya bergantian agar feed tidak monoton: **Style 1 – kartu miring**, **Style 2 – blok warna lembut**, dan **Style 3 – satu gambar padat** (mis. tabel "tanpa vs dengan AI"; detail di `references/gaya.md`). Kanvas 9:16 (1080 × 1920) dengan semua isi di **zona aman 4:5** (y = 285–1635).

### `sosmed-caption`
Menulis judul + dua versi caption dari desain final: ber-enter untuk Instagram & Threads, satu paragraf untuk TikTok (TikTok membuang enter pada posting foto). Tanpa hashtag nama perusahaan, ≤ 500 karakter. Disimpan sebagai `caption.md` di folder Google Drive posting.

### `sosmed-posting`
Satu konfirmasi di awal, lalu: `scripts/render.py` merender frame terpilih jadi JPEG 9:16 (`9x16-tiktok-threads/`) dan crop 4:5 (`4x5-instagram/`) dalam hitungan detik (font & logo/latar Venturo dibundel di `assets/`), simpan ke `Sosmed/<judul>/` di Google Drive, lalu jadwalkan tiga posting di Metricool: TikTok (9:16, musik otomatis), Threads (9:16), Instagram (carousel/gambar 4:5). Selesai begitu terjadwal, dengan estimasi waktu tayang dan durasi tiap langkah. Batasan platform yang sudah terbukti ada di `references/teknis.md`.

### `motion-graphic`
Mengubah aplikasi SaaS pengguna jadi **video motion graphic MP4**. Bahannya **screenshot asli** dari layar browser pengguna (lewat Claude-in-Chrome) yang disamarkan dulu — nama & jabatan diganti dummy, 4 digit terakhir nomor telepon di-blur, foto profil tetap — lalu dianimasikan dengan kursor, klik, dan zoom kamera, dan dirender frame-per-frame. Tiga gaya: **Style 1 – promo fitur 9:16**, **Style 2 – walkthrough 16:9**, **Style 3 – walkthrough 9:16** (detail di `references/gaya.md`). Hasil: **satu** MP4 kecil (≤ 3 MB, 720p) dengan nama file berkata kunci untuk SEO, siap dipasang di website + snippet embed yang lolos PageSpeed (Performance ≥ 90, CLS 0, 0 byte video sebelum diklik).

> **Catatan lingkungan:** butuh **Claude-in-Chrome**, **macOS** (screenshot ditangkap dengan `screencapture`, perlu izin Screen Recording), serta `ffmpeg`, Python `playwright` + Chromium, Pillow, dan `lighthouse` di komputer — skill mengecek dan menawarkan pemasangannya di langkah awal. Hasil disimpan di folder pilihan pengguna (default `motion-graphic/<produk>/` di working directory).

### `docs-article`
Mengubah folder **dokumentasi/panduan aplikasi** (halaman HTML/Markdown + screenshot) jadi **seri artikel tutorial** untuk tamu website, lalu memposting otomatis ke CMS **api.lakukan.id**. Screenshot disamarkan dulu dengan OCR Vision (`scripts/samarkan.py`): nama orang → nama dummy yang konsisten, email → dummy, 4 digit terakhir nomor telepon di-blur, foto profil tetap; gambar placeholder dilewati. Kategori selalu dua level — **Docs › kelompok tutorial** — dan judul cukup nama tutorialnya (tanpa nomor seri; urutan diatur frontend). `scripts/posting.py` (Python standar) memvalidasi, membuat/memperbarui kategori & artikel, mengunggah gambar isi + sampul, menerbitkan berurutan, dan memverifikasi API publik. Bisa juga untuk **satu artikel** saja atau **mengupdate artikel** yang sudah terbit (`posting.py ambil` → edit → `posting`). Field yang tidak diubah tetap seperti semula, tanpa duplikat, dan posisi artikel di daftar tidak bergeser. Hasilnya langsung menjadi isi menu **Panduan** yang dibangun `website-seo`.

> **Catatan lingkungan:** butuh **macOS** (`swiftc` untuk OCR Vision), Python **Pillow** untuk penyamaran, dan **API key Lakukan** dari user (dipakai lewat env `LAKUKAN_API_KEY`, tidak pernah disimpan ke file).

> **Catatan lingkungan:** tiga skill sosmed butuh Claude desktop yang terhubung ke komputer (folder Google Drive lokal), konektor **Google Drive** dan **Metricool**, serta tipe artifact **Design** di claude.ai.

## Pakai

```
/business-knowledge
/business-reviewer
/keyword-research
/sosmed-desain
/sosmed-caption
/sosmed-posting
/motion-graphic
/docs-article
```

Atau cukup minta dengan bahasa biasa: *"buat BKB untuk produk baru X"*, *"isi positioning dan pricing"*, *"audit BKB, cek duplikasi"* (→ `business-knowledge`); *"review BKB, berapa skornya"*, *"analisa kompetitor"*, *"stress test positioning kami"* (→ `business-reviewer`); *"cari kata kunci"*, *"riset keyword"*, *"bikin rencana Google Ads/SEO"* (→ `keyword-research`); *"buat carousel tentang X"* (→ `sosmed-desain`), *"buat caption"* (→ `sosmed-caption`), *"ekspor dan posting ke TikTok, IG, Threads"* (→ `sosmed-posting`); *"buat motion graphic"*, *"video demo aplikasi"*, *"walkthrough aplikasi untuk landing page"* (→ `motion-graphic`); *"pelajari folder panduan ini lalu posting ke CMS"*, *"jadikan dokumentasi ini artikel di website"*, *"update artikel X"* (→ `docs-article`). Skill aktif otomatis saat tugasnya cocok.

## Roadmap skill berikutnya

Plugin ini dirancang menampung banyak skill AI Marketing OS: brand-story-writer, company-profile-writer, content-ideator, blog writer — masing-masing membaca output skill sebelumnya.
