# Tiga gaya desain posting

Contoh Style 1 & 2 (topik "3 Pekerjaan Admin yang Bisa Dibantu AI"): baris atas = Style 1, baris `B1–B6` = Style 2. Contoh Style 3: posting "Hari Kerja Tim Anda – Tanpa AI vs Dengan AI". Tanyakan pengguna gaya mana sebelum mendesain; selang-seling antar-posting agar feed tidak monoton.

Semua frame: root `1080 × 1920`, `padding: 315px 88px 315px`, flex kolom, `overflow: hidden`, font Montserrat.

## Style 1 – Kartu miring

- Latar: putih + lapisan `.bgpat` (pola biner, `background-size: cover`) dengan mask `radial-gradient` di pojok kanan-atas dan kiri-bawah.
- Header frame isi: logo kiri (260 × 63, crop dari PNG logo) + pill "1 / 3" kanan.
- Eyebrow italic kapital `letter-spacing: 0.08em` abu `#58585a`; judul 76–84 px weight 800.
- Visual: kartu putih `border-radius: 24px`, `box-shadow: 0 24px 48px rgba(31,42,46,.18)`, diputar `rotate(±1.5–5deg)`; chip pill warna (teal-700 teks putih, mint/hijau teks ink); mockup chat (bubble putih + bubble hijau muda ber-border `#93cc7c`); diagram alur.
- Kotak bawah "HASILNYA"/"PILIH INI JIKA": latar `#1f2a2e`, teks putih, eyebrow `#93cc7c`, `rotate(-1deg)`.
- Penutup: pita `#259ead` di bagian bawah (mulai y ≈ 1060–1085), kartu CTA putih + logo.

## Style 2 – Blok warna lembut

Urutan latar per frame (lembut, BUKAN pekat):

| Frame | Latar | Aksen |
|---|---|---|
| 1 Hook | putih + pola biner pojok kanan-atas | 3 pita selebar layar: `#eaf6f7`, `#eff8ea`, `#eaf6f7` dengan garis `#d5dfe0`, teks ink, label italic teal/hijau |
| 2 Konteks | `#eaf6f7` | judul 120 px, kata kunci teal; daftar 01/02/03 bergaris `rgba(27,122,134,.25)` |
| 3 Isi 1 | `#f4f7f6` | angka **01** 220 px `#1b7a86` |
| 4 Isi 2 | `#eff8ea` | angka **02** 220 px `#3c7a2a` |
| 5 Isi 3 | `#eaf6f7` | angka **03** 220 px `#1b7a86` |
| 6 Penutup | putih + pita `#1b7a86` di bawah (y ≈ 1060) | chip warna PENUH (teal-700/mint/hijau), kartu CTA putih bayangan tegas `0 24px 48px rgba(31,42,46,.22)` |

- Judul hook 96 px, isi: angka raksasa di kiri + eyebrow & judul 64 px di kanan (flex `align-items: flex-end`).
- Logo di frame berwarna: alas putih `border-radius: 14px; padding: 10px 16px`.
- Kartu isi & "HASILNYA": putih, `box-shadow: 0 8px 24px rgba(31,42,46,.10–.12)`, eyebrow berwarna aksen frame.
- Pengguna TIDAK suka latar pekat untuk frame isi (sudah dicoba: teal/hitam/mint/hijau penuh terasa terlalu kontras). Penutup dengan pita teal tua justru disukai.

## Style 3 – Satu gambar padat

Satu frame, tampilan Style 1 (putih + `.bgpat` bermask, bayangan kartu sama). Susunan yang terbukti muat di zona 4:5 (konten y 315–1616) dengan root `gap: 22px`:

| Bagian | Spesifikasi |
|---|---|
| Header | logo kiri (260 × 63) + eyebrow kanan: kotak 18 px `#1b7a86` + teks italic kapital 24 px `#58585a` (mis. "EFISIENSI DI ERA AI") |
| Judul | 70 px / 78 px weight 800, 2 baris; baris kedua `#1b7a86` |
| Kartu tabel | putih, `border-radius: 24px`, padding 20 px, `rotate(-1deg)`, bayangan `0 24px 48px rgba(31,42,46,.18)`; grid `196px 1fr 1fr`, gap 10 px |
| Kepala kolom | "PEKERJAAN" 18 px abu; chip "✕ TANPA AI" latar `#d5dfe0` teks `#58585a`; chip "✓ DENGAN AI" latar `#1b7a86` teks putih (ikon SVG garis) |
| Baris (5–6) | label 23 px weight 800; sel kiri `#f4f7f6` teks `#6b7072` 500; sel kanan `#eff8ea` border 2 px `#93cc7c` teks ink 600; sel 22 px / 28 px, padding 12 × 16, radius 14 |
| HASILNYA | kotak `#1f2a2e`, `rotate(1deg)`, eyebrow `#93cc7c`, teks 28 px weight 700, frasa kunci `#93cc7c` |
| CTA | kalimat tanya 24 px 600 + pil "Konsultasi gratis" `#259ead` teks putih; baris bawah "WA kami atau klik link di bio" 22 px abu |

- Teks sel maksimal ±50 karakter (≤ 3 baris). Persingkat, jangan kecilkan font di bawah 22 px.
- Kalau `render.py` melaporkan keluar zona beberapa px, kurangi `gap` root dulu (26 → 22) sebelum mengubah isi.
