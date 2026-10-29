---
name: proposal-pdf
description: Membuat TIGA PDF Venturo langsung jadi dari System Requirement Brief klien (txt/pdf/docx) — (1) Penawaran Layanan + form persetujuan (Managed Service) dengan tanda tangan+stempel dan paraf CEO, (2) Lampiran Estimasi Delivery Point (Poin per modul & item, pengembangan tahap berikutnya), dan (3) Service Agreement 23 pasal — dengan estimasi Poin, paket bulanan, termin, dan Layanan Lanjutan setelah go-live dihitung dari brief. Pakai saat diminta "buat PDF penawaran", "penawaran dari brief", "buat penawaran dari requirement", "estimasi delivery point", "lampiran estimasi", "service agreement", "penawaran baru untuk klien X", atau "export penawaran ke PDF".
---

# Penawaran Venturo dari Brief → 3 PDF

Dari satu **System Requirement Brief** klien, skill ini menghasilkan tiga PDF dengan **satu nomor dokumen dan satu nomor revisi**:
1. **Penawaran Layanan**: penawaran sekaligus form persetujuan. Fungsinya mengikat, bukan membujuk (bujukan ada di presentasi).
2. **Lampiran Estimasi Delivery Point**: rincian Poin per modul dan item yang menjadi dasar paket.
3. **Service Agreement**: perjanjian induk kerja sama Managed Service (23 pasal) yang menjadi rujukan penawaran.

Acuan kualitas: sesi penawaran *Platform Pembelajaran Kebijakan – Universitas Sebelas Maret*, Rev 016. Hasil skill harus setara dengan itu.

## 0. Cek alat
Jangan jalankan skrip dengan `python3 -I`: pip di macOS memasang Playwright ke user site-packages, sedangkan `-I` mematikannya (`ModuleNotFoundError`). Jalankan `mkdir -p <folder preview>` sebelum `pdftoppm`.

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
- `assets/contoh-penawaran.html` — template Penawaran final (Rev 016).
- `assets/contoh-lampiran-estimasi.html` — template Lampiran Estimasi Delivery Point final.
- `assets/contoh-service-agreement.html` — template Service Agreement final.
- `scripts/render.py` — `python3 <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]`; render A4 dengan Playwright Chromium + footer (prefix · No. dokumen | Paraf Venturo [paraf.png] + Paraf Klien | Halaman X dari Y), padding footer 12 mm. Membaca `paraf.png` dari folder yang sama dengan HTML.
- `references/venturo-cloud.md` — rate card Venturo Cloud (Shared Hosting & VPS) dan aturan pemakaiannya.
- `references/generator-uns/` — `build.py`, `sla.py`, `fix.py` dari sesi UNS: **contoh** struktur data modul → HTML. Skrip ini membaca file template lama dari folder kerja sesi itu, jadi jadikan acuan pola, bukan untuk dijalankan apa adanya.

## 1. Alur
1. **Input:** System Requirement Brief (txt/pdf/docx). Baca seluruh isinya.
2. **Data klien:** bila nama, jabatan, instansi, atau alamat tidak ada di brief, **tanyakan sekali di awal** dalam satu pesan, dan jangan tanyakan hal lain. Jabatan boleh umum (mis. "Pimpinan"); nama penanda tangan klien dikosongkan bila tidak diketahui.
3. **Estimasi Poin** per modul → item (§2), lalu pilih paket (§3).
4. **Susun 3 HTML** dari template (§4–§6), dengan nomor dokumen dan revisi yang sama.
5. **Render ketiganya** (§8) → **verifikasi** (§9) → kirim **3 file** dengan SendUserFile.
6. **Laporan singkat** ke pengguna: ringkasan biaya, Poin per modul, cadangan (beri tahu bila < ±5%), item pengembangan tahap berikutnya, dan hal yang perlu dicek.

## 2. Aturan estimasi Poin
- **Kalibrasi internal: 1 Poin ≈ 1 jam kerja senior (dibantu AI).** Jangan pernah menampilkan "jam" kerja ke klien; ke klien Poin disajikan sebagai **besar pekerjaan**.
- Hitung **per tugas** (backend, frontend, pengujian), bukan per fitur. Satu item = akumulasi tugasnya, sehingga angka item bisa besar (mis. 70 Poin).
- Bobot per tugas tetap dicantumkan di dokumen: ringan 0,25 · kecil 0,5 · menengah 0,75 · besar 1 Poin.
- Meeting review & pelatihan: 1 Poin = 1 jam sesi.
- Pecah per modul. Pola modul (sesuaikan dengan brief): Fondasi & Administrasi · UI/UX (web & mobile) · tiap kanal/fitur utama · Notifikasi · Laporan & Analitik · Pembayaran (bila ada) · Aplikasi Mobile (fitur pengguna akhir seperti peserta/dosen; admin cukup web) · Meeting Review & Pelatihan.
- Patokan dari sesi UNS (scope LMS + hackathon + forum + internship + mobile): total **818 Poin**; UI/UX 72, Fondasi 61, LMS 132, Mobile 232.
- **Fitur mahal/lama yang bukan inti** tidak masuk paket. Masukkan ke Lampiran bagian **"Pengembangan Tahap Berikutnya"** (§5), bukan sebagai pengecualian di Asumsi.
- Fitur yang disebut brief sebagai "opsional" tapi diputuskan pengguna masuk pekerjaan → jadikan modul biasa (contoh: Payment Gateway 24 Poin).

## 3. Paket & biaya
- Tarif **Rp150.000/Poin**. Setup Awal **Rp10.000.000** (sekali bayar, tidak memotong Poin).
- Paket bulanan: 50 / 100 / 150 / 200 / 250 Poin. Boleh beberapa bulan (contoh: 250 × 3 + 100 = 850 Poin).
- Sisakan **cadangan penyesuaian & hasil UAT** (contoh 32 Poin); beri tahu pengguna bila cadangan < ±5%.
- Termin: Setup Awal saat tanda tangan; tiap bulan ditagih di akhir bulan.
- **Layanan Berlangganan Bulanan** (wajib dicantumkan, **di luar Total Investasi**), satu tabel berisi dua baris:
  1. **Layanan Lanjutan** — *Managed Service – Pemeliharaan & Pengembangan Lanjutan*: default 50 Poin/bulan (Rp7.500.000/bulan), mulai tanggal 1 bulan setelah periode proyek terakhir.
  2. **Venturo Cloud** — server production dari rate card `references/venturo-cloud.md`, kolom Poin "–", mulai 1 bulan sebelum go-live.

### Tanggal mulai Managed Service
- Setup Awal dibayar **saat tanda tangan**, sebelum periode kerja pertama dimulai; pembayaran ini tidak memakai jatuh tempo H+14.
- Periode Managed Service dimulai **tanggal 1 bulan kalender berikutnya** setelah tanda tangan (tanda tangan 28 Okt → mulai 1 Nov; tanda tangan 5 Nov → mulai 1 Des).
- Hari di antara tanda tangan dan tanggal mulai dipakai untuk pekerjaan **Setup Awal** (kickoff, roadmap, boilerplate, repository, staging) dan tidak memotong Poin.
- Periode **tidak pernah dimulai di tengah bulan**: kuota Poin bulanan hangus di akhir periode, jadi bulan yang terpotong berarti Poin terbuang.
- Tanggal mulai mengikuti perkiraan tanggal tanda tangan. Bila tanda tangan bergeser ke bulan berikutnya, geser seluruh periode dan naikkan nomor revisi.
- Tanggal invoice termin = akhir tiap bulan periode. Layanan Lanjutan mulai tanggal 1 bulan setelah periode terakhir.

## 4. Dokumen 1 — Penawaran Layanan (`contoh-penawaran.html`)
**Hero:** "Managed Service" + nama project; kartu No./Project/Tanggal; kartu "Kepada Yth." (Bapak/Ibu [Jabatan], instansi, alamat). Paragraf pembuka: tim IT profesional **"kurang lebih 100 orang"**.

**1. Lingkup Layanan**
- Kartu *Setup Awal* (proyek baru): Kickoff & Roadmap · Setup Core Venturo (boilerplate) · Akses & Deployment · Backup & Keamanan · Dokumentasi & Transfer Ilmu.
- Kartu *Managed Service*, **urutan: pengerjaan dulu, baru support**:
  1. Sistem Delivery Point (selanjutnya disebut Poin) berdasarkan bobot dan kompleksitas pekerjaan
  2. Kategori pekerjaan: ringan (0,25 Poin), kecil (0,5 Poin), menengah (0,75 Poin), dan besar (1 Poin)
  3. Cakupan pekerjaan …
  4. Estimasi dan bobot Poin setiap fitur tercantum pada Lampiran Estimasi Delivery Point dokumen ini
  5. Perhitungan Poin dapat terdiri dari beberapa pekerjaan dalam satu fitur
  6. Meeting review dan pelatihan: 1 Poin setara dengan 1 jam sesi (tanpa "terlepas dari jumlah anggota tim…")
  7. Sisa Poin yang tidak terpakai hangus di akhir periode
  8. Dukungan teknis responsif melalui WhatsApp, dengan prioritas penanganan bug berdasarkan dampak
  9. Garansi perbaikan bug tanpa biaya tambahan
- **Jangan tulis angka SLA** (15 menit, 2 jam, 30 hari) di penawaran. Angka hanya di Service Agreement.

**2. Rincian Biaya**
- Tabel: Setup Awal + satu baris per bulan (deskripsi modul yang dikerjakan bulan itu) → **Total Investasi**.
- Di bawahnya tabel **"Layanan Berlangganan Bulanan"** dengan subjudul *"Di luar Total Investasi"* (menggantikan judul lama "Layanan Lanjutan Setelah Go-Live"), satu section dua baris:
  1. *Managed Service – Pemeliharaan & Pengembangan Lanjutan* — 50 Poin/bulan, Rp7.500.000, mulai bulan setelah periode proyek.
  2. *Venturo Cloud – [Jenis] [Paket]* — deskripsi fungsi server (web, API mobile, database), spesifikasi, dan opsi upgrade; dukungan tim DevOps disebut **hanya untuk paket VPS**; kolom Poin "–"; mulai 1 bulan sebelum go-live.
- Istilah **"Layanan Lanjutan"** tetap dipakai untuk baris Managed Service 50 Poin, karena dirujuk di Pembayaran, Batasan, Persetujuan, Lampiran, dan Service Agreement (Pasal 17 & 19).

**3. Pembayaran**
- Kalimat pajak baku: *"Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien."* (jangan tulis "PPN tidak ditagihkan", jangan ada baris PPN; tinjau ulang bila Venturo sudah PKP); H+14; Setup dimulai setelah pembayaran pertama; layanan dihentikan sementara bila telat bayar.
- Tambahkan: *"Layanan Lanjutan (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai [tanggal] dan berlanjut otomatis setiap bulan hingga salah satu pihak menghentikannya dengan pemberitahuan tertulis 30 (tiga puluh) hari sebelumnya."*
- Tambahkan: *"Venturo Cloud (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai [tanggal] dengan ketentuan perpanjangan dan penghentian yang sama dengan Layanan Lanjutan."*
- Rekening BCA + tabel termin → **Total Pembayaran** (Setup Awal: "Saat tanda tangan").

**4. Batasan dan Pengecualian** — biaya pihak ketiga dari brief (hosting/server, CDN video, DRM berlisensi, lisensi video conference, email/push, akun Apple/Google, akses API kampus/pihak ketiga disediakan klien, akun merchant & biaya transaksi payment gateway, konten disediakan klien), out-of-pocket, pekerjaan mendesak di luar jam kerja 2× bobot Poin, ditambah:
- *"[Fitur tahap berikutnya] direncanakan pada pengembangan tahap berikutnya setelah rilis fitur utama (lihat Lampiran Estimasi Delivery Point)"*
- *"Pemeliharaan setelah periode [bulan terakhir] mengikuti ketentuan Layanan Lanjutan pada bagian 2"*
- *"Server production di luar Venturo Cloud (apabila Klien memilih menyediakan server sendiri), serta domain"*
- *"Permintaan pekerjaan di luar alokasi Poin dalam dokumen ini akan dituangkan dalam penawaran atau kontrak baru…"*

**5. Persetujuan** — kalimat persetujuan (bagian tidak terpisahkan dari Service Agreement), lalu kotak pilihan:
☐ *Lanjutkan Managed Service 50 Poin/bulan mulai [tanggal]* ☐ *Diputuskan kemudian*
☐ *Venturo Cloud [Paket] Rp[harga]/bulan mulai [tanggal]* ☐ *Server disediakan Klien*
Blok tanda tangan: Venturo (Yulianto Frandi, CEO, `ttd.png`) · Klien (nama kosong bila belum diketahui, jabatan umum).

## 5. Dokumen 2 — Lampiran Estimasi Delivery Point (`contoh-lampiran-estimasi.html`)
- Hero: "Lampiran Penawaran Layanan" / "Estimasi Delivery Point" + nama project; kartu Lampiran (No. penawaran), Project, Tanggal; kartu Kepada Yth.
- Intro: *"…Poin setiap item merupakan akumulasi tugas di dalamnya (backend, frontend, pengujian) dengan bobot per tugas: ringan 0,25 · kecil 0,5 · menengah 0,75 · besar 1 Poin."*
- **1. Ringkasan Estimasi:** tabel Modul | Platform | Poin, lalu 3 baris **biasa (tidak di-highlight)**: Total estimasi · Paket Managed Service · Cadangan penyesuaian & hasil UAT.
- **2. Rincian per Item Pekerjaan** (mulai halaman baru): No | Item Pekerjaan | Poin, baris judul modul "· Platform" + subtotal; tanpa kolom Kategori. Baris akhir **Total Estimasi** (highlight).
- **3. Pengembangan Tahap Berikutnya** *(setelah rilis fitur utama)*:
  - Kolom: Item Pekerjaan | **Estimasi Poin**.
  - Setiap item menjelaskan kondisi di rilis pertama, mis. *"…Pada rilis pertama, sesi langsung memakai tautan yang diinput manual."*
  - Catatan: *"Fitur di atas sengaja tidak dimasukkan ke rilis pertama agar fitur utama dapat dirilis lebih cepat dengan biaya yang efisien. Fitur ini dapat ditambahkan setelah rilis melalui Layanan Lanjutan atas persetujuan Klien, dan belum termasuk dalam Total Investasi. Estimasi Poin di atas dikonfirmasi ulang saat fitur akan dikerjakan."*
- **4. Asumsi & Catatan:** hanya asumsi kerja (estimasi disepakati di awal, perubahan lingkup dihitung ulang, API pihak ketiga tersedia, role yang diasumsikan, cakupan mobile, jaminan kualitas tidak memotong Poin). Hal yang "belum termasuk" ada di bagian 3, bukan di sini.
- Footer paraf Venturo + klien; **tanpa blok tanda tangan penuh**.

## 6. Dokumen 3 — Service Agreement (`contoh-service-agreement.html`)
Diadaptasi dari SLA Venturo untuk model Managed Service. Hero: "Perjanjian Induk Kerja Sama" / "Service Agreement" / "Venturo Managed Service"; kartu No., Penawaran, Tanggal; kartu Klien.

23 pasal (judul bernomor):
1. **Para Pihak** — PT Venturo Pro Indonesia, Jl. Rinjani No. 26 Oro-oro Dowo, Klojen, Malang 65119, diwakili Yulianto Frandi selaku CEO; Klien diwakili "______ selaku [Jabatan]".
2. Masa Berlaku · 3. Lingkup Pengerjaan (rujuk nomor Penawaran & Lampiran)
4. **Support Service**:
   - Jam kerja Senin–Jumat 08.00–17.00 WIB; respons WhatsApp maks. 15 menit pada jam kerja; di luar jam kerja respons pada hari yang sama, kecuali laporan bug yang ditangani sesuai ayat 6.
   - Major/Minor Bug dibedakan **hanya untuk urutan prioritas** (Major lebih dulu).
   - Ayat 6: *"Venturo berupaya menyelesaikan setiap Major Bug maupun Minor Bug dalam waktu maksimal 2 (dua) jam sejak laporan diterima, baik di dalam maupun di luar jam kerja operasional. Waktu pukul 21.00–08.00 WIB tidak dihitung; laporan yang diterima pada rentang tersebut mulai dihitung pukul 08.00 WIB."* (berlaku setiap hari, termasuk akhir pekan/libur)
   - Ayat 7: bila lebih dari 2 jam, Venturo **wajib** menyampaikan penyebab, langkah penanganan, estimasi selesai, dan workaround bila memungkinkan dalam batas 2 jam itu, lalu terus melaporkan perkembangan.
   - Penanganan bug tidak memotong Poin.
5. Komunikasi — Space, Grup WhatsApp, Online Meeting, **GitHub Repository** (bukan GitLab)
6. Project Management · 7. Metode Development (Scrum) · 8. Deployment Environment (staging gratis; production: *"Infrastruktur Production disediakan oleh Klien, atau melalui layanan Venturo Cloud apabila dipilih Klien pada Penawaran Layanan."*)
9. Laporan Pekerjaan — **harian** (WA), **meeting review mingguan**, **rekap bulanan** termasuk realisasi pemakaian Poin
10. Biaya Out of Pocket · 11. **Pekerjaan di Luar Jam Kerja** (2× bobot Poin)
12. Kerahasiaan
13. **Hak Kekayaan Intelektual** — source code & HKI **milik Klien**, diserahkan saat serah terima setelah lunas (ayat 2 "…dengan memperhatikan ketentuan ayat 4"). Ayat 4: *"Kepemilikan HKI oleh Klien tidak membatasi hak Venturo untuk menggunakan kembali komponen umum, pustaka kode, kerangka dasar aplikasi (Setup Core Venturo/boilerplate), serta pengetahuan dan metode teknis yang tidak spesifik pada bisnis Klien untuk proyek lain, sepanjang tidak memuat Informasi rahasia, data, maupun fitur dan logika bisnis yang khusus dikembangkan untuk Klien."* Ayat 5: data milik Klien.
14. Keterlambatan Pengerjaan (karena Venturo: tambah sumber daya tanpa biaya dan tanpa memotong Poin; karena Klien: pekerjaan tambahan dihitung Poin)
15. **Tim Pelaksana** · 16. **Perekrutan** — biaya pengalihan *"6 (enam) kali gaji bulanan terakhir pegawai yang bersangkutan"*
17. Terminasi Kontrak (performa 30 hari; bisnis 60 hari; Layanan Lanjutan 30 hari; sisa Poin tidak dapat diuangkan)
18. Berita Acara Serah Terima · 19. Garansi (30 hari kalender sejak rilis tiap fitur ke Production; setelahnya lewat Layanan Lanjutan)
20. Pembatasan Tanggung Jawab · 21. **Force Majeure** · 22. Penyelesaian Perselisihan (musyawarah untuk mufakat → BANI)
23. Persetujuan + blok tanda tangan (sama dengan penawaran)

Bersihkan sisa template klien lain (mis. kode "YPIA" di footer, "PT Kuda Pacu").

## 7. Istilah & redaksi
| Aturan | Keterangan |
|---|---|
| Singkatan **Poin**, bukan "DP" | Penyebutan pertama: "Delivery Point (selanjutnya disebut Poin)"; header tabel "Poin"; "250 Poin", "1 Poin = 1 jam" |
| Tim "kurang lebih 100 orang" | Semua dokumen (bukan "lebih dari 100 orang") |
| Penanda tangan Venturo | Yulianto Frandi, **CEO**; tanggal tanda tangan = tanggal dokumen; selalu tempel `ttd.png` di kotak Venturo dan `paraf.png` di footer setiap halaman ketiga PDF |
| Nama perusahaan | **PT Venturo Pro Indonesia** |
| Klien | Kotak tanda tangan kosong + Nama, Jabatan, Tanggal; **tanpa kotak meterai** |
| Angka SLA | Hanya di Service Agreement; penawaran cukup menyebut manfaat |
| Istilah ke klien | "rilis pertama" / "fitur utama" / "pengembangan tahap berikutnya" — bukan "MVP" atau "Item Opsional" |
| Masa berlaku | **Tidak** ditulis di dokumen (disampaikan di pesan pengantar) |
| Format | Bahasa Indonesia formal; rupiah bertitik (`Rp10.000.000`); desimal koma (`0,75`); tanggal "22 Oktober 2026" |
| Tipografi | ’ untuk apostrof, “ ” untuk kutipan, – untuk rentang |

**Nomor dokumen:** `KODE/Project/Tahun/Revisi` → `VEN/PolicyLab/2026/016`. KODE = kode perusahaan (Venturo = VEN; tanyakan bila bukan Venturo). Project = singkatan maks 2 kata, tanpa spasi. Tahun 4 digit. Revisi 001, 002, …

## 8. Desain & teknis
- Warna: brand-teal #259ead, teal-700 #1b7a86, teal-800 #176a74, teal-50 #eaf6f7, ink #1f2a2e, muted #58585a, subtle #6b7072, border #d5dfe0, surface-200 #f4f7f6, hijau diskon #3c7a2a. Sumber design system lengkap: artifact https://claude.ai/artifact/9Xz8mMr54wVGngfEdtyfFn.
- Template sudah memuat override berikut; pertahankan saat mengisi:
```css
@page{size:A4;margin:11mm 12mm 15mm 12mm}
.hero{margin:-11mm -12mm 0;padding:8mm 12mm 3mm}
.logo{margin-left:0}
tr.grand td{background:var(--t50);border:0;border-top:.5mm solid var(--teal);padding:3mm;vertical-align:middle}
tr.grand td:first-child{text-align:left;font-size:8.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--t7);border-bottom-left-radius:2.5mm}
tr.grand td:last-child{font-size:11pt;font-weight:800;color:var(--t8);border-bottom-right-radius:2.5mm}
```
  Khusus Service Agreement (banyak pasal):
```css
h2{font-size:10.5pt;margin:5mm 0 1.8mm;gap:2.2mm;line-height:1.2}
h2 i{width:auto;min-width:5.6mm;height:5.6mm;padding:0 1.2mm;border-radius:1.4mm;font-size:8pt;font-weight:700}
.sec p,.sec ol,.sec ul{font-size:9pt}
```
- Tata letak: Penawaran **jangan** memaksa `break-before:page` di Batasan (biarkan Pembayaran + Batasan satu halaman, Persetujuan utuh). Lampiran: bagian 2 Rincian mulai halaman baru agar judul tidak yatim.
- `<title>` HTML = nama file (tampil di tab browser saat klien membuka link).
- Render (salin `assets/*` ke folder kerja lebih dulu):
```bash
python3 <folder skill ini>/scripts/render.py penawaran.html "<output>/VEN-<Project>-<Tahun>-<Rev>.pdf" "VEN/<Project>/<Tahun>/<Rev>"
python3 <folder skill ini>/scripts/render.py lampiran.html  "<output>/VEN-<Project>-<Tahun>-<Rev>-Lampiran-Estimasi.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Lampiran Estimasi Delivery Point"
python3 <folder skill ini>/scripts/render.py sla.html       "<output>/VEN-<Project>-<Tahun>-<Rev>-Service-Agreement.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Service Agreement"
```

## 9. Penamaan, revisi & verifikasi
- Nama file **tanpa spasi**, pakai "-": `VEN-<Project>-<Tahun>-<Rev>.pdf` · `…-Lampiran-Estimasi.pdf` · `…-Service-Agreement.pdf`.
- Satu set = satu nomor revisi. Setiap perubahan (isi maupun tampilan) → render ulang **ketiganya**, naikkan nomor revisi, dan hapus file versi lama dari `<output>`.
- Verifikasi tiap render (`pdftoppm -r 60` per halaman): jumlah halaman wajar tanpa halaman sisa kecil, logo utuh, TTD/paraf tampil transparan, nomor dokumen konsisten di ketiga file, tidak ada sisa "DP"/"GitLab"/"lebih dari 100", serta total dan termin cocok.

## 10. Di luar skill ini
Pesan WhatsApp pengantar dokumen, termasuk masa berlaku penawaran, adalah skill terpisah, bukan bagian `proposal-pdf`.

## Mengganti tanda tangan
Bila pengguna memberi file TTD baru: render PDF/gambar ke PNG 300 dpi, alpha = luminans (gelap → opak, putih → transparan; untuk PNG RGBA, pakai alpha aslinya dan buang yang mendekati putih), crop bbox, simpan menimpa `ttd.png` / `paraf.png` di folder kerja.
