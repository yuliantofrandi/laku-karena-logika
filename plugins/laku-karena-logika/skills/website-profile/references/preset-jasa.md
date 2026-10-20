# Preset `jasa`

Untuk website bisnis **jasa software** (software house, IT outsourcing, dedicated team, managed services, jasa pembuatan aplikasi/website/AI). Aktif dengan `site.json → "preset": "jasa"`. Mulai dari `assets/starter/site-jasa.json` (salin jadi `site.json`).

Isi & gaya bahasa: baca `references/aturan-konten-jasa.md`. Contoh nyata keputusan bisnis jasa: `references/log-keputusan-venturo.md`.

## Beda dengan preset `produk`

| | produk | jasa |
|---|---|---|
| Menu utama | Solusi ▾ (+ White Label terakhir) · Harga · Blog · Panduan | **Layanan ▾ · Portfolio · Blog** (· Karir bila ada) |
| Tombol kanan header | Sign In + Langganan | **Konsultasi** (WhatsApp); Sign In hanya bila `signin_url` diisi |
| Tombol utama (hero, CTA, header) | checkout / modal langganan | **WhatsApp sales** (`whatsapp` + `whatsapp_text`) |
| Harga | wajib di `/harga` (tabel + switch) | **dilarang di mana pun**: token harga dan angka `Rp…`/`… juta` = ERROR |
| Halaman wajib | Harga, White Label, Syarat Layanan, Kebijakan Privasi, Blog | **Kebijakan Privasi, Blog** (Portfolio sangat disarankan, WARNING bila tidak ada) |
| `data/pricing.json` | wajib | tidak dipakai |
| Schema beranda | Organization + SoftwareApplication/Offer (halaman produk) | Organization + **ProfessionalService** (alamat dari `site.json → alamat`, telepon dari `whatsapp`) |
| Konten CMS | Blog, Panduan | Blog, **Portfolio** (+ Panduan opsional) |

Semua aturan lain sama: brief keyword plan, title/meta/H1, kata minimum, link internal, ilustrasi per section, standar UI section, dokumen legal, PageSpeed, deploy Cloudflare.

## Portfolio dari CMS (Cloudflare Functions)

- Aktif bila menu `["/portfolio", "Portfolio"]` ada di `site.json nav`. Build menulis `dist/_templates/shell-portfolio.html`.
- Sumber: kategori `lakukan.kategori_portfolio` (default `portfolio`) beserta variannya (`portfolio-ai`, …). Artikel AI diberi **dua** kategori di CMS: `portfolio` + `portfolio-ai`.
- Rute: `/portfolio` (semua + chip filter Semua/AI), `/portfolio/ai` (hanya AI, muncul bila ada artikel AI), `/portfolio/<slug>` (studi kasus: daftar isi, tombol "Diskusikan proyek serupa" ke WhatsApp dengan judul proyek, 3 portfolio lain, CTA penutup).
- Teks hero: `lakukan.portfolio_eyebrow`, `lakukan.portfolio_lead`.
- Link internal ke `/portfolio/<slug>` di konten statis tidak divalidasi build (artikelnya hidup di CMS); cek manual setelah deploy.
- Isi artikel ditulis dengan skill `article-portfolio`.

## Ceklis tambahan preset jasa

- `whatsapp` terisi (build publish ERROR bila kosong) dan sama dengan nomor di Google Business Profile.
- Tidak ada angka harga di konten, FAQ, maupun gambar (build hanya membaca teks; cek gambar manual).
- Setiap klaim angka (jumlah engineer, proyek, tahun berdiri) tampil sekali per halaman di elemen sorotan: `python3 scripts/dupe.py` dari folder `dist/` (ubah pola `PAT` sesuai klaim perusahaan).
- Setelah live: `python3 scripts/audit.py https://domain` (status, title/meta, H1, JSON-LD, link & gambar rusak, teks terlarang).
