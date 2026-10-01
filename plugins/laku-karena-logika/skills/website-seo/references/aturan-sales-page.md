# Aturan Sales Page (Beranda & Landing Ads)

Tujuan: konversi tinggi **tanpa** klaim yang tidak bisa dipertanggungjawabkan. Framework halaman = **AIDA**; blok Interest memakai **PAS**.

## Urutan blok beranda

| # | Blok | Tahap | Isi wajib |
|---|---|---|---|
| 1 | Hero | Attention | **H1 = hasil terbesar untuk klien**, bukan nama/fitur produk. Biasanya juga menjawab keberatan utama. Sub 1–2 kalimat (mekanisme + manfaat). CTA utama + CTA kedua. Microcopy risk reversal di bawah tombol |
| 2 | Paragraf entitas | — | "<Brand> adalah <category BKB> untuk <segmen>…" untuk Google & mesin AI. Primary = nama brand |
| 3 | `{{bukti_sosial}}` | Interest | Metrik + logo/industri klien |
| 4 | Problem | Interest (P) | Situasi pembeli dengan bahasanya sendiri (BKB Persona 1 Pain Points) |
| 5 | Agitation | Interest (A) | Kerugian **waktu** dan **uang** dengan hitungan transparan (rumusnya ditulis), plus kerugian emosional (kepercayaan tim) |
| 6 | Solution | Interest (S) → Desire | Kapabilitas inti BKB §4 dalam 3–4 kartu + link ke halaman Prioritas 1 |
| 7 | Cara kerja | Desire | 3 langkah sampai aktif, sesuai model penjualan. Self-serve: Pilih skema → Bayar, akun aktif → Pasang/onboarding. Mengurangi kesan "ribet" |
| 8 | Penanganan keberatan | Desire | Keberatan terbesar Persona 1/2 (mis. "dicap mata-mata") dijawab dengan checklist fakta |
| 9 | `{{testimoni}}` | Desire | 3 kutipan: masalah → hasil, nama berinisial, jabatan, jenis perusahaan + kota |
| 10 | Harga + `{{tanpa_risiko}}` | Desire → Action | Kartu skema, masing-masing dengan tombol beli (`Pilih <Skema>` → checkout `{skema}`/`{periode}`) + link bayar tahunan; satu "Disarankan" (sesuai BKB §5); lalu risk reversal |
| 11 | Urgensi | Action | Alasan mulai sekarang |
| 12 | Jujur soal batas | Kepercayaan | GAP utama BKB, 2–3 kalimat |
| 13 | FAQ | Action | Keberatan terakhir: kontrak, reaksi tim, lama aktif, siapa yang tidak cocok |
| 14 | `{{cta}}` | Action | Judul berorientasi hasil + 2 tombol + syarat |

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
| **CTA** | Kata kerja + kepemilikan, sesuai model penjualan. Self-serve: "Aktifkan <Produk> untuk Tim Saya", "Pilih Skema 2", "Bandingkan Skema" | "Kirim", "Submit", "Klik di sini"; CTA demo untuk produk yang dijual langsung langganan |
| **Anchoring harga** | Skema termahal di kanan, skema yang disarankan di tengah dengan badge | Coret harga palsu |

## Teks CTA & copy global

Semua teks yang dipakai berulang ada di `site.json → copy` (`nav_cta`, `cta_primary`, `cta_secondary`, `cta_title`, `cta_text`, `plan_button`, `chat_text`, `chat_link`, `risk_label`, `risk_extra`, `proof_caption`). Ubah di sana, jangan di `build.py`.

## Navigasi

- Menu utama ringkas: **satu menu group** untuk halaman solusi/landing (mis. "Solusi ▾" → Monitoring, Time Tracking, Kerja Remote, Absensi Hybrid, masing-masing dengan deskripsi 1 baris), lalu **Harga**, lalu tombol CTA. Halaman panduan/SEO cukup di footer.
- Dropdown memakai `<details>`/`<summary>` (tanpa JavaScript). Panel rata kanan agar tidak terpotong di layar sempit; di mobile tampil inline di dalam menu hamburger. Group diberi tanda aktif saat salah satu submenunya sedang dibuka.

## Konversi teknis

- CTA utama = link ke `checkout_url` (template `{skema}`, `{periode}`), `rel="nofollow"`. Kosong = ke `/harga#pilih-skema`. WhatsApp hanya link opsional "Ada pertanyaan sebelum berlangganan?" di blok CTA. Tanpa widget chat pihak ketiga.
- Sticky CTA bawah di mobile (≤640px).
- Konversi Google Ads dipasang pada **pembayaran berhasil** (klik tombol beli sebagai konversi sekunder) **sebelum** iklan jalan.
