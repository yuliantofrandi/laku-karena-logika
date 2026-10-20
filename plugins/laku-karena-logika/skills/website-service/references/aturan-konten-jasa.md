# Aturan Konten Website Jasa

## Tujuan setiap halaman

Halaman jasa harus **menjual**: pembaca paham masalahnya dipahami, percaya Venturo mampu (bukti), lalu klik WhatsApp. Urutan umum:

1. Hero: H1 berisi keyword, subjudul manfaat, 1–2 CTA WA, foto tim asli.
2. Masalah / kebutuhan klien.
3. Solusi & lingkup layanan (kartu).
4. Model kerja sama (Dedicated Team / Managed Services) atau proses kerja.
5. Bukti: portfolio dari CMS (kartu nyata), logo klien, video, angka (sekali saja).
6. Section **Bayar Bulanan** (lihat bawah) di halaman yang relevan.
7. FAQ (FAQPage JSON-LD).
8. CTA akhir.

## Peta keyword

- **1 keyword utama = 1 halaman.** Keyword pendukung dimasukkan ke halaman yang sama (H2, FAQ, alt).
- Kalau dua halaman ternyata menjawab niat yang sama (contoh "jasa pembuatan aplikasi" vs "jasa pembuatan aplikasi web" ketika semua aplikasi berbasis web), **gabungkan**: pindahkan isi terbaik, redirect 301, perbarui sitemap/llms/menu/footer/README.
- Topik ditempatkan di halaman yang niatnya cocok. Contoh: **toko online / e-commerce** masuk halaman jasa pembuatan website (fokus "website yang mendatangkan traffic dan penjualan"), bukan halaman aplikasi. Contoh modul aplikasi bisnis: HRIS, CRM, Finance.
- Halaman lokal (kota) memakai LocalBusiness JSON-LD + alamat + peta.
- Catat peta di README proyek.

## Harga

- **Tidak ada angka harga** di teks, tabel, FAQ, atau JSON-LD (tidak ada `offers.price`).
- Halaman "harga pembuatan aplikasi" menjelaskan **faktor biaya** + **estimator** (pilihan jenis aplikasi, platform, deskripsi fitur bebas di textarea) yang dikirim sebagai pesan WhatsApp.
- Pertanyaan biaya di FAQ dijawab dengan faktor + ajakan konsultasi.

## CTA WhatsApp

- Semua tombol `data-wa="<kunci>"`; `main.js` membangun link `wa.me` + pesan otomatis dari `WA_MESSAGES[kunci]` sehingga sales tahu asal tombol.
- Nomor sales untuk semua halaman jual; nomor rekrutmen khusus halaman karir/magang.
- Nomor yang tampil sebagai teks (footer, JSON-LD `telephone`) harus sama dengan nomor di `main.js`.
- Tidak ada email (kecuali pengguna meminta). Tidak ada form yang mengirim data ke pihak ketiga.
- Teks tombol pendek dan jelas ("Konsultasi via WhatsApp", "Minta Proposal").

## Model kerja sama (pola Venturo, pakai ulang bila cocok)

- **Dedicated Team**: tim/talent dikontrak bulanan, dikelola klien. Long Term (>3 bulan) / Short Term (<3 bulan).
- **Managed Services**: target hasil dikelola Venturo, memakai **Delivery Point** (kuota pekerjaan per bulan; Delivery Point **hangus tiap bulan**, tulis sebagai catatan kecil). Termasuk: **Jaminan Kualitas** dan **Dukungan**.
- Ganti talent atau akhiri kontrak: **pemberitahuan 30 hari**.
- Hindari menyebut angka minimal yang belum disetujui pengguna.

## Section "Bayar Bulanan"

Dipasang di halaman layanan utama dan halaman AI. Isi pokok:
- Judul: "Dedicated Team / Managed Services Venturo", subjudul "Bayar Bulanan, Anda Terima Beres".
- Poin: tanpa rekrut sendiri, tanpa beban HR, **THR ditanggung**, "Jika target tidak tercapai, Venturo yang menanggung", laporan progres **harian**.
- Di halaman AI: catatan bahwa proyek AI bisa dimulai dengan tim kecil.
- Pertahankan layout yang sudah disetujui pengguna (jangan mendesain ulang tanpa diminta).

## Klaim & fakta

- Semua angka (jumlah engineer, proyek, tahun berdiri, garansi, persentase) harus dari company profile atau pengguna.
- **Setiap klaim tampil maksimal sekali per halaman di elemen sorotan.** FAQ/paragraf boleh. Cek dengan `scripts/dupe.py`.
- Kalau sebuah section mengulang klaim yang sudah ada di hero/stat, ganti dengan manfaat lain, jangan hapus section-nya.
- Sebut perbandingan teknologi secara netral (native dan cross-platform sama-sama punya kelebihan).

## Gaya bahasa

- Bahasa Indonesia baku santai, kalimat pendek, fokus ke manfaat bisnis.
- Hindari tanda pisah panjang berlebihan dan jargon tanpa penjelasan.
- Rapikan redaksi pengguna saat diminta, tapi pertahankan maksud dan istilahnya.
- Laporan progres disebut "harian" (bukan mingguan) bila itu praktik perusahaan.

## GEO (mesin AI)

- `llms.txt` di root: ringkasan perusahaan, layanan + URL, model kerja sama, kontak WA, kota. Perbarui setiap ada halaman baru/gabung.
- FAQ yang menjawab pertanyaan langsung ("berapa lama", "apakah bisa", "bagaimana jika target tidak tercapai").
- Section "Sekilas Tentang <Brand>" berisi fakta singkat yang mudah dikutip.
