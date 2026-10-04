# Standar Halaman Harga (`/harga`)

Disetujui user (website Timebase, 2 Okt 2026): *"page harga sudah cocok, simpan hal penting di rules, karena setiap landing page harus punya page ini"*.

**Wajib di setiap website produk.** `build.py` memberi ERROR bila `/harga` tidak ada di `site.json extra_pages`, menu "Harga" tidak ada di `nav`, atau halaman `pricing_page` tidak memakai `{{pricing_table}}`. Template siap pakai: `assets/starter/content/harga.html`.

## Prinsip
- **Harga hanya di halaman ini.** Beranda & landing produk tidak menampilkan angka; cukup menautkan ke menu Harga.
- **Minimalis.** Penekanan lewat tipografi, garis, dan badge kecil — bukan blok warna gelap/gradasi penuh.
- **Tidak ada pesan dobel** antara pembuka, catatan, kartu, dan FAQ.

## Hero
- Layout hero standar (badge pill · H1 · subjudul · 1 CTA → · 3 statistik · media hero yang sama dengan semua halaman).
- **Badge = kalimat ajakan**, bukan nama halaman (contoh: "Pilih paket yang pas untuk tim Anda"; user: "kata-kata seperti ajakan"). Atur lewat `extra_pages[/harga].eyebrow`.
- H1 memuat primary keyword "Harga <Brand>" (contoh: "Harga Timebase dalam Rupiah, per Karyawan"). Lead: cara hitung + aturan tahunan.
- Halaman ini **tanpa band intro**.

## Section 1 — Tabel harga
| Bagian | Standar |
|---|---|
| Judul | **Kalimat ajakan**, bukan "Tabel harga" (contoh: "Pilih paket, aktif hari ini"). Rata tengah. Jangan menjanjikan hal yang belum tentu terjadi hari itu (mis. "tercatat hari ini" bila perlu pemasangan agen) |
| Pembuka | Satu paragraf ringkasan: "**Harga <Brand>** dihitung per … dalam rupiah — makin besar tim, makin murah … Semua paket sudah termasuk …". Rata tengah, memuat primary keyword (cek paragraf pertama) |
| Switch | Bulanan / Tahunan (CSS-only), label "Hemat N bulan" |
| Tabel | Satu tabel: harga per jumlah pengguna + fitur. **Header minimalis**: latar putih, nama paket font heading 17px (15px mobile), garis bawah 2px. **Semua kolom berwarna sama, tanpa badge** di header. Sel pojok kiri tanpa label terlihat ("Jumlah karyawan" hanya `.sr-only`) |
| Tombol beli | **Hanya di bawah tabel** (footer), paket disarankan = tombol gradasi. Tidak ada baris tombol di atas tabel |
| Add-on | **Satu kotak** di bawah tabel, badge ungu "ADD-ON" menempel di garis atas kotak; tiap add-on satu baris: nama (boleh link ke halaman detailnya via `addons[].link`) · deskripsi 1 kalimat · harga yang ikut switch. >1 add-on → baris dipisah garis, kolom sejajar (nama 180px) di desktop, bertumpuk di mobile. Tanpa section/H2/ilustrasi/tabel add-on terpisah |
| Catatan | Tidak ada catatan kecil yang mengulang paragraf pembuka (`pricing.json note` dikosongkan bila sama) |

## Section 2 — Paket mana yang cocok?
- Judul + 1 kalimat pembuka **rata tengah**.
- `div.grid.persona` berisi **3 kartu persona** sejajar (bertumpuk di mobile): ikon dalam kotak tint · nama paket · "Untuk <persona>" · 2 poin pembeda (`ul.checks`, ≤6 kata/poin).
- Paket disarankan: `card featured` (garis ungu) + badge ungu "DISARANKAN" menempel di garis atas kartu.
- **Tanpa gambar besar dan tanpa tombol** (tombol beli sudah di tabel). Ilustrasi contoh tagihan ditolak user ("kurang menarik").
- Penutup `p.penutup` rata tengah: "Belum yakin? Lihat … atau mulai dari <paket disarankan> bulanan — berhenti kapan saja."

## Section 3 — FAQ harga
Layout FAQ standar (judul ajakan rata tengah, mis. "Masih ragu soal harga?", subjudul otomatis, satu kotak bergaris + chevron). 3 pertanyaan penting: cara hitung tahunan, biaya pemasangan, add-on tanpa paket (hapus bila tidak ada add-on).

## Section 4 — CTA penutup
`{{cta}}` ringkas standar (1 kalimat + 2 tombol | ≤4 poin pendek).

## Gambar
Cukup media hero (`min_per_halaman_khusus: {"/harga": 1}` di `data/ilustrasi.json`). Isi utama halaman ini adalah tabel dan kartu.

## Data yang diisi per produk
- `data/pricing.json`: `schemes` (nama paket, harga per tier, `featured`, `for`), `tier_labels`, `annual_months_paid`, `features`, `addons[]` (`name`, `monthly`, `desc`, `applies_to`, `link`), `terms`, `note` (boleh kosong).
- `content/harga.html`: salin template, isi pembuka, 3 kartu persona, jawaban FAQ dari BKB.
- `site.json extra_pages[/harga]`: `title`, `meta`, `h1`, `primary` ("Harga <Brand>"), `eyebrow` (ajakan), `links` (halaman produk + halaman detail add-on), `min_words` 300.


## Modal langganan → QRIS (tombol "Pilih <paket>")
User (4 Okt 2026): "saat pilih paket, munculkan modal untuk subscription dan dilanjutkan nanti akan memunculkan QRIS pembayaran. Untuk link QRIS-nya menyusul". Modul: `scripts/langganan.py`, aktif bila `site.json` punya blok `"langganan"`.

- **Tombol paket** di tabel harga diberi class `js-langganan` + `data-paket`. Tanpa JS, tombol tetap link biasa (`checkout_url` / `#pilih-skema`).
- **Langkah 1 – Langganan <paket>:**
  - Pilihan Bulanan/Tahunan (mengikuti switch tabel) dan jumlah karyawan.
  - Add-on dari `pricing.json` sebagai kotak centang.
  - Ringkasan harga langsung dihitung: tier dari jumlah karyawan, tahunan = bulanan × `annual_months_paid`, add-on per karyawan.
  - Data aktivasi: nama, perusahaan, email kerja, WhatsApp, dengan validasi wajib isi.
  - Kalimat persetujuan yang menautkan Syarat Layanan & Kebijakan Privasi.
- **Langkah 2 – Bayar dengan QRIS:**
  - Total, no. pesanan (`TB-YYYYMMDD-XXXX`), ringkasan paket, dan 3 langkah bayar.
  - Area QRIS:
    - `qris_url` berakhiran gambar → gambar QR ditampilkan.
    - URL lain → tombol "Tampilkan QRIS".
    - Kosong → kotak "QRIS sedang disiapkan" (build memberi WARNING).
  - `qris_url` boleh memuat `{order} {total} {paket} {periode} {karyawan}`.
  - Tombol konfirmasi membuka WhatsApp dengan ringkasan pesanan lengkap (butuh `site.json whatsapp`).
- **Data formulir tidak dikirim ke server mana pun** dari halaman statis ini. Data hanya masuk ke pesan WhatsApp yang dikirim sendiri oleh pengunjung. Bila nanti ada API pesanan, sambungkan di langkah 2.
- Bila blok `langganan` ada, `checkout_url` tidak wajib lagi.
- **Mobile:** modal tampil sebagai bottom sheet selebar layar. Elemen `[hidden]` di dalam modal wajib `display:none!important`, karena aturan flex bisa menimpanya.
