# Standar Halaman SEO (landing dari keyword plan / page brief)

Disetujui user (website Timebase, halaman `/aplikasi-monitoring-karyawan`, 4 Okt 2026): *"catat hal penting selama sesi chat untuk page ini, untuk page SEO yang di-generate dari SEO analysis"*. Contoh jadi: `references/contoh-halaman-seo-monitoring.html`.

Berlaku untuk setiap halaman yang lahir dari `data/brief.json` (title, meta, H1, primary/secondary keyword, link internal dari keyword plan). Aturan SEO dasar tetap di `aturan-konten.md`; dokumen ini merangkum **struktur & keputusan visual** yang disetujui.

## Urutan section (template)
| # | Section | Isi & layout |
|---|---|---|
| Hero | — | Badge = nama halaman (boleh diganti ajakan via `eyebrow`) · H1 dari brief · lead 1–2 kalimat · CTA langganan · 3 statistik · **media hero sama dengan semua halaman** |
| Intro | Band intro | Paragraf entitas berisi **primary keyword di kalimat pertama** + strip logo/industri (`{{bukti_sosial}}`) |
| 1 | Masalah ("Kenapa … butuh …") | Pembuka 1 kalimat + 3 kartu bernomor (masalah) + catatan 1 kalimat yang menjembatani ke solusi |
| 2 | Apa yang dicatat/dilakukan produk | **Video demo user** (bila ada) + 4 kartu fitur (2×2 di samping video potret) + 2 poin centang |
| 3 | Pembeda/kepercayaan (mis. transparan, bukan diam-diam) | Pembuka memuat **secondary keyword** secara alami + video/ilustrasi + 5 poin centang + catatan bertaut ke halaman panduan terkait |
| 4 | Pilih paket | Poin per paket **tanpa angka harga** + catatan "Harga … ada di menu Harga" |
| 5 | Testimoni | `{{testimoni}}` (avatar inisial sampai ada foto asli) |
| 6 | Dukungan/pemasangan | Ilustrasi jendela chat generik (`jenis: chat`) + 3 poin |
| 7 | Jawaban jujur (batas produk) | `callout honest` + catatan bertaut ke 1–2 halaman SEO lain |
| 8 | FAQ | 4–6 pertanyaan penting (judul ajakan, subjudul otomatis) |
| 9 | CTA | `{{cta}}` ringkas |

**Tidak dipakai:** section "Cara memulai"/"Langkah menerapkan …" (langkah onboarding bernomor) di halaman SEO — dihapus user di halaman Monitoring dan Absensi Hybrid, "Cara kerja" juga dihapus di White Label. Section yang menjelaskan **cara kerja fitur** (mis. "Cara kerja start/stop per issue") boleh tetap ada. Alur mulai cukup dijelaskan di FAQ ("Berapa lama sampai bisa dipakai?", "Bagaimana cara mulai memakai …?") — isi langkah yang dihapus dipindah ke satu jawaban FAQ bila jumlah kata perlu dijaga.

## Keputusan visual yang disetujui (halaman ini)
- **Video demo milik user menggantikan ilustrasi** bila user memberikannya ("ganti dengan ilustrasi saya ini"). Prosedur: salin ke `static/video/`, poster dari frame **setelah animasi pembuka** (±3 detik; frame awal sering masih kosong/0), entri `ilustrasi.json` `auto:false` + `video` + `file` + `w/h` asli. Kompres hanya bila >5 MB (`scripts/kompres_video.swift`).
- **Media potret (9:16)**: kolom media 340px (`split media potret`), kartu section ikut ke kolom teks 2×2 — tidak ada area kosong lebar di sisi video ("areanya terlalu lebar").
- **Ilustrasi chat dukungan**: jendela chat generik. Versi ponsel ala WhatsApp dan versi beranimasi sudah dicoba lalu **dibatalkan** user — jangan dipakai otomatis.
- Ilustrasi grafik (`bars`) boleh dianimasikan bila diminta; ilustrasi lain statis secara default.
- Semua video dimuat setelah `load`, autoplay tanpa suara, menunggu tab terlihat, diam bila *reduce motion*.

## Panjang halaman
- Minimal 700 kata (ERROR), target keyword plan 1.000–1.500 (WARNING). User lebih memilih **halaman ringkas tanpa section pengisi** daripada mengejar target kata: jangan menambah section/paragraf hanya demi jumlah kata; bila perlu tambah, pakai FAQ bernilai atau poin yang benar-benar informatif.

## Cek sebelum selesai
Primary keyword di paragraf pertama, title, H1 · secondary keyword muncul alami · link internal dari brief ada · tanpa angka harga · tiap section punya pembuka 1–2 kalimat menempel ke judul · tidak ada pesan dobel · kolom seimbang (≤1,8×) · tanpa overflow di 1440/1280/768/375.
