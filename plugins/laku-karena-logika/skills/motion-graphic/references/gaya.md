# Tiga gaya motion graphic

Semua gaya: 30 fps, font Inter (fallback dari font aplikasi), warna primer diambil dari menu aktif aplikasi, latar halus (gradien radial pastel + blob blur), tanpa audio (pengguna menambah musik sendiri).

## Style 1 – Promo fitur (9:16)

Template: `assets/style1-promo-fitur-9x16.html` (27 dtk, 6 scene).

| Scene | Durasi | Isi |
|---|---|---|
| Intro | ±3,4 dtk | Hook 2 baris muncul per kata (mis. "Tim kerja dari mana saja. / Tapi jam kerjanya terukur?"), lalu logo + tagline membesar |
| Fitur ×4 | ±4,5–5 dtk tiap | Kicker pill "01 · NAMA FITUR" + headline 76px (kata kunci diwarnai primer) di atas; kartu mockup UI putih radius 40 di bawah, isinya beranimasi (kartu muncul bertahap, angka menghitung naik, bar terisi, timeline terbuka, thumbnail pop, klik tombol + toast) |
| Outro | ±3,8 dtk | Logo besar, kalimat nilai, chip fitur (6 maks, termasuk keunggulan non-fitur mis. "Server di Indonesia"), tombol CTA domain berdenyut |

Aturan: satu pesan per scene; headline ≤ 8 kata; mockup meniru komponen asli aplikasi (bukan screenshot); perpindahan scene crossfade 0,35–0,45 dtk.

## Style 2 – Walkthrough layar (16:9)

Template: `assets/style2-walkthrough-16x9.html` (50,5 dtk, 9 halaman).

- Rekreasi aplikasi pada kanvas logis **1600×900**, diskalakan 1,2× ke 1920×1080. Sidebar persisten (menu aktif berganti), topbar (filter tanggal, filter karyawan, avatar akun dummy), area konten berisi halaman.
- Tiap halaman: elemen masuk bertahap (fade + naik 18px), bar terisi, angka menghitung.
- Kursor SVG + riak klik hijau. Alur khas: daftar → klik item → halaman detail (klik tab-tab di dalamnya) → klik menu sidebar satu per satu → interaksi form di Pengaturan (ketik di input, chip baru muncul, klik Simpan → toast).
- Kamera: zoom 1,15–1,45× ke area yang sedang dibahas (timeline, kolom tabel, form), lalu kembali 1×. Modal pratinjau untuk screenshot.
- Tanpa teks promosi. Penutup: layar putih, logo + tagline + pill domain.
- Durasi per halaman 3,5–5 dtk; halaman utama (detail) boleh 8–9 dtk.

## Style 3 – Walkthrough layar (9:16)

Template: `assets/style3-walkthrough-9x16.html` (turunan Style 2, waktu & klik identik).

- Aplikasi 1600×900 di dalam jendela berbingkai **1000×1170** (radius 32, bayangan), skala dasar **1,3×** agar teks terbaca di HP → lebar terlihat ±770 px logis, sehingga kamera harus pan.
- Posisi pan standar (z=1): sidebar `cx=385`, konten kiri `cx=685`, konten kanan `cx=1215`. Halaman pendek (daftar, tabel, kartu) pakai z=1,15 dan cy=380 agar ruang kosong bawah tidak terlihat.
- Pola kamera tiap halaman: di sidebar saat klik menu → pan ke konten kiri (nama, bar) → pan ke kanan (durasi, kolom lanjutan) → kembali ke sidebar sebelum klik menu berikutnya. Pastikan target klik ada di area terlihat saat klik terjadi.
- Elemen di luar jendela: logo (64px) kiri atas + pill nama menu kanan atas (y≈200), indikator progres titik (halaman aktif memanjang) + domain di bawah jendela.
- Bila pengguna minta "hanya layar", hapus header/footer dan perbesar jendela.
