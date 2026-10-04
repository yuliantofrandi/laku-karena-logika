#!/usr/bin/env python3
"""Render animasi HTML deterministik (window.render(t) + window.DUR) jadi video.

Pakai:
  python3 render.py <file.html> <output_basename> --size 1080x1920 [--fps 30] [--snap 2,6.5,12]

Hasil:
  <output_basename>.mp4          bahan H.264 resolusi penuh (sementara — hasil ekspor dibuat web_optimize.py)
  <output_basename>-snap-<t>.png (opsional --snap) frame cek kualitas sementara, bukan hasil ekspor

Syarat HTML: memanggil render(0) bila URL berisi '?rec', dan mengekspos window.render & window.DUR.
"""
import argparse, subprocess, sys, os
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("html"); ap.add_argument("out")
ap.add_argument("--size", default="1080x1920")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--snap", default=None, help="hanya ambil frame PNG di detik-detik ini (koma), tanpa render video")
a = ap.parse_args()
W, H = map(int, a.size.lower().split("x"))
url = "file://" + os.path.abspath(a.html) + "?rec"
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto(url); pg.wait_for_timeout(400)
    dur = pg.evaluate("window.DUR")
    if a.snap:
        for t in [float(x) for x in a.snap.split(",")]:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{a.out}-snap-{t}.png")
        b.close(); sys.exit(0)
    mp4 = a.out + ".mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-f", "image2pipe", "-framerate", str(a.fps), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                           "-movflags", "+faststart", mp4], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = int(round(dur * a.fps))
    for i in range(n):
        pg.evaluate(f"render({i / a.fps})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=95))
    ff.stdin.close(); ff.wait()
    b.close()

print(f"OK {mp4} ({dur}s, {n} frame, {W}x{H})")
