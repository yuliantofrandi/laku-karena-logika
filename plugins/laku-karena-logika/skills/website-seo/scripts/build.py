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
    # tanpa badge "Disarankan" di header tabel (user: "hilangkan"); rekomendasi cukup di kartu persona & tombol utama
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
    strip = addon_strip(P)
    catatan = f'<p class="note">{P["note"]}</p>' if P.get("note") else ""
    return (f'<div class="periode" id="pilih-skema">{periode_switch(P)}<p class="table-hint">Geser ke kanan untuk melihat semua paket →</p><div class="table-wrap"><table class="pricing"><thead><tr><th scope="col"><span class="sr-only">Jumlah karyawan</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>{foot}</table></div>{strip}{catatan}</div>')


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


def nama_addon(a):
    nama = html.escape(a["name"])
    return f'<a href="{a["link"]}">{nama}</a>' if a.get("link") else nama


def addon_strip(P):
    """Add-on ringkas di bawah tabel harga (user: "add-on gabung di bawah section harga, jangan terlalu banyak
    informasi"). Satu kotak: label "Add-on" sekali di kiri, tiap add-on satu baris (nama · deskripsi 1 kalimat ·
    harga yang ikut switch bulanan/tahunan), dipisah garis tipis bila lebih dari satu."""
    m = P["annual_months_paid"]
    adds = P.get("addons", [])
    if not adds:
        return ""
    rows = "".join(
        f'<li><strong>{nama_addon(a)}</strong><span class="addon-desc">{html.escape(a["desc"])}</span>'
        f'<span class="addon-price"><span class="bln">+{rupiah(a["monthly"])}/karyawan/bln</span>'
        f'<span class="thn">+{rupiah(a["monthly"] * m)}/karyawan/thn</span></span></li>'
        for a in adds)
    return f'<div class="addon-strip"><span class="badge-addon">Add-on</span><ul class="addon-list">{rows}</ul></div>'


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
    """CTA penutup = satu-satunya tempat urgensi + jaminan (tidak diulang di section lain), dibuat RINGKAS.
    Kiri: judul, satu kalimat pendek, tombol. Kanan: satu daftar centang copy.cta_poin (maks 4 poin, masing-masing ≤6 kata)."""
    C = S["copy"]
    points = "".join(f"<li>{t}</li>" for t in C.get("cta_poin", []))            # boleh berisi link
    side = f'<div class="cta-side"><ul class="terms">{points}</ul></div>' if points else ""
    return (f'<aside class="cta" id="kontak"><div class="cta-main"><h2>{C["cta_title"]}</h2><p>{C["cta_text"]}</p>'
            f'<div class="cta-btns"><a class="btn btn-primary" href="{checkout_link(S)}" rel="nofollow">{C["cta_primary"]}</a>'
            f'<a class="btn btn-ghost" href="{C["cta_secondary_href"]}">{C["cta_secondary"]}</a></div></div>{side}</aside>')


def check_cta_copy(S):
    """CTA penutup harus padat (keluhan user: "terlalu banyak teks")."""
    C = S["copy"]
    n = len(strip_tags(C.get("cta_text", "")).split())
    if n > 16:
        warnings.append(f"site.json: copy.cta_text {n} kata (maks ±16) — CTA penutup harus singkat")
    pts = C.get("cta_poin", [])
    if len(pts) > 4:
        warnings.append(f"site.json: copy.cta_poin {len(pts)} poin (maks 4)")
    for t in pts:
        if len(strip_tags(t).split()) > 6:
            warnings.append(f"site.json: copy.cta_poin '{strip_tags(t)}' > 6 kata — ringkas jadi frasa pendek")


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
    items = [x for it in S["nav"] if isinstance(it, dict) for x in it["items"] if x[0] != "/white-label"]
    li = "".join(f'<li><a href="{x[0]}"><strong>{x[1]}</strong></a>' + (f" — {html.escape(x[2])}" if len(x) > 2 else "") + "</li>"
                 for x in items)
    return f'<ul class="checks">{li}</ul>'


def ul_checks(items):
    return '<ul class="checks">' + "".join(f"<li>{html.escape(t)}</li>" for t in items) + "</ul>"


def cta_whitelabel(S):
    W = S["whitelabel"]
    return (f'<aside class="cta solo" id="kontak"><div class="cta-main"><h2>{fill_brand(S, W["cta_title"])}</h2><p>{fill_brand(S, W["cta_text"])}</p>'
            f'<div class="cta-btns"><a class="btn btn-primary" href="{wa_link(S, fill_brand(S, W["wa_text"]))}" target="_blank" rel="nofollow noopener">{W["cta_button"]}</a>'
            f'<a class="btn btn-ghost" href="/harga">Lihat harga versi langganan</a></div></div></aside>')


IKON_TRUST = {
    "server": '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8 12l3 3 5-6"/>',
    "support": '<path d="M4 13v-1a8 8 0 0 1 16 0v1"/><rect x="2" y="13" width="5" height="7" rx="2"/><rect x="17" y="13" width="5" height="7" rx="2"/>',
}


TAHUN = __import__("datetime").date.today().year


def foot_legal(S):
    """Link legal di footer bawah (site.json legal). Email tidak ditampilkan bila user memilih kontak lewat WA saja."""
    items = S.get("legal", [])
    return ('<nav class="foot-legal" aria-label="Legal">' + "".join(f'<a href="{x["slug"]}">{html.escape(x["name"])}</a>' for x in items) + "</nav>") if items else ""


def foot_trust(S):
    """Baris kepercayaan di kolom logo footer (mengisi ruang kosong di bawah deskripsi). site.json footer_trust:
    [{"ikon": "server|shield|support", "teks": "..."}] — hanya fakta yang sudah tertulis di website/BKB."""
    items = S.get("footer_trust", [])
    if not items:
        return ""
    li = "".join(f'<li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IKON_TRUST.get(x.get("ikon"), IKON_TRUST["shield"])}</svg>'
                 f'{html.escape(x["teks"])}</li>' for x in items)
    return f'<ul class="foot-trust">{li}</ul>'


def logo(S):
    """Logo: SVG di-inline; PNG/WebP (logo asli brand) dipasang sebagai <img> dengan width/height dari file
    (tinggi tampil = site.json logo_tinggi, default 26px) agar tidak CLS."""
    path = S.get("logo", "static/logo.svg")
    f = ROOT / path
    if f.suffix.lower() == ".svg":
        return re.sub(r'\s*xmlns="[^"]+"', "", f.read_text(encoding="utf-8").strip(), count=1)
    import struct
    head = f.read_bytes()[:32]
    pw, ph = struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else (S.get("logo_w", 200), S.get("logo_h", 26))
    th = S.get("logo_tinggi", 26)
    tw = round(pw * th / ph)
    return f'<img class="logo" src="{versi("/" + path)}" width="{tw}" height="{th}" alt="{html.escape(S["brand"])}" decoding="async">'


# ---------- gambar & ilustrasi ----------

def versi(path):
    """URL aset + ?v=<hash isi file> agar gambar/video yang diganti langsung terlihat (tidak tertahan cache browser/CDN)."""
    f = ROOT / path.lstrip("/")
    if not f.exists():
        return path
    import hashlib
    return f"{path}?v={hashlib.md5(f.read_bytes()).hexdigest()[:8]}"


def img_src(g):
    return "/" + (g.get("file") or f'static/ilustrasi/{g["id"]}.svg')


def figure(g, hero=False):
    w, h = g.get("w", ILUS.W), g.get("h", ILUS.H)
    load = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    cap = f'<figcaption>{html.escape(g["caption"])}</figcaption>' if g.get("caption") else ""
    media = (f'<img src="{versi(img_src(g))}" width="{w}" height="{h}" '
             f'alt="{html.escape(g["alt"])}" {load} decoding="async">')
    if hero:   # bingkai: bentuk gradasi kecil & miring yang hanya mengintip di belakang media (pemanis)
        media = f'<span class="hero-media">{media}</span>'
    portrait = " portrait" if h > w else ""
    return f'<figure class="ilus{portrait}{" hero-img" if hero else ""}">{media}{cap}</figure>'


def video_figure(g, hero=False):
    """Motion graphic milik user (field "video" di ilustrasi.json, "file" = poster JPG/WebP).
    Tanpa suara, loop; file video baru diunduh saat mendekati layar (VIDEO_JS) agar tidak membebani PageSpeed."""
    w, h = g.get("w", 1080), g.get("h", 1920)
    cap = f'<figcaption>{html.escape(g["caption"])}</figcaption>' if g.get("caption") else ""
    portrait = " portrait" if h > w else ""
    media = (f'<video muted loop playsinline preload="none" poster="{versi(img_src(g))}" data-src="{versi("/" + g["video"])}" '
             f'width="{w}" height="{h}" aria-label="{html.escape(g["alt"])}"></video>')
    if hero:
        media = f'<span class="hero-media">{media}</span>'
    sama = " kolom-sama" if g.get("kolom") == "sama" else ""
    return f'<figure class="ilus video{portrait}{sama}{" hero-img" if hero else ""}">{media}{cap}</figure>'


# Setelah halaman selesai dimuat (tidak bersaing dengan LCP), muat video saat mendekati layar;
# hormati prefers-reduced-motion (tampil poster + kontrol).
VIDEO_JS = (
    "<script>addEventListener('load',function(){var v=document.querySelectorAll('video[data-src]');if(!v.length)return;"
    "var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;"
    "function main(x){x.play().catch(function(){if(document.hidden){document.addEventListener('visibilitychange',function f(){if(!document.hidden){document.removeEventListener('visibilitychange',f);main(x)}})}else{x.controls=true}})}"
    "function go(x){x.src=x.dataset.src;x.removeAttribute('data-src');if(rm){x.controls=true}else{x.autoplay=true;main(x)}}"
    "if(!('IntersectionObserver'in window)){v.forEach(go);return}"
    "var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){go(e.target);o.unobserve(e.target)}})},{rootMargin:'200px'});"
    "v.forEach(function(x){o.observe(x)})})</script>")


def gambar_token(m):
    gid = m.group(1)
    if gid not in GAMBAR:
        return f"{{{{gambar:{gid}}}}}"   # dibiarkan -> tertangkap cek token tak dikenal
    g = GAMBAR[gid]
    return video_figure(g) if g.get("video") else figure(g)


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
WIDE = ("grid", "table-wrap", "periode", "plans", "quotes", "proof", "cta", "guarantee", "penutup")   # penutup: paragraf rata tengah di bawah blok lebar
# blok yang tetap terlihat di kolom teks
KEEP = ("callout", "agitate", "checks", "faq", "note", "stat")


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
    - FAQ             → judul besar rata tengah + satu kotak daftar bergaris dengan chevron
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
    if fig and scan and "portrait" in fig:   # video/gambar potret tinggi → kartu ikut ke kolom teks agar tidak ada ruang kosong
        for i, b in enumerate(wide):
            if "grid" in kind(b)[1]:
                scan.append(wide.pop(i)); break
    if fig and not scan:   # kartu (grid) atau tabel perbandingan ikut ke kolom teks, sejajar dengan gambar
        for i, b in enumerate(wide):
            if "grid" in kind(b)[1] or ("table-wrap" in kind(b)[1] and len(strip_tags(b)) <= 460):   # tabel panjang tetap lebar
                scan.append(wide.pop(i)); break
    # daftar panjang di panel → dua kolom supaya panel tidak terlalu tinggi
    scan = [re.sub(r'^<(ul|ol)( class="checks")?', lambda m: f'<{m.group(1)} class="{"checks " if m.group(2) else ""}two-col"', b, count=1)
            if kind(b)[0] in ("ul", "ol") and b.count("<li") > 4 and not fig else b for b in scan]
    faq = any("faq" in kind(b)[1] for b in scan)
    lead = h2 + "".join(paras)
    if fig:
        flip = " flip" if idx % 2 else ""
        # media potret → kolom media selebar media saja, kecuali entri meminta kolom 50:50 ("kolom": "sama")
        potret = " potret" if "portrait" in fig and "kolom-sama" not in fig else ""
        row = (f'<div class="split media{flip}{potret}"><div class="col-text">{lead}{"".join(scan)}</div>'
               f'<div class="col-media">{fig}</div></div>')
    elif faq:
        # FAQ (layout referensi user): judul besar rata tengah + satu kotak daftar bergaris dengan chevron.
        # Siap 20+ pertanyaan: accordion eksklusif (<details name>) dan grup topik <h3> → chip navigasi. Tanpa JS.
        faq_html = "".join(scan).replace('<details class="faq">', f'<details class="faq" name="faq-{idx}">')
        parts = re.split(r"(<h3[^>]*>.*?</h3>)", faq_html, flags=re.S)
        topics, body_parts, buf = [], [], []
        def flush():
            if "".join(buf).strip():
                body_parts.append(f'<div class="faq-list">{"".join(buf)}</div>')
            buf.clear()
        for part in parts:
            if part.startswith("<h3"):
                flush()
                label = strip_tags(part).strip()
                tid = f"faq-{idx}-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
                topics.append((tid, label))
                body_parts.append(f'<h3 class="faq-group" id="{tid}">{html.escape(label)}</h3>')
            else:
                buf.append(part)
        flush()
        nav = ""
        if topics:
            nav = ('<nav class="faq-topics" aria-label="Topik pertanyaan">'
                   + "".join(f'<a href="#{t}">{html.escape(l)}</a>' for t, l in topics) + "</nav>")
        # Subjudul wajib di bawah judul FAQ: paragraf pembuka section, atau copy.faq_lead bila tidak ada
        intro = "".join(paras) or (f'<p>{S["copy"]["faq_lead"]}</p>' if S and S.get("copy", {}).get("faq_lead") else "")
        row = f'<div class="faq-center">{h2}{intro}{nav}{"".join(body_parts)}</div>'
    elif scan:
        flip = " flip" if idx % 2 else ""
        # angka besar (div.stat) mengisi kolom teks supaya tidak menyisakan ruang kosong di samping panel
        stats = [b for b in scan if "stat" in kind(b)[1]]
        scan = [b for b in scan if b not in stats]
        # isi panel jauh lebih panjang dari judul+pembuka → kolom teks akan menyisakan ruang kosong;
        # susun judul di atas dan panel selebar kontainer (keluhan user: "atas bawahnya ada blank space")
        lead_len = len(strip_tags(h2)) * 1.8 + sum(len(strip_tags(p)) for p in paras) + 160 * len(stats)
        if stats:
            # section dengan angka besar: judul + pembuka rata tengah di atas, lalu angka | panel (permintaan user: "jadikan di tengah section")
            row = (f'<div class="sec-center">{lead}</div>'
                   f'<div class="stat-row"><div class="col-stat">{"".join(stats)}</div><div class="panel">{"".join(scan)}</div></div>')
        elif len(strip_tags("".join(scan))) > 2.3 * lead_len:
            scan = [re.sub(r'^<(ul|ol)( class="checks")?(?! class="[^"]*two-col)', lambda m: f'<{m.group(1)} class="{"checks " if m.group(2) else ""}two-col"', b, count=1)
                    if kind(b)[0] in ("ul", "ol") and b.count("<li") > 2 and "two-col" not in b else b for b in scan]
            row = f'<div class="split stack"><div class="col-text">{lead}</div></div><div class="panel panel-wide">{"".join(scan)}</div>'
        else:
            row = f'<div class="split panel-row{flip}"><div class="col-text">{lead}</div><div class="col-panel"><div class="panel">{"".join(scan)}</div></div></div>'
    else:
        # section tabel harga & kartu ikon rata tengah: judul + pembuka rata tengah di atas (permintaan user)
        tengah = " center" if any(c in kind(b)[1] for b in wide for c in ("periode", "persona", "ikon-tengah")) else ""
        row = f'<div class="split stack{tengah}"><div class="col-text">{lead}</div></div>'
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
    if page.get("sederhana"):   # halaman legal: hero polos (judul + lead), tanpa CTA & statistik
        hero_cta = ""
    elif page["slug"] == "/404":
        hero_cta = f'<a class="btn btn-primary btn-lg hero-cta" href="/">Kembali ke beranda <span aria-hidden="true">→</span></a>'
    elif page["slug"] == "/white-label" and S.get("whitelabel"):
        hero_cta = (f'<a class="btn btn-primary btn-lg hero-cta" href="{wa_link(S, fill_brand(S, S["whitelabel"]["wa_text"]))}" '
                    f'target="_blank" rel="nofollow noopener">{S["whitelabel"]["cta_button"]} <span aria-hidden="true">→</span></a>')
    else:
        hero_cta = f'<a class="btn btn-primary btn-lg hero-cta" href="{checkout_link(S)}" rel="nofollow">{S["copy"]["cta_primary"]} <span aria-hidden="true">→</span></a>'
    hero_class = "hero home" if page["slug"] == "/" else "hero"
    if page.get("sederhana"):   # hero polos halaman legal: padding lebih rapat
        hero_class += " hero-sederhana"
    lead = page.get("lead", "")
    hg = GAMBAR.get(HERO.get(page["slug"]))
    hero_img = ((video_figure(hg, hero=True) if hg.get("video") else figure(hg, hero=True)) if hg else "")
    # poster video hero = kandidat LCP → preload prioritas tinggi
    hero_preload = (f'<link rel="preload" as="image" href="{versi(img_src(hg))}" fetchpriority="high">\n' if hg and hg.get("video") else "")
    # kolom footer pertama = nama & urutan menu atas (grup Solusi lalu menu utama lain), supaya konsisten dengan header
    urut = [x[0] for it in S["nav"] if isinstance(it, dict) for x in it["items"]] + [it[0] for it in S["nav"] if isinstance(it, list)]
    by_slug = {p["slug"]: p for p in all_pages}
    produk = [by_slug[u] for u in urut if u in by_slug]
    label_menu = next((it["label"] for it in S["nav"] if isinstance(it, dict)), "Produk")
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
{hero_preload}<link rel="preload" href="/static/fonts/montserrat-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
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
{hero_stats(S) if page["slug"] != "/404" and not page.get("sederhana") else ""}
</div>{hero_img}</div></section>
<article class="content prose">
{('<section class="band dok-band"><div class="wrap">' + body + '</div></section>') if page.get("dokumen") else layout_sections(body)}
</article>
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-brand">{logo(S)}<p>{S["tagline"]}</p><p class="muted">{html.escape(S["description"])}</p>{foot_trust(S)}</div>
<div><h2>{label_menu}</h2><ul>{flinks(produk)}</ul></div>
<div><h2>Panduan</h2><ul>{flinks(panduan)}</ul></div>
</div><div class="wrap foot-bottom"><span>© {TAHUN} {S["brand"]}. Hak cipta dilindungi.</span>{foot_legal(S)}</div></footer>
{float_bar(S)}
{VIDEO_JS if 'video muted' in body + hero_img else ''}
</body>
</html>
"""


# ---------- cek aturan ----------

# standar minimum UI per section (disetujui user): H2 → 1–2 kalimat → minimal satu elemen visual/yang bisa dipindai
VISUAL_CLASSES = {"stat", "grid", "table-wrap", "periode", "plans", "quotes", "proof", "callout", "agitate", "checks", "faq", "cta"}


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


def ilus_teks(x):
    """Semua teks label di data ilustrasi (rekursif)."""
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [t for k, v in x.items() if k not in ("icon", "warna", "color") for t in ilus_teks(v)]
    if isinstance(x, list):
        return [t for v in x for t in ilus_teks(v)]
    return []


def check_stat(sid, raw):
    """WARNING bila angka besar (strong) dan keterangannya (span) di div.stat mengulang angka/kata yang sama
    (kasus nyata: "300 karyawan" + "berarti 300 biaya lisensi")."""
    kata = lambda t: {w for w in re.findall(r"[a-z0-9]+", strip_tags(t).lower()) if len(w) > 2 or w.isdigit()}
    for big, cap in re.findall(r'<div class="stat"><strong>(.*?)</strong><span>(.*?)</span>', raw, flags=re.S):
        sama = kata(big) & kata(cap)
        if sama:
            warn(sid, f"kartu angka '{strip_tags(big)}': keterangan mengulang '{', '.join(sorted(sama))}' — pakai kata lain")


def check_ilustrasi_duplikat(sid, raw):
    """WARNING bila ilustrasi sebuah section hanya mengulang poin/kartu di section itu
    (kasus nyata: ilustrasi 3 langkah di samping 3 kartu langkah yang sama). Ilustrasi harus menambah
    informasi — hasil/layar produk, bukan salinan teks section."""
    kata = lambda t: {w for w in re.findall(r"[a-z0-9]+", strip_tags(t).lower()) if len(w) > 2}
    for chunk in re.split(r"<h2[^>]*>", raw)[1:]:
        h2 = strip_tags(chunk.split("</h2>")[0])
        items = [kata(m) for m in re.findall(r"<(?:h3|li)[^>]*>(.*?)</(?:h3|li)>", chunk, flags=re.S)]
        for gid in re.findall(r"\{\{gambar:([a-z0-9-]+)\}\}", chunk):
            labels = [kata(t) for t in ilus_teks(GAMBAR.get(gid, {}).get("data", {}))]
            labels = [l for l in labels if len(l) >= 2]
            sama = sum(1 for l in labels if any(len(l & it) >= 0.6 * len(l) for it in items))
            if labels and sama >= 2 and sama >= len(labels) / 2:
                warn(sid, f"ilustrasi '{gid}' di section '{h2}' mengulang {sama}/{len(labels)} poin isi section — "
                          "ganti dengan visual yang menambah info (hasil/layar produk) atau hapus gambarnya")


MAX_VIDEO_MB = 5


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
        if g.get("video"):
            vf = ROOT / g["video"]
            if not vf.exists():
                err(sid, f"video {g['video']} tidak ada")
            elif vf.suffix.lower() not in (".mp4", ".webm"):
                err(sid, f"video '{gid}' harus MP4 (H.264) atau WebM")
            elif vf.stat().st_size > MAX_VIDEO_MB * 1024 * 1024:
                warn(sid, f"video '{gid}' {vf.stat().st_size / 1048576:.1f} MB (sebaiknya ≤{MAX_VIDEO_MB} MB) — kompres")
            if f.suffix.lower() not in (".webp", ".avif", ".jpg", ".jpeg"):
                err(sid, f"poster video '{gid}' harus WebP/AVIF/JPG")
            if not (g.get("w") and g.get("h")):
                err(sid, f"video '{gid}' wajib punya w & h (ukuran asli) agar tidak CLS")
        elif not g.get("auto", True):
            if f.suffix.lower() not in (".webp", ".avif", ".svg"):
                err(sid, f"gambar '{gid}' harus WebP/AVIF (atau SVG), bukan {f.suffix}")
            if not (g.get("w") and g.get("h")):
                err(sid, f"gambar '{gid}' wajib punya w & h (ukuran asli) agar tidak CLS")
        kb = f.stat().st_size / 1024
        if kb > MAX_KB:
            err(sid, f"gambar '{gid}' {kb:.0f} KB (maks {MAX_KB} KB) — kompres dulu")
    n = len(set(used + ([HERO[sid]] if sid in HERO else [])))
    minimal = IL.get("min_per_halaman_khusus", {}).get(sid, IL.get("min_per_halaman", 3))
    if n < minimal:
        err(sid, f"hanya {n} gambar (minimal {minimal} per halaman)")
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
    check_cta_copy(S)
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

    # aturan tetap: setiap landing page wajib punya Syarat Layanan & Kebijakan Privasi (isi nyata, tautan di footer)
    legal_slugs = [x["slug"] for x in S.get("legal", [])]
    for wajib, nama in (("/syarat-layanan", "Syarat Layanan"), ("/kebijakan-privasi", "Kebijakan Privasi")):
        if wajib not in legal_slugs:
            err(wajib, f'"{nama}" wajib ada di site.json legal (tautan footer) — lihat references/standar-dokumen-legal.md')

    # aturan tetap: setiap website produk punya halaman Harga standar (references/standar-halaman-harga.md)
    hp = S.get("pricing_page", "/harga")
    if hp not in slugs:
        err(hp, "halaman Harga wajib ada di site.json extra_pages (salin template assets/starter/content/harga.html)")
    if not any(isinstance(it, list) and it[0] == hp for it in S["nav"]):
        err(hp, "menu 'Harga' wajib ada di menu utama (site.json nav)")
    hf = ROOT / "content" / (hp.strip("/") + ".html")
    if hf.exists() and "{{pricing_table}}" not in hf.read_text(encoding="utf-8"):
        err(hp, "halaman Harga wajib memakai {{pricing_table}} (satu tabel harga + switch + add-on)")

    # aturan tetap: setiap produk bisa dibeli whitelabel -> halaman + menu utama wajib ada
    if "/white-label" not in slugs:
        err("/white-label", "halaman White Label wajib ada di site.json extra_pages (salin dari template skill)")
    wlf = ROOT / "content" / "white-label.html"
    if wlf.exists() and "{{cta_whitelabel}}" not in wlf.read_text(encoding="utf-8"):
        err("/white-label", "halaman White Label wajib memakai {{cta_whitelabel}} (konsultasi WA, bukan checkout) — lihat references/standar-halaman-white-label.md")
    # White Label = item terakhir di grup Solusi, bukan menu utama (user: "90% pembeli tidak ingin whitelabel")
    nav_slugs = [it[0] for it in S["nav"] if isinstance(it, list)] + [x[0] for it in S["nav"] if isinstance(it, dict) for x in it["items"]]
    if "/white-label" not in nav_slugs:
        err("/white-label", "menu 'White Label' wajib ada di menu (item terakhir grup Solusi di site.json nav)")
    elif "/white-label" in [it[0] for it in S["nav"] if isinstance(it, list)]:
        warn("/white-label", "White Label sebaiknya di dalam grup Solusi (item terakhir), bukan menu utama")

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
        check_ilustrasi_duplikat(p["slug"], raw)
        check_stat(p["slug"], raw)
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
        # halaman legal: pakai content/<slug>.html bila sudah ada; bila belum, placeholder noindex
        def pasal_legal(lg):
            f = ROOT / "content" / (lg["slug"].strip("/") + ".html")
            if not f.exists():
                return []
            return [(m.group(1), m.group(2).strip().replace("{{brand}}", S["brand"])) for m in re.finditer(r"<h2>(\d+)\.\s*(.*?)</h2>", f.read_text(encoding="utf-8"))]
        def nav_legal(aktif):
            grup = []
            for lg in S.get("legal", []):
                cur = lg["slug"] == aktif
                items = "".join(f'<li><a href="{"" if cur else lg["slug"]}#pasal-{n}">{n}. {html.escape(strip_tags(t))}</a></li>' for n, t in pasal_legal(lg))
                grup.append(f'<details class="dok-grup{" aktif" if cur else ""}"{" open" if cur else ""}><summary>{html.escape(lg["name"])}</summary><ol>{items}</ol></details>')
            isi = "".join(grup)
            # desktop: sidebar kiri selalu terbuka; mobile: "Daftar isi" tertutup agar tidak mendorong isi dokumen ke bawah
            return (f'<aside class="dok-nav" aria-label="Daftar isi dokumen">{isi}</aside>'
                    f'<details class="dok-toc-hp"><summary>Daftar isi</summary>{isi}</details>')
        for lg in S.get("legal", []):
            src = ROOT / "content" / (lg["slug"].strip("/") + ".html")
            if src.exists():
                body_lg = src.read_text(encoding="utf-8")
                tgl = S.get("legal_berlaku", "")
                body_lg = (body_lg.replace("{{brand}}", S["brand"]).replace("{{tanggal_berlaku}}", tgl)
                           .replace("{{wa_link}}", wa_link(S, f'Halo, saya ingin bertanya tentang {lg["name"]} {S["brand"]}')))
                body_lg = re.sub(r"<h2>(\d+)\.\s*(.*?)</h2>", r'<h2 id="pasal-\1"><span class="no">\1</span>\2</h2>', body_lg)
                body_lg = (f'<div class="dok-grid">{nav_legal(lg["slug"])}<div class="dokumen">'
                           f'{body_lg}</div></div>')
            else:
                err(lg["slug"], f'dokumen "{lg["name"]}" belum ditulis — wajib di setiap landing page; tulis content{lg["slug"]}.html dengan isi nyata (references/standar-dokumen-legal.md)')
                body_lg = (f'<p>Dokumen {html.escape(lg["name"])} {S["brand"]} sedang disiapkan dan akan segera tersedia di halaman ini.</p>'
                           f'<p>Ada pertanyaan? <a href="{wa_link(S, "Halo, saya ingin bertanya tentang " + lg["name"] + " " + S["brand"])}" rel="nofollow noopener" target="_blank">Hubungi kami lewat WhatsApp</a>.</p>')
            pg = {"slug": lg["slug"], "name": lg["name"], "title": f'{lg["name"]} {S["brand"]}', "meta": "",
                  "h1": lg["name"], "eyebrow": "Dokumen legal",
                  "lead": lg.get("lead", "Ketentuan yang berlaku untuk pengguna {brand}.").replace("{brand}", S["brand"]),
                  "sederhana": True, "dokumen": src.exists()}
            out = DIST / lg["slug"].strip("/") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(S, pg, body_lg, P, pages, False), encoding="utf-8")
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
