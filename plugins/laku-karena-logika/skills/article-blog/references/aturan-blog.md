# Aturan artikel blog

Contoh yang sudah disetujui user: `contoh-blog-timebase.json` ("Kerja WFA Profesional: Panduan agar Hak WFA Tetap Terjaga", 4 Okt 2026). Artikel ini dibuat dari aturan WFA internal perusahaan user dan terbit di kategori Blog TimeBase.

## Pembaca & tujuan
- Pembaca blog: karyawan, atasan/HR, dan calon pelanggan yang mencari wawasan, bukan petunjuk klik menu (petunjuk klik adalah wilayah `article-docs`).
- Tujuan: mengedukasi dan membangun kepercayaan, lalu mengarahkan pembaca dengan lembut ke produk. Produk muncul sebagai solusi alami di satu bagian, bukan iklan di setiap paragraf.

## Kategori
- Artikel masuk ke kategori **Blog** (slug `blog`, level 0) atau anak kategorinya bila sudah ada dan cocok. Website `website-seo` membangun /blog dari `blog` beserta anak-anaknya.
- **Jangan** memasukkan artikel blog ke `docs`.
- Jangan membuat kategori anak Blog baru kecuali diminta user.

## Judul, slug, ringkasan
- **Judul** 40–60 karakter dan memuat kata kunci utama. Pola yang efektif: *"Topik: manfaat yang dijanjikan"*. Contoh: "Kerja WFA Profesional: Panduan agar Hak WFA Tetap Terjaga".
- **Slug** berupa kata kunci, huruf kecil dan tanda hubung, tanpa tanggal atau nomor. Contoh: `kerja-wfa-profesional`.
- **Ringkasan** 120–160 karakter: masalah pembaca + apa yang akan mereka dapat.

## Struktur isi (±900–1.500 kata)
1. **Pembuka** 2 paragraf: konteks yang dekat dengan pembaca, lalu janji isi artikel. Kata kunci utama muncul di paragraf pertama.
2. **4–6 bagian `<h2>`** yang masing-masing menjawab satu pertanyaan. Pakai `<ol>` untuk langkah, `<ul>` untuk poin, `<table>` untuk checklist/perbandingan, dan `<blockquote>` dengan ikon (💡 Tips, ℹ️ Catatan, ⚠️ Hati-hati) maksimal 2–3 kali.
3. **Satu bagian produk** ("Buktikan … dengan data"): fitur nyata yang relevan, dengan 1–2 screenshot produk tersamar.
4. **Checklist/ringkasan praktis** (tabel) yang bisa langsung dipakai pembaca.
5. **Kesimpulan** + CTA lembut ke menu Panduan atau konsultasi. **Tanpa harga** (aturan website: harga hanya di /harga), tanpa klaim "satu-satunya/termurah", dan tanpa nama kompetitor.
- HTML yang dipakai: `h2 h3 p ul ol li strong em blockquote table tr th td img`. Tanpa `h1`, `script`, `iframe`, `style`, atau `on*`.

## Materi dari user (kebijakan internal, SOP, data)
- Sajikan sebagai **"contoh kebijakan dari sebuah perusahaan …"**. Jangan sebut nama perusahaan user atau nama sistem internalnya kecuali user memintanya. Contohnya, "Venturo Hub" ditulis menjadi "aplikasi monitoring" atau nama produk.
- Pertahankan angka dan syaratnya persis (09.00, 8 jam, NPS 8,5, dst.). Rapikan kalimatnya tanpa mengubah maknanya.
- Tambahkan catatan bahwa contoh ini bisa disesuaikan dengan budaya perusahaan pembaca.
- Lengkapi dengan sisi lain yang adil, misalnya peran atasan di samping kewajiban karyawan.

## Gambar
- **3 infografis bermerek + 1–2 screenshot produk tersamar** per artikel. Letakkan satu gambar setelah paragraf pengantar bagian yang dijelaskannya.
- Infografis: kanvas 1600×900 (16:9), memakai template `assets/infografis/` (lihat bawah), dirender dengan `scripts/render_infografis.py`. Ukuran hasil ±120–140 KB.
- Pola & tema: lihat "Variasi infografis" di bawah. Tiga infografis dalam satu artikel tidak boleh terlihat seragam.
- Teks infografis singkat: judul ≤ 1 baris dengan bagian penting diberi gradasi (`<span class="g">`), eyebrow, maksimal ±12 kata per kartu, dan footer berisi logo teks + tagline.
- Warna & font mengikuti merek produk: ambil token dari `static/style.css` website produk (`--purple`, `--pink`, `--orange`, `--grad`, `--ink`) dan font judul dari `static/fonts/`. Default template = TimeBase.
- Nama file gambar memakai kata kunci, misalnya `infografis-ritme-harian-kerja-wfa.jpg` atau `screenshot-detail-aktivitas-karyawan.jpg`.
- Keterangan gambar berupa satu kalimat tentang isinya. Screenshot ditandai "Data pribadi pada gambar disamarkan" bila ada data yang disamarkan.
- Screenshot produk wajib disamarkan dengan aturan yang sama seperti `article-docs`: nama → dummy, 4 digit akhir telepon di-blur, foto profil tetap. Hasil `img-anonim/` dari `article-docs` boleh dipakai ulang.
- **Lihat setiap gambar** setelah dirender: tidak ada teks terpotong atau tumpang tindih, dan judul tidak memakan dua baris kecuali disengaja.

## Variasi infografis (agar pembaca tidak bosan)

Satu artikel = 3 infografis dengan **3 pola berbeda dari kelompok berbeda** dan **minimal 2 tema latar**. Antar-artikel, rotasi pola sampul dan hindari mengulang kombinasi pola artikel blog terakhir.

### Katalog pola (`assets/infografis/`)
| Kelompok | Pola | Cocok untuk | Tema bawaan contoh |
|---|---|---|---|
| Ringkasan | `contoh-kartu-pilar.html` | 3–4 prinsip/pilar berikon | terang |
| Ringkasan | `contoh-pernyataan.html` | satu pesan utama besar + 3 poin pendukung — sampul yang mencolok | `tema-gradasi` |
| Ringkasan | `contoh-siklus.html` | 4 kebiasaan yang berulang mengelilingi satu tujuan | `tema-lembut` |
| Proses | `contoh-timeline.html` | 4–6 langkah berurutan / ritme jam | terang |
| Proses | `contoh-tangga-level.html` | 3–4 tingkat kematangan / tahapan naik | terang |
| Perbandingan & keputusan | `contoh-hindari-vs-lakukan.html` | ✕ kesalahan vs ✓ kebiasaan baik | terang |
| Perbandingan & keputusan | `contoh-alur-keputusan.html` | 2 pertanyaan ya/tidak → hasil | terang |
| Data & praktik | `contoh-angka-besar.html` | 3–4 angka kunci (jam, batas, target) | `tema-gelap` |
| Data & praktik | `contoh-checklist.html` | checklist yang bisa langsung dipakai pembaca | terang |

### Tema latar (kelas di `<body>`, didefinisikan di `base.css`)
- *(tanpa kelas)* terang — putih dengan cahaya lembut warna merek.
- `tema-lembut` — latar tint warna merek, kartu putih.
- `tema-gelap` — latar gelap, teks putih, angka/aksen gradasi. Paling kuat untuk angka besar.
- `tema-gradasi` — latar gradasi merek penuh, teks putih. Maksimal satu per artikel, paling cocok untuk sampul.
- Pola dengan warna isi tetap (`contoh-hindari-vs-lakukan`, `contoh-alur-keputusan`, `contoh-tangga-level`) dipakai di tema terang atau `tema-lembut`.

### Contoh kombinasi yang baik
- Sampul `pernyataan` (gradasi) + `timeline` (terang) + `checklist` (lembut).
- Sampul `angka-besar` (gelap) + `siklus` (lembut) + `hindari-vs-lakukan` (terang).
- Sampul `kartu-pilar` (lembut) + `alur-keputusan` (terang) + `tangga-level` (terang).
