---
name: sosmed-caption
description: Menulis judul dan caption posting sosial media Venturo dari isi desain (carousel atau satu gambar) yang sudah final — dua versi: ber-enter untuk Instagram & Threads, satu paragraf untuk TikTok — lalu menyimpannya sebagai caption.md di folder Google Drive posting. Gunakan saat pengguna berkata "buat caption", "tulis caption", "sosmed caption", "caption untuk posting ini", atau setelah desain carousel selesai.
---

# Sosmed – Caption

Tulis judul dan caption dari isi frame yang sudah final, simpan ke `caption.md`.

## 1. Baca isi desain

- Sumber: kanvas Design posting (artboard versi yang dipilih, sesuai urutan), brief yang sudah disetujui, atau gambar hasil ekspor di folder Drive posting.
- Ambil: hook frame pertama, poin tiap frame isi, dan CTA penutup.

## 2. Tulis judul

- Maksimal ±60 karakter, pertanyaan atau pernyataan tajam, sama dengan inti hook. Contoh: "3 Pekerjaan Admin yang Bisa Dibantu AI Mulai Minggu Depan".
- Judul dipakai sebagai `title` foto/carousel TikTok.

## 3. Tulis caption – versi Instagram & Threads (ber-enter)

- Singkat. JANGAN merinci ulang isi gambar.
- Susunan dengan baris kosong antarparagraf:
  1. Baris hook (boleh satu emoji relevan di akhir, mis. 🤖).
  2. 1–2 kalimat inti/insight.
  3. 1 kalimat penegasan/manfaat atau risiko salah pilih.
  4. CTA, mis. "Mau tahu mana yang paling cocok untuk bisnis Anda? WA kami atau klik link di bio."
  5. 3–5 hashtag topik. JANGAN pakai hashtag nama perusahaan (`#Venturo`).
- Panjang total ≤ 500 karakter (batas Threads). Hitung dan pastikan.

## 4. Tulis caption – versi TikTok (satu paragraf)

TikTok (posting foto lewat Metricool) membuang semua enter; trik karakter tak terlihat `⠀` sudah dicoba dan GAGAL (jadi spasi aneh). Jadi:

- Isi sama dengan versi ber-enter, disusun sebagai SATU paragraf yang tetap enak dibaca: kalimat pendek, tiap bagian diakhiri titik/tanda tanya, tanpa `⠀` dan tanpa baris kosong.
- Hashtag di akhir, dipisah spasi.

## 5. Tampilkan dan minta persetujuan

Tampilkan judul dan kedua versi caption dalam blok kode. Terapkan revisi pengguna sebelum menyimpan. Persetujuan caption di sini boleh digabung dengan konfirmasi posting (lihat `sosmed-posting`).

## 6. Simpan `caption.md`

Lokasi: `Sosmed/<Judul Posting>/caption.md` (nama folder TANPA `:` `/` `?` — ganti titik dua dengan " – ", mis. `Hari Kerja Tim Anda – Tanpa AI vs Dengan AI`; judul TikTok tetap boleh memakai titik dua) di Google Drive pengguna yang tersinkron ke komputernya (Google Drive for desktop). Temukan folder `Sosmed` lewat daftar folder di komputer pengguna; bila ada lebih dari satu akun Drive atau folder tidak ditemukan, tanyakan. Minta akses folder bila belum terhubung. Jangan menimpa `caption.md` yang sudah ada tanpa izin — jika sudah ada, edit bagian yang berubah saja.

Format file:

```markdown
# <Judul Posting>

## Judul (khusus TikTok, postingan foto/carousel)
<judul>

## Caption (Instagram & Threads)
<caption dengan jeda baris>

## Caption TikTok (satu paragraf)
<caption satu paragraf>

## Urutan gambar
1. 01-<nama>.jpg
2. ... (satu baris saja untuk posting satu gambar)

Desain: <Style 1/2/3>, artboard <daftar artboard> di kanvas <link>.
```

## 7. Serah terima

Tawarkan langkah berikut: `sosmed-posting`.
