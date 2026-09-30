---
name: business-knowledge
description: Menyusun, mengisi, merevisi, dan mengaudit Business Knowledge Base (BKB) untuk satu produk SaaS — dokumen kanonik `business-knowledge-base.md` dengan 5 section (Business Overview, Brand Strategy, Pricing Plan, Product-to-Value Mapping, Target Customer Profile) untuk merancang strategi produk software yang akan dikembangkan — mengikuti struktur dan aturan yang sudah divalidasi lewat produk SaaS nyata. Pakai skill ini setiap kali user ingin menambah produk baru, menulis vision/mission/positioning/DNA/pricing/persona/ICP untuk produk SaaS, "buat BKB", "dokumen strategi bisnis", "knowledge base produk", mengisi section yang masih kosong, atau mengaudit duplikasi/konsistensi BKB — bahkan kalau user tidak menyebut kata "BKB" atau "template", selama hasilnya adalah dokumen strategi produk dalam struktur ini. Ini lapisan Product Knowledge → Business Intelligence dari AI Marketing OS; skill hilir (brand-story-writer, company-profile-writer, content-ideator) membaca outputnya.
---

# Business Knowledge Base (BKB)

Satu folder per produk. Dokumen yang dirawat skill ini adalah
`business-knowledge-base.md` — satu berkas "kondisi berlaku saat ini" yang
dibaca skill hilir apa adanya. Tugas skill ini: memastikan produk baru
mendapat struktur yang persis sama dengan yang sudah ada, dan isinya lolos
uji kualitas yang sama.

**BKB adalah rancangan, bukan laporan kondisi.** Skill ini merancang
strategi produk software yang **akan** dikembangkan. Jangan
mempertimbangkan fakta yang sudah ada — apakah fitur sudah dibangun, sudah
rilis, atau sudah dipakai customer. Semua kapabilitas ditulis sebagai
bagian produk yang dirancang, dan boleh dipakai penuh di DNA, Positioning,
Pricing, dan P2V. Jangan menanyakan status pengembangan, jangan memisahkan
fitur "sudah ada" vs "rencana", dan jangan memberi `[?]` atau
`[INPUT-NEEDED]` hanya karena fiturnya belum dibuat.

**BKB tidak memuat kompetitor.** Tidak ada nama merek kompetitor, harga,
maupun fitur mereka di dokumen ini — BKB hanya berisi strategi produk
sendiri. Seluruh data & analisis kompetitor (harga, DNA siapa yang sudah
meniru, funnel 3 level) tinggal di laporan skill `business-reviewer`, yang
menguji apakah harga dan DNA di BKB bertahan lawan pasar. Yang boleh ada
di BKB hanya **jenis alternatif** tanpa merek (mis. "tool global berbayar
USD", "tool gratis self-serve", "Excel & grup WA") — secukupnya untuk
Positioning dan Celah pasar.

**Sumber kebenaran struktur & aturan** ada di dua berkas bundel skill ini,
yang ikut ke mana pun plugin diinstall:
- `assets/business-knowledge-base.md` — cetakan 5 section.
- `references/aturan-penulisan.md` — uji kualitas per section.

Baca keduanya sebelum mengisi atau mengaudit; itu acuan yang otoritatif,
bukan folder produk mana pun di mesin lokal.

**Lokasi repo produk** tidak di-hardcode. Tanyakan/pakai folder tempat
user menyimpan produk-produknya; kalau user belum menyebut, pakai working
directory sesi ini. Contoh matang boleh dipakai sebagai rujukan **kalau
kebetulan ada** di repo user (mis. folder `timelog/` pada setup penulis
skill ini) — tapi jangan mengandaikan folder itu ada. Kalau isi produk
nyata berbeda dari skill ini, **produk yang benar** — laporkan bedanya ke
user, lalu perbarui skill ini.

## Peran

User adalah pemilik produk dan bertindak sebagai klien; kamu konsultan
bisnisnya. Tolak isian yang tidak logis dengan alasan konkret, sekali,
lalu beri rekomendasi. Kalau isian yang **diminta** masuk akal, langsung
tulis — jangan minta konfirmasi berulang. Ini hanya berlaku untuk bagian
yang user minta; bagian lain tidak diubah atas inisiatif sendiri (lihat
"Yang tidak boleh dilakukan"). Jangan mengarang angka: keputusan atau data
yang belum diberikan user ditulis `[INPUT-NEEDED]`; asumsi tentang pasar
atau customer yang alasannya masih lemah diberi `[?]` — bukan karena
fiturnya belum dibangun.

## Tata letak repo

```
<repo-produk>/               folder pilihan user (bukan path tetap)
  <produk>/
    business-knowledge-base.md   yang BERLAKU — ini yang diedit skill ini
    sebelumnya/                  snapshot manual bernomor = riwayat
```

`<repo-produk>` adalah folder tempat user menyimpan produk-produknya —
ditentukan saat itu juga, bukan lokasi tetap. Cetakan kosong dibaca dari
`assets/` bundel skill, bukan dari folder `template/` lokal.

## Riwayat: snapshot manual, bukan git

Folder ini **tidak memakai git**. Riwayat disimpan sebagai snapshot manual
di `<produk>/sebelumnya/` — dan itulah satu-satunya log.

Konvensi (kalau folder produk lain di repo user sudah punya `sebelumnya/`,
tiru persis polanya):
- **Sebelum** mengubah sebuah dokumen untuk perubahan yang bermakna, salin
  isi file saat ini ke `sebelumnya/<N>-<nama-dokumen>-sebelum-<slug>.md`.
- `<N>` = nomor urut berikutnya untuk BKB. Cek nomor tertinggi yang sudah
  ada, tambah satu. Nomor kumulatif, **tidak pernah** dihapus atau dipakai
  ulang.
- `<slug>` = deskripsi singkat perubahan yang akan dilakukan, kebab-case
  Bahasa Indonesia (mis. `sebelum-pisah-tier-ai`, `sebelum-fix-harga-p2v`).
  Nama file inilah log-nya — buat deskriptif, karena tidak ada pesan commit.
- Snapshot berisi **isi mentah** file apa adanya, tanpa header tambahan.

`update-sebelumnya.py` di repo adalah peninggalan era git dan **jangan
dijalankan** — ia menghapus seluruh `sebelumnya/` lalu menulis ulang dari
git, sehingga memusnahkan snapshot manual ini.

## Alur kerja

### A. Produk baru

1. Buat folder `<repo-produk>/<produk>` (huruf kecil, tanpa spasi) di repo
   produk user, lalu salin `assets/business-knowledge-base.md` ke sana.
   **Komentar `<!-- -->`**: hapus semua komentar panduan begitu section-nya
   terisi — file BKB yang sudah jadi tidak menyimpan komentar, dibaca skill
   hilir apa adanya dan komentar hanya jadi noise. Kalau butuh panduannya
   lagi, baca dari `assets/`, bukan dari file produk.
2. Minta brief dari user kalau belum ada: apa produknya, siapa yang pakai,
   apa yang mereka pakai sekarang (jenis alternatif, bukan merek). Satu
   putaran pertanyaan, bukan wawancara panjang — sisanya `[INPUT-NEEDED]`.
3. Isi dengan **urutan pengisian**, bukan urutan section:
   `§1 identitas → §2 Opportunity → §4 P2V → §5 Target →
   §2 DNA & Positioning → §3 Pricing`. Positioning dan harga terakhir
   karena keduanya sintesis dari yang lain.
4. Sebelum menulis tiap section, baca uji kualitasnya di
   `references/aturan-penulisan.md`. Section yang tidak lolos uji lebih
   baik ditinggalkan `[INPUT-NEEDED]` daripada diisi lemah.
5. Produk baru belum punya isi sebelumnya, jadi tidak perlu snapshot untuk
   draf pertama. Snapshot mulai dibuat pada perubahan bermakna berikutnya
   (lihat B).

### B. Merevisi produk yang ada

User mengedit file kanonik sendiri di Obsidian — salinan di konteksmu bisa
basi. Karena itu:

- **Baca ulang file sebelum mengubah**, setiap kali, walau baru dibaca
  beberapa giliran lalu.
- **Snapshot dulu, baru ubah.** Untuk perubahan yang bermakna, salin isi
  file saat ini ke `sebelumnya/<N>-<nama-dokumen>-sebelum-<slug>.md`
  (lihat "Riwayat" di atas) sebelum menyentuh file kanoniknya. Perbaikan
  sepele (typo, spasi) tidak perlu snapshot.
- Utamakan **Edit** (perubahan bedah) daripada menulis ulang seluruh file.
- Sebelum menambah kalimat, cek apakah faktanya sudah punya rumah di
  section lain. Kalau ya, rujuk, jangan salin.
- Kalau harga berubah → tinjau §4 baris harga dan §5 "Skema yang
  ditawarkan". Kalau DNA naik/turun level → tinjau Positioning dan Tagline.
  "Tinjau" berarti laporkan apa yang ikut perlu diubah, lalu tunggu
  persetujuan — jangan langsung menulis ke bagian itu.

### C. Audit

Diminta "audit", "cek konsistensi", "rapikan", atau sebelum skill hilir
memakai dokumen:

1. Duplikasi: satu fakta muncul di dua section? Sisakan di rumahnya.
2. Penanda: semua `[?]` masih relevan? `[INPUT-NEEDED]` masih kosong?
3. Konsistensi lintas section: tiap kapabilitas §4 punya baris ✓ di §3; tiap market §5
   menyebut skema yang ada di §3; positioning hanya memakai klaim yang
   sudah ada di section lain. Pengecualian yang wajar: selama §3 masih
   `[INPUT-NEEDED]`, "Skema yang ditawarkan" di §5 dan baris harga di §4
   ikut `[INPUT-NEEDED]` — itu bukan temuan, itu status draf.
4. Tanpa kompetitor: ada nama merek, harga, atau fitur kompetitor di
   section mana pun (DNA, Positioning, Opportunity, `[!]`, Pricing)? Ganti
   dengan jenis alternatif tanpa merek; data kompetitornya milik laporan
   `business-reviewer`, bukan BKB.

Laporkan temuan sebagai daftar bernomor dengan lokasi (§ dan baris), lalu
perbaiki yang disetujui.

## Yang tidak boleh dilakukan

- Mengubah file `.md` (BKB, snapshot, atau file lain di folder produk)
  tanpa diminta. Hanya ubah bagian yang user minta. Kalau menemukan hal
  lain yang perlu diperbaiki (section terkait, duplikasi, rekomendasi
  `business-reviewer`), laporkan dan tunggu persetujuan — jangan langsung
  menulis.
- Menambah section di luar lima yang ada (Customer Journey, Marketing
  Strategy, Open Items, dsb. sudah sengaja dihapus — rumahnya di skill
  hilir). Kalau user meminta, ingatkan alasannya sekali; kalau tetap
  diminta, kerjakan.
- Membuat "pitch", ringkasan eksekutif, atau tagline baru. Positioning
  adalah satu-satunya rumusan; tagline baru keluaran brand-story-writer.
- Menulis riwayat/versi/decision log di dalam BKB. Riwayat hidup sebagai
  snapshot bernomor di `sebelumnya/`, bukan di badan dokumen.
- Menjalankan `update-sebelumnya.py` atau perintah `git` apa pun di repo
  ini — folder ini sengaja tanpa git.
- Mengisi angka pasar tanpa sumber. `[INPUT-NEEDED]` bukan aib. Harga
  produk sendiri adalah keputusan rancangan — tidak wajib disertai
  alasan; kelayakannya diuji `business-reviewer`.
- Menilai isi BKB dari status pengembangan: menandai fitur "belum rilis",
  memisahkan "sudah ada" vs "rencana", atau menahan klaim DNA/Positioning
  karena fiturnya belum dibuat. BKB merancang produk yang akan dibangun.
- Menulis kompetitor di BKB — nama merek, harga, fitur, atau perbandingan
  "N× lebih murah dari X". Kalau review `business-reviewer` merekomendasikan
  perubahan, terapkan **kesimpulannya** (DNA diturunkan, harga dikoreksi,
  positioning dipertajam), bukan data kompetitornya.
- Merujuk file produk lain ("lihat timelog/business-knowledge-base.md").
  Tiap folder produk harus berdiri sendiri karena skill hilir membaca
  satu folder saja. Fakta bersama disalin per produk lengkap dengan
  tanggal dan sumbernya — aturan "satu fakta satu rumah" berlaku di dalam
  satu produk, bukan lintas produk.

## File pendukung

- `assets/business-knowledge-base.md` — cetakan BKB 5 section, komentar
  panduan tiap bagian. Salin untuk produk baru.
- `references/aturan-penulisan.md` — uji kualitas per section dengan
  contoh lolos/gagal dari Timelog. Baca sebelum mengisi atau mengaudit.
