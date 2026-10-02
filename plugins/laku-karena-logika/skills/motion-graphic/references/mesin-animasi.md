# Mesin animasi (kontrak template)

## Kontrak dasar
- Seluruh animasi adalah fungsi murni `render(t)` (t = detik). Dilarang memakai CSS animation/transition atau `setTimeout` — render frame-per-frame membutuhkan hasil yang sama untuk t yang sama.
- Ekspos `window.render` dan `window.DUR`. Bila URL berisi `?rec`, panggil `render(0)` saja; selain itu jalankan loop `requestAnimationFrame` untuk pratinjau di browser.
- Helper: `p(t,a,b)` progres 0..1, `eo` ease-out cubic, `eio` ease-in-out, `eb` ease-back (pop), `fmt(menit)` → "8j 12m".
- Ukuran `html,body` = ukuran video (1080×1920 atau 1920×1080), `overflow:hidden`.

## Style 1
- Scene = `.scene` absolut dengan rentang `SC={id:[mulai,selesai]}`; alpha scene = fade-in 0,45 dtk / fade-out 0,35 dtk; `.head` (kicker + headline) masuk otomatis.
- `pop(el,t,mulai,durasi,dy)` untuk kartu/thumbnail. Data karyawan dummy di array `EMP` (nama, jabatan, menit).
- Mengganti produk: ubah teks hook, kicker/headline tiap scene, isi kartu mockup, chip outro, domain CTA, gradien logo.

## Style 2 & 3 (walkthrough)
- **Halaman**: `<div class="page" id="p-...">` di dalam `#main`. Jadwal di `PAGES=[[idHalaman, detikMulai, idMenuAktif], ...]`. Elemen `.in` otomatis masuk bertahap; `.fill[data-w][data-d][data-dur]` bar terisi; `.cntm[data-m][data-d]` angka menit menghitung; `.cnt[data-n]` angka biasa.
- **Kursor**: `MOVES=[[detikTiba, '#selector' | [x,y], durasiGerak], ...]`. Selector di-resolve sekali ke koordinat logis aplikasi (tengah elemen; menu sidebar digeser ke x+80). `CLICKS=[detik,...]` memicu riak + kursor mengecil — taruh ±0,1 dtk setelah kursor tiba, dan halaman berikutnya mulai ±0,3 dtk setelah klik.
- **Kamera**: `CAM=[[detik, zoom, cx, cy], ...]` dalam koordinat logis 1600×900, diinterpolasi ease-in-out; `setCam` meng-clamp agar tidak keluar tepi aplikasi (zoom minimum 1).
  - Style 2: `S=1.2`, pusat layar 960×540.
  - Style 3: `S=1.3`, jendela 1000×1170 → pusat 500×585.
- **State khusus** (tab di halaman detail, modal, ketik di input, chip baru, toast) diatur di `render(t)` berdasarkan rentang waktu.
- Konversi Style 2 → Style 3: bungkus `#app` dengan `#win`, ganti ukuran body, `S`, `setCam`, dan susun ulang `CAM` dengan pola pan sidebar → kiri → kanan (lihat `gaya.md`). `PAGES`, `MOVES`, `CLICKS` tetap.

## Thumbnail screenshot palsu
Fungsi `scr(jenis, big)` menggambar layar mini dengan CSS: 0 = code editor gelap, 1 = tool desain, 2 = dashboard grafik, 3 = spreadsheet. Untuk pratinjau besar di modal pakai faktor skala ±5,4.

## Jebakan yang pernah terjadi
- `camAt` mengembalikan elemen waktu di indeks 0 → harus `slice(1)` sebelum dipakai sebagai `[z,cx,cy]` (gejala: seluruh layar bergeser/terpotong).
- Kartu grid dengan tinggi tetap memotong baris terakhir → hitung tinggi isi atau longgarkan.
- Daftar dalam tab setinggi tetap: thumbnail 2 baris butuh tinggi ±128 px per baris.
- `range(FPS*DUR)` dengan DUR desimal → bulatkan ke int (sudah ditangani `render.py`).
- Unduh logo/font dari domain aplikasi bisa diblokir proxy/CORS; `toDataURL` besar dari browser bisa diblokir juga → rekreasi logo sebagai teks.
- Emoji dipakai sebagai ikon kecil di template; ganti dengan SVG bila hasil render emoji kurang rapi.
