# Aturan konten artikel panduan

Pembacanya adalah **tamu website**: calon pelanggan atau pengguna baru yang ingin paham cara aplikasi SaaS bekerja. Tulis sebagai tutorial yang ramah, bukan catatan internal. Contoh lengkap yang sudah disetujui user ada di `contoh-timebase.json` (12 artikel TimeBase).

## Judul, slug, ringkasan
- **Judul = nama tutorialnya saja**, berorientasi aksi. Contoh: "Memantau Aktivitas Karyawan" atau "Mengatur Role & Hak Akses". **Jangan** memakai awalan seri atau nomor ("Panduan X #3: …"), karena urutan diatur di frontend.
- **Slug** bersih, huruf kecil, tanpa nomor urut. Contoh: `memantau-aktivitas-karyawan`. Slug tidak bisa diubah setelah dibuat, jadi tetapkan dengan benar sejak awal.
- **Ringkasan** berupa satu kalimat 120–180 karakter (maksimal 280) tentang apa yang bisa dilakukan pembaca. Kalimat ini tampil di kartu daftar artikel.

## Kategori
- **Level 0 = Docs** (slug `docs`, sudah ada). **Level 1 = nama kelompok tutorial.** Tidak ada level nama produk di tengah.
- Ambil kelompok dari struktur sumber (mis. grup sidebar: Memulai, Navigasi & Akun, Monitoring, Manajemen, Referensi). Kalau sumbernya tidak berkelompok, susun 3–6 kelompok yang logis.
- Nama kelompok ditulis apa adanya ("Monitoring"). **Slug kelompok diberi awalan slug produk** (`timebase-monitoring`) supaya tidak bentrok dengan produk lain. `website-seo` membuang awalan ini dari URL.
- Isi deskripsi kelompok (satu kalimat) dan `urutan` sesuai urutan belajar.
- Satu artikel masuk ke satu kelompok level 1.

## Isi (HTML)
- Pembuka 1–2 kalimat: fungsi menu atau fitur ini, dan kapan dipakai.
- Bagian `<h2>` bernomor ("1. Membuka panel …") untuk alur bertahap, dan `<h3>` untuk sub-bagian (mis. tab).
- Langkah berurutan memakai `<ol>`. Daftar fitur atau field memakai `<ul>` dengan label UI yang **ditebalkan** persis seperti di aplikasi (`<strong>Simpan Setelan WFA</strong>`).
- Kotak tips memakai `<blockquote>` dengan ikon di depan: 💡 Tips, ℹ️ Penting/Ingat, ⚠️ Hati-hati/Perlu diketahui, 🔒 Keamanan. Satu artikel cukup 1–2 kotak.
- Tabel (`<table><tr><th>…`) untuk glosarium atau perbandingan.
- Tag yang dipakai: `h2 h3 p ul ol li strong em code blockquote table tr th td img hr`. **Jangan** memakai `h1` (judul sudah menjadi H1), `script`, `iframe`, `style`, atau atribut `on*`.
- Rujuk artikel lain dengan **judulnya**, bukan nomor. Jangan memasang tautan "Sebelumnya/Selanjutnya", karena navigasi dibuat frontend.
- Bahasa Indonesia baku yang santai, menyapa "Anda". Nama produk ditulis sesuai merek publik. Ganti nama internal atau tenant (mis. "Hub Venturo") dengan nama produk.

## Gambar
- Tulis `{{img:<nama-file>|<keterangan>}}` tepat setelah paragraf yang menjelaskannya. `posting.py` mengunggah gambar lalu menggantinya dengan `<img>` dan keterangan miring di bawahnya.
- Keterangan berupa satu kalimat tentang apa yang terlihat. Jika data pribadi disamarkan, boleh ditambah "Data pribadi pada gambar disamarkan".
- Pakai **hanya gambar hasil penyamaran**. Gambar placeholder ("Ganti dengan screenshot baru") dilewati, dan bagiannya tetap dijelaskan dengan teks.
- **Sampul** artikel adalah screenshot (tersamar) yang paling mewakili isi artikel.

## Yang dibuang dari sumber
- Catatan audit internal, tanggal audit, "diperbarui per …", dan temuan QA.
- Tautan internal (folder Google Drive, localhost, URL admin).
- Kalimat seperti "fitur ini tidak dieksekusi saat audit", serta keterangan versi tampilan lama vs baru. Tulis keadaan sekarang saja, dan beri label *(baru)* bila fitur memang baru.
