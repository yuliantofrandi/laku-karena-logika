# Standar UI

Warna & font mengikuti brand (Venturo: Montserrat, teal `#007f96`). Semua komponen ada di `assets/css/style.css` proyek; pola di bawah adalah aturan yang sudah disetujui pengguna.

## Latar section selang-seling

- Section bergantian `section` (putih) dan `section--canvas` (abu muda), diatur otomatis oleh script, jadi menambah/memindah section tidak merusak ritme.
- Dua section berurutan dengan latar sama: padding antar keduanya diciutkan (tidak dobel). **Kecualikan** blok yang punya latar/kotak sendiri: `.eco`, `.offer`, `.assure`, `.pf-cta`, `.proof-band`.
- Setelah perubahan, cek jarak antar section di semua halaman (keluhan umum: "padding terlalu tinggi").

## Teks panjang → kartu

- Paragraf panjang dipecah jadi kartu `.features--why` (3 kartu) atau `.features--pair` (2 kartu).
- Grid 4 kolom turun ke 2 kolom di tablet dan 1 di ponsel.
- "Fakta singkat" ditampilkan sebagai kotak kecil berjudul "Sekilas Tentang <Brand>".

## Video

- Layout `.why`: video di satu sisi, poin di sisi lain.
- Lite YouTube: `<div class="yt-lite" data-yt="<id>">` dengan thumbnail self-host di `assets/img/video/`, iframe `youtube-nocookie.com` baru dibuat saat diklik (`main.js`).

## Bukti

- `.proof-band`: pita bukti dengan foto tim pudar di latar.
- Kartu portfolio nyata dari CMS (judul, cover, badge AI bila kategori `portfolio-ai`), bukan placeholder.
- Related portfolio 4 kolom.

## Hero & tombol

- H1 `clamp(32px, 3.4vw, 50px)`. Cek di laptop 14" agar tidak terlalu besar.
- `.btn--lg`: padding 16px 28px, font 16px. Jangan lebih besar.
- Foto hero = foto tim asli; foto khusus (misal foto acara) hanya di halaman yang diminta.
- Foto dan teks rata tengah vertikal bila berdampingan.

## Navbar & footer

- Navbar dengan grup dropdown; footer **mencerminkan grup navbar** (contoh Venturo: Model kerja sama / Solusi / AI Project / Perusahaan / Karir).
- Setiap halaman jasa wajib ada di menu (keluhan umum: "saya tidak menemukan menu ini di header").
- Footer: alamat kantor dengan ikon, nomor WA, tanpa email, tanpa "PT" bila pengguna minta.
- Menu mobile: animasi `clip-path` agar halus; submenu dengan garis pemisah antar item.

## Tabel

- `table-layout: fixed`, kolom sama lebar. Di ponsel bungkus dengan scroll horizontal di dalam kontainer (bukan seluruh halaman).

## Cek tampilan (wajib setelah edit UI)

- Lebar 375px (ponsel), 768px (tablet), 1366–1440px (laptop 14").
- Tidak ada teks meluber/terpotong, tidak ada scroll horizontal halaman, caption foto terbaca di mobile.
- Ambil screenshot dengan headless Chrome atau browser pane, lalu lampirkan ke pengguna.
