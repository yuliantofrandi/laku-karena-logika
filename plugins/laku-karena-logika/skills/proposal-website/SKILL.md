---
name: proposal-website
description: Membuat DUA PDF penawaran Venturo untuk PAKET WEBSITE (Landing Page, Company Profile, Company Profile Pro, Toko Katalog, Toko Online Pro) dari brief atau kebutuhan klien — (1) Penawaran Layanan Paket Website + form persetujuan dengan tanda tangan+stempel dan paraf CEO, berisi Lingkup Layanan (pembuatan website, fitur admin dashboard CMS & kepemilikan, hosting/domain/support), Rincian Biaya (pembuatan website + hosting, domain & CMS tahun ke-1), Pembayaran dengan termin 50% DP + 50% sebelum go-live, Batasan dan Pengecualian, dan Persetujuan, dan (2) Service Agreement Paket Website (kepemilikan CMS/domain/konten, perpanjangan, storage 5 GB, hosting sendiri) — dibangun lewat generator scripts/build.py dari satu file data. Pakai saat diminta "penawaran website", "proposal website", "paket website", "buat website company profile/landing page/toko online untuk klien X", "penawaran company profile", atau "penawaran toko online". Kebutuhan custom (booking, membership, marketplace, integrasi ERP, jual putus) pakai proposal-managed atau proposal-dedicated.
---

# Penawaran Paket Website dari Brief → 2 PDF

Paket website dijual dengan **satu harga di awal** (desain + CMS + hosting tahun pertama) lalu **perpanjangan tahunan** mulai tahun ke-2. CMS adalah layanan berlangganan milik Venturo; domain atas nama klien; konten milik klien dan bisa diekspor. Harga, isi paket, dan aturan negosiasi: `references/paket-website.md`.

Dua PDF, satu nomor dokumen dan satu nomor revisi:
1. **Penawaran Layanan Paket Website** — penawaran sekaligus form persetujuan.
2. **Service Agreement Paket Website** — perjanjian ringkas 15 pasal.

## 0. Alat
- Cek: `python3 -c "import playwright"` dan `command -v pdftoppm`. Bila kurang, minta izin sebelum memasang (`python3 -m pip install playwright`, `python3 -m playwright install chromium`, `brew install poppler`).
- **Jangan jalankan skrip dengan `python3 -I`** (Playwright di user site-packages jadi tidak terbaca). Jalankan `python3 <skrip> …` biasa.
- Jalankan `mkdir -p <folder preview>` sebelum `pdftoppm`.
- Folder hasil: folder yang disebut pengguna, atau `penawaran/` di working directory (`<output>`); folder kerja HTML `<output>/src`.

## Aset & skrip (`<folder skill ini>/`)
- `scripts/build.py` — **generator**: `python3 <folder skill ini>/scripts/build.py <data.json> <output>/src` membangun `penawaran.html` dan `sla.html` (+ salin logo, bg, TTD, paraf, font). Mengambil harga, perpanjangan, waktu kerja, isi paket, dan fitur CMS (tabel `CMS`) dari tabel PAKET; memecah harga paket menjadi Pembuatan Website + Hosting, Domain & CMS Tahun ke-1; menghitung termin; meng-`assert` Σ termin = Total, diskon ≤ 10% dengan imbalan, kode project huruf & angka saja, dan tidak ada istilah terlarang ("biaya tahunan", "sewa", "PPN tidak ditagihkan") atau sisa teks di `cek_tidak_boleh_ada`. **Revisi = ubah data → build → render ulang.**
- `scripts/render.py` — `python3 <folder skill ini>/scripts/render.py <html> <out.pdf> "<No. dokumen>" ["<prefix footer>"]`.
- `assets/contoh-data.json` — format data. Salin lalu ganti isinya.
- `assets/website.css`, `assets/sa-website.html` — gaya dan template Service Agreement (dipakai build.py).
- `assets/contoh-*.html` — hasil build dari contoh data, untuk acuan visual.
- `references/paket-website.md` — daftar harga, isi paket, standar, perpanjangan, kebijakan negosiasi.

## 1. Input & data klien
- Input: brief, chat, catatan meeting, atau dokumen kebutuhan klien. Data klien yang tidak ada (instansi, penerima, alamat, penanda tangan) ditanyakan **sekali** di awal — termasuk **alamat** klien, karena tampil di hero dan Pasal 1 Service Agreement.
- Data klien yang tetap tidak diketahui tampil sebagai garis isian `______________________` (otomatis). **Jangan isi jabatan "Pimpinan".**
- **Nomor dokumen** `VEN/<Kode>/<Tahun>/<Rev>`: kode project **huruf dan angka saja**, tanpa spasi dan tanda hubung (dicek build.py). `file` = `VEN-<Kode>-<Tahun>-<Rev>`.
- **Revisi**: revisi yang belum diunggah/dikirim ke klien boleh diperbaiki tanpa menaikkan nomor; naikkan nomor bila isi/harga berubah setelah dikirim atau perubahan diminta di sesi baru.

## 2. Memilih paket
Pilih **satu** paket yang paling sesuai kebutuhan dan isi `paket` dengan kode data. Alasan pemilihan paket **tidak** ditampilkan di dokumen — sampaikan di laporan ke pemilik saja (kutip kebutuhan klien: jumlah halaman, rutin update artikel, cara order, pembayaran online).
- **Keluarga Company Profile** (Landing Page · Company Profile · Company Profile Pro) — bisnis yang ingin tampil kredibel dan mudah dihubungi.
  - 1 halaman untuk promosi/kampanye → Landing Page.
  - ≤ 7 halaman, jarang update → Company Profile.
  - > 7 halaman (maks 15) **atau** rutin menerbitkan berita/artikel → Company Profile Pro.
- **Keluarga Toko Online** (Toko Katalog · Toko Online Pro) — bisnis yang menjual produk.
  - Order cukup lewat WhatsApp → Toko Katalog.
  - Perlu keranjang, checkout, payment gateway, ongkir otomatis, laporan penjualan → Toko Online Pro.
- **Custom** (booking, membership, marketplace, integrasi ERP/sistem internal, jual putus atau hosting sendiri penuh) **bukan** skill ini → arahkan ke `proposal-managed` atau `proposal-dedicated`.
- Kebutuhan sedikit di atas paket (mis. 9 halaman) → paket di atasnya; jangan menambah add-on berbayar tanpa harga dari pemilik.

## 3. Harga, pembayaran, dan negosiasi
- Harga **hanya** dari `references/paket-website.md`. Di Rincian Biaya, harga paket dipecah menjadi **Pembuatan Website** (harga paket − perpanjangan, periode = waktu kerja) dan **Hosting, Domain & CMS — Tahun ke-1** (= nilai perpanjangan, periode "1 tahun sejak go-live"). **Total Investasi tetap = harga paket.**
- Selalu pakai istilah **"Perpanjangan"**, bukan "biaya tahunan" atau "sewa".
- **Pajak**: kalimat baku (sudah di build.py) — *"Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien."* Jangan ada baris PPN.
- **Pembayaran**: 50% Down Payment saat tanda tangan, 50% pelunasan setelah uji coba disetujui Klien, sebelum go-live. Poin pembayaran: pajak (kalimat baku) · tagihan dibayar paling lambat H+14 dari tanggal invoice · waktu pengerjaan dihitung sejak DP diterima dan materi konten lengkap; go-live setelah pelunasan diterima · keterlambatan bayar → layanan berhak dihentikan sementara · perpanjangan ditagih 30 hari sebelum jatuh tempo mulai tahun ke-2. `bayar_lunas: true` → satu termin lunas saat tanda tangan.
- **Negosiasi** (hanya bila pemilik memintanya):
  - Jangan turunkan harga paket — tukar dengan `nilai_tambah` (halaman tambahan, 3 artikel SEO pertama, setup Google Business/Search Console, revisi tambahan), tampil sebagai kotak **Nilai Tambah** (Tanpa biaya tambahan) di Lingkup Layanan.
  - Budget kurang → paket di bawahnya + add-on.
  - `diskon = {nama, nilai, imbalan}` **hanya atas instruksi CEO**, maksimal 10%, wajib dengan imbalan (bayar lunas di depan, kontrak perpanjangan 2 tahun di muka, izin portfolio/testimoni, referensi klien). Nama baris diskon menyebut imbalannya.
  - Lebih disarankan `diskon_perpanjangan = {persen, imbalan}` (mis. tahun ke-2 diskon 20%).
  - `addon = [{nama, keterangan, harga, waktu}]` (`waktu` opsional, default "–") hanya dengan harga dari pemilik.
- `punya_domain_hosting: true` → kalimat "Sudah punya domain & hosting?" muncul di kotak Hosting, Domain & Support; penyesuaian biaya **dibahas terpisah** (belum ada tarif baku).

## 4. Struktur dokumen (dibangun build.py)
**Penawaran:** Hero → paragraf pembuka baku (sama dengan proposal-managed) → **1 Lingkup Layanan** (kotak Pembuatan Website · kotak Admin Dashboard (CMS) berisi fitur per paket + Kepemilikan · kotak Hosting, Domain & Support · kotak Nilai Tambah bila ada) → **2 Rincian Biaya** (tabel Layanan/Periode/Harga: Pembuatan Website + Hosting, Domain & CMS Tahun ke-1 → Total Investasi; catatan perpanjangan tahun ke-2) → **3 Pembayaran** (poin pajak, H+14, waktu pengerjaan & go-live, penghentian sementara, penagihan perpanjangan → rekening → tabel Periode Kerja/Termin/Tgl Invoice/Nominal → Total Pembayaran) → **4 Batasan dan Pengecualian** (payment gateway & ongkir pihak ketiga, akomodasi meeting luar Malang, halaman/fitur di luar paket, storage di atas 5 GB, + `batasan` dari data) → **5 Persetujuan**.

**Service Agreement Paket Website** (15 pasal): Para Pihak · Ruang Lingkup · Masa Berlaku · Biaya dan Pembayaran · Waktu Pengerjaan dan Kewajiban Klien · Kepemilikan (CMS milik Venturo, domain & konten milik Klien, hosting sendiri) · Perpanjangan Tahunan (tagihan 30 hari sebelum jatuh tempo, penyesuaian harga dengan pemberitahuan 30 hari, masa tenggang 14 hari, aktivasi ulang) · Kapasitas Penyimpanan · Support, Pemeliharaan, dan Garansi · Penghentian Layanan (ekspor konten, pemindahan domain) · Kerahasiaan · Pembatasan Tanggung Jawab · Force Majeure · Penyelesaian Perselisihan · Persetujuan. Isi SA adalah dokumen hukum — perubahan pasal dikonfirmasi ke pengguna.

## 5. Langkah kerja
1. Baca kebutuhan → pilih paket (bagian 2) → susun `data.json` (salin `assets/contoh-data.json`): nomor, file, tanggal, project, klien, paket, opsi negosiasi bila diminta, `cek_tidak_boleh_ada`.
2. `python3 <folder skill ini>/scripts/build.py data.json <output>/src` — perbaiki data bila ada assert yang gagal.
3. Render:
```bash
python3 <folder skill ini>/scripts/render.py <output>/src/penawaran.html "<output>/VEN-<Kode>-<Tahun>-<Rev>.pdf" "VEN/<Kode>/<Tahun>/<Rev>"
python3 <folder skill ini>/scripts/render.py <output>/src/sla.html "<output>/VEN-<Kode>-<Tahun>-<Rev>-Service-Agreement-Website.pdf" "VEN/<Kode>/<Tahun>/<Rev>" "Service Agreement Paket Website"
```
4. Verifikasi: `mkdir -p <output>/preview && pdftoppm -r 60 -png <pdf> <output>/preview/<nama>` — kotak Lingkup Layanan tidak terpotong, tabel Rincian Biaya & termin utuh, TTD/paraf tampil, tanpa halaman sisa kecil.
5. Kirim 2 PDF (SendUserFile). Laporan: paket + alasan pemilihan paket (tidak tampil di dokumen), Total Investasi, termin, perpanjangan tahun ke-2, waktu kerja, dan hal yang perlu dicek pemilik.
6. Unggah & pesan WhatsApp: skill `proposal-upload` (mengenali set website dari akhiran `-Service-Agreement-Website`).

## Yang tidak boleh dilakukan
- Harga di luar `references/paket-website.md`, menurunkan harga paket, atau diskon tanpa instruksi CEO / di atas 10% / tanpa imbalan.
- Memecah harga paket selain menjadi Pembuatan Website + Hosting, Domain & CMS Tahun ke-1, atau membuat Total Investasi berbeda dari harga paket.
- Menulis "biaya tahunan", "sewa", "PPN tidak ditagihkan", atau menambahkan baris PPN.
- Menawarkan Custom lewat skill ini.
- Mengisi jabatan penanda tangan klien yang tidak diketahui (mis. "Pimpinan"), atau memakai tanda hubung/spasi di kode project.
- Menjalankan skrip dengan `python3 -I`, atau menulis masa berlaku penawaran / kotak meterai di dokumen.
