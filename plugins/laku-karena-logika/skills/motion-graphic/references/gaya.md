# Tiga gaya motion graphic

Semua gaya: 30 fps, bahan = screenshot asli layar aplikasi pengguna (sudah disamarkan), warna aksen = warna primer menu aktif aplikasi, latar halus (gradien radial dari warna primer), tanpa audio. Satu template: `assets/video-screenshot.html`, pilih lewat `GAYA`.

## Style 1 – Promo fitur (9:16, `GAYA = 1`)

| Bagian | Durasi | Isi |
|---|---|---|
| Intro | ±3 dtk | Kartu putih: hook 2 baris (mis. "Tim kerja dari mana saja. / Jamnya tetap terukur?") + nama produk |
| Fitur ×3–5 | ±4,5–5 dtk tiap | Kicker pill "01 · NAMA FITUR" + headline 76px (kata kunci di `<b>`) di atas; screenshot asli di kartu berbingkai di bawah, kamera zoom 1,4–1,8× ke bagian yang dibahas |
| Outro | ±3,5 dtk | Logo, tagline, tombol CTA domain |

Aturan: satu pesan per scene; headline ≤ 8 kata dalam bahasa manfaat; satu screenshot per fitur (`SHOTS` dan `CAPS` berbagi rentang waktu); kursor boleh diam di luar layar kalau tidak ada klik.

## Style 2 – Walkthrough layar (16:9, `GAYA = 2`)

- Screenshot memenuhi seluruh video 1920×1080. Ambil screenshot dengan jendela sekitar 1440×900 agar teks tetap terbaca setelah diskalakan.
- Alur khas: daftar → klik item → halaman detail (klik tab-tabnya) → klik menu sidebar satu per satu → pengaturan.
- Kamera: zoom 1,15–1,45× ke area yang sedang dibahas (tabel, grafik, form), lalu kembali 1× sebelum klik menu berikutnya.
- Tanpa teks promosi. Penutup: kartu logo + tagline + domain (`OUTRO`).
- Durasi per layar 3,5–5 dtk; layar utama boleh 8–9 dtk.

## Style 3 – Walkthrough layar (9:16, `GAYA = 3`)

- Screenshot di dalam jendela berbingkai 1000×1170 (radius 32, bayangan). Pakai zoom dasar **1,3** agar teks terbaca di HP, sehingga kamera harus pan.
- Pola kamera tiap layar: di sidebar saat klik menu → pan ke konten kiri → pan ke konten kanan → kembali ke sidebar sebelum klik menu berikutnya. Pastikan target klik terlihat di jendela saat klik terjadi.
- Layar pendek (tinggi screenshot < tinggi jendela): naikkan zoom ke ±1,5 agar ruang kosong atas/bawah tidak terlihat.
- Di luar jendela: logo kiri atas + pill nama menu (`SHOTS[i][2]`) kanan atas, indikator titik (layar aktif memanjang) + domain di bawah jendela.
- Bila pengguna minta "hanya layar", ubah `PRESET[3].win` menjadi `[0,0,1080,1920]`, `rad:0`, dan hapus `hdr` dari `PRESET[3]` (header, titik, dan domain ikut hilang).
