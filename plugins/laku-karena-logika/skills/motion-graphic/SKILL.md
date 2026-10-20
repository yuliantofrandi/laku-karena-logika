---
name: motion-graphic
description: Membuat video motion graphic MP4 dari aplikasi/software SaaS pengguna — memakai SCREENSHOT ASLI dari layar browser pengguna (nama & jabatan diganti dummy, 4 digit akhir nomor telepon di-blur, foto profil tetap), lalu menganimasikannya dengan kursor, klik, dan zoom kamera, dan merender SATU video MP4 kecil bernama berkata kunci yang siap dipasang di website dan lolos PageSpeed. Tiga gaya — Style 1 promo fitur 9:16 (headline per fitur), Style 2 walkthrough layar 16:9 (klik antar menu, tanpa teks promosi), Style 3 walkthrough layar 9:16 (kamera pan mengikuti klik). Gunakan saat pengguna berkata "buat motion graphic", "video demo aplikasi", "video fitur software saya", "walkthrough aplikasi", "video untuk landing page/website", "video yang lolos PageSpeed", "video produk untuk calon pembeli", atau "motion graphic style 1/2/3".
---

# Motion Graphic – Video Produk SaaS

Ubah aplikasi web milik pengguna menjadi **satu** video MP4 untuk dipasang di website: file kecil (≤ 3 MB) agar lolos PageSpeed, dengan nama file berkata kunci untuk SEO. Tidak ada file ekspor lain. Bahan video adalah **screenshot asli** dari layar browser pengguna — setelah data pribadi disamarkan sesuai aturan privasi di bawah — yang lalu dianimasikan (kursor, klik, zoom/pan kamera, headline) dalam HTML deterministik dan dirender frame-per-frame. Hasilnya tajam, bisa direvisi, dan aman dibagikan.

Urutan WAJIB: cek alat → pilih gaya → jelajahi aplikasi → storyboard (setujui) → samarkan + tangkap screenshot asli → susun HTML → cek snapshot → render bahan → MP4 web berkata kunci + uji PageSpeed → serahkan satu MP4.

Video utamanya dipakai di website SEO: hasil akhir HARUS lolos PageSpeed (Performance ≥ 90 mobile & desktop, CLS 0). Jangan pernah menyerahkan embed `<video autoplay src=...>` mentah.

## 0. Cek alat & folder output

Skill ini merender di komputer pengguna. Sebelum mulai, cek alat yang
dibutuhkan:

```bash
command -v ffmpeg ffprobe node; python3 -c "import playwright, PIL; print('python ok')"; command -v lighthouse
```

Kalau ada yang belum terpasang, sebutkan yang kurang dan **minta izin
pengguna** sebelum memasang. Perintah pasang (macOS dengan Homebrew;
sesuaikan untuk OS lain):

```bash
brew install ffmpeg
python3 -m pip install playwright pillow
python3 -m playwright install chromium
npm i -g lighthouse@12
```

Screenshot ditangkap dengan `screencapture` bawaan **macOS**: aplikasi Claude/terminal perlu izin
*System Settings → Privacy & Security → Screen Recording*. Kalau belum diizinkan, minta pengguna
mengaktifkannya (Claude tidak boleh mengubah setelan ini sendiri).

**Folder output** tidak di-hardcode: pakai folder yang disebut pengguna;
kalau belum disebut, pakai `motion-graphic/<produk>/` di working directory
sesi ini. Di bawah, folder ini ditulis `<output>`. Skrip dipanggil dari
folder skill ini, ditulis `<folder skill ini>`.

## 1. Pilih gaya (tanyakan setiap kali)

Tanyakan dengan AskUserQuestion, sekalian tanyakan produk/URL aplikasinya bila belum jelas:

| Style | Format | Isi | Cocok untuk |
|---|---|---|---|
| **Style 1 – Promo fitur** | 9:16, 1080×1920, ±25–30 dtk | Hook pembuka → 3–5 scene fitur (kicker "01 · FITUR" + headline besar + screenshot asli di kartu, di-zoom ke bagian yang dibahas) → outro logo + tagline + CTA domain | Hero section mobile, section fitur |
| **Style 2 – Walkthrough 16:9** | 1920×1080, ±45–60 dtk | Screenshot asli layar demi layar + kursor yang mengklik antar menu + kamera zoom ke area penting; tanpa teks promosi; kartu penutup logo + domain | Landing page, halaman fitur, demo ke calon pembeli |
| **Style 3 – Walkthrough 9:16** | 1080×1920, ±45–60 dtk | Alur klik sama dengan Style 2, screenshot dalam jendela berbingkai yang di-zoom ±1,3× dan di-pan mengikuti kursor; header logo + pill nama menu, indikator progres + domain di bawah | Versi mobile landing page |

Ketiga gaya memakai satu template (`assets/video-screenshot.html`, ganti `GAYA`) dan bisa memakai set screenshot yang sama.

Detail visual, struktur scene, dan parameter kamera tiap gaya ada di `references/gaya.md`.

## 2. Jelajahi aplikasi

- Pakai Claude in Chrome di tab aplikasi pengguna: lihat setiap menu, tab, dan detail penting (klik kartu → halaman detail, tab di dalamnya, pengaturan). Klik hanya untuk melihat — jangan menyimpan, menghapus, atau mengubah data.
- Ambil warna primer menu aktif dengan `javascript_tool` (untuk aksen headline, kursor, kartu penutup).
- Catat daftar layar yang akan masuk video + 1 hal paling menjual di tiap layar, dan kumpulkan **semua nama orang dan nama jabatan** yang terlihat (pakai `get_page_text`) untuk peta penyamaran.

## 3. Storyboard (tampilkan di chat, tunggu persetujuan)

Tabel per scene/halaman: detik mulai–selesai, layar, aksi kursor/animasi, fokus kamera (Style 2/3) atau headline (Style 1). Untuk Style 1 tulis headline dalam bahasa manfaat ("Pantau aktivitas seluruh tim dalam satu layar"), bukan nama menu.

Sertakan di storyboard **peta penyamaran**: tiap nama orang → nama dummy, tiap jabatan → jabatan dummy (dummy yang wajar dan konsisten — nama yang sama selalu jadi dummy yang sama di semua layar).

Aturan privasi (WAJIB, ketetapan pengguna):

| Data di layar | Perlakuan |
|---|---|
| Foto profil | **Tetap** — tidak diubah, tidak di-blur |
| Nama jabatan | Diganti **jabatan dummy** |
| Data berisi nama (orang) | Diganti **nama dummy** |
| Nomor telepon | **4 digit terakhir di-blur** |

Data sensitif lain yang tidak diatur tabel ini (mis. email, alamat, NIK, nama perusahaan klien) — tanyakan ke pengguna sebelum screenshot diambil. Teks promosi tanpa klaim angka karangan; klaim fitur hanya yang benar-benar terlihat di aplikasi atau dinyatakan pengguna.

## 4. Samarkan lalu tangkap screenshot asli

Untuk tiap layar di storyboard, di tab aplikasi pengguna:
1. Siapkan tampilan: zoom browser 100%, tidak ada popup/devtools, lebar jendela sama untuk semua layar (pakai `resize_window` Claude in Chrome bila perlu, mis. 1440×900 untuk 16:9).
2. Samarkan: jalankan isi `scripts/privasi.js` lalu `samarkan({...peta penyamaran...})` lewat `javascript_tool`. Fungsi ini mengganti nama & jabatan sesuai peta, mem-blur 4 digit terakhir semua nomor telepon, dan tidak menyentuh gambar (foto profil tetap). Perubahan hanya di DOM tab — tidak tersimpan ke server.
3. Catat posisi target klik untuk animasi kursor: `getBoundingClientRect()` elemen yang akan diklik (tengah elemen, px CSS halaman).
4. Ambil posisi area halaman di layar, lalu tangkap:
   `({x: screenX, y: screenY + (outerHeight - innerHeight), w: innerWidth, h: innerHeight})` →
   `bash <folder skill ini>/scripts/tangkap_layar.sh <output>/sumber/shots/01.png <x> <y> <w> <h>`
5. **Periksa PNG-nya** (baca gambarnya): tidak boleh ada nama/jabatan asli yang tertinggal (mis. di dalam gambar, grafik canvas, atau inisial avatar) dan 4 digit akhir semua nomor harus ter-blur. Kalau ada yang lolos, tambahkan ke peta dan ulangi.
6. Pindah layar lewat klik menu biasa (bukan menyimpan data), ulangi 2–5 — navigasi memuat ulang DOM, jadi penyamaran harus dijalankan lagi di tiap layar.

Selesai: muat ulang tab agar tampilan asli kembali dan kembalikan ke halaman awal. Peta penyamaran berisi nama asli — simpan hanya di percakapan, jangan ditulis ke file.

## 4b. Susun HTML

Salin `assets/video-screenshot.html` ke `<output>/sumber/video.html` (screenshot di `<output>/sumber/shots/`), lalu isi blok "ISI VIDEO": `GAYA`, `CFG` (`shotW` = `innerWidth` saat screenshot), `SHOTS`, `MOVES` (koordinat dari langkah 4.3), `CLICKS`, `CAM`, dan untuk Style 1 `CAPS` + `INTRO`.

Kontrak template, pola kamera tiap gaya, dan jebakan yang sudah ditemui ada di `references/mesin-animasi.md` dan `references/gaya.md`. Wajib baca sebelum mengisi.

## 5. Cek lalu render

1. Ambil snapshot beberapa detik kunci (tiap scene) dan lihat sebagai contact sheet:
   `python3 <folder skill ini>/scripts/render.py <output>/sumber/video.html <output>/.kerja/cek --size 1080x1920 --snap 2,6.5,12,17`
   Periksa: kamera keluar area/menampilkan ruang kosong, kursor tepat di target saat klik, teks screenshot terbaca di ukuran HP, tidak ada data asli yang lolos penyamaran.
2. Perbaiki, lalu render **bahan** resolusi penuh (≈2 dtk proses per 1 dtk video) ke folder kerja sementara — ini bukan hasil ekspor:
   `python3 <folder skill ini>/scripts/render.py <output>/sumber/video.html <output>/.kerja/bahan --size 1920x1080` (Style 1/3: `--size 1080x1920`)
3. Ekstrak 3–4 frame dari MP4 bahan dengan ffmpeg untuk verifikasi visual.

## 5b. Satu MP4 web berkata kunci + uji PageSpeed

Ekspor HANYA **satu** file MP4 untuk website — tanpa master 1080p, WebM, teaser, atau file gambar terpisah.

1. **Nama file berkata kunci (wajib).** Slug = keyword utama halaman tempat video dipasang + kata "demo"/"video", huruf kecil, dipisah tanda hubung, tanpa nama style/versi, maks ±6 kata — mis. `aplikasi-absensi-karyawan-whatsapp-demo`. Ambil keyword dari keyword plan/page brief skill `keyword-research` bila ada; kalau tidak ada, pilih keyword beli paling relevan dari produk dan sebutkan ke pengguna.
2. Buat MP4 web dari bahan:
   `python3 <folder skill ini>/scripts/web_optimize.py <output>/.kerja/bahan.mp4 <output> <slug> --poster <detik> --title "..." --desc "..." --domain https://<domain>`
   Hasil: satu `<slug>.mp4` 720p/24 fps/H.264/tanpa audio (≤ 3 MB, kompresi dinaikkan otomatis bila lewat). Snippet embed dicetak ke layar: `<video preload="none">` + tombol putar + poster frame pratinjau yang ditanam sebagai data URI (±35 KB, tanpa file gambar) + JSON-LD VideoObject. Pilih detik poster yang menampilkan layar paling informatif (bukan saat transisi/zoom).
3. Uji di halaman contoh dengan Lighthouse mobile & desktop sesuai `references/website-seo.md`. Harus: Performance ≥ 90, SEO 100, CLS 0, TBT < 200 ms, dan 0 byte video terunduh sebelum klik.

Butuh: Python Playwright + Chromium, ffmpeg (libx264), Pillow, Node + `lighthouse` untuk uji (lihat langkah 0). Font fallback: Inter.

## 6. Serahkan

- Serahkan **satu** file: `<output>/<slug>.mp4`. Hapus folder `<output>/.kerja/` (bahan render & snapshot) setelah lolos uji. Tempel snippet embed sebagai blok kode di chat (bukan file). HTML sumber disimpan di `<output>/sumber/` untuk revisi — bukan hasil ekspor.
- Ringkas: durasi & format, urutan layar/klik, peta penyamaran yang dipakai (nama & jabatan → dummy, jumlah nomor yang di-blur), batasan (tanpa audio).
- Laporkan hasil Lighthouse (skor mobile & desktop, LCP, CLS, TBT, berat awal halaman) dan hal yang menjadi tanggung jawab server (cache, kompresi) dari `references/website-seo.md`, plus usulan penempatan video di halaman.
- Revisi = edit HTML (atau ganti screenshot tertentu) lalu render ulang; jangan bangun dari nol.
