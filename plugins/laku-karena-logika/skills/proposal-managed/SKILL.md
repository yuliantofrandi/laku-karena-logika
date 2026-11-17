---
name: proposal-managed
description: Membuat TIGA PDF Venturo model MANAGED SERVICES berbasis KUOTA FITUR BULANAN dari System Requirement Brief klien (txt/pdf/docx) — (1) Penawaran Layanan + form persetujuan dengan tanda tangan+stempel dan paraf CEO, (2) Lampiran Estimasi Fitur (diagram Alur Sistem, ukuran fitur per modul & item — kecil/standar/besar — panduan ukuran, pengembangan tahap berikutnya), dan (3) Service Agreement 23 pasal — dengan estimasi fitur, paket bulanan 2/4/6/8/10 fitur, Setup Awal, termin, dan Layanan Lanjutan setelah go-live, dibangun lewat generator scripts/build.py dari satu file data. Pakai saat diminta "buat PDF penawaran", "penawaran dari brief", "penawaran managed service", "buat penawaran dari requirement", "estimasi fitur", "lampiran estimasi", "service agreement", "penawaran baru untuk klien X", atau "export penawaran ke PDF". Model Dedicated Team (tim per fase) pakai proposal-dedicated; programmer di kantor klien pakai proposal-onsite.
---

# Penawaran Managed Services dari Brief → 3 PDF

**Managed Services**: satu biaya bulanan untuk membangun, merawat, dan mengembangkan aplikasi Klien. Setiap permintaan diukur dalam **satuan fitur** yang disepakati sebelum dikerjakan; Klien memilih **paket kuota fitur per bulan**. Harga, ukuran fitur, dan yang sudah termasuk: `references/paket-fitur.md` (sumber: deck "VENTURO - Managed Services").

Tiga PDF, satu nomor dokumen dan satu nomor revisi:
1. **Penawaran Layanan** — penawaran sekaligus form persetujuan. Fungsinya mengikat, bukan membujuk (bujukan ada di presentasi).
2. **Lampiran Estimasi Fitur** — diagram alur sistem, lalu ukuran fitur per modul dan item yang menjadi dasar paket (file tetap `…-Lampiran-Estimasi.pdf`).
3. **Service Agreement** — perjanjian induk 23 pasal.

## 0. Alat
- Cek: `python3 -c "import playwright"` dan `command -v pdftoppm`. Bila kurang, minta izin sebelum memasang (`python3 -m pip install playwright`, `python3 -m playwright install chromium`, `brew install poppler`).
- **Jangan jalankan skrip dengan `python3 -I`** (Playwright di user site-packages jadi tidak terbaca). Jalankan `python3 <skrip> …` biasa.
- Jalankan `mkdir -p <folder preview>` sebelum `pdftoppm`.
- Folder hasil: folder yang disebut pengguna, atau `penawaran/` di working directory (`<output>`); folder kerja HTML `<output>/src`.

## Aset & skrip (`<folder skill ini>/`)
- `scripts/build.py` — **generator**: `python3 <folder skill ini>/scripts/build.py <data.json> <output>/src` membangun `penawaran.html`, `lampiran.html`, `sla.html` (+ salin logo, bg, TTD, paraf, font). Menghitung harga paket, ukuran item, total estimasi, kuota, cadangan, periode & termin, Layanan Lanjutan, Venturo Cloud, dan meng-`assert`: paket hanya 2/4/6/8/10 fitur, item ≤ 2 fitur, estimasi ≤ kuota, kode project huruf & angka, tidak ada istilah lama ("Delivery Point", "Poin", "GitLab", "MVP", "lebih dari 100 orang", "PPN tidak ditagihkan") atau sisa teks di `cek_tidak_boleh_ada`. Mencetak ringkasan + `peringatan_cadangan` bila cadangan < 5%. **Revisi = ubah data → build → render ulang.**
- `scripts/render.py` — `python3 <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]`.
- `assets/contoh-data.json` — format data (contoh HRIS: alur sistem 3 lajur, 4 kategori fitur, tahap berikutnya, Venturo Cloud). Salin lalu ganti isinya.
- `assets/managed.css`, `assets/sa-managed.html` — gaya dan template Service Agreement (dipakai build.py).
- `assets/contoh-*.html` — hasil build dari contoh data, untuk acuan visual.
- `references/paket-fitur.md` — harga paket, ukuran fitur per kategori, yang sudah termasuk, layanan berlangganan.
- `references/venturo-cloud.md` — rate card Venturo Cloud dan aturan pemakaiannya.

## 1. Alur
1. **Input:** System Requirement Brief (txt/pdf/docx). Baca seluruh isinya.
2. **Data klien:** bila nama, jabatan, instansi, atau alamat tidak ada di brief, **tanyakan sekali di awal** dalam satu pesan. Data klien yang tetap tidak diketahui tampil sebagai garis isian `______________________` (otomatis). **Jangan isi jabatan "Pimpinan".**
3. **Alur sistem** (§2a), lalu **estimasi fitur** per modul → item (§2), lalu pilih paket per bulan (§3).
4. Susun `data.json` → `build.py` → render 3 PDF (§5) → verifikasi → kirim **3 file** dengan SendUserFile.
5. **Laporan singkat**: total estimasi & kuota, cadangan (beri tahu bila < 5%), fitur per modul, termin, Total Investasi, item tahap berikutnya, dan hal yang perlu dicek pemilik.

## 2. Aturan estimasi fitur
- **Satuan fitur**, bukan jam. Ukuran per item:
  - **Kecil** (< 1 fitur, desimal): tambahan pada modul/otomasi/integrasi/data yang sudah ada — mis. tambah 1 field = 0,1; laporan baru atau alur approval tambahan ≈ 0,5.
  - **Standar** (1 fitur): 1 modul utuh (master + transaksi + approval + laporan + notifikasi, mis. Modul Cuti) · 1 otomasi utuh (workflow n8n, pengingat terjadwal) · 1 integrasi utuh (API pihak ketiga, SSO, payment gateway) · 1 migrasi data 1 modul.
  - **Besar** (2 fitur): beberapa transaksi saling terkait (PO → penerimaan → stok) · chatbot AI untuk 1 alur bisnis · integrasi dua arah dengan 1 sistem · migrasi beberapa modul + validasi.
  - **> 2 fitur** (sistem besar seperti akuntansi/payroll, AI agent multi-alur, integrasi ERP, migrasi seluruh sistem lama) **dipecah** menjadi beberapa item ≤ 2 fitur — build.py menolak item > 2.
- Setiap modul diberi `kategori`: Pengembangan aplikasi · Otomasi & AI · Integrasi sistem · Pengelolaan data, dan `platform` (Web, Mobile, Web & Mobile, WhatsApp, …).
- **Sudah termasuk dalam 1 fitur**: meeting analisa, rancangan aplikasi (UI/UX), penyesuaian maks. 2× revisi, dokumentasi. Jadi **tidak ada** modul terpisah untuk UI/UX, meeting review, testing/UAT, atau pelatihan saat rilis.
- Aplikasi mobile: fitur pengguna akhir di mobile dihitung pada item modulnya (platform "Web & Mobile"); fitur admin cukup web. Rilis ke store bisa jadi item kecil.
- Pelatihan tambahan di luar rilis fitur: ½ hari = ½ fitur.
- **Fitur mahal/lama yang bukan inti** tidak masuk paket → `tahap_berikutnya` (dengan `kondisi` di rilis pertama dan `singkat` untuk kalimat Batasan).
- Fitur yang disebut brief sebagai "opsional" tapi diputuskan pengguna masuk pekerjaan → modul biasa.

## 2a. Alur Sistem (Lampiran bagian 1, wajib)
Sebelum melihat angka, klien harus paham dulu **alur software yang akan dibangun**. build.py menggambar diagram SVG dari `alur` (gaya swimlane: lajur per aktor/sistem, langkah bernomor dengan panah, layanan luar bergaris putus oranye, sumber data di bawah, catatan gelap di akhir) dan menolak data tanpa `alur`.
- `alur = {judul, pengantar, lajur, langkah, sumber_judul, sumber, catatan}`.
- **`lajur`** 2–4 kolom, kiri → kanan mengikuti arah data: pengguna (mis. "Karyawan & Atasan", ket = aplikasi mobile & web) → sistem yang kami bangun (`"sistem": true`, latar teal muda) → pihak ketiga (`"eksternal": true`: WhatsApp API, AI, payment gateway, ERP, akuntansi). `ket` pendek (platform/perangkat).
- **`langkah`** 5–8 langkah alur bisnis inti, berurutan (panah otomatis dari langkah n ke n+1): `{lajur, judul (2–4 kata, kata kerja), ket (≤ 10 kata), label (1–2 kata untuk panah masuk), baris_sama (true = sebaris dengan langkah sebelumnya), utama (true = hasil akhir yang dilihat pengguna, kotak teal penuh)}`. Langkah terakhir biasanya `utama`.
- Bahasa klien, bukan teknis: "Validasi & simpan", bukan "POST /api/leave". Setiap langkah harus terwakili di modul estimasi.
- **`sumber`** (opsional, 1–3): sumber data yang sudah ada (mesin fingerprint, Excel lama, database ERP). **`catatan`** 1–2 kalimat jaminan penting (angka dihitung sistem, data di server Klien, akses baca-saja).
- Diagram dibatasi `tinggi_maks_mm` (default 148) agar muat di halaman 1 setelah hero; alur panjang otomatis diperkecil — lebih dari 8 langkah, ringkas atau gabungkan dengan `baris_sama`.

## 3. Paket & biaya
- Paket per bulan: **2 fitur Rp7,5 jt · 4 fitur Rp14 jt · 6 fitur Rp19,5 jt · 8 fitur Rp24 jt · 10 fitur Rp27,5 jt**. Paket boleh berbeda tiap bulan (mis. 10 + 10 + 2): besar saat membangun, kecil saat stabil.
- **Setup Awal Rp10.000.000** sekali bayar, tidak memotong kuota. Isinya: Kickoff & Roadmap · **Setup Core Venturo** (proyek baru) atau **Audit Sistem** (`aplikasi_berjalan: true`) · Akses & Deployment · Backup & Keamanan · Dokumentasi & Transfer Ilmu.
- Sisakan **cadangan penyesuaian & hasil UAT** (kuota − estimasi); beri tahu pengguna bila < 5%.
- Pengerjaan yang melebihi ukuran yang disepakati **ditanggung Venturo** (tidak memotong kuota). Sisa kuota hangus di akhir periode.
- **Layanan Berlangganan Bulanan** (di luar Total Investasi): **Layanan Lanjutan** default 2 fitur Rp7.500.000/bulan (`layanan_lanjutan.fitur` bisa dinaikkan) mulai tanggal 1 bulan setelah periode terakhir; **Venturo Cloud** (`venturo_cloud.paket`, rate card `references/venturo-cloud.md`) mulai bulan terakhir periode (1 bulan sebelum go-live); dukungan DevOps hanya disebut untuk paket VPS. Bila Klien menyediakan server sendiri, `venturo_cloud: null`.
- **Pajak**: kalimat baku (sudah di build.py) — *"Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien."* Jangan ada baris PPN.

### Tanggal mulai
- Setup Awal dibayar **saat tanda tangan**; periode Managed Service dimulai **tanggal 1 bulan kalender berikutnya** (`mulai`, mis. "Desember 2026"). Periode tidak pernah dimulai di tengah bulan, karena kuota bulanan hangus di akhir periode.
- Hari di antara tanda tangan dan tanggal mulai dipakai untuk Setup Awal. Bila tanda tangan bergeser ke bulan berikutnya, geser `mulai` dan naikkan nomor revisi.
- Invoice termin = akhir tiap bulan periode (otomatis).

## 4. Struktur dokumen (dibangun build.py)
**Penawaran:** Hero → paragraf pembuka baku → **1 Lingkup Layanan** (kotak Setup Awal · kotak Managed Service: satuan & ukuran fitur, isi 1 fitur, empat kategori, rujukan Lampiran, kelebihan ditanggung Venturo, pelatihan tambahan, laporan harian & bulanan, kuota hangus · kotak Sudah Termasuk di Semua Paket) → **2 Rincian Biaya** (Setup Awal + Bulan n dengan ringkasan & kuota → Total Investasi; catatan harga paket; tabel Layanan Berlangganan Bulanan) → **3 Pembayaran** (pajak, H+14, Setup setelah pembayaran pertama, penghentian sementara, penagihan Layanan Lanjutan & Venturo Cloud → rekening → tabel termin → Total Pembayaran) → **4 Batasan dan Pengecualian** (server di luar Venturo Cloud, `batasan` dari data, tahap berikutnya, out-of-pocket, pekerjaan mendesak di luar jam kerja 2× ukuran fitur, pemeliharaan setelah periode, pekerjaan di luar kuota) → **5 Persetujuan** (kotak pilihan Layanan Lanjutan & Venturo Cloud, tanda tangan).
- **Jangan tulis angka SLA** di penawaran (deck menulis "isu kritis direspons maks. 1 hari kerja"; di penawaran cukup "prioritas utama"). Angka SLA hanya di Service Agreement.

**Lampiran Estimasi Fitur:** Hero → intro → **1 Alur Sistem** (diagram dari `alur`, halaman 1) → **2 Ringkasan Estimasi** (mulai halaman baru; Modul | Kategori · Platform | Fitur; Total estimasi · Kuota paket · Cadangan) → **3 Rincian per Item** (No | Item | Ukuran | Fitur, judul modul + subtotal → Total Estimasi) → **4 Panduan Ukuran Fitur** (tabel 4 kategori × 4 ukuran) → **5 Pengembangan Tahap Berikutnya** (bila ada) → **Asumsi & Catatan**. Tanpa blok tanda tangan penuh.

**Service Agreement** (23 pasal): Pasal 3 menyebut model kuota fitur bulanan + rujukan Lampiran Estimasi Fitur + selisih di atas ukuran disepakati ditanggung Venturo; Pasal 4 Support Service (respons WhatsApp 15 menit, bug maks. 2 jam, penanganan bug tidak memotong kuota fitur); Pasal 9 laporan harian/mingguan/bulanan dengan pemakaian kuota fitur; Pasal 11 di luar jam kerja 2× ukuran fitur; Pasal 14 keterlambatan; Pasal 17 sisa kuota tidak dapat diuangkan; Pasal 19 garansi 30 hari per rilis. Isi SA adalah dokumen hukum — perubahan pasal lain dikonfirmasi ke pengguna.

## 5. Penamaan, render & verifikasi
**Nomor dokumen:** `VEN/<Project>/<Tahun>/<Rev>` — Project singkatan maks 2 kata, **huruf dan angka saja** (`VEN/TGXPortal/2026/001`, bukan `TGX-Portal`). `file` = `VEN-<Project>-<Tahun>-<Rev>`.
```bash
python3 <folder skill ini>/scripts/build.py data.json <output>/src
python3 <folder skill ini>/scripts/render.py <output>/src/penawaran.html "<output>/VEN-<Project>-<Tahun>-<Rev>.pdf" "VEN/<Project>/<Tahun>/<Rev>"
python3 <folder skill ini>/scripts/render.py <output>/src/lampiran.html  "<output>/VEN-<Project>-<Tahun>-<Rev>-Lampiran-Estimasi.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Lampiran Estimasi Fitur"
python3 <folder skill ini>/scripts/render.py <output>/src/sla.html       "<output>/VEN-<Project>-<Tahun>-<Rev>-Service-Agreement.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Service Agreement"
```
- Satu set = satu nomor revisi. Setiap perubahan → build + render ulang **ketiganya**, hapus versi lama. Revisi yang belum diunggah/dikirim ke klien boleh diperbaiki tanpa menaikkan nomor; naik bila isi/harga berubah setelah dikirim atau perubahan diminta di sesi baru.
- Verifikasi (`mkdir -p <output>/preview && pdftoppm -r 60 -png <pdf> <output>/preview/<nama>`): diagram Alur Sistem utuh di halaman 1 Lampiran, panah tidak menembus kotak, teks tidak terpotong, tanpa halaman sisa kecil, logo utuh, TTD/paraf tampil, nomor dokumen konsisten, total & termin cocok.

## 6. Istilah & redaksi
| Aturan | Keterangan |
|---|---|
| Satuan **fitur** | "10 fitur", "0,5 fitur", "kuota fitur"; header tabel "Fitur". Jangan pakai "Poin", "Delivery Point", atau "jam" |
| Tim "kurang lebih 100 orang" | Semua dokumen |
| Penanda tangan Venturo | Yulianto Frandi, **CEO**; `ttd.png` di kotak Venturo, `paraf.png` di footer |
| Klien | Kotak tanda tangan kosong + Nama, Jabatan, Tanggal; **tanpa kotak meterai** |
| Istilah ke klien | "rilis pertama" / "fitur utama" / "pengembangan tahap berikutnya" — bukan "MVP" |
| Masa berlaku | **Tidak** ditulis di dokumen (disampaikan di pesan pengantar `proposal-upload`) |
| Format | Bahasa Indonesia formal; `Rp10.000.000`; desimal koma (`0,5`); tanggal "16 November 2026" |

## 7. Di luar skill ini
Unggah PDF dan pesan WhatsApp pengantar (termasuk masa berlaku): skill `proposal-upload`.

## Mengganti tanda tangan
Bila pengguna memberi file TTD baru: render PDF/gambar ke PNG 300 dpi, alpha = luminans (gelap → opak, putih → transparan; untuk PNG RGBA, pakai alpha aslinya dan buang yang mendekati putih), crop bbox, simpan menimpa `assets/ttd.png` / `assets/paraf.png`.
