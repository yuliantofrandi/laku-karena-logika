---
name: website-service
description: Membangun, merombak, dan merawat website untuk bisnis JASA software (software house, IT outsourcing, dedicated team, managed services, jasa pembuatan aplikasi/website/AI, maintenance) dengan fokus SEO lokal, GEO, PageSpeed, dan penjualan lewat WhatsApp. Statis HTML + Cloudflare Pages Functions, portfolio & blog dari CMS Lakukan, tanpa harga, satu keyword satu halaman. Gunakan saat pengguna berkata "buat website jasa", "website software house", "landing page layanan", "halaman jasa pembuatan X", "website company profile jasa", "rombak website venturo", "tambah halaman layanan", "audit website venturo", atau "deploy website jasa ke cloudflare". Untuk website PRODUK SaaS gunakan skill website-seo, bukan skill ini.
---

# Website Service – Website untuk Lini Bisnis Jasa Software

Skill ini merangkum cara membangun **venturo.id** (2026), yang sudah live dan terbukti: semua halaman 200, Lighthouse mobile 90–93, dan siap jual. Pakai pola yang sama untuk website jasa lain milik pengguna.

## Kapan skill ini, kapan website-seo

Pengguna punya dua lini bisnis software:

| Lini | Skill | Ciri website |
|---|---|---|
| **Jasa / service** (software house, outsourcing, dedicated team, managed services) | **website-service** (ini) | Menjual tim & kemampuan. Tanpa harga. CTA ke WhatsApp sales. Banyak halaman layanan per keyword + halaman lokal (kota). Bukti: portfolio, klien, tim, video. |
| **Produk SaaS** | **website-seo** | Menjual produk. Fitur, harga/paket, trial/daftar, dokumentasi. |

Kalau ragu, tanya: "yang dijual tim/jasa atau produk/langganan software?"

## Bahan yang diminta sebelum mulai

1. **Company profile / rate card PDF** (sumber fakta: model kerja sama, klaim angka, klien, alamat). Jangan mengarang klaim; setiap angka harus ada sumbernya.
2. **Keyword plan** (xlsx/daftar). Ini jadi peta halaman: 1 keyword utama = 1 halaman. Bisa dibuat dulu dengan skill `keyword-research`.
3. **Nomor WhatsApp**: sales dan rekrutmen (kalau ada halaman karir/magang).
4. **CMS Lakukan**: company slug publik (contoh `venturo-web`) dan kategori portfolio. Isi portfolio ditulis dengan skill `article-portfolio`, blog dengan `article-blog`.
5. **Aset**: logo (untuk favicon), foto tim asli, video YouTube lama, logo klien yang boleh tampil.
6. **ID tracking**: GA4 (`G-…`) dan Google Ads (`AW-…`) jika ada.

## Alur kerja

1. **Peta halaman** dari keyword plan. Tulis tabel "halaman → keyword utama → keyword pendukung" di README proyek. Gabungkan halaman yang isinya mirip (redirect 301), jangan buat dua halaman untuk satu niat pencarian. Lihat `references/aturan-konten-jasa.md`.
2. **Kerangka proyek**: salin `assets/starter/` (Functions CMS, `_headers`, `_redirects`, `robots.txt`, `main.js`, `wrangler.toml`) lalu sesuaikan slug CMS, nomor WA, pesan WA, dan domain. Lihat `references/arsitektur-dan-deploy.md`.
3. **Tulis halaman** satu per satu mengikuti pola section di `references/standar-ui.md` dan aturan konten (tanpa harga, klaim sekali per halaman, CTA WA berkonteks).
4. **Portfolio & blog** dari CMS: `/portfolio/`, `/portfolio/ai/` (filter), `/portfolio/<slug>/`, `/blog/`. Lihat `references/cms-portfolio-blog.md`.
5. **SEO/GEO**: title ≤65, description ≤165, 1 H1, canonical, og:image, JSON-LD (Organization/LocalBusiness, Service, FAQPage, BreadcrumbList), `sitemap.xml`, `llms.txt`.
6. **Performa**: font self-host + preload, hero `srcset` + preload, gtag ditunda, gambar diberi width/height. Target Lighthouse mobile ≥90.
7. **Audit prapublish**: jalankan `scripts/audit.py` dan `scripts/dupe.py`, cek tampilan mobile (375px) dan laptop 14". Lihat `references/checklist-prapublish.md`.
8. **Deploy** ke Cloudflare Pages + hubungkan domain + redirect www. **Minta izin dulu** sebelum deploy produksi atau mengubah DNS.
9. **Pasca-launch**: Search Console, key event GA4, import konversi Ads, Google Business Profile.

## Aturan wajib (ringkas)

- **Tidak ada harga** di mana pun (teks, JSON-LD, FAQ). Halaman "harga" menjelaskan faktor biaya + estimator yang dikirim ke WhatsApp.
- **CTA ke WhatsApp** dengan pesan otomatis sesuai konteks tombol; setiap klik mengirim `generate_lead` dengan `cta_position`. Tidak ada email di website kecuali pengguna minta.
- **1 keyword = 1 halaman**, tidak ada kanibalisasi.
- **Setiap klaim sekali per halaman** di elemen sorotan (hero, stat, kartu). FAQ dan paragraf boleh menyebut ulang.
- **Tidak ada API key/rahasia** di file website atau repo. CMS dibaca lewat API publik di server (Functions).
- **Nama perusahaan** ditulis sesuai keinginan pengguna (Venturo: "Venturo Pro", tanpa "PT").
- **Jangan merendahkan** satu teknologi demi teknologi lain (contoh: native vs Flutter disajikan netral).
- Setiap edit HTML massal → validasi JSON-LD dan cek ulang dengan screenshot.
- Balas pengguna dalam **Bahasa Indonesia**.

## Referensi

- `references/arsitektur-dan-deploy.md`: struktur folder, Cloudflare Pages/Functions, cache, `_headers`/`_redirects`/404, deploy wrangler, DNS + redirect www, GA4/Ads tertunda, PageSpeed.
- `references/aturan-konten-jasa.md`: peta keyword, model kerja sama (Dedicated Team & Managed Services), section Bayar Bulanan, CTA WA, klaim, penggabungan halaman.
- `references/standar-ui.md`: pola section, warna selang-seling, kartu vs teks panjang, video lite YouTube, hero, navbar/footer, mobile.
- `references/cms-portfolio-blog.md`: API publik Lakukan, kategori portfolio + portfolio-ai, render server, ukuran gambar otomatis, sitemap.
- `references/checklist-prapublish.md`: checklist sebelum dan sesudah publish.
- `references/log-keputusan-venturo.md`: fakta & keputusan khusus venturo.id (nomor WA, peta halaman, keputusan yang sudah diambil pengguna). Baca ini setiap kali mengerjakan venturo.id.

## Starter & script

- `assets/starter/`: kode yang dipakai venturo.id. `functions/_lib/` (cms, render, render-blog, image-size), route `portfolio/[[path]].js`, `blog/[[path]].js`, `sitemap.xml.js`, serta `website/_headers`, `_redirects`, `robots.txt`, `assets/js/main.js`, dan `wrangler.toml`. Ganti semua nilai khusus Venturo (slug CMS, nomor WA, domain, ID GA/Ads, nama brand) sebelum dipakai untuk proyek lain.
- `scripts/audit.py <base-url>`: audit SEO teknis + link/gambar rusak + teks terlarang.
- `scripts/dupe.py`: cari klaim yang diulang dalam satu halaman (ubah pola `PAT` sesuai klaim perusahaan).
