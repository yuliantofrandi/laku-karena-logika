# Arsitektur & Deploy

## Struktur proyek

```
<proyek>/
├── wrangler.toml            # name, pages_build_output_dir = "website", [vars] CMS_COMPANY_SLUG, CMS_CATEGORY
├── functions/               # Cloudflare Pages Functions (dibaca otomatis)
│   ├── _lib/cms.js          # fetch API publik Lakukan + cache edge
│   ├── _lib/render.js       # HTML portfolio (list, filter AI, detail), ASSET_VERSION
│   ├── _lib/render-blog.js  # HTML blog
│   ├── _lib/image-size.js   # tambah width/height ke <img> konten CMS (anti-CLS)
│   ├── portfolio/[[path]].js
│   ├── blog/[[path]].js
│   └── sitemap.xml.js       # halaman statis + semua artikel CMS
└── website/                 # output statis (tanpa build)
    ├── index.html, <slug-layanan>/index.html, ...
    ├── 404.html             # Pages otomatis menyajikan dengan status 404
    ├── _headers, _redirects, robots.txt, sitemap.xml (statis cadangan), llms.txt
    ├── _templates/portfolio.html   # kerangka yang diisi Functions (noindex)
    ├── favicon.ico, favicon-48/192/512.png, apple-touch-icon.png, site.webmanifest
    └── assets/css/style.css, assets/js/main.js, assets/fonts/, assets/img/
```

HTML biasa + CSS + vanilla JS. Header & footer ditulis ulang di setiap halaman, jadi perubahan menu harus diterapkan ke semua file (pakai script Python + regex, lalu verifikasi).

## Cache-busting

- CSS/JS dipanggil dengan `?v=<versi>` (contoh `style.css?v=20261021u`) dan di-cache 1 tahun (`immutable`).
- **Setiap ubah CSS/JS → naikkan `?v=` di semua HTML DAN `ASSET_VERSION` di `functions/_lib/render.js`.** Halaman CMS di-cache edge 600 detik dengan cache key yang memuat `ASSET_VERSION`; kalau tidak dinaikkan, halaman portfolio/blog tetap memanggil CSS lama.

## `_headers`

- Header keamanan global (nosniff, referrer-policy, X-Frame-Options SAMEORIGIN, permissions-policy).
- `/assets/css/*`, `/assets/js/*`, `/assets/fonts/*`: `max-age=31536000, immutable` (font + `Access-Control-Allow-Origin: *`).
- `/assets/img/*`: 30 hari + stale-while-revalidate.
- `/_templates/*` dan PDF company profile: `X-Robots-Tag: noindex, nofollow`. PDF boleh diakses lewat link langsung tapi tidak dipublikasikan/diindeks.

## `_redirects`

Halaman yang digabung → 301 (dengan dan tanpa garis miring):

```
/jasa-pembuatan-aplikasi-web /jasa-pembuatan-aplikasi/ 301
/jasa-pembuatan-aplikasi-web/ /jasa-pembuatan-aplikasi/ 301
```

Hapus juga halaman lama dari `sitemap.xml`, `llms.txt`, menu, footer, dan link internal.

## Uji lokal

```bash
npx wrangler@4 pages dev website
```

Halaman statis saja: `python3 -m http.server 8080 --directory website`. Kalau cache lokal Functions bikin bingung, hentikan server lalu hapus `.wrangler/state`.

## Deploy (Cloudflare Pages, direct upload)

```bash
npx wrangler@4 pages deploy --branch main
```

dijalankan dari root proyek (yang berisi `wrangler.toml`). Proyek pertama kali dibuat otomatis oleh perintah ini; hasilnya `<nama>.pages.dev`. **Minta izin pengguna sebelum deploy ke produksi.**

## Domain & DNS (Cloudflare)

1. Pages → proyek → Custom domains → tambah `domain.id` dan `www.domain.id`.
2. DNS: apex dan `www` CNAME ke `<nama>.pages.dev`, **proxied** (oranye). Jangan sentuh record MX/TXT email (misalnya Google Workspace).
3. **Redirect www → apex**: Rules → Redirect Rules, `hostname eq www.domain.id` → `https://domain.id${path}` 301, pertahankan query string. Uji: `curl -sI https://www.domain.id/x/` harus 301 ke apex.
4. Kalau website lama di cPanel: arahkan DNS ke Pages, bukan upload ke cPanel (Functions butuh Cloudflare).

## GA4 + Google Ads (ditunda demi PageSpeed)

Letakkan di `<head>` semua halaman (termasuk template portfolio & blog). Antrean `dataLayer` menyimpan event sebelum script dimuat:

```html
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-XXXX');gtag('config','AW-XXXX');(function(){var d=0;function l(){if(d)return;d=1;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-XXXX';document.head.appendChild(s);}['scroll','click','touchstart','keydown','mousemove'].forEach(function(e){addEventListener(e,l,{once:true,passive:true});});addEventListener('load',function(){setTimeout(l,3500);});})();</script>
```

`main.js` mengirim `generate_lead` (`method: 'whatsapp'`, `cta_position`) di setiap klik WA. `ADS_CONVERSION = 'AW-…/label'` diisi setelah konversi dibuat di Google Ads; konversi Ads hanya untuk nomor sales (bukan rekrutmen). Matikan Cloudflare Web Analytics jika GA4 sudah terpasang (script tambahan menurunkan skor).

## PageSpeed (yang terbukti menaikkan mobile 69 → 90+)

- **Font self-host**: Montserrat variable woff2 (subset latin) + 1 file italic 900. `<link rel="preload" as="font" crossorigin>` + `@font-face` inline dengan `font-display:swap`. Hapus Google Fonts.
- **Hero**: varian `-640.webp`, `-828.webp`, asli 1200; `<img srcset sizes fetchpriority="high">` + `<link rel="preload" as="image" imagesrcset imagesizes>`.
- Semua `<img>` punya `width`/`height`, gambar di bawah fold `loading="lazy" decoding="async"`.
- Kompres logo/klien (WebP, ukuran sesuai tampilan).
- YouTube pakai **lite embed** (thumbnail self-host, iframe `youtube-nocookie` baru dimuat saat diklik).
- gtag ditunda (di atas).
- Ukur: `npx lighthouse@12 <url> --form-factor=mobile --only-categories=performance`. PSI bisa lebih rendah (81 vs 90) karena throttling berbeda; Lighthouse lab cukup untuk iterasi, lalu pantau Core Web Vitals pengguna asli di Search Console.
- Critical CSS inline **tidak wajib** kalau skor sudah ≥80–90; tunggu data CWV asli dulu.

## Favicon dari logo pengguna

Buat `favicon.ico` (16/32/48), `favicon-48.png`, `favicon-192.png`, `favicon-512.png`, `apple-touch-icon.png` (180, latar solid), dan `site.webmanifest`. Pasang `<link rel="icon">` + `apple-touch-icon` + manifest di semua halaman dan template.
