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

## Ilustrasi tidak boleh mengulang isi section
User: "yang ini kurang bagus, ilustrasi dengan isi kontennya sama" (ilustrasi 3 langkah di samping 3 kartu langkah yang sama). Ilustrasi harus **menambah informasi**: contoh data/layar produk (tabel catatan kerja, profil HRIS), percakapan, atau hasil — bukan daftar label yang sama dengan kartu/poin di sebelahnya.
- Section langkah/kartu yang sudah jelas → **tanpa gambar**; kartu tampil sebaris selebar kontainer (`split.stack`). Pastikan halaman tetap punya ≥3 gambar.
- Build memberi WARNING `ilustrasi '<id>' … mengulang N/M poin isi section` bila ≥2 label ilustrasi (dan ≥ separuhnya) tumpang tindih ≥60% kata dengan judul kartu/poin section.
- Kasus Timebase yang diperbaiki: langkah aktivasi (gambar dihapus), 4 data agen (→ tabel catatan kerja satu hari), alur white label (→ chat konsultasi), fitur HRIS (→ tabel profil karyawan).

## Video / motion graphic dari user
User bisa mengganti ilustrasi dengan motion graphic sendiri ("ganti dengan motion graphic saya"). Cara memasang:
1. Salin video ke `static/video/<nama>.mp4` (MP4 H.264 atau WebM, tanpa suara, ≤5 MB; build WARNING bila lebih). Bila lebih besar, kompres dengan `scripts/kompres_video.swift` (macOS, tanpa ffmpeg; preset `avconvert` justru memperbesar file). Hero 16:9 cukup 960×540 @ 500 kbps (demo 50 detik: 11,8 MB → 3,1 MB, teks UI tetap terbaca).
2. Ambil satu frame yang informatif (bukan frame awal yang masih fade-in) sebagai poster dengan `scripts/poster_video.swift`, lalu `sips -Z 960 -s format jpeg -s formatOptions 70` (±70 KB).
3. Di `data/ilustrasi.json` ubah entri gambarnya: `"auto": false, "video": "static/video/<nama>.mp4", "file": "<poster>", "w": <lebar asli>, "h": <tinggi asli>`; hapus `jenis`/`data`; perbarui `alt`, `caption`, `brief`.

Render: `<video muted loop playsinline preload="none" poster data-src>`. Skrip kecil (`VIDEO_JS`, hanya disisipkan di halaman yang punya video) menunggu event `load` (tidak bersaing dengan LCP), lalu memasang `src` saat video mendekati layar (IntersectionObserver) dan autoplay.

**Video di hero** (user: "ganti dengan ilustrasi saya" di hero): pasang di entri hero (`hero` map di ilustrasi.json) dengan cara yang sama. Poster hero otomatis di-`preload` dengan `fetchpriority="high"` karena menjadi kandidat LCP, dan video mendapat perlakuan visual yang sama dengan gambar hero (miring −3°, di atas bentuk gradasi). Bila pengguna memilih *reduced motion*, video tidak autoplay dan diberi kontrol. Video potret (9:16) dibatasi lebar 340 px (280 px di mobile) dengan bayangan lembut. Kasus Timebase: motion graphic 1080×1920, 27 detik, 3,9 MB di section "data kerja yang bisa dibaca bersama"; re-encode dengan `avconvert` justru memperbesar file, jadi file asli dipakai.

