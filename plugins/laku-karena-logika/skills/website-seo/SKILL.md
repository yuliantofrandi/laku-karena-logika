---
name: website-seo
description: Membangun website marketing statis (sales page + landing page SEO/Ads + halaman White Label) untuk produk SaaS/GaaS mana pun dari Business Knowledge Base (BKB) dan keyword plan Excel hasil keyword-research — copywriting AIDA/PAS yang jujur, SEO on-page, schema JSON-LD, dan target hijau PageSpeed (CSS inline, tanpa JS). Pakai skill ini setiap kali user ingin "buat website dari BKB", "buat landing page/sales page", "website dari keyword plan/page brief", "halaman SEO", "landing page Google Ads", menulis isi halaman per slug, atau merevisi website yang sudah dibangun skill ini — bahkan tanpa menyebut kata "website-seo". Skill hilir dari business-knowledge dan keyword-research dalam AI Marketing OS.
---

# Website SEO dari BKB + Keyword Plan

Dipakai berulang untuk **banyak produk SaaS/GaaS** milik user, jadi semua aturan dan template harus tetap generik. Data khusus produk hanya masuk lewat BKB, keyword plan, `site.json`, dan `data/`.

Mengubah dua dokumen hulu menjadi website statis siap deploy:

- **BKB** (`business-knowledge-base.md`, skill `business-knowledge`) → semua fakta: kapabilitas, harga, segmen, GAP, positioning.
- **Keyword plan** (`.xlsx`, skill `keyword-research`) → struktur: slug, title, meta, H1, keyword, isi wajib, link internal, nama kompetitor.

Website = HTML statis + CSS inline, dirakit `scripts/build.py` (Python standar, tanpa dependensi) yang **sekaligus memeriksa aturan** di bawah. Bahasa deliverable: Indonesia.

Bundel skill ini:
- `scripts/build.py` — perakit + pemeriksa aturan. Salin ke root folder website.
- `scripts/brief_to_json.py` — Excel → `data/brief.json` (butuh `openpyxl`, cukup di venv sementara).
- `scripts/ilustrasi.py` — generator ilustrasi SVG (mockup UI & konsep) dari `data/ilustrasi.json`. Salin ke root folder website, di samping `build.py`.
- `scripts/og_image.py` — og:image 1200×630 PNG dari brand/tagline/deskripsi. Salin ke `website/tools/`.
- `assets/starter/` — `site.json`, `data/pricing.json`, `data/social-proof.json`, `static/` (CSS bertoken warna, logo, favicon), dan kerangka halaman. Isi `data/` adalah contoh nyata produk Timebase — **ganti**.
- `references/aturan-konten.md` — aturan isi halaman SEO (wajib dibaca sebelum menulis).
- `references/standar-ui-section.md` — **standar minimum UI setiap section** (disetujui user), dengan gambar acuan di `references/contoh-ui/`. Wajib dibaca sebelum menulis atau menata halaman.
- `references/aturan-sales-page.md` — struktur & psikologi sales page, dan batas kejujurannya.
- `references/aturan-ilustrasi.md` — aturan gambar ilustrasi per section, SEO gambar, og:image, dan cara mengganti dengan gambar asli user.
- `references/checklist-deployment.md` — aturan performa + langkah publish.
- `references/contoh-timebase.md` — peta halaman & keputusan yang sudah divalidasi.

Lokasi folder produk tidak di-hardcode: pakai folder tempat BKB berada (biasanya working directory). Website dibuat di `<folder-produk>/website/`.

## Langkah 0 — Baca input, lalu tanya SEKALI

Baca BKB dan keyword plan sampai tuntas. Jangan mencari-cari file di luar folder produk. Kalau salah satu tidak ada, minta user melampirkannya.

Lalu satu ronde `AskUserQuestion` untuk hal yang **tidak boleh dikarang** (taruh rekomendasi di opsi pertama):
1. **Model penjualan** — langsung langganan (pilih paket → bayar → aktif) atau lewat demo/sales? Ini menentukan semua CTA. **Jangan mengandaikan demo.**
2. **Social proof** — sudah ada data asli (klien, testimoni, metrik)? Kalau belum: slot tersembunyi, atau data contoh yang terlihat asli untuk preview (lihat aturan contoh di bawah).
3. **Risk reversal** yang benar-benar berlaku — free trial / bulanan berhenti kapan saja / garansi uang kembali / belum ada.
4. **Urgensi** — urgensi alami (disarankan) atau promo asli dengan kuota + tanggal berakhir.
5. **Title & rating** — ikuti aturan keyword plan (tanpa "terbaik"/tahun; rating hanya dari ulasan asli) — disarankan.

Domain, `checkout_url`, dan nomor WhatsApp marketing tidak perlu ditanyakan di awal: biarkan kosong di `site.json`. Build memberi WARNING saat preview, dan ERROR untuk `checkout_url`/`whatsapp` kosong saat publish.

## Langkah 1 — Siapkan folder

```
website/
  build.py              ← scripts/build.py
  tools/brief_to_json.py
  site.json             ← assets/starter/site.json (isi brand, tagline, description, nav, copy CTA)
                          nav: halaman solusi/landing dikelompokkan dalam SATU menu group
                          ("Solusi ▾" berisi submenu + deskripsi 1 baris), lalu Harga + tombol CTA.
                          Jangan menjajarkan tiap halaman solusi di menu utama.
                          Menu "White Label" WAJIB ada di menu utama (Solusi ▾ · White Label · Harga · CTA).
  data/brief.json       ← hasil brief_to_json.py
  data/pricing.json     ← dari BKB §3
  data/social-proof.json
  content/<slug>.html   ← satu file per slug; "/" = index.html
  static/style.css      ← ganti token warna di :root dengan warna brand
  static/logo.svg       ← wajib punya width & height
  ilustrasi.py          ← scripts/ilustrasi.py
  data/ilustrasi.json   ← daftar gambar per halaman/section + brief (lihat aturan-ilustrasi.md)
  static/og-image.png   ← python3 tools/og_image.py
  static/fonts/         ← font heading (Montserrat 800 + lisensi OFL) dari assets/starter
```

- `brief_to_json.py <keyword-plan.xlsx> data/brief.json`. **Metadata tidak diketik ulang**: title/meta/H1/keyword/link wajib dibaca build dari brief. Kalau brief melanggar aturan (mis. meta > 155), perbaiki sel di Excel (`openpyxl` tanpa `data_only` agar rumus selamat), lalu jalankan ulang konverter.
- `pricing.json` disalin dari BKB §3: harga tahunan = **10 × bulanan** (bayar 10 dapat 12), add-on selalu menempel ke paket. Setiap skema BKB diberi **nama paket** di `schemes[].name` (tanpa kata "Skema"; lihat aturan-sales-page.md). Syarat baru dari user yang belum ada di BKB (mis. "bulanan, berhenti kapan saja") masuk ke `terms` **dan** dilaporkan ke user untuk ditambahkan ke BKB. **Jangan mengedit BKB atas inisiatif sendiri.**
- **Halaman `/white-label` wajib di setiap produk**, karena semua produk user bisa dibeli dengan merek sendiri. Salin `assets/starter/content/white-label.html` (copy global, jangan ditulis ulang) dan blok `whitelabel` + entri `extra_pages` dari `assets/starter/site.json`. Bagian khusus produk terisi otomatis: `{{brand}}`, `{{deskripsi_kecil}}`, `{{daftar_solusi}}` (dari menu group), `{{wl_kustomisasi}}`, dan `{{wl_ditangani}}`. Konfirmasi ke user daftar `kustomisasi` & `ditangani` untuk produk itu: hapus yang tidak tersedia, jangan menambah klaim. Kalau nama brand panjang membuat title > 60 karakter, pendekkan template title-nya.
- Halaman tambahan di luar brief (beranda `/`, `/harga`, `/white-label`) didefinisikan di `site.json → extra_pages`. `{{brand}}` di title/meta/H1 extra page diganti otomatis. Beranda **tidak** boleh memakai primary keyword halaman lain (kanibalisasi). Primary beranda = nama brand.

## Langkah 2 — Tulis isi

Baca `references/standar-ui-section.md`, `references/aturan-konten.md`, dan `references/aturan-sales-page.md` dulu. Setiap section minimal setara gambar acuan `contoh-ui/standar-section-disetujui.jpg`. Ringkasnya:

- Beranda = **sales page** (AIDA, dengan PAS di blok Interest). Halaman Prioritas 1 (landing Ads) = halaman SEO + komponen jualan (`{{bukti_sosial}}`, `{{testimoni}}`, `{{tanpa_risiko}}`). Halaman Prioritas 2–3 = panduan edukatif + CTA lembut.
- Setiap "Isi Wajib di Halaman" dari brief harus ada. Tulis ringkas: H2 → 1–2 kalimat → poin/kartu/tabel (aturan-sales-page.md). Target 1.000–1.500 kata, minimal 700.
- Fakta hanya dari BKB. Tidak mengarang OS, integrasi, angka pelanggan, atau fitur.

**Ilustrasi wajib di setiap halaman** (aturan tetap user): baca `references/aturan-ilustrasi.md`. Rencanakan satu gambar hero per halaman, plus gambar untuk section-section utama (minimal 3 per halaman). Tulis entri di `data/ilustrasi.json` dengan `brief` gambar pengganti, lalu letakkan `{{gambar:<id>}}` setelah paragraf pertama di bawah H2 section-nya.

Token yang tersedia di konten: `{{gambar:<id>}}` · `{{pricing_table}}` `{{pricing_cards}}` `{{addon_table}}` `{{addon_total_table}}` `{{tanpa_risiko}}` `{{bukti_sosial}}` `{{testimoni}}` `{{cta}}` `{{checkout_link}}` `{{wa_link}}` `{{harga_mulai}}` `{{brand}}` `{{deskripsi}}` `{{deskripsi_kecil}}` `{{daftar_solusi}}` · khusus whitelabel: `{{wl_kustomisasi}}` `{{wl_ditangani}}` `{{wa_whitelabel}}` `{{cta_whitelabel}}`. Lead di bawah H1 ditulis sebagai komentar pertama: `<!-- lead: ... -->`. FAQ ditulis sebagai `<details class="faq"><summary>…</summary><p>…</p></details>` supaya otomatis jadi schema FAQPage.

## Langkah 3 — Build sampai OK

`python3 build.py` (atau `--check`). Build berhenti dengan kode 1 kalau ada **ERROR**:

| Cek | Level |
|---|---|
| Title 40–60, meta 120–155, H1 ≠ title, title/meta/H1 tidak duplikat antar halaman | ERROR |
| Primary keyword di paragraf pertama | ERROR |
| Jumlah kata < 700 (halaman brief) atau < `min_words` (extra page) | ERROR |
| Link internal wajib dari brief belum ada · link internal ke halaman yang tidak ada | ERROR |
| Nama kompetitor (dari sheet Negative, kategori "Nama kompetitor") muncul di halaman | ERROR |
| Klaim terlarang: satu-satunya, termurah, paling murah, pertama di…, nomor satu | ERROR |
| Data social proof `contoh: true` saat `site_url` terisi (build publish) | ERROR |
| `checkout_url` kosong saat `site_url` terisi (tombol beli mati) | ERROR |
| Halaman `/white-label` tidak ada, atau menu "White Label" tidak ada di menu utama | ERROR |
| Section yang hanya berisi teks (tanpa poin, kartu, tabel, callout, blockquote, FAQ, atau gambar), atau tanpa kalimat pembuka setelah H2 | ERROR |
| Lebih dari satu tampilan harga (`{{pricing_cards}}` + `{{pricing_table}}`) di satu halaman | ERROR |
| Gambar per halaman < `min_per_halaman` (3) · gambar tanpa alt · file gambar tidak ada · gambar asli bukan WebP/AVIF/SVG, tanpa w/h, atau > 200 KB | ERROR |
| Halaman tanpa gambar hero · gambar tidak dipakai · alt > 125 karakter · `og_image` kosong saat publish | WARNING |
| `whatsapp` kosong saat `site_url` terisi (tombol WA melayang mati) | ERROR |
| `signin_url` kosong saat `site_url` terisi (tombol Sign In mati) | ERROR |
| Primary keyword tidak ada di title/H1 (berasal dari brief) · secondary keyword belum muncul · 700–999 atau > 1.800 kata · paragraf > ±45 kata · section > 2 paragraf · judul section > 12 kata | WARNING |
| Halaman hukum belum direview (otomatis `noindex` + keluar sitemap) · `site_url`/`checkout_url`/`whatsapp` kosong · data contoh (preview) | WARNING |

Target Python 3.9 (bawaan macOS): **jangan pakai backslash di dalam ekspresi f-string**. Simpan string berisi tanda kutip ke variabel dulu.

## Langkah 4 — Verifikasi di browser

Sajikan `dist/` (`python3 -m http.server <port> --directory dist`, lewat `.claude/launch.json` + `preview_start`), lalu periksa:
- Screenshot desktop dan mobile (375px): nav tidak terbungkus dua baris, harga tidak meluber, logo rapat.
- Lewat `javascript_tool`: `performance.getEntriesByType('resource')` harus **kosong** (nol request eksternal), CLS = 0, `scrollWidth <= innerWidth` di mobile, urutan heading, tipe JSON-LD.
- **Ilustrasi:** buat lembar kontak semua SVG (satu halaman HTML berisi grid `<img>`) dan periksa satu per satu: teks tidak terpotong, tidak menumpuk, dan warna sesuai brand. Lalu di mobile: CLS 0, elemen LCP = gambar hero atau H1, dan gambar di bawah lipatan `loading="lazy"`.
- **Keseimbangan dua kolom:** muat tiap halaman di iframe 1440px, lalu untuk setiap `section.band .split` bandingkan tinggi kolom pertama dan kedua. Rasio > ±2,2 (selain FAQ) berarti ada ruang kosong; perbaiki isinya atau layoutnya.
- **Kepadatan teks:** tidak ada paragraf > ±45 kata (lihat WARNING build), setiap section punya poin/kartu/tabel, dan tidak ada teks tersembunyi ("Baca selengkapnya"). Cek per band di desktop & mobile: dua kolom seimbang, tanpa ruang kosong besar.
- **Kerapian tepi kiri-kanan semua halaman** di lebar 1440, 1280, 768, dan 375 px: muat tiap halaman di iframe selebar itu, lalu bandingkan `getBoundingClientRect()` dari `.brand`, `.hero h1`, dan setiap `article.prose > *`. Tepi kiri harus satu nilai, dan tepi kanan blok (kartu, tabel, CTA) juga satu nilai. Selisih ±4px yang sama di semua elemen biasanya berasal dari scrollbar iframe, jadi bandingkan dengan `clientWidth`.
- Skor PageSpeed asli hanya bisa diukur setelah live. Katakan itu ke user, jangan mengklaim skornya.

## Langkah 5 — Dokumen pendamping

Tulis ke `website/docs/`:
- `wireframe-copywriting.md` — blok demi blok dari hero sampai footer: teks, tahap AIDA/PAS, hook psikologisnya, dan tabel "yang sengaja tidak dipakai + alasannya".
- `checklist-deployment.md` — salin dari `references/checklist-deployment.md`, sesuaikan slug.

- `daftar-ilustrasi.md` dibuat otomatis oleh build. Sampaikan ke user sebagai daftar gambar yang bisa dikirim untuk mengganti placeholder.

Plus `website/README.md`: perintah build, dan tabel "ubah apa → di file mana".

## Cara melaporkan ke user

Singkat dan to the point. Sampaikan:
- Halaman yang jadi + jumlah kata, dan bahwa semua cek lolos.
- **WARNING yang tersisa** apa adanya (mis. primary keyword tidak ada di H1 karena brief) dan usul perbaikannya di Excel.
- Data yang masih contoh, dan bahwa build publish akan menolaknya.
- Yang wajib sebelum publish: domain, link checkout, link Sign In, nomor WA marketing, review hukum, data asli, dan konfirmasi bahwa semua fitur yang disebut sudah tersedia (BKB adalah rancangan; website adalah janji ke pembeli).
- Bagian permintaan user yang tidak diikuti dan alasannya (mis. "Terbaik" di title, rating dari data karangan, kuota palsu).
