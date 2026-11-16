# Pricelist Onsite Engineer Venturo 2026

Sumber: deck "VENTURO - Onsite Engineer" (slide 8–14). Harga nett.

## Model
Programmer bekerja **di kantor Klien** (onsite), tetapi hubungan kerjanya hanya dengan Venturo. Venturo merekrut, menggaji, memantau, melatih, dan mengganti talent; Klien memberi arahan kerja harian.

**Tarif per talent / bulan = (Biaya Talent + Biaya Penempatan) × (1 + Management Fee).**

| Komponen | Isi |
|---|---|
| Biaya Talent | Gaji pokok · BPJS Ketenagakerjaan & Kesehatan · Provisi THR · Provisi kompensasi PKWT |
| Biaya Penempatan | AI Engineering Platform Rp500.000 · Laptop kerja Rp500.000 · Training & sertifikasi Rp150.000 |
| Management Fee | Kontrak 3–5 bulan **15%** · 6–11 bulan **12,5%** · ≥ 12 bulan **10%** (minimal kontrak 3 bulan) |
| Engineering Kick-off | **1× tarif bulanan per talent**, sekali bayar sebagai Down Payment — rekrutmen & seleksi, onboarding, setup kerja, garansi penggantian talent |

Management fee sudah mencakup: monitoring harian, talent cadangan, laporan bulanan, Account Manager, payroll & pajak.

## Preset kota & level (simulasi harga slide 9)
| Kode preset | Kota · Level | Gaji pokok (rekomendasi) | BPJS | THR | Kompensasi PKWT | Biaya dasar |
|---|---|---|---|---|---|---|
| `jakarta-intermediate` | Jakarta · Intermediate | Rp6.500.000 | Rp675.000 | Rp550.000 | Rp550.000 | Rp9.425.000 ⚠️ |
| `jakarta-senior` | Jakarta · Senior | Rp10.000.000 | Rp935.000 | Rp760.000 | Rp760.000 | Rp13.605.000 ⚠️ |
| `surabaya` | Surabaya · Intermediate | Rp6.500.000 | Rp630.000 | Rp510.000 | Rp510.000 | Rp9.300.000 |
| `malang` | Malang · Intermediate | Rp4.500.000 | Rp440.000 | Rp360.000 | Rp360.000 | Rp6.810.000 |

Biaya dasar = komponen talent + biaya penempatan Rp1.150.000. Contoh tarif Malang: 3 bulan Rp7.831.500 · 6 bulan Rp7.661.250 · 12 bulan Rp7.491.000.

⚠️ **Jakarta di deck slide 9 tidak konsisten:** total biaya dasar tertulis Rp9.925.000 (Intermediate) dan Rp13.105.000 (Senior), padahal jumlah komponennya Rp9.425.000 dan Rp13.605.000. build.py selalu menjumlah komponen; bila angka di deck yang benar, perbaiki komponen di PRESET.

- Kota/level lain, atau gaji mengikuti kandidat yang dipilih Klien: **komponen gaji, BPJS, THR, dan PKWT diminta dari pemilik** lalu diisi di `komponen` — jangan menghitung sendiri.
- Harga final mengikuti kandidat yang dipilih Klien.

## Ketentuan kerja sama
- 8 jam per hari atau 40 jam per minggu, jadwal ditentukan Klien; talent mengikuti SOP dan peraturan perusahaan Klien.
- Klien menyediakan meja kerja, internet, dan akses sistem. Talent hanya mengerjakan pekerjaan pengembangan software.
- Lembur atas perintah tertulis Klien, dihitung per jam, ditagih terpisah.
- Invoice bulanan di awal bulan, dibayar maksimal 14 hari kalender. PPh 23 ditanggung Klien.
- Harga disesuaikan bila ada perubahan UMP/UMK atau regulasi ketenagakerjaan.
- Perpanjangan dikonfirmasi tertulis paling lambat 2 bulan sebelum kontrak berakhir.
- Hak, kewajiban, dan perubahan dituangkan dalam Service Agreement dan addendum.

## Penggantian talent (biaya rekrutmen & onboarding pengganti ditanggung Venturo)
Ketidakcocokan budaya kerja/komunikasi · sering absen, terlambat, izin tanpa keterangan · melanggar tata tertib, disiplin, sopan santun · memanipulasi absensi/timesheet · membocorkan data atau menyalahgunakan akses · tidak jujur atau tindak pidana. Permintaan tertulis kepada Account Manager.

## Belum termasuk (tetap bisa disediakan, ditagih biaya aktual + biaya layanan atas persetujuan tertulis Klien)
Lembur · perjalanan dinas di luar kota penempatan · lisensi software, server, atau hardware khusus · sertifikasi vendor di luar program training Venturo.

## Venturo Cloud (opsional)
Bila Klien butuh server (deck slide 10), ditagih per bulan bersama tarif talent (tabel `CLOUD` di build.py):

| Kode | Paket | Spesifikasi | Harga/bulan |
|---|---|---|---|
| `shared-mini` | Shared Hosting Mini | 1 CPU · 2 GB RAM · 5 GB | Rp200.000 |
| `shared-small` | Shared Hosting Small | 2 CPU · 3 GB RAM · 5 GB | Rp350.000 |
| `shared-medium` | Shared Hosting Medium | 2 CPU · 4 GB RAM · 5 GB | Rp600.000 |
| `vps-mini` | VPS Cloud Server Mini | 2 vCPU · 4 GB RAM · 32 GB | Rp800.000 |
| `vps-small` | VPS Cloud Server Small | 4 vCPU · 4 GB RAM · 32 GB | Rp900.000 |
| `vps-medium` | VPS Cloud Server Medium | 4 vCPU · 8 GB RAM · 32 GB | Rp1.050.000 |
| `vps-large` | VPS Cloud Server Large | 6 vCPU · 8 GB RAM · 32 GB | Rp1.150.000 |

Dukungan tim DevOps (monitoring, konfigurasi, optimasi, patching) hanya untuk paket VPS.
