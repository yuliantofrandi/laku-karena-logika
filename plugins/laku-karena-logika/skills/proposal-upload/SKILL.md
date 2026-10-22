---
name: proposal-upload
description: Mengunggah 3 PDF penawaran Venturo hasil skill proposal-pdf (Penawaran Layanan, Lampiran Estimasi Delivery Point, Service Agreement) ke bucket R2 Cloudflare di proposal.venturo.id — terpisah dari website company profile — langsung tanpa konfirmasi dengan URL sesuai nama file, memverifikasi ketiga link, lalu menyusun pesan WhatsApp pengantar berisi link dan masa berlaku penawaran 14 hari. Pakai saat diminta "upload penawaran", "unggah PDF penawaran", "kirim penawaran ke klien", "buat link penawaran", "pesan WA penawaran", atau setelah proposal-pdf selesai.
---

# Upload Penawaran → proposal.venturo.id (R2) + Pesan WhatsApp

Lanjutan skill `proposal-pdf`. Tiga PDF satu set (nomor dokumen dan revisi sama) diunggah langsung dari **folder hasil `proposal-pdf`** ke bucket R2 **`proposal`** yang tersambung ke domain **`proposal.venturo.id`**, terpisah dari website company profile venturo.id. Hasilnya:

`https://proposal.venturo.id/<nama-file>.pdf` (mis. `https://proposal.venturo.id/VEN-PolicyLab-2026-016.pdf`)

- URL = **nama file apa adanya** di akar bucket, tanpa kode acak. R2 tidak menampilkan daftar isi bucket.
- Hanya **revisi terbaru** per project yang di-hosting; objek revisi lama dihapus saat revisi baru diunggah.
- Unggah dilakukan **langsung**, tanpa meminta konfirmasi (ketetapan pengguna).
- `robots.txt` (`Disallow: /`) dipasang di bucket agar mesin pencari tidak merayapi.

## 0. Persiapan
- **Folder PDF** = folder hasil `proposal-pdf` (default `penawaran/` di working directory). Harus berisi set lengkap `VEN-<Project>-<Tahun>-<Rev>.pdf`, `…-Lampiran-Estimasi.pdf`, `…-Service-Agreement.pdf`.
- **Auth Cloudflare** (pilih salah satu; cek dengan `npx wrangler@4 whoami`):
  1. **Login wrangler** di komputer ini: pengguna menjalankan sendiri `npx wrangler@4 login` (membuka browser, OAuth). Tidak perlu memberikan apa pun ke Claude.
  2. **API token** (untuk komputer/server lain atau otomatisasi): pengguna membuat token di Cloudflare dashboard → My Profile → API Tokens → Create Token → Custom token dengan izin **Account › Workers R2 Storage › Edit** untuk akun Venturo, lalu menyetelnya sendiri sebagai env `CLOUDFLARE_API_TOKEN` dan `CLOUDFLARE_ACCOUNT_ID` (Account ID ada di dashboard). Token **jangan** ditempel di chat, ditulis ke file skill, memori, atau commit.
- Catatan unggahan disimpan di `<folder PDF>/.proposal-upload.json` (project → nomor, objek, URL). Wrangler tidak bisa menampilkan isi bucket, jadi file ini yang dipakai untuk mengenali revisi lama. Jangan dihapus.

### Setup sekali (cek bila link belum bisa dibuka)
1. Bucket R2 `proposal` (sudah dibuat): `npx wrangler@4 r2 bucket list`.
2. **Hubungkan domain** `proposal.venturo.id` ke bucket: `npx wrangler@4 r2 bucket domain list proposal`. Bila belum ada, record DNS lama `proposal.venturo.id` (yang mengarah ke server lain) harus dihapus dulu, lalu tambahkan custom domain di dashboard Cloudflare (R2 → `proposal` → Settings → Custom Domains) atau `npx wrangler@4 r2 bucket domain add proposal --domain proposal.venturo.id --zone-id <zone id venturo.id>`. Ini **mengubah DNS: minta izin pengguna** dan lebih baik dilakukan pengguna sendiri di dashboard.
3. **Disarankan:** Transform Rule di zona venturo.id (Rules → Transform Rules → Modify Response Header) untuk hostname `proposal.venturo.id`: set `X-Robots-Tag: noindex, nofollow`. Tanpa ini `cek` memberi PERINGATAN (bukan gagal).

## 1. Unggah
```bash
python3 <folder skill ini>/scripts/upload.py unggah --pdf <folder PDF>
```
Skrip memilih set lengkap dengan revisi tertinggi (set yang tidak lengkap dilewati dengan PERINGATAN — laporkan), menjalankan `npx wrangler@4 r2 object put … --remote` untuk ketiga PDF (`Content-Type: application/pdf`, `Content-Disposition: inline` agar terbuka di browser, cache 1 jam), memasang `robots.txt`, menghapus objek revisi lama project yang sama, lalu memperbarui `.proposal-upload.json`. Mengunggah ulang revisi yang sama menimpa file yang sama (link tidak berubah).

## 2. Verifikasi link
```bash
python3 <folder skill ini>/scripts/upload.py cek --url <url1> <url2> <url3>
```
Ketiganya harus `OK` (200, `application/pdf`). Jangan menyusun pesan WA sebelum ketiga link OK. Bila 404/gagal tersambung, periksa setup domain (§0).

## 3. Pesan WhatsApp pengantar
Tampilkan sebagai blok teks di chat; pengguna menyalin dan mengirim sendiri (skill **tidak** mengirim pesan). Aturan:
- Sapaan sesuai jam WIB saat ini (pagi < 11.00, siang < 15.00, sore < 18.00, malam), lalu "Bapak/Ibu [nama atau jabatan]" sesuai data klien di penawaran.
- **Masa berlaku 14 hari** dihitung dari **tanggal dokumen** penawaran, ditulis lengkap ("5 November 2026").
- Tanpa angka harga dan tanpa angka SLA (keduanya ada di dokumen). Format WhatsApp `*tebal*` seperlunya.
- Pengirim: Yulianto Frandi, CEO Venturo.

Contoh:
```
Selamat siang, Ibu Pimpinan.

Terima kasih atas kesempatan yang diberikan kepada Venturo. Berikut kami sampaikan penawaran untuk *Platform Pembelajaran Kebijakan* (No. VEN/PolicyLab/2026/016):

1. Penawaran Layanan
https://proposal.venturo.id/VEN-PolicyLab-2026-016.pdf

2. Lampiran Estimasi Delivery Point
https://proposal.venturo.id/VEN-PolicyLab-2026-016-Lampiran-Estimasi.pdf

3. Service Agreement
https://proposal.venturo.id/VEN-PolicyLab-2026-016-Service-Agreement.pdf

Penawaran ini berlaku hingga *5 November 2026*.

Apabila sudah sesuai, mohon menandatangani bagian Persetujuan pada Penawaran Layanan dan mengirimkannya kembali kepada kami. Kami dengan senang hati menjelaskan detailnya kapan pun Bapak/Ibu berkenan.

Salam,
Yulianto Frandi
CEO, Venturo
```

## 4. Laporan
- Nomor dokumen, 3 URL beserta hasil `cek`, dan objek revisi lama yang dihapus.
- Pesan WhatsApp (blok teks di atas).
- Ingatkan: link revisi lama tidak aktif lagi; bila klien sudah menerima link lama, kirim ulang link revisi terbaru.

## Yang tidak boleh dilakukan
- Mengunggah set yang tidak lengkap atau mencampur revisi.
- Menaruh penawaran di website company profile (venturo.id) atau menautkannya dari halaman mana pun.
- Mengubah DNS/custom domain atau Transform Rule tanpa izin pengguna.
- Mengirim pesan WhatsApp atas nama pengguna.
