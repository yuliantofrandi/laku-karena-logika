# Video untuk website SEO — hanya MP4, wajib lolos PageSpeed

Hasil ekspor HANYA file MP4 (tanpa WebM, teaser, atau file gambar). Target: Lighthouse/PageSpeed **Performance ≥ 90 (mobile & desktop), SEO 100, CLS 0, TBT < 200 ms**.

## Cara kerjanya (otomatis oleh `scripts/web_optimize.py`)
1. **MP4 web**: 1280×720 (16:9) atau 720×1280 (9:16), 24 fps, H.264 High, tanpa audio, `+faststart`, ≤ 3 MB (CRF dinaikkan otomatis bila lewat). H.264 dipilih karena didecode hardware di semua browser/HP.
2. **`preload="none"`**: browser tidak mengunduh satu byte video pun sampai pengunjung klik tombol putar → berat awal halaman tetap ±35–40 KB.
3. **Poster ditanam sebagai data URI WebP (≤ 35 KB)** di atribut `poster` — pratinjau langsung tampil (jadi elemen LCP) tanpa file gambar terpisah.
4. **Ruang dikunci** dengan `aspect-ratio` + `width/height` → CLS 0.
5. JSON-LD `VideoObject` disertakan.

Catatan teruji: `preload="metadata"` + `#t=` (ambil frame dari MP4) TIDAK dipakai — Chromium tetap mengunduh hampir seluruh video sebelum diklik.

## Perintah
```bash
python3 <folder skill ini>/scripts/web_optimize.py \
  <output>/<produk>-style2.mp4 <output>/web <slug-berkata-kunci> \
  --poster 6.8 --title "Demo aplikasi <Produk>: <manfaat utama>" \
  --desc "<1–2 kalimat berisi keyword utama dan fitur yang tampil>" --domain https://<domain> --path /media/
```
Snippet embed dicetak di akhir output — tempelkan ke chat sebagai blok kode untuk pengguna. Isi `uploadDate` sebelum dipasang.

## Verifikasi (wajib sebelum menyerahkan)
- Sajikan halaman uji (H1, paragraf, CTA, snippet) dengan server yang mendukung HTTP Range, lalu jalankan Lighthouse:
```bash
npm i -g lighthouse@12   # sekali
# Chromium bawaan Playwright — path-nya dideteksi otomatis (macOS/Linux/Windows)
CHROME_PATH=$(python3 -c "from playwright.sync_api import sync_playwright as s; p=s().start(); print(p.chromium.executable_path); p.stop()") \
lighthouse http://localhost:8767/uji.html --quiet --chrome-flags="--headless=new --no-sandbox" \
  --only-categories=performance,seo,accessibility,best-practices [--preset=desktop] --output=json --output-path=lh.json
```
- Chromium bawaan Playwright tidak bisa memutar H.264; untuk menguji klik-putar & jumlah byte sebelum klik, buat salinan WebM sementara khusus pengujian (jangan diserahkan).
- Laporkan skor mobile & desktop, LCP, CLS, TBT, total byte. Acuan Timebase: Performance 100 (mobile & desktop, 3× uji), SEO/Accessibility/Best Practices 100, LCP 0,8 dtk mobile, TBT 0 ms, CLS 0, berat awal 36–38 KB, 0 KB video sebelum klik.
- Sarankan pengguna mengecek ulang di PageSpeed Insights setelah halaman live.

## Batasan yang perlu disampaikan
- **Rich result video Google** mewajibkan `thumbnailUrl` berupa URL gambar. Karena ekspor hanya MP4, isi `thumbnailUrl` dengan URL gambar yang sudah ada di website (mis. og:image halaman), atau biarkan — video tetap tampil & halaman tetap lolos PageSpeed, hanya tidak memenuhi syarat rich result video.
- Pengaturan server: `Cache-Control: public, max-age=31536000, immutable` untuk `/media/*`, kompresi Brotli/gzip untuk HTML, dukungan HTTP Range (default di Nginx/Apache/CDN).

## Penempatan & SEO konten
- Style 2 (16:9): hero/section "Lihat cara kerjanya" di desktop. Style 3 (9:16): versi mobile. Style 1: section fitur, iklan, sosmed.
- Satu video utama per halaman; nama file berkata kunci (`aplikasi-monitoring-karyawan-wfa-demo.mp4`).
- Tulis ringkasan alur video sebagai teks di bawahnya (H2 "Cara kerjanya" + paragraf).
