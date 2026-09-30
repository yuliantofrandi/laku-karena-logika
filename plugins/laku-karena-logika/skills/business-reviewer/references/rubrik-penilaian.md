# Rubrik Penilaian BKB & Metode Competitive Analysis

Dipakai saat MEMBERI SKOR pada BKB dan menyusun competitive analysis. Rubrik
ini adalah sisi penilai dari `business-knowledge/references/aturan-penulisan.md`
— aturan itu dipakai untuk MENULIS, rubrik ini untuk MENILAI hasilnya. Kalau
keduanya berbeda, aturan penulisan yang benar; laporkan bedanya.

## Cara memberi skor

Total **100 poin**, dibagi per dimensi dengan bobot di bawah. Untuk tiap
dimensi: mulai dari poin penuh, lalu kurangi tiap kali sebuah uji di aturan
penulisan gagal. Tiap pengurangan **wajib** menunjuk baris/section BKB dan uji
yang dilanggar. Bulatkan ke bilangan bulat.

Pisahkan dua jenis kekurangan — keduanya mengurangi poin, tapi dilaporkan beda:
- **Cacat penulisan** — melanggar aturan penulisan (vision menyebut fitur,
  angka tanpa sumber, duplikasi, benefit = business outcome, dst.).
- **Celah strategis** — tulisannya lolos aturan, tapi logikanya tidak bertahan
  saat diuji ke pasar (celah pasar yang ternyata sudah terisi, DNA yang
  ternyata mudah ditiru, harga yang cuma menang lawan sebagian kompetitor).
  Celah strategis ditemukan lewat competitive analysis, bukan lewat membaca
  BKB saja — dan biasanya lebih mahal daripada cacat penulisan.

### Bobot per dimensi

| Dimensi | Bobot | Yang dinilai |
|---|---:|---|
| §1 Business Overview | 15 | Vision & Mission lolos ujinya masing-masing |
| §2 Brand Strategy | 30 | Category, DNA L1/L2 (satu baris to the point per pembeda, tanpa keterangan/alasan), Positioning, Tagline, Opportunity, blok risiko `[!]` — inti strategis, bobot terberat |
| §3 Pricing Plan | 15 | Tier oleh kapabilitas bukan ukuran; tahunan = bayar 10 bulan dapat 12 (ketetapan user — jangan rekomendasikan skema tahunan lain) dengan harga efektif per bulan; blok fitur per kapabilitas; harga terendah menutup biaya variabel. Harga tidak wajib beralasan di BKB — jangan kurangi skor karena alasan harga tidak ditulis; kelayakan harganya diuji di competitive analysis & Verdict pasar |
| §4 Product-to-Value Mapping | 15 | Urut dari problem tersakit; benefit ≠ business outcome; kapabilitas terpetakan ke tier; baris "tidak perlu pindah" bila relevan |
| §5 Target Customer Profile | 15 | Primary/Secondary + "Bukan target"; business type = ciri operasional; persona dengan trigger berupa kejadian; pain point end-user teknis yang bisa diantisipasi |
| Konsistensi lintas-section | 10 | Satu fakta satu rumah; tidak ada nama/harga/fitur kompetitor di section mana pun; tiap kapabilitas §4 punya baris ✓ di §3; tiap market §5 menyebut skema §3; positioning hanya memakai klaim yang sudah ada; penanda `[?]`/`[INPUT-NEEDED]` dipakai jujur. Klaim superlatif tanpa `[?]` BUKAN cacat penulisan — BKB sengaja ditulis versi terbaik; kebenaran klaimnya diuji di competitive analysis & Verdict pasar. Keputusan strategis (harga, skema, tagline, segmen) yang diisi rekomendasi konsultan juga bukan cacat — nilai apakah pilihannya tepat untuk laris, dan kalau tidak, sebut pilihan yang lebih baik |

### Panduan pengurangan (contoh, bukan daftar tertutup)

- Uji inti sebuah sub-bagian gagal total (mis. Vision menyebut mekanisme):
  −3 sampai −5 dari dimensinya.
- Cacat sebagian (mis. Celah pasar menyebut merek kompetitor, atau
  "Kenapa sekarang" tidak menyebut perubahan eksternal): −2 sampai −3.
- Celah strategis yang membalik logika satu section (mis. funnel Level 2
  tidak mengerucut, atau celah pasar §2 ternyata sudah diisi pemain nyata
  yang lebih murah): −4 sampai −8 di §2, karena merusak fondasi positioning.
- Cacat kecil/kosmetik (format, satu duplikasi minor): −1.
- BKB memuat nama merek, harga, atau fitur kompetitor (melanggar aturan
  "Tanpa kompetitor"): −1 per kemunculan di dimensi tempatnya, maks −3 per
  dimensi. Data itu dipindah ke competitive analysis laporan, bukan dibuang.

### Band verdict

| Skor | Verdict |
|---:|---|
| 90–100 | **Siap dipakai skill hilir.** Perbaikan opsional. |
| 75–89 | **Kuat, ada perbaikan bermakna.** Layak dipakai, tapi tutup temuan utama dulu. |
| 60–74 | **Perlu revisi bermakna.** Ada celah strategis atau cacat penulisan yang mengganggu keandalan. |
| < 60 | **Belum layak.** Fondasi strategis atau penulisan belum berdiri; jangan dipakai skill hilir dulu. |

Skor tinggi karena penulisan rapi TIDAK menutup celah strategis. Kalau
competitive analysis menemukan lubang yang membalik positioning, sebut di
verdict walau skor penulisan tinggi — mis. "80/100: rapi, tapi funnel Level 2
belum mengerucut — DNA §2 kemungkinan terbalik".

## Metode competitive analysis

Tujuannya bukan mendaftar semua kompetitor, tapi **menguji apakah klaim
strategis BKB bertahan**. Selalu tanya: kalau temuan ini benar, apakah
positioning/celah pasar/DNA di BKB masih berdiri?

### Kelompokkan — funnel 3 level DNA (metode utama, wajib)

Jangan mengelompokkan kompetitor bebas per sumbu (mis. "sekanal vs status
quo") sebagai langkah pertama — itu pengelompokan subjektif yang beda-beda
tiap review. Pengelompokan utama **wajib** mengikuti struktur DNA yang sudah
ada di §2 BKB, sebagai funnel yang makin sempit:

- **Level 1 — Category saja.** Ambil kalimat Category §2 BKB, buang syarat
  DNA-nya. Cari semua pemain yang masuk kategori umum ini. Biasanya jumlahnya
  banyak — level ini **tidak sah** dipakai untuk klaim "celah pasar kami
  kosong", karena semua pemain sejenis ada di sini.
- **Level 2 — Category + DNA Level 1.** Tambahkan syarat DNA Level 1 §2 (yang
  diklaim BKB "paling sulit ditiru"). Saring ulang daftar Level 1: siapa yang
  masih lolos?
- **Level 3 — Category + DNA Level 1 + Pembeda Level 2.** Tambahkan syarat
  DNA Level 2 §2. Saring ulang daftar Level 2: siapa yang masih lolos?

**Cara membaca hasilnya:** jumlah kompetitor harus **monoton mengerucut**
Level 1 ≥ Level 2 ≥ Level 3, idealnya nol di Level 3 (blue ocean — positioning
BKB benar-benar tidak tertandingi). Ada dua pola gagal yang harus ditangkap:

- **Funnel berhenti mengerucut sebelum Level 3** (Level 2 masih menyisakan
  pemain yang sama banyak/hampir sama dengan Level 1) → DNA Level 1 **bukan**
  penyaring efektif, kemungkinan BUKAN yang paling sulit ditiru seperti
  diklaim. Kalau Level 3 justru nol, curigai **inversi DNA**: pembeda yang
  benar-benar langka ada di Level 2 BKB, bukan Level 1. Ini wajib jadi celah
  strategis di Temuan utama, dengan pengurangan skor §2 sesuai panduan di
  bawah — bukan catatan opsional.
- **Funnel tidak pernah mengerucut ke nol** (masih ada pemain lolos di Level
  3) → positioning belum blue ocean sama sekali; ini temuan paling berat,
  karena berarti moat yang diklaim BKB sudah ditembus penuh.

Kolom tabel **menyesuaikan keputusan tiap level** (jangan dipaksa identik),
tapi selalu mulai dari **Kompetitor** dan tutup dengan **Dicek**
(`[FAKTA]` + tanggal atau `[?]`):

- **Level 1** — Kompetitor · Kanal · Harga · Dicek. Cuma mendaftar isi
  kategori; belum menilai kekuatan/kelemahan.
- **Level 2** — Kompetitor · Kekuatan · Kelemahan · Lolos filter Level 2? ·
  Dicek.
- **Level 3** — Kompetitor · Metode/pembeda mereka · Lolos filter Level 3? ·
  Dicek.

Isi kolom lolos dengan `Lolos` / `Gugur` / `Borderline`. Tiap level ditutup
paragraf "Kesimpulan Level N", dan boleh ada "Catatan tambahan" untuk celah
yang hanya berlaku di sebagian level.

### Di luar funnel

- **Indirect** — Excel, grup WA, proses manual, mesin yang sudah terbeli,
  "tidak melakukan apa-apa". Sering pemenang sebenarnya karena gratis dan sudah
  dipakai. Jangan dilewati.
- **Ancaman struktural** — bukan kompetitor, tapi bisa mematikan produk:
  ketergantungan API/platform, biaya variabel per transaksi, regulasi, ToS.
  Cocokkan dengan blok `[!]` di BKB §2 — kalau BKB tidak menyebut ancaman yang
  kamu temukan, itu temuan utama.

### Tandai kesegaran

Tiap baris data kompetitor: `[FAKTA]` (dicek langsung ke sumber, dengan tanggal
& URL) atau `[?]` (dugaan/belum diverifikasi). Tidak ketemu → `[INPUT-NEEDED]`,
jangan ditebak. Cantumkan kolom "Terakhir dicek" bertanggal dan daftar sumber
(URL) di akhir. Harga kompetitor yang salah lebih berbahaya daripada kosong —
seluruh logika celah pasar berdiri di atasnya.

### Uji silang ke BKB (checklist)

- **Celah pasar §2** — kebutuhan yang BKB klaim tak terlayani, benar kosong
  di Level 3 funnel? Adakah pemain Level 1 yang lebih murah atau sudah lolos
  ke Level 2?
- **DNA §1/§2** — apakah funnel benar-benar mengerucut di Level 2, atau baru
  mengerucut di Level 3? Kalau baru di Level 3, itu inversi DNA: pembeda yang
  benar-benar sulit ditiru ada di Level 2 BKB, bukan Level 1. Inversi seperti
  ini adalah temuan besar.
- **Harga §3** — menang lawan **semua level funnel**, atau cuma sebagian?
  Sebut eksplisit level mana harga kita kalah, dan apa gantinya (fitur,
  kepercayaan) yang membenarkan selisihnya.
- **Positioning** — "alternatif" yang dilawan sudah mencakup pemenang
  sebenarnya (sering: status quo indirect), atau cuma kompetitor berbayar?

Temuan yang membalik salah satu di atas masuk **Temuan utama** laporan sebagai
celah strategis, dan memicu pengurangan skor di §2/§3, bukan sekadar catatan di
bagian competitive analysis.
