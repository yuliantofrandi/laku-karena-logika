---
name: sosmed-posting
description: Mengekspor frame carousel dari kanvas Design Claude menjadi JPEG 9:16 (TikTok & Threads) dan 4:5 (Instagram) dengan satu skrip, menyimpannya ke folder Google Drive posting, lalu menjadwalkan posting ke TikTok, Threads, dan Instagram lewat Metricool — selesai begitu terjadwal, tanpa menunggu tayang. Gunakan saat pengguna berkata "ekspor dan posting", "upload ke tiktok/instagram/threads", "posting carousel ini", "sosmed posting", atau setelah caption disetujui.
---

# Sosmed – Ekspor & Posting

Target: selesai dalam beberapa menit. Jalan TANPA berhenti setelah satu konfirmasi di awal, dan BERHENTI begitu posting terjadwal di Metricool (tidak memantau sampai tayang). Detail teknis: `references/teknis.md`.

## Input

- Link kanvas Design posting dan daftar artboard versi yang dipilih (mis. `B1-Hook … B6-Penutup`). Kalau kanvas berisi lebih dari satu versi/gaya, ekspor HANYA versi yang dipilih — tanyakan bila belum jelas.
- Judul posting (= nama folder Drive).
- `caption.md` (dari `sosmed-caption`) berisi judul, caption ber-enter, dan caption TikTok satu paragraf.

## 1. Konfirmasi sekali di awal (WAJIB)

Posting publik butuh persetujuan eksplisit. Tampilkan SATU ringkasan dan tunggu "ya" (boleh digabung dengan persetujuan caption):

- Platform & versi: TikTok (9:16, caption satu paragraf, musik otomatis), Threads (9:16, caption ber-enter), Instagram (carousel 4:5, caption ber-enter, tanpa musik).
- Judul, frame yang diekspor, waktu tayang (default ±3 menit setelah dikirim, WIB).

Setelah "ya", jalankan langkah 2–5 sekaligus tanpa bertanya lagi. Folder induk `Sosmed` di Drive sudah publik permanen ("siapa saja dengan link"), jadi JANGAN minta pengguna mengubah akses folder.

## 2. Ekspor frame (satu perintah)

1. `Artifact` read kanvas: `project/canvas.json` + file `.dc.html` artboard yang dipilih (satu panggilan dengan `paths`), `out_dir` ke satu folder scratch.
2. Jalankan skrip bundel (font & logo/latar Venturo sudah ada di `assets/` skill ini, tidak perlu unduh):

   ```bash
   python3 <folder skill ini>/scripts/render.py --src <folder kanvas> \
     --boards B1-Hook,B2-Konteks,... --names 01-hook,02-...,... --out <folder output>
   ```

   Hasil: `9x16-tiktok-threads/*.jpg` (1080×1920), `4x5-instagram/*.jpg` (1080×1350), `contact.png`, dan laporan per frame.
3. Skrip berakhir "SEMUA OK" → lanjut. Bila ada "KELUAR ZONA" atau font tidak termuat, berhenti dan laporkan. Lihat `contact.png` sekali untuk cek visual cepat.
4. Aset `/_blob/` selain logo & pola latar Venturo harus diunduh (`Artifact` read `path: <id>`) lalu dipetakan dengan `--blob id=path`; skrip memberi tahu bila ada yang belum.

## 3. Simpan ke Google Drive

- Folder: `Sosmed/<Judul Posting>/` di Google Drive pengguna yang tersinkron ke komputernya. Tulis kedua subfolder dengan satu `device_commit_files`. JANGAN menimpa `caption.md`.
- Tunggu ±30–60 detik, lalu cari ID file dengan konektor Google Drive `search_files` (`parentId` subfolder) — satu query untuk kedua subfolder bila bisa.

## 4. Kirim ke Metricool (tiga posting, satu giliran paralel)

Media dari link `https://drive.google.com/uc?export=download&id=<ID>` berurutan 01→06.

1. `tiktok` → media 9:16, `text` = caption TikTok satu paragraf, `tiktokData.autoAddMusic: true`, `title` = judul.
2. `threads` → media 9:16, `text` = caption ber-enter.
3. `instagram` → media 4:5, `text` = caption ber-enter, `instagramData.type: "POST"`.

Semua `publicationDate` sama (±3 menit ke depan). Respons tiap posting harus berisi `media` di `static.metricool.com` dan status `PENDING` — itu tanda terjadwal. Bila salah satu ditolak (mis. error media), perbaiki dan kirim ulang platform itu saja.

## 5. Laporan akhir (lalu selesai)

- Jam tayang terjadwal dan link Planner Metricool tiap posting.
- Estimasi kapan muncul di sosmed (kasar, bukan jaminan): Threads & Instagram beberapa menit setelah jam jadwal; TikTok bisa 10–15 menit (proses di sisi TikTok).
- Pengguna bisa minta "cek status posting <judul>" nanti untuk memeriksa `getScheduledPosts` dan mengambil link publik — JANGAN polling sekarang.
- Catatan musik: carousel Instagram tidak bisa diberi musik lewat API (tambahkan manual di aplikasi bila perlu).
