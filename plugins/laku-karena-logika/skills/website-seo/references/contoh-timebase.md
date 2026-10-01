# Contoh Tervalidasi — Timebase (Okt 2026)

Software monitoring aktivitas & akuntabilitas kerja untuk tim WFA di Indonesia. Website pertama yang dibangun dengan skill ini. Dipakai sebagai rujukan pola, bukan folder yang harus ada di mesin.

## Peta halaman

| Slug | Prioritas | Peran | Komponen jualan |
|---|---|---|---|
| `/` | — | Sales page (AIDA+PAS), primary = brand | semua |
| `/harga` | — | Tabel harga + add-on + risk reversal | `tanpa_risiko` |
| `/white-label` | — | Copy global whitelabel (wajib di semua produk), CTA konsultasi WA | — |
| `/aplikasi-monitoring-karyawan` | 1 | Landing Ads + SEO | bukti sosial, testimoni, risk reversal |
| `/aplikasi-time-tracking` | 1 | Landing Ads + SEO (Skema 3, agensi) | bukti sosial, testimoni, risk reversal |
| `/aplikasi-kerja-remote` | 2 | SEO + Ads kecil; definisi WFA/WFH/hybrid | CTA |
| `/monitoring-karyawan-uu-pdp` | 2 | SEO otoritas; **noindex sampai review hukum** | CTA |
| `/laporan-kerja-harian` | 2 | SEO; format laporan siap pakai | CTA |
| `/produktivitas-karyawan` | 3 | SEO; output vs aktivitas, "Idle ≠ malas" | CTA |
| `/hris-vs-monitoring-aktivitas` | 3 | SEO; perbandingan **kategori** | CTA |
| `/absensi-karyawan-hybrid` | 3 | Add-on presensi; tegaskan bukan untuk pekerja lapangan; tabel harga total | CTA |

## Keputusan user yang membentuk aturan skill

- Social proof: "buatkan seperti asli, nanti diganti data asli", sehingga lahir mekanisme `contoh: true` + blokir publish.
- **Model penjualan: langsung langganan, tanpa demo** ("tidak ada jadwalkan demo, langsung subscription, bayar aktif"). Versi pertama memakai CTA "Jadwalkan Demo" dan dikoreksi user, sehingga skill sekarang menanyakan model penjualan di Langkah 0.
- **Navigasi:** "menu Monitoring, Time Tracking, Kerja Remote, Absensi Hybrid mending dijadikan 1 menu group dengan submenu". Hasilnya: Solusi ▾ · Harga · Langganan.
- **Tombol WA melayang:** "di bagian bawah selalu tambahkan CTA untuk klik ke WA marketing … baik di desktop/mobile", dengan contoh gambar tombol "Hubungi Kami !! / Konsultasi 100% Gratis". Koreksi lanjutan: "warnanya sesuaikan dengan design system" dan "di mobile cukup tombol WA saja, jangan mengganggu layar HP". Versi pertama memakai warna indigo dari gambar dan bar bawah berisi Langganan + WA, dan keduanya dikoreksi. Lalu: "di mobile tulisan Konsultasi 100% Gratis jangan dihilangkan" dan "button-nya minimalis saja", lalu "padding-nya lebih besar sehingga tulisannya lebih kecil".
- **Whitelabel:** "selalu tambahkan menu Whitelabel, software SaaS yang saya buat selalu bisa dibeli dengan merek sendiri; buatkan copywriting global agar bisa dipakai di produk manapun", karena skill ini dipakai untuk banyak landing page produk SaaS/GaaS.
- **Nama menu:** user bertanya apakah "Whitelabel" tepat. Rekomendasi yang disetujui: **"White Label"** (ejaan baku dua kata, istilah yang dicari calon mitra), slug `/white-label`.
- **Layout:** "cek layout bagian kanan kiri semua page, terlihat tidak rapi". Penyebabnya: hero di kolom 1120px, isi di kolom 760px. Diperbaiki menjadi satu kolom 920px untuk semua bagian.
- **Ilustrasi:** "cek semua page selalu tambah gambar-gambar ilustrasi aplikasi / ilustrasi yang dibutuhkan … sehingga website tidak monoton … perhatikan SEO dan PageSpeed karena akan lanjut ke audit SEO". Hasilnya: 35 SVG (≤7 KB) di 11 halaman (3–5 per halaman), hero dua kolom, `docs/daftar-ilustrasi.md` berisi brief, dan og:image PNG.
- **Switch harga:** "untuk harga ada button switch antara ke tahunan dan bulanan". Diterapkan di kartu & tabel, tanpa JS, default Bulanan, label "Hemat 2 bulan".
- **Satu tampilan harga:** "tabel harganya cukup 1 saja". `/harga` hanya tabel (tombol beli di header & footer), halaman lain hanya kartu. Tabel di mobile diberi kolom kiri sticky + petunjuk geser.
- **Tampilan:** "kurang bagus, banyak blank space, terlalu banyak tulisan". Solusinya: kontainer 1160px, band dua kolom otomatis, dan teks sekunder dilipat. Paragraf yang terlihat turun ke 29–58% di halaman konten tanpa mengurangi jumlah kata.
- **Nama paket:** "di bagian harga tidak perlu ada tulisan skema". Skema 1/2/3 → Aktivitas / Bukti Visual / Waktu Per Tugas di seluruh website (BKB tetap memakai Skema).
- **Header:** "semua menu taruh tengah, kecuali menu Langganan; di sebelah kiri Langganan ada tombol Sign In".
- **Hero:** "untuk hero selalu buat referensinya seperti ini layoutnya" + gambar referensi (badge "Accountability in every hour", H1 besar, CTA "Daftar Sekarang Juga →", statistik, foto orang memegang laptop di atas bentuk gradasi). Statistik "24/7 Monitoring" dari referensi sengaja tidak disalin.
- **Tanpa "Baca selengkapnya":** "saya tidak suka ada baca selengkapnya, karena rata-rata orang tidak klik ini". User memilih "ringkas jadi poin & kartu". Semua halaman ditulis ulang; paragraf terpanjang turun dari 100 ke ≤38 kata; jumlah kata 669–1.033 (minimum diturunkan ke 700).
- **Standar UI section:** "harusnya UI-nya bagus seperti 3 section yang saya suruh revisi ini … minimal standard setiap section desain UI-nya seperti ini". Hero, band intro, dan section pertama beranda dijadikan acuan (`standar-ui-section.md` + `contoh-ui/`).
- **Standardisasi semua section:** "cek semua page, dan standardkan untuk desain semua section". Audit menemukan 66 dari 91 section memakai layout judul-kiri yang menyisakan ruang kosong. Diganti 4 layout otomatis (media / panel / FAQ / susun), 15 kalimat pembuka ditambahkan, dan sisa ketimpangan turun dari 66 ke 10 section dengan rasio ±2,2–2,6 yang secara visual masih rapi.
- **Harga hanya di menu Harga:** "tidak perlu harga untuk di semua page, cukup di menu harga saja" (perluasan dari aturan beranda). Kartu harga di Monitoring & Time Tracking, tabel add-on di Absensi, dan "mulai Rp 6.000" di Kerja Remote diganti tautan ke /harga.
- **Beranda tanpa harga (awal):** "tidak perlu harga di home, biarkan orang klik di menu harga saja". Kartu harga dihapus dari beranda, blok jaminan dipindah ke "Kenapa sebaiknya mulai bulan ini", schema Offer dicabut dari beranda.
- **Kontras:** "tulisannya tidak terlihat" (daftar syarat di blok CTA gelap tertimpa `.prose li`). Audit kontras semua halaman lalu memperbaiki 6 jenis elemen lain di bawah WCAG AA.
- **Pesan dobel:** "ini sama pesannya seperti yang di kiri" (catatan hitungan 110 jam mengulang poin di panel). Ditambah cek otomatis, yang menemukan 2 kasus lain (Add-on di /harga, caption Cara kerja white label).
- **Beranda tanpa section "Jujur soal batasnya":** "section ini sepertinya tidak perlu". Batasan (Idle, belum ada ekspor payroll/invoice) tetap ada di 6 halaman fitur.
- **Urgensi + jaminan digabung ke CTA penutup:** "dua section ini sepertinya punya pesan yang sama, gabung jadi 1 section saja" (section "Kenapa sebaiknya mulai bulan ini" + blok jaminan vs CTA penutup). Blok jaminan terpisah juga dihapus dari Monitoring, Time Tracking, dan Harga.
- **Foto testimoni:** "tambahkan foto dari yang memberikan testimoni, agar lebih terlihat real". Diterapkan sebagai slot foto asli + avatar inisial; foto stok/wajah AI sengaja tidak dipakai karena testimoninya masih data contoh. Lanjutan: "selalu buatkan foto dulu, sebelum saya kasih yang asli" → avatar inisial diganti potret ilustrasi flat-vector otomatis per testimoni (rambut/hijab, warna kulit, kacamata, baju warna brand).
- **FAQ dinamis:** "buat layoutnya lebih dinamis, misal ada 20 FAQ di sini, siapkan untuk itu". Diuji dengan 20 pertanyaan dalam 4 topik: chip topik, kolom kiri sticky, accordion eksklusif, tanpa overflow di mobile.
- **FAQ gaya referensi:** "mending buat begini, dan pertanyaan FAQ-nya berikan yang penting-penting" (gambar FAQ Humanis). Layout dua kolom + kartu bantuan diganti judul besar rata tengah + satu kotak daftar bergaris dengan chevron. FAQ beranda disusun ulang jadi 6 pertanyaan keputusan (dimata-matai, lokasi & lama simpan data, kontrak, lama aktif, tim lapangan, white label); pertanyaan teknis kecil di halaman lain dibuang.
- Risk reversal: "bulanan, berhenti kapan saja" (belum ada trial/garansi).
- Urgensi alami, bukan kuota. Title tanpa "terbaik"/tahun. Rating hanya dari ulasan asli.
- Meta description maks **155** (diperketat dari 160). Kolom Cek di Excel keyword plan ikut disesuaikan.

## Temuan saat membangun

- Brief dari keyword plan bisa melanggar aturannya sendiri (meta 157 karakter; primary keyword tidak ada di H1). Perbaiki di Excel, jangan ditimpa di website.
- Halaman edukatif mudah kurang dari 1.000 kata. Tambah bagian praktis (variasi format per peran, pertanyaan sebelum memilih, contoh aturan), bukan kalimat pengisi.
- Regex klaim terlarang harus spesifik ("pertama di Indonesia", "aplikasi pertama"), karena "yang pertama" juga muncul dalam kalimat biasa.
- Logo SVG berbasis `<text>` perlu `textLength` agar jarak ke ikon konsisten di semua font.
- Hasil: tiap halaman 1 request HTML ±30–40 KB, nol request eksternal, CLS 0.
