---
name: proposal-pdf
description: Membuat PDF penawaran + form agreement Venturo (Managed Service / Dedicated Team) dari Google Sheet penawaran, lengkap dengan tanda tangan+stempel dan paraf CEO, siap ditandatangani klien. Pakai saat diminta "buat PDF penawaran", "penawaran baru untuk klien X", "export penawaran ke PDF", atau "buat agreement dari sheet penawaran".
---

# Penawaran Venturo → PDF Agreement

Dokumen penawaran Venturo **sekaligus form agreement/kontrak**. Fungsinya mengikat, bukan membujuk (bujukan ada di presentasi). SLA dan Lampiran Estimasi Pengembangan Fitur dikirim terpisah.

## 0. Cek alat
Skill ini merender PDF di komputer pengguna. Cek dulu:
```bash
python3 -c "import playwright; print('playwright ok')"; command -v pdftoppm
```
Bila belum ada, sebutkan yang kurang dan minta izin pengguna sebelum memasang:
```bash
python3 -m pip install playwright
python3 -m playwright install chromium
brew install poppler
```
Folder hasil tidak di-hardcode: pakai folder yang disebut pengguna; bila belum disebut, pakai `penawaran/` di working directory sesi ini (ditulis `<output>` di bawah).

## Aset yang dibundel (`<folder skill ini>/`)
- `assets/logo.png` — logo resmi Venturo (jangan digambar ulang).
- `assets/bg_flat.jpg` — pola biner yang pudarannya sudah digabung ke gambar (jangan pakai CSS opacity/gradient: beberapa PDF viewer menampilkannya pink).
- `assets/ttd.png` — tanda tangan + stempel CEO (transparan) untuk kotak tanda tangan Venturo.
- `assets/paraf.png` — tanda tangan tanpa stempel untuk kolom paraf di footer.
- `assets/fonts/*.woff2` — Montserrat 400/400-italic/500/600/700/800 (Google Fonts diblokir di sandbox).
- `assets/contoh-penawaran.html` — template HTML lengkap (contoh: Alldila Seats, `VEN/Kursi3D/2026/001`). Salin ke folder kerja bersama aset di atas, lalu ganti isinya.
- `scripts/render.py` — `python3 -I <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>"`; render A4 dengan Playwright Chromium + footer (No. dokumen | Paraf Venturo [paraf.png] + Paraf Klien | Halaman X dari Y). Membaca `paraf.png` dari folder yang sama dengan HTML.

## 1. Sumber data
- Sumber: Google Sheet penawaran (mis. "Penawaran -2027"), satu tab per klien.
- Baca isi tab via Claude in Chrome di tab sheet yang terbuka (sheet di-render canvas — jangan baca teks dari screenshot):
  - `fetch('/spreadsheets/d/<ID>/htmlview/sheet?headers=true&gid=<GID>')` → parse `<tr>`: nomor baris dari `<th>`, kolom dari `colspan`. Output tool terpotong ±1000 karakter — simpan di `window._x` lalu ambil per chunk ±900.
  - gviz `tqx=out:json&range=A20` untuk isi lengkap satu sel.
- **Ikuti isi sheet apa adanya.** Kalau ada inkonsistensi (istilah periode, tanggal tidak valid, nama berbeda), tanyakan dulu.
- Edit sel (bila diminta): Name Box (klik ±(50,126)) → ketik ref → Enter → Enter (mode edit) → cmd+a → dispatch `ClipboardEvent('paste')` text/plain ke `document.activeElement` → Enter. Paste di luar mode edit merusak format sel. Bold baris pertama: Selection API pada teks editor lalu cmd+b.

## 2. Konvensi wajib
- **Nomor dokumen:** `KODE/Project/Tahun/Revisi` → `VEN/Kursi3D/2026/001`.
  - KODE = kode perusahaan (Venturo = VEN; pengguna punya beberapa perusahaan — tanyakan bila bukan Venturo).
  - Project = singkatan maks 2 kata dari judul project, tanpa spasi ("Presentasi Kursi 3D Interaktif" → `Kursi3D`).
  - Tahun = 4 digit. Revisi = 001, 002, …
  - Samakan juga sel nomor dokumen di sheet.
- **Nama file** = nomor dokumen, `/` → `-` → `VEN-Kursi3D-2026-001.pdf`. Hapus file versi lama.
- **Penanda tangan Venturo:** Yulianto Frandi · **CEO** · **PT Venturo Pro Indonesia** · tanggal tanda tangan **= tanggal dokumen**. Selalu tempel `ttd.png` di kotak Venturo dan `paraf.png` di footer setiap halaman.
- **Klien:** kotak tanda tangan kosong + Nama, Jabatan, Tanggal. **Tanpa kotak meterai.**
- **Tanpa "Berlaku s/d"** dan tanpa kalimat masa berlaku (pengguna menyampaikannya di pesan saat mengirim).
- Bahasa Indonesia formal; rupiah bertitik (`Rp10.000.000`); tanggal "19 Oktober 2026"; "Kepada Yth." + "Bapak/Ibu" lengkap.

## 3. Struktur dokumen (A4, ±3 halaman)
1. **Header**: logo, eyebrow "PENAWARAN LAYANAN & PERSETUJUAN KERJA SAMA", judul layanan + nama project (teal). Kartu kiri: No., Project, Tanggal. Kartu kanan (teal-50): Kepada Yth., nama, jabatan & perusahaan, alamat. Paragraf pembuka umum ("…membangun, mengembangkan, dan memelihara aplikasi Klien…").
2. **1. Lingkup Layanan**: kartu Setup Awal (sekali bayar, tidak memotong poin) dan kartu Managed Service (Point-Based Development). Label poin **tidak bold**.
3. **2. Rincian Biaya**: Layanan | Periode | Poin | Harga (deskripsi fitur teks kecil di bawah nama layanan) → Total, Diskon (hijau, "–"), **Total Investasi**.
4. **3. Pembayaran**: syarat dari sheet, kotak rekening, tabel Periode Kerja | Termin | Tgl Invoice | Nominal → Total Pembayaran.
5. **4. Batasan dan Pengecualian** — mulai halaman baru bila perlu supaya blok persetujuan tidak terpotong.
6. **5. Persetujuan**: kalimat "Dengan menandatangani dokumen ini, … bagian tidak terpisahkan dari dokumen Service Agreement Venturo." → "Ditandatangani di Malang, pada tanggal ____ <tahun>." → kotak PENYEDIA LAYANAN | KLIEN.

## 4. Desain (design system Venturo)
- Warna: brand-teal #259ead, teal-700 #1b7a86 (header tabel/label), teal-800 #176a74, teal-50 #eaf6f7, ink #1f2a2e, muted #58585a, subtle #6b7072, border #d5dfe0, surface-200 #f4f7f6, hijau diskon #3c7a2a.
- Kartu radius 4mm, border tipis; `break-inside: avoid` untuk kartu, tabel, dan blok tanda tangan. `@page { size:A4; margin:16mm 16mm 18mm }`.
- Sumber design system lengkap: artifact https://claude.ai/artifact/9Xz8mMr54wVGngfEdtyfFn.

## 5. Langkah kerja
1. Baca tab sheet klien → kumpulkan semua teks & angka.
2. Salin `assets/*` + `contoh-penawaran.html` ke folder kerja; isi ulang HTML dari data sheet (jaga struktur & kelas CSS).
3. Render: `python3 -I <folder skill ini>/scripts/render.py penawaran.html "<output>/<nama file>.pdf" "<No. dokumen>"`, lalu SendUserFile.
4. Verifikasi: `pdftoppm -r 60` tiap halaman → cek tidak ada halaman berisi sisa kecil, TTD & paraf transparan (bukan kotak hitam/putih), nomor dokumen di header + footer + nama file sama.
5. Laporkan singkat apa yang berubah dan yang perlu dicek pengguna; ingatkan SLA & Lampiran Estimasi dikirim bersama.

## Mengganti tanda tangan
Bila pengguna memberi file TTD baru: render PDF/gambar ke PNG 300 dpi, alpha = luminans (gelap → opak, putih → transparan; untuk PNG RGBA, pakai alpha aslinya dan buang yang mendekati putih), crop bbox, simpan menimpa `ttd.png` / `paraf.png` di folder kerja.
