# Aturan Penulisan & Uji Kualitas per Section

Dipakai saat MENGISI atau MEREVIEW isi. Tiap section punya uji yang harus
lolos sebelum dianggap selesai. Contoh di bawah diambil dari Timelog, produk
SaaS nyata yang dipakai memvalidasi struktur ini — sekadar ilustrasi
"lolos/gagal", bukan folder yang harus ada di mesin Anda.

## Prinsip umum

1. **Satu fakta satu rumah.** Sebelum menambah kalimat, tanya: sudah ada di
   section lain? Kalau ya, rujuk ("lihat §4"), jangan salin. User berulang
   kali memangkas duplikasi — jangan menambah pekerjaan itu.
2. **Rancangan terkini.** Tidak ada "sebelumnya kami...", tidak ada
   decision log, tidak ada versi di badan dokumen. Riwayat hidup sebagai
   snapshot bernomor di `<produk>/sebelumnya/`.
3. **Keputusan = kesimpulan + alasan.** Pola `... — karena ...`. Reviewer
   menilai dasarnya, bukan hasilnya. **Kecuali DNA Level 1 & 2** — keduanya
   ditulis tanpa alasan (lihat §2), dan harga §3 yang tidak wajib
   beralasan.
4. **Angka mengalahkan sifat.** "Lebih hemat" lemah; "cukup Rp 5.000/
   karyawan/bln, tanpa biaya setup" kuat. Angka keputusan kita (harga,
   batas tier, diskon) → tetapkan rekomendasi terbaik. Angka fakta pasar
   yang belum ada sumbernya → `[INPUT-NEEDED]`. Angka di sini angka
   produk sendiri atau pasar — bukan angka kompetitor (prinsip 7).
5. **Bahasa:** Indonesia, ringkas, tanpa jargon marketing kosong. Istilah
   teknis/kategori boleh Inggris kalau memang begitu dipakai di pasar
   (Decision Maker, End User, Primary Market).
6. **Format:** heading `##` bernomor untuk section, `###` sub, `####` untuk
   persona. Kutipan `> ...` untuk pernyataan inti (vision, mission,
   category, DNA, positioning, tagline). Tabel untuk data terstruktur.
   Tidak ada H1 — nama produk cukup di folder dan field Product name.
7. **Tanpa kompetitor.** Tidak ada nama merek, harga, atau fitur kompetitor
   di section mana pun — hanya jenis alternatif tanpa merek. Lihat
   "Kompetitor tidak ditulis di BKB" di akhir berkas ini.
8. **Rancangan, bukan laporan kondisi.** BKB merancang strategi produk
   software yang akan dikembangkan. Semua kapabilitas ditulis sebagai
   bagian produk yang dirancang — tanpa membedakan sudah dibangun, sudah
   rilis, atau masih rencana. Status pengembangan bukan alasan memberi
   `[?]`/`[INPUT-NEEDED]` atau menahan klaim di DNA, Positioning, Tagline,
   dan Pricing.
9. **Pikirkan versi terbaik.** Rancang dan tulis strategi paling kuat dan
   ambisius yang masuk akal untuk produk ini. Klaim superlatif ("terbaik",
   "paling cepat", "satu-satunya") boleh ditulis dan **tidak** diberi
   `[?]` — jangan melunakkan klaim demi aman. Menguji apakah klaim itu
   bertahan di pasar adalah tugas `business-reviewer`.
10. **Pilihkan rekomendasi terbaik.** Tujuan BKB adalah membuat produk
    laris. Setiap keputusan strategis yang belum diputuskan user — segmen,
    DNA, positioning, skema, harga, add-on, tagline — diisi dengan pilihan
    yang paling mungkin menang di pasar, bukan dibiarkan `[INPUT-NEEDED]`
    atau diisi opsi tengah yang aman. Pertanggungjawabannya diuji
    `business-reviewer`.

## §1 Business Overview

**Vision — uji:**
- Ditulis sebagai keadaan yang tercipta di dunia, bukan kegiatan kita.
  ✗ "Membantu 1.000 usaha" · ✓ "1.000 usaha di Indonesia punya presensi
  karyawan yang rapi tanpa ribet — berapa pun jumlah karyawannya — pada 2030."
- Ada angka + tanggal → punya masa berlaku.
- Tidak menyebut mekanisme/fitur.

**Mission — uji:**
- Menjawab apa yang customer dapatkan kembali, bukan apa yang kita lakukan.
  ✓ "Membuat administrasi karyawan berhenti jadi beban — cukup pakai yang
  sudah ada, tanpa pindah sistem apa pun."
- Tidak bisa "selesai" (beda dengan vision).
- Kalau menyebut teknologi → itu deskripsi produk, pindahkan ke DNA.

## §2 Brand Strategy

**Category:** satu frasa yang menaruh produk di kotak yang benar; boleh
menyertakan pembeda kategori. ✓ "Alat presensi karyawan berbasis WhatsApp
+ verifikasi AI".

**Level 1 DNA — uji:**
- **To the point.** Satu baris tebal per pembeda, maks ±12 kata, yang
  langsung dipahami orang awam apa bedanya bisnis ini. Tidak ada label
  abstrak + keterangan, tidak ada "karena", tidak ada alasan kenapa sulit
  ditiru, tidak ada perbandingan panjang.
  ✗ "**Setup Minimal**: karyawan cukup kirim foto — tanpa install app,
  tanpa atur jadwal atau shift dulu, presensi langsung jalan."
  ✓ "**Absen cukup kirim foto di WhatsApp, tanpa install aplikasi**"
- Kalimatnya sendiri harus menjelaskan pembedanya — kalau butuh keterangan
  tambahan supaya dipahami, tulis ulang kalimatnya, jangan menambah
  penjelasan.
- Pilih yang paling sulit ditiru, bukan yang paling canggih — tapi alasan
  sulit ditirunya tidak ditulis. Apakah benar sulit ditiru diuji
  `business-reviewer`.

**Level 2 — uji:** kuat saat produk dirilis, tapi bisa dikejar 1-2 tahun.
Format sama dengan Level 1: satu baris tebal per pembeda, to the point,
tanpa keterangan atau alasan. ✓ "**Verifikasi wajah & lokasi otomatis
dengan AI**".

**Positioning — uji:**
- Satu paragraf, berisi: product + category + cara kerja inti (DNA) +
  pembeda vs alternatif + opsi Level 2 untuk segmen tertentu.
- Semua bahannya sudah ada di section lain; positioning hanya merangkai.
- Tidak mengklaim keadaan jangka panjang dari Vision sebagai hasil produk.
- Ini satu-satunya "pitch". Jangan buat versi pendek/panjang lain.

**Tagline:** pakai yang sudah ditetapkan user; kalau belum ada,
rekomendasikan tagline terbaik yang menjual Level 1. Cek apakah
menjual Level 1. ✓ "_Urus Karyawan Cukup Chat_" menjual zero-install.

**Opportunity — uji:**
- Bicara pasar, bukan produk kita.
- "Kenapa sekarang" menyebut perubahan eksternal (teknologi jadi murah,
  regulasi, perilaku).
- "Celah pasar" menyebut kebutuhan yang tidak terlayani **jenis**
  alternatif yang ada — tanpa nama merek, harga, atau fitur kompetitor:
  ✓ "Aplikasi absensi yang ada menuntut install app dan atur jadwal dulu;
  grup WA gratis tapi tak tercatat". Apakah celah ini benar-benar kosong
  diuji `business-reviewer`, bukan ditulis di sini.
- Kalau ada ketergantungan yang bisa mematikan klaim (mis. memakai API
  tidak resmi yang rawan diblokir), tulis blok `[!]` di sini — ringkas,
  lengkap dengan risikonya. Jangan disembunyikan
  demi positioning yang bersih — reviewer akan menemukannya.
- Kalau risikonya bergantung pada keputusan yang belum dibuat user (mis.
  pilihan kanal), pilihkan keputusan terbaik lalu tulis risiko dari
  pilihan itu — jangan dibiarkan bersyarat. Hapus blok hanya kalau memang
  tidak ada risiko struktural.

## §3 Pricing Plan

- Diisi PALING TERAKHIR, setelah §4 dan §5. Tetapkan skema dan harga
  rekomendasi terbaikmu — harga yang paling mungkin membuat produk laris
  dan menguntungkan di segmen §5 — jangan dibiarkan `[INPUT-NEEDED]`.
- Tier dibedakan oleh kapabilitas (Skema 1 vs Skema 2), bukan oleh ukuran
  perusahaan. Ukuran perusahaan → diskon volume di dalam tier.
- Tahunan **selalu** bayar 10 bulan, dapat 12 — harga tahunan = 10 ×
  harga bulanan, untuk semua skema dan add-on. Ini ketetapan user: jangan
  diganti skema diskon lain walau sedang memilihkan rekomendasi terbaik.
  Tulis harga efektif per bulan
  ("Rp 60.000 (Rp 5.000/bln)") supaya bisa dibandingkan langsung dengan
  harga bulanan.
- Blok **Fitur** di bawah harga: satu baris per kapabilitas §4, ✓ atau
  kosong. "Dukungan" selalu baris terakhir.
- Add-on di sub-section `### Add-on (...)` dengan tabel sendiri — kolom
  `Add-on | Harga | Fitur yang didapat` — diletakkan setelah tabel harga
  skema. **Jangan** jadikan baris di dalam tabel harga skema: tabel skema
  hanya berisi harga, blok Fitur, dan Dukungan.
- Judul sub-section menyebut skema yang bisa memasang add-on, sesuai
  jumlah skema produk ("bisa dipasang ke Skema 1, Skema 2, atau Skema 3";
  kalau hanya untuk skema tertentu, sebut itu).
- Harga add-on ditulis per karyawan per bulan (`+Rp .../karyawan/bln`);
  harga tahunan boleh ditambahkan di bawahnya (`<br>(Rp .../thn)`),
  tetap 10 × harga bulanan.
  Keterangan umum (tidak ikut diskon volume, status `[?]`) ditulis sekali
  di bawah tabel, bukan diulang per baris.
- Harga **tidak wajib** disertai alasan ("kenapa harga ini"). Apakah harga
  layak dan menang lawan pasar diuji `business-reviewer`. Kalau user tetap
  ingin menulis alasannya, dasarkan pada nilai (§4), segmen (§5), dan
  biaya — tanpa membandingkan dengan harga kompetitor.
- Uji konsistensi: harga terendah harus masih menutup biaya variabel (AI,
  pesan) — kalau biaya variabelnya belum diketahui, pakai perkiraan
  terbaikmu dan tulis sebagai asumsi di bawah tabel harga.

## §4 Product-to-Value Mapping

- Urut dari problem paling menyakitkan. Baris pertama = headline konten.
- Kolom **Customer Problem** ditulis dari mulut customer, konkret, sering
  menyebut alternatif yang gagal: "Aplikasi absensi lain ribet: harus
  install, lalu atur jadwal/shift dulu sebelum bisa dipakai".
- **Benefit** untuk end-user (yang memakai), **Business Outcome** untuk
  decision-maker (yang membayar). Kalau dua kolom ini berisi hal yang sama,
  salah satunya belum dipikirkan.
- Kapabilitas yang terikat tier/skema/add-on diberi keterangan dalam kurung
  di kolom Capability, supaya §3 bisa memetakan ✓ per baris.
- Harga boleh jadi satu baris — "bayar hanya modul yang dipakai" adalah value.
- Problem tanpa fitur → Capability `[GAP]`. Jangan dihapus.
- Kalau customer sudah punya aset (spreadsheet gaji dengan rumus PPh21
  sendiri), value "tidak perlu pindah" adalah baris tersendiri — ini sering
  jadi pembeda paling kuat terhadap incumbent yang memaksa migrasi.

## §5 Target Customer Profile

- Primary Market: Industry, Company size, Geography, Business type,
  Kematangan teknologi, Skema yang ditawarkan. Sebut juga **Bukan target**
  dan kenapa ("usaha yang sudah pakai HRIS lengkap — bukan kandidat migrasi,
  kita menang di setup minimal, bukan kelengkapan fitur").
- Business type = ciri operasional yang membuat problem §4 paling terasa
  (tersebar di banyak lokasi, sudah terbiasa koordinasi via grup WA).
- Skema yang ditawarkan menghubungkan segmen ke §3 dan memberi alasan:
  "langsung Skema 2 — anti-kecurangan visual jadi kebutuhan inti segmen
  ini, bukan upsell".
- Persona 1 (Decision Maker): Role boleh berbeda per market ("HR/Ops
  Manager (Primary) — atau Owner langsung (Secondary)").
- Persona 2 (End User) bukan pembeli → Buying Motivation/Trigger diawali
  "*(bukan pembeli — ...)*".
- Buying Trigger = kejadian: "kecurangan absen ketahuan", "salah hitung
  gaji", "buka cabang baru", "sadar bayar mahal HRIS yang cuma dipakai
  modul absensinya".
- Pain Points end-user harus memuat kekhawatiran teknis yang bisa
  diantisipasi (foto ditolak
  karena pencahayaan, sinyal lemah, tidak tahu komplain ke siapa) — ini
  bahan untuk konten onboarding dan FAQ, bukan hanya untuk empati.

## Kompetitor tidak ditulis di BKB

BKB berisi strategi produk sendiri; kompetitor adalah bahan **pengujian**
strategi itu, dan rumahnya laporan `business-reviewer` (funnel 3 level DNA,
harga & fitur bertanggal). Karena itu di BKB:

- **Tidak ada** nama merek kompetitor, harga, fitur, atau perbandingan
  angka ("3× lebih murah dari X") — di section mana pun.
- **Boleh** menyebut **jenis alternatif** tanpa merek, secukupnya untuk
  Celah pasar, DNA, dan Positioning: "tool global berbayar USD", "tool
  gratis self-serve", "HRIS lengkap", status quo ("Excel, grup WA, proses
  manual").
- **Blok `[!]` risiko struktural** tetap ada di §2 — regulasi,
  ketergantungan API/platform, biaya variabel, dan ancaman dari jenis
  pemain ("tool gratis menjadikan lantai harga nol") — tanpa menyebut merek.
- Rekomendasi dari `business-reviewer` diterapkan sebagai **kesimpulan**
  (DNA turun level, harga dikoreksi, positioning dipertajam), bukan dengan
  menyalin data kompetitornya ke BKB.
