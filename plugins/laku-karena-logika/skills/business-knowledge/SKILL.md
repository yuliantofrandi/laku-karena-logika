---
name: business-knowledge
description: Menyusun, mengisi, merevisi, dan mengaudit Business Knowledge Base (BKB) untuk satu produk SaaS — dokumen kanonik `business-knowledge-base.md` dengan 5 section (Business Overview, Brand Strategy, Product-to-Value Mapping, Pricing Plan, Target Customer Profile) — mengikuti struktur dan aturan yang sudah divalidasi lewat produk SaaS nyata. Pakai skill ini setiap kali user ingin menambah produk baru, menulis vision/mission/positioning/DNA/pricing/persona/ICP untuk produk SaaS, "buat BKB", "dokumen strategi bisnis", "knowledge base produk", mengisi section yang masih kosong, atau mengaudit duplikasi/konsistensi BKB — bahkan kalau user tidak menyebut kata "BKB" atau "template", selama hasilnya adalah dokumen strategi produk dalam struktur ini. Ini lapisan Product Knowledge → Business Intelligence dari AI Marketing OS; skill hilir (brand-story-writer, company-profile-writer, content-ideator) membaca outputnya.
---

# Business Knowledge Base (BKB)

Satu folder per produk. Dokumen yang dirawat skill ini adalah
`business-knowledge-base.md` — satu berkas "kondisi berlaku saat ini" yang
dibaca skill hilir apa adanya. Tugas skill ini: memastikan produk baru
mendapat struktur yang persis sama dengan yang sudah ada, dan isinya lolos
uji kualitas yang sama.

Angka dan risiko kompetitor tinggal di dalam BKB — §2 Opportunity (Celah
pasar) dan Positioning — sebagai satu-satunya rumahnya. Tidak ada file
kompetitor terpisah.

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
lalu beri rekomendasi. Kalau isian masuk akal, langsung tulis — jangan
minta konfirmasi berulang. Jangan mengarang angka: data yang tidak ada
ditulis `[INPUT-NEEDED]`, klaim yang belum terbukti diberi `[?]`.

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
   apa yang mereka pakai sekarang, harga kompetitor yang diketahui. Satu
   putaran pertanyaan, bukan wawancara panjang — sisanya `[INPUT-NEEDED]`.
3. Isi dengan **urutan pengisian**, bukan urutan section:
   `§1 identitas → §2 Opportunity → §3 P2V → §5 Target →
   §2 DNA & Positioning → §4 Pricing`. Positioning dan harga terakhir
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
- Kalau harga berubah → tinjau §3 baris harga dan §5 "Skema yang
  ditawarkan". Kalau DNA naik/turun level → tinjau Positioning dan Tagline.

### C. Audit

Diminta "audit", "cek konsistensi", "rapikan", atau sebelum skill hilir
memakai dokumen:

1. Duplikasi: satu fakta muncul di dua section? Sisakan di rumahnya.
2. Penanda: semua `[?]` masih relevan? `[INPUT-NEEDED]` masih kosong?
3. Konsistensi lintas section: harga tertinggi §4 < batas di §2 Celah
   pasar; tiap kapabilitas §3 punya baris ✓ di §4; tiap market §5
   menyebut skema yang ada di §4; positioning hanya memakai klaim yang
   sudah ada di section lain. Pengecualian yang wajar: selama §4 masih
   `[INPUT-NEEDED]`, "Skema yang ditawarkan" di §5 dan baris harga di §3
   ikut `[INPUT-NEEDED]` — itu bukan temuan, itu status draf.
4. Konsistensi angka kompetitor di dalam §2: harga/batas kompetitor yang
   dipakai di "Celah pasar" harus sama dengan yang dipakai untuk menurunkan
   batas harga dan yang dirujuk blok `[!]`. Satu angka kompetitor, satu
   nilai — jangan ada dua versi di section yang sama.

Laporkan temuan sebagai daftar bernomor dengan lokasi (§ dan baris), lalu
perbaiki yang disetujui.

## Yang tidak boleh dilakukan

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
- Mengisi angka pasar/harga tanpa sumber. `[INPUT-NEEDED]` bukan aib.
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
