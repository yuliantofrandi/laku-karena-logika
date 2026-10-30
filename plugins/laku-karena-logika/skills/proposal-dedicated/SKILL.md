---
name: proposal-dedicated
description: Membuat TIGA PDF penawaran Venturo model DEDICATED TEAM (man power based) dari System Requirement Brief, RFI, atau dokumen tender klien (txt/pdf/docx) — (1) Penawaran Layanan Dedicated Team + form persetujuan dengan tanda tangan+stempel dan paraf CEO, (2) Lampiran Rincian Biaya & Rencana Kerja, dan (3) Service Agreement Dedicated Team. Penawaran disusun PER FASE (Requirement → Fondasi → Fitur Utama → SIT → UAT & Pentest → Go-Live → Hypercare → Annual Support) dengan jumlah orang per fase dalam pecahan (1, ½, ¼), tarif Long Term/Short Term, Engineering Kick-off proporsional, perjalanan dinas, dan termin per bulan — dibangun lewat generator scripts/build.py dari satu file data. Pakai saat diminta "penawaran dedicated team", "proposal dedicated", "penawaran man power", "hire programmer/tim dari Venturo", "outsourcing tim", "respons RFI/tender", atau "buat penawaran dedicated dari brief". Untuk model Managed Service berbasis Poin, pakai proposal-managed.
---

# Penawaran Dedicated Team dari Brief → 3 PDF

**Managed Service** menghitung Poin; **Dedicated Team** menghitung **berapa orang di setiap bulan**, ditambah **fitur yang dikerjakan pada periode itu**. Penawaran disusun **per fase**, jumlah orang boleh berbeda di setiap fase. Tim "bekerja khusus untuk proyek Klien sesuai alokasi setiap fase" (bukan "penuh waktu").

Tiga PDF, satu nomor dokumen dan satu nomor revisi:
1. **Penawaran Layanan Dedicated Team** — penawaran sekaligus form persetujuan.
2. **Lampiran Rincian Biaya & Rencana Kerja** — komponen biaya per orang, komposisi, alokasi per fase, fitur per fase.
3. **Service Agreement Dedicated Team** — perjanjian induk 23 pasal.

Acuan kualitas: sesi penawaran Customer 360 Dashboard & Analytics (rev 015, Oktober 2026). Contoh data di `assets/contoh-data.json` mengikuti pola dan hitungannya dengan klien disamarkan.

## Satuan & rumus
| Satuan | 1 | ½ | ¼ |
|---|---|---|---|
| Orang | 8 jam/hari | 4 jam/hari | 2 jam/hari |
| Bulan | 4 minggu | 2 minggu | 1 minggu |

**Biaya = tarif bulanan × orang × bulan.**

## 0. Alat
- Cek dengan perintah yang sama dengan perintah render: `python3 -c "import playwright"` dan `command -v pdftoppm`. Bila kurang, minta izin sebelum memasang (`python3 -m pip install playwright`, `python3 -m playwright install chromium`, `brew install poppler`).
- **Jangan jalankan skrip dengan `python3 -I`**: pip di macOS memasang Playwright ke user site-packages, sedangkan `-I` mematikannya (`ModuleNotFoundError`). Jalankan `python3 <skrip> …` biasa.
- Jalankan `mkdir -p <folder preview>` sebelum `pdftoppm` (tanpa itu gagal "Could not write image").
- Folder hasil: folder yang disebut pengguna, atau `penawaran/` di working directory (`<output>`); folder kerja HTML `<output>/src`.

## Aset & skrip (`<folder skill ini>/`)
- `scripts/build.py` — **generator**: `python3 <folder skill ini>/scripts/build.py <data.json> <output>/src` membangun `penawaran.html`, `lampiran.html`, `sla.html` (+ salin logo, bg, TTD, paraf, font). Menghitung skema Long/Short Term, Kick-off proporsional, biaya per fase, timeline (satuan ½ bulan), termin per bulan kalender, perjalanan dinas, dan meng-`assert` Total Investasi = Σ termin = Total Pembayaran serta tidak ada sisa teks yang dilarang (`cek_tidak_boleh_ada`). **Revisi = ubah data → build → render ulang.**
- `scripts/render.py` — `python3 <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]`.
- `assets/contoh-data.json` — format data lengkap (klien, posisi, fase + lingkup + fitur + alokasi, perjalanan dinas, batasan, Venturo Cloud/on-premise, diskon). Salin lalu ganti isinya.
- `assets/dedicated.css`, `assets/sa-dedicated.html` — gaya dan template Service Agreement (dipakai build.py).
- `assets/contoh-*.html` — hasil build dari contoh data, untuk acuan visual.
- `references/pricelist-dedicated.md` — pricelist Long Term & Short Term, aturan Kick-off, tarif perjalanan dinas.
- `references/venturo-cloud.md` — rate card Venturo Cloud.

## 1. Input & data klien
- Input: System Requirement Brief, RFI, atau dokumen tender (txt/pdf/docx). Data klien yang tidak ada ditanyakan **sekali** di awal.
- **Penerima**: bila nama/jabatan tidak disebut, pakai nama unit (mis. "Tim Pengadaan & Digitalisasi"). Alamat boleh dari halaman pengumuman resmi (e-proc).
- **Jabatan dan nama penanda tangan klien yang tidak diketahui dikosongkan** (`ttd_nama`/`ttd_jabatan` = ""): tampil sebagai garis titik-titik di blok tanda tangan dan "diwakili oleh ____ selaku ____" di SA. **Jangan isi "Pimpinan".**
- **Tanggal mulai**: proyek biasa → tanggal 1 bulan berikutnya setelah tanda tangan; **tender → ±2 bulan setelah tanggal dokumen** (dokumen 28 Okt 2026 → mulai 1 Jan 2027).

## 2. Posisi & komposisi tim
**Hanya jabatan yang ada di Venturo:** Software Engineer (Senior/Intermediate), Pentester, DevOps, UI/UX, QA, BA. Spesialisasi ditulis setelah "–" (mis. *Senior Software Engineer – Backend & Arsitektur*, *Senior Software Engineer – Integrasi Data* untuk ETL/initial load/rekonsiliasi/data mart, *Software Engineer – Backend Analitik*, *Software Engineer – Frontend Dashboard*). **Jangan** memakai jabatan seperti "Data Engineer". Level di data: `Senior`, `Intermediate`, `Pentester/DevOps`, `UI/UX/QA/BA`.

Siapa masuk fase mana:
- **Requirement Analysis / Design**: Backend Senior, Integrasi Data, Frontend, BA, UI/UX — **tanpa QA dan DevOps**.
- **QA** mulai di fase pengembangan (saat test scenario disusun).
- **DevOps hanya di fase belakang**: SIT & Performance Test, Go-Live, Annual Support (development, staging, CI/CD sudah ada di ekosistem Venturo). Peran: environment Testing & Production on-premise klien, deployment, monitoring, backup, hardening.
- **BA** penuh di Analysis, UAT, Go-Live; ¼–½ di fase pengembangan; tidak di SIT. BA juga menangani pelatihan (functional, key user/train the trainer), Design & Build Report, definisi KPI.
- **Frontend** mengikuti jumlah layar fase itu; fase dominan backend/integrasi cukup 2; Hypercare ½. Jangan menggelembungkan.
- **UI/UX** cukup di fase pertama (Short Term); bila brief sudah punya prototype, perannya review dan desain final.
- **Pentester** di UAT & Pentest + ¼ untuk retest di Go-Live (Short Term).

**Preferensi pemilik — timeline pendek, tim besar:** fase pengembangan inti dibuat **1 bulan per fase** dengan menambah orang (bukan 2 bulan tim kecil), total orang-bulan dijaga kurang lebih sama. Cek setiap orang tambahan:
- terlibat **< 2 bulan** → posisi terpisah "… (tambahan)" yang otomatis **Short Term**, tanpa Kick-off;
- terlibat **≥ 2 bulan** → naikkan alokasi posisi Long Term-nya (Kick-off proporsional ikut naik).

## 3. Harga (`references/pricelist-dedicated.md`)
- **Long Term** (terlibat ≥ 2 bulan, dari awal fase pertama sampai akhir fase terakhir): Senior/Pentester/DevOps Rp11.550.000, Intermediate/UI/UX/QA/BA Rp9.550.000 per orang/bulan, **dengan** Engineering Kick-off.
- **Short Term** (< 2 bulan): Rp16.170.000 / Rp13.370.000 (sudah termasuk Project Enablement Fee), **tanpa** Kick-off; label "(short term)". build.py menentukan skema otomatis.
- **Engineering Kick-off proporsional**: sekali per posisi Long Term × **alokasi tertinggi** di seluruh fase; ditagih sebagai **Down Payment** saat tanda tangan.
- **Pajak** — harga selalu nett; kalimat baku di Pembayaran (sudah di build.py): *"Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien."* Berlaku juga untuk BUMN/BUMD dan brief yang meminta "harga termasuk pajak". **Jangan** tulis "PPN tidak ditagihkan" dan **jangan** ada baris PPN. ⚠️ Bila Venturo sudah PKP, tinjau ulang.
- **Diskon**: hanya bila pemilik menyebutnya (`diskon` di data; dipotong dari Down Payment). Tanpa diskon, tabel langsung ditutup **Total Investasi** (tanpa baris TOTAL).
- **Perjalanan dinas** (klien di luar Malang) dianggarkan sebagai grup baris di Rincian Biaya: tiket PP Rp3.500.000 × orang × kali; penginapan Rp3.000.000 × **kamar** (orang ÷ 2, dibulatkan ke atas) × malam; **uang saku bulanan** Rp3.000.000 × orang × bulan kunjungan (bukan per kunjungan). Ditagih rata di termin bulan kunjungan (umumnya Go-Live dan bulan pertama Hypercare). Batasan otomatis memuat "Perjalanan dinas di luar yang telah dianggarkan".
- **Server**: bila brief mewajibkan **on-premise**, `venturo_cloud` = null → Venturo Cloud dan kotak pilihan server hilang, Batasan memuat server Testing/UAT & Production (OS, lisensi, domain, SSL) disediakan Klien; Development & staging memakai ekosistem Venturo. Selain itu tawarkan Venturo Cloud (`references/venturo-cloud.md`).

## 4. Fase & fitur
Pola fase standar: 1 Requirement Analysis & System Design · 2 Fondasi Data & Platform · 3 Fitur Utama/Dashboard · 4 SIT & Performance Test · 5 UAT & Penetration Test · 6 Go-Live & Pelatihan · 7 **Hypercare 3 bulan** · 8 **Annual Support 12 bulan** (`"annual_support": true` → termin "Maintenance 1…12"). Hypercare dan Annual Support adalah fase dengan alokasi pecahan.
- Fase pertama mulai tanggal 1; fase berikutnya boleh mulai tanggal 16 (satuan ½ bulan). Fase harus berurutan tanpa celah (dicek build.py).
- **Lingkup per fase** (Penawaran) berbahasa mudah dibaca, dikelompokkan per modul dengan pola "Modul: rincian" (dicetak tebal otomatis).
- **Fitur per fase** (Lampiran): Kode | Fitur | Ringkasan. Pakai kode dari brief (F-xx, NF-xx); pekerjaan tanpa kode diberi LP-n.
- Teks baku aktivitas uji:
  - **SIT**: end-to-end test scenario, kecocokan angka dengan data sumber, negative & regression test, compatibility test.
  - **Performance Test**: K6, baseline → stress → endurance, P95/P99, analisis bottleneck, tuning.
  - **UAT**: defect log, Quality Release Checklist, sign-off formal.
  - **Penetration Test**: scope & RoE, recon, OWASP Top 10/CVE/dependency scan, manual pentest, laporan severity, perbaikan temuan Critical/High sebelum go-live, retest.
- Asumsi: urutan fitur boleh disesuaikan prioritas Klien selama total alokasi tim pada fase itu tetap.

## 5. Struktur dokumen (dibangun build.py)
**Penawaran:** Hero → 1 Lingkup Pekerjaan & Timeline (tabel per fase: lingkup | periode, durasi, orang) → 2 Rincian Biaya (satu tabel Posisi | Tarif/Bulan | Orang | Bulan | Total; grup Engineering Kick-off → Fase 1…n → Perjalanan Dinas → **Total Investasi**; tiap grup `<tbody style="break-inside:avoid">`; lalu kotak **Satuan** dan **"Sudah termasuk dalam biaya"** (Kick-off, tim sesuai alokasi + Technical Lead/Engineering Management, **jaminan target** — selaras SA Pasal 14, penggantian anggota & WhatsApp, kepemilikan source code/data/dokumentasi, gaji/BPJS/PPh 21/AI/Workspace)) → [Layanan Berlangganan Bulanan bila Venturo Cloud] → 3 Pembayaran (kalimat pajak baku, Kick-off sebagai Down Payment, tagihan akhir bulan sesuai alokasi + H+14, tabel termin per bulan kalender "Termin n – Fase x & y (+ perjalanan dinas)" / "Maintenance n", **Total Pembayaran**) → 4 Batasan (spesifik brief + server + perjalanan + **lembur atas permintaan percepatan dari Klien** berbayar + perubahan scope/timeline) → 5 Persetujuan.
Tidak ada lagi: bagian Komposisi Tim terpisah, Lingkup Layanan terpisah, tabel Ringkasan Investasi, matriks alokasi di Penawaran, kalimat "Total sebelum PPN". Rincian Biaya mengalir setelah Lingkup tanpa page break paksa; tabel fase panjang tidak dibungkus `.keep`.

**Lampiran "Rincian Biaya & Rencana Kerja"** (file tetap `…-Lampiran-Rincian-Biaya.pdf`): 1 Komponen Biaya per Orang — selalu LENGKAP sesuai pricelist, apa pun posisi yang dipakai: tabel Long Term (Kick-off + 5 komponen bulanan) dan tabel Short Term (5 komponen + Project Enablement Fee), masing-masing 4 kolom Software Engineering (Senior | Intermediate) dan Product Engineering (Pentester / DevOps | UI/UX / QA / BA); catatan "< 2 bulan = Short Term" dan kotak "Tidak perlu Anda kelola" (gaji & THR, tunjangan, BPJS, PPh 21 & PKWT, employee engagement, pengembangan talenta) → 2 Komposisi Tim & Peran (Posisi | Level & Skema | Alokasi Maks. | Peran) → 3 Alokasi Tim per Fase (matriks Posisi × F1…Fn, "–" bila tidak terlibat, baris Durasi dan Total Tim) → 4 Rencana Kerja & Fitur per Fase (halaman baru) → 5 Sudah Ditangani Venturo → 6 Asumsi & Catatan (komposisi dapat disesuaikan, Kick-off proporsional, daftar posisi Short Term + durasi, fleksibilitas urutan fitur).

**Service Agreement**: Pasal 3 "berdasarkan posisi, alokasi waktu (penuh waktu, ½ orang, atau ¼ orang), dan fase pengerjaan" + rujukan ke "Lampiran Rincian Biaya & Rencana Kerja"; Pasal 14 keterlambatan karena Venturo → perbaikan/tambah sumber daya tanpa biaya, karena Klien → target baru dan biaya bulanan tetap berjalan (dasar "Jaminan target"); Pasal 8 & 17 menyesuaikan Venturo Cloud/on-premise. Isi SA adalah dokumen hukum — perubahan pasal lain dikonfirmasi ke pengguna.

## 6. Langkah kerja
1. Baca brief → susun `data.json` (salin `assets/contoh-data.json`): klien, posisi + peran, fase + lingkup + fitur + alokasi, perjalanan dinas, batasan, server, `cek_tidak_boleh_ada` (nama klien contoh, "Pimpinan", dll.).
2. `python3 <folder skill ini>/scripts/build.py data.json <output>/src` — perbaiki data bila ada assert yang gagal.
3. Render (nomor dokumen `VEN/<Project>/<Tahun>/<Rev>`, nama file tanpa spasi):
```bash
python3 <folder skill ini>/scripts/render.py <output>/src/penawaran.html "<output>/VEN-<Project>-<Tahun>-<Rev>.pdf" "VEN/<Project>/<Tahun>/<Rev>"
python3 <folder skill ini>/scripts/render.py <output>/src/lampiran.html  "<output>/VEN-<Project>-<Tahun>-<Rev>-Lampiran-Rincian-Biaya.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Lampiran Rincian Biaya & Rencana Kerja"
python3 <folder skill ini>/scripts/render.py <output>/src/sla.html       "<output>/VEN-<Project>-<Tahun>-<Rev>-Service-Agreement.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Service Agreement"
```
4. Verifikasi: `mkdir -p <output>/preview && pdftoppm -r 60 -png <pdf> <output>/preview/<nama>` — tanpa halaman sisa kecil, logo utuh, TTD/paraf tampil, nomor dokumen konsisten. Satu set = satu revisi; perubahan → build + render ulang ketiganya, naikkan revisi, hapus versi lama.
5. Kirim 3 PDF (SendUserFile). Laporan: tabel fase (periode, orang, biaya), Kick-off, tim, perjalanan dinas, **Total Investasi**, posisi Short Term, dan hal yang perlu dicek pemilik.
6. Unggah & pesan WhatsApp: skill `proposal-upload`.

## 7. Brief berupa RFI / tender
**Deteksi:** RFI, *Request for Information*, market sounding, tender, e-proc, HPS. RFI biasanya meminta **dokumen respons dengan struktur sendiri**; tiga PDF Dedicated adalah **lampirannya**, bukan respons utama. Butir yang umum diminta:

| Butir | Isi | Sumber |
|---|---|---|
| Surat pengantar | Ditandatangani pimpinan | Skill |
| A. Profil perusahaan | Tahun berdiri, NIB + KBLI, jumlah karyawan & komposisi teknis, struktur organisasi, kemitraan | **Tanyakan pemilik** |
| B. Pengalaman | Proyek sejenis, skala data | **Tanyakan pemilik** |
| C. Solusi | Pendekatan (custom build), arsitektur, tech stack, lisensi pihak ketiga, rule engine, analitik, peta | Skill |
| D. Matriks Kesesuaian | Tiap kode kebutuhan diberi S/K/P/T + keterangan; fitur berisiko | Skill (dari kode F/NF) |
| E. Data & integrasi | Metode penarikan data, validasi, initial load, rekonsiliasi, asumsi kesiapan data | Skill |
| F. Infrastruktur | Spesifikasi server Dev/UAT/Prod, software, topologi, kapasitas | Skill |
| G. Metodologi, jadwal, tim | Tata kelola, timeline, **kualifikasi minimum per peran** | Skill + 3 PDF |
| H. Kepemilikan | Source code dan HKI | Skill |
| I. Biaya | Per komponen, lisensi/hardware terpisah, **Annual Support tahun ke-2 dst.**, **tarif man-day per peran** | 3 PDF + **tarif man-day dari pemilik** |

- **Laporan akhir wajib menyebut**: format nama berkas yang diminta (mis. `RFI-C360_[Nama Perusahaan]`), struktur respons, batas waktu, alamat email **persis seperti tertulis di dokumen RFI** (jangan dicampur dengan alamat di halaman e-proc tanpa menyebut sumbernya), dan lampiran yang dirujuk RFI tetapi tidak ada (mis. "Lampiran 2").
- **Tawarkan** pembuatan dokumen utama respons RFI mengikuti urutan butir RFI, dengan tiga PDF Dedicated sebagai lampiran.
- **Tarif man-day per peran** belum ada di pricelist — harus diputuskan pemilik; jangan dihitung sendiri.

## Yang tidak boleh dilakukan
- Memakai jabatan yang tidak ada di Venturo, atau harga di luar `references/pricelist-dedicated.md`.
- Menambahkan PPN, atau menulis "PPN tidak ditagihkan".
- Menampilkan baris DISKON tanpa instruksi pemilik.
- Membuat tabel Ringkasan Investasi atau bagian Lingkup Layanan/Komposisi Tim terpisah di Penawaran.
- Memasukkan QA atau DevOps di fase Requirement Analysis.
- Menghitung uang saku per kunjungan, atau penginapan per orang.
- Menaikkan alokasi Long Term untuk orang yang hanya dibutuhkan < 2 bulan (pakai posisi "(tambahan)" Short Term).
- Mengisi jabatan penanda tangan klien yang tidak diketahui (mis. "Pimpinan").
- Menjalankan skrip dengan `python3 -I`, atau menulis angka SLA / masa berlaku penawaran / kotak meterai di dokumen.
