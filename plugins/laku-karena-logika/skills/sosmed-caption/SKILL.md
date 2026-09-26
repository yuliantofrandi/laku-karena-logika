---
name: sosmed-caption
description: Menulis judul dan caption posting sosial media Venturo (TikTok, Instagram, Threads) dari isi desain carousel yang sudah final, lalu menyimpannya sebagai caption.md di folder Google Drive posting. Gunakan saat pengguna berkata "buat caption", "tulis caption", "sosmed caption", "caption untuk posting ini", atau setelah desain carousel selesai.
---

# Sosmed – Caption

Tulis judul dan caption dari isi frame yang sudah final, simpan ke `caption.md`.

## 1. Baca isi desain

- Sumber utama: kanvas Design posting (baca file artboard sesuai urutan `order`), atau gambar hasil ekspor di folder Drive posting.
- Ambil: hook frame pertama, poin tiap frame isi, dan CTA penutup.

## 2. Tulis judul

- Maksimal ±60 karakter, berbentuk pertanyaan atau pernyataan tajam, sama dengan inti hook. Contoh: "Coding, Automation, atau AI Agent?"
- Judul dipakai sebagai `title` foto/carousel TikTok.

## 3. Tulis caption (gaya pengguna)

- Singkat. JANGAN merinci ulang isi gambar.
- Susunan dengan jeda baris (baris kosong antarparagraf):
  1. Baris hook (boleh satu emoji relevan di akhir, mis. 🤖).
  2. 1–2 kalimat inti/insight.
  3. 1–2 kalimat penegasan atau risiko salah pilih.
  4. CTA: "Butuh bantuan memilih? WA kami atau klik link di bio." (sesuaikan).
  5. 3–5 hashtag, selalu sertakan `#Venturo`.
- Panjang total ≤ 500 karakter (batas Threads). Hitung dan pastikan.

## 4. Tampilkan dan minta persetujuan

Tampilkan judul dan caption di chat dalam blok kode agar jeda baris terlihat. Terapkan revisi pengguna sebelum menyimpan.

## 5. Simpan `caption.md`

Lokasi: `Sosmed/<Judul Posting>/caption.md` di Google Drive pengguna yang tersinkron ke komputernya (Google Drive for desktop). Temukan folder `Sosmed` lewat daftar folder di komputer pengguna; bila ada lebih dari satu akun Drive atau folder tidak ditemukan, tanyakan ke pengguna. Minta akses folder bila belum terhubung. Jangan menimpa `caption.md` yang sudah ada tanpa izin — jika sudah ada, edit bagian caption saja.

Format file:

```markdown
# <Judul Posting>

## Judul (khusus TikTok, postingan foto/carousel)
<judul>

## Caption (Instagram, TikTok & Threads)
<caption dengan jeda baris>

## Urutan gambar
1. 01-<nama>.jpg
2. ...
```

## 6. Serah terima

Tawarkan langkah berikut: `sosmed-posting`.
