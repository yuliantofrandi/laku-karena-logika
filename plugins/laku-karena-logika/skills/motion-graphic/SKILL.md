---
name: motion-graphic
description: Membuat video motion graphic MP4 dari aplikasi/software SaaS pengguna — menjelajahi aplikasi aslinya lewat browser, lalu merekreasi tampilannya dengan data dummy dan merender SATU video MP4 kecil bernama berkata kunci yang siap dipasang di website dan lolos PageSpeed. Tiga gaya — Style 1 promo fitur 9:16 (headline per fitur), Style 2 walkthrough layar 16:9 (klik antar menu, tanpa teks promosi), Style 3 walkthrough layar 9:16 (kamera pan mengikuti klik). Gunakan saat pengguna berkata "buat motion graphic", "video demo aplikasi", "video fitur software saya", "walkthrough aplikasi", "video untuk landing page/website", "video yang lolos PageSpeed", "video produk untuk calon pembeli", atau "motion graphic style 1/2/3".
---

# Motion Graphic – Video Produk SaaS

Ubah aplikasi web milik pengguna menjadi **satu** video MP4 untuk dipasang di website: file kecil (≤ 3 MB) agar lolos PageSpeed, dengan nama file berkata kunci untuk SEO. Tidak ada file ekspor lain. Video TIDAK merekam layar asli: tampilan direkreasi dalam HTML yang dianimasikan secara deterministik, lalu dirender frame-per-frame. Hasilnya tajam, bisa direvisi, dan aman dibagikan.

Urutan WAJIB: cek alat → pilih gaya → jelajahi aplikasi → storyboard (setujui) → bangun HTML → cek snapshot → render bahan → MP4 web berkata kunci + uji PageSpeed → serahkan satu MP4.

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

**Folder output** tidak di-hardcode: pakai folder yang disebut pengguna;
kalau belum disebut, pakai `motion-graphic/<produk>/` di working directory
sesi ini. Di bawah, folder ini ditulis `<output>`. Skrip dipanggil dari
folder skill ini, ditulis `<folder skill ini>`.

## 1. Pilih gaya (tanyakan setiap kali)

Tanyakan dengan AskUserQuestion, sekalian tanyakan produk/URL aplikasinya bila belum jelas:

| Style | Format | Isi | Cocok untuk |
|---|---|---|---|
| **Style 1 – Promo fitur** | 9:16, 1080×1920, ±25–30 dtk | Hook pembuka → 3–5 scene fitur (kicker "01 · FITUR" + headline besar + mockup UI beranimasi) → outro logo + chip fitur + CTA domain | Reels/TikTok, hero section mobile, iklan |
| **Style 2 – Walkthrough 16:9** | 1920×1080, ±45–60 dtk | Hanya layar aplikasi (sidebar, topbar, halaman) + kursor yang mengklik antar menu + kamera zoom ke area penting; tanpa teks promosi; kartu penutup logo + domain | Landing page, halaman fitur, YouTube, demo ke calon pembeli |
| **Style 3 – Walkthrough 9:16** | 1080×1920, ±45–60 dtk | Alur klik sama dengan Style 2, layar dalam jendela berbingkai yang di-zoom ±1,3× dan di-pan mengikuti kursor; header logo + pill nama menu, indikator progres + domain di bawah | Reels/TikTok/Shorts, versi mobile landing page |

Style 2 dan 3 bisa dibuat sekaligus dari satu rekreasi (Style 3 = Style 2 + kamera vertikal).

Detail visual, struktur scene, dan parameter kamera tiap gaya ada di `references/gaya.md`.

## 2. Jelajahi aplikasi

- Pakai Claude in Chrome di tab aplikasi pengguna: screenshot setiap menu, tab, dan detail penting (klik kartu → halaman detail, tab di dalamnya, pengaturan). Klik hanya untuk melihat — jangan menyimpan, menghapus, atau mengubah data.
- Ambil token visual dengan `javascript_tool`: font (`getComputedStyle(document.body).fontFamily`), warna primer menu aktif, warna teks. Logo: unduh bila bisa; bila diblokir (proxy/CORS), rekreasi sebagai teks bergradasi/warna sesuai logo asli dan beri tahu pengguna.
- Catat daftar menu + 1 hal paling menjual di tiap layar. Kembalikan tab pengguna ke halaman awal setelah selesai.

## 3. Storyboard (tampilkan di chat, tunggu persetujuan)

Tabel per scene/halaman: detik mulai–selesai, layar, aksi kursor/animasi, fokus kamera (Style 2/3) atau headline (Style 1). Untuk Style 1 tulis headline dalam bahasa manfaat ("Pantau aktivitas seluruh tim dalam satu layar"), bukan nama menu.

Aturan konten (jelaskan di storyboard):
- **Data dummy**: nama karyawan/pelanggan, foto, isi screenshot, nama perusahaan tenant, dan akun login diganti fiktif (inisial berwarna sebagai avatar). Jangan pernah menampilkan data asli tanpa izin eksplisit.
- Label yang menyebut sistem internal/klien (mis. nama HRIS internal) diganti istilah umum; sebutkan perubahan ini ke pengguna.
- Tanpa klaim angka karangan di teks promosi; angka di dalam UI dummy boleh.
- Klaim fitur hanya yang benar-benar terlihat di aplikasi atau dinyatakan pengguna.

## 4. Bangun HTML

Mulai dari template di `assets/` (contoh nyata dari produk Timebase) — salin, lalu ganti isi:
- `assets/style1-promo-fitur-9x16.html`
- `assets/style2-walkthrough-16x9.html`
- `assets/style3-walkthrough-9x16.html`

Kontrak mesin animasi, cara menambah halaman/klik/kamera, dan jebakan yang sudah ditemui ada di `references/mesin-animasi.md`. Wajib baca sebelum mengedit template.

## 5. Cek lalu render

1. Ambil snapshot beberapa detik kunci (tiap scene) dan lihat sebagai contact sheet:
   `python3 <folder skill ini>/scripts/render.py video.html <output>/.kerja/cek --size 1080x1920 --snap 2,6.5,12,17`
   Periksa: elemen terpotong/overflow, kartu kosong, kamera keluar area, kursor di target saat klik, teks terbaca di ukuran HP.
2. Perbaiki, lalu render **bahan** resolusi penuh (≈2 dtk proses per 1 dtk video) ke folder kerja sementara — ini bukan hasil ekspor:
   `python3 <folder skill ini>/scripts/render.py video.html <output>/.kerja/bahan --size 1920x1080`
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
- Ringkas: durasi & format, urutan scene/klik, data apa yang di-dummy-kan, label yang diubah, batasan (tanpa audio, logo rekreasi bila ada).
- Laporkan hasil Lighthouse (skor mobile & desktop, LCP, CLS, TBT, berat awal halaman) dan hal yang menjadi tanggung jawab server (cache, kompresi) dari `references/website-seo.md`, plus usulan penempatan video di halaman.
- Revisi = edit HTML lalu render ulang; jangan bangun dari nol.
