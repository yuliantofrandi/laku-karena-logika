---
name: proposal-dedicated
description: Membuat TIGA PDF penawaran Venturo model DEDICATED TEAM (man power based) langsung jadi dari System Requirement Brief klien (txt/pdf/docx) — (1) Penawaran Layanan Dedicated Team + form persetujuan dengan tanda tangan+stempel dan paraf CEO, (2) Lampiran Rincian Biaya per Posisi, dan (3) Service Agreement Dedicated Team — dengan rekomendasi komposisi tim (posisi, level, jumlah orang, durasi) dari brief, Engineering Kick-off per orang, biaya bulanan per orang, termin, dan Venturo Cloud. Pakai saat diminta "penawaran dedicated team", "proposal dedicated", "penawaran man power", "hire programmer/tim dari Venturo", "outsourcing tim", atau "buat penawaran dedicated dari brief". Untuk model Managed Service berbasis Poin, pakai proposal-pdf.
---

# Penawaran Dedicated Team dari Brief → 3 PDF

Turunan skill `proposal-pdf` untuk model **Dedicated Team (man power based)**: klien membayar **per orang per bulan** sesuai posisi dan level, bukan per Poin. Dari satu **System Requirement Brief**, skill ini menghasilkan tiga PDF dengan **satu nomor dokumen dan satu nomor revisi**:
1. **Penawaran Layanan Dedicated Team**: penawaran sekaligus form persetujuan.
2. **Lampiran Rincian Biaya per Posisi**: komponen biaya per orang (seperti slide pricelist) dan komposisi tim beserta perannya.
3. **Service Agreement Dedicated Team**: perjanjian induk 23 pasal, diadaptasi dari Service Agreement Managed Service.

Konvensi umum (tanda tangan, paraf, desain, istilah, penamaan, verifikasi) mengikuti `proposal-pdf`; yang berbeda dijelaskan di bawah.

## 0. Cek alat
```bash
python3 -c "import playwright; print('playwright ok')"; command -v pdftoppm
```
Bila belum ada, sebutkan yang kurang dan minta izin pengguna sebelum memasang (`python3 -m pip install playwright`, `python3 -m playwright install chromium`, `brew install poppler`). Folder hasil: folder yang disebut pengguna, atau `penawaran/` di working directory (ditulis `<output>`).

## Aset yang dibundel (`<folder skill ini>/`)
- `assets/logo.png`, `assets/bg_flat.jpg`, `assets/ttd.png`, `assets/paraf.png`, `assets/fonts/*.woff2` — sama dengan `proposal-pdf`.
- `assets/contoh-penawaran-dedicated.html` — template Penawaran Dedicated Team (contoh: UNS, 6 orang, 4 bulan).
- `assets/contoh-lampiran-rincian-biaya.html` — template Lampiran Rincian Biaya per Posisi.
- `assets/contoh-service-agreement-dedicated.html` — template Service Agreement Dedicated Team.
- `references/pricelist-dedicated.md` — **pricelist man power** (Kick-off, komponen bulanan per level, "You Don't Need to Manage"). Satu-satunya sumber harga.
- `references/venturo-cloud.md` — rate card Venturo Cloud.
- `scripts/render.py` — `python3 -I <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]` (default prefix "Penawaran Layanan Dedicated Team").

## 1. Alur
1. **Input:** System Requirement Brief (txt/pdf/docx). Data klien (nama, jabatan, instansi, alamat) yang tidak ada di brief ditanyakan **sekali di awal**; jangan tanyakan hal lain.
2. **Rekomendasikan komposisi tim** dari brief (§2).
3. **Hitung biaya** dari pricelist (§3).
4. **Susun 3 HTML** dari template (§4–§6), render (§7), verifikasi, kirim 3 file dengan SendUserFile.
5. **Laporan singkat**: komposisi tim + alasannya, durasi, total Kick-off, biaya per bulan, Total Investasi, dan hal yang perlu dicek pengguna.

## 2. Rekomendasi komposisi tim (dari brief)
- Pecah brief per modul/kanal seperti di `proposal-pdf`, lalu petakan ke **posisi**:
  - **Software Engineering – Senior**: arsitektur, backend inti, integrasi kompleks (SSO, payment, API pihak ketiga), pemimpin teknis tiap platform.
  - **Software Engineering – Intermediate**: implementasi fitur web/mobile di bawah arahan Senior.
  - **Product Engineering – Pentester / DevOps** (tarif setara Senior): infrastruktur, CI/CD, keamanan, uji penetrasi — hanya bila brief menuntut.
  - **Product Engineering – UI/UX / QA / BA** (tarif setara Intermediate): desain antarmuka, pengujian, analisis kebutuhan.
- Beri nama posisi yang jelas fungsinya (mis. "Senior Software Engineer – Mobile", "QA Engineer") dan satu kalimat peran.
- **Durasi**: perkirakan dari besar pekerjaan (kalibrasi internal `proposal-pdf`: 1 Poin ≈ 1 jam kerja senior; jangan tampilkan jam ke klien), dengan seluruh tim pada periode yang sama kecuali brief jelas membutuhkan posisi tertentu lebih singkat (mis. UI/UX hanya di awal).
- Pilih komposisi terbaik yang realistis untuk menyelesaikan scope tepat waktu; jangan sengaja menggelembungkan jumlah orang.

## 3. Biaya
- Harga per orang dari `references/pricelist-dedicated.md`:
  | Level | Engineering Kick-off (sekali) | Biaya bulanan/orang |
  |---|---:|---:|
  | Senior / Pentester / DevOps | Rp11.550.000 | Rp11.550.000 |
  | Intermediate / UI/UX / QA / BA | Rp9.550.000 | Rp9.550.000 |
- **Engineering Kick-off ditagih sekali untuk setiap orang** yang di-hire, saat tanda tangan; berlaku juga untuk anggota baru di tengah periode.
- Biaya bulanan = tarif × jumlah orang; Total Investasi = total Kick-off + (biaya bulanan × jumlah bulan) — bila durasi per posisi berbeda, hitung per posisi.
- Tanpa minimal kontrak.
- **Tanggal mulai** (sama dengan `proposal-pdf`): periode Dedicated Team mulai **tanggal 1 bulan kalender berikutnya** setelah tanda tangan; hari di antaranya dipakai untuk Engineering Kick-off; periode tidak pernah dimulai di tengah bulan; bila tanda tangan bergeser ke bulan berikutnya, geser periode dan naikkan nomor revisi. Invoice bulanan di akhir tiap bulan periode.
- **Venturo Cloud** tetap ditawarkan di tabel **Layanan Berlangganan Bulanan** (di luar Total Investasi) dengan aturan `references/venturo-cloud.md` (mulai 1 bulan sebelum go-live; DevOps hanya untuk VPS). Tidak ada baris Layanan Lanjutan 50 Poin — perpanjangan Dedicated Team dibuat lewat penawaran/addendum baru.

## 4. Dokumen 1 — Penawaran Layanan Dedicated Team (`contoh-penawaran-dedicated.html`)
- **Hero**: "Dedicated Team" + nama project; kartu No./Project/Tanggal; kartu Kepada Yth.; pembuka "kurang lebih 100 orang" + penyediaan tim penuh waktu.
- **1. Komposisi Tim**: Posisi (+ peran singkat) | Level | Orang → Total Tim; catatan periode kerja.
- **2. Lingkup Layanan**: kartu *Engineering Kick-off* (sekali bayar per orang: onboarding, kickoff & roadmap, Setup Core Venturo, akses & environment, dokumentasi) dan kartu *Dedicated Team* (penuh waktu sesuai backlog Klien, Technical Lead & Engineering Management, AI Subscription & workspace, "Klien tidak perlu mengelola …", penggantian talent, dukungan WhatsApp, rujukan ke Lampiran). **Tanpa angka SLA.**
- **3. Rincian Biaya**: tabel Engineering Kick-off (Posisi | Orang | Per Orang | Subtotal) → tabel Biaya Bulanan (Posisi | Orang | Per Orang/Bulan | Subtotal/Bulan) → total per bulan, total N bulan, **Total Investasi**; lalu **Layanan Berlangganan Bulanan** (Venturo Cloud).
- **4. Pembayaran**: nett, PPh 23 ditanggung Klien, PPN tidak ditagihkan; Kick-off saat tanda tangan; bulanan di akhir bulan, H+14; layanan dihentikan sementara bila telat; Venturo Cloud bila dipilih; rekening BCA + tabel termin → **Total Pembayaran**.
- **5. Batasan dan Pengecualian**: server production di luar Venturo Cloud + domain, biaya pihak ketiga dari brief, out-of-pocket, **lembur** (diajukan dan disetujui Klien sebelum dikerjakan), penambahan anggota/perpanjangan lewat penawaran atau addendum baru.
- **6. Persetujuan**: kalimat persetujuan, kotak pilihan ☐ *Venturo Cloud [Paket] Rp[harga]/bulan mulai [tanggal]* ☐ *Server disediakan Klien*, blok tanda tangan.

## 5. Dokumen 2 — Lampiran Rincian Biaya per Posisi (`contoh-lampiran-rincian-biaya.html`)
- Hero "Lampiran Penawaran Layanan" / "Rincian Biaya per Posisi" + nama project; kartu Lampiran (No. penawaran), Project, Tanggal; kartu Kepada Yth.
- **1. Komponen Biaya per Orang**: kolom hanya untuk level yang dipakai; baris Engineering Kick-off, lalu Development Squad, Technical Lead, AI Subscription & RND, Engineering Workspace, Engineering Management → **Biaya Bulanan per Orang**.
- **2. Komposisi Tim & Peran**: Posisi | Level | Orang | Peran → Total Tim.
- **3. Sudah Ditangani Venturo**: daftar "You Don't Need to Manage".
- **4. Asumsi & Catatan**: komposisi dari brief dan dapat disesuaikan, perubahan anggota lewat addendum, Kick-off untuk setiap anggota baru.
- Footer paraf; tanpa blok tanda tangan penuh.

## 6. Dokumen 3 — Service Agreement Dedicated Team (`contoh-service-agreement-dedicated.html`)
Diadaptasi dari 23 pasal Service Agreement Managed Service (`proposal-pdf`), dengan perubahan:
- Hero "Venturo Dedicated Team".
- **3. Lingkup Pengerjaan**: penyediaan tim penuh waktu berdasarkan posisi dan jumlah orang; rujuk Penawaran + Lampiran Rincian Biaya.
- **4. Support Service**: jam kerja, respons WhatsApp maks. 15 menit pada jam kerja, tim mengikuti prioritas backlog Klien, Major Bug diprioritaskan di atas pekerjaan lain (tanpa target 2 jam dan tanpa Poin).
- **9. Laporan Pekerjaan**: rekap bulanan berisi kehadiran dan pekerjaan setiap anggota tim.
- **11. Pekerjaan di Luar Jam Kerja**: lembur dengan persetujuan tertulis dan biaya yang diajukan sebelum dikerjakan.
- **14. Keterlambatan**: karena Venturo → perbaikan kinerja/tambah dukungan tanpa biaya; karena Klien → target baru, biaya bulanan tetap berjalan.
- **15. Pemenuhan dan Penggantian Talent**: tim sesuai Penawaran; hubungan kerja, gaji, THR, BPJS, PPh 21, PKWT tanggung jawab Venturo; penggantian 7–14 hari tanpa biaya; cuti/sakit ditutup Technical Lead/pengganti; perubahan anggota lewat addendum.
- **17. Terminasi**: 30 hari (performa) / 60 hari (bisnis) / Venturo Cloud 30 hari; pembayaran termasuk Kick-off tidak dapat dikembalikan.
- **19. Garansi**: bug selama periode ditangani tim tanpa biaya; 30 hari setelah periode berakhir.
- Pasal lain (Para Pihak, Komunikasi, Project Management, Scrum, Deployment Environment + Venturo Cloud, Out of Pocket, Kerahasiaan, HKI, Perekrutan, BAST, Pembatasan Tanggung Jawab, Force Majeure, Perselisihan, Persetujuan) sama dengan versi Managed Service.
- Pastikan tidak ada sisa "Poin", "Delivery Point", "Managed Service", atau "Layanan Lanjutan".

> Isi Service Agreement adalah dokumen hukum: perubahan pasal di luar daftar ini dikonfirmasi ke pengguna.

## 7. Penamaan, render & verifikasi
- Nomor dokumen `VEN/<Project>/<Tahun>/<Rev>` (aturan sama dengan `proposal-pdf`). Nama file tanpa spasi:
  `VEN-<Project>-<Tahun>-<Rev>.pdf` · `…-Lampiran-Rincian-Biaya.pdf` · `…-Service-Agreement.pdf`. `<title>` HTML = nama file.
- Render (salin `assets/*` ke folder kerja lebih dulu):
```bash
python3 -I <folder skill ini>/scripts/render.py penawaran.html "<output>/VEN-<Project>-<Tahun>-<Rev>.pdf" "VEN/<Project>/<Tahun>/<Rev>"
python3 -I <folder skill ini>/scripts/render.py lampiran.html  "<output>/VEN-<Project>-<Tahun>-<Rev>-Lampiran-Rincian-Biaya.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Lampiran Rincian Biaya"
python3 -I <folder skill ini>/scripts/render.py sla.html       "<output>/VEN-<Project>-<Tahun>-<Rev>-Service-Agreement.pdf" "VEN/<Project>/<Tahun>/<Rev>" "Service Agreement"
```
- Satu set = satu nomor revisi; setiap perubahan → render ulang ketiganya, naikkan revisi, hapus versi lama.
- Verifikasi (`pdftoppm -r 60`): tanpa halaman sisa kecil, logo utuh, TTD/paraf tampil, nomor dokumen konsisten, total Kick-off + bulanan = Total Investasi = Total Pembayaran, tanpa sisa istilah Managed Service.
- Unggah ke proposal.venturo.id dan pesan WhatsApp: skill `proposal-upload` (mengenali set `…-Lampiran-Rincian-Biaya.pdf`).

## Yang tidak boleh dilakukan
- Memakai harga di luar `references/pricelist-dedicated.md`, atau menggabungkan model Poin (Managed Service) ke penawaran Dedicated.
- Lupa menagih Engineering Kick-off per orang, atau memulai periode di tengah bulan.
- Menulis angka SLA di penawaran (angka hanya di Service Agreement).
- Menulis masa berlaku penawaran di dokumen, atau kotak meterai.
