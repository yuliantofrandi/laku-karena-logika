# Checklist Prapublish & Pasca-launch

## Sebelum publish

- [ ] `python3 scripts/audit.py http://localhost:8788` → semua `OK`: status 200, title ≤65, description ≤165, canonical, 1 H1, og:image, JSON-LD valid, `<img>` ada alt + width, tidak ada judul ganda, link & gambar tidak rusak.
- [ ] Tidak ada harga, lorem, TODO, email, nomor WA lama (tambah pola lewat env `FORBID`).
- [ ] `python3 scripts/dupe.py` (dari folder `website/`) → tidak ada klaim ganda di elemen sorotan.
- [ ] Semua halaman ada di menu, footer, `sitemap.xml`, `llms.txt`; halaman gabungan sudah 301.
- [ ] `404.html` ada dan bermerek (link ke beranda + WA).
- [ ] Halaman kebijakan privasi ada (wajib bila memakai GA/Ads), boleh tidak ditautkan di footer bila pengguna minta.
- [ ] Favicon + manifest di semua halaman dan template.
- [ ] GA4 + Ads terpasang di semua halaman dan template CMS; klik WA mengirim `generate_lead`.
- [ ] `?v=` CSS/JS = `ASSET_VERSION` di `render.js`.
- [ ] Logo klien sudah boleh ditampilkan.
- [ ] Screenshot 375px dan 1440px untuk halaman yang diubah.
- [ ] Lighthouse mobile ≥90 untuk beranda dan 1–2 halaman layanan.

## Saat publish (minta izin pengguna)

- [ ] `npx wrangler@4 pages deploy --branch main`.
- [ ] Custom domain apex + www, CNAME proxied, record email tidak berubah.
- [ ] Redirect Rule www → apex 301.
- [ ] `python3 scripts/audit.py https://domain.id --extra /url-lama/ /file.pdf` di situs live.
- [ ] URL lama dari website sebelumnya: putuskan bersama pengguna mana yang di-301 dan mana yang dibiarkan 404.

## Setelah publish

- [ ] Google Search Console: verifikasi domain (DNS TXT), submit `sitemap.xml`.
- [ ] GA4: tandai `generate_lead` sebagai key event; buat custom dimension `cta_position` (event-scoped).
- [ ] Google Ads: import key event dari GA4 atau buat konversi lalu isi `ADS_CONVERSION` di `main.js`.
- [ ] Google Business Profile: website + nomor WA sama dengan situs.
- [ ] Tambah testimoni dan portfolio baru secara berkala (CMS).
- [ ] Pantau Core Web Vitals pengguna asli di Search Console sebelum optimasi lanjutan.
