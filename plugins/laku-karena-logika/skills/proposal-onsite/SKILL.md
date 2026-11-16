---
name: proposal-onsite
description: Membuat DUA PDF penawaran Venturo model ONSITE ENGINEER (programmer ditempatkan dan bekerja di kantor/lokasi klien, dikelola Venturo) dari kebutuhan klien — (1) Penawaran Layanan Onsite Engineer + form persetujuan dengan tanda tangan+stempel dan paraf CEO, berisi Lingkup Layanan (talent yang ditempatkan, penempatan & jam kerja, yang dikelola Venturo, penggantian talent), Rincian Biaya (komponen biaya per talent — gaji, BPJS, THR, kompensasi PKWT, AI Engineering Platform, laptop, training — + management fee 15/12,5/10% sesuai durasi, Engineering Kick-off, Venturo Cloud opsional), Pembayaran dengan invoice bulanan di awal bulan, Batasan dan Pengecualian, dan Persetujuan, dan (2) Service Agreement Onsite Engineer (hubungan ketenagakerjaan, jam kerja & lembur, penggantian talent, perekrutan, kerahasiaan) — dibangun lewat generator scripts/build.py dari satu file data. Pakai saat diminta "penawaran onsite", "proposal onsite engineer", "programmer ditempatkan di kantor klien", "penempatan programmer", "outsourcing programmer onsite", atau "tenaga IT di lokasi klien". Tim yang bekerja dari kantor Venturo per fase pakai proposal-dedicated; proyek berbasis Poin pakai proposal-managed.
---

# Penawaran Onsite Engineer → 2 PDF

**Onsite Engineer**: programmer bekerja **di kantor Klien** dengan arahan kerja harian dari Klien, tetapi hubungan kerjanya hanya dengan Venturo. Venturo merekrut, menggaji, memantau, melatih, dan mengganti talent. Bedanya dengan **Dedicated Team**: dedicated bekerja dari ekosistem Venturo per fase proyek dengan pricelist tetap; onsite dihitung **per talent per bulan** dari komponen biaya yang transparan + management fee, dengan durasi kontrak yang sama untuk semua talent.

Dua PDF, satu nomor dokumen dan satu nomor revisi:
1. **Penawaran Layanan Onsite Engineer** — penawaran sekaligus form persetujuan.
2. **Service Agreement Onsite Engineer** — perjanjian 18 pasal.

Harga dan ketentuan: `references/pricelist-onsite.md` (sumber: deck "VENTURO - Onsite Engineer").

## 0. Alat
- Cek: `python3 -c "import playwright"` dan `command -v pdftoppm`. Bila kurang, minta izin sebelum memasang (`python3 -m pip install playwright`, `python3 -m playwright install chromium`, `brew install poppler`).
- **Jangan jalankan skrip dengan `python3 -I`** (Playwright di user site-packages jadi tidak terbaca). Jalankan `python3 <skrip> …` biasa.
- Jalankan `mkdir -p <folder preview>` sebelum `pdftoppm`.
- Folder hasil: folder yang disebut pengguna, atau `penawaran/` di working directory (`<output>`); folder kerja HTML `<output>/src`.

## Aset & skrip (`<folder skill ini>/`)
- `scripts/build.py` — **generator**: `python3 <folder skill ini>/scripts/build.py <data.json> <output>/src` membangun `penawaran.html` dan `sla.html` (+ salin logo, bg, TTD, paraf, font). Menghitung komponen biaya dari gaji pokok (tabel `PRESET` atau `gaji` di data), menghitung tarif per talent, Kick-off, tagihan bulanan, termin per bulan kalender, dan meng-`assert` Σ termin = Total, durasi ≥ 3 bulan, maksimal 4 baris talent, kode project huruf & angka saja, dan tidak ada sisa teks di `cek_tidak_boleh_ada`. **Revisi = ubah data → build → render ulang.**
- `scripts/render.py` — `python3 <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]`.
- `assets/contoh-data.json` — format data. Salin lalu ganti isinya.
- `assets/onsite.css`, `assets/sa-onsite.html` — gaya dan template Service Agreement (dipakai build.py).
- `assets/contoh-*.html` — hasil build dari contoh data, untuk acuan visual.
- `references/pricelist-onsite.md` — preset kota & level, biaya penempatan, management fee, Kick-off, ketentuan, Venturo Cloud.

## 1. Input & data klien
- Input: brief, chat, catatan meeting, atau dokumen kebutuhan klien (role, tech stack, level, lokasi, jam kerja, durasi). Data yang tidak ada (instansi, penerima, alamat, penanda tangan, lokasi kerja, bulan mulai, durasi) ditanyakan **sekali** di awal.
- Data klien yang tetap tidak diketahui tampil sebagai garis isian `______________________` (otomatis). **Jangan isi jabatan "Pimpinan".**
- **Nomor dokumen** `VEN/<Kode>/<Tahun>/<Rev>`: kode project **huruf dan angka saja** (dicek build.py). `file` = `VEN-<Kode>-<Tahun>-<Rev>`.
- **Revisi**: revisi yang belum diunggah/dikirim ke klien boleh diperbaiki tanpa menaikkan nomor; naikkan nomor bila isi/harga berubah setelah dikirim atau perubahan diminta di sesi baru.
- `project`: nama singkat kebutuhan (mis. "Tim Engineer Sistem Logistik") — judul hero sudah bertuliskan "Onsite Engineer", jangan diulang.

## 2. Talent & harga
- `talent = [{posisi, preset | (kota, level, gaji), jumlah, keahlian}]`, maksimal **4 baris** (posisi sejenis digabung dengan `jumlah`).
- **Jabatan hanya yang ada di Venturo**: Software Engineer (Senior/Intermediate, spesialisasi setelah "–", mis. *Software Engineer – Frontend*), DevOps, UI/UX, QA, BA. `keahlian` = tech stack dari brief.
- **Preset gaji pokok** (`references/pricelist-onsite.md`): `jakarta-senior` Rp10 jt, `jakarta-intermediate` Rp6,5 jt, `surabaya` Rp6,5 jt, `malang` Rp4,5 jt. Kota/level lain atau gaji mengikuti kandidat pilihan klien → **minta gaji pokok dari pemilik** lalu isi `gaji` + `kota` + `level`. **Jangan menebak gaji sendiri.**
- **Komponen** dihitung build.py dari gaji: BPJS 10,24%, Provisi THR 1/12, Provisi kompensasi PKWT 1/12.
- **Tarif per talent / bulan** = (gaji + BPJS + THR + PKWT + AI Engineering Platform Rp500.000 + Laptop Rp500.000 + Training Rp150.000) × (1 + management fee), **dibulatkan ke atas ke ribuan terdekat**.
- **Management fee** dari `durasi_bulan` (sama untuk semua talent): 3–5 bulan 15% · 6–11 bulan 12,5% · ≥ 12 bulan 10%. Minimal 3 bulan.
- **Engineering Kick-off** = 1× tarif bulanan per talent, sekali bayar sebagai Down Payment saat tanda tangan.
- **Venturo Cloud** (opsional, bila klien butuh server): `venturo_cloud = [{paket, jumlah, keterangan}]`, kode paket di pricelist; ditagih per bulan bersama invoice talent.
- **Pajak**: kalimat baku (sudah di build.py) — *"Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien."* Jangan ada baris PPN.
- **Diskon** hanya bila pemilik menyebutnya: `diskon = {nama, nilai}`; disebar rata ke invoice bulanan.

## 3. Struktur dokumen (dibangun build.py)
**Penawaran:** Hero → paragraf pembuka baku → **1 Lingkup Layanan** (tabel Talent yang Ditempatkan: posisi + keahlian · level · kota · orang → Total Talent; kotak Penempatan & Jam Kerja; kotak Dikelola Venturo; kotak Penggantian Talent) → **2 Rincian Biaya** (tabel Komponen per Talent / Bulan dengan satu kolom per talent → Total Biaya Dasar → Management Fee → Tarif per Talent / Bulan; catatan tier fee; tabel Layanan/Tarif/Orang/Bulan/Total: Engineering Kick-off → Talent Onsite → Venturo Cloud bila ada → Total Investasi) → **3 Pembayaran** (pajak, Kick-off sebagai DP, invoice awal bulan H+14 hari kalender, penghentian sementara bila telat bayar, penyesuaian UMP/UMK & regulasi, perpanjangan dikonfirmasi 2 bulan sebelum berakhir → rekening → tabel Periode Kerja/Termin/Tgl Invoice/Nominal → Total Pembayaran) → **4 Batasan dan Pengecualian** (lembur, perjalanan dinas di luar kota penempatan, lisensi/server/hardware khusus, sertifikasi vendor, + `batasan` dari data; tetap bisa disediakan dengan biaya aktual + biaya layanan) → **5 Persetujuan**.

**Service Agreement Onsite Engineer** (18 pasal): Para Pihak · Ruang Lingkup · Masa Berlaku dan Perpanjangan · Biaya dan Pembayaran · Seleksi dan Penempatan · Jam Kerja dan Lembur · Kewajiban Klien · Monitoring dan Pelaporan · Penggantian Talent (penggantian paling lambat 14 hari) · Hubungan Ketenagakerjaan · Perekrutan (biaya pengalihan 6× gaji) · Kerahasiaan · Hak Kekayaan Intelektual · Terminasi Kontrak · Pembatasan Tanggung Jawab · Force Majeure · Penyelesaian Perselisihan · Persetujuan. Isi SA adalah dokumen hukum — perubahan pasal dikonfirmasi ke pengguna.

## 4. Langkah kerja
1. Baca kebutuhan → susun `data.json` (salin `assets/contoh-data.json`): nomor, file, tanggal, project, klien, `lokasi`, `mulai` ("<Bulan> <Tahun>"), `durasi_bulan`, talent, `venturo_cloud`, `batasan`, `cek_tidak_boleh_ada`.
2. `python3 <folder skill ini>/scripts/build.py data.json <output>/src` — perbaiki data bila ada assert yang gagal.
3. Render:
```bash
python3 <folder skill ini>/scripts/render.py <output>/src/penawaran.html "<output>/VEN-<Kode>-<Tahun>-<Rev>.pdf" "VEN/<Kode>/<Tahun>/<Rev>"
python3 <folder skill ini>/scripts/render.py <output>/src/sla.html "<output>/VEN-<Kode>-<Tahun>-<Rev>-Service-Agreement-Onsite.pdf" "VEN/<Kode>/<Tahun>/<Rev>" "Service Agreement Onsite Engineer"
```
4. Verifikasi: `mkdir -p <output>/preview && pdftoppm -r 60 -png <pdf> <output>/preview/<nama>` — tabel komponen dan termin utuh, TTD/paraf tampil, tanpa halaman sisa kecil.
5. Kirim 2 PDF (SendUserFile). Laporan: talent & tarif per talent, management fee, Kick-off (DP), tagihan bulanan, Total Investasi, dan hal yang perlu dicek pemilik (mis. gaji dari pemilik).
6. Unggah & pesan WhatsApp: skill `proposal-upload` (mengenali set onsite dari akhiran `-Service-Agreement-Onsite`).

## Yang tidak boleh dilakukan
- Menebak gaji pokok di luar preset, mengubah rumus BPJS/THR/PKWT, atau management fee di luar tier durasi.
- Memakai jabatan yang tidak ada di Venturo.
- Menambahkan PPN, menulis "PPN tidak ditagihkan", atau diskon tanpa instruksi pemilik.
- Mengisi jabatan penanda tangan klien yang tidak diketahui (mis. "Pimpinan"), atau memakai tanda hubung/spasi di kode project.
- Menjalankan skrip dengan `python3 -I`, atau menulis masa berlaku penawaran / kotak meterai di dokumen.
