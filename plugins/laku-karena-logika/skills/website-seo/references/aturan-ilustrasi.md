# Aturan Ilustrasi & Gambar

Aturan tetap dari user: **setiap halaman selalu diberi gambar ilustrasi**, baik ilustrasi tampilan aplikasi maupun ilustrasi konsep yang dibutuhkan section itu, supaya website tidak monoton dan tidak hanya berisi teks. Ilustrasi adalah **placeholder dengan brief**: user melihat tiap section butuh gambar seperti apa, lalu mengirim gambar yang lebih bagus.

## Sistem

- `data/ilustrasi.json` adalah satu sumber untuk semua gambar. Per entri: `id` (kebab-case deskriptif = nama file, baik untuk SEO), `halaman`, `section` (teks H2 persis, atau `Hero`), `jenis`, `judul`, `alt`, `caption`, **`brief`** (gambar asli seperti apa yang dibutuhkan), `auto`, dan `data` (isi mockup). `hero` memetakan slug → id gambar hero.
- `ilustrasi.py` membuat SVG 800×500 untuk setiap entri `auto: true`, dengan warna dari `site.json → ilustrasi_warna`. Jenis komponen: `timeline`, `bars`, `grouped`, `gallery`, `tasklist`, `table`, `chat`, `doc`, `dialog`, `steps`, `cards`, `map`, `compare`, `venn`, `shield`, `brand`, `tiers`. Lihat `references/contoh-ilustrasi-timebase.json` untuk contoh tiap jenis.
- Di konten: `{{gambar:<id>}}` diletakkan **setelah paragraf pertama** di bawah H2 section-nya. Gambar hero dirender otomatis di kolom kanan hero (dua kolom ≥900px, menumpuk di mobile).
- `build.py` menulis `docs/daftar-ilustrasi.md` (halaman, section, id, status, ukuran, brief). Berikan daftar ini ke user sebagai panduan gambar yang perlu dikirim.

## Wajib (dicek build)

| Aturan | Level |
|---|---|
| Minimal `min_per_halaman` (default 3) gambar per halaman, termasuk hero | ERROR |
| Setiap gambar punya `alt` deskriptif. Alt ilustrasi UI diawali "Ilustrasi …". Keyword halaman masuk alami di alt gambar hero | ERROR (kosong) · WARNING (>125 karakter) |
| Token `{{gambar:id}}` harus ada di data, dan file-nya harus ada | ERROR |
| Gambar asli user: WebP/AVIF (atau SVG), `w` & `h` diisi ukuran asli, ≤200 KB | ERROR |
| Halaman tanpa gambar hero | WARNING |
| Gambar di data tapi tidak dipakai | WARNING |

## SEO & PageSpeed

- `<img>` selalu dengan `width`/`height` (CSS `height:auto`) sehingga CLS 0. Gambar hero `loading="eager" fetchpriority="high"`, sisanya `loading="lazy" decoding="async"`. Gambar hero biasanya jadi elemen LCP, jadi jaga tetap kecil (SVG ≤10 KB, foto WebP ≤120 KB).
- `<figure>` + `<figcaption>` memberi konteks tambahan untuk mesin pencari. Caption ilustrasi UI menyebut "Ilustrasi" agar tidak terbaca sebagai screenshot asli.
- **og:image** 1200×630 PNG/JPG (SVG tidak didukung WhatsApp/sosmed): `python3 tools/og_image.py` membuatnya dari brand, tagline, dan deskripsi (macOS: qlmanage + sips). Isi `site.json → og_image`. Meta `og:image` + `twitter:card` muncul saat `site_url` terisi.
- Jangan memasukkan logo merek pihak lain atau logo lembaga pemerintah di ilustrasi.

## Foto testimoni
- Setiap testimoni menampilkan foto bulat 48px. Sumbernya **hanya** foto asli pemberi testimoni dengan izin tertulis (persegi ±160×160, WebP/AVIF ≤40 KB, di `static/testimoni/`, diisi di `data/social-proof.json → foto`).
- Sebelum ada foto asli, tampil avatar inisial (gradasi brand). Jangan memakai foto stok atau wajah buatan AI: itu membuat testimoni terlihat asli padahal tidak.
- `build.py` menambahkan tabel "Foto testimoni" ke `docs/daftar-ilustrasi.md`, memberi ERROR bila file foto tidak ada atau bukan WebP/AVIF ≤40 KB, dan WARNING bila testimoni asli belum berfoto.

## Mengganti dengan gambar asli user

1. Terima gambar, lalu kompres/konversi ke WebP atau AVIF dengan lebar ≤1600 px dan rasio sesuai brief (default 16:10). macOS tidak punya encoder WebP bawaan: pakai `cwebp` (`brew install webp`, minta izin user dulu) atau minta user mengekspor WebP dari tool desainnya.
2. Simpan ke `static/ilustrasi/<id>.webp`, lalu di entri isi `"file": "static/ilustrasi/<id>.webp"`, `"w"`, `"h"` (ukuran asli), dan `"auto": false`.
3. Perbarui `alt` dan `caption` bila isi gambar berubah (mis. kata "Ilustrasi" dihapus kalau gambarnya screenshot asli).
4. `python3 build.py`, lalu cek tampilan.
