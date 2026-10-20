#!/usr/bin/env python3
"""Render infografis HTML (1600x900) menjadi JPG siap unggah, lewat Chrome headless.

  python3 render_infografis.py --src <folder html> --out <folder hasil> [--nama a.html=nama-seo.jpg ...]

- Setiap *.html di --src dirender ke PNG lalu dikonversi ke JPG (Pillow kualitas 86, atau `sips` di macOS bila Pillow tidak ada).
  Tanpa --nama, file JPG memakai nama HTML-nya.
- Folder --src harus berisi base.css + font (salin dari assets/infografis skill ini).
- Chrome dicari di env CHROME, lalu lokasi standar macOS/Linux.
"""
import argparse, glob, os, shutil, subprocess, sys

CANDIDATES = [os.environ.get("CHROME", ""),
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or ""]

def chrome():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    sys.exit("Chrome/Chromium tidak ditemukan. Set env CHROME ke path-nya.")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--nama", nargs="*", default=[], help="pemetaan file.html=nama-file-seo.jpg")
    ap.add_argument("--lebar", type=int, default=1600); ap.add_argument("--tinggi", type=int, default=900)
    a = ap.parse_args()
    nama = dict(x.split("=", 1) for x in a.nama)
    src, out = os.path.abspath(a.src), os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    exe = chrome()
    files = sorted(glob.glob(os.path.join(src, "*.html")))
    if not files:
        sys.exit("Tidak ada file .html di --src")
    for f in files:
        base = os.path.basename(f)
        png = os.path.join(out, base[:-5] + ".png")
        jpg = os.path.join(out, nama.get(base, base[:-5] + ".jpg"))
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={a.lebar},{a.tinggi}", f"--screenshot={png}", "file://" + f],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        try:   # Pillow menghasilkan file ±40% lebih kecil; sips (macOS) sebagai cadangan
            from PIL import Image
            Image.open(png).convert("RGB").save(jpg, quality=86, optimize=True, progressive=True)
        except ImportError:
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", png, "--out", jpg],
                           stdout=subprocess.DEVNULL, check=True)
        os.remove(png)
        print(f"{base:<34} -> {os.path.basename(jpg)}  ({os.path.getsize(jpg)//1024} KB)")
    print("Selesai. WAJIB lihat setiap JPG: teks tidak terpotong, tidak ada ruang kosong janggal.")

if __name__ == "__main__":
    main()
