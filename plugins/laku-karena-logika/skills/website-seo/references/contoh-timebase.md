# Contoh Tervalidasi — Timebase (Okt 2026)

Software monitoring aktivitas & akuntabilitas kerja untuk tim WFA di Indonesia. Website pertama yang dibangun dengan skill ini. Dipakai sebagai rujukan pola, bukan folder yang harus ada di mesin.

## Peta halaman

| Slug | Prioritas | Peran | Komponen jualan |
|---|---|---|---|
| `/` | — | Sales page (AIDA+PAS), primary = brand | semua |
| `/harga` | — | Tabel harga + add-on + risk reversal | `tanpa_risiko` |
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
- Risk reversal: "bulanan, berhenti kapan saja" (belum ada trial/garansi).
- Urgensi alami, bukan kuota. Title tanpa "terbaik"/tahun. Rating hanya dari ulasan asli.
- Meta description maks **155** (diperketat dari 160). Kolom Cek di Excel keyword plan ikut disesuaikan.

## Temuan saat membangun

- Brief dari keyword plan bisa melanggar aturannya sendiri (meta 157 karakter; primary keyword tidak ada di H1). Perbaiki di Excel, jangan ditimpa di website.
- Halaman edukatif mudah kurang dari 1.000 kata. Tambah bagian praktis (variasi format per peran, pertanyaan sebelum memilih, contoh aturan), bukan kalimat pengisi.
- Regex klaim terlarang harus spesifik ("pertama di Indonesia", "aplikasi pertama"), karena "yang pertama" juga muncul dalam kalimat biasa.
- Logo SVG berbasis `<text>` perlu `textLength` agar jarak ke ikon konsisten di semua font.
- Hasil: tiap halaman 1 request HTML ±30–40 KB, nol request eksternal, CLS 0.
