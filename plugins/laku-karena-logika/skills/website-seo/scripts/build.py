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

ROOT = Path(__file__).resolve().parent
SOCIAL = {"testimonials": []}
DIST = ROOT / "dist"

# Klaim yang tidak boleh muncul (BKB: penelusuran jam→tugas→aplikasi→layar adalah standar kategori)
BANNED_CLAIMS = [
    r"satu-satunya", r"satu satunya", r"termurah", r"paling murah",
    r"pertama di (indonesia|dunia|pasar|kelasnya)", r"(aplikasi|software|platform|alat) pertama",
    r"nomor satu", r"#1\b",
]

errors, warnings = [], []


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

def pricing_table(P):
    s = P["schemes"]
    FEAT = ' class="featured"'
    head = "".join(f'<th scope="col"{FEAT if x.get("featured") else ""}>{x["name"]}<span>{x["label"]}</span></th>' for x in s)
    rows = []
    rows.append(f'<tr class="group"><th scope="rowgroup" colspan="{len(s)+1}">Bulanan / karyawan</th></tr>')
    for i, lab in enumerate(P["tier_labels"]):
        cells = "".join(f'<td>{rupiah(x["monthly"][i])}</td>' for x in s)
        rows.append(f"<tr><th scope=\"row\">{lab}</th>{cells}</tr>")
    m = P["annual_months_paid"]
    rows.append(f'<tr class="group"><th scope="rowgroup" colspan="{len(s)+1}">Tahunan / karyawan — {P["annual_rule"].lower()}</th></tr>')
    for i, lab in enumerate(P["tier_labels"]):
        cells = "".join(
            f'<td>{rupiah(x["monthly"][i]*m)}<small>setara {rupiah(x["monthly"][i]*m/12)}/bln</small></td>' for x in s)
        rows.append(f"<tr><th scope=\"row\">{lab}</th>{cells}</tr>")
    rows.append(f'<tr class="group"><th scope="rowgroup" colspan="{len(s)+1}">Fitur</th></tr>')
    for f in P["features"]:
        cells = "".join(f"<td>{html.escape(c)}</td>" for c in f[1:])
        rows.append(f"<tr><th scope=\"row\">{html.escape(f[0])}</th>{cells}</tr>")
    return (f'<div class="table-wrap"><table class="pricing"><thead><tr><th scope="col">Jumlah karyawan</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div><p class="note">{P["note"]}</p>')


def pricing_cards(S, P):
    cards = []
    for x in P["schemes"]:
        lo, hi = min(x["monthly"]), max(x["monthly"])
        feat = ' featured' if x.get("featured") else ''
        badge = '<span class="badge">Disarankan</span>' if x.get("featured") else ''
        cards.append(
            f'<div class="card plan{feat}">{badge}<h3>{x["name"]} · {x["label"]}</h3>'
            f'<p class="price">{rupiah(hi)}<span>/karyawan/bln</span></p>'
            f'<p class="price-sub">turun sampai {rupiah(lo)} untuk 100+ karyawan</p>'
            f'<p>{html.escape(x["for"])}</p>'
            f'<a class="btn {"btn-primary" if x.get("featured") else "btn-ghost"} btn-block" href="{checkout_link(S, x["id"])}" rel="nofollow">'
            f'{S["copy"]["plan_button"].replace("{nama}", x["name"])}</a>'
            f'<p class="annual"><a href="{checkout_link(S, x["id"], "tahunan")}" rel="nofollow">Bayar tahunan</a> — {P["annual_rule"].lower()}</p></div>')
    return f'<div class="plans" id="pilih-skema">{"".join(cards)}</div><p class="note">Detail lengkap di <a href="/harga">halaman harga</a>.</p>'


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
    C = S["copy"]
    title, text = C["cta_title"], C["cta_text"]
    terms = "".join(f"<li>{html.escape(t)}</li>" for t in P.get("terms", []))
    return (f'<aside class="cta" id="kontak"><h2>{title}</h2><p>{text}</p>'
            f'<a class="btn btn-primary" href="{checkout_link(S)}" rel="nofollow">{C["cta_primary"]}</a>'
            f'<a class="btn btn-ghost" href="{C["cta_secondary_href"]}">{C["cta_secondary"]}</a>'
            f'<ul class="terms">{terms}</ul></aside>')


def risk_reversal(S, P):
    items = "".join(f"<li>{html.escape(t)}</li>" for t in P.get("terms", []) + S["copy"].get("risk_extra", []))
    return f'<div class="callout guarantee"><p class="label">{S["copy"]["risk_label"]}</p><ul class="checks">{items}</ul></div>'


def social_proof(S, SP):
    m = "".join(f'<div class="metric"><strong>{html.escape(x["value"])}</strong><span>{html.escape(x["label"])}</span></div>' for x in SP["metrics"])
    l = "".join(f'<li>{html.escape(x["name"])}</li>' for x in SP["logos"])
    return (f'<section class="proof wide" aria-label="Bukti sosial"><div class="metrics">{m}</div>'
            f'<p class="proof-cap">{S["copy"]["proof_caption"]}</p><ul class="logos">{l}</ul></section>')


def testimonials(SP):
    out = []
    for t in SP["testimonials"]:
        stars = "★" * t["rating"] + "☆" * (5 - t["rating"])
        out.append(f'<figure class="card quote"><div class="stars" aria-label="Rating {t["rating"]} dari 5">{stars}</div>'
                   f'<blockquote><p>{html.escape(t["quote"])}</p></blockquote>'
                   f'<figcaption><strong>{html.escape(t["name"])}</strong> · {html.escape(t["role"])}, {html.escape(t["company"])}</figcaption></figure>')
    return f'<div class="quotes wide">{"".join(out)}</div>' 


def checkout_link(S, skema=None, periode="bulanan"):
    """Tombol beli. site.json checkout_url boleh memuat {skema} dan {periode}."""
    url = S.get("checkout_url", "")
    if not url:
        return "/harga#pilih-skema"
    return url.replace("{skema}", str(skema or "")).replace("{periode}", periode)


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


# ---------- whitelabel (wajib di setiap produk) ----------

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
        offers = [{"@type": "Offer", "name": f'{x["name"]} — {x["label"]}', "priceCurrency": "IDR",
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
    faqs = re.findall(r'<details class="faq">\s*<summary>(.*?)</summary>(.*?)</details>', body, flags=re.S)
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


def render(S, page, body, P, all_pages, indexable):
    base = S["site_url"]
    canonical = f'<link rel="canonical" href="{base}{page["slug"]}">' if base else ""
    robots = '<meta name="robots" content="index,follow">' if indexable else '<meta name="robots" content="noindex,follow">'
    CUR = ' aria-current="page"'
    nav = "".join(nav_item(it, page["slug"], CUR) for it in S["nav"])
    crumbs = "" if page["slug"] == "/" else f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">{S["brand"]}</a> / <span>{page["name"]}</span></nav>'
    hero_class = "hero home" if page["slug"] == "/" else "hero"
    lead = page.get("lead", "")
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
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#7B2CFF">
<style>{CSS}</style>
<script type="application/ld+json">{jsonld(S, page, body, P, indexable)}</script>
</head>
<body>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="{S["brand"]} — beranda">{logo(S)}</a>
<input type="checkbox" id="menu" class="menu-toggle" aria-label="Buka menu"><label for="menu" class="menu-btn" aria-hidden="true"><span></span></label>
<nav class="nav" aria-label="Utama">{nav}<a class="btn btn-primary btn-sm" href="{checkout_link(S)}" rel="nofollow">{S["copy"]["nav_cta"]}</a></nav>
</div></header>
<main>
<section class="{hero_class}"><div class="wrap">
{crumbs}
<h1>{html.escape(page["h1"])}</h1>
{f'<p class="lead">{lead}</p>' if lead else ''}
</div></section>
<article class="wrap prose">
{body}
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
    minw = page.get("min_words", 1000)
    if wc < minw:
        err(sid, f"isi {wc} kata (minimal {minw})")
    elif minw >= 1000 and wc > 1800:
        warn(sid, f"isi {wc} kata (target 1.000–1.500)")
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


def main():
    check_only = "--check" in sys.argv
    S, B, P = load("site.json"), load("data/brief.json"), load("data/pricing.json")
    SP = load("data/social-proof.json")
    global SOCIAL
    SOCIAL = SP
    pages = S["extra_pages"] + B["pages"]
    for p in S["extra_pages"]:
        for k in ("name", "title", "meta", "h1", "primary"):
            p[k] = fill_brand(S, p[k])
    for p in pages:
        p["product_schema"] = p["slug"] in S["product_pages"]
    slugs = {p["slug"] for p in pages}

    # aturan tetap: setiap produk bisa dibeli whitelabel -> halaman + menu utama wajib ada
    if "/whitelabel" not in slugs:
        err("/whitelabel", "halaman whitelabel wajib ada di site.json extra_pages (salin dari template skill)")
    if not any(isinstance(it, list) and it[0] == "/whitelabel" for it in S["nav"]):
        err("/whitelabel", "menu 'Whitelabel' wajib ada di menu utama (site.json nav)")

    for key in ("title", "meta", "h1"):
        seen = {}
        for p in pages:
            v = p[key].strip().lower()
            if v in seen:
                err(p["slug"], f"{key} sama persis dengan {seen[v]}")
            seen[v] = p["slug"]

    tokens = {
        "{{pricing_table}}": pricing_table(P), "{{pricing_cards}}": pricing_cards(S, P),
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
        lead = re.match(r"\s*<!--\s*lead:(.*?)-->", raw, flags=re.S)
        if lead:
            p["lead"] = lead.group(1).strip()
            raw = raw[lead.end():]
        for k, v in tokens.items():
            raw = raw.replace(k, v)
            if p.get("lead"):
                p["lead"] = p["lead"].replace(k, v)
        check_page(S, B, p, raw, slugs)
        indexable = S.get("legal_reviewed", {}).get(p["slug"], True)
        if not indexable:
            warn(p["slug"], "belum direview ahli hukum → noindex & tidak masuk sitemap")
        built.append((p, raw, indexable))

    n_contoh = sum(1 for k in ("metrics", "logos", "testimonials") for x in SP[k] if x.get("contoh"))
    if n_contoh:
        msg = f"data/social-proof.json: {n_contoh} entri masih data CONTOH"
        if S.get("site_url"):
            errors.append(msg + " — ganti dengan data asli sebelum publish")
        else:
            warnings.append(msg + " — boleh untuk preview, build publish akan ditolak")
    if not S.get("site_url"):
        warnings.append("site.json: site_url kosong → canonical, og:url, sitemap.xml tidak dibuat")
    if not S.get("checkout_url"):
        msg = "site.json: checkout_url kosong → tombol beli mengarah ke /harga#pilih-skema"
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
