# Standar Dokumen Legal (Kebijakan Privasi & Syarat Layanan)

User (4 Okt 2026): *"selalu buatkan kebijakan privasi dan syarat layanan, buatkan isinya secara real, sebisa mungkin saya tidak perlu mengedit lagi isinya"*.

**Urutan:** Syarat Layanan dulu, lalu Kebijakan Privasi — di footer dan di navigasi kiri (urutan `site.json legal`; user: "syarat layanan naikkan ke atas, lebih penting").

**Dijaga build (ERROR):** `site.json legal` wajib berisi `/syarat-layanan` dan `/kebijakan-privasi`, dan kedua file `content/…html` wajib sudah ditulis (tidak ada lagi halaman placeholder). User: "di semua landing page nanti harus ada syarat layanan & kebijakan privasi".

**Wajib di setiap website produk:** `content/kebijakan-privasi.html` dan `content/syarat-layanan.html`, ditautkan di footer bawah (`site.json legal`). Tulis isinya lengkap saat membuat website — jangan biarkan placeholder. Contoh lengkap yang sudah dipakai: `references/contoh-legal/` (Timebase).

## Cara menulis
- **Sumber fakta hanya BKB + isi website** (data yang dikumpulkan, paket, retensi, lokasi server, peran data, cara bayar, dukungan). Jangan mengarang fitur, sertifikasi, enkripsi, atau angka yang tidak tertulis.
- Bahasa Indonesia baku, lugas, kalimat pendek; poin bernomor per pasal. Rujuk **UU 27/2022 (UU PDP)**.
- Token yang diisi build: `{{brand}}`, `{{tanggal_berlaku}}` (`site.json legal_berlaku`), `{{wa_link}}` (kontak lewat WhatsApp — user tidak memakai email).
- Halaman dirender sebagai **dokumen dengan navigasi kiri** (user: "buat jadi ada navigasi di sebelah kiri, seperti contoh ini"): hero polos tanpa CTA/statistik, `noindex`.
  - Desktop: sidebar 280px **sticky** berlatar abu muda berisi grup per dokumen legal (`<details>`; dokumen aktif terbuka & berwarna ungu, lainnya tertutup), item = pasal ("1. …") yang menaut ke `#pasal-N`.
  - Hero ringkas (`hero-sederhana`: padding 36/32px, user: "padding atas bawahnya terlalu tinggi"): badge **"Dokumen legal"** · H1 nama dokumen · subjudul **ringkasan isi** dari `site.json legal[].lead` (mis. "Data apa yang dicatat <Brand>, berapa lama disimpan, siapa yang bisa melihatnya, dan hak Anda atas data tersebut."). Badge, judul, dan subjudul tidak boleh mengulang pesan yang sama (user: "3 hal ini memiliki makna pesan yang sama").
  - Isi: kotak info biru muda "Berlaku sejak …", judul pasal dengan **lingkaran nomor bergradasi**. Tulis judul pasal sebagai `<h2>N. Judul</h2>` — build menambah id & lingkaran nomor.
  - Mobile: sidebar disembunyikan, diganti "Daftar isi" yang tertutup (tidak mendorong isi ke bawah). Tanpa JavaScript.

## Kebijakan Privasi — pasal wajib
1. Tentang kebijakan ini (cakupan: situs, akun, agen/produk; acuan UU PDP)
2. Peran kami: **pengendali** untuk data akun/penagihan/komunikasi/situs; **prosesor** untuk data yang diproses atas instruksi pelanggan (pelanggan = pengendali)
3. Data yang dikumpulkan (per kategori, sesuai fitur & paket; kapan dicatat dan kapan tidak)
4. Tujuan & dasar pemrosesan (perjanjian, instruksi pengendali + persetujuan, kepentingan sah, kewajiban hukum); tidak menjual data
5. Transparansi bagi orang yang datanya diproses (bila produk memantau/merekam)
6. Penyimpanan & masa simpan (lokasi + retensi per jenis data dari BKB)
7. Keamanan (hanya langkah yang benar ada)
8. Pihak penerima (infrastruktur, pembayaran, komunikasi, aparat bila diwajibkan)
9. Hak subjek data UU PDP + jalur pengajuan (langsung vs lewat pengendali)
10. Kegagalan pelindungan data: pemberitahuan ≤ 3 × 24 jam
11. Anak-anak · 12. Perubahan kebijakan · 13. Kontak (WhatsApp)

## Syarat Layanan — pasal wajib
Penerimaan · definisi · akun · paket/harga/pembayaran (dari pricing.json & BKB) · berhenti berlangganan · **kewajiban pelanggan sebagai pengendali** · pemrosesan data oleh penyedia (prosesor) · penggunaan yang dilarang · pemasangan & dukungan (per paket) · batasan layanan (keterbatasan nyata produk dari BKB) · hak kekayaan intelektual · White Label (perjanjian terpisah) · batasan tanggung jawab · pengakhiran · hukum & sengketa · perubahan syarat · kontak.

## Default yang dipakai bila BKB tidak mengatur (sebutkan ke user saat menyerahkan)
- Berhenti berlaku di akhir periode yang sudah dibayar; biaya periode berjalan tidak dikembalikan kecuali diwajibkan hukum.
- Batas tanggung jawab = biaya yang dibayar 12 bulan terakhir.
- Hukum RI; musyawarah 30 hari, lalu pengadilan negeri yang berwenang di Indonesia (tanpa menyebut kota).
- Situs tanpa cookie pelacakan pihak ketiga (perbarui kebijakan sebelum memasang analitik/piksel iklan).
- Nama pihak = nama brand (bukan nama PT) kecuali user memberi nama badan usaha.
