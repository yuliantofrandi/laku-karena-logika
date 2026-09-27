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
3. **Product-to-Value Mapping** — problem → benefit → business outcome
4. **Pricing Plan** — tier, diskon volume, add-on
5. **Target Customer Profile** — segmen + buyer persona

Prinsip yang dijaga: satu fakta satu rumah (anti-duplikasi), tidak mengarang angka (`[INPUT-NEEDED]` / `[?]`), dan setiap keputusan strategis disertai alasannya.

### `business-reviewer`
Menilai dan memberi **skor** pada BKB, lalu menguji strateginya lawan lanskap kompetitor nyata (**competitive analysis**) — semuanya sebagai satu laporan review, **read-only** (tidak mengedit BKB). Sementara `business-knowledge` menulis & merapikan dokumen, skill ini berdiri di luar sebagai kritikus: skor 100 poin per dimensi, temuan (cacat penulisan vs celah strategis), dan analisis kompetitor. Angka kompetitor permanen tetap tinggal di BKB §2; analisis kompetitor yang lebih dalam dan bertanggal tinggal di dalam laporan review ini.

### `keyword-research`
Riset buying keyword di Google Ads Keyword Planner (lewat browser), lalu susun jadi Excel siap eksekusi: keyword plan, page brief (title/meta/H1/slug), dan negative keyword. Skill hilir — Langkah 0-nya membaca brief/BKB produk untuk menilai relevansi keyword, jadi melanjutkan rantai dari `business-knowledge`.

> **Catatan lingkungan:** skill ini butuh **Claude-in-Chrome** (otomasi browser) dan skill **`anthropic-skills:xlsx`**, serta menyimpan hasil ke `/mnt/user-data/outputs/` — jadi ditujukan untuk lingkungan **claude.ai/Chat**, bukan alur file lokal Cowork seperti dua skill di atas.

### `sosmed-desain`
Ide → brief (disetujui di chat) → pilih gaya → carousel 5–7 frame di kanvas Design Claude dengan design system Venturo. Dua gaya bergantian agar feed tidak monoton: **Style 1 – kartu miring** dan **Style 2 – blok warna lembut** (detail di `references/gaya.md`). Kanvas 9:16 (1080 × 1920) dengan semua isi di **zona aman 4:5** (y = 285–1635).

### `sosmed-caption`
Menulis judul + dua versi caption dari desain final: ber-enter untuk Instagram & Threads, satu paragraf untuk TikTok (TikTok membuang enter pada posting foto). Tanpa hashtag nama perusahaan, ≤ 500 karakter. Disimpan sebagai `caption.md` di folder Google Drive posting.

### `sosmed-posting`
Satu konfirmasi di awal, lalu: `scripts/render.py` merender frame terpilih jadi JPEG 9:16 (`9x16-tiktok-threads/`) dan crop 4:5 (`4x5-instagram/`) dalam hitungan detik (font & logo/latar Venturo dibundel di `assets/`), simpan ke `Sosmed/<judul>/` di Google Drive, lalu jadwalkan tiga posting di Metricool: TikTok (9:16, musik otomatis), Threads (9:16), Instagram (carousel 4:5). Selesai begitu terjadwal, dengan estimasi waktu tayang. Batasan platform yang sudah terbukti ada di `references/teknis.md`.

> **Catatan lingkungan:** tiga skill sosmed butuh Claude desktop yang terhubung ke komputer (folder Google Drive lokal), konektor **Google Drive** dan **Metricool**, serta tipe artifact **Design** di claude.ai.

## Pakai

```
/business-knowledge
/business-reviewer
/keyword-research
/sosmed-desain
/sosmed-caption
/sosmed-posting
```

Atau cukup minta dengan bahasa biasa: *"buat BKB untuk produk baru X"*, *"isi positioning dan pricing"*, *"audit BKB, cek duplikasi"* (→ `business-knowledge`); *"review BKB, berapa skornya"*, *"analisa kompetitor"*, *"stress test positioning kami"* (→ `business-reviewer`); *"cari kata kunci"*, *"riset keyword"*, *"bikin rencana Google Ads/SEO"* (→ `keyword-research`); *"buat carousel tentang X"* (→ `sosmed-desain`), *"buat caption"* (→ `sosmed-caption`), *"ekspor dan posting ke TikTok, IG, Threads"* (→ `sosmed-posting`). Skill aktif otomatis saat tugasnya cocok.

## Roadmap skill berikutnya

Plugin ini dirancang menampung banyak skill AI Marketing OS: brand-story-writer, company-profile-writer, content-ideator, blog writer — masing-masing membaca output skill sebelumnya.
