"""Konten dari API Lakukan (api.lakukan.id), dirender statis: menu Panduan (per kategori) dan Blog.

Konfigurasi di site.json:
  "lakukan": {"api": "https://api.lakukan.id/api", "company_slug": "<slug>",
              "kategori_panduan": "docs", "kategori_blog": "blog", "blog_lead": "..."}

Saat build, data diambil dari API lalu disimpan ke data/lakukan-cache.json. Bila API tidak bisa
dihubungi, build memakai cache terakhir (WARNING), supaya situs tetap bisa dibangun.
Panduan = kategori anak dari `kategori_panduan`. Blog = kategori `kategori_blog` beserta anaknya.
Artikel lain (mis. uji coba di kategori induk Docs) dilewati.
"""
import html
import json
import re
import urllib.request
from pathlib import Path

CUR = ' aria-current="page"'


def _get(cfg, path):
    req = urllib.request.Request(cfg["api"].rstrip("/") + path,
                                 headers={"X-Company-Slug": cfg["company_slug"], "Accept": "application/json",
                                          "User-Agent": "website-build"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def ambil(cfg, cache: Path, warn):
    """Ambil pohon kategori + artikel lengkap (Panduan & Blog) dari API; fallback ke cache. Return dict atau None."""
    try:
        kategori = _get(cfg, "/article-categories")["data"]
        daftar, page = [], 1
        while True:
            d = _get(cfg, f"/articles?limit=100&page={page}")
            daftar += d["data"]
            if page >= d.get("meta", {}).get("pagination", {}).get("total_pages", 1):
                break
            page += 1
        cari = lambda slug: next((k for k in kategori if k["slug"] == slug), None)
        induk = cari(cfg.get("kategori_panduan", "docs"))
        anak = sorted(induk["children"], key=lambda k: k["sort_order"]) if induk else []
        blog = cari(cfg.get("kategori_blog", "blog"))
        blog_kat = ([{k: v for k, v in blog.items() if k != "children"}]
                    + sorted(blog.get("children", []), key=lambda k: k["sort_order"])) if blog else []
        boleh = {k["slug"] for k in anak} | {k["slug"] for k in blog_kat}
        artikel = [_get(cfg, f"/articles/{a['slug']}")["data"] for a in daftar if a["category"]["slug"] in boleh]
        data = {"kategori": anak, "blog_kategori": blog_kat, "artikel": artikel}
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return data
    except Exception as e:  # jaringan/API bermasalah → pakai cache
        if cache.exists():
            warn(f"API Lakukan tidak bisa diambil ({e}) → memakai cache {cache.name}")
            return json.loads(cache.read_text(encoding="utf-8"))
        warn(f"API Lakukan tidak bisa diambil ({e}) dan belum ada cache → Panduan & Blog dilewati")
        return None


def bersihkan(isi):
    """Isi artikel dari CMS: buang script/iframe/style & atribut event, gambar lazy."""
    isi = re.sub(r"<(script|style|iframe|object|embed)\b.*?</\1>", "", isi, flags=re.S | re.I)
    isi = re.sub(r"<(script|iframe|object|embed)\b[^>]*/?>", "", isi, flags=re.I)
    isi = re.sub(r'\s+on\w+\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', "", isi, flags=re.I)
    isi = re.sub(r'(href|src)\s*=\s*"\s*javascript:[^"]*"', r'\1="#"', isi, flags=re.I)
    isi = re.sub(r"<img(?![^>]*\bloading=)", '<img loading="lazy" decoding="async"', isi)
    return isi


def slug_kat(k, cfg):
    """timebase-memulai → memulai (awalan company slug dibuang supaya URL ringkas)."""
    pre = cfg["company_slug"] + "-"
    return k["slug"][len(pre):] if k["slug"].startswith(pre) else k["slug"]


def tanggal(iso):
    bln = "Januari Februari Maret April Mei Juni Juli Agustus September Oktober November Desember".split()
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {bln[int(m) - 1]} {y}"


IKON_KAT = {  # ikon garis per kategori (dicocokkan dari slug); default: buku
    "mulai": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "navigasi": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "akun": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "monitor": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "manajemen": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
    "referensi": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5"/><path d="M9 8h6"/>',
}


def ikon_kat(k, cfg):
    s = slug_kat(k, cfg)
    path = next((v for key, v in IKON_KAT.items() if key in s), IKON_KAT["referensi"])
    return ('<span class="ikon-bulat" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg></span>')


def diperbarui(a):
    """Baris info di atas artikel: hanya tanggal pembaruan terakhir, tanpa nama penulis (permintaan user)."""
    iso = a.get("updated_at") or a.get("published_at") or a["created_at"]
    return f'<p class="pd-meta">Terakhir diperbarui <time datetime="{iso[:10]}">{tanggal(iso)}</time></p>'


def kartu(a, url):
    cover = (f'<img class="pd-cover" src="{html.escape(a["cover_url"])}" alt="" loading="lazy" decoding="async">'
             if a.get("cover_url") else '<span class="pd-cover pd-cover-kosong" aria-hidden="true"></span>')
    return (f'<a class="pd-kartu" href="{url}">{cover}<span class="pd-isi">'
            f'<span class="pd-judul">{html.escape(a["title"])}</span>'
            f'<span class="pd-ringkas">{html.escape(a.get("excerpt") or "")}</span></span></a>')


def halaman(S, cfg, data):
    """Return list (page_dict, body) untuk /panduan, tiap kategori, dan tiap artikel."""
    brand = S["brand"]
    kats = [k for k in data["kategori"] if any(a["category"]["slug"] == k["slug"] for a in data["artikel"])]
    per_kat = {k["slug"]: [a for a in data["artikel"] if a["category"]["slug"] == k["slug"]] for k in kats}
    url_kat = {k["slug"]: f'/panduan/{slug_kat(k, cfg)}' for k in kats}
    url_art = {a["slug"]: f'{url_kat[a["category"]["slug"]]}/{a["slug"]}' for a in data["artikel"] if a["category"]["slug"] in url_kat}
    jumlah = sum(len(v) for v in per_kat.values())

    def chips(aktif=None):
        semua = f'<a href="/panduan"{CUR if aktif is None else ""}>Semua <span>{jumlah}</span></a>'
        return ('<nav class="pd-chips" aria-label="Kategori panduan">' + semua + "".join(
            f'<a href="{url_kat[k["slug"]]}"{CUR if aktif == k["slug"] else ""}>'
            f'{html.escape(k["name"])} <span>{len(per_kat[k["slug"]])}</span></a>' for k in kats) + "</nav>"
                # mobile: chip bisa digeser; geser chip aktif ke dalam layar
                + '<script>(function(n){var a=n&&n.querySelector("[aria-current]");if(a)n.scrollLeft=a.offsetLeft-20})(document.currentScript.previousElementSibling)</script>')

    def grid(arts):
        return '<div class="pd-grid">' + "".join(kartu(a, url_art[a["slug"]]) for a in arts) + "</div>"

    out = []
    # hub: satu kartu per kategori berisi daftar judul artikelnya (padat, tanpa ruang kosong walau kategori hanya 1 artikel)
    def kartu_kat(k):
        items = "".join(f'<li><a href="{url_art[a["slug"]]}">{html.escape(a["title"])}</a></li>' for a in per_kat[k["slug"]])
        n = len(per_kat[k["slug"]])
        return (f'<section class="pd-katkartu" id="{slug_kat(k, cfg)}">{ikon_kat(k, cfg)}'
                f'<h2><a href="{url_kat[k["slug"]]}">{html.escape(k["name"])}</a></h2>'
                f'<p>{html.escape(k.get("description") or "")}</p><ul>{items}</ul>'
                f'<a class="pd-lihat" href="{url_kat[k["slug"]]}">{n} panduan <span aria-hidden="true">→</span></a></section>')
    blok = '<div class="pd-katgrid">' + "".join(kartu_kat(k) for k in kats) + "</div>"
    out.append(({"slug": "/panduan", "name": "Panduan", "title": f"Panduan {brand}: Cara Memakai {brand}",
                 "meta": f"Panduan memakai {brand} per kategori: memulai, navigasi & akun, monitoring, manajemen, dan referensi istilah.",
                 "h1": f"Panduan {brand}", "eyebrow": "Pusat bantuan",
                 "lead": f"Langkah demi langkah memakai {brand}, dikelompokkan per kategori.",
                 "sederhana": True, "mentah": True, "crumbs": [("Panduan", "/panduan")]},
                f'<section class="band pd-band"><div class="wrap">{chips()}{blok}</div></section>'))
    # halaman per kategori
    for k in kats:
        out.append(({"slug": url_kat[k["slug"]], "name": k["name"], "title": f'{k["name"]} — Panduan {brand}',
                     "meta": k.get("description") or f'Panduan {brand} kategori {k["name"]}.',
                     "h1": k["name"], "eyebrow": "Panduan",
                     "lead": html.escape(k.get("description") or ""),
                     "sederhana": True, "mentah": True,
                     "crumbs": [("Panduan", "/panduan"), (k["name"], url_kat[k["slug"]])]},
                    f'<section class="band pd-band"><div class="wrap">{chips(k["slug"])}{grid(per_kat[k["slug"]])}</div></section>'))

    # halaman artikel: navigasi kiri per kategori (pola halaman legal)
    def nav(aktif_kat, aktif_art):
        grup = []
        for k in kats:
            cur = k["slug"] == aktif_kat
            items = "".join(f'<li><a href="{url_art[a["slug"]]}"{CUR if a["slug"] == aktif_art else ""}>'
                            f'{html.escape(a["title"])}</a></li>' for a in per_kat[k["slug"]])
            grup.append(f'<details class="dok-grup{" aktif" if cur else ""}"{" open" if cur else ""}>'
                        f'<summary>{html.escape(k["name"])}</summary><ol>{items}</ol></details>')
        isi = "".join(grup)
        return (f'<aside class="dok-nav" aria-label="Daftar panduan">{isi}</aside>'
                f'<details class="dok-toc-hp"><summary>Daftar panduan</summary>{isi}</details>')

    for k in kats:
        arts = per_kat[k["slug"]]
        for i, a in enumerate(arts):
            prev_ = arts[i - 1] if i > 0 else None
            next_ = arts[i + 1] if i + 1 < len(arts) else None
            pn = "".join(
                f'<a class="pd-pn {cls}" href="{url_art[x["slug"]]}"><span>{lab}</span>{html.escape(x["title"])}</a>'
                for x, cls, lab in ((prev_, "prev", "← Sebelumnya"), (next_, "next", "Berikutnya →")) if x)
            pn_nav = f'<nav class="pd-pn-wrap" aria-label="Panduan lain">{pn}</nav>' if pn else ""
            meta = diperbarui(a)
            cover = (f'<img class="pd-hero-img" src="{html.escape(a["cover_url"])}" alt="" decoding="async" fetchpriority="high">'
                     if a.get("cover_url") else "")
            body = (f'<section class="band dok-band"><div class="wrap"><div class="dok-grid">{nav(k["slug"], a["slug"])}'
                    f'<div class="dokumen pd-artikel">{meta}{cover}{bersihkan(a["content"])}'
                    f'{pn_nav}</div></div></div></section>')
            out.append(({"slug": url_art[a["slug"]], "name": a["title"], "title": f'{a["title"]} — Panduan {brand}',
                         "meta": a.get("excerpt") or a["title"], "h1": a["title"], "eyebrow": k["name"],
                         "lead": html.escape(a.get("excerpt") or ""), "sederhana": True, "mentah": True,
                         "crumbs": [("Panduan", "/panduan"), (k["name"], url_kat[k["slug"]]), (a["title"], url_art[a["slug"]])],
                         "artikel": {"published": a["published_at"], "updated": a.get("updated_at") or a["published_at"],
                                     "author": a.get("author") or brand, "image": a.get("cover_url")}},
                        body))
    footer = [(k["name"], url_kat[k["slug"]]) for k in kats]
    return out, footer


# ---------- Blog ----------

PER_HALAMAN = 12


def draf(a):
    """Artikel yang tampak seperti uji coba/draf (tanpa ringkasan dan isi < 60 kata) tidak diterbitkan."""
    kata = len(re.sub(r"<[^>]+>", " ", a.get("content") or "").split())
    return not (a.get("excerpt") or "").strip() and kata < 60


def blog(S, cfg, data, warn, cta_html=""):
    """Return list (page_dict, body, indexable) untuk /blog, /blog/halaman/N, /blog/kategori/<k>, /blog/<artikel>."""
    brand = S["brand"]
    bk = data.get("blog_kategori", [])
    slugs_blog = {k["slug"] for k in bk}
    semua = [a for a in data["artikel"] if a["category"]["slug"] in slugs_blog]
    for a in semua:
        if draf(a):
            warn(f'blog: artikel "{a["title"]}" ({a["slug"]}) tampak draf/uji coba (tanpa ringkasan, isi < 60 kata) → tidak diterbitkan')
    arts = sorted([a for a in semua if not draf(a)], key=lambda a: a.get("published_at") or "", reverse=True)
    sub = [k for k in bk[1:] if any(a["category"]["slug"] == k["slug"] for a in arts)]
    url_sub = {k["slug"]: f'/blog/kategori/{slug_kat(k, cfg)}' for k in sub}
    nama_kat = {k["slug"]: k["name"] for k in bk}
    url = lambda a: f'/blog/{a["slug"]}'
    lead = (cfg.get("blog_lead") or "Artikel dan wawasan terbaru dari {brand}.").replace("{brand}", brand)

    def chips(aktif=None):
        if not sub:
            return ""
        return ('<nav class="pd-chips" aria-label="Kategori blog">'
                f'<a href="/blog"{CUR if aktif is None else ""}>Semua <span>{len(arts)}</span></a>'
                + "".join(f'<a href="{url_sub[k["slug"]]}"{CUR if aktif == k["slug"] else ""}>{html.escape(k["name"])} '
                          f'<span>{sum(a["category"]["slug"] == k["slug"] for a in arts)}</span></a>' for k in sub) + "</nav>")

    def meta_baris(a):
        return f'{html.escape(nama_kat.get(a["category"]["slug"], "Blog"))} · {tanggal(a.get("published_at") or a["created_at"])}'

    def kartu_blog(a, utama=False):
        cover = (f'<img class="pd-cover" src="{html.escape(a["cover_url"])}" alt="" loading="{"eager" if utama else "lazy"}" decoding="async">'
                 if a.get("cover_url") else '<span class="pd-cover pd-cover-kosong" aria-hidden="true"></span>')
        return (f'<a class="pd-kartu{" bl-utama" if utama else ""}" href="{url(a)}">{cover}<span class="pd-isi">'
                f'<span class="bl-meta">{meta_baris(a)}</span>'
                f'<span class="pd-judul">{html.escape(a["title"])}</span>'
                f'<span class="pd-ringkas">{html.escape(a.get("excerpt") or "")}</span></span></a>')

    def daftar(list_, aktif, base):
        """Halaman daftar + paginasi (12 per halaman). Artikel terbaru tampil besar di halaman pertama."""
        hal = [list_[i:i + PER_HALAMAN] for i in range(0, len(list_), PER_HALAMAN)] or [[]]
        out = []
        for n, isi in enumerate(hal, 1):
            if isi:
                utama = kartu_blog(isi[0], True) if n == 1 else ""
                sisa = isi[1:] if n == 1 else isi
                grid = (utama + ('<div class="pd-grid">' + "".join(kartu_blog(a) for a in sisa) + "</div>" if sisa else ""))
            else:
                link_pd = (f' Sementara itu, baca <a href="/panduan">panduan memakai {brand}</a>.' if data.get("kategori") else "")
                grid = ('<div class="bl-kosong"><span class="ikon-bulat" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26" '
                        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                        '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></span>'
                        f'<h2>Artikel pertama segera terbit</h2><p>Kami sedang menyiapkan tulisan pertama.{link_pd}</p></div>')
            pag = ""
            if len(hal) > 1:
                link = lambda i: base if i == 1 else f"{base}/halaman/{i}"
                pag = ('<nav class="bl-pag" aria-label="Halaman">' + "".join(
                    f'<a href="{link(i)}"{CUR if i == n else ""}>{i}</a>' for i in range(1, len(hal) + 1)) + "</nav>")
            out.append((n, f'<section class="band pd-band"><div class="wrap">{chips(aktif)}{grid}{pag}</div></section>', bool(isi)))
        return out

    pages = []
    for n, body, ada in daftar(arts, None, "/blog"):
        slug = "/blog" if n == 1 else f"/blog/halaman/{n}"
        pages.append(({"slug": slug, "name": "Blog", "title": f"Blog {brand}" + (f" — Halaman {n}" if n > 1 else ""),
                       "meta": lead, "h1": f"Blog {brand}",
                       # badge = kalimat ajakan, bukan pengulangan H1 "Blog <Brand>" (keluhan user: "masih memiliki makna yang sama")
                       "eyebrow": cfg.get("blog_eyebrow") or "Pusat edukasi", "lead": html.escape(lead),
                       "sederhana": True, "mentah": True, "crumbs": [("Blog", "/blog")]}, body, ada))
    for k in sub:
        ka = [a for a in arts if a["category"]["slug"] == k["slug"]]
        for n, body, ada in daftar(ka, k["slug"], url_sub[k["slug"]]):
            slug = url_sub[k["slug"]] if n == 1 else f'{url_sub[k["slug"]]}/halaman/{n}'
            pages.append(({"slug": slug, "name": k["name"], "title": f'{k["name"]} — Blog {brand}',
                           "meta": k.get("description") or f'Artikel {brand} kategori {k["name"]}.',
                           "h1": k["name"], "eyebrow": "Blog", "lead": html.escape(k.get("description") or ""),
                           "sederhana": True, "mentah": True,
                           "crumbs": [("Blog", "/blog"), (k["name"], url_sub[k["slug"]])]}, body, ada))
    for a in arts:
        # kolom kanan: artikel terbaru lain (tepi kiri-kanan sejajar header; tanpa ruang kosong di samping artikel)
        lain = [x for x in arts if x is not a][:5]
        samping = ('<aside class="bl-samping"><p class="bl-samping-judul">Artikel terbaru</p><ol>'
                   + "".join(f'<li><a href="{url(x)}"><span>{html.escape(x["title"])}</span>'
                             f'<small>{tanggal(x.get("published_at") or x["created_at"])}</small></a></li>' for x in lain)
                   + '</ol><a class="bl-semua" href="/blog">Semua artikel <span aria-hidden="true">→</span></a></aside>') if lain else ""
        cover = (f'<img class="pd-hero-img" src="{html.escape(a["cover_url"])}" alt="" decoding="async" fetchpriority="high">'
                 if a.get("cover_url") else "")
        body = (f'<section class="band dok-band"><div class="wrap"><div class="bl-grid{" tunggal" if not samping else ""}"><div class="bl-artikel dokumen">'
                f'{diperbarui(a)}'
                f'{cover}{bersihkan(a["content"])}</div>{samping}</div></div></section>{cta_html}')
        kat = nama_kat.get(a["category"]["slug"], "Blog")
        crumbs = [("Blog", "/blog")] + ([(kat, url_sub[a["category"]["slug"]])] if a["category"]["slug"] in url_sub else []) + [(a["title"], url(a))]
        pages.append(({"slug": url(a), "name": a["title"], "title": f'{a["title"]} — Blog {brand}',
                       "meta": a.get("excerpt") or a["title"], "h1": a["title"], "eyebrow": kat,
                       "lead": html.escape(a.get("excerpt") or ""), "sederhana": True, "mentah": True, "crumbs": crumbs,
                       "artikel": {"tipe": "BlogPosting", "published": a.get("published_at") or a["created_at"],
                                   "updated": a.get("updated_at") or a["created_at"],
                                   "author": a.get("author") or brand, "image": a.get("cover_url")}}, body, True))
    return pages
