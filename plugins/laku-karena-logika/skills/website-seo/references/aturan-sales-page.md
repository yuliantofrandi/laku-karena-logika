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

Semua teks yang dipakai berulang ada di `site.json → copy` (`nav_cta`, `cta_primary`, `cta_secondary`, `cta_title`, `cta_text`, `plan_button`, `wa_title`, `wa_subtitle`, `risk_label`, `risk_extra`, `proof_caption`). Ubah di sana, jangan di `build.py`.

## Halaman Whitelabel (wajib di setiap produk)

Semua produk SaaS/GaaS user bisa dibeli dengan merek sendiri. Halaman `/whitelabel` memakai **copy global** (`assets/starter/content/whitelabel.html`), jadi tidak ditulis ulang per produk. Bagian khusus produk masuk lewat token.

| Blok | Isi |
|---|---|
| Hero | H1 memuat "Whitelabel" + hasil: jual software dengan merek sendiri tanpa membangun dari nol. CTA `Minta Penawaran Whitelabel` (WA, teks otomatis menyebut brand) + `Lihat Cara Kerjanya` |
| Paragraf entitas | "Program whitelabel <Brand> …" + `{{deskripsi_kecil}}` |
| Untuk siapa | Konsultan & agensi · software house & integrator · reseller & distributor · grup & asosiasi |
| Agitasi | Membangun sendiri: waktu, biaya tetap, pemeliharaan tanpa akhir, risiko produk. **Tanpa angka karangan** |
| Perbandingan | Tabel "Whitelabel vs membangun sendiri" (perbandingan metode, aman) |
| Yang dijual | `{{daftar_solusi}}` dari menu group Solusi + link ke harga |
| Kustomisasi / ditangani | `{{wl_kustomisasi}}`, `{{wl_ditangani}}` dari `site.json → whitelabel` (dikonfirmasi per produk) |
| Cara kerja | Konsultasi → Penawaran & kesepakatan → Penyiapan brand → Rilis ke klien |
| Keuntungan | Produk sendiri tanpa tim dev · pendapatan berulang · klien tetap milik Anda · cepat ke pasar · ikut pembaruan |
| FAQ | Apa itu whitelabel · apakah klien melihat merek kami · harga (per penawaran) · perlu tim IT? · beda dengan langganan biasa |
| CTA | `{{cta_whitelabel}}`: konsultasi WA, **bukan checkout**, karena whitelabel adalah penawaran per klien |

Larangan: tidak menyebut harga, minimum lisensi, bagi hasil, atau persentase penghematan yang belum diputuskan user. Halaman ini sengaja tidak memakai `{{bukti_sosial}}`/`{{testimoni}}` sampai ada mitra whitelabel asli.

## Navigasi

- Menu utama ringkas: **satu menu group** untuk halaman solusi/landing (mis. "Solusi ▾" → Monitoring, Time Tracking, Kerja Remote, Absensi Hybrid, masing-masing dengan deskripsi 1 baris), lalu **Whitelabel** (wajib), lalu **Harga**, lalu tombol CTA. Halaman panduan/SEO cukup di footer.
- Dropdown memakai `<details>`/`<summary>` (tanpa JavaScript). Panel rata kanan agar tidak terpotong di layar sempit; di mobile tampil inline di dalam menu hamburger. Group diberi tanda aktif saat salah satu submenunya sedang dibuka.

## Konversi teknis

- CTA utama = link ke `checkout_url` (template `{skema}`, `{periode}`), `rel="nofollow"`. Kosong = ke `/harga#pilih-skema`.
- **Tombol WA marketing melayang di bagian bawah SETIAP halaman, desktop & mobile** (aturan tetap user). Bentuk dari contoh user, **minimalis, warna dari design system produk** (bukan warna gambar contoh): latar solid `--ink`, tanpa bingkai gradasi, bayangan tipis, **padding lega dan teks kecil** (desktop: padding 12/22px, judul 14px, subjudul 11.5px; mobile: padding 10/16px, judul 12.5px, subjudul 10.5px), ikon WhatsApp hijau di kiri (SVG inline, boleh tetap hijau agar mudah dikenali), judul tebal putih `copy.wa_title` ("Hubungi Kami !!"), dan subjudul `copy.wa_subtitle` ("Konsultasi 100% Gratis"). Link `wa.me/<whatsapp>?text=<whatsapp_text>`, `target="_blank" rel="nofollow noopener"`.
  - Desktop: pojok kanan bawah. `body` diberi `padding-bottom` agar footer tidak tertutup.
  - Mobile (≤640px): **hanya tombol WA**, versi ringkas di kanan bawah (±181×49 px, <3% layar). **Judul + subjudul tetap tampil.** Jangan tambahkan tombol lain di bar bawah, dan jangan dibuat selebar layar.
  - Tanpa widget/skrip chat pihak ketiga. WA dipakai untuk konsultasi, bukan pengganti checkout dan bukan "jadwalkan demo".
- Konversi Google Ads dipasang pada **pembayaran berhasil** (klik tombol beli sebagai konversi sekunder) **sebelum** iklan jalan.
