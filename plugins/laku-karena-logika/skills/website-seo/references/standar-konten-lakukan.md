# Standar konten dari API Lakukan: menu Panduan & Blog

Disetujui user pada 4 Okt 2026 untuk website Timebase. Instruksi user: "tambahkan menu panduan, artikelnya diambil dari api.lakukan.id … ada kategorinya juga, pastikan tampilannya memuat per kategori juga".

## Sumber data
- API publik: `https://api.lakukan.id/api`, dengan header `X-Company-Slug: <slug produk>` (contoh: `timebase`). Company id (mis. `venturo`) tidak dipakai di header; slug produk yang menentukan marketplace.
- Endpoint yang dipakai:
  - `GET /article-categories` → pohon kategori (`children`, `sort_order`, `description`).
  - `GET /articles?limit=100&page=N` → daftar artikel (`meta.pagination`).
  - `GET /articles/<slug>` → isi HTML lengkap (`content`, `cover_url`, `author`, `updated_at`).
- Hanya **kategori anak dari `kategori_induk`** (default `docs`) yang ditampilkan. Artikel di kategori induk itu sendiri atau di kategori lain (mis. Blog, artikel uji "aaa"/"ccc") dilewati.
- Konfigurasi di `site.json`: `"lakukan": {"api": …, "company_slug": "<slug>", "kategori_panduan": "docs", "kategori_blog": "blog", "blog_lead": "…"}`. Menu utama: `… Harga, ["/panduan", "Panduan"], ["/blog", "Blog"]`. Menu Panduan opsional (hanya bila produk punya artikel bantuan).
- Build menyimpan data ke `data/lakukan-cache.json`. Bila API gagal, build memakai cache (WARNING).
- Artikel baru di CMS baru tampil setelah build ulang dan deploy.

## Struktur halaman (`scripts/lakukan.py`)
- **`/panduan` (hub):**
  - Hero ringkas: badge "Pusat bantuan", H1 "Panduan <Brand>", dan satu kalimat pembuka.
  - Chip kategori dengan jumlah artikel.
  - **Satu kartu per kategori**: ikon bulat gradasi, nama kategori, deskripsi, daftar judul artikel (baris bergaris + ›), dan link "N panduan →".
  - 5 kategori disusun 3 + 2.
  - Bukan grid sampul per kategori: kategori yang hanya berisi 1 artikel akan menyisakan ruang kosong. User menolak ruang kosong.
- **`/panduan/<kategori>`:**
  - Chip kategori, dengan chip aktif berwarna gelap.
  - Grid kartu artikel: sampul 16:9, judul, ringkasan maksimal 3 baris.
- **`/panduan/<kategori>/<artikel>`:**
  - Layout dokumen seperti halaman legal: navigasi kiri per kategori (grup aktif terbuka, artikel aktif disorot) dan "Daftar panduan" tertutup di mobile.
  - Isi artikel: "Terakhir diperbarui <tanggal>" → sampul → isi HTML (dibersihkan dari script/iframe/on*).
  - Gambar isi memakai lazy load. Blockquote tampil sebagai kotak tips.
  - Di bawah artikel ada tombol Sebelumnya/Berikutnya dalam kategori yang sama.
- **URL kategori** membuang awalan slug produk: `timebase-memulai` → `/panduan/memulai`.
- **Menu "Panduan"** tetap aktif di semua sub-halaman.
- **Footer:**
  - Kolom tambahan "Panduan" berisi daftar kategori + "Semua panduan".
  - Kolom artikel SEO berganti nama menjadi "Artikel".
- **SEO:** semua halaman panduan index dan masuk sitemap. JSON-LD berisi BreadcrumbList bertingkat, dan halaman artikel juga memakai `Article`.
- **Di mobile:** chip kategori satu baris yang bisa digeser, dan chip aktif otomatis digeser ke dalam layar.

## Tidak boleh
- Mengedit isi artikel dari CMS di build. Penulisan merek seperti "TimeBase" diikuti apa adanya; perbaikan dilakukan di CMS.
- Menjalankan cek kata minimum atau ilustrasi wajib halaman SEO pada halaman panduan.

## Blog (WAJIB di setiap landing page)
User (4 Okt 2026): "tambahkan menu Blog, connect ke API Lakukan juga, ambil artikel di kategori Blog. Di semua website landing page saya nantinya harus selalu ada ini."
- **Build ERROR** bila `lakukan.company_slug` kosong, atau bila `["/blog", "Blog"]` tidak ada di menu utama.
- Sumber: kategori `kategori_blog` (default `blog`) beserta sub-kategorinya. Artikel diurutkan dari yang terbaru (`published_at`).
- **Artikel draf/uji coba tidak diterbitkan.** Artikel tanpa ringkasan dengan isi < 60 kata (mis. "aaa" berisi "bbbb") memicu WARNING dan dilewati. Perbaikannya di CMS, bukan di build.
- **Blog belum punya artikel:**
  - `/blog` menampilkan kartu "Artikel pertama segera terbit" (ikon bulat, plus tautan ke Panduan bila ada).
  - Halaman ini **noindex** dan tidak masuk sitemap. Build memberi WARNING.
- **`/blog`:**
  - Hero ringkas: badge berupa kalimat ajakan (`blog_eyebrow`, default "Pusat edukasi", pilihan user), H1 "Blog <Brand>", dan `blog_lead`. **Badge tidak boleh mengulang H1.** User (4 Okt 2026) menolak badge "Blog" di atas "Blog Timebase": "masih memiliki makna yang sama".
  - Artikel terbaru tampil sebagai kartu besar horizontal (sampul 58% | kategori · tanggal, judul, ringkasan), lalu grid kartu di bawahnya.
  - Paginasi 12 artikel per halaman (`/blog/halaman/N`).
  - Chip kategori dan `/blog/kategori/<k>` hanya muncul bila Blog punya sub-kategori yang berisi artikel.
- **`/blog/<artikel>`:**
  - Dua kolom, dengan tepi kiri-kanan sejajar header (artikel tidak di-center, karena hero rata kiri).
  - Kolom kiri: "Terakhir diperbarui <tanggal>", sampul, isi (maks. 780px).
  - Kolom kanan: kotak sticky berisi **"Di artikel ini"** (daftar isi dari semua H2 artikel, dengan sorotan bagian yang sedang dibaca), lalu "Artikel terbaru" (5 judul + tanggal, "Semua artikel →") bila ada artikel lain.
  - **Artikel tidak dilebarkan memenuhi layar.** Baris > 90 karakter melelahkan dibaca, jadi kolom kanan diisi daftar isi. Ini rekomendasi yang dipakai saat user (4 Okt 2026) bertanya "artikelnya kenapa tidak penuh di layar? kolom kanan diberikan apa, atau dilebarkan saja?".
  - Daftar isi hanya muncul bila artikel punya ≥ 2 H2. Di mobile daftar isi disembunyikan, dan kotak samping yang kosong ikut disembunyikan.
  - Di bawahnya ada CTA penutup (`cta`) di band `end`.
  - JSON-LD memakai `BlogPosting` dan BreadcrumbList Blog → (kategori) → artikel.
- **Footer:** kolom **"Blog"** berisi **5 artikel terbaru** dari API + "Semua artikel →". Isinya ikut berubah setiap build.
  - Judul ditampilkan **ringkas dan selalu 1 baris**: bagian sebelum ":" (`judul_pendek`). Sisanya dipotong "…" oleh CSS (`white-space: nowrap; text-overflow: ellipsis`, dan kolom grid `min-width: 0` supaya kolom tidak melebar). Judul lengkap tersedia di atribut `title`.
  - User (4 Okt 2026): "title blog terlalu panjang untuk diletakkan di footer", lalu memilih opsi ini.

## Baris info artikel (Panduan & Blog)
Hanya **"Terakhir diperbarui <tanggal>"** (dari `updated_at`, dalam `<time datetime>`), kecil dan abu. Nama penulis tidak ditampilkan. User (4 Okt 2026): "tidak perlu ada nama penulisnya, cukup informasikan last update-nya kapan". Penulis tetap ada di JSON-LD `author` untuk mesin pencari.


## Halaman "(SEO saja)" → artikel Blog di CMS
User (4 Okt 2026): halaman keyword plan berlabel **"(SEO saja)"** tidak dibuat sebagai halaman statis. Isinya masuk Blog dinamis di CMS Lakukan.
1. `python3 tools/ekspor_blog.py` → `export/blog/<slug>.json` + `.html` (pratinjau) + `gambar/*.png`. Hasil ekspor:
   - kartu → H3 + paragraf, callout → blockquote, FAQ → H3 + jawaban;
   - SVG ilustrasi dirender ke PNG 1600×1000 (Quick Look macOS);
   - token `{{cta}}` dibuang, dan link antar halaman "(SEO saja)" diarahkan ke `/blog/<slug>`.
2. Masukkan ke kategori Blog di CMS dengan **slug yang sama**:
   ```bash
   LAKUKAN_API_KEY=… python3 tools/unggah_blog.py      # --draf untuk menyimpan sebagai draf
   ```
   - Autentikasinya admin API `https://api.lakukan.id/core/v1/admin` dengan header **`X-API-Key`** (bukan Bearer). Kunci terikat ke satu company, jadi `X-Company-Slug` tidak diperlukan.
   - Urutannya: buat **draf** → unggah sampul (`/articles/{slug}/cover`) dan gambar isi (`/content-media`, mengembalikan URL publik) → `PUT` isi dengan URL CMS + status. Artikel tidak pernah tampil setengah jadi.
   - Gambar pertama dipakai sebagai sampul dan tidak diulang di isi.
   - Slug yang sudah ada dilewati, kecuali memakai `--perbarui`.
   - **Kunci API hanya lewat env.** Jangan disimpan di file proyek, skill, atau memori. Sarankan user merotasi kunci yang pernah ditempel di chat.
3. `build.py` mengurus sisanya secara otomatis:
   - halaman `ad_group: "(SEO saja)"` **tidak dibangun statis**;
   - URL lamanya menjadi halaman pengalihan (meta refresh + canonical ke `/blog/<slug>`, noindex);
   - link wajib dari keyword plan diterima sebagai `/blog/<slug>`;
   - gambar halaman itu tidak dianggap "tidak dipakai";
   - `legal_reviewed: false` untuk URL lama ikut membuat artikel blognya noindex (mis. UU PDP yang belum direview ahli hukum).

   Link internal di `content/*.html` diarahkan ke `/blog/<slug>`. WARNING muncul bila artikelnya belum ada di CMS.
