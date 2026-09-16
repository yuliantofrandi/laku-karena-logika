# Laku karena logika — AI Marketing OS

Rangkaian skill Claude yang mengubah **pengetahuan produk** jadi **output marketing** untuk bisnis SaaS. Dibangun berlapis: dari mendokumentasikan strategi bisnis, sampai memproduksi materi marketing yang konsisten dengannya.

Semua skill di sini berbahasa Indonesia, berbasis pola yang sudah divalidasi lewat produk nyata (Timelog, Humanis).

## Install

```
/plugin marketplace add yuliantofrandi/laku-karena-logika
/plugin install laku-karena-logika@laku-karena-logika
```

## Skill di dalamnya

### `business-knowledge-base`
Menyusun, mengisi, merevisi, dan mengaudit **Business Knowledge Base (BKB)** satu produk SaaS — dokumen strategi bisnis yang jadi sumber kebenaran untuk semua materi marketing di hilir.

Struktur BKB (5 section):
1. **Business Overview** — identitas, vision, mission
2. **Brand Strategy** — category, DNA & pembeda berlevel, positioning, tagline, opportunity
3. **Product-to-Value Mapping** — problem → benefit → business outcome
4. **Pricing Plan** — tier, diskon volume, add-on
5. **Target Customer Profile** — segmen + buyer persona

Prinsip yang dijaga: satu fakta satu rumah (anti-duplikasi), tidak mengarang angka (`[INPUT-NEEDED]` / `[?]`), dan setiap keputusan strategis disertai alasannya.

## Pakai

```
/business-knowledge-base
```

Atau cukup minta dengan bahasa biasa, mis. *"buat BKB untuk produk baru X"*, *"isi positioning dan pricing"*, *"audit BKB, cek duplikasi"*. Skill aktif otomatis saat tugasnya menyusun dokumen strategi produk.

## Roadmap skill berikutnya

Plugin ini dirancang menampung banyak skill AI Marketing OS: competitive-landscape, brand-story-writer, company-profile-writer, content-ideator, blog/social content writer — masing-masing membaca output skill sebelumnya.
