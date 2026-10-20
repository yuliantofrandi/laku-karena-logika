#!/usr/bin/env python3
"""Ekspor halaman "(SEO saja)" dari keyword plan menjadi artikel Blog siap-CMS (API Lakukan).

Halaman SEO dengan ad_group "(SEO saja)" di data/brief.json bukan halaman statis: isinya
dipindah ke Blog dinamis (kategori "blog" di CMS Lakukan). Skrip ini mengubah content/<slug>.html
menjadi HTML artikel biasa yang aman untuk CMS:
  - komentar `<!-- lead: … -->` → ringkasan (excerpt)
  - kartu (grid/card) → <h3> + <p>, ikon & nomor dibuang
  - callout → <blockquote>, FAQ <details> → <h3> pertanyaan + jawaban
  - {{gambar:id}} → <img> (SVG ilustrasi dirender ke PNG 1600×1000 lewat Quick Look macOS)
  - {{cta}} dibuang (halaman artikel blog sudah memasang CTA penutup), token brand diisi
  - link ke halaman "(SEO saja)" lain diarahkan ke /blog/<slug>

Hasil: export/blog/<slug>.json (judul, slug, ringkasan, meta, kategori, isi HTML, daftar gambar)
dan export/blog/<slug>.html (pratinjau), plus export/blog/gambar/*.png.

Pemakaian:  python3 tools/ekspor_blog.py
"""
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "export" / "blog"


def seo_saja(B):
    return [p for p in B["pages"] if p.get("ad_group") == "(SEO saja)"]


def png_dari_svg(svg: Path, tujuan: Path):
    """Render SVG ilustrasi (viewBox 800×500) ke PNG 1600×1000 via Quick Look, lalu potong padding persegi."""
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(["qlmanage", "-t", "-s", "1600", "-o", t, str(svg)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        hasil = Path(t) / (svg.name + ".png")
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg.read_text(encoding="utf-8"))
        tinggi = round(1600 * float(vb.group(2)) / float(vb.group(1))) if vb else 1000
        subprocess.run(["sips", "-c", str(tinggi), "1600", "--cropOffset", "0", "0", str(hasil), "--out", str(tujuan)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def bersihkan(isi, S, slugs_blog, gambar, IL):
    lead = re.search(r"<!--\s*lead:\s*(.*?)\s*-->", isi, flags=re.S)
    isi = re.sub(r"<!--.*?-->", "", isi, flags=re.S)
    isi = isi.replace("{{cta}}", "").replace("{{brand}}", S["brand"])
    isi = re.sub(r"\{\{(?!gambar:)[a-z_]+\}\}", "", isi)

    def img(m):
        g = IL.get(m.group(1))
        if not g:
            return ""
        gambar.append({"id": g["id"], "file": f'gambar/{g["id"]}.png', "alt": g.get("alt", "")})
        return f'<img src="gambar/{g["id"]}.png" alt="{html.escape(g.get("alt", ""))}">'
    isi = re.sub(r"\{\{gambar:([a-z0-9-]+)\}\}", img, isi)
    # ikon/nomor kartu dibuang; kartu → h3 + p
    isi = re.sub(r'<span class="(ikon-bulat|ikon|num)"[^>]*>.*?</span>', "", isi, flags=re.S)
    isi = re.sub(r'<div class="card[^"]*">\s*(.*?)\s*</div>', r"\1", isi, flags=re.S)
    isi = re.sub(r'<div class="grid[^"]*">\s*(.*?)\s*</div>', r"\1", isi, flags=re.S)
    # callout → blockquote (label jadi teks tebal)
    def callout(m):
        dalam = re.sub(r'<p class="label">(.*?)</p>', r"<p><strong>\1</strong></p>", m.group(1))
        return f"<blockquote>{dalam.strip()}</blockquote>"
    isi = re.sub(r'<div class="callout[^"]*">\s*(.*?)\s*</div>', callout, isi, flags=re.S)
    # FAQ details → h3 + jawaban
    faq = re.findall(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', isi, flags=re.S)
    isi = re.sub(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>', r"<h3>\1</h3>\2", isi, flags=re.S)
    # tabel: buang pembungkus
    isi = re.sub(r'<div class="table-wrap">\s*(.*?)\s*</div>', r"\1", isi, flags=re.S)
    # atribut class sisa dibuang (CMS memakai gaya bawaannya)
    isi = re.sub(r'\s+class="[^"]*"', "", isi)
    # link ke halaman "(SEO saja)" lain → /blog/<slug>
    for s in slugs_blog:
        isi = re.sub(rf'href="{re.escape(s)}(#[^"]*)?"', lambda m, s=s: f'href="/blog{s}{m.group(1) or ""}"', isi)
    isi = re.sub(r"\n{3,}", "\n\n", isi).strip()
    return isi, (lead.group(1).strip() if lead else ""), faq


def main():
    S = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    B = json.loads((ROOT / "data" / "brief.json").read_text(encoding="utf-8"))
    IL = {g["id"]: g for g in json.loads((ROOT / "data" / "ilustrasi.json").read_text(encoding="utf-8"))["gambar"]}
    halaman = seo_saja(B)
    if not halaman:
        print("Tidak ada halaman \"(SEO saja)\" di data/brief.json")
        return
    slugs = [p["slug"] for p in halaman]
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "gambar").mkdir(parents=True)
    for p in halaman:
        src = ROOT / "content" / (p["slug"].strip("/") + ".html")
        gambar = []
        isi, lead, faq = bersihkan(src.read_text(encoding="utf-8"), S, slugs, gambar, IL)
        for g in gambar:
            svg = ROOT / "dist" / "static" / "ilustrasi" / f'{g["id"]}.svg'
            if not svg.exists():
                sys.exit(f"SVG {svg} belum ada — jalankan python3 build.py dulu")
            png_dari_svg(svg, OUT / g["file"])
        artikel = {
            "slug": p["slug"].strip("/"),
            "title": p["h1"],
            "meta_title": p["title"],
            "excerpt": p["meta"],
            "lead": lead,
            "category": "blog",
            "primary_keyword": p.get("primary", ""),
            "cover": gambar[0]["file"] if gambar else "",
            "images": gambar,
            "faq": [{"q": html.unescape(re.sub(r"<[^>]+>", "", q)).strip(),
                     "a": " ".join(html.unescape(re.sub(r"<[^>]+>", " ", a)).split())} for q, a in faq],
            "content": isi,
            "url_lama": p["slug"],
            "url_baru": f'/blog{p["slug"]}',
        }
        (OUT / f'{artikel["slug"]}.json').write_text(json.dumps(artikel, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / f'{artikel["slug"]}.html').write_text(
            f'<!doctype html><meta charset="utf-8"><title>{html.escape(artikel["title"])}</title>'
            f'<style>body{{font:17px/1.65 system-ui;max-width:760px;margin:40px auto;padding:0 16px;color:#1b1626}}'
            f'img{{max-width:100%;border-radius:12px;border:1px solid #e9e5f0}}table{{border-collapse:collapse;width:100%}}'
            f'td,th{{border:1px solid #e9e5f0;padding:8px;text-align:left}}blockquote{{margin:20px 0;padding:12px 16px;'
            f'border-left:4px solid #7b2cff;background:#f3eefc}}</style>'
            f'<h1>{html.escape(artikel["title"])}</h1><p><em>{html.escape(artikel["excerpt"])}</em></p>{isi}',
            encoding="utf-8")
        kata = len(re.sub(r"<[^>]+>", " ", isi).split())
        print(f'  {p["slug"]:<32} → /blog{p["slug"]:<32} {kata:>4} kata, {len(gambar)} gambar, {len(faq)} FAQ')
    print(f"\nOK — hasil di {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
