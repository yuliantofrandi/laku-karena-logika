<!--
Dokumen ini adalah SINGLE SOURCE OF TRUTH rancangan strategi produk
software yang AKAN dikembangkan. Isinya selalu rancangan terkini — tidak menyimpan riwayat versi,
tidak ada decision log. Riwayat hidup di git, bukan di sini.

Skill hilir (brand-story-writer, company-profile-writer, content-ideator,
blog-content-writer) membaca dokumen ini apa adanya.

PENANDA (hanya ini, semuanya untuk skill hilir & reviewer):

[?]            — asumsi pasar/customer yang alasannya masih lemah (BUKAN
                 penanda fitur yang belum dibangun). Boleh dipakai sebagai sudut
                 pandang, TAPI jangan dijadikan klaim absolut di materi
                 publik ("terbaik", "nomor satu", "paling X").
[INPUT-NEEDED] — keputusan/data belum diberikan user. Skill hilir DILARANG mengarang
                 isian untuk bagian ini.
`[!]`          — catatan risiko yang harus dibaca sebelum memakai klaim
                 di dekatnya (mis. ketergantungan infrastruktur).

Teks tanpa penanda = berlaku dan aman dipakai.

Semua kapabilitas di dokumen ini adalah bagian produk yang DIRANCANG —
tidak dibedakan sudah dibangun, sudah rilis, atau masih rencana.

Keputusan strategis (positioning, target) disertai alasan singkat
"... — karena ...", supaya reviewer bisa menilai dasar keputusannya,
bukan cuma kesimpulannya. Harga TIDAK wajib beralasan — kelayakan harga
diuji business-reviewer.


ATURAN ANTI-DUPLIKASI
=====================
Satu fakta hanya boleh punya SATU rumah. Kalau tergoda menyalin ringkasan
ke section lain, jangan — cukup rujuk section aslinya. Dua salinan berarti
suatu saat satu direvisi dan satunya tertinggal.

Rumah tiap jenis fakta:
  identitas & arah        → §1      problem & value        → §4
  DNA, positioning, pasar → §2      harga & add-on         → §3
  segmen & persona        → §5      risiko struktural      → §2 blok [!]

KOMPETITOR TIDAK DITULIS DI SINI — tidak ada nama merek, harga, atau
fitur kompetitor. Cukup JENIS alternatif tanpa merek ("tool global
berbayar USD", "tool gratis", "Excel & grup WA"). Data & analisis
kompetitor adalah milik laporan business-reviewer.


URUTAN DOKUMEN vs URUTAN PENGISIAN
=================================
Letak section mengikuti kebutuhan PEMBACA (siapa kita → apa bedanya →
berapa harganya → apa nilainya → untuk siapa). Urutan PENGISIAN mengikuti
ketergantungan data:

  §1 identitas → §2 Opportunity → §4 P2V → §5 Target → §2 DNA & Positioning
  → §3 Pricing (PALING TERAKHIR — turunan dari segmen + value)

Positioning statement dan harga ditulis terakhir karena keduanya
sintesis dari section lain. Kalau harga berubah, §4 baris "Harga" dan §5
"Skema yang ditawarkan" wajib ditinjau ulang.
-->

## 1. Business Overview

<!-- Identitas dan arah. Bagian yang hampir tak pernah berubah — saat
pivot, yang disentuh adalah §2, bukan section ini. -->

### Product name
...

### Vision

<!-- KE MANA — tujuan perjalanan, ditulis sebagai KEADAAN yang tercipta,
bukan kegiatan kita dan bukan sekadar angka penjualan.

  "Membantu 1.000 klien"                  → pencapaian kita (lemah)
  "1.000 usaha punya presensi rapi
   tanpa ribet pada 2030"                 → keadaan yang tercipta;
                                            angkanya melekat pada perubahan

Boleh berskala & terukur, sebaiknya bertanggal. Vision berskala punya
masa berlaku — begitu tercapai, tetapkan yang baru. -->

> ...

### Mission

<!-- KENAPA produk ini ada bagi customer — apa yang customer DAPATKAN
KEMBALI, bukan fitur apa yang kita berikan. Kalau kalimatnya menyebut
teknologi atau mekanisme, itu sudah deskripsi produk — mekanismenya ada
di §2 DNA.

Beda dengan Vision: vision bisa selesai, mission tidak. -->

> ...

## 2. Brand Strategy

<!-- Apa yang membuat produk ini beda, dan di pasar seperti apa.

Urutan pengisian di dalam section ini:
  1. Category      — identitas kategori, jarang berubah
  2. Opportunity   — gambaran pasar, paling awal
  3. Level 1 & 2   — setelah tahu apa yang sulit ditiru
  4. Positioning   — PALING TERAKHIR; sintesis Opportunity, DNA, §4, §5,
                     dan jenis alternatif (tanpa merek) dari Opportunity
  5. Tagline       — hanya MENCATAT yang sudah ditetapkan user -->

### Category

<!-- Satu frasa: jenis produk + pembeda kategori. Ini yang dipakai
pembaca untuk menaruh produk di kotak yang benar — bukan tagline. -->

> ...

### Level 1 — DNA · paling sulit ditiru

<!-- Inti produk; kalau hanya boleh menyebut satu hal, ini yang disebut.
Diurutkan dari yang paling SULIT DITIRU, bukan paling mengesankan —
fitur paling canggih biasanya justru paling cepat disalin.

TO THE POINT: satu baris tebal per pembeda, langsung dipahami orang
awam tanpa penjelasan. Tanpa label abstrak + keterangan, tanpa "karena",
tanpa alasan kenapa sulit ditiru. Maks ±12 kata.
  ✗ **Setup Minimal**: karyawan cukup kirim foto — tanpa install app, ...
  ✓ **Absen cukup kirim foto di WhatsApp, tanpa install aplikasi** -->

> **...**

### Level 2 — Pembeda pendukung · kuat saat rilis, bisa dikejar 1-2 tahun

<!-- Kuat saat produk rilis, tapi kompetitor bisa menyusul. Boleh jadi pendukung
headline, tidak boleh jadi headline utama.

Format sama dengan Level 1: satu baris tebal per pembeda, to the point,
tanpa keterangan atau alasan.

Syarat masuk pasar (yang semua kompetitor juga punya) TIDAK perlu
ditulis — dan jangan pernah dijadikan headline. -->

> **...**

### Positioning

<!-- SATU-SATUNYA rumusan strategi di dokumen ini. Jangan menambah
"pitch" atau ringkasan versi lain — semuanya rakitan ulang bahan yang
sama dan harus ditulis ulang setiap positioning berubah.

Kerangka: [product] adalah [category] — [cara kerja inti dari DNA],
[pembeda vs alternatif], dengan opsi [Level 2] untuk [segmen yang butuh].

Bahannya: category di atas · DNA Level 1 · problem dari §4 · segmen dari
§5 · alternatif dari Opportunity di bawah (termasuk status quo:
Excel, grup WA, proses manual). -->

> ...

### Tagline

<!-- MENCATAT tagline yang sudah ditetapkan user, bukan mengarang baru. Tagline
baru adalah keluaran brand-story-writer. Kosongkan kalau belum ada.

Cek: apakah tagline menjual DNA Level 1? Tagline yang menonjolkan
Level 2 berarti menjual keunggulan yang mudah ditiru. -->

> _..._

### Opportunity

<!-- Menjawab "kenapa sekarang dan di mana celahnya" — soal
PASAR, bukan soal produk kita. Alasan customer memilih kita ada di DNA.

Celah pasar ditulis sebagai kebutuhan yang tidak terlayani JENIS
alternatif yang ada — tanpa nama merek, harga, atau fitur kompetitor.
Apakah celahnya benar-benar kosong diuji business-reviewer. -->

- **Kenapa sekarang:** perubahan yang membuat kebutuhan ini mendesak
  belakangan — teknologi jadi murah, regulasi, perubahan perilaku. ...
- **Celah pasar:** kebutuhan yang tidak terlayani jenis alternatif yang
  ada (tanpa merek). ... — [product] lebih cocok karena ...

> `[!]` **Catatan risiko:** <!-- ketergantungan atau ancaman struktural
> yang bisa mematikan klaim di atas. Hapus blok ini kalau tidak ada. -->

## 3. Pricing Plan

<!-- DIISI PALING TERAKHIR — turunan dari §4 (value) dan §5 (segmen).

Pola: tier dibedakan oleh KAPABILITAS (bukan oleh ukuran perusahaan);
ukuran perusahaan menentukan DISKON VOLUME di dalam tiap tier. Tahunan
= bayar 10 bulan dapat 12, tulis juga harga efektif per bulan supaya
bisa dibandingkan langsung dengan harga bulanan.

Baris fitur di bawah harga: ✓ atau kosong, satu baris per kapabilitas
dari §4 — jadi pembaca bisa memetakan value ke harga tanpa bolak-balik.

Tulis asumsi di bawah tabel kalau ada (mis. "harga sudah mencakup
infrastruktur"). Alasan "kenapa harga ini" TIDAK wajib — kelayakan
harga diuji business-reviewer. -->

| **Harga Bulanan / Karyawan** | **Skema 1 — ...** | **Skema 2 — ...** |
| --- | --- | --- |
| < ... | Rp ... | Rp ... |
| < ... (Rp ... lebih murah) | Rp ... | Rp ... |
| > ... (Rp ... lebih murah) | Rp ... | Rp ... |
| **Harga Tahunan / Karyawan**<br>(bayar 10 bulan, dapat 12) | **Skema 1 — ...** | **Skema 2 — ...** |
| < ... | Rp ...<br>(Rp .../bln) | Rp ...<br>(Rp .../bln) |
| **Fitur** | | |
| ... | ✓ | ✓ |
| ... | | ✓ |
| Dukungan | Chat, jam kerja | Chat prioritas |

Harga sudah mencakup ... <!-- asumsi yang perlu diketahui pembaca -->

### Add-on (bisa dipasang ke Skema 1 atau Skema 2)

<!-- Tabel terpisah — JANGAN taruh add-on sebagai baris di tabel harga
skema. Sesuaikan judul dengan skema yang bisa memasangnya. Harga tahunan
opsional di bawah harga bulanan: "+Rp .../karyawan/bln<br>(Rp .../thn)". -->

| Add-on | Harga | Fitur yang didapat |
| --- | --- | --- |
| ... | +Rp .../karyawan/bln | ... |

Add-on dijual terpisah dari skema dan tidak ikut diskon volume. ...

## 4. Product-to-Value Mapping

<!-- Section paling penting untuk content-ideator dan company-profile-
writer. Setiap baris = bahan mentah ide konten dan copy website.

RUMAH TUNGGAL untuk problem sekaligus value. Jangan membuat daftar
"Problems" atau ringkasan value di §1/§2.

URUTKAN dari problem yang paling menyakitkan, bukan per kelompok fitur —
urutan ini jadi prioritas content-ideator.

Dua kolom benefit dipisah karena pembacanya beda orang:
  Benefit          — yang dirasakan END-USER (pemakai harian)
  Business Outcome — yang dirasakan DECISION-MAKER (pembayar)

Kalau kapabilitas hanya ada di tier/skema/add-on tertentu, sebut di
kolom Capability: "(tier X)", "(bagian dari Skema 2)", "(add-on Y)".
Harga sendiri boleh jadi satu baris — "bayar hanya modul yang dipakai"
adalah value.

Problem yang BELUM terjawab kapabilitas yang dirancang tetap dicatat, kolom Capability
diisi [GAP] — kalau tidak, problem itu hilang dari pandangan. -->

| Product Capability | Customer Problem | Benefit<br>(end-user) | Business Outcome (decision-maker) |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
| ... | ... | ... | ... |

## 5. Target Customer Profile

<!-- Kriteria tingkat PERUSAHAAN di Primary/Secondary Market; atribut
ORANG (goals, pain, trigger) di Buyer Personas. Jangan dicampur.

Tiap market wajib menyebut SKEMA yang ditawarkan (rujuk §3) — ini
penghubung segmen ke harga, dan jadi sinyal ke sales/konten skema mana
yang dipimpin untuk siapa.

Sebut juga siapa yang BUKAN target dan kenapa — itu mencegah skill hilir
menulis konten untuk segmen yang tidak akan membeli. -->

### Primary Market

- **Industry:** ...
- **Company size:** ... — titik masuk paling kuat di ...
- **Geography:** ...
- **Business type:** ciri operasional yang membuat problem di §4 paling
  terasa. ...
- **Kematangan teknologi:** ... **Bukan** target: ... (karena ...)
- **Skema yang ditawarkan:** ... — karena ...

### Secondary Market

- ... — masuk tier ..., karena ...
- **Skema yang ditawarkan:** ... — karena ...

### Buyer Personas

<!-- Persona 1 = yang MEMUTUSKAN & membayar. Persona 2 = yang MEMAKAI
tiap hari. Untuk persona yang bukan pembeli, tulis "*(bukan pembeli —
...)*" di Buying Motivation/Trigger supaya skill hilir tidak menulis
CTA beli untuk mereka.

Buying Trigger = KEJADIAN spesifik yang memicu pembelian (kecurangan
ketahuan, salah hitung gaji, buka cabang baru), bukan keinginan umum. -->

#### Persona 1 — Decision Maker

| Aspek | Detail |
| --- | --- |
| Role | ... (Primary Market) — atau ... (Secondary Market) |
| Goals | ... |
| Pain Points | ... |
| Buying Motivation | ... |
| Buying Trigger | ... |

#### Persona 2 — End User

| Aspek | Detail |
| --- | --- |
| Role | ... |
| Goals | ... |
| Pain Points | ... |
| Buying Motivation | *(bukan pembeli — dipengaruhi kemudahan pakai)* ... |
| Buying Trigger | *(bukan pembeli)* ... |
