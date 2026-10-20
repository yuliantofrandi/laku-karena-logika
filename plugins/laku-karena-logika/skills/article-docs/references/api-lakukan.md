# API CMS Lakukan — yang dipakai skill ini

Semua perilaku di bawah sudah diverifikasi langsung ke server (Okt 2026). Spesifikasi resmi: `GET https://api.lakukan.id/docs/openapi.yaml` dengan header `X-API-Key` (halaman `/docs` meminta key yang sama).

## Koneksi
- **Base URL:** `https://api.lakukan.id`
- **Admin** (`/core/v1/admin/*`): header `X-API-Key: <key>`. Company ditentukan oleh key, jadi admin tidak butuh `X-Company-Slug`. Key diminta ke user setiap sesi dan disimpan hanya di env `LAKUKAN_API_KEY`. Jangan menulis key ke file, memori, atau commit.
- **Publik** (`/api/*`): wajib header `X-Company-Slug: <slug produk>`, misalnya `timebase`. Slug ini milik produk, bukan nama perusahaan. Jika tidak dikirim, server membalas 400 "Marketplace not specified". Slug yang tidak dikenal dibalas 404.
- **Cloudflare** menolak user-agent bawaan Python `urllib` (HTTP 403, `error code: 1010`). `posting.py` sudah mengirim User-Agent sendiri.
- Sesekali koneksi direset (`Connection reset by peer`). `posting.py` mencoba ulang hingga 3 kali.

## Kategori
| Aksi | Endpoint | Catatan |
|---|---|---|
| Pohon kategori | `GET /core/v1/admin/article-categories` | Berisi `children` (bertingkat, **maks 3 level**), `article_count` (artikel published langsung di node), dan `total_article_count` (termasuk keturunan). |
| Buat | `POST /core/v1/admin/article-categories` | `{slug, name, description, sort_order, parent_id}` → 201. `parent_id` adalah id kategori induk. |
| Ubah / pindah | `PUT /core/v1/admin/article-categories/:slug` | `name`, `description`, `sort_order`, dan **`parent_id`** (memindahkan kategori). Slug tidak bisa diubah. |
| Hapus | `DELETE /core/v1/admin/article-categories/:slug` | Soft delete. Artikel di dalamnya menjadi uncategorised. |

Struktur wajib: **level 0 = `docs` (Docs), level 1 = kelompok tutorial.** Skill `website-seo` membangun menu Panduan dari anak-anak `docs` dan membuang awalan slug produk dari URL (`timebase-monitoring` → `/panduan/monitoring`).

## Artikel
| Aksi | Endpoint | Catatan |
|---|---|---|
| Buat | `POST /core/v1/admin/articles` | `{title 3–160, slug ≤180, excerpt ≤280, content HTML, status draft/published, category_ids: [uuid, …]}` → 201. |
| Detail | `GET /core/v1/admin/articles/:slug` | Mengembalikan artikel dalam status apa pun. Artikel yang dihapus → 404. |
| Ubah | `PUT /core/v1/admin/articles/:slug` | Semua field opsional. **Slug tidak bisa diubah.** `status → published` mengisi `published_at`; `→ draft` mengosongkannya. `category_ids`: tidak dikirim/`null` = kategori tetap, `[]` = hapus semua, array = ganti seluruh set. |
| Hapus | `DELETE /core/v1/admin/articles/:slug` | Soft delete. Sampul dan media isi ikut dibersihkan. |
| Gambar isi | `POST /core/v1/admin/articles/:slug/content-media` | Multipart `file`. Mengembalikan `{data:{url}}` (URL publik GCS) yang di-embed sebagai `<img src>`. Artikel harus sudah ada, jadi buat draft dulu. |
| Sampul | `POST /core/v1/admin/articles/:slug/cover` | Multipart `file` (jpeg/png/webp). Sampul baru menggantikan yang lama. |

- Daftar publik `GET /api/articles` diurutkan **`published_at` menurun**. Karena itu artikel diterbitkan dari urutan terakhir ke pertama, dengan jeda sekitar 1 detik.
- `PUT` dengan `status: published` pada artikel yang sudah published tidak perlu dikirim. `posting.py` hanya mengirim `status` bila nilainya berubah, sehingga `published_at` dan urutan publik tetap.
- Mengganti slug berarti membuat artikel baru lalu menghapus yang lama.
- Mengunggah ulang gambar saat update membuat aset lama tetap tersimpan, karena tidak ada endpoint hapus per media isi. Aset itu tidak berbahaya, tapi hindari update berulang tanpa perlu.
- `author` diisi server ("Tim Redaksi").

### Kategori artikel = `category_ids` / `categories` (berubah Okt 2026)
- **Kirim** kategori lewat `category_ids` (array UUID). Field lama `category_id` **diabaikan tanpa error**, sehingga artikel tersimpan tanpa kategori dan tidak muncul di menu kategori website. Kejadian nyata: 2 portfolio Venturo sempat tampil tanpa kategori karena ini.
- **Baca** kategori dari `categories`: selalu array (`[]` bila kosong), berisi `{id, slug, name}`, setara tanpa kategori utama. Field `category` sudah tidak ada.
- `posting.py` mengirim `category_ids: [id kelompok]`, lalu membaca ulang artikel dan **berhenti dengan error** bila kategorinya tidak sesuai. `publik` menandai `KATEGORI SALAH` bila kategori di API publik tidak cocok.

## Publik (untuk verifikasi)
- `GET /api/article-categories`
- `GET /api/articles?category=<slug kategori>&limit=100` — mencakup kategori itu **dan seluruh sub-kategorinya**. Parameter lain: `search`, `page`, `limit`.
- `GET /api/articles/:slug`

Semua endpoint publik memakai header `X-Company-Slug`.
