---
name: proposal-upload
description: Mengunggah 3 PDF penawaran Venturo hasil skill proposal-pdf (Penawaran Layanan, Lampiran Estimasi Delivery Point, Service Agreement) — file hasil sesi chat sebelumnya — ke bucket R2 Cloudflare di proposal.venturo.id, terpisah dari website company profile, langsung tanpa konfirmasi dengan URL sesuai nama file; mengecek domain, memverifikasi ketiga link, lalu menyusun pesan WhatsApp pengantar 2 bubble berisi link, masa berlaku penawaran 14 hari, dan ajakan review. Pakai saat diminta "upload penawaran", "unggah PDF penawaran", "kirim penawaran ke klien", "buat link penawaran", "pesan WA penawaran", atau setelah proposal-pdf selesai.
---

# Upload Penawaran → proposal.venturo.id (R2) + Pesan WhatsApp

Lanjutan skill `proposal-pdf`. Tiga PDF satu set (nomor dokumen dan revisi sama) diunggah dari **file PDF hasil `proposal-pdf` di sesi chat sebelumnya** ke bucket R2 **`proposal`** yang tersambung ke domain **`proposal.venturo.id`**, terpisah dari website company profile venturo.id. Hasilnya:

`https://proposal.venturo.id/<nama-file>.pdf` (mis. `https://proposal.venturo.id/VEN-PolicyLab-2026-016.pdf`)

- URL = **nama file apa adanya** di akar bucket, tanpa kode acak. R2 tidak menampilkan daftar isi bucket.
- Hanya **revisi terbaru** per project yang di-hosting; objek revisi lama dihapus saat revisi baru diunggah.
- Unggah dilakukan **langsung**, tanpa meminta konfirmasi (ketetapan pengguna).
- `robots.txt` (`Disallow: /`) dipasang di bucket agar mesin pencari tidak merayapi.
- Semua laporan dan komunikasi dalam **Bahasa Indonesia**.

## 0. Persiapan
- **Input**: 3 PDF yang dihasilkan `proposal-pdf` di **sesi chat sebelumnya** — set lengkap `VEN-<Project>-<Tahun>-<Rev>.pdf`, `…-Lampiran-Estimasi.pdf`, `…-Service-Agreement.pdf`. `--pdf` menerima satu atau beberapa **folder dan/atau file**, jadi file boleh tersebar di lokasi berbeda. Cara menemukannya, berurutan:
  1. Path file yang dilampirkan/disebut pengguna di chat.
  2. Folder hasil `proposal-pdf` (default `penawaran/` di working directory sesi tersebut).
  3. Bila belum jelas, cari PDF penawaran terbaru (scratchpad sesi Claude ikut dicari), lalu pastikan ke pengguna bila ada lebih dari satu project/revisi:
     ```bash
     find ~ /private/tmp/claude-* -maxdepth 7 -name 'VEN-*-[0-9][0-9][0-9]*.pdf' -mtime -30 -not -path '*/Library/*' 2>/dev/null | xargs ls -t 2>/dev/null | head -20
     ```
- **Auth Cloudflare** (pilih salah satu; cek dengan `npx wrangler@4 whoami`):
  1. **Login wrangler** di komputer ini: pengguna menjalankan sendiri `npx wrangler@4 login` (membuka browser, OAuth). Tidak perlu memberikan apa pun ke Claude.
  2. **API token** (untuk komputer/server lain atau otomatisasi): pengguna membuat token di Cloudflare dashboard → My Profile → API Tokens → Create Token → Custom token dengan izin **Account › Workers R2 Storage › Edit** untuk akun Venturo, lalu menyetelnya sendiri sebagai env `CLOUDFLARE_API_TOKEN` dan `CLOUDFLARE_ACCOUNT_ID`. Token **jangan** ditempel di chat, ditulis ke file skill, memori, atau commit.
- **Log unggahan** disimpan di lokasi tetap `~/.venturo/proposal-upload.json` (bisa diubah dengan env `PROPOSAL_UPLOAD_LOG`), **bukan** di folder PDF — folder hasil sesi sebelumnya (mis. scratchpad) bisa sementara. Wrangler tidak bisa menampilkan isi bucket, jadi log inilah yang dipakai untuk mengenali dan menghapus revisi lama. Jangan dihapus. Log lama `.proposal-upload.json` di folder PDF tetap dibaca (migrasi otomatis).

### Setup domain (sekali)
1. Bucket R2 `proposal` (sudah dibuat): `npx wrangler@4 r2 bucket list`.
2. **Hapus dulu record DNS lama** `proposal.venturo.id` (dulu mengarah ke server nginx). Tanpa itu custom domain R2 tidak bisa ditambahkan.
3. Tambahkan custom domain di dashboard Cloudflare: R2 → `proposal` → Settings → Custom Domains → `proposal.venturo.id`. Tunggu status **Active** (± 1–2 menit) sebelum `cek`.
4. **Transform Rule** di zona venturo.id (Rules → Transform Rules → Modify Response Header) untuk hostname `proposal.venturo.id`: set `X-Robots-Tag: noindex, nofollow`. Belum terpasang; tanpa ini `cek` memberi PERINGATAN (bukan gagal).

Langkah 2–4 mengubah DNS/aturan zona: **dilakukan pengguna sendiri** di dashboard; Claude hanya mengingatkan.

Ciri domain belum terhubung: `robots.txt` tetap 200 (dari server lama), tapi PDF 404.

## 1. Cek domain (wajib, di awal)
```bash
python3 <folder skill ini>/scripts/upload.py domain
```
Bila hasilnya **BELUM ADA custom domain**, semua link akan 404. Beri tahu pengguna (dengan langkah setup di atas) **sebelum atau bersamaan** dengan unggah; unggah tetap boleh dijalankan.

## 2. Unggah
```bash
python3 <folder skill ini>/scripts/upload.py unggah --pdf <folder/file PDF> [<folder/file PDF> ...]
```
Skrip memilih set lengkap dengan revisi tertinggi (set yang tidak lengkap dilewati dengan PERINGATAN — laporkan), menjalankan `npx wrangler@4 r2 object put … --remote` untuk ketiga PDF (`Content-Type: application/pdf`, `Content-Disposition: inline` agar terbuka di browser, cache 1 jam), memasang `robots.txt`, menghapus objek revisi lama project yang sama, lalu memperbarui log. Mengunggah ulang revisi yang sama menimpa file yang sama (link tidak berubah).

## 3. Verifikasi link
```bash
python3 <folder skill ini>/scripts/upload.py cek --url <url1> <url2> <url3>
```
Ketiganya harus `OK` (200, `application/pdf`). Jangan menyusun pesan WA sebelum ketiga link OK, kecuali pengguna sudah diberi tahu domain belum tersambung. **Jangan membuka URL PDF di browser pane** (memicu dialog unduh); cukup `cek`.

## 4. Data untuk pesan
```bash
python3 <folder skill ini>/scripts/upload.py info --pdf <folder/file PDF> [<folder/file PDF> ...]
```
Membaca teks PDF (PDFKit bawaan macOS; cadangan `pdftotext`/`pypdf`) → **nama project**, **tanggal dokumen**, **berlaku hingga** (+14 hari), dan **ada/tidaknya diskon** di ketiga PDF (kata kunci: diskon, potongan, discount, promo; kata "gratis" di Service Agreement — akses pantau progres — **bukan** diskon). Bila nama/tanggal tidak terbaca, periksa teks PDF secara manual.

## 5. Pesan WhatsApp pengantar
Tampilkan di chat sebagai **2 bubble** (dua blok teks terpisah); pengguna menyalin dan mengirim sendiri — skill **tidak** mengirim pesan.

Aturan:
- **Bubble 1**: sapaan sesuai jam WIB saat ini (pagi < 11.00, siang < 15.00, sore < 18.00, malam) + `...` sebagai tempat sapaan & nama (diisi pengguna) + ucapan terima kasih.
- **Bubble 2**: dari link penawaran sampai permintaan feedback.
- **Tanpa nomor dokumen**, tanpa "Bapak/Ibu" di badan pesan.
- **Penawaran Layanan = dokumen utama**; Lampiran Estimasi dan Service Agreement disebut sebagai pelengkap.
- **Masa berlaku 14 hari** dari tanggal dokumen, ditulis lengkap, beserta alasannya (persiapan tim & setup) dan akibat bila lewat (ketersediaan tim dan harga berbeda → penawaran diperbarui).
- **Diskon**: bila `info` → `ada_diskon: false`, **jangan menyebut diskon sama sekali**. Bila `true`, tambahkan tepat setelah kalimat masa berlaku: "Potongan harga hanya berlaku dalam masa penawaran ini, karena kondisi project dan ratecard dapat berubah setelahnya."
- **Tidak meminta tanda tangan**; arahkan ke kontak langsung atau meeting.
- **Tanpa salam penutup** dan tanpa nama pengirim; penutup = meminta review & feedback.
- Tanpa angka harga dan angka SLA. Format WhatsApp `*tebal*` seperlunya.

Template — Bubble 1:
```
Selamat siang, ...
Terima kasih atas kesempatan yang diberikan 🙏
```

Template — Bubble 2:
```
Berikut kami sampaikan penawaran layanan untuk *<Nama Project>*:
https://proposal.venturo.id/<VEN-Project-Tahun-Rev>.pdf

Sebagai pelengkap, kami lampirkan juga:
• Lampiran Estimasi Delivery Point
https://proposal.venturo.id/<VEN-Project-Tahun-Rev>-Lampiran-Estimasi.pdf
• Service Agreement
https://proposal.venturo.id/<VEN-Project-Tahun-Rev>-Service-Agreement.pdf

Penawaran ini berlaku hingga *<tanggal dokumen + 14 hari>*. Waktu ini kami perlukan untuk menyiapkan tim dan setup agar project berjalan lancar. Setelah tanggal tersebut, ketersediaan tim dan harga dapat berbeda, sehingga penawaran perlu kami perbarui.

Apabila ada hal yang ingin ditanyakan, silakan menghubungi saya langsung, atau dengan senang hati jika ada jadwal meeting untuk membahasnya.

Saya tunggu review dan feedbacknya .. 🙏
```

## 6. Laporan (Bahasa Indonesia)
- Status domain, 3 URL beserta hasil `cek`, dan objek revisi lama yang dihapus.
- Pesan WhatsApp (2 bubble di atas).
- Ingatkan: link revisi lama tidak aktif lagi; bila klien sudah menerima link lama, kirim ulang link revisi terbaru. Bila domain/Transform Rule belum disetel, sebutkan langkahnya.

## Yang tidak boleh dilakukan
- Mengunggah set yang tidak lengkap atau mencampur revisi.
- Menaruh penawaran di website company profile (venturo.id) atau menautkannya dari halaman mana pun.
- Mengubah DNS/custom domain atau Transform Rule tanpa izin pengguna.
- Menyimpan log unggahan di folder sementara.
- Membuka URL PDF di browser pane.
- Menyebut diskon bila penawaran tidak memuat diskon.
- Meminta klien menandatangani di pesan WA.
- Mengirim pesan WhatsApp atas nama pengguna.
