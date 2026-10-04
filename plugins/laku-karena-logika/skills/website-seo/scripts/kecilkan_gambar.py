#!/usr/bin/env python3
"""Kecilkan gambar dari user (PNG/JPG/WebP, boleh transparan) jadi WebP ≤ ±180 KB untuk website.
Butuh Pillow; bila belum ada, buat venv sementara:  python3 -m venv /tmp/venv-img && /tmp/venv-img/bin/pip install pillow
Pakai:  /tmp/venv-img/bin/python kecilkan_gambar.py <masuk> <keluar.webp> [lebar=1100]
Lebar 1100 px = 2× lebar tampil kolom media (±532 px), tajam di layar retina."""
import os
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
lebar = int(sys.argv[3]) if len(sys.argv) > 3 else 1100
im = Image.open(src).convert("RGBA")
if im.width > lebar:
    im = im.resize((lebar, round(im.height * lebar / im.width)), Image.LANCZOS)
for q in (82, 78, 72, 66, 60):
    im.save(dst, "WEBP", quality=q, method=6)
    kb = os.path.getsize(dst) / 1024
    if kb <= 180:
        break
print(f"{im.width}x{im.height} · {kb:.0f} KB · quality {q} → isi ilustrasi.json: auto false, file, w {im.width}, h {im.height}")
