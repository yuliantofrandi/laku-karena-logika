# Referensi teknis – Ekspor & Posting

## Membaca kanvas

- `Artifact` action `read` pada link kanvas dengan `paths`: `project/canvas.json` dan setiap `project/<Nama>.dc.html`.
- Aset `/_blob/<id>` (logo, pola latar) diunduh dengan `Artifact` read `path: "<id>"` (satu per panggilan).
- Aset Venturo yang sudah dikenal: pola latar `b120523b5d2d48dc25a92beb1d3b8e49` (jpg), logo `03ea41e2dbe15f069fc52835ab9bcbc0` (png). ID bisa berbeda di kanvas lain — ambil dari HTML.

## Render ke PNG/JPEG (Playwright di workspace cloud)

1. Ubah tiap `.dc.html` jadi HTML biasa: isi `<helmet>` → `<head>`, isi `<x-dc>` → `<body>`. Hapus `<script src="./support.js">` dan blok `data-dc-script` (frame statis tanpa `{{hole}}`). Ganti `/_blob/<id>` dengan path file lokal.
2. **Font:** Google Fonts diblokir proxy. Unduh via npm: `npm pack @fontsource/montserrat @fontsource/jetbrains-mono`, ekstrak, lalu tulis `@font-face` lokal untuk Montserrat 400/500/600/700/800 (normal+italic) dan JetBrains Mono 400/600 (subset `latin`, `.woff2`). Buang `<link>` Google Fonts.
3. Chromium: `launch(args=["--allow-file-access-from-files"])`, viewport 1080×1920, `device_scale_factor=1`, tunggu `networkidle` dan `document.fonts.ready`, screenshot `clip` 0,0,1080,1920.
4. Cek font termuat: `[...document.fonts].filter(f=>f.status=='loaded')` harus berisi Montserrat.
5. Konversi dengan Pillow: `convert('RGB').save(..., quality=95, subsampling=0)`; crop 4:5 = `crop((0,285,1080,1635))`.

## Menyimpan ke Drive lokal

- Minta akses folder `~/Library/CloudStorage` (sekali per sesi) lewat `device_request_folder_access`.
- Tulis file dengan `device_commit_files` (`stagedPath` di `/mnt/user-data/outputs/...`).
- Membaca file Drive lokal kadang gagal "Resource deadlock avoided" — pakai `device_stage_files` sebagai gantinya.
- Rename/pindah pakai `mv -n` lewat `device_bash`.

## Link media untuk Metricool

- Setelah file tersinkron (tunggu ±30–60 detik), cari ID file dengan Google Drive `search_files` (`parentId = '<id folder>'`).
- Format media: `https://drive.google.com/uc?export=download&id=<FILE_ID>`. Syarat: folder berakses "Siapa saja yang memiliki link". Tool Drive tidak bisa mengubah akses ke publik — pengguna yang melakukannya.
- Metricool menyalin gambar ke `static.metricool.com/...`; URL salinan ini bisa dipakai ulang untuk posting berikutnya tanpa Drive publik.

## Metricool

- Brand: `venturo.pro`, `blogId` **7096352**, timezone `Asia/Jakarta`. Terhubung: TikTok, Instagram, Threads, YouTube (cek ulang dengan `getBrandSettings`).
- `date` dan `publicationDate` harus di masa depan (±3–5 menit dari sekarang).

Payload TikTok + Threads (9:16):

```json
{
  "autoPublish": true, "draft": false, "descendants": [], "firstCommentText": "",
  "hasNotReadNotes": false, "shortener": false, "smartLinkData": {"ids": []},
  "media": ["<6 url 9:16 berurutan>"], "mediaAltText": [],
  "providers": [{"network": "tiktok"}, {"network": "threads"}],
  "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Asia/Jakarta"},
  "text": "<caption>",
  "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": "<judul>",
                 "autoAddMusic": true, "photoCoverIndex": 0,
                 "disableComment": false, "disableDuet": false, "disableStitch": false,
                 "commercialContentThirdParty": false, "commercialContentOwnBrand": false},
  "threadsData": {}
}
```

Payload Instagram (4:5): sama, tetapi `media` versi 4:5, `providers: [{"network":"instagram"}]`, `instagramData: {"type":"POST","collaborators":[]}`, tanpa `tiktokData`/`threadsData`.

## Batasan yang sudah terbukti

| Hal | Aturan |
|---|---|
| Format TikTok | Hanya JPEG/WebP. PNG → error "image/png type is not allowed". |
| Feed Instagram | Maks 4:5. Gambar 9:16 tampil dengan bar kanan-kiri. |
| TikTok dengan 4:5 | Tampil dengan bar atas-bawah (tidak full layar). |
| Threads | Tidak memotong; 9:16 full layar saat dibuka. |
| Musik | Otomatis hanya TikTok (`autoAddMusic`). Carousel IG tidak bisa. Reel IG butuh video + `audioConfiguration.audioId` (kata kunci/ID katalog) dan akun IG Business terhubung Facebook Page; token IG kedaluwarsa → sambungkan ulang di Metricool. |
| Caption Threads | ≤ 500 karakter. |
| Integrasi Drive Metricool | Fitur premium — pakai link publik `uc?export=download`. |

## Reel Instagram (opsional)

Slideshow video dari frame 9:16 dengan ffmpeg (3,5 s per frame, transisi `xfade` slideleft 0,4 s, 30 fps, `yuv420p`, track audio senyap `anullsrc`). Kirim `instagramData.type: "REEL"` dengan `audioConfiguration: {"audioId": "<kata kunci>", "videoVolume": 0}`; bila kata kunci cocok banyak lagu, Metricool mengembalikan kandidat untuk dipilih.
