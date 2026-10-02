# Aturan Sales Page (Beranda & Landing Ads)

Tujuan: konversi tinggi **tanpa** klaim yang tidak bisa dipertanggungjawabkan. Framework halaman = **AIDA**; blok Interest memakai **PAS**.

## Urutan blok beranda

| # | Blok | Tahap | Isi wajib |
|---|---|---|---|
| 1 | Hero | Attention | **Layout hero tetap (lihat "Hero" di bawah).** H1 = hasil terbesar untuk klien, bukan nama/fitur produk. **Singkat, satu ide, ≤55 karakter, tanpa anak kalimat setelah tanda pisah** (contoh yang disetujui user: "Tahu Pasti Apa yang Dikerjakan Tim Remote Anda"). Keberatan dijawab di subjudul atau section lain |
| 2 | Paragraf entitas | — | "<Brand> adalah <category BKB> untuk <segmen>…" untuk Google & mesin AI. Primary = nama brand |
| 3 | `{{bukti_sosial}}` | Interest | Metrik + logo/industri klien |
| 4 | Problem | Interest (P) | Situasi pembeli dengan bahasanya sendiri (BKB Persona 1 Pain Points) |
| 5 | Agitation | Interest (A) | Kerugian **waktu** dan **uang** dengan hitungan transparan (rumusnya ditulis), plus kerugian emosional (kepercayaan tim) |
| 6 | Solution | Interest (S) → Desire | Kapabilitas inti BKB §4 dalam 3–4 kartu + link ke halaman Prioritas 1 |
| 7 | Cara kerja | Desire | 3 langkah sampai aktif, sesuai model penjualan. Self-serve: Pilih skema → Bayar, akun aktif → Pasang/onboarding. Mengurangi kesan "ribet" |
| 8 | Penanganan keberatan | Desire | Keberatan terbesar Persona 1/2 (mis. "dicap mata-mata") dijawab dengan checklist fakta |
| 9 | `{{testimoni}}` | Desire | 3 kutipan: masalah → hasil, nama berinisial, jabatan, jenis perusahaan + kota, **dengan foto bulat pemberi testimoni** (aturan user: "agar lebih terlihat real"). Foto harus orang asli dengan izin (`foto` di social-proof.json, WebP ≤40 KB); sebelum ada → avatar inisial bergradasi. **Jangan** foto stok/wajah AI |
| 10 | ~~Harga~~ → hanya `{{tanpa_risiko}}` | Desire → Action | **Harga hanya di halaman Harga** (aturan user: "tidak perlu harga di semua page, cukup di menu harga saja"). Beranda dan landing produk menjelaskan paket tanpa angka + tautan ke menu Harga; blok jaminan tetap ada. Build ERROR bila token harga (`pricing_*`, `addon_*`, `harga_mulai`) dipakai di luar `pricing_page`, dan WARNING untuk angka "Rp" di teks. Ketentuan di bawah ini hanya untuk halaman `/harga`: **Switch Bulanan/Tahunan** (wajib), lalu kartu skema masing-masing dengan tombol beli (`Pilih <Nama Paket>` → checkout `{paket}` + `{periode}` sesuai switch); satu "Disarankan" (sesuai BKB §5); lalu risk reversal |
| 11 | ~~Urgensi~~ → masuk CTA penutup | Action | Tidak jadi section sendiri (user: "dua section ini punya pesan yang sama, gabung jadi 1"). Alasan mulai sekarang ditulis sebagai frasa pendek di `copy.cta_poin` |
| 12 | ~~Jujur soal batas~~ | — | **Tidak di beranda** (user: "section ini sepertinya tidak perlu"). GAP BKB tetap wajib ditulis jujur di halaman fitur yang relevan (callout `honest`), bukan dihapus |
| 13 | FAQ | Action | Keberatan terakhir: kontrak, reaksi tim, lama aktif, siapa yang tidak cocok |
| 14 | `{{cta}}` | Action | **Satu-satunya tempat urgensi + jaminan.** Dua kolom di blok gelap: kiri judul + 1 kalimat pendek + 2 tombol; kanan **satu daftar centang `copy.cta_poin`** (maks 4 frasa ≤6 kata: urgensi + jaminan, tanpa label). User: "terlalu banyak teks". Jaminan lengkap (`pricing.json terms` + `copy.risk_extra`) hanya di /harga. `{{tanpa_risiko}}` tidak dipakai lagi bersama `{{cta}}` (build WARNING) |

Landing Ads (Prioritas 1): pakai format halaman SEO (aturan-konten), lalu sisipkan `{{bukti_sosial}}` setelah paragraf pertama, serta `{{tanpa_risiko}}` + `{{testimoni}}` sebelum blok penutup.

## Elemen psikologi — dan batas kejujurannya

| Elemen | Lakukan | Jangan |
|---|---|---|
| **Killer headline** | Hasil untuk klien + jawaban atas ketakutannya | Superlatif ("terbaik", "#1") |
| **Agitasi** | Hitungan dengan asumsi tertulis (mis. 20 orang × 15 menit × 22 hari = 110 jam) | Angka statistik pasar tanpa sumber |
| **Social proof** | Data asli. Atas permintaan user boleh **data contoh yang terlihat asli** untuk preview, di `data/social-proof.json` dengan `"contoh": true` | Menerbitkan data contoh. Build menolak publish selama masih ada `contoh: true` |
| **Rating bintang (schema)** | `AggregateRating` dibuat otomatis **hanya** dari testimoni `contoh: false` yang tampil di halaman | Rating karangan: melanggar kebijakan review snippet Google, berisiko manual action |
| **Risk reversal** | Hanya yang benar berlaku (pilihan user): bulanan berhenti kapan saja, trial, garansi + syaratnya, bantuan pemasangan | Menjanjikan trial/garansi yang belum diputuskan |
| **Scarcity/urgency** | Default **urgensi alami**: biaya per bulan menunda, data tidak bisa dibuat mundur, regulasi yang sudah berlaku. Promo hanya jika asli (kuota + tanggal berakhir nyata) | Kuota palsu, hitung mundur palsu |
| **CTA** | Kata kerja + kepemilikan, sesuai model penjualan. Self-serve: "Aktifkan <Produk> untuk Tim Saya", "Pilih Bukti Visual", "Bandingkan Paket" | "Kirim", "Submit", "Klik di sini"; CTA demo untuk produk yang dijual langsung langganan |
| **Anchoring harga** | Skema termahal di kanan, skema yang disarankan di tengah dengan badge | Coret harga palsu |

## Teks CTA & copy global

Semua teks yang dipakai berulang ada di `site.json → copy` (`nav_cta`, `cta_primary`, `cta_secondary`, `cta_title`, `cta_text`, `plan_button`, `wa_title`, `wa_subtitle`, `risk_label`, `risk_extra`, `proof_caption`). Ubah di sana, jangan di `build.py`.

## Hero (layout tetap dari referensi user — semua halaman)

Dirender otomatis oleh `build.py`, sama di semua halaman:
1. **Badge pill** (`.eyebrow`): bingkai tipis, teks bergradasi brand. Beranda memakai `site.json → eyebrow` (slogan brand); halaman lain memakai nama halaman (atau `eyebrow` di `extra_pages`).
2. **H1** besar, warna tinta gelap (bukan teks gradasi), font heading `--font-head` (Montserrat 800, di-host sendiri, `font-display:optional` + preload → tanpa render-block dan tanpa CLS). H1 > 55 karakter diberi kelas `long` dan diperkecil.
3. **Subjudul** = `<!-- lead: … -->` di konten. Isinya teks saja, jangan memasukkan tombol.
4. **Satu tombol CTA** gradasi besar + panah "→": `copy.cta_primary` ke checkout. Di `/white-label` tombolnya mengarah ke WA penawaran.
5. **Baris 3 statistik** dari `data/social-proof.json → metrics` (3 pertama). Hanya fakta, atau data contoh yang memblokir publish. Jangan klaim yang bertentangan dengan produk (mis. "24/7 Monitoring" untuk produk yang hanya mencatat sesi kerja). Strip bukti sosial di isi halaman hanya berisi logo/industri agar angka tidak dobel.
6. **Gambar kanan** di atas **bentuk gradasi brand** yang membulat (pseudo-element), dengan gambar sedikit keluar dari bentuknya. **Gambar/video tetap tegak; yang miring hanya bentuk gradasinya** (±2,5°; user: "videonya jangan miring, buat background belakangnya saja yang miring"). Bentuknya **kecil, sekadar pemanis**: `span.hero-media:before` dengan `inset:-5px -6px`, hanya garis tipis di tepi media (user: "jangan kelihatan besar, hanya pemanis muncul sedikit saja", lalu "kecilkan lagi agar tidak mengganggu area video"). Bentuknya digeser `translate(16px,0)` sehingga hanya mengintip di sisi kanan media ("geser ke kanan sedikit sehingga tidak di area tengah video", lalu "geser ke atas sedikit"). Media hero diberi bayangan **rapat tapi pekat** (`0 1px 2px .28` + `0 4px 10px .30` + `0 16px 32px -12px .38`) agar batas media vs bentuk gradasi tegas (user: "shadownya tipis namun agak tebal, untuk menekankan perbedaan antara layer utama dengan layer background"); aturan video potret di section memakai `:not(.hero-img)` supaya tidak menimpa bayangan hero. Gambar hero beranda idealnya **foto orang memegang laptop berisi dashboard, latar transparan**. Tulis ini di `brief`, karena Claude tidak bisa membuat foto.
- Breadcrumb tidak tampil (badge menggantikannya); BreadcrumbList tetap ada di JSON-LD.

## Nama paket, bukan "Skema N" (wajib)

Koreksi user: "di bagian harga tidak perlu ada tulisan skema, langsung jadikan teks di bawahnya jadi nama paketnya". Di website, setiap tingkatan harga tampil dengan **nama paketnya** (untuk Timebase: Aktivitas · Bukti Visual · Waktu Per Tugas), bukan "Skema 1/2/3".
- `data/pricing.json → schemes[].name` = nama paket. `id` hanya untuk checkout (`{paket}`/`{skema}` di `checkout_url`).
- Kartu, header tabel, tombol (`Pilih <Nama Paket>`), tabel add-on, dan schema Offer (`<Brand> <Nama Paket>`) memakai nama paket.
- Di teks halaman, sebut "paket <Nama>" (awal kalimat: "Paket <Nama>"). Kata umum "skema" diganti "paket" (mis. "Bandingkan Paket", "Pilih paket").
- BKB boleh tetap memakai istilah Skema. Pemetaannya dilakukan saat menyalin ke `pricing.json`, bukan dengan mengedit BKB.

## Satu tampilan harga per halaman (wajib)

Aturan tetap user: "tabel harganya cukup 1 saja". Setiap halaman memuat **paling banyak satu** dari `{{pricing_cards}}` / `{{pricing_table}}` (build ERROR bila lebih).
- `/harga` → `{{pricing_table}}` saja: satu tabel lengkap (switch, harga per jumlah karyawan, fitur) dengan tombol beli **hanya di bawah tabel** (footer). User: "tidak perlu tombol di bagian atas". Sel pojok kiri atas tanpa label terlihat ("label ini hilangkan"); teks "Jumlah karyawan" tetap ada sebagai `.sr-only` untuk pembaca layar. **Header tabel menonjol** ("buat headernya lebih kelihatan"): baris header gelap (`--ink`), teks putih font heading 19px (15px di mobile), kolom paket disarankan bergradasi ungu→pink (tanpa oranye, demi kontras teks putih) dengan label kecil "Disarankan".
- Halaman lain (beranda, landing Prioritas 1) → `{{pricing_cards}}` saja (ringkas + link ke `/harga`).
- Mobile: tabel bisa digeser dengan kolom kiri dan judul grup tetap di tempat (sticky), teks panjang dipatahkan, dan ada petunjuk "Geser ke kanan untuk melihat semua skema →". Skema yang disarankan harus tetap mudah ditemukan.

## Switch harga Bulanan / Tahunan (wajib)

Aturan tetap user: bagian harga **selalu** punya tombol switch Bulanan/Tahunan, baik di kartu (`{{pricing_cards}}`) maupun di tabel lengkap (`{{pricing_table}}`). Keduanya otomatis dari `build.py`.
- **Tanpa JavaScript:** dua radio tersembunyi + label pil; isi `.bln` / `.thn` ditampilkan/disembunyikan lewat CSS sibling selector. Bisa dipakai dengan keyboard (panah kiri/kanan) dan punya fokus terlihat. Kedua harga tetap ada di HTML, jadi aman untuk SEO.
- **Default Bulanan.** Label Tahunan menyebut penghematan dari data (`12 − annual_months_paid`, mis. "Hemat 2 bulan").
- **Tahunan:** harga setara per bulan sebagai angka besar, total per tahun + aturan tahunan sebagai keterangan, tombol beli membawa `periode=tahunan`.
- Radio tersembunyi diletakkan di posisi switch (`top:40px; left:50%`) supaya klik tidak menggeser halaman.

## Halaman White Label (wajib di setiap produk)

Semua produk SaaS/GaaS user bisa dibeli dengan merek sendiri. Halaman `/white-label` memakai **copy global** (`assets/starter/content/white-label.html`), jadi tidak ditulis ulang per produk. Bagian khusus produk masuk lewat token.

| Blok | Isi |
|---|---|
| Hero | H1 memuat "White Label" + hasil: jual software dengan merek sendiri tanpa membangun dari nol. CTA `Minta Penawaran White Label` (WA, teks otomatis menyebut brand) + `Lihat Cara Kerjanya` |
| Paragraf entitas | "Program whitelabel <Brand> …" + `{{deskripsi_kecil}}` |
| Untuk siapa | Konsultan & agensi · software house & integrator · reseller & distributor · grup & asosiasi |
| Agitasi | Membangun sendiri: waktu, biaya tetap, pemeliharaan tanpa akhir, risiko produk. **Tanpa angka karangan** |
| Perbandingan | Tabel "White label vs membangun sendiri" (perbandingan metode, aman) |
| Yang dijual | `{{daftar_solusi}}` dari menu group Solusi + link ke harga |
| Kustomisasi / ditangani | `{{wl_kustomisasi}}`, `{{wl_ditangani}}` dari `site.json → whitelabel` (dikonfirmasi per produk) |
| Cara kerja | Konsultasi → Penawaran & kesepakatan → Penyiapan brand → Rilis ke klien |
| Keuntungan | Produk sendiri tanpa tim dev · pendapatan berulang · klien tetap milik Anda · cepat ke pasar · ikut pembaruan |
| FAQ | Apa itu whitelabel · apakah klien melihat merek kami · harga (per penawaran) · perlu tim IT? · beda dengan langganan biasa |
| CTA | `{{cta_whitelabel}}`: konsultasi WA, **bukan checkout**, karena whitelabel adalah penawaran per klien |

Larangan: tidak menyebut harga, minimum lisensi, bagi hasil, atau persentase penghematan yang belum diputuskan user. Halaman ini sengaja tidak memakai `{{bukti_sosial}}`/`{{testimoni}}` sampai ada mitra whitelabel asli.

## Tampilan: band dua kolom, teks sekunder dilipat

Koreksi user: "tampilan kurang bagus, banyak blank space, terlalu banyak tulisan yang dibaca". `build.py` (fungsi `layout_sections`) menata isi secara otomatis, jadi konten cukup ditulis sebagai urutan H2 → 1–2 kalimat → poin/kartu → gambar → blok:
- **Band per H2** dengan latar bergantian, **dimulai dari abu muda (`.band.alt`)** tepat setelah band intro yang putih. Kalau dimulai dari putih, band intro dan section pertama terlihat menyatu (dikoreksi user: "2 section ini seperti gabung?"). Blok sebelum H2 pertama menjadi **band intro**, dan `{{cta}}` menjadi band penutup.
- **Band intro** (dikoreksi user: "UI layout-nya masih kurang"): strip bukti sosial tampil **tepat di bawah hero** sebagai *logo cloud* tanpa kotak (label kecil + deretan nama/logo abu-abu, garis tipis pemisah), lalu paragraf pengantar 1–2 kalimat sebagai **pernyataan rata tengah** (maks ±820px; rata kiri di mobile).
- **Ada gambar** (`{{gambar:…}}`) → dua kolom teks | gambar, bergantian kiri-kanan (`.split.media`, `.flip`). **Tanpa gambar** → judul kiri (sticky) | isi kanan (`.split.head`). Di mobile semuanya menumpuk.
- **Blok lebar** (`grid`, `table-wrap`, `periode`, `plans`, `quotes`, `proof`) tampil selebar kontainer di bawah baris dua kolom.
- **Tanpa "Baca selengkapnya" / teks tersembunyi** (koreksi user: "saya tidak suka ada baca selengkapnya, karena rata-rata orang tidak klik ini"). Semua teks selalu terlihat, jadi **teks harus ditulis ringkas sejak awal**:
  - Setiap section: **H2 → 1–2 kalimat (≤ ±30 kata) → elemen yang bisa dipindai**: `ul.checks` (poin pendek dengan awalan tebal), `div.grid` berisi `.card` (judul + 1 kalimat, `span.num` untuk langkah), tabel kecil, atau callout.
  - Hindari dua paragraf berturut-turut. Kalimat penutup/rujukan ditulis sebagai `p.note` dengan link.
  - Build memberi WARNING untuk paragraf > ±45 kata.
  - FAQ tetap memakai accordion `<details class="faq">` (pola yang dikenal pengunjung), dengan jawaban 1–2 kalimat.
- **Jumlah kata:** karena isinya dipadatkan, halaman brief cukup **≥ 700 kata (ERROR di bawahnya)**, dengan target keyword plan 1.000–1.500 (WARNING di bawah 1.000). Tambah kedalaman lewat kartu, tabel, atau FAQ yang berguna, bukan paragraf pengisi.

## Layout: satu kolom, tepi kiri-kanan segaris

- Header, hero (breadcrumb, H1, lead), setiap band, dan footer memakai **satu kontainer yang sama** (`.wrap`, `--wrap: 1160px`, padding 20px). Kolom-kolom berada *di dalam* kontainer itu. Jangan memberi hero/header kolom lebar dan isi kolom sempit: tepi kiri judul dan isi jadi tidak segaris, dan user menilainya "tidak rapi".
- Tidak ada blok yang keluar dari kontainer. Kartu, tabel, testimoni, dan CTA mengikuti lebar kontainer.
- Verifikasi di Langkah 4 dengan mengukur tepi kiri-kanan semua halaman di 1440/1280/768/375 px (lihat SKILL.md).

## Navigasi

- **Tata letak header (aturan tetap user):** Logo di kiri · **semua menu di tengah** (tepat di tengah header) · di kanan tombol **"Sign In"** (sekunder/outline, ke `signin_url`) lalu tombol **Langganan** (utama, ke checkout). Grid 3 kolom `1fr auto 1fr`; `.nav-panel` memakai `display:contents` di desktop dan menjadi panel hamburger di mobile (menu, lalu Sign In + Langganan berdampingan). Dropdown Solusi muncul tepat di bawah tengah item-nya.
- Menu utama ringkas: **satu menu group** untuk halaman solusi/landing (mis. "Solusi ▾" → Monitoring, Time Tracking, Kerja Remote, Absensi Hybrid, masing-masing dengan deskripsi 1 baris), lalu **White Label** (wajib), lalu **Harga**, lalu tombol CTA. Halaman panduan/SEO cukup di footer.
- Dropdown memakai `<details>`/`<summary>` (tanpa JavaScript). Panel rata kanan agar tidak terpotong di layar sempit; di mobile tampil inline di dalam menu hamburger. Group diberi tanda aktif saat salah satu submenunya sedang dibuka.

## Konversi teknis

- CTA utama = link ke `checkout_url` (template `{skema}`, `{periode}`), `rel="nofollow"`. Kosong = ke `/harga#pilih-skema`.
- **Tombol WA marketing melayang di bagian bawah SETIAP halaman, desktop & mobile** (aturan tetap user). Bentuk dari contoh user, **minimalis, warna dari design system produk** (bukan warna gambar contoh): latar solid `--ink`, tanpa bingkai gradasi, bayangan tipis, **padding lega dan teks kecil** (desktop: padding 12/22px, judul 14px, subjudul 11.5px; mobile: padding 10/16px, judul 12.5px, subjudul 10.5px), ikon WhatsApp hijau di kiri (SVG inline, boleh tetap hijau agar mudah dikenali), judul tebal putih `copy.wa_title` ("Hubungi Kami !!"), dan subjudul `copy.wa_subtitle` ("Konsultasi 100% Gratis"). Link `wa.me/<whatsapp>?text=<whatsapp_text>`, `target="_blank" rel="nofollow noopener"`.
  - Desktop: pojok kanan bawah. Ruang agar teks footer tidak tertutup diberikan sebagai **`padding-bottom` di `.site-footer`** (±92px desktop, ±76px mobile), **bukan di `body`**. Padding di `body` membuat area putih di bawah latar footer (dikoreksi user: "ada blank space").
  - Mobile (≤640px): **hanya tombol WA**, versi ringkas di kanan bawah (±181×49 px, <3% layar). **Judul + subjudul tetap tampil.** Jangan tambahkan tombol lain di bar bawah, dan jangan dibuat selebar layar.
  - Tanpa widget/skrip chat pihak ketiga. WA dipakai untuk konsultasi, bukan pengganti checkout dan bukan "jadwalkan demo".
- Konversi Google Ads dipasang pada **pembayaran berhasil** (klik tombol beli sebagai konversi sekunder) **sebelum** iklan jalan.
