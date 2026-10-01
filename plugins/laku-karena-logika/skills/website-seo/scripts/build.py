#!/usr/bin/env python3
"""Rakit website statis dari data/brief.json + data/pricing.json + content/*.html,
lalu jalankan cek aturan SEO & klaim. Hanya pakai library standar Python.

Pemakaian:
    python3 build.py            # build ke dist/ + laporan cek
    python3 build.py --check    # cek saja, tanpa menulis dist/

Keluar dengan kode 1 kalau ada ERROR. WARNING tidak menghentikan build,
tapi wajib dilaporkan ke user.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import ilustrasi as ILUS

ROOT = Path(__file__).resolve().parent
SOCIAL = {"testimonials": [], "metrics": []}
SITE = {}
DIST = ROOT / "dist"

# Klaim yang tidak boleh muncul (BKB: penelusuran jam→tugas→aplikasi→layar adalah standar kategori)
BANNED_CLAIMS = [
    r"satu-satunya", r"satu satunya", r"termurah", r"paling murah",
    r"pertama di (indonesia|dunia|pasar|kelasnya)", r"(aplikasi|software|platform|alat) pertama",
    r"nomor satu", r"#1\b",
]

errors, warnings = [], []
GAMBAR = {}          # id -> entri data/ilustrasi.json
HERO = {}            # slug -> id gambar hero
MAX_KB = 200         # batas ukuran gambar asli (WebP/AVIF) per file


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def rupiah(n):
    return "Rp " + f"{int(round(n)):,}".replace(",", ".")


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def word_count(s):
    return len(re.findall(r"\w+", strip_tags(s)))


def content_file(slug):
    return ROOT / "content" / ("index.html" if slug == "/" else slug.strip("/") + ".html")


def out_file(slug):
    return DIST / ("index.html" if slug == "/" else slug.strip("/") + "/index.html")


# ---------- komponen dari data ----------

_SW = [0]   # penomoran switch periode: token harga dibuat sekali per build, jadi id unik di setiap halaman


def periode_switch(P):
    """Switch Bulanan/Tahunan tanpa JS: dua radio + label; konten .bln/.thn diatur CSS (sibling selector)."""
    _SW[0] += 1
    n = f"periode{_SW[0]}"
    hemat = 12 - P["annual_months_paid"]
    return (f'<input type="radio" class="p-bln" name="{n}" id="{n}-bln" checked>'
            f'<input type="radio" class="p-thn" name="{n}" id="{n}-thn">'
            f'<div class="periode-switch" role="group" aria-label="Periode tagihan">'
            f'<label for="{n}-bln">Bulanan</label><label for="{n}-thn">Tahunan <span>Hemat {hemat} bulan</span></label></div>')


def pricing_table(S, P):
    s = P["schemes"]
    FEAT = ' class="featured"'
    head = "".join(f'<th scope="col"{FEAT if x.get("featured") else ""}>{x["name"]}</th>' for x in s)
    m = P["annual_months_paid"]
    rows = []
    rows.append(f'<tr class="group bln"><th scope="rowgroup" colspan="{len(s)+1}"><span>Harga bulanan / karyawan</span></th></tr>')
    for i, lab in enumerate(P["tier_labels"]):
        cells = "".join(f'<td>{rupiah(x["monthly"][i])}<small>per bulan</small></td>' for x in s)
        rows.append(f'<tr class="bln"><th scope="row">{lab}</th>{cells}</tr>')
    rows.append(f'<tr class="group thn"><th scope="rowgroup" colspan="{len(s)+1}"><span>Harga tahunan / karyawan — {P["annual_rule"].lower()}</span></th></tr>')
    for i, lab in enumerate(P["tier_labels"]):
        cells = "".join(
            f'<td>{rupiah(x["monthly"][i]*m)}<small>setara {rupiah(x["monthly"][i]*m/12)}/bln</small></td>' for x in s)
        rows.append(f'<tr class="thn"><th scope="row">{lab}</th>{cells}</tr>')
    rows.append(f'<tr class="group"><th scope="rowgroup" colspan="{len(s)+1}"><span>Fitur</span></th></tr>')
    for f in P["features"]:
        cells = "".join(f"<td>{html.escape(c)}</td>" for c in f[1:])
        rows.append(f"<tr><th scope=\"row\">{html.escape(f[0])}</th>{cells}</tr>")
    def beli(x):
        btn = "btn-primary" if x.get("featured") else "btn-ghost"
        lab = S["copy"]["plan_button"].replace("{nama}", x["name"])
        return (f'<td><a class="btn {btn} btn-sm bln" href="{checkout_link(S, x["id"])}" rel="nofollow">{lab}</a>'
                f'<a class="btn {btn} btn-sm thn" href="{checkout_link(S, x["id"], "tahunan")}" rel="nofollow">{lab}</a></td>')
    foot = f'<tfoot><tr><th scope="row"></th>{"".join(beli(x) for x in s)}</tr></tfoot>'
    buy_head = f'<tr class="buy"><td></td>{"".join(beli(x) for x in s)}</tr>'
    return (f'<div class="periode" id="pilih-skema">{periode_switch(P)}<p class="table-hint">Geser ke kanan untuk melihat semua paket →</p><div class="table-wrap"><table class="pricing"><thead><tr><th scope="col">Jumlah karyawan</th>{head}</tr>{buy_head}</thead>'
            f'<tbody>{"".join(rows)}</tbody>{foot}</table></div><p class="note">{P["note"]}</p></div>')


def pricing_cards(S, P):
    m = P["annual_months_paid"]
    cards = []
    for x in P["schemes"]:
        lo, hi = min(x["monthly"]), max(x["monthly"])
        feat = ' featured' if x.get("featured") else ''
        badge = '<span class="badge">Disarankan</span>' if x.get("featured") else ''
        btn = "btn-primary" if x.get("featured") else "btn-ghost"
        label = S["copy"]["plan_button"].replace("{nama}", x["name"])
        cards.append(
            f'<div class="card plan{feat}">{badge}<h3>{x["name"]}</h3>'
            f'<div class="bln"><p class="price">{rupiah(hi)}<span>/karyawan/bln</span></p>'
            f'<p class="price-sub">turun sampai {rupiah(lo)} untuk 100+ karyawan</p></div>'
            f'<div class="thn"><p class="price">{rupiah(hi*m/12)}<span>/karyawan/bln, dibayar tahunan</span></p>'
            f'<p class="price-sub">{rupiah(hi*m)}/karyawan/tahun · {P["annual_rule"].lower()}</p></div>'
            f'<p>{html.escape(x["for"])}</p>'
            f'<a class="btn {btn} btn-block bln" href="{checkout_link(S, x["id"])}" rel="nofollow">{label}</a>'
            f'<a class="btn {btn} btn-block thn" href="{checkout_link(S, x["id"], "tahunan")}" rel="nofollow">{label} · Tahunan</a></div>')
    return (f'<div class="periode" id="pilih-skema">{periode_switch(P)}<div class="plans">{"".join(cards)}</div>'
            f'<p class="note">Detail lengkap di <a href="/harga">halaman harga</a>.</p></div>')


def addon_table(P):
    rows = "".join(
        f'<tr><th scope="row">{a["name"]}</th><td>+{rupiah(a["monthly"])}/{a["unit"]}<small>tahunan: +{rupiah(a["monthly"]*P["annual_months_paid"])}/karyawan</small></td><td>{html.escape(a["desc"])}</td></tr>'
        for a in P["addons"])
    return (f'<div class="table-wrap"><table class="pricing addon"><thead><tr><th scope="col">Add-on</th><th scope="col">Harga</th>'
            f'<th scope="col">Fitur yang didapat</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="note">Add-on dipasang ke {P["addons"][0]["applies_to"]} — tidak dijual terpisah.</p>')


def addon_total_table(P):
    a = P["addons"][0]
    head = "".join(f'<th scope="col">{x["name"]} + {a["name"]}</th>' for x in P["schemes"])
    rows = "".join(
        f'<tr><th scope="row">{lab}</th>' + "".join(f'<td>{rupiah(x["monthly"][i] + a["monthly"])}</td>' for x in P["schemes"]) + "</tr>"
        for i, lab in enumerate(P["tier_labels"]))
    return (f'<div class="table-wrap"><table class="pricing"><thead><tr><th scope="col">Bulanan / karyawan</th>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def cta(S, P):
    """CTA penutup = satu-satunya tempat urgensi + jaminan (tidak diulang di section lain).
    Kiri: judul, ajakan, tombol. Kanan: alasan mulai sekarang (copy.cta_points) + jaminan (pricing terms + risk_extra)."""
    C = S["copy"]
    points = "".join(f"<li>{t}</li>" for t in C.get("cta_points", []))            # boleh berisi link
    terms = "".join(f"<li>{html.escape(t)}</li>" for t in P.get("terms", []) + C.get("risk_extra", []))
    side = (f'<div class="cta-side">'
            + (f'<p class="cta-label">{C.get("cta_points_label", "Kenapa mulai sekarang")}</p><ul class="terms">{points}</ul>' if points else "")
            + f'<p class="cta-label">{C["risk_label"]}</p><ul class="terms">{terms}</ul></div>')
    return (f'<aside class="cta" id="kontak"><div class="cta-main"><h2>{C["cta_title"]}</h2><p>{C["cta_text"]}</p>'
            f'<a class="btn btn-primary" href="{checkout_link(S)}" rel="nofollow">{C["cta_primary"]}</a>'
            f'<a class="btn btn-ghost" href="{C["cta_secondary_href"]}">{C["cta_secondary"]}</a></div>{side}</aside>')


def risk_reversal(S, P):
    items = "".join(f"<li>{html.escape(t)}</li>" for t in P.get("terms", []) + S["copy"].get("risk_extra", []))
    return f'<div class="callout guarantee"><p class="label">{S["copy"]["risk_label"]}</p><ul class="checks">{items}</ul></div>'


def hero_stats(S):
    """Baris 3 statistik di hero — dari data/social-proof.json metrics (fakta atau data contoh yang memblokir publish)."""
    m = SOCIAL.get("metrics", [])[:3]
    if not m:
        return ""
    return '<ul class="hero-stats">' + "".join(
        f'<li><strong>{html.escape(x["value"])}</strong><span>{html.escape(x["label"])}</span></li>' for x in m) + "</ul>"


def social_proof(S, SP):
    """Strip logo/industri klien (angka statistik sudah tampil di hero)."""
    l = "".join(f'<li>{html.escape(x["name"])}</li>' for x in SP["logos"])
    return (f'<section class="proof" aria-label="Bukti sosial">'
            f'<p class="proof-cap">{S["copy"]["proof_caption"]}</p><ul class="logos">{l}</ul></section>')


def initials(name):
    parts = [w for w in re.split(r"[\s.]+", name) if w]
    return "".join(w[0] for w in parts[:2]).upper()


def testimonials(SP):
    """Kartu testimoni dengan foto pemberi testimoni. Foto harus orang asli dengan izin;
    sebelum ada, tampil avatar inisial (bukan foto stok/wajah AI)."""
    out = []
    for t in SP["testimonials"]:
        stars = "★" * t["rating"] + "☆" * (5 - t["rating"])
        if t.get("foto"):
            avatar = (f'<img class="avatar" src="/{t["foto"]}" width="48" height="48" loading="lazy" decoding="async" '
                      f'alt="Foto {html.escape(t["name"])}">')
        else:
            avatar = f'<span class="avatar" aria-hidden="true">{html.escape(initials(t["name"]))}</span>'
        out.append(f'<figure class="card quote"><div class="stars" aria-label="Rating {t["rating"]} dari 5">{stars}</div>'
                   f'<blockquote><p>{html.escape(t["quote"])}</p></blockquote>'
                   f'<figcaption>{avatar}<span class="who"><strong>{html.escape(t["name"])}</strong>'
                   f'<span>{html.escape(t["role"])}, {html.escape(t["company"])}</span></span></figcaption></figure>')
    return f'<div class="quotes">{"".join(out)}</div>'


def checkout_link(S, skema=None, periode="bulanan"):
    """Tombol beli. site.json checkout_url boleh memuat {paket} (alias {skema}) dan {periode}."""
    url = S.get("checkout_url", "")
    if not url:
        return "/harga#pilih-skema"
    pid = str(skema or "")
    return url.replace("{paket}", pid).replace("{skema}", pid).replace("{periode}", periode)


WA_ICON = ('<svg class="wa-icon" width="44" height="44" viewBox="0 0 32 32" aria-hidden="true">'
           '<circle cx="16" cy="16" r="16" fill="#25D366"/>'
           '<path d="M16 6.6a9.4 9.4 0 0 0-8.1 14.2L6.6 25.4l4.7-1.3A9.4 9.4 0 1 0 16 6.6z" fill="none" stroke="#fff" stroke-width="2"/>'
           '<path d="M12.7 10.9c.3-.1.6 0 .8.3l1 1.9c.1.3.1.6-.1.8l-.7.8c.6 1.3 1.7 2.4 3 3l.8-.7c.2-.2.5-.3.8-.1l1.9 1'
           'c.3.2.4.5.3.8-.3 1.1-1.3 1.8-2.4 1.6-3.3-.6-5.9-3.2-6.5-6.5-.2-1.1.5-2.1 1.6-2.4z" fill="#fff"/></svg>')


def float_bar(S):
    """Tombol WA marketing melayang di semua halaman. Mobile: versi ringkas (ikon + judul), tanpa tombol lain."""
    C = S["copy"]
    return (f'<div class="float-bar">'
            f'<a class="wa-float" href="{wa_link(S)}" target="_blank" rel="nofollow noopener" aria-label="{C["wa_title"]} — WhatsApp">'
            f'{WA_ICON}<span><strong>{C["wa_title"]}</strong><small>{C["wa_subtitle"]}</small></span></a></div>')


def wa_link(S, text=None):
    if S.get("whatsapp"):
        return f'https://wa.me/{S["whatsapp"]}?text={quote(text or S["whatsapp_text"])}'
    return "#kontak"


# ---------- White Label (wajib di setiap produk; kunci config tetap 'whitelabel') ----------

def fill_brand(S, txt):
    return txt.replace("{{brand}}", S["brand"]).replace("{{deskripsi}}", S["description"])


def daftar_solusi(S):
    items = [x for it in S["nav"] if isinstance(it, dict) for x in it["items"]]
    li = "".join(f'<li><a href="{x[0]}"><strong>{x[1]}</strong></a>' + (f" — {html.escape(x[2])}" if len(x) > 2 else "") + "</li>"
                 for x in items)
    return f'<ul class="checks">{li}</ul>'


def ul_checks(items):
    return '<ul class="checks">' + "".join(f"<li>{html.escape(t)}</li>" for t in items) + "</ul>"


def cta_whitelabel(S):
    W = S["whitelabel"]
    return (f'<aside class="cta" id="kontak"><h2>{fill_brand(S, W["cta_title"])}</h2><p>{fill_brand(S, W["cta_text"])}</p>'
            f'<a class="btn btn-primary" href="{wa_link(S, fill_brand(S, W["wa_text"]))}" target="_blank" rel="nofollow noopener">{W["cta_button"]}</a>'
            f'<a class="btn btn-ghost" href="/harga">Lihat harga versi langganan</a></aside>')


def logo(S):
    """Logo inline dari static/logo.svg (wajib punya width & height agar tidak CLS)."""
    svg = (ROOT / S.get("logo", "static/logo.svg")).read_text(encoding="utf-8").strip()
    return re.sub(r'\s*xmlns="[^"]+"', "", svg, count=1)


# ---------- gambar & ilustrasi ----------

def img_src(g):
    return "/" + (g.get("file") or f'static/ilustrasi/{g["id"]}.svg')


def figure(g, hero=False):
    w, h = g.get("w", ILUS.W), g.get("h", ILUS.H)
    load = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    cap = f'<figcaption>{html.escape(g["caption"])}</figcaption>' if g.get("caption") else ""
    return (f'<figure class="ilus{" hero-img" if hero else ""}"><img src="{img_src(g)}" width="{w}" height="{h}" '
            f'alt="{html.escape(g["alt"])}" {load} decoding="async">{cap}</figure>')


def gambar_token(m):
    gid = m.group(1)
    if gid not in GAMBAR:
        return f"{{{{gambar:{gid}}}}}"   # dibiarkan -> tertangkap cek token tak dikenal
    return figure(GAMBAR[gid])


# ---------- layout ----------

def _min_css(c):
    c = re.sub(r"/\*.*?\*/", "", c, flags=re.S)
    c = re.sub(r"\s+", " ", c)
    return re.sub(r"\s*([{}:;,>])\s*", r"\1", c).replace(";}", "}").strip()


CSS = _min_css((ROOT / "static" / "style.css").read_text(encoding="utf-8"))

def jsonld(S, page, body, P, indexable):
    base = S["site_url"]
    url = (base + page["slug"]) if base else page["slug"]
    graph = [{
        "@type": "Organization", "@id": f"{base}/#org", "name": S["brand"], "slogan": S["tagline"],
        **({"url": base + "/"} if base else {}),
    }, {
        "@type": "WebPage", "name": page["title"], "description": page["meta"], "inLanguage": "id-ID",
        **({"url": url} if base else {}), "publisher": {"@id": f"{base}/#org"},
    }]
    if page["slug"] != "/":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": S["brand"], **({"item": base + "/"} if base else {})},
            {"@type": "ListItem", "position": 2, "name": page["name"], **({"item": url} if base else {})}]})
    if page.get("product_schema"):
        offers = [{"@type": "Offer", "name": f'{S["brand"]} {x["name"]}', "priceCurrency": "IDR",
                   "price": str(max(x["monthly"])),
                   "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(max(x["monthly"])),
                                          "priceCurrency": "IDR", "unitText": "karyawan per bulan"}} for x in P["schemes"]]
        app = {"@type": "SoftwareApplication", "name": S["brand"], "applicationCategory": "BusinessApplication",
               "description": page["meta"], "offers": offers}
        real = [t for t in SOCIAL["testimonials"] if not t.get("contoh") and t.get("rating")]
        if real:  # rating bintang HANYA dari ulasan asli yang tampil di halaman
            app["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": f'{sum(t["rating"] for t in real)/len(real):.1f}',
                                      "reviewCount": str(len(real)), "bestRating": "5"}
            app["review"] = [{"@type": "Review", "author": {"@type": "Person", "name": t["name"]},
                              "reviewRating": {"@type": "Rating", "ratingValue": str(t["rating"]), "bestRating": "5"},
                              "reviewBody": t["quote"]} for t in real]
        graph.append(app)
    faqs = re.findall(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', body, flags=re.S)
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q).strip(),
             "acceptedAnswer": {"@type": "Answer", "text": " ".join(strip_tags(a).split())}} for q, a in faqs]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def nav_item(it, current, CUR):
    """[slug, label] = link biasa; {label, items} = menu group (dropdown <details>, tanpa JS)."""
    if isinstance(it, dict):
        active = any(x[0] == current for x in it["items"])
        subs = "".join(
            f'<li><a href="{x[0]}"{CUR if x[0] == current else ""}><strong>{x[1]}</strong>'
            + (f'<span>{html.escape(x[2])}</span>' if len(x) > 2 else "") + "</a></li>"
            for x in it["items"])
        return (f'<details class="nav-group{" active" if active else ""}"><summary>{it["label"]}</summary>'
                f'<ul class="submenu">{subs}</ul></details>')
    slug, label = it[0], it[1]
    return f'<a href="{slug}"{CUR if slug == current else ""}>{label}</a>'


# ---------- tata letak section (band dua kolom + teks dilipat) ----------

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# blok visual: selalu terlihat dan dibuat selebar kontainer
WIDE = ("grid", "table-wrap", "periode", "plans", "quotes", "proof", "cta", "guarantee")
# blok yang tetap terlihat di kolom teks
KEEP = ("callout", "agitate", "checks", "faq", "note")


def top_blocks(src):
    """Pecah HTML jadi elemen tingkat-atas (tanpa parser eksternal)."""
    blocks, depth, start = [], 0, None
    for m in re.finditer(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*?(/?)>", src, flags=re.S):
        if m.group(0).startswith("<!--"):
            continue
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or selfclose:
            if depth == 0:
                blocks.append(m.group(0))
            continue
        if not closing:
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(src[start:m.end()])
    return blocks


def kind(b):
    m = re.match(r'<([a-z0-9]+)(?:[^>]*class="([^"]*)")?', b)
    return (m.group(1), (m.group(2) or "").split()) if m else ("", [])


def words(b):
    return len(re.findall(r"\w+", strip_tags(b)))


def render_section(blocks, idx, S=None):
    """Satu H2 + isinya → band, mengikuti standar UI section (acuan disetujui user):
    - ada gambar      → teks | gambar (posisi gambar bergantian)
    - ada poin/daftar → teks | panel kartu berisi poin (panel = pengganti kartu gambar)
    - FAQ             → judul + kartu bantuan WA | daftar pertanyaan
    - hanya blok lebar → judul + pembuka di atas, kartu/tabel selebar kontainer di bawah
    Semua teks terlihat (tanpa lipatan)."""
    h2, rest = blocks[0], blocks[1:]
    fig, wide, paras, scan = None, [], [], []
    for b in rest:
        tag, cls = kind(b)
        if tag == "figure" and fig is None:
            fig = b
        elif tag == "aside" or any(c in WIDE for c in cls):
            wide.append(b)
        elif tag == "p" and "label" not in cls:
            paras.append(b)
        else:
            scan.append(b)
    band = "band" if idx % 2 else "band alt"   # section pertama setelah band intro (putih) berlatar abu → batas terlihat
    # keseimbangan kolom: teks pendek di samping gambar → kartu langkah/fitur pertama ikut ke kolom teks
    if fig and not scan:
        for i, b in enumerate(wide):
            if "grid" in kind(b)[1]:
                scan.append(wide.pop(i)); break
    # daftar panjang di panel → dua kolom supaya panel tidak terlalu tinggi
    scan = [re.sub(r'^<(ul|ol)( class="checks")?', lambda m: f'<{m.group(1)} class="{"checks " if m.group(2) else ""}two-col"', b, count=1)
            if kind(b)[0] in ("ul", "ol") and b.count("<li") > 4 and not fig else b for b in scan]
    faq = any("faq" in kind(b)[1] for b in scan)
    if faq and not paras and S and S.get("copy", {}).get("faq_lead"):
        paras = [f'<p>{S["copy"]["faq_lead"]}</p>']
    lead = h2 + "".join(paras)
    if fig:
        flip = " flip" if idx % 2 else ""
        row = (f'<div class="split media{flip}"><div class="col-text">{lead}{"".join(scan)}</div>'
               f'<div class="col-media">{fig}</div></div>')
    elif faq:
        help_card = ""
        if S and S.get("copy", {}).get("faq_help_title"):
            C = S["copy"]
            help_card = (f'<div class="help-card"><p class="help-title">{C["faq_help_title"]}</p><p>{C["faq_help_text"]}</p>'
                         f'<a class="btn btn-ghost btn-sm" href="{wa_link(S)}" target="_blank" rel="nofollow noopener">{C["faq_help_button"]}</a></div>')
        # FAQ dinamis: siap untuk 20+ pertanyaan — grup topik (<h3>) jadi chip navigasi, kolom kiri sticky,
        # dan accordion eksklusif (<details name>) supaya hanya satu jawaban terbuka. Tanpa JavaScript.
        faq_html = "".join(scan)
        n = faq_html.count('<details class="faq"')
        faq_html = faq_html.replace('<details class="faq">', f'<details class="faq" name="faq-{idx}">')
        topics = []
        def _topic(m):
            label = strip_tags(m.group(1)).strip()
            tid = f"faq-{idx}-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
            topics.append((tid, label))
            return f'<h3 class="faq-group" id="{tid}">{m.group(1)}</h3>'
        faq_html = re.sub(r"<h3[^>]*>(.*?)</h3>", _topic, faq_html, flags=re.S)
        nav = ""
        if topics:
            nav = ('<nav class="faq-topics" aria-label="Topik pertanyaan">'
                   + "".join(f'<a href="#{t}">{html.escape(l)}</a>' for t, l in topics) + "</nav>")
        count = f'<p class="faq-count">{n} pertanyaan</p>' if n >= 6 else ""
        long_cls = " long" if n > 6 else ""
        row = (f'<div class="split faq-row{long_cls}"><div class="col-text">{count}{lead}{nav}{help_card}</div>'
               f'<div class="col-faq">{faq_html}</div></div>')
    elif scan:
        flip = " flip" if idx % 2 else ""
        row = f'<div class="split panel-row{flip}"><div class="col-text">{lead}</div><div class="col-panel"><div class="panel">{"".join(scan)}</div></div></div>'
    else:
        row = f'<div class="split stack"><div class="col-text">{lead}</div></div>'
    return f'<section class="{band}"><div class="wrap">{row}{"".join(wide)}</div></section>'


def layout_sections(body):
    blocks = top_blocks(body)
    intro, sections, cur, tail = [], [], None, []
    for b in blocks:
        tag, cls = kind(b)
        if tag == "aside" and "cta" in cls:
            tail.append(b)
        elif tag == "h2":
            cur = [b]; sections.append(cur)
        elif cur is None:
            intro.append(b)
        else:
            cur.append(b)
    out = []
    if intro:
        out.append(f'<section class="band intro"><div class="wrap">{"".join(intro)}</div></section>')
    out += [render_section(s, i, SITE) for i, s in enumerate(sections)]
    if tail:
        out.append(f'<section class="band end"><div class="wrap">{"".join(tail)}</div></section>')
    return "\n".join(out)


def render(S, page, body, P, all_pages, indexable):
    base = S["site_url"]
    canonical = f'<link rel="canonical" href="{base}{page["slug"]}">' if base else ""
    robots = '<meta name="robots" content="index,follow">' if indexable else '<meta name="robots" content="noindex,follow">'
    CUR = ' aria-current="page"'
    nav = "".join(nav_item(it, page["slug"], CUR) for it in S["nav"])
    # hero mengikuti layout referensi user: badge pill · H1 · subjudul · 1 CTA → · 3 statistik · gambar di atas bentuk gradasi
    eyebrow = page.get("eyebrow") or (S.get("eyebrow") if page["slug"] == "/" else page["name"])
    if page["slug"] == "/404":
        hero_cta = f'<a class="btn btn-primary btn-lg hero-cta" href="/">Kembali ke beranda <span aria-hidden="true">→</span></a>'
    elif page["slug"] == "/white-label" and S.get("whitelabel"):
        hero_cta = (f'<a class="btn btn-primary btn-lg hero-cta" href="{wa_link(S, fill_brand(S, S["whitelabel"]["wa_text"]))}" '
                    f'target="_blank" rel="nofollow noopener">{S["whitelabel"]["cta_button"]} <span aria-hidden="true">→</span></a>')
    else:
        hero_cta = f'<a class="btn btn-primary btn-lg hero-cta" href="{checkout_link(S)}" rel="nofollow">{S["copy"]["cta_primary"]} <span aria-hidden="true">→</span></a>'
    hero_class = "hero home" if page["slug"] == "/" else "hero"
    lead = page.get("lead", "")
    hero_img = figure(GAMBAR[HERO[page["slug"]]], hero=True) if HERO.get(page["slug"]) in GAMBAR else ""
    produk = [p for p in all_pages if p["slug"] in S["footer_produk"]]
    panduan = [p for p in all_pages if p not in produk and p["slug"] != "/"]
    flinks = lambda ps: "".join(f'<li><a href="{p["slug"]}">{p["name"]}</a></li>' for p in ps)
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page["title"])}</title>
<meta name="description" content="{html.escape(page["meta"])}">
{robots}
{canonical}
<meta property="og:type" content="website">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="{S["brand"]}">
<meta property="og:title" content="{html.escape(page["title"])}">
<meta property="og:description" content="{html.escape(page["meta"])}">
{f'<meta property="og:url" content="{base}{page["slug"]}">' if base else ''}
{f'<meta property="og:image" content="{base}/{S["og_image"]}"><meta name="twitter:card" content="summary_large_image">' if base and S.get("og_image") else ''}
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#7B2CFF">
<link rel="preload" href="/static/fonts/montserrat-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
<script type="application/ld+json">{jsonld(S, page, body, P, indexable)}</script>
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="{S["brand"]} — beranda">{logo(S)}</a>
<input type="checkbox" id="menu" class="menu-toggle" aria-label="Buka menu"><label for="menu" class="menu-btn" aria-hidden="true"><span></span></label>
<div class="nav-panel"><nav class="nav" aria-label="Utama">{nav}</nav>
<div class="nav-actions"><a class="btn btn-ghost btn-sm" href="{S.get("signin_url") or "#"}" rel="nofollow">{S["copy"]["signin"]}</a><a class="btn btn-primary btn-sm" href="{checkout_link(S)}" rel="nofollow">{S["copy"]["nav_cta"]}</a></div></div>
</div></header>
<main>
<section class="{hero_class}"><div class="wrap{' hero-grid' if hero_img else ''}"><div class="hero-text">
<p class="eyebrow"><span>{html.escape(eyebrow)}</span></p>
<h1{' class="long"' if len(page["h1"]) > 55 else ''}>{html.escape(page["h1"])}</h1>
{f'<p class="lead">{lead}</p>' if lead else ''}
{hero_cta}
{hero_stats(S) if page["slug"] != "/404" else ""}
</div>{hero_img}</div></section>
<article class="content prose">
{layout_sections(body)}
</article>
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-brand">{logo(S)}<p>{S["tagline"]}</p><p class="muted">{html.escape(S["description"])}</p></div>
<div><h2>Produk</h2><ul>{flinks(produk)}</ul></div>
<div><h2>Panduan</h2><ul>{flinks(panduan)}</ul></div>
</div><div class="wrap foot-bottom">© {S["brand"]}{(' · <a href="mailto:' + S["email"] + '">' + S["email"] + '</a>') if S.get("email") else ''}</div></footer>
{float_bar(S)}
</body>
</html>
"""


# ---------- cek aturan ----------

# standar minimum UI per section (disetujui user): H2 → 1–2 kalimat → minimal satu elemen visual/yang bisa dipindai
VISUAL_CLASSES = {"grid", "table-wrap", "periode", "plans", "quotes", "proof", "callout", "agitate", "checks", "faq", "cta"}


def check_sections(sid, body):
    blocks = top_blocks(body)
    sections, cur = [], None
    for b in blocks:
        tag, cls = kind(b)
        if tag == "h2":
            cur = [b]; sections.append(cur)
        elif cur is not None:
            cur.append(b)
    for sec in sections:
        title = strip_tags(sec[0]).strip()
        rest = sec[1:]
        visual = any(kind(b)[0] in ("figure", "ul", "ol", "table", "blockquote", "details", "aside")
                     or VISUAL_CLASSES & set(kind(b)[1]) for b in rest)
        if not visual:
            err(sid, f"section “{title[:50]}” hanya teks — tambah poin, kartu, tabel, callout, atau gambar (standar UI section)")
        is_faq = any("faq" in kind(b)[1] for b in rest)
        if not is_faq and (not rest or kind(rest[0])[0] != "p"):
            err(sid, f"section “{title[:50]}” tidak punya kalimat pembuka setelah judul (standar UI section)")
        paras = [b for b in rest if kind(b)[0] == "p" and not kind(b)[1]]
        if len(paras) > 2:
            warn(sid, f"section “{title[:50]}” punya {len(paras)} paragraf — padatkan jadi 1–2 kalimat + poin/kartu")
        # pesan dobel: kalimat di kolom teks mengulang isi panel/kartu dalam section yang sama
        def grams(t, n=4):
            w = re.findall(r"\w+", strip_tags(t).lower())
            return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
        lead_txt = "".join(b for b in rest if kind(b)[0] == "p")
        other_txt = "".join(b for b in rest if kind(b)[0] != "p")
        nums = lambda t: set(re.findall(r"\d+(?:[.,]\d+)?", strip_tags(t)))
        dup = grams(lead_txt) & grams(other_txt)
        if len(dup) >= 3 or len(nums(lead_txt) & nums(other_txt)) >= 2:
            warn(sid, f"section “{title[:50]}”: pembuka/catatan mengulang isi poin/kartu ({', '.join(sorted(dup)[:2]) or 'angka sama'}) — sampaikan sekali saja")
        if len(re.findall(r"\w+", title)) > 12:
            warn(sid, f"judul section “{title[:50]}…” terlalu panjang (>12 kata)")

def check_page(S, B, page, body, slugs):
    sid = page["slug"]
    t, m, h1, prim = page["title"], page["meta"], page["h1"], page["primary"].lower()
    if not 40 <= len(t) <= 60:
        err(sid, f"title {len(t)} karakter (harus 40–60): {t}")
    if not 120 <= len(m) <= 155:
        err(sid, f"meta description {len(m)} karakter (harus 120–155)")
    if t.strip().lower() == h1.strip().lower():
        err(sid, "H1 sama dengan title — harus berbeda")
    if prim not in t.lower():
        warn(sid, f"primary keyword '{page['primary']}' tidak ada di title (dari brief)")
    if prim not in h1.lower():
        warn(sid, f"primary keyword '{page['primary']}' tidak ada di H1 (dari brief)")
    first_p = re.search(r"<p[^>]*>(.*?)</p>", body, flags=re.S)
    if not first_p or prim not in strip_tags(first_p.group(1)).lower():
        err(sid, f"primary keyword '{page['primary']}' tidak ada di paragraf pertama")
    wc = word_count(body)
    if "min_words" in page:                      # halaman tambahan (beranda, harga, white label)
        if wc < page["min_words"]:
            err(sid, f"isi {wc} kata (minimal {page['min_words']})")
    elif wc < 700:                               # halaman brief: ditulis ringkas (poin/kartu), tapi tetap cukup dalam
        err(sid, f"isi {wc} kata (minimal 700)")
    elif wc < 1000:
        warn(sid, f"isi {wc} kata (target keyword plan 1.000–1.500; pertimbangkan tambah poin/kartu/FAQ)")
    elif wc > 1800:
        warn(sid, f"isi {wc} kata (target 1.000–1.500)")
    for para in re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", body, flags=re.S):
        n = len(re.findall(r"\w+", strip_tags(para)))
        if n > 45:
            warn(sid, f"paragraf {n} kata — pecah jadi poin/kartu (maks ±45 kata): “{strip_tags(para).strip()[:50]}…”")
    page["_words"] = wc
    for link in page.get("links", []):
        if f'href="{link}"' not in body:
            err(sid, f"link internal wajib ke {link} belum ada")
    for href in re.findall(r'href="(/[^"#?]*)', body):
        if href not in slugs and not href.startswith("/static/"):
            err(sid, f"link ke {href} — halaman tidak ada")
    text = (t + " " + m + " " + h1 + " " + strip_tags(body)).lower()
    for c in B["competitors"]:
        if re.search(rf"\b{re.escape(c.lower())}\b", text):
            err(sid, f"menyebut nama kompetitor '{c}'")
    for pat in BANNED_CLAIMS:
        hit = re.search(pat, text)
        if hit:
            err(sid, f"klaim terlarang '{hit.group(0)}'")
    for s in page.get("secondary", []):
        if s.lower() not in text:
            warn(sid, f"secondary keyword '{s}' belum muncul di halaman")
    if "{{" in body:
        err(sid, "masih ada token {{...}} yang tidak dikenal")
    check_sections(sid, body)


def check_images(p, used, IL):
    sid = p["slug"]
    for gid in used + ([HERO[sid]] if sid in HERO else []):
        if gid not in GAMBAR:
            err(sid, f"gambar '{gid}' tidak ada di data/ilustrasi.json")
            continue
        g = GAMBAR[gid]
        f = ROOT / img_src(g).lstrip("/")
        if not (g.get("alt") or "").strip():
            err(sid, f"gambar '{gid}' tanpa alt")
        elif len(g["alt"]) > 125:
            warn(sid, f"alt gambar '{gid}' {len(g['alt'])} karakter (sebaiknya ≤125)")
        if not f.exists():
            err(sid, f"file gambar {f.relative_to(ROOT)} tidak ada")
            continue
        if not g.get("auto", True):
            if f.suffix.lower() not in (".webp", ".avif", ".svg"):
                err(sid, f"gambar '{gid}' harus WebP/AVIF (atau SVG), bukan {f.suffix}")
            if not (g.get("w") and g.get("h")):
                err(sid, f"gambar '{gid}' wajib punya w & h (ukuran asli) agar tidak CLS")
        kb = f.stat().st_size / 1024
        if kb > MAX_KB:
            err(sid, f"gambar '{gid}' {kb:.0f} KB (maks {MAX_KB} KB) — kompres dulu")
    n = len(set(used + ([HERO[sid]] if sid in HERO else [])))
    if n < IL.get("min_per_halaman", 3):
        err(sid, f"hanya {n} gambar (minimal {IL.get('min_per_halaman', 3)} per halaman)")
    if sid not in HERO:
        warn(sid, "belum ada gambar hero")


def daftar_ilustrasi_md(S, pages, IL):
    rows = ["# Daftar Ilustrasi — " + S["brand"], "",
            "Dibuat otomatis oleh `build.py` dari `data/ilustrasi.json`. Kirim gambar pengganti sesuai **brief**; "
            "kami simpan sebagai WebP/AVIF, lalu `auto` diubah jadi `false`.", "",
            "| Halaman | Section | ID | Status | Ukuran tampil | Brief gambar pengganti |", "|---|---|---|---|---|---|"]
    order = {p["slug"]: i for i, p in enumerate(pages)}
    for g in sorted(IL["gambar"], key=lambda g: (order.get(g["halaman"], 99), g["section"] != "Hero")):
        status = "placeholder SVG" if g.get("auto", True) else "gambar asli"
        rows.append(f'| `{g["halaman"]}` | {g["section"]} | `{g["id"]}` | {status} | {g.get("w", ILUS.W)}×{g.get("h", ILUS.H)} (16:10) | {g["brief"]} |')
    rows += ["", "## Foto testimoni", "",
             "Foto **asli** pemberi testimoni, dengan izin tertulis. Persegi ±160×160 px, wajah jelas, WebP ≤ 40 KB. "
             "Jangan foto stok/wajah AI. Sebelum ada: avatar inisial.", "",
             "| Nama | Jabatan & perusahaan | Status |", "|---|---|---|"]
    for t in SOCIAL.get("testimonials", []):
        st = "foto asli" if t.get("foto") else ("avatar inisial · testimoni CONTOH (ganti dengan pelanggan asli)" if t.get("contoh") else "avatar inisial · perlu foto")
        rows.append(f'| {t["name"]} | {t["role"]}, {t["company"]} | {st} |')
    return "\n".join(rows) + "\n"


def main():
    check_only = "--check" in sys.argv
    S, B, P = load("site.json"), load("data/brief.json"), load("data/pricing.json")
    SP = load("data/social-proof.json")
    IL = load("data/ilustrasi.json")
    GAMBAR.update({g["id"]: g for g in IL["gambar"]})
    HERO.update(IL.get("hero", {}))
    ILUS.generate(ROOT, IL, S.get("ilustrasi_warna"))
    global SOCIAL
    SOCIAL = SP
    SITE.update(S)
    pages = S["extra_pages"] + B["pages"]
    for p in S["extra_pages"]:
        for k in ("name", "title", "meta", "h1", "primary"):
            p[k] = fill_brand(S, p[k])
    for p in pages:
        p["product_schema"] = p["slug"] in S["product_pages"]
    slugs = {p["slug"] for p in pages}

    # aturan tetap: setiap produk bisa dibeli whitelabel -> halaman + menu utama wajib ada
    if "/white-label" not in slugs:
        err("/white-label", "halaman White Label wajib ada di site.json extra_pages (salin dari template skill)")
    if not any(isinstance(it, list) and it[0] == "/white-label" for it in S["nav"]):
        err("/white-label", "menu 'White Label' wajib ada di menu utama (site.json nav)")

    for key in ("title", "meta", "h1"):
        seen = {}
        for p in pages:
            v = p[key].strip().lower()
            if v in seen:
                err(p["slug"], f"{key} sama persis dengan {seen[v]}")
            seen[v] = p["slug"]

    tokens = {
        "{{pricing_table}}": pricing_table(S, P), "{{pricing_cards}}": pricing_cards(S, P),
        "{{addon_table}}": addon_table(P), "{{addon_total_table}}": addon_total_table(P),
        "{{cta}}": cta(S, P), "{{wa_link}}": wa_link(S), "{{checkout_link}}": checkout_link(S),
        "{{tanpa_risiko}}": risk_reversal(S, P), "{{bukti_sosial}}": social_proof(S, SP), "{{testimoni}}": testimonials(SP),
        "{{harga_mulai}}": rupiah(min(min(x["monthly"]) for x in P["schemes"])),
        "{{brand}}": S["brand"], "{{deskripsi}}": S["description"],
        "{{deskripsi_kecil}}": S["description"][:1].lower() + S["description"][1:].rstrip("."), "{{daftar_solusi}}": daftar_solusi(S),
    }
    if S.get("whitelabel"):
        tokens.update({"{{wl_kustomisasi}}": ul_checks(S["whitelabel"]["kustomisasi"]),
                       "{{wl_ditangani}}": ul_checks(S["whitelabel"]["ditangani"]),
                       "{{cta_whitelabel}}": cta_whitelabel(S),
                       "{{wa_whitelabel}}": wa_link(S, fill_brand(S, S["whitelabel"]["wa_text"]))})
    built = []
    for p in pages:
        f = content_file(p["slug"])
        if not f.exists():
            err(p["slug"], f"file konten {f.relative_to(ROOT)} belum ada")
            continue
        raw = f.read_text(encoding="utf-8")
        n_harga = raw.count("{{pricing_cards}}") + raw.count("{{pricing_table}}")
        if "{{tanpa_risiko}}" in raw and "{{cta}}" in raw:
            warn(p["slug"], "{{tanpa_risiko}} + {{cta}} di halaman yang sama → jaminan tampil dua kali; CTA penutup sudah memuat jaminan")
        harga_page = S.get("pricing_page", "/harga")
        harga_tokens = [t for t in ("{{pricing_cards}}", "{{pricing_table}}", "{{addon_table}}", "{{addon_total_table}}", "{{harga_mulai}}") if t in raw]
        if p["slug"] != harga_page and harga_tokens:
            err(p["slug"], f"harga hanya boleh tampil di {harga_page} (aturan user) — hapus {', '.join(harga_tokens)}, tautkan ke menu Harga")
        if p["slug"] != harga_page and re.search(r"\bRp\s?\d", strip_tags(raw)):
            warn(p["slug"], "ada angka rupiah di teks — harga hanya di halaman Harga (kecuali bukan harga produk)")
        if p["slug"] in S["product_pages"] and not n_harga:
            err(p["slug"], "ada di product_pages (schema Offer/harga) tapi halaman tidak menampilkan harga")
        if n_harga > 1:
            err(p["slug"], f"{n_harga} tampilan harga — cukup satu per halaman ({{{{pricing_table}}}} di /harga, {{{{pricing_cards}}}} di halaman lain)")
        lead = re.match(r"\s*<!--\s*lead:(.*?)-->", raw, flags=re.S)
        if lead:
            p["lead"] = lead.group(1).strip()
            raw = raw[lead.end():]
        for k, v in tokens.items():
            raw = raw.replace(k, v)
            if p.get("lead"):
                p["lead"] = p["lead"].replace(k, v)
        used = re.findall(r"\{\{gambar:([a-z0-9-]+)\}\}", raw)
        raw = re.sub(r"\{\{gambar:([a-z0-9-]+)\}\}", gambar_token, raw)
        p["_gambar"] = used + ([HERO[p["slug"]]] if p["slug"] in HERO else [])
        check_images(p, used, IL)
        check_page(S, B, p, raw, slugs)
        indexable = S.get("legal_reviewed", {}).get(p["slug"], True)
        if not indexable:
            warn(p["slug"], "belum direview ahli hukum → noindex & tidak masuk sitemap")
        built.append((p, raw, indexable))

    for t in SP["testimonials"]:
        if t.get("foto"):
            fp = ROOT / t["foto"]
            if not fp.exists():
                errors.append(f"data/social-proof.json: foto {t['foto']} tidak ada")
            elif fp.suffix.lower() not in (".webp", ".avif") or fp.stat().st_size > 40 * 1024:
                errors.append(f"data/social-proof.json: foto {t['foto']} harus WebP/AVIF ≤ 40 KB")
        elif not t.get("contoh"):
            warnings.append(f"data/social-proof.json: testimoni asli '{t['name']}' belum ada fotonya (sementara avatar inisial)")
    n_contoh = sum(1 for k in ("metrics", "logos", "testimonials") for x in SP[k] if x.get("contoh"))
    if n_contoh:
        msg = f"data/social-proof.json: {n_contoh} entri masih data CONTOH"
        if S.get("site_url"):
            errors.append(msg + " — ganti dengan data asli sebelum publish")
        else:
            warnings.append(msg + " — boleh untuk preview, build publish akan ditolak")
    used_all = {gid for p, _, _ in built for gid in p.get("_gambar", [])}
    for gid in GAMBAR:
        if gid not in used_all:
            warnings.append(f"data/ilustrasi.json: gambar '{gid}' tidak dipakai di halaman mana pun")
    if not check_only:
        (ROOT / "docs").mkdir(exist_ok=True)
        (ROOT / "docs" / "daftar-ilustrasi.md").write_text(daftar_ilustrasi_md(S, pages, IL), encoding="utf-8")
    if S.get("site_url") and not S.get("og_image"):
        warnings.append("site.json: og_image kosong → pratinjau link di WhatsApp/sosmed tanpa gambar")
    if not S.get("site_url"):
        warnings.append("site.json: site_url kosong → canonical, og:url, sitemap.xml tidak dibuat")
    if not S.get("checkout_url"):
        msg = "site.json: checkout_url kosong → tombol beli mengarah ke /harga#pilih-skema"
        (errors if S.get("site_url") else warnings).append(msg + (" — wajib diisi sebelum publish" if S.get("site_url") else ""))
    if not S.get("signin_url"):
        msg = "site.json: signin_url kosong → tombol Sign In belum mengarah ke halaman login"
        (errors if S.get("site_url") else warnings).append(msg + (" — wajib diisi sebelum publish" if S.get("site_url") else ""))
    if not S.get("whatsapp"):
        msg = "site.json: whatsapp kosong → tombol WA melayang mengarah ke #kontak"
        (errors if S.get("site_url") else warnings).append(msg + (" — wajib diisi sebelum publish" if S.get("site_url") else ""))

    if not check_only and not errors:
        if DIST.exists():
            shutil.rmtree(DIST)
        shutil.copytree(ROOT / "static", DIST / "static")
        for p, body, indexable in built:
            o = out_file(p["slug"])
            o.parent.mkdir(parents=True, exist_ok=True)
            o.write_text(render(S, p, body, P, pages, indexable), encoding="utf-8")
        nf = {"slug": "/404", "name": "Halaman tidak ditemukan", "title": "Halaman tidak ditemukan", "meta": "",
              "h1": "Halaman tidak ditemukan", "lead": "Alamat ini tidak ada. Coba mulai dari beranda."}
        (DIST / "404.html").write_text(render(S, nf, '<p><a href="/">Kembali ke beranda</a></p>', P, pages, False), encoding="utf-8")
        robots = "User-agent: *\nAllow: /\n"
        if S.get("site_url"):
            urls = "".join(f"<url><loc>{S['site_url']}{p['slug']}</loc></url>" for p, _, ok in built if ok)
            (DIST / "sitemap.xml").write_text(
                f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
                encoding="utf-8")
            robots += f"Sitemap: {S['site_url']}/sitemap.xml\n"
        (DIST / "robots.txt").write_text(robots, encoding="utf-8")

    print(f"{len(built)} halaman diperiksa")
    for p, _, ok in built:
        print(f"  {p['slug']:<34} {p.get('_words', 0):>5} kata  {'index' if ok else 'NOINDEX'}")
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR  ", e)
    if errors:
        print(f"\n{len(errors)} error — build dihentikan.")
        sys.exit(1)
    print("\nOK" + ("" if check_only else f" — hasil di {DIST.relative_to(ROOT)}/"))


if __name__ == "__main__":
    main()
