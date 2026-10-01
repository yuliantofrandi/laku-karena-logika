# Standar Minimum UI per Section

Disetujui user (website Timebase, 1 Okt 2026): *"harusnya UI-nya bagus seperti 3 section yang saya suruh revisi ini … minimal standard setiap section desain UI-nya seperti ini"*.

Acuan visual:
- `contoh-ui/standar-section-disetujui.jpg` — hero (bagian bawah) → band intro → section pertama, versi yang disetujui.
- `contoh-ui/referensi-hero-user.webp` — referensi hero asli dari user (foto orang + laptop di atas bentuk gradasi).

**Setiap section di setiap website wajib setidaknya setara dengan acuan ini.** Kalau sebuah section tidak bisa dibuat seperti ini, ubah isinya, jangan turunkan standarnya.

## 1. Hero
Lihat "Hero" di `aturan-sales-page.md`. Ringkasnya: badge pill gradasi · H1 Montserrat 800 gelap ≤55 karakter · subjudul abu 2–3 baris · satu CTA gradasi dengan → · tiga statistik sejajar (angka besar + label kecil) · gambar di atas bentuk gradasi brand · latar gradasi lembut.

## 2. Band intro (tepat di bawah hero)
- **Logo cloud tanpa kotak:** label kecil berhuruf kapital renggang ("DIPAKAI TIM DI BERBAGAI INDUSTRI"), lalu deretan nama/logo abu-abu (Montserrat 800, ±17px; logo asli: grayscale, tinggi seragam ±28px), lalu garis tipis pemisah selebar kontainer.
- **Pernyataan rata tengah:** satu paragraf entitas 1–2 kalimat ("<Brand> adalah …"), ±20px, maks ±820px, nama brand berwarna primer. Rata kiri di mobile.
- Latar putih.

## 3. Section isi (setiap H2)
| Elemen | Standar |
|---|---|
| Latar | Bergantian, **dimulai abu muda** setelah band intro (putih), supaya batas antar-section selalu terlihat. Padding atas-bawah ±64px (±44px mobile) |
| Tata letak | Ada gambar → **dua kolom** teks \| gambar, posisi gambar bergantian kiri-kanan. Tanpa gambar → judul kiri (sticky) \| isi kanan. Mobile: menumpuk |
| Judul (H2) | Montserrat 800, ±32px, ≤12 kata, idealnya 2 baris. Pertanyaan atau pernyataan yang tajam |
| Pembuka | **1–2 kalimat**, ≤ ±30 kata, warna abu tua. Tidak ada dua paragraf berturut-turut |
| Isi yang dipindai | **Wajib minimal satu**: daftar centang (`ul.checks`, awalan tebal + sisa kalimat biasa), kartu (`div.grid` > `.card`, judul + 1 kalimat, `span.num` untuk langkah), tabel kecil, callout, atau gambar |
| Gambar | Ilustrasi dalam kartu membulat (radius ±18px, latar tint lembut) + caption kecil abu di bawahnya |
| Blok lebar | Kartu, tabel, harga, testimoni tampil selebar kontainer di bawah baris dua kolom |
| Teks tersembunyi | **Tidak boleh.** Tidak ada "Baca selengkapnya". FAQ boleh accordion |

## 4. Elemen global yang selalu ada
- Header: logo kiri · menu tengah · Sign In + Langganan kanan (sticky, latar putih transparan + blur).
- Tombol WA melayang minimalis di kanan bawah.
- Footer berlatar abu muda, dengan ruang bawah untuk tombol WA di dalam footer.
- Satu kontainer (`--wrap`) untuk semua bagian, sehingga tepi kiri-kanan selalu segaris.

## Cek otomatis (`build.py`)
- **ERROR** jika ada section yang **hanya berisi teks** (tanpa poin, kartu, tabel, callout, blockquote, FAQ, atau gambar).
- **WARNING** jika sebuah section punya > 2 paragraf, judul > 12 kata, atau ada paragraf > ±45 kata.

## Cek manual sebelum melapor selesai
1. Screenshot setiap halaman per band di 1440px dan 375px. Bandingkan dengan `contoh-ui/standar-section-disetujui.jpg`: kepadatan teks, ruang kosong, ukuran judul, dan dua kolom yang seimbang.
2. Pastikan tidak ada dua band berurutan dengan latar sama (batas harus terlihat).
3. Ukur tepi kiri-kanan dan overflow di 1440/1280/768/375px.
