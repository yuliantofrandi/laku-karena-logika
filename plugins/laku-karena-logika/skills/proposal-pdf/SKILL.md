---
name: proposal-pdf
description: Membuat DUA PDF Venturo langsung jadi dari System Requirement Brief klien (txt/pdf/docx) — (1) Penawaran + form agreement (Managed Service / Dedicated Team) lengkap dengan tanda tangan+stempel dan paraf CEO, dan (2) Lampiran Estimasi Delivery Point berisi estimasi DP per modul — dengan estimasi DP, paket bulanan, dan termin pembayaran dihitung dari brief. Pakai saat diminta "buat PDF penawaran", "penawaran dari brief", "buat penawaran dari requirement", "estimasi delivery point", "lampiran estimasi", "penawaran baru untuk klien X", atau "export penawaran ke PDF".
---

# Penawaran Venturo dari Brief → 2 PDF

Dari satu **System Requirement Brief** klien, skill ini menghasilkan dua PDF yang langsung jadi:
1. **Penawaran**: dokumen penawaran **sekaligus form agreement/kontrak**. Fungsinya mengikat, bukan membujuk (bujukan ada di presentasi).
2. **Lampiran Estimasi Delivery Point**: rincian DP per modul yang menjadi dasar paket di penawaran.

SLA tetap dikirim terpisah.

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
- `assets/fonts/*.woff2` — Montserrat 400/400-italic/500/600/700/800.
- `assets/contoh-penawaran.html` — template Penawaran lengkap (contoh: Alldila Seats, `VEN/Kursi3D/2026/001`).
- `assets/contoh-lampiran-estimasi.html` — template Lampiran Estimasi Delivery Point dengan contoh proyek yang sama.
- `scripts/render.py` — `python3 -I <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<label footer>"]`; render A4 dengan Playwright Chromium + footer (label · No. dokumen | Paraf Venturo [paraf.png] + Paraf Klien | Halaman X dari Y). Label default "Penawaran Layanan Managed Service"; untuk lampiran pakai "Lampiran Estimasi Delivery Point". Membaca `paraf.png` dari folder yang sama dengan HTML.

## 1. Input: System Requirement Brief
- Brief dari pengguna berupa file **txt, pdf, atau docx**. Baca seluruh isinya.
- Data klien yang wajib ada: **nama, jabatan, instansi/perusahaan, dan alamat**. Bila salah satunya tidak ada di brief, **tanyakan sekali di awal** dalam satu pesan. **Jangan menanyakan hal lain**; semua yang lain diputuskan dari brief dan aturan di skill ini.

## 2. Estimasi Delivery Point (DP) dari brief
1. **Pecah brief per modul/kanal**, lalu tiap modul menjadi **item pekerjaan** yang konkret.
2. **Bobot per item:** ringan **0,25** · kecil **0,5** · menengah **0,75** · besar **1 DP**. Satu fitur bisa terdiri dari beberapa pekerjaan dan beberapa DP. Tulis kategorinya sebagai "Besar × 6" (= 6 DP), "Menengah × 4" (= 3 DP), dst.
3. **Hitung terpisah per kelompok:**
   - **Web**: semua fitur web, termasuk seluruh fitur admin.
   - **Mobile**: hanya fitur untuk pengguna akhir (mis. peserta, dosen). Fitur admin **web-only**, tidak dihitung lagi di mobile.
   - **UI/UX**: wireframe, desain layar, desain aset.
   - **Meeting review & pelatihan**: **1 DP = 1 jam** sesi.
   - Hilangkan kelompok yang tidak ada di brief (mis. proyek tanpa aplikasi mobile).
4. **Item opsional** dari brief dicantumkan di lampiran beserta DP-nya, tetapi **tidak dihitung** ke total.
5. **Tarif:** Rp150.000/DP. **Setup Awal:** Rp10.000.000 (sekali bayar, tidak memotong DP).
6. **Pilih paket bulanan** 50 / 100 / 150 / 200 / 250 DP yang menutup total estimasi. Boleh beberapa bulan (mis. 150 + 150 DP), sesuaikan dengan urutan pengerjaan modul. **Sisa DP** dari total paket = cadangan revisi/UAT.

## 3. PDF 1 – Penawaran (`contoh-penawaran.html`)
1. **Header**: logo, eyebrow "PENAWARAN LAYANAN & PERSETUJUAN KERJA SAMA", judul layanan + nama project (teal). Kartu kiri: No., Project, Tanggal. Kartu kanan (teal-50): Kepada Yth., nama, jabatan & perusahaan, alamat. Paragraf pembuka umum ("…membangun, mengembangkan, dan memelihara aplikasi Klien…").
2. **1. Lingkup Layanan**: kartu Setup Awal dan kartu Managed Service (Delivery Point Based Development). Label poin **tidak bold**.
3. **2. Rincian Biaya**: Layanan | Periode | DP | Harga, **per periode/paket bulanan**, dengan deskripsi modul singkat (teks kecil) di bawah nama layanan → Total, Diskon (hijau, "–") bila ada, **Total Investasi**. Di bawah tabel sebutkan bahwa rincian estimasi ada di **Lampiran Estimasi Delivery Point** No. yang sama.
4. **3. Pembayaran**: syarat pembayaran, kotak rekening, tabel Periode Kerja | Termin | Tgl Invoice | Nominal dengan **satu termin per bulan sesuai paket** (Setup Awal saat tanda tangan) → Total Pembayaran.
5. **4. Batasan dan Pengecualian**: biaya pihak ketiga yang disebut di brief (hosting/server, video streaming/DRM, API video conference, layanan email/push notification, akun developer store, fee payment gateway, dll.) dan item opsional, ditambah poin standar template (out-of-pocket, kerja di luar jam kerja 2×, pekerjaan di luar alokasi DP). Mulai halaman baru bila perlu supaya blok persetujuan tidak terpotong.
6. **5. Persetujuan**: kalimat "Dengan menandatangani dokumen ini, … bagian tidak terpisahkan dari dokumen Service Agreement Venturo." → "Ditandatangani di Malang, pada tanggal ____ <tahun>." → kotak PENYEDIA LAYANAN | KLIEN.

## 4. PDF 2 – Lampiran Estimasi Delivery Point (`contoh-lampiran-estimasi.html`)
1. **Header** bergaya sama dengan penawaran. Eyebrow/judul "LAMPIRAN ESTIMASI DELIVERY POINT"; kartu kiri berisi **No. Penawaran** yang diacu, Project, Tanggal; kartu kanan berisi data klien.
2. **1. Rincian per Modul**: satu tabel per modul (No | Item Pekerjaan | Kategori | DP) dengan **subtotal** tiap modul.
3. **2. Ringkasan**: DP per modul → **total estimasi DP** vs **DP paket** (mis. "2 bulan × 150 DP") → **sisa cadangan revisi/UAT**; lalu tabel **item opsional** (+DP, tidak termasuk paket).
4. **3. Asumsi & Catatan**: bobot DP disepakati di awal; perubahan scope dihitung ulang dan diajukan untuk persetujuan; asumsi teknis dari brief (mis. level keamanan video, ketersediaan API pihak ketiga, materi/aset disediakan klien).
5. Footer paraf Venturo + klien seperti penawaran (lewat `render.py` dengan label lampiran). **Tanpa blok tanda tangan penuh.**

## 5. Konvensi wajib
- **Nomor dokumen:** `KODE/Project/Tahun/Revisi` → `VEN/Kursi3D/2026/001`.
  - KODE = kode perusahaan (Venturo = VEN; pengguna punya beberapa perusahaan — tanyakan bila bukan Venturo).
  - Project = singkatan maks 2 kata dari judul project, tanpa spasi ("Presentasi Kursi 3D Interaktif" → `Kursi3D`).
  - Tahun = 4 digit. Revisi = 001, 002, …
- **Nama file:**
  - Penawaran: `VEN-<Project>-<Tahun>-<Rev>.pdf`
  - Lampiran: `VEN-<Project>-<Tahun>-<Rev>-Lampiran-Estimasi.pdf`
  - **Nomor revisi keduanya selalu sama.** Revisi = render ulang **keduanya** dengan nomor revisi naik; hapus file versi lama.
- **Penanda tangan Venturo:** Yulianto Frandi · **CEO** · **PT Venturo Pro Indonesia** · tanggal tanda tangan **= tanggal dokumen**. Selalu tempel `ttd.png` di kotak Venturo dan `paraf.png` di footer setiap halaman kedua PDF.
- **Klien:** kotak tanda tangan kosong + Nama, Jabatan, Tanggal. **Tanpa kotak meterai.**
- **Tanpa "Berlaku s/d"** dan tanpa kalimat masa berlaku (pengguna menyampaikannya di pesan saat mengirim).
- Bahasa Indonesia formal; rupiah bertitik (`Rp10.000.000`); DP desimal pakai koma (`0,75`); tanggal "19 Oktober 2026"; "Kepada Yth." + "Bapak/Ibu" lengkap.

## 6. Desain (design system Venturo)
- Warna: brand-teal #259ead, teal-700 #1b7a86 (header tabel/label), teal-800 #176a74, teal-50 #eaf6f7, ink #1f2a2e, muted #58585a, subtle #6b7072, border #d5dfe0, surface-200 #f4f7f6, hijau diskon #3c7a2a.
- Kartu radius 4mm, border tipis; `break-inside: avoid` untuk kartu, tabel kecil, dan blok tanda tangan (tabel estimasi panjang boleh terpotong antarbaris). `@page { size:A4; margin:16mm 16mm 18mm }`.
- Sumber design system lengkap: artifact https://claude.ai/artifact/9Xz8mMr54wVGngfEdtyfFn.

## 7. Langkah kerja
1. Baca brief → lengkapi data klien (tanya sekali bila kurang) → susun estimasi DP dan pilih paket (langkah 2).
2. Salin `assets/*` ke folder kerja; isi `contoh-penawaran.html` dan `contoh-lampiran-estimasi.html` dari hasil estimasi (jaga struktur & kelas CSS). Angka di penawaran (DP paket, harga, termin) dan di lampiran (total, sisa) harus konsisten.
3. Render keduanya:
   - `python3 -I <folder skill ini>/scripts/render.py penawaran.html "<output>/VEN-<Project>-<Tahun>-<Rev>.pdf" "<No. dokumen>"`
   - `python3 -I <folder skill ini>/scripts/render.py lampiran.html "<output>/VEN-<Project>-<Tahun>-<Rev>-Lampiran-Estimasi.pdf" "<No. dokumen>" "Lampiran Estimasi Delivery Point"`
4. Verifikasi kedua PDF: `pdftoppm -r 60` tiap halaman → tidak ada halaman berisi sisa kecil, TTD & paraf transparan (bukan kotak hitam/putih), nomor dokumen sama di header, footer, dan nama file kedua PDF.
5. Kirim **2 file** dengan SendUserFile.

## 8. Laporan ke pengguna
- Tabel ringkas DP per modul → total estimasi, paket yang dipilih (bulan × DP), sisa cadangan, dan total investasi.
- Item opsional beserta DP-nya.
- **Asumsi yang perlu dicek** pengguna (dari brief maupun yang diputuskan skill), mis. pembagian web vs mobile, bobot item yang paling besar, biaya pihak ketiga.
- Pengingat bahwa SLA dikirim terpisah.

## Mengganti tanda tangan
Bila pengguna memberi file TTD baru: render PDF/gambar ke PNG 300 dpi, alpha = luminans (gelap → opak, putih → transparan; untuk PNG RGBA, pakai alpha aslinya dan buang yang mendekati putih), crop bbox, simpan menimpa `ttd.png` / `paraf.png` di folder kerja.
