# Log Keputusan venturo.id

Fakta dan keputusan yang sudah diambil pengguna (pemilik Venturo). Jangan diubah tanpa diminta. Status per Oktober 2026.

## Identitas

- Brand: **Venturo Pro** (jangan tulis "PT" di halaman mana pun).
- Klaim footer: "The Largest …" (opsi 1 yang dipilih pengguna).
- Kantor: Malang (pusat), Jakarta (disebut kedua), Bandung (pengganti Jember).
- Bahasa balasan ke pengguna: Indonesia.

## Kontak

- WA sales: `6285128043814` (tampil `0851-2804-3814`) → semua halaman jual. Nomor lama `0881-…` tidak dipakai lagi.
- WA rekrutmen: `6285174187053` → `/magang-it-malang/` dan `/job/`.
- **Tidak ada email** di website, termasuk footer.

## Hosting & tracking

- Cloudflare Pages, proyek `venturo-website`, deploy direct upload dengan wrangler. DNS di Cloudflare, apex + www proxied, Redirect Rule www → apex. Email Google Workspace (MX jangan diubah).
- CMS Lakukan slug publik `venturo-web`, kategori `portfolio` + `portfolio-ai`.
- GA4 `G-EWGMG89CHE`, Google Ads `AW-16682756931`, `ADS_CONVERSION` masih kosong sampai konversi dibuat.
- Cloudflare Web Analytics dimatikan.

## Peta halaman (1 keyword = 1 halaman)

| Halaman | Keyword utama |
|---|---|
| `/` | software house |
| `/software-house-malang/` | software house malang |
| `/jasa-pembuatan-aplikasi/` | jasa pembuatan aplikasi (+ aplikasi web, digabung) |
| `/jasa-pembuatan-aplikasi-android/` | jasa pembuatan aplikasi android |
| `/jasa-pembuatan-website/` | jasa pembuatan website (+ toko online / e-commerce) |
| `/jasa-pembuatan-ai/` | jasa pembuatan AI |
| `/enterprise-ai-transformation/` | enterprise AI |
| `/outsourcing-programmer/` | outsourcing programmer |
| `/jasa-maintenance-aplikasi/` | jasa maintenance website/aplikasi |
| `/harga-pembuatan-aplikasi/` | harga pembuatan aplikasi (tanpa angka, estimator) |
| `/it-outsourcing-jakarta/` | software house jakarta |
| `/it-outsourcing-terbaik/` | it outsourcing terbaik |
| `/job/`, `/magang-it-malang/` | karir & magang |
| `/kebijakan-privasi/` | (tidak ditautkan di footer) |

`/jasa-pembuatan-aplikasi-web/` → 301 ke `/jasa-pembuatan-aplikasi/`. URL lama `/profile`, `/partnership`, `/ratecard-compro` sengaja dibiarkan 404 (sudah tercakup PDF).

PDF company profile (link langsung, noindex, tidak dipublikasikan): `/VENTURO-Managed-Services.pdf`, `/VENTURO-Dedicated-Team.pdf`.

## Keputusan konten

- Tanpa harga di semua halaman. Estimator di halaman harga: deskripsi fitur bebas (textarea), tanpa pilihan integrasi.
- Model: **Dedicated Team** dan **Managed Services** (dengan Delivery Point, hangus tiap bulan). Long Term >3 bulan / Short Term <3 bulan (di beberapa tempat cukup tanpa menyebut "3 bulan").
- Yang termasuk Managed Services hanya **Jaminan Kualitas** dan **Dukungan**.
- Ganti talent / akhiri kontrak: pemberitahuan 30 hari (Dedicated Team & Managed Services).
- Section Bayar Bulanan ("Dedicated Team / Managed Services Venturo", "Bayar Bulanan, Anda Terima Beres") di 6 halaman, termasuk halaman AI dengan catatan tim kecil. Pengguna menolak versi dua kartu; pakai layout lama.
- "Jika target tidak tercapai, Venturo yang menanggung"; THR ditanggung; laporan progres **harian**.
- Rekrutmen: tanpa technical test → seleksi CV & portfolio; fresh graduate boleh dengan portfolio (bukan syarat D3). Tanpa materi training di halaman magang.
- Native tidak direndahkan dibanding Flutter.
- Klaim (100+ engineer, 200+ proyek, sejak 2013, garansi 30 hari, 90% Jakarta) maksimal sekali per halaman di elemen sorotan.
- Foto acara Bali hanya di `/job/`. Hero harga memakai foto.
- Portfolio AI: kartu nyata dari CMS + filter `/portfolio/ai/`. Kandidat tambahan: CCTV AI, Telcobot.

## Hasil terakhir

- Audit live: semua halaman 200, link & gambar OK, redirect OK, sitemap ±100 URL.
- Lighthouse mobile 90–93, PSI 81. Critical CSS ditunda sampai ada data CWV asli.
