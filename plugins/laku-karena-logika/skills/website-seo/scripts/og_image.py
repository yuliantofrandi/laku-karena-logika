#!/usr/bin/env python3
"""Buat gambar pratinjau link (og:image) 1200×630 dari site.json → static/og-image.png.

Isi: nama brand, tagline, deskripsi, dan warna design system (ilustrasi_warna).
Render PNG memakai alat bawaan macOS (qlmanage + sips). Di OS lain, file SVG-nya
tetap dibuat (static/og-image.svg) dan bisa dikonversi manual ke PNG/JPG.

Pemakaian (dari folder website):  python3 tools/og_image.py
Lalu isi site.json → "og_image": "static/og-image.png".
"""
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])


def svg(S):
    c = {"p": "#7B2CFF", "k": "#E83AAE", "o": "#FF8A00", "ink": "#1b1626"}
    c.update(S.get("ilustrasi_warna") or {})
    e = html.escape
    tag = "".join(f'<tspan x="80" dy="{0 if i == 0 else 78}">{e(l)}</tspan>' for i, l in enumerate(wrap(S["tagline"], 26)[:2]))
    desc = "".join(f'<tspan x="80" dy="{0 if i == 0 else 40}">{e(l)}</tspan>' for i, l in enumerate(wrap(S["description"], 60)[:2]))
    # kanvas persegi 1200×1200 dengan desain 1200×630 di tengah → qlmanage merender persegi, lalu di-crop tengah
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 -285 1200 1200">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{c["p"]}"/><stop offset=".52" stop-color="{c["k"]}"/><stop offset="1" stop-color="{c["o"]}"/></linearGradient></defs>
<rect x="0" y="-285" width="1200" height="1200" fill="{c["ink"]}"/>
<rect x="0" y="0" width="1200" height="630" fill="{c["ink"]}"/>
<circle cx="1080" cy="80" r="260" fill="{c["p"]}" opacity=".25"/><circle cx="1150" cy="560" r="200" fill="{c["o"]}" opacity=".18"/>
<text x="80" y="130" font-family="Arial,Helvetica,sans-serif" font-size="56" font-weight="700" font-style="italic" fill="url(#g)">{e(S["brand"].upper())}</text>
<text x="80" y="290" font-family="Arial,Helvetica,sans-serif" font-size="68" font-weight="700" fill="#fff">{tag}</text>
<text x="80" y="480" font-family="Arial,Helvetica,sans-serif" font-size="30" fill="#d9d1ea">{desc}</text>
<rect x="80" y="560" width="300" height="10" rx="5" fill="url(#g)"/>
</svg>'''


def main():
    S = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    out_svg = ROOT / "static" / "og-image.svg"
    out_svg.write_text(svg(S), encoding="utf-8")
    if not (shutil.which("qlmanage") and shutil.which("sips")):
        sys.exit(f"SVG dibuat di {out_svg}. qlmanage/sips tidak ada (bukan macOS): konversi manual ke PNG 1200×630.")
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["qlmanage", "-t", "-s", "1200", "-o", tmp, str(out_svg)], capture_output=True, check=True)
        png = Path(tmp) / (out_svg.name + ".png")
        subprocess.run(["sips", "--cropToHeightWidth", "630", "1200", str(png)], capture_output=True, check=True)
        dest = ROOT / "static" / "og-image.png"
        shutil.copy(png, dest)
    out_svg.unlink()
    print(f"og:image dibuat: {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
