---
name: sosmed-posting
description: Mengekspor frame carousel dari kanvas Design Claude menjadi JPEG 9:16 (TikTok & Threads) dan 4:5 (Instagram), menyimpannya ke folder Google Drive posting, lalu memposting ke TikTok, Threads, dan Instagram lewat Metricool dan memantau statusnya sampai tayang. Gunakan saat pengguna berkata "ekspor dan posting", "upload ke tiktok/instagram/threads", "posting carousel ini", "sosmed posting", atau setelah caption disetujui.
---

# Sosmed – Ekspor & Posting

Detail teknis (render, font, aset, link Drive, payload Metricool) ada di `references/teknis.md`. Baca sebelum mulai.

## Input

- Link kanvas Design posting.
- Judul posting (= nama folder Drive).
- `caption.md` di folder posting (buat dulu dengan `sosmed-caption` bila belum ada).

## Langkah

### 1. Ekspor frame

1. Baca `project/canvas.json`; ambil artboard sesuai urutan `order`.
2. Render tiap artboard persis 1080 × 1920 (lihat referensi: font lokal, aset `/_blob/`).
3. Simpan dua versi, **selalu JPEG** (kualitas 95) — TikTok menolak PNG:
   - `9x16-tiktok-threads/NN-nama.jpg` — frame utuh 1080 × 1920.
   - `4x5-instagram/NN-nama.jpg` — crop tengah `(0, 285, 1080, 1635)` = 1080 × 1350.
4. Penamaan: `01-hook.jpg`, `02-…`, dst. sesuai urutan.
5. Verifikasi: buat lembar kontak kecil semua frame (9:16 dan 4:5) dan LIHAT gambarnya. Pastikan tidak ada teks/logo terpotong di versi 4:5 dan font Montserrat termuat. Jika terpotong, hentikan dan minta desain diperbaiki (zona konten y = 285–1635).

### 2. Simpan ke Google Drive

- Folder: `My Drive/Sosmed/<Judul Posting>/` di akun `hello@venturo.id` (lokal Mac: `~/Library/CloudStorage/GoogleDrive-hello@venturo.id/My Drive/Sosmed/<Judul Posting>/`).
- Tulis kedua subfolder. JANGAN menimpa `caption.md`.
- Cek jumlah file, ukuran piksel, dan urutan.

### 3. Konfirmasi sebelum tayang (WAJIB)

Posting publik butuh persetujuan eksplisit. Tampilkan satu ringkasan dan tunggu jawaban "ya":

- Platform & versi: TikTok + Threads (9:16), Instagram (4:5 carousel).
- Judul, caption (dari `caption.md`), musik TikTok otomatis.
- Waktu tayang (default: ±5 menit dari sekarang, WIB).

Minta pengguna membuat folder posting **publik sementara** ("Siapa saja yang memiliki link – Viewer") bila belum — Metricool paket Free tidak punya integrasi Drive, jadi gambar diambil lewat link publik.

### 4. Kirim ke Metricool

Buat **dua** posting (media berbeda per ukuran):

1. `tiktok` + `threads` → media 9:16, `tiktokData.autoAddMusic: true`, `title` = judul.
2. `instagram` → media 4:5, `instagramData.type: "POST"` (carousel).

Catatan: musik otomatis hanya didukung TikTok. Carousel Instagram tidak bisa diberi musik lewat API — sampaikan ke pengguna bila ia meminta musik di Instagram (opsi: tambahkan manual di aplikasi, atau jadikan Reel video + lagu katalog, lihat referensi).

### 5. Pantau sampai tayang

- Cek `getScheduledPosts` setiap beberapa menit setelah jadwal. Status berjalan: `PENDING` → `PUBLISHING` → `PUBLISHED` (TikTok bisa `AWAITING_CONFIRMATION` sebentar).
- Jika `ERROR`, baca `detailedStatus`, perbaiki (mis. format gambar), lalu kirim ulang posting baru untuk platform yang gagal saja.

### 6. Laporan akhir

- Berikan link publik tiap platform.
- Ingatkan pengguna mengembalikan akses folder Drive ke **Dibatasi** (Metricool sudah menyimpan salinan gambar).
- Sebutkan posting gagal lama (jika ada) yang bisa dihapus dari Planner Metricool.
