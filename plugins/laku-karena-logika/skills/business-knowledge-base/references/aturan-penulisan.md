# Aturan Penulisan & Uji Kualitas per Section

Dipakai saat MENGISI atau MEREVIEW isi. Tiap section punya uji yang harus
lolos sebelum dianggap selesai. Contoh diambil dari Timelog
(`~/Dev/claude/timelog/`), produk yang menjadi acuan struktur ini.

## Prinsip umum

1. **Satu fakta satu rumah.** Sebelum menambah kalimat, tanya: sudah ada di
   section lain? Kalau ya, rujuk ("lihat §3"), jangan salin. User berulang
   kali memangkas duplikasi — jangan menambah pekerjaan itu.
2. **Kondisi berlaku saat ini.** Tidak ada "sebelumnya kami...", tidak ada
   decision log, tidak ada versi di badan dokumen. Riwayat hidup sebagai
   snapshot bernomor di `<produk>/sebelumnya/`.
3. **Keputusan = kesimpulan + alasan.** Pola `... — karena ...`. Reviewer
   menilai dasarnya, bukan hasilnya.
4. **Angka mengalahkan sifat.** "Lebih murah" lemah; "di bawah ~Rp12.500/
   karyawan/bln, batas termurah kompetitor bundel" kuat. Kalau angkanya
   belum ada → `[INPUT-NEEDED]`, jangan dikira-kira tanpa `[?]`.
5. **Bahasa:** Indonesia, ringkas, tanpa jargon marketing kosong. Istilah
   teknis/kategori boleh Inggris kalau memang begitu dipakai di pasar
   (Decision Maker, End User, Primary Market).
6. **Format:** heading `##` bernomor untuk section, `###` sub, `####` untuk
   persona. Kutipan `> ...` untuk pernyataan inti (vision, mission,
   category, DNA, positioning, tagline). Tabel untuk data terstruktur.
   Tidak ada H1 — nama produk cukup di folder dan field Product name.

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
- Satu klaim tebal, lalu penjelasan dari sisi pengguna (apa yang TIDAK
  perlu mereka lakukan sering lebih kuat dari apa yang mereka dapat).
  ✓ "**Setup Minimal**: karyawan cukup kirim foto — tanpa install app,
  tanpa atur jadwal atau shift dulu, presensi langsung jalan."
- Sulit ditiru karena alasan struktural (incumbent harus mengkanibal
  produknya sendiri, dsb.), bukan karena teknologinya canggih.
- Kalau alasan sulit-ditirunya masih hipotesis → `[?]`.

**Level 2 — uji:** kuat sekarang, tapi jujur bisa dikejar 1-2 tahun. Ditulis
kontras dengan alternatif: "bukan cuma mencocokkan nomor HP".

**Positioning — uji:**
- Satu paragraf, berisi: product + category + cara kerja inti (DNA) +
  pembeda vs alternatif + opsi Level 2 untuk segmen tertentu.
- Semua bahannya sudah ada di section lain; positioning hanya merangkai.
- Tidak menjanjikan hal yang masih di Vision.
- Ini satu-satunya "pitch". Jangan buat versi pendek/panjang lain.

**Tagline:** hanya yang sudah beredar; kosongkan kalau belum. Cek apakah
menjual Level 1. ✓ "_Urus Karyawan Cukup Chat_" menjual zero-install.

**Opportunity — uji:**
- Bicara pasar, bukan produk kita.
- "Kenapa sekarang" menyebut perubahan eksternal (teknologi jadi murah,
  regulasi, perilaku).
- "Celah pasar" memuat angka kompetitor lalu menurunkan batas harga:
  "Timelog bisa lebih murah dari semua nama ini selama harga jualnya di
  bawah ~Rp12.500/karyawan/bln".
- Kalau ada ketergantungan yang bisa mematikan klaim (mis. memakai API
  tidak resmi yang rawan diblokir), tulis blok `[!]` di sini dan detailnya
  di `competitive-landscape.md` § Ancaman Struktural. Jangan disembunyikan
  demi positioning yang bersih — reviewer akan menemukannya.
- Blok `[!]` boleh bersyarat kalau keputusannya belum dibuat: "Kalau
  memakai WhatsApp tidak resmi, ... [INPUT-NEEDED: keputusan kanal]".
  Risiko yang bergantung keputusan tertunda tetap ditulis — justru itu
  yang memaksa keputusannya diambil. Hapus blok hanya kalau memang tidak
  ada risiko struktural.

## §3 Product-to-Value Mapping

- Urut dari problem paling menyakitkan. Baris pertama = headline konten.
- Kolom **Customer Problem** ditulis dari mulut customer, konkret, sering
  menyebut alternatif yang gagal: "Aplikasi absensi lain ribet: harus
  install, lalu atur jadwal/shift dulu sebelum bisa dipakai".
- **Benefit** untuk end-user (yang memakai), **Business Outcome** untuk
  decision-maker (yang membayar). Kalau dua kolom ini berisi hal yang sama,
  salah satunya belum dipikirkan.
- Kapabilitas yang terikat tier/skema/add-on diberi keterangan dalam kurung
  di kolom Capability, supaya §4 bisa memetakan ✓ per baris.
- Harga boleh jadi satu baris — "bayar hanya modul yang dipakai" adalah value.
- Problem tanpa fitur → Capability `[GAP]`. Jangan dihapus.
- Kalau customer sudah punya aset (spreadsheet gaji dengan rumus PPh21
  sendiri), value "tidak perlu pindah" adalah baris tersendiri — ini sering
  jadi pembeda paling kuat terhadap incumbent yang memaksa migrasi.

## §4 Pricing Plan

- Diisi PALING TERAKHIR. Kalau §3 dan §5 belum jadi, tandai seluruh section
  `[INPUT-NEEDED]` dan jangan menebak.
- Tier dibedakan oleh kapabilitas (Skema 1 vs Skema 2), bukan oleh ukuran
  perusahaan. Ukuran perusahaan → diskon volume di dalam tier.
- Tahunan: bayar 10 dapat 12, tulis harga efektif per bulan
  ("Rp 60.000 (Rp 5.000/bln)") supaya bisa dibandingkan langsung dengan
  kompetitor yang memasang harga per bulan.
- Blok **Fitur** di bawah harga: satu baris per kapabilitas §3, ✓ atau
  kosong. "Dukungan" selalu baris terakhir.
- Add-on di tabel terpisah, harga per karyawan per bulan, bisa dipasang ke
  semua skema.
- Uji konsistensi: harga tertinggi harus di bawah batas yang dipasang di
  §2 Celah pasar; harga terendah harus masih menutup biaya variabel (AI,
  pesan) — kalau belum tahu biaya variabelnya, tulis `[?]` dan catat di
  Ancaman Struktural.

## §5 Target Customer Profile

- Primary Market: Industry, Company size, Geography, Business type,
  Kematangan teknologi, Skema yang ditawarkan. Sebut juga **Bukan target**
  dan kenapa ("usaha yang sudah pakai HRIS lengkap — bukan kandidat migrasi,
  kita menang di setup minimal, bukan kelengkapan fitur").
- Business type = ciri operasional yang membuat problem §3 paling terasa
  (tersebar di banyak lokasi, sudah terbiasa koordinasi via grup WA).
- Skema yang ditawarkan menghubungkan segmen ke §4 dan memberi alasan:
  "langsung Skema 2 — anti-kecurangan visual jadi kebutuhan inti segmen
  ini, bukan upsell".
- Persona 1 (Decision Maker): Role boleh berbeda per market ("HR/Ops
  Manager (Primary) — atau Owner langsung (Secondary)").
- Persona 2 (End User) bukan pembeli → Buying Motivation/Trigger diawali
  "*(bukan pembeli — ...)*".
- Buying Trigger = kejadian: "kecurangan absen ketahuan", "salah hitung
  gaji", "buka cabang baru", "sadar bayar mahal HRIS yang cuma dipakai
  modul absensinya".
- Pain Points end-user harus memuat kekhawatiran teknis nyata (foto ditolak
  karena pencahayaan, sinyal lemah, tidak tahu komplain ke siapa) — ini
  bahan untuk konten onboarding dan FAQ, bukan hanya untuk empati.

## Rujukan ke competitive-landscape.md

File kompetitor dirawat skill terpisah. Yang perlu skill ini tahu hanya
titik singgungnya:

- **§2 Opportunity** memuat angka kompetitor (harga, batas minimum, add-on
  berbayar) untuk mengukur celah pasar. Angka ini harus konsisten dengan
  yang tercatat di `competitive-landscape.md` kalau file itu sudah ada —
  tapi rumah detail per kompetitor tetap di sana, di sini cukup angka yang
  membentuk celahnya.
- **Blok `[!]` risiko struktural** di §2 menunjuk pembaca ke bagian Ancaman
  Struktural di `competitive-landscape.md`. Tulis ringkasan risikonya di
  BKB; detail, sumber, dan tanggalnya biar skill kompetitor yang mengurus.
- **Positioning** menarik "alternatif" (termasuk status quo: Excel, grup
  WA, proses manual) dari daftar kompetitor. Kalau file kompetitor belum
  ada, tulis alternatif sebisanya dan tandai `[?]`.

Jangan mengedit `competitive-landscape.md` dari skill ini walau terlihat
salah — laporkan ke user sebagai temuan audit.
