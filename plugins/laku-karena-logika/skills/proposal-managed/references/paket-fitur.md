# Paket Managed Services — kuota fitur bulanan

Sumber: deck "VENTURO - Managed Services" (2026). Harga nett.

## Model
Satu biaya bulanan untuk membangun, merawat, dan mengembangkan aplikasi. Setiap permintaan diukur dalam **satuan fitur** dan ukurannya disepakati sebelum dikerjakan. Paket besar saat membangun, turun ke paket kecil saat aplikasi sudah stabil.

## Harga
| Kuota / bulan | Harga / bulan | Per fitur | Cocok untuk |
|---|---|---|---|
| 2 fitur | Rp7.500.000 | Rp3.750.000 | Sistem yang sudah stabil |
| 4 fitur | Rp14.000.000 | Rp3.500.000 (hemat 7%) | Operasional yang dinamis |
| 6 fitur | Rp19.500.000 | Rp3.250.000 (hemat 13%) | Bisnis yang tumbuh cepat |
| 8 fitur | Rp24.000.000 | Rp3.000.000 (hemat 20%) | Sistem inti multi-divisi |
| 10 fitur | Rp27.500.000 | Rp2.750.000 (hemat 27%) | Skala enterprise |

**Setup Awal Rp10.000.000** (sekali bayar, tidak memotong kuota fitur): Kickoff & Roadmap · Audit Sistem (aplikasi berjalan) atau Setup Core Venturo (proyek baru) · Backup & Keamanan · Akses & Deployment · Dokumentasi & Transfer Ilmu.

## Ukuran fitur
1 fitur sudah termasuk meeting analisa, rancangan aplikasi, penyesuaian (maks. 2× revisi), dan dokumentasi.

| Kategori | < 1 fitur (kecil) | 1 fitur (standar) | 2 fitur (besar) | > 2 fitur (dipecah saat analisa) |
|---|---|---|---|---|
| Pengembangan aplikasi | Tambahan pada modul yang ada: laporan baru, field, atau alur approval | 1 modul utuh: master + transaksi + approval + laporan + notifikasi (mis. Modul Cuti) | Beberapa transaksi saling terkait (mis. PO → penerimaan → stok) | Sistem besar (mis. akuntansi, payroll) |
| Otomasi & AI | Tambahan pada otomasi yang ada: notifikasi WA baru, ubah prompt | 1 otomasi utuh: workflow n8n / pengingat terjadwal (mis. reminder tagihan) | Chatbot AI untuk 1 alur bisnis (mis. cek status pesanan) | AI agent multi-alur yang terhubung ke beberapa sistem |
| Integrasi sistem | Tambahan pada integrasi yang ada / webhook ke 1 endpoint | 1 integrasi utuh: API pihak ketiga, login SSO, atau payment gateway | Integrasi dua arah dengan 1 sistem (mis. marketplace) | Integrasi ERP / sinkronisasi real-time banyak sistem |
| Pengelolaan data | Tambahan pada data yang ada: import Excel, koreksi & rapikan data | 1 migrasi utuh: data 1 modul dari sistem lama | Migrasi beberapa modul + validasi data | Migrasi seluruh sistem lama |

- Contoh: Modul Cuti lengkap (master + pengajuan + approval + laporan + notifikasi WA) = 1 fitur.
- Fitur di atas ukuran besar dipecah menjadi beberapa fitur saat meeting analisa.
- Fitur kecil dinilai desimal sesuai besar pekerjaan (mis. tambah 1 field = 0,1).
- Pelatihan tambahan di luar rilis fitur: ½ hari = ½ fitur. Pelatihan onsite ditambah biaya perjalanan.

## Sudah termasuk di semua paket (tanpa memotong kuota fitur)
Garansi perbaikan bug tanpa biaya · ukuran fitur disepakati di awal · meeting analisa & rancangan aplikasi · lebih dari estimasi ditanggung Venturo · testing & UAT di staging setiap rilis · revisi maks. 2× per fitur · bantuan penggunaan aplikasi · help desk grup WhatsApp khusus · pelatihan pengguna saat rilis fitur · isu kritis ditangani prioritas · koordinasi vendor pihak ketiga · dokumentasi aplikasi.

Deck menulis "isu kritis direspons maks. 1 hari kerja"; di dokumen penawaran **angka SLA tidak ditulis** — angka SLA hanya di Service Agreement Pasal 4 (respons 15 menit, penyelesaian bug maks. 2 jam).

## Layanan berlangganan setelah proyek
- **Layanan Lanjutan**: default paket 2 fitur (Rp7.500.000/bulan), mulai tanggal 1 bulan setelah periode proyek terakhir.
- **Venturo Cloud**: rate card `references/venturo-cloud.md`, mulai 1 bulan sebelum go-live.
