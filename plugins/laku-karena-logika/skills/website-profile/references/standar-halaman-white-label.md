# Standar Halaman White Label (`/white-label`)

Disetujui user (website Timebase, 3 Okt 2026): *"simpan jika ada rule yang penting, karena setiap landing page juga harus ada white label ini"*.

**Wajib di setiap website produk.** Semua produk SaaS/GaaS user bisa dibeli dengan merek sendiri. `build.py` memberi ERROR bila halaman `/white-label` tidak ada, tidak ada di menu, atau tidak memakai `{{cta_whitelabel}}`. Template global siap pakai (tidak ditulis ulang per produk): `assets/starter/content/white-label.html` + blok `whitelabel` dan entri `/white-label` di `assets/starter/site.json`.

## Positioning (jangan diubah tanpa user)
- **Pain point utama:** perusahaan dengan banyak karyawan **tidak mau bayar bulanan per karyawan** karena tagihannya jadi tinggi.
- **Skema:** **beli putus (sekali bayar)**, karyawan tidak terbatas, **dipasang di server milik pembeli**, memakai **merek pembeli**.
- **Bukan program reseller.** Sudut "dijual lagi ke klien" sudah tidak relevan (membuat produk sendiri kini cepat dengan AI) — hanya **satu jawaban FAQ**.
- Penjualan lewat **konsultasi WhatsApp**, bukan checkout. Harga "per penawaran".

## Menu
Item **terakhir** di dropdown "Solusi" dengan deskripsi "Beli putus dengan merek & server sendiri" — **bukan** menu utama (±90% pembeli tidak mencari white label). Footer otomatis mengikuti (kolom "Solusi"). `{{daftar_solusi}}` mengecualikan `/white-label`.

## Struktur halaman (urutan tetap)
| # | Section | Isi & layout |
|---|---|---|
| Hero | — | Badge **ajakan** "Miliki software-nya, bukan menyewa" · H1 "White Label: Sekali Bayar, Tanpa Biaya per Karyawan" · lead untuk perusahaan dengan banyak karyawan · CTA `Minta Penawaran White Label` (WA) · media hero sama dengan semua halaman |
| Intro | Paragraf entitas | "Program **white label** <Brand> untuk perusahaan dengan tim besar: beli lisensinya sekali, pasang di server sendiri, dan pakai dengan nama, logo, serta domain perusahaan Anda. <Brand> adalah `{{deskripsi_kecil}}`." (≤45 kata) |
| 1 | Tagihan bulanan yang ikut membengkak | Header rata tengah + kartu angka `300×` / "biaya lisensi yang ditagih setiap bulan" / "Ilustrasi tim 300 karyawan…" + panel 3 poin (tidak pernah berhenti · naik saat tim tumbuh · data di server pihak lain) |
| 2 | Untuk siapa White Label ini? | 3 kartu **berikon**: perusahaan dengan ratusan karyawan · grup usaha & holding · organisasi dengan aturan data ketat |
| 3 | Langganan vs White Label | Grafik batang **beranimasi** (tagihan 50→400 karyawan naik vs "sekali bayar", tanpa rupiah) + tabel 4 baris (cara bayar · saat tim bertambah · tempat data · merek) |
| 4 | Yang ikut dalam lisensi | `{{daftar_solusi}}` dalam panel + link ke harga |
| 5 | Yang bisa disesuaikan dengan brand Anda | `{{wl_kustomisasi}}` — **layout polos** judul + panel. Jangan diberi mockup/ikon hiasan (dua kali ditolak user) |
| 6 | Keuntungan beli putus | **4 kartu berikon**: Sekali bayar · Tim bertambah, biaya tidak · Data di server sendiri · Merek perusahaan Anda (gabungan "Yang menjadi milik Anda" + "Keuntungan" yang pesannya dobel) |
| 7 | Masih ragu soal White Label? | FAQ standar: apa itu white label · masih ada biaya bulanan? · di mana data disimpan · harga (per penawaran) · bisa dijual lagi ke klien? (satu jawaban) · beda dengan langganan |
| 8 | CTA | `{{cta_whitelabel}}` "Siap lepas dari tagihan bulanan per karyawan?" → WA |

**Tidak ada:** section "Cara kerja" (dihapus user), testimoni/bukti sosial (sampai ada pembeli white label asli), angka rupiah, harga/minimum lisensi/persentase hemat yang belum diputuskan, janji siapa yang memasang atau dukungan/pembaruan pasca-beli sebelum dikonfirmasi user.

## Angka & gambar
- `min_words` 600 (halaman sengaja ringkas). Gambar: hero + grafik tagihan (`min_per_halaman_khusus["/white-label"] = 2`).
- Kartu angka dan keterangannya tidak boleh mengulang kata/angka yang sama (build WARNING).

## Data yang diisi per produk
- `site.json → whitelabel`: `kustomisasi` (hanya yang benar tersedia), `wa_text`, `cta_title`, `cta_text`, `cta_button`.
- `site.json extra_pages[/white-label]`: `title` ("<Brand> White Label: Sekali Bayar, Tanpa Biaya Bulanan"), `meta`, `h1`, `primary` "white label", `eyebrow`, `min_words` 600.
- `data/ilustrasi.json`: entri grafik `white-label-vs-bangun-sendiri` (`jenis: bars`, `animasi: true`).
- Bila produk berbeda skemanya (mis. tidak bisa self-hosted), **tanya user dulu** sebelum mengubah copy global.
