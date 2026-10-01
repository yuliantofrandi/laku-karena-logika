# Aturan Konten Halaman

Dipakai saat MENULIS atau MEREVISI `content/*.html`. Sebagian besar dicek otomatis oleh `build.py`. Sisanya dicek dengan membaca ulang halaman.

## 1. Struktur & SEO on-page

1. **1 slug = 1 halaman = 1 ad group.** Jangan membuat dua halaman untuk keyword yang sama, termasuk beranda: primary beranda = nama brand, bukan keyword kategori.
2. **Metadata dari Page Brief, bukan diketik ulang.** Title 40–60 karakter, meta 120–155, H1 berbeda dari title (title untuk SERP, H1 untuk pembaca). Perbaikan dilakukan di Excel, lalu konverter dijalankan ulang.
3. **Primary keyword** ada di paragraf pertama (wajib), title, dan H1. **Secondary keyword** disebar alami di subjudul dan isi. Keyword berbentuk pertanyaan ("… adalah") cukup dijawab di paragraf dan FAQ, jangan dipaksakan ke H1.
4. **Panjang & bentuk:** target 1.000–1.500 kata untuk halaman brief (minimal 700), tapi **ditulis dalam bentuk yang bisa dipindai**: 1–2 kalimat per section + poin/kartu/tabel. Tidak ada paragraf > ±45 kata dan tidak ada teks tersembunyi. Beranda ±900+, halaman harga ±300+.
5. **Heading runtut:** satu H1 (dari layout), H2 untuk bagian, H3 di dalam H2. Jangan melompat.
6. **Semua "Isi Wajib di Halaman"** dari brief ada. **Semua "Internal Link ke"** ditautkan dengan anchor yang deskriptif (bukan "klik di sini").
7. **Slug tanpa tahun.** Title tanpa tahun dan tanpa "terbaik".
8. **FAQ** di akhir halaman, memakai `<details class="faq">`, jawaban 1–3 kalimat yang berdiri sendiri. **Tampilkan hanya pertanyaan penting** (permintaan user): biasanya 4–6 pertanyaan yang menentukan keputusan beli (privasi/keamanan data, kontrak & berhenti, lama sampai aktif, siapa yang cocok/tidak cocok, white label), ditambah pertanyaan dari keyword plan di halaman SEO. Buang pertanyaan teknis kecil atau yang mengulang isi section. Layout tetap siap 20+. Lebih dari ±6 pertanyaan: kelompokkan dengan `<h3>Topik</h3>` di antara pertanyaan, karena build otomatis membuat chip topik. FAQ otomatis jadi schema FAQPage.

## 2. Klaim & objektivitas

1. **Tanpa nama kompetitor** di halaman mana pun: tidak ada halaman "X vs Y" atau "alternatif <merek>". Data kompetitor cepat basi, dan penilaian dari satu sudut tidak objektif.
2. **Bandingkan metode atau kategori**, bukan perusahaan: timesheet manual vs otomatis, fingerprint vs GPS vs QR vs agen desktop, HRIS vs monitoring aktivitas.
3. **Uji kalimat:** kalau kalimat bisa diganti nama merek dan jadi tuduhan, jangan ditulis. Kalau tetap benar untuk semua produk sejenis, itu kategori dan aman.
4. **Klaim terlarang:** satu-satunya, pertama, termurah, paling murah, nomor satu, dan "terbaik" untuk produk sendiri. Fitur standar kategori tidak boleh disajikan sebagai pembeda.
5. **Fakta hanya dari BKB.** Jangan menambahkan OS yang didukung, integrasi, angka pelanggan, kecepatan, sertifikasi, atau perilaku fitur yang tidak tertulis. Kalau sebuah FAQ butuh fakta yang tidak ada, ganti pertanyaannya.
6. **Jujur soal kekurangan — di halaman fitur, bukan di beranda.** Setiap `[GAP]` di BKB §4 yang relevan ditulis di halaman terkait dalam `callout honest`. Contoh: "Idle saat membaca/berpikir", "belum ada ekspor ke payroll/invoice — ada di roadmap".
7. **BKB = rancangan; website = janji.** BKB menulis semua fitur seolah sudah ada. Sebelum publish, user harus mengonfirmasi bahwa semua yang disebut di website sudah tersedia.

## 3. Segmen

- Tulis **siapa yang tidak cocok** (BKB §5 "Bukan target") di halaman yang menarik pencari salah, misalnya halaman absensi yang menarik pekerja lapangan.
- Skema yang dipimpin sesuai BKB §5 (mis. Primary → Skema 2 "Disarankan", Secondary → Skema 3).

## 4. Harga

- **Harga hanya di halaman `/harga`** (`site.json → pricing_page`). Halaman lain boleh menyebut nama paket dan pembedanya, tanpa angka, lalu menautkan ke menu Harga. Isi wajib brief seperti "tabel harga" diganti tautan.

- Satu sumber: `data/pricing.json`, disalin dari BKB §3. Di halaman, harga hanya ditampilkan lewat token, tidak diketik manual (kecuali `{{harga_mulai}}`).
- Tahunan = 10 × bulanan. Add-on tidak dijual terpisah, jadi tampilkan **harga total** skema + add-on (`{{addon_total_table}}`).

## 5. Data pribadi & hukum

- Halaman yang membahas hukum (mis. UU PDP) memuat callout "Bukan nasihat hukum" **setelah** paragraf pertama, dan tetap `noindex` + keluar dari sitemap sampai `legal_reviewed` = `true` di `site.json`.
- Fitur yang menambah jenis data (lokasi, screenshot) selalu disertai ajakan memperbarui persetujuan karyawan.

## 6. Bahasa

Indonesia sehari-hari untuk pemilik usaha/HR, kalimat pendek, angka konkret ("tiap 30 menit", "60 hari"), tanpa jargon marketing kosong. Istilah yang memang dicari dalam bahasa Inggris (time tracker, employee monitoring, work from anywhere) dipakai apa adanya.
