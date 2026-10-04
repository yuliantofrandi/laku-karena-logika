# Standar Minimum UI per Section

Disetujui user (website Timebase, 1 Okt 2026): *"harusnya UI-nya bagus seperti 3 section yang saya suruh revisi ini … minimal standard setiap section desain UI-nya seperti ini"*.

Acuan visual:
- `contoh-ui/standar-section-disetujui.jpg` — hero (bagian bawah) → band intro → section pertama, versi yang disetujui.
- `contoh-ui/referensi-hero-user.webp` — referensi hero asli dari user (foto orang + laptop di atas bentuk gradasi).

**Setiap section di setiap website wajib setidaknya setara dengan acuan ini.** Kalau sebuah section tidak bisa dibuat seperti ini, ubah isinya, jangan turunkan standarnya.

## 1. Hero
Lihat "Hero" di `aturan-sales-page.md`. Ringkasnya: badge pill gradasi · H1 Montserrat 800 gelap ≤55 karakter · subjudul abu 2–3 baris · satu CTA gradasi dengan → · tiga statistik sejajar (angka besar + label kecil) · gambar di atas bentuk gradasi brand · latar gradasi lembut.

## 2. Band intro (tepat di bawah hero)
- **Logo cloud tanpa kotak:** label kecil berhuruf kapital renggang ("DIPAKAI TIM DI BERBAGAI INDUSTRI"), lalu deretan nama/logo abu-abu (Montserrat 800, ±17px; logo asli: grayscale, tinggi seragam ±28px), lalu garis tipis pemisah selebar kontainer.
- **Pernyataan rata tengah:** satu paragraf entitas 1–2 kalimat ("<Brand> adalah …"), ±20px, maks ±820px, nama brand berwarna primer. Rata kiri di mobile.
- Latar putih.

## 3. Section isi (setiap H2)
| Elemen | Standar |
|---|---|
| Latar | Bergantian, **dimulai abu muda** setelah band intro (putih), supaya batas antar-section selalu terlihat. Padding atas-bawah ±64px (±44px mobile) |
| Tata letak | **Selalu dua kolom yang seimbang**, dipilih otomatis oleh `render_section` dari isi section (tabel di bawah). Mobile: menumpuk |
| Judul (H2) | Montserrat 800, ±32px, ≤12 kata, idealnya 2 baris. Pertanyaan atau pernyataan yang tajam |
| Pembuka | **1–2 kalimat**, ≤ ±30 kata, warna abu tua. Tidak ada dua paragraf berturut-turut. **Menempel ke judul**: jarak kotak H2 → pembuka ±4px (`.prose h2{margin-bottom:4px;line-height:1.15}` + `.prose h2+p{margin-top:0}`; FAQ 6px). User: "jarak atas jangan terlalu jauh dengan heading-nya", lalu 8–12px pun masih "terlalu tinggi" |
| Isi yang dipindai | **Wajib minimal satu**: daftar centang (`ul.checks`, awalan tebal + sisa kalimat biasa), kartu (`div.grid` > `.card`, judul + 1 kalimat, `span.num` untuk langkah), tabel kecil, callout, atau gambar  Kartu tanpa nomor langkah (mis. "Untuk siapa") diberi **ikon ilustrasi** `<span class="ikon">` + SVG garis 22px di kotak tint ungu 42px di atas judul (user: "tambahkan icon ilustrasi di setiap card"); kartu langkah tetap memakai `span.num`. |
| Gambar | Ilustrasi dalam kartu membulat (radius ±18px, latar tint lembut) + caption kecil abu di bawahnya |
| Blok lebar | Kartu, tabel, harga, testimoni tampil selebar kontainer di bawah baris dua kolom |
| Teks tersembunyi | **Tidak boleh.** Tidak ada "Baca selengkapnya". FAQ boleh accordion |
| Pesan dobel | **Satu pesan sekali per section.** Pembuka, catatan, caption gambar, dan poin/kartu tidak boleh mengulang hal yang sama. Kasus nyata: catatan "Hitungan 110 jam = 20 × 15 × 22" mengulang poin di panel; asumsi hitungannya cukup ditulis di poin itu sendiri |

### Layout otomatis per jenis isi (hasil "standardkan semua section")
| Isi section | Layout | Catatan |
|---|---|---|
| Ada `{{gambar:…}}` | `split.media`: teks \| gambar, bergantian kiri-kanan | Kalau kolom teks hanya judul + pembuka, kartu (`grid`) pertama ikut ke kolom teks (2 kolom) supaya seimbang dengan gambar |
| Ada poin/langkah/contoh/callout (tanpa gambar) | `split.panel-row`: teks (5) \| **panel kartu putih** (7) berisi poin, bergantian kiri-kanan | Panel = pengganti kartu gambar. Daftar > 4 poin otomatis 2 kolom di dalam panel |
| FAQ | `faq-center` (referensi user, gaya Humanis): **judul besar rata tengah** → **satu kotak putih membulat** berisi baris pertanyaan bergaris pemisah, pertanyaan tebal di kiri + **chevron** di kanan (berputar saat terbuka) | Tanpa kolom kiri, tanpa kartu bantuan (tombol WA melayang sudah ada). **Wajib subjudul** abu ±18px rata tengah di bawah judul (permintaan user): paragraf pembuka section, atau otomatis dari `copy.faq_lead`. **Judul tidak boleh mengulang makna subjudul**: jangan "Pertanyaan yang sering ditanyakan"; pakai judul yang mengajak, mis. "Masih ragu? Ini jawabannya" / "Masih ragu soal harga?" (permintaan user). **Isi hanya pertanyaan penting** (4–6 yang menentukan keputusan beli: privasi, keamanan data, kontrak, lama aktif, cocok/tidak cocok, white label). Tetap siap 20+ pertanyaan: accordion eksklusif (`<details name>`), `<h3>` di antara pertanyaan → grup topik (kotak per grup) + chip navigasi rata tengah. Tanpa JS |
| Hanya kartu/tabel/testimoni (atau harga di /harga) | `split.stack`: judul + pembuka (maks 760px) di atas, blok selebar kontainer di bawah | Blok jaminan (`guarantee`) selalu selebar kontainer |

### Mengisi ruang kosong di kolom teks (user: "atas bawahnya ada blank space, berikan sesuatu")
- **Angka besar (`div.stat`)**: `<div class="stat"><strong>110 jam</strong><span>arti angka</span><small>cara hitung</small></div>`. Section yang punya stat otomatis memakai layout **header rata tengah** (judul + pembuka, maks 760px) lalu baris **angka | panel** (5fr | 7fr, tinggi sama, isi kartu angka rata tengah); mobile bertumpuk. User: "jadikan di tengah section". Angka harus fakta/hitungan yang ditulis jelas, dan **dipindah** dari panel (jangan diulang di poin panel). **Angka dan keterangannya tidak boleh mengulang kata/angka yang sama** (user: "2 div ini mirip kata-katanya"; contoh buruk "300 karyawan" + "berarti 300 biaya lisensi", baik "300×" + "biaya lisensi yang ditagih setiap bulan"); build WARNING. Angka pendek juga mencegah teks meluber di HP.
- **Panel jauh lebih panjang dari judul+pembuka** (teks panel > 2,3× judul·1,8 + pembuka): build otomatis menyusun judul di atas dan panel selebar kontainer (`.panel-wide`, daftar >2 poin jadi dua kolom).
- **Kolom media potret selebar medianya** (`split media potret`: `1fr 340px`): kolom 50% untuk video 340px menyisakan area kosong lebar di kiri-kanan video (user: "areanya terlalu lebar"). Pengecualian per entri: `"kolom": "sama"` di `ilustrasi.json` → kolom 50:50 (video tetap 340px di tengah kolom) — dipakai bila kolom teks berisi callout/poin panjang (user: "buat kolomnya jadi 50:50", section bukti jam tertagih di Time Tracking).
- **Video/gambar potret (9:16) di section yang punya poin**: kartu (`grid`) section ikut ke kolom teks (2×2) di samping media, karena media potret ±635px tinggi akan menyisakan ruang kosong bila kolom teks hanya judul + poin (kasus: video detail aktivitas menggantikan grafik pemakaian aplikasi).
- **Gambar + tabel perbandingan pendek** (≤460 karakter): tabel ikut ke kolom teks di samping gambar (di desktop tabel menyesuaikan lebar kolom, font 14px). Tabel panjang tetap selebar kontainer.
- Grid item `.split>*{min-width:0}` wajib agar tabel/konten lebar tidak membuat halaman meluber di mobile.

Target keseimbangan: tinggi kolom terpanjang ≤ ±1,8× kolom terpendek di 1440px (kecuali FAQ). Ukur dengan skrip di SKILL.md Langkah 4. Hasil Timebase setelah perbaikan: semua section ≤1,8× (sebelumnya sampai 2,96×), tanpa overflow di 1440/1280/768/375.

## 3b. CTA penutup (blok gelap, satu per halaman)
Latar band CTA (`band end`) memakai **gradasi yang sama dengan hero** (ungu muda kiri atas, peach kanan atas, di atas #fbfafe) di semua halaman. User (4 Okt 2026): "buat gradasi saja seperti section hero". Hasilnya selalu berbeda dari section tepat di atasnya: abu (`alt`) bila section terakhir putih, dan putih bila section terakhir abu. Ini diatur otomatis di `layout_sections`, dan artikel blog selalu memakai `alt` karena artikelnya berlatar putih. User (4 Okt 2026): "buat background-nya warna berbeda daripada section yang atasnya".

**Ringkas** (keluhan user: "terlalu banyak teks"). Dua kolom: kiri judul + **satu kalimat pendek** (`copy.cta_text` ≤16 kata) + dua tombol berdampingan; kanan panel transparan berisi **satu daftar centang** `copy.cta_poin`: maks 4 frasa ≤6 kata (urgensi + jaminan), tanpa label, tanpa penjelasan panjang. Jaminan lengkap tetap di /harga. Build memberi WARNING bila melebihi. Urgensi dan jaminan **tidak** diulang di section lain. Band CTA memakai padding atas = bawah yang sama dengan band lain (64px / 44px mobile); jangan beri override padding khusus (kasus nyata: 8px atas vs 64px bawah, ditegur user "padding atas bawahnya tidak sama").

## 3c. Kartu poin berikon (bukan angka)
Disetujui user (4 Okt 2026): "jika butuh point, kasih icon saja jangan pakai angka".
- Markup: `<div class="grid ikon-tengah">`, dan tiap kartu diawali `<span class="ikon-bulat" aria-hidden="true"><svg …stroke="currentColor"…></svg></span>`, lalu `h3` dan `p`. Pakai ikon garis (24×24, stroke 2) yang sesuai maknanya.
- Tampilan: lingkaran gradasi `--grad` 58px dengan ikon putih di tengah atas, judul tebal rata tengah, deskripsi abu rata tengah. Kartu abu muda di band putih dan putih di band `alt`.
- Judul section dan pembuka otomatis rata tengah (`split stack center`).
- Cukup **satu paragraf pembuka**. Jangan menambah `p.note` di bawahnya; gabungkan pesannya ke pembuka ("2 p ini jadikan 1 saja").
- `span.num` hanya untuk urutan langkah yang memang berurutan, bukan untuk daftar poin.
- Berlaku di **semua halaman** (user, 4 Okt 2026: "ya, terapkan ke semua halaman"): masalah, fitur, metrik, kesalahan, dan kartu berikon White Label. Kartu di samping video juga memakai gaya ini, dengan susunan 2×2.
- 5 kartu disusun 3 + 2 di desktop (otomatis lewat CSS), supaya tidak ada satu kartu sendirian di baris kedua.
- `p.note` yang dulu ada di bawah pembuka digabung ke kalimat pembuka. Tautan internalnya tetap dipertahankan.

## 3d. Badge hero tidak mengulang H1
Badge (eyebrow) di atas H1 harus menambah makna, misalnya kalimat ajakan atau sudut pandang, bukan kata yang sudah ada di H1. Contoh yang ditolak user (4 Okt 2026): badge "Blog" + H1 "Blog Timebase". Contoh yang disetujui: "Pilih paket yang pas untuk tim Anda" (Harga), "Miliki software-nya, bukan sekadar menyewa" (White Label), "Pusat edukasi" (Blog).
Halaman SEO juga diberi field `eyebrow` di `data/brief.json` (contoh: "Ukur hasil, bukan jam duduk"), jangan dibiarkan memakai nama halaman. `build.py` (`check_badge`) memberi WARNING bila semua kata badge sudah ada di H1.

## 3e. Jarak H1 hero ke subjudul
H1 hero memakai `margin-bottom: 4px` di semua halaman, sama dengan H2 section (10px masih dinilai user "terlalu tinggi") (beranda, halaman SEO, Harga, legal, Panduan, Blog). Instruksi user (4 Okt 2026): "margin bawahnya kurangi, berlaku juga untuk semua halaman". Jangan memberi H1 hero jarak bawah yang lebih besar per halaman.

## 3f. Jarak atas halaman dokumen
Halaman dokumen (legal, artikel Panduan, artikel Blog) memakai band `dok-band` dengan `padding-top: 32px` (24px di mobile), bukan 64px seperti band biasa. Isinya langsung tampil di bawah hero. User (4 Okt 2026) pada artikel blog: "margin atasnya terlalu tinggi".

## 4. Elemen global yang selalu ada
- Header: logo kiri · menu tengah · Sign In + Langganan kanan (sticky, latar putih transparan + blur).
- Tombol WA melayang minimalis di kanan bawah.
- Footer berlatar abu muda, dengan ruang bawah untuk tombol WA di dalam footer.
- Satu kontainer (`--wrap`) untuk semua bagian, sehingga tepi kiri-kanan selalu segaris.

## Cek otomatis (`build.py`)
- **ERROR** jika ada section yang **hanya berisi teks** (tanpa poin, kartu, tabel, callout, blockquote, FAQ, atau gambar), atau **tanpa kalimat pembuka** setelah judul (kecuali FAQ).
- **WARNING** jika sebuah section punya > 2 paragraf, judul > 12 kata, ada paragraf > ±45 kata, atau **pembuka/catatan mengulang isi poin, kartu, atau caption** (≥3 frasa 4-kata yang sama, atau ≥2 angka yang sama).

## Warna & kontras
- **Semua tabel** (bukan hanya tabel harga): kotak tabel berlatar putih, header putih dengan font heading tebal dan garis bawah 2px warna tinta. Header bertint abu (`--bg-soft`) tidak terlihat di band abu (user: "bagian tabel aspek, langganan, white label kurang terlihat"). Header tabel biasa **berwarna beda dari isi**: latar ungu muda `#ece4ff` + garis bawah ungu 2px (user: "header tabelnya berikan warna yang berbeda"); header tabel harga tetap putih (sudah disetujui terpisah). Baris isi **belang (striped)**: baris genap abu netral `#f7f6f9` (user: "buat tabelnya jadi striped") agar tidak mirip warna header; tabel harga dikecualikan karena barisnya ikut switch bulanan/tahunan dan punya baris grup.
- Semua teks ≥4,5:1 (teks besar 3:1). `--muted` = #5f5870; logo cloud #736c88 (19px tebal); bintang & label callout amber tua #b45309.
- Elemen di permukaan gelap (`.cta`) menulis selektornya dengan `.prose .cta …` supaya tidak tertimpa warna teks isi halaman (kasus nyata: daftar syarat di CTA nyaris tak terlihat).

## Cek manual sebelum melapor selesai
1. Screenshot setiap halaman per band di 1440px dan 375px. Bandingkan dengan `contoh-ui/standar-section-disetujui.jpg`: kepadatan teks, ruang kosong, ukuran judul, dan dua kolom yang seimbang.
2. Pastikan tidak ada dua band berurutan dengan latar sama (batas harus terlihat).
3. Ukur tepi kiri-kanan dan overflow di 1440/1280/768/375px.
