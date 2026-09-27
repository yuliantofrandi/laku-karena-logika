#!/usr/bin/env python3
"""Render artboard .dc.html kanvas Design jadi JPEG 9:16 + crop 4:5, dalam satu langkah.

Pemakaian:
  python3 render.py --src <folder berisi project/*.dc.html> \
      --boards B1-Hook,B2-Konteks,... --names 01-hook,02-mulai-kecil,... \
      --out <folder output> [--blob <id>=<path> ...]

Hasil:
  <out>/9x16-tiktok-threads/NN-nama.jpg   (1080 x 1920)
  <out>/4x5-instagram/NN-nama.jpg         (1080 x 1350, crop y 285-1635)
  <out>/contact.png                       (lembar kontak untuk dicek visual)
  Laporan per frame: font termuat, batas konten di dalam zona 4:5.

Aset /_blob/:
  - <img alt="Venturo..."> otomatis diganti logo bundel (assets/logo-venturo.png)
  - url(/_blob/..) di aturan .bgpat otomatis diganti pola bundel (assets/background-venturo.jpg)
  - /_blob/ lain wajib dipetakan lewat --blob id=path (unduh dengan Artifact read path=<id>)
Font: @font-face lokal dari assets/fonts (Google Fonts diblokir proxy).
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
FONTS = os.path.join(ASSETS, "fonts")
LOGO = os.path.join(ASSETS, "logo-venturo.png")
BG = os.path.join(ASSETS, "background-venturo.jpg")
W, H, Y0, Y1 = 1080, 1920, 285, 1635


def font_css():
    css = []
    for w in (400, 500, 600, 700, 800):
        for s in ("normal", "italic"):
            css.append(f"@font-face{{font-family:Montserrat;font-weight:{w};font-style:{s};"
                       f"src:url(file://{FONTS}/montserrat-latin-{w}-{s}.woff2)}}")
    for w in (400, 600):
        css.append(f"@font-face{{font-family:'JetBrains Mono';font-weight:{w};"
                   f"src:url(file://{FONTS}/jetbrains-mono-latin-{w}-normal.woff2)}}")
    return "".join(css)


def convert(src_html, blobs):
    t = open(src_html, encoding="utf-8").read()
    m_h = re.search(r"<helmet>(.*?)</helmet>", t, re.S)
    helm = m_h.group(1) if m_h else ""
    helm = re.sub(r"<link[^>]*fonts\.(googleapis|gstatic)[^>]*>", "", helm)
    body = re.search(r"<x-dc>(.*?)</x-dc>", t, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
    if "{{" in body:
        print(f"PERINGATAN {os.path.basename(src_html)}: ada {{{{hole}}}} — frame dinamis tidak didukung", file=sys.stderr)
    # logo & pola latar bundel
    body = re.sub(r'(<img[^>]*?)src="/_blob/[0-9a-f]+"([^>]*alt="Venturo)', rf'\1src="file://{LOGO}"\2', body)
    body = re.sub(r'(<img[^>]*alt="Venturo[^"]*"[^>]*?)src="/_blob/[0-9a-f]+"', rf'\1src="file://{LOGO}"', body)
    helm = re.sub(r"(\.bgpat\{[^}]*?)url\(/_blob/[0-9a-f]+\)", rf"\1url(file://{BG})", helm)
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}</style>{helm}</head><body>{body}</body></html>'
    for k, v in blobs.items():
        html = html.replace(f"/_blob/{k}", f"file://{os.path.abspath(v)}")
    left = sorted(set(re.findall(r"/_blob/([0-9a-f]+)", html)))
    if left:
        sys.exit(f"GAGAL {os.path.basename(src_html)}: aset belum dipetakan: {left} (pakai --blob id=path)")
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder kanvas (berisi project/ atau langsung *.dc.html)")
    ap.add_argument("--boards", required=True, help="nama artboard tanpa .dc.html, dipisah koma, sesuai urutan slide")
    ap.add_argument("--names", required=True, help="nama file output tanpa .jpg, dipisah koma, jumlah sama dengan --boards")
    ap.add_argument("--out", required=True)
    ap.add_argument("--blob", action="append", default=[], help="id=path untuk aset /_blob/ lain")
    a = ap.parse_args()
    boards = [b.strip() for b in a.boards.split(",") if b.strip()]
    names = [n.strip() for n in a.names.split(",") if n.strip()]
    if len(boards) != len(names):
        sys.exit("--boards dan --names harus sama jumlahnya")
    blobs = dict(x.split("=", 1) for x in a.blob)
    src = os.path.join(a.src, "project") if os.path.isdir(os.path.join(a.src, "project")) else a.src
    tmp = os.path.join(a.out, "_html")
    d916 = os.path.join(a.out, "9x16-tiktok-threads")
    d45 = os.path.join(a.out, "4x5-instagram")
    for d in (tmp, d916, d45):
        os.makedirs(d, exist_ok=True)

    from playwright.sync_api import sync_playwright
    from PIL import Image

    probe = """()=>{const root=document.body.querySelector(':scope > div');
      let t=1e9,b=0; root.querySelectorAll('*').forEach(e=>{
        const bg=e.closest('[aria-hidden=true]'); if(bg&&bg.parentElement===root) return;
        let p=e.parentElement, clipped=false; while(p&&p!==root){ if(getComputedStyle(p).overflow==='hidden'){clipped=true;break} p=p.parentElement }
        if(clipped) return; const r=e.getBoundingClientRect(); if(r.width&&r.height){t=Math.min(t,r.top);b=Math.max(b,r.bottom)}});
      const fonts=[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family);
      return {top:Math.round(t), bottom:Math.round(b), montserrat: fonts.some(f=>f.includes('Montserrat'))}}"""
    ok = True
    thumbs = []
    exe = "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"])
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for bd, nm in zip(boards, names):
            f = os.path.join(src, bd + ".dc.html")
            hp = os.path.join(tmp, bd + ".html")
            open(hp, "w", encoding="utf-8").write(convert(f, blobs))
            pg.goto("file://" + os.path.abspath(hp))
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            r = pg.evaluate(probe)
            png = os.path.join(tmp, nm + ".png")
            pg.screenshot(path=png, clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(png).convert("RGB")
            im.save(os.path.join(d916, nm + ".jpg"), quality=95, subsampling=0)
            c = im.crop((0, Y0, W, Y1))
            c.save(os.path.join(d45, nm + ".jpg"), quality=95, subsampling=0)
            thumbs.append((im.resize((270, 480)), c.resize((270, 338))))
            zone = Y0 <= r["top"] and r["bottom"] <= Y1
            ok = ok and zone and r["montserrat"]
            print(f"{nm}: konten y {r['top']}–{r['bottom']} {'OK' if zone else 'KELUAR ZONA 285–1635'}; "
                  f"Montserrat {'termuat' if r['montserrat'] else 'TIDAK termuat'}")
        br.close()
    sheet = Image.new("RGB", (280 * len(thumbs), 830), "gray")
    for i, (a9, a4) in enumerate(thumbs):
        sheet.paste(a9, (i * 280, 0))
        sheet.paste(a4, (i * 280, 490))
    sheet.save(os.path.join(a.out, "contact.png"))
    print("lembar kontak:", os.path.join(a.out, "contact.png"))
    print("SEMUA OK" if ok else "ADA MASALAH — cek baris di atas sebelum posting")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
