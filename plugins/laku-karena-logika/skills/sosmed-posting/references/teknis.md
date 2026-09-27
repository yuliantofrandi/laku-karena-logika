# Referensi teknis – Ekspor & Posting

## Membaca kanvas

- `Artifact` action `read` pada link kanvas dengan `paths`: `project/canvas.json` dan `project/<Nama>.dc.html` artboard yang dipilih — satu panggilan, `out_dir` ke folder scratch. Folder itu yang dipakai sebagai `--src` untuk `render.py`.
- Logo & pola latar Venturo TIDAK perlu diunduh: `render.py` otomatis mengganti `<img alt="Venturo…">` dengan `assets/logo-venturo.png` dan `url(/_blob/…)` di `.bgpat` dengan `assets/background-venturo.jpg`.
- Aset lain (foto, ilustrasi upload): `Artifact` read `path: "<id>"`, lalu `--blob <id>=<path>`.

## render.py (di `scripts/`)

- Mengubah `.dc.html` jadi HTML biasa (isi `<helmet>` → `<head>`, isi `<x-dc>` → `<body>`, buang skrip DC dan link Google Fonts), memasang `@font-face` lokal dari `assets/fonts` (Montserrat 400–800 normal+italic, JetBrains Mono 400/600, subset latin; lisensi OFL disertakan).
- Chromium Playwright (`/opt/pw-browsers/chromium` bila ada), viewport 1080×1920, tunggu `networkidle` + `document.fonts.ready`.
- Simpan JPEG kualitas 95 (`subsampling=0`), crop 4:5 = `(0, 285, 1080, 1635)`, lembar kontak `contact.png`.
- Memeriksa tiap frame: batas konten (mengabaikan lapisan latar dan isi yang terpotong `overflow:hidden`) harus di dalam y 285–1635, dan Montserrat termuat. Exit code 0 = OK, 2 = ada masalah.
- Waktu: ±7 detik untuk 6 frame.

## Menyimpan ke Drive lokal

- Temukan folder Google Drive lokal dengan `get_device_info` / `device_list_dir` (Google Drive for desktop menaruhnya di folder CloudStorage pengguna), minta akses sekali per sesi lewat `device_request_folder_access`. Tanyakan bila ada lebih dari satu akun Drive.
- Tulis semua file dalam SATU `device_commit_files` (`stagedPath` di folder output sesi).
- Membaca file Drive lokal kadang gagal "Resource deadlock avoided" — pakai `device_stage_files`.
- Upload langsung lewat konektor Drive (`create_file` + base64) secara teknis mungkin, tetapi tiap JPEG ±300 KB harus dikirim sebagai teks base64 dalam argumen tool — jauh lebih lambat dan boros daripada sinkron lokal. Tetap pakai sinkron lokal.

## Link media untuk Metricool

- Setelah tersinkron (±30–60 detik), cari ID dengan Google Drive `search_files` (`parentId = '<id subfolder>'`; bisa `parentId = 'A' or parentId = 'B'`).
- Format media: `https://drive.google.com/uc?export=download&id=<FILE_ID>`. Folder induk `Sosmed` sudah publik permanen, jadi subfolder baru otomatis bisa diakses.
- Metricool menyalin gambar ke `static.metricool.com/...`; URL itu bisa dipakai ulang untuk posting ulang tanpa Drive.

## Metricool

- Brand: ambil `blogId` dan `timezone` dari `getBrandSettings` (tanyakan bila ada lebih dari satu brand). Pastikan TikTok, Instagram, Threads terhubung.
- `date` dan `publicationDate` harus di masa depan (±3 menit).
- Kirim tiga `createScheduledPost` dalam satu giliran (paralel).

Kerangka payload (isi `providers`, `text`, dan data jaringan per posting):

```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<url berurutan>"], "mediaAltText": [],
  "providers": [{"network": "tiktok"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Jakarta"},
  "text": "<caption>"
}
```

- TikTok: + `"tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": "<judul>", "autoAddMusic": true, "photoCoverIndex": 0, "disableComment": false, "disableDuet": false, "disableStitch": false, "commercialContentThirdParty": false, "commercialContentOwnBrand": false}`, media 9:16, caption satu paragraf.
- Threads: `providers: [{"network":"threads"}]`, + `"threadsData": {}`, media 9:16, caption ber-enter.
- Instagram: `providers: [{"network":"instagram"}]`, + `"instagramData": {"type":"POST","collaborators":[]}`, media 4:5, caption ber-enter.

## Cek status (hanya bila pengguna meminta)

`getScheduledPosts` rentang jam jadwal. Status: `PENDING` → `PUBLISHING` → `PUBLISHED` (TikTok bisa `AWAITING_CONFIRMATION`). `publicUrl` berisi link publik. `ERROR` → baca `detailedStatus`, perbaiki, kirim ulang platform itu saja.

## Batasan yang sudah terbukti

| Hal | Aturan |
|---|---|
| Format TikTok | Hanya JPEG/WebP. PNG → error "image/png type is not allowed". |
| Enter di caption TikTok | Dibuang oleh TikTok (posting foto via Metricool). Trik `⠀` gagal (jadi spasi). Pakai caption satu paragraf. |
| Feed Instagram | Maks 4:5. Gambar 9:16 tampil dengan bar kanan-kiri. |
| TikTok dengan 4:5 | Tampil dengan bar atas-bawah (tidak full layar). |
| Threads | Tidak memotong; 9:16 full layar saat dibuka. |
| Musik | Otomatis hanya TikTok (`autoAddMusic`). Carousel IG tidak bisa. Reel IG butuh video + `audioConfiguration.audioId` dan akun IG Business terhubung Facebook Page. |
| Caption Threads | ≤ 500 karakter. |
| Integrasi Drive Metricool | Fitur premium — pakai link publik `uc?export=download`. |
| Waktu tayang | Threads/IG beberapa menit setelah jadwal; TikTok bisa 10–15 menit. |

## Reel Instagram (opsional)

Slideshow video dari frame 9:16 dengan ffmpeg (3,5 s per frame, `xfade` slideleft 0,4 s, 30 fps, `yuv420p`, audio senyap `anullsrc`). Kirim `instagramData.type: "REEL"` dengan `audioConfiguration: {"audioId": "<kata kunci>", "videoVolume": 0}`; bila kata kunci cocok banyak lagu, Metricool mengembalikan kandidat.
