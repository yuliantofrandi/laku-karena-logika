# Checklist Deployment — target hijau (90–100) di PageSpeed Insights

## Sudah ditangani oleh build (otomatis)
- [x] **Nol render-blocking:** CSS di-*minify* dan di-*inline* di `<head>`. Tidak ada file CSS eksternal, Google Fonts, atau JavaScript.
- [x] **Font sistem**, jadi tidak ada unduhan font, tidak ada FOIT/FOUT, dan tidak ada CLS dari font.
- [x] **LCP = teks H1** (tanpa gambar hero). Satu request HTML ±30–40 KB.
- [x] **CLS = 0** (terukur di preview). Logo SVG punya `width`/`height` eksplisit.
- [x] **Tanpa widget pihak ketiga.** Tombol beli adalah link biasa ke checkout; chat WA (opsional) link `wa.me` biasa, tanpa skrip.
- [x] Semantic HTML5: `header`, `nav`, `main`, `article`, `section`, `aside`, `figure`, `footer`, `details`.
- [x] Satu H1 per halaman, H2/H3 berurutan.
- [x] Title 40–60 karakter, meta description 120–155, H1 ≠ title. Dicek otomatis oleh build.
- [x] JSON-LD: `Organization`, `WebPage`, `BreadcrumbList`, `SoftwareApplication` + `Offer` (harga IDR), `FAQPage`; `AggregateRating` hanya dari ulasan asli.
- [x] Halaman hukum (mis. panduan UU PDP) `noindex` sampai direview ahli hukum.
- [x] Gambar: setiap `<img>` punya alt, width/height (CLS 0), hero `fetchpriority="high"`, sisanya `loading="lazy"`; ilustrasi SVG ≤10 KB; og:image 1200×630 PNG.
- [x] Mobile: tanpa scroll horizontal di 375px. Tombol WA melayang minimalis (latar `--ink`): desktop di kanan bawah; mobile hanya tombol WA ringkas (<3% layar) dengan judul + subjudul. SVG inline, tanpa skrip.

## Wajib sebelum publish (isi manual)
1. `site.json` → isi `site_url` (mis. `https://domain-anda.id`), **`checkout_url`** (link langganan/pembayaran, boleh memuat `{skema}` dan `{periode}`), **`signin_url`** (halaman login aplikasi untuk tombol Sign In), **`whatsapp`** (nomor WA marketing untuk tombol melayang), opsional `email`. Build publish ditolak kalau `checkout_url`, `signin_url`, atau `whatsapp` kosong.
2. `data/social-proof.json` → ganti semua entri **contoh** dengan data asli, lalu `"contoh": false`. Build publish **ditolak** selama masih ada data contoh.
3. Halaman hukum → review ahli hukum → ubah `legal_reviewed` jadi `true`.
4. Pastikan setiap fitur yang disebut di website sudah benar-benar tersedia (BKB adalah rancangan; website adalah janji ke pembeli).
5. Jalankan `python3 build.py`, harus berakhir dengan `OK`.

## Hosting: Cloudflare Pages + Functions (sama dengan website-service)
Blog & Panduan dirender Functions, jadi hosting statis biasa (Netlify/Vercel/cPanel) **tidak** cukup.
1. Push folder proyek ke repo GitHub (private). `dist/` boleh tidak di-commit; commit `data/lakukan-cache.json` sebagai cadangan bila API gagal saat build.
2. Cloudflare → Workers & Pages → Create → Pages → **Connect to Git** → pilih repo.
   - Root directory: `website` (folder yang berisi `build.py`, `functions/`, `wrangler.toml`).
   - Build command: `python3 build.py` · Output directory: `dist`. Build ERROR = deploy dibatalkan (gerbang kualitas otomatis).
3. Setiap `git push` ke `main` → build + deploy otomatis ±1 menit. Branch lain mendapat URL preview.
4. Custom domain: apex + `www` (CNAME proxied), Redirect Rule `www` → apex 301.
- `build.py` menulis `slug.html`: Cloudflare Pages menyajikannya di `/slug` **tanpa redirect** (folder `slug/index.html` akan dialihkan 308 ke `/slug/`). Cek `curl -I https://domain/slug` → `200`.
- `build.py` juga menulis `_routes.json` (Functions tidak dipanggil untuk `/static/*`), `_headers`, `_redirects` (URL lama "(SEO saja)" → `/blog/<slug>` 301), dan `robots.txt`. `404.html` dipakai Pages dan Functions.
- Artikel CMS tampil ≤ 10 menit (cache edge Functions). Perubahan CSS/menu baru tampil di Blog/Panduan setelah deploy berikutnya (kunci cache memuat id build).
- Paksa **HTTPS** dan pilih satu versi domain (www atau tanpa www) dengan redirect 301.

## Header cache (`_headers` dibuat otomatis oleh build; contoh isinya)
```
/*
  Cache-Control: public, max-age=0, must-revalidate
/static/*
  Cache-Control: public, max-age=31536000, immutable
```

## Kalau nanti menambah aset
- **Gambar:** pakai AVIF/WebP via `<picture>`, isi `width` + `height`, beri `loading="lazy"` + `decoding="async"` untuk yang di bawah lipatan. Gambar di atas lipatan **jangan** lazy, sebaliknya beri `fetchpriority="high"`.
- **Logo klien:** SVG inline atau WebP ≤10 KB per logo.
- **Analytics:** muat setelah interaksi pertama atau `requestIdleCallback`. Jangan taruh di `<head>`. Tag Google Ads conversion juga dimuat tertunda, dan pastikan konversi (klik WA/form) tetap terekam.
- **Chat widget WhatsApp pihak ketiga:** jangan. Pertahankan link `wa.me` biasa.
- **Font kustom:** self-host WOFF2, subset latin, `font-display: swap`, `<link rel="preload">` hanya untuk 1 bobot.

## Verifikasi setelah live
1. https://pagespeed.web.dev → uji `/` dan halaman Prioritas 1, **Mobile dan Desktop**, target ≥90 di keempat kategori.
2. Google Search Console → submit `sitemap.xml`, minta indexing halaman Prioritas 1.
3. https://search.google.com/test/rich-results → cek `SoftwareApplication`, `FAQPage`, `BreadcrumbList`.
4. Uji semua tombol beli di HP: `Pilih <Nama Paket>` dan `Bayar tahunan` membuka checkout dengan skema & periode yang benar, sampai akun aktif setelah bayar.
5. Google Ads: pasang konversi pada **pembayaran berhasil** (dan klik tombol beli sebagai konversi sekunder) **sebelum** iklan jalan.
- [ ] **Dokumen legal**: isi `content/kebijakan-privasi.html` dan `content/syarat-layanan.html` (dari user/ahli hukum) sebelum iklan Google Ads jalan; selama kosong, halamannya placeholder noindex.
