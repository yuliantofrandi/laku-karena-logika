---
name: sosmed-desain
description: Membuat desain carousel/story sosial media Venturo (5–7 frame) di kanvas Design Claude dari sebuah topik atau naskah — mulai dari ide, brief, pilihan gaya (Style 1 kartu miring / Style 2 blok warna lembut), sampai frame jadi — memakai design system Venturo dengan kanvas 9:16 dan zona aman 4:5 agar satu desain bisa dipakai di TikTok, Threads, dan feed Instagram. Gunakan saat pengguna berkata "buat konten sosmed", "bikin carousel", "carikan ide posting", "desain story Venturo", "buat postingan tentang [topik]", atau "sosmed desain".
---

# Sosmed – Desain Carousel

Ubah satu topik menjadi carousel 5–7 frame di kanvas Design Claude, siap diekspor oleh skill `sosmed-posting`. Urutannya WAJIB: ide → brief → pilih gaya → desain. Jangan mulai mendesain sebelum brief dan gaya disetujui.

## 1. Ide (bila pengguna belum punya topik)

- Tawarkan SATU ide per giliran; kalau pengguna minta "yang lain", beri ide dengan sudut berbeda.
- Ide berangkat dari kebutuhan nyata klien/bisnis (tanpa menyebut nama klien) dan sebaiknya menyambung posting sebelumnya.
- Tiap ide: judul/hook, pesan inti, alur frame singkat, alasan cocok.

## 2. Brief (tampilkan di chat, tunggu persetujuan)

Susun brief lengkap sebelum desain:

- Tujuan, target pembaca, pesan inti, nada.
- Format (jumlah frame, 9:16 + zona 4:5).
- **Isi per frame** dalam tabel: judul/teks utama, teks pendukung, visual.
- Aturan konten: tanpa angka karangan (pakai placeholder `[angka]`), tanpa nama klien, tanpa merek AI tertentu kecuali diminta.
- Draft caption (difinalkan nanti oleh `sosmed-caption`).

Terapkan revisi pengguna, lalu lanjut hanya setelah pengguna setuju.

## 3. Pilih gaya (tanyakan setiap posting)

Tanyakan mau **Style 1** atau **Style 2** (AskUserQuestion bila pengguna hadir) supaya desain antar-posting tidak monoton. Detail tiap gaya: `references/gaya.md`.

- **Style 1 – Kartu miring:** latar putih + pola biner di pojok, kartu putih miring ±2–5° dengan bayangan, chip warna, mockup chat/alur, kotak "HASILNYA" gelap.
- **Style 2 – Blok warna lembut:** latar pastel berganti per frame, judul sangat besar, angka 01/02/03 raksasa, logo di alas putih, kartu HASILNYA putih; penutup memakai pita teal tua.

Aturan warna kedua gaya: HINDARI latar pekat/terlalu kontras (teal, hitam, mint, hijau penuh) untuk frame isi — warna tegas hanya untuk aksen dan frame penutup.

## 4. Alur frame default

1. **Hook** – masalah/pertanyaan pembaca + janji jawaban.
2. **Konteks** – gambaran besar / kriteria / cara kerja.
3–5. **Isi** – satu poin per frame, penanda "1 / 3", label kategori, visual (mockup chat, kode, diagram alur), kotak "HASILNYA" atau "PILIH INI JIKA".
6. **Penutup** – ringkasan + CTA ("Konsultasi gratis – WA kami atau klik link di bio") + logo Venturo.

Teks final Bahasa Indonesia yang singkat, sapa pembaca "Anda".

## 5. Terapkan design system Venturo

- Design system: pakai design system brand milik pengguna (`Artifact` action `list` dengan `type: "Design System"`; ambil yang ditandai default, tanyakan bila lebih dari satu). Baca `project/README.md` dan `project/tokens.json`, lalu pasang sesuai instruksi tipe Design.
- Font: Montserrat (judul 800, isi 500–700); kode: JetBrains Mono.
- Warna: teks `#1f2a2e`, teal `#1b7a86` / `#259ead`, mint `#56bf99`, hijau `#93cc7c`, abu `#58585a`, garis `#d5dfe0`; latar lembut `#eaf6f7` (teal-50), `#eff8ea` (green-50), `#f4f7f6` (surface-200). Tanpa gradien warna.
- Latar bergambar: hanya pola angka biner Venturo, dengan mask gradasi (pekat di pojok, memudar ke putih). Jangan penuh satu layar.
- Logo hanya di atas putih; di frame berwarna beri alas putih kecil.
- Ikon garis (inline SVG), bukan emoji.

## 6. Aturan ukuran (WAJIB)

- Kanvas setiap frame **1080 × 1920 px** (9:16).
- **Zona konten: y = 285–1635** (1080 × 1350 = 4:5). Semua teks, logo, dan elemen penting HARUS di dalam zona ini — versi Instagram adalah crop tengah zona ini.
- Padding root yang terbukti pas: `315px 88px 315px`, gap antarelemen 28–36 px. Area di luar zona hanya untuk latar/ornamen.
- Margin samping ±88 px. Hindari kata ber-tanda-hubung terpotong di judul besar (bungkus dengan `white-space: nowrap`).
- Cek hasil dengan `sosmed-posting/scripts/render.py` (laporan "konten y …" harus di dalam 285–1635) sebelum menyerahkan.

## 7. Buat di kanvas

- Satu kanvas Design per posting, judul = judul posting. Nama artboard berurutan dan urut di `order`.
- Bila membuat varian gaya lain di kanvas yang sama, letakkan di baris terpisah dengan awalan nama (mis. `B1-Hook` … `B6-Penutup`) dan catatan judul baris.
- Ikuti instruksi tipe Design untuk format `.dc.html`.

## 8. Serah terima

Beri tahu link kanvas, gaya yang dipakai, dan daftar frame berurutan (nama artboard). Tawarkan langkah berikut: `sosmed-caption`.
