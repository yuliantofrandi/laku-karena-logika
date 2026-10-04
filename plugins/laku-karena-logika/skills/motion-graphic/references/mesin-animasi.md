# Mesin animasi — kontrak `assets/video-screenshot.html`

## Kontrak dasar
- Seluruh animasi adalah fungsi murni `render(t)` (t = detik). Dilarang memakai CSS animation/transition atau `setTimeout` — render frame-per-frame membutuhkan hasil yang sama untuk t yang sama.
- Template mengekspos `window.render`, `window.DUR`, dan `window.READY` (true setelah semua screenshot dimuat; `render.py` menunggunya). Bila URL berisi `?rec`, animasi tidak diputar sendiri; selain itu ada loop pratinjau `requestAnimationFrame`.
- Helper: `p(t,a,b)` progres 0..1, `eo` ease-out cubic, `eio` ease-in-out.
- Yang diedit hanya blok **ISI VIDEO**. Ukuran video, posisi jendela, dan ukuran huruf diatur oleh `PRESET` per `GAYA`.

## Blok ISI VIDEO
| Nama | Isi |
|---|---|
| `GAYA` | 1 = promo fitur 9:16, 2 = walkthrough 16:9, 3 = walkthrough 9:16 |
| `CFG.shotW` | `window.innerWidth` tab saat screenshot diambil (px CSS). Semua screenshot satu video harus diambil dengan lebar jendela yang sama |
| `CFG.dur` | durasi total (detik) |
| `CFG.produk / tagline / domain / pri` | teks logo, tagline, domain CTA, warna primer (warna menu aktif aplikasi) |
| `SHOTS` | `[file, detikMulai, labelMenu]`. Tiap screenshot tampil sampai screenshot berikutnya; pergantian crossfade 0,35 dtk. `labelMenu` dipakai pill Style 3 |
| `MOVES` | `[detikTiba, [x,y], lamaGerak]` — kursor bergerak ease-in-out dan tiba di `[x,y]` pada `detikTiba` |
| `CLICKS` | detik klik → riak warna primer + kursor mengecil. Taruh ±0,1 dtk setelah kursor tiba; screenshot berikutnya mulai ±0,3 dtk setelah klik |
| `CAM` | `[detik, zoom, cx, cy]` — titik fokus kamera, diinterpolasi ease-in-out. Zoom 1 = lebar screenshot pas selebar jendela |
| `CAPS` | Style 1: `[mulai, selesai, 'KICKER', 'Headline <b>kata kunci</b>']` (kata di `<b>` diwarnai primer) |
| `INTRO` | Style 1: `[detikSelesai, 'Hook baris 1<br>Hook baris 2']`, `null` = tanpa |
| `OUTRO` | detik mulai kartu penutup (logo + tagline + domain), `null` = tanpa |

## Koordinat
- `MOVES` dan `CAM` memakai **piksel CSS halaman aplikasi** — persis `getBoundingClientRect()` di tab pengguna saat screenshot diambil (x dari kiri viewport, y dari atas viewport). Bukan piksel video, bukan piksel PNG (PNG Retina = 2× lebih besar).
- Untuk target klik pakai tengah elemen: `x = left + width/2`, `y = top + height/2`.
- `setCam` meng-clamp fokus agar kamera tidak keluar tepi screenshot; kalau screenshot lebih pendek dari jendela, gambar diletakkan di tengah vertikal (naikkan zoom supaya ruang kosong tidak terlihat).

## Jebakan
- Screenshot dengan lebar jendela berbeda membuat koordinat dan skala meleset — ambil semua screenshot dengan ukuran jendela yang sama.
- Zoom browser selain 100% membuat `innerWidth` (px CSS) tidak cocok dengan ukuran tangkapan layar.
- Animasi/loading di aplikasi (skeleton, spinner, toast) bisa ikut tertangkap — tunggu halaman tenang sebelum menangkap.
- Penyamaran (`privasi.js`) hilang setiap kali halaman dinavigasi/dirender ulang — jalankan lagi tepat sebelum tiap tangkapan.
- Teks di dalam gambar/canvas (grafik, foto dokumen) tidak bisa disamarkan lewat DOM — pilih layar lain atau minta keputusan pengguna.
- `range(FPS*DUR)` dengan DUR desimal → dibulatkan oleh `render.py`.
