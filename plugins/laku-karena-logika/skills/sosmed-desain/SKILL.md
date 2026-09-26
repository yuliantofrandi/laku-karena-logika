---
name: sosmed-desain
description: Membuat desain carousel/story sosial media Venturo (5–7 frame) di kanvas Design Claude dari sebuah topik atau naskah, memakai design system Venturo dengan kanvas 9:16 dan zona aman 4:5 agar satu desain bisa dipakai di TikTok, Threads, dan feed Instagram. Gunakan saat pengguna berkata "buat konten sosmed", "bikin carousel", "desain story Venturo", "buat postingan tentang [topik]", atau "sosmed desain".
---

# Sosmed – Desain Carousel

Ubah satu topik menjadi carousel 5–7 frame di kanvas Design Claude, siap diekspor oleh skill `sosmed-posting`.

## 1. Kumpulkan brief

Tanyakan hanya yang belum jelas (pakai AskUserQuestion bila pengguna hadir):

- Topik dan pesan utama (satu kalimat).
- Target pembaca (mis. pemilik UMKM, HRD, owner catering).
- CTA penutup (default: "Konsultasi gratis – WA kami atau klik link di bio").
- Jumlah frame (default 6).

## 2. Susun alur frame

Pakai struktur default ini, sesuaikan dengan topik:

1. **Hook** – pertanyaan/masalah pembaca + janji jawaban ("Ada 3 cara, dan bedanya besar.").
2. **Konteks** – gambaran besar/cara kerja dalam satu diagram sederhana.
3–5. **Isi** – satu poin per frame, beri penanda "1 / 3", label kategori, visual (mockup chat, cuplikan kode, diagram alur), ringkasan plus/minus, kotak "PILIH INI JIKA".
6. **Penutup** – satu hal penting/peringatan + CTA dan logo Venturo.

Tulis teks final dalam Bahasa Indonesia yang singkat. Jangan mengarang angka, harga, atau klaim; beri penanda relatif ("*Perkiraan relatif, tergantung kebutuhan bisnis.") bila membandingkan.

## 3. Terapkan design system Venturo

- Design system: pakai design system brand milik pengguna (`Artifact` action `list` dengan `type: "Design System"`; ambil yang ditandai default, tanyakan bila lebih dari satu). Baca `project/README.md` dan `project/tokens.json`-nya, lalu pasang sesuai instruksi tipe Design.
- Font: Montserrat (judul 800, isi 500–700); kode: JetBrains Mono.
- Warna utama: teks `#1f2a2e`, teal `#1b7a86` / `#259ead`, hijau `#56bf99`, hijau muda `#93cc7c`, abu `#58585a`, garis `#d5dfe0`.
- Latar: SELALU pakai aset pola angka biner milik Venturo (background_venturo) dengan mask gradasi — pekat di pojok kanan-atas dan kiri-bawah, memudar ke putih. Jangan latar penuh satu layar.
- Logo Venturo di frame hook, isi, dan penutup.
- Gaya: elemen sedikit dimiringkan (rotate ±2–5°), kartu putih dengan bayangan lembut, chip/pill berwarna, ikon garis (bukan emoji).

## 4. Aturan ukuran (WAJIB)

- Kanvas setiap frame **1080 × 1920 px** (9:16).
- **Zona konten: y = 285–1635** (area 1080 × 1350 = 4:5). Semua teks, logo, dan elemen penting HARUS di dalam zona ini, karena versi Instagram adalah crop tengah dari zona ini.
- Padding root yang terbukti pas: `315px 88px 315px`, gap antarelemen 28–32 px. Area di luar zona (0–285 dan 1635–1920) hanya untuk latar/ornamen.
- Margin samping ±88 px; hindari teks penting di ±120 px kanan dan ±350 px bawah (tertutup tombol dan caption TikTok) sejauh zona 4:5 mengizinkan.
- Setelah membuat frame, cek bahwa tinggi konten alami tiap frame ≤ 1290 px; jika lebih, rapatkan gap atau perkecil elemen, jangan melanggar zona.

## 5. Buat di kanvas

- Buat satu kanvas Design per posting dengan judul posting. Beri nama artboard berurutan (mis. `Main`, `Konteks`, `Coding`, …) dan urutkan di `order` kanvas sesuai urutan slide — urutan ini dipakai saat ekspor.
- Ikuti instruksi tipe Design untuk format `.dc.html`.

## 6. Serah terima

Beri tahu pengguna link kanvas dan daftar frame berurutan. Tawarkan langkah berikut: `sosmed-caption` untuk menulis caption.
