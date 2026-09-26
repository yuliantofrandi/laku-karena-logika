---
name: keyword-research
description: Riset buying keyword di Google Ads Keyword Planner lewat browser, lalu susun jadi Excel berisi keyword plan, page brief (title/meta/H1/slug), dan negative keyword. Pakai saat diminta cari kata kunci, riset keyword, atau bikin rencana Google Ads/SEO untuk sebuah produk.
---

# Riset Keyword Google Ads → Excel Plan

Alur lengkap dari riset di Keyword Planner sampai jadi file Excel siap eksekusi.
Bahasa deliverable: **Indonesia**. Bahasa penjelasan ke user: ikuti bahasa user.

## Langkah 0 — Pahami produknya dulu

Baca knowledge base / brief produk yang dilampirkan user sebelum menyentuh Keyword Planner.
Yang harus didapat: positioning, harga sendiri, harga kompetitor, nama kompetitor,
segmen target, dan pain point pembeli. Tanpa ini, keyword tidak bisa dinilai relevansinya.

Tanyakan ke user (pakai AskUserQuestion, satu ronde saja):
- Sumber data: ambil live dari Keyword Planner, atau cukup daftar tanpa angka?
- Tujuan: Google Ads, SEO organik, atau keduanya?

Jangan tanya lagi setelah itu kecuali ada keputusan yang benar-benar mengubah hasil.

## Langkah 1 — Riset di Keyword Planner (browser)

Pakai tool Claude-in-Chrome. Buka `ads.google.com/aw/keywordplanner/home` →
"Temukan kata kunci baru" → pastikan lokasi **Indonesia** dan bahasa **Indonesian**.

Masukkan maksimal 10 seed, ketik satu-satu diakhiri Enter (jadi chip). **Dua pass:**

**Pass 1 — seed generik produk.** Contoh untuk software absensi:
`aplikasi absensi karyawan`, `software absensi karyawan`, `absensi online`,
`aplikasi absensi whatsapp`, `aplikasi hris`, `harga aplikasi absensi`

**Pass 2 — seed kompetitor + harga + long-tail spesifik.** Nama kompetitor dari knowledge base,
`harga <kompetitor>`, plus 2–3 long-tail yang mendeskripsikan produk persis.
Pass 2 penting bukan cuma untuk menemukan keyword, tapi untuk **membuktikan** long-tail
spesifik sering bervolume 0–10/bln — temuan itu sendiri adalah insight untuk user.

### Cara mengekstrak tabelnya (WAJIB — jangan pakai cara lain)

Tabel Keyword Planner ada di **shadow DOM** dan pakai **virtual scroll**.
`get_page_text` hanya mengembalikan ~10 baris, dan `querySelectorAll` biasa mengembalikan 0.
Pasang collector ini sekali lewat `javascript_tool`:

```js
window.__deepAll=function(sel,root=document,out=[]){
  out.push(...root.querySelectorAll(sel));
  root.querySelectorAll('*').forEach(e=>{ if(e.shadowRoot) window.__deepAll(sel,e.shadowRoot,out); });
  return out; };
window.__kw=new Map();
window.__grab=()=>{ window.__deepAll('.particle-table-row').forEach(r=>{
  const c=r.innerText.split('\n').map(s=>s.trim());
  if(c[0]) window.__kw.set(c[0], c.join(' | ')); }); return window.__kw.size; };
window.__grab()
```

Lalu pakai **browser_batch**: `computer.scroll` (down, 5 tik) → `javascript_tool: window.__grab()`,
diulang 8–10 kali per halaman. Jangan set `scrollTop` lewat JS — layout Google Ads collapse
saat di-set dan hasilnya 0. Naikkan "Jumlah baris" ke 100, lalu klik next page dan ulangi.

Output `javascript_tool` terpotong sekitar 1.000 karakter. Jadi:
1. Filter dulu di dalam page context (buang keyword tidak relevan, buang volume `0 – 10`).
2. Padatkan jadi `keyword ~ volume ~ kompetisi`.
3. Dump 20–22 baris per call.

Filter buang standar:
`siswa|pns|asn|sekolah|guru|mahasiswa|kuliah|dosen|kelas|rapat|seminar|peserta|tanda tangan|ttd|posyandu|skripsi|jurnal`

## Langkah 2 — Kelompokkan dan ambil keputusan struktur

Aturan yang sudah terbukti dipakai — terapkan sebagai default, jangan tanya ulang:

1. **1 URL slug = 1 halaman = 1 ad group.** Tiap keyword wajib punya slug tujuan.
   Kalau dua halaman menargetkan keyword yang sama → gabung, jangan biarkan berkanibal.
2. **Jangan bikin halaman yang menilai kompetitor.** Data kompetitor berubah sehingga halaman
   cepat basi, dan penilaian dari satu sudut pandang sulit dipertanggungjawabkan sebagai objektif.
   Yang boleh: membandingkan **metode** (fingerprint vs GPS vs QR vs foto+AI) dan **kategori**
   ("kelemahan HRIS lengkap kalau cuma butuh presensi") — bukan perusahaan.
   Uji kalimatnya: *bisa diganti nama merek dan jadi tuduhan → jangan tulis; tetap benar untuk
   semua produk sejenis → itu kategori, aman.*
3. **Keyword nama kompetitor tidak dipasang di Ads**, tapi **tetap jadi negative level akun** —
   tanpa itu keyword generik masih melayani query brand lewat close variant.
4. **Prioritas = urutan pengerjaan, bukan nilai penting.** 1 = hari pertama, 2 = minggu 3–4
   setelah ada search term report, 3 = uji budget kecil. Halaman Prioritas 1 harus jadi
   sebelum iklan bisa jalan.
5. **Halaman dipakai Ads + SEO sekaligus** → harus 1.000–1.500 kata, bukan hero + form.
   Ingatkan user: **belanja Ads bukan faktor ranking Google.** Dua kanal, satu halaman,
   tidak saling mengangkat.

## Langkah 3 — Bangun Excel-nya

Baca skill `anthropic-skills:xlsx` dulu. Font Arial. 4 sheet:

**Sheet 1 · Keyword Plan** — kolom: Prioritas | URL Slug | Ad Group | Keyword | Match Type |
Tipe Intent | Volume/bln (GKP) | Kompetisi | Bid Atas Hal. (rendah) | Bid Atas Hal. (tinggi) | Catatan.
Semua Match Type `Phrase` untuk awal. Keyword yang khusus SEO ditandai di kolom Ad Group:
`(SEO saja — tidak di Ads)`. Freeze panes di kolom Keyword, autofilter aktif.

**Sheet 2 · Page Brief** — satu baris per halaman: Prioritas | URL Slug | Nama Halaman | Ad Group |
Jml Keyword | Title Tag | Char | Cek | Meta Description | Char | Cek | H1 | Primary Keyword |
Secondary Keyword | Isi Wajib di Halaman | Internal Link ke.

- Title tag **40–60 karakter**, meta description **120–160**. Verifikasi pakai rumus, bukan hitung manual:
  `=LEN(F2)` dan `=IF(LEN(F2)>60,"Terlalu panjang",IF(LEN(F2)<40,"Terlalu pendek","OK"))`
- Jml Keyword: `=COUNTIF('Keyword Plan'!$B$2:$B$<last>,B2)`
- Baris TOTAL: `=SUM(...)` + `=IF(E<tot>=<jumlah keyword>,"Semua keyword ter-mapping","Ada keyword tanpa halaman — cek kolom URL Slug di sheet 1")`
- H1 dibuat **berbeda** dari Title Tag (Title untuk SERP, H1 untuk pembaca).
- Slug pendek, **tanpa angka tahun** (supaya tidak perlu redirect tiap tahun).
- Jangan tempel nama brand di Title; sebutkan sisa ruang karakternya ke user.

**Sheet 3 · Negative Keywords (Ads)** — Kategori | Negative Keyword | Match Type | Level Pemasangan | Alasan.
Kategori wajib: nama kompetitor, pencari gratis, DIY/tutorial, developer/akademik, segmen salah
(pendidikan & instansi), portal internal, download/bajakan, lowongan.
Kolom **Level Pemasangan** krusial: sebagian negative TIDAK boleh di level akun —
misal `excel` harus per-ad-group kalau ada ad group payroll, dan `gaji` jangan diblokir
kalau ada ad group slip gaji. Tandai baris itu dengan warna.

**Sheet 4 · Catatan & Cara Pakai** — layout dua kolom: A = label (lebar 34), B = penjelasan (lebar 118),
gridline dimatikan, header section berlatar gelap. Section wajib:
Mulai Dari Sini · Isi Tiap Sheet · Arti Kolom Sheet 1 · Arti Kolom Sheet 2 · **Kamus Istilah** ·
Aturan Yang Jangan Dilanggar · Cara Menjaga Objektif · Temuan Riset · Urutan Eksekusi ·
Ceklis Sebelum Publish · Sumber Data & Batasannya.

Kamus istilah wajib ada dan ditulis dengan bahasa sehari-hari — asumsikan pembacanya belum pernah
pakai Google Ads: keyword, search term, search term report, negative keyword, match type
(phrase/broad/exact), close variant, CPC, bid, bid cap, Quality Score, CPA, impression,
landing page, slug, index/noindex, sitemap.xml, schema markup, kanibalisasi keyword.

Jelaskan eksplisit dua hal yang paling sering disalahpahami:
- Kolom **Kompetisi bukan tingkat kesulitan SEO** — itu jumlah pengiklan lain yang memasang keyword sama.
- Kolom **Prioritas adalah urutan pengerjaan**, bukan nilai penting.

## Langkah 4 — Verifikasi sebelum kirim

Jalankan `scripts/recalc.py` dari skill xlsx sampai `total_errors: 0`, lalu cek lewat script:

- Jumlah baris keyword sesuai, tidak ada slug di sheet 1 yang tak ada di Page Brief (dan sebaliknya)
- Tidak ada slug duplikat di Page Brief
- Semua Char Title dan Meta berstatus `OK`
- Baris TOTAL berbunyi "Semua keyword ter-mapping"
- Regex nama kompetitor → **nol hasil** di sheet Keyword Plan dan Page Brief
- Tidak ada keyword Ads yang diblokir oleh negative level akun sendiri (konflik = bug)

## Cara melaporkan ke user

Simpan di `/mnt/user-data/outputs/`. Jangan cuma bilang "sudah jadi" — sampaikan **temuan yang
mengubah keputusan**, dan sampaikan yang tidak enak juga:

- Kalau volume tipis, katakan Ads realistis jadi kanal pelengkap, bukan mesin akuisisi.
- Kalau volume terbesar ada di nama kompetitor, katakan — lalu jelaskan bahwa sebagian besar
  volume itu intent **navigasional** (bukti: kemunculan `<brand> login`, `admin <brand>`,
  `download aplikasi <brand>`), jadi bukan berarti harus dikejar.
- Kalau keyword yang paling khas dari produk ternyata hampir tidak dicari, katakan terang-terangan:
  kategorinya belum ada di kepala pasar, harus dibangun lewat kanal non-search.
- Selalu sebutkan rentang bid yang ekstrem dan peringatkan soal bid cap.
- Selalu sebutkan bahwa volume berbentuk rentang karena akun belum punya riwayat belanja,
  dan sarankan riset ulang setelah kampanye jalan sebulan.
