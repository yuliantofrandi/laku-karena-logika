#!/usr/bin/env python3
"""Ubah video master (hasil render.py) jadi SATU file MP4 ringan untuk website yang lolos PageSpeed.

Pakai:
  python3 web_optimize.py master.mp4 <folder_output> <slug> [--poster 6.8]
         [--title "..."] [--desc "..."] [--domain https://contoh.id] [--path /media/]

<slug> = nama file berkata kunci, mis. aplikasi-monitoring-karyawan-wfa-demo

Hasil: <folder_output>/<slug>.mp4 saja — 720p (atau 720x1280 untuk 9:16), 24 fps, H.264, tanpa audio,
faststart. Snippet embed dicetak ke layar (bukan file): <video preload="none"> dengan poster frame pratinjau
yang DITANAM di HTML (data URI WebP kecil) -> tidak ada file gambar tambahan dan tidak ada byte video yang
diunduh sebelum pengunjung klik putar.
"""
import argparse, base64, io, json, os, subprocess, sys
from PIL import Image

BUDGET = 3_000_000  # byte

ap = argparse.ArgumentParser()
ap.add_argument("master"); ap.add_argument("outdir"); ap.add_argument("slug")
ap.add_argument("--poster", type=float, default=None, help="detik frame pratinjau (default 30%% durasi)")
ap.add_argument("--title", default="Demo aplikasi"); ap.add_argument("--desc", default="")
ap.add_argument("--domain", default="https://[domain]"); ap.add_argument("--path", default="/media/")
ap.add_argument("--fps", type=int, default=24)
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
out = os.path.join(a.outdir, a.slug + ".mp4")

r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                    "stream=width,height:format=duration", "-of", "json", a.master], capture_output=True, text=True)
j = json.loads(r.stdout); W, H = j["streams"][0]["width"], j["streams"][0]["height"]; DUR = float(j["format"]["duration"])
tw, th = (720, 1280) if H > W else (1280, 720)
pt = a.poster if a.poster is not None else round(DUR * 0.3, 2)

crf = 30
for _ in range(5):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.master, "-vf", f"scale={tw}:{th}:flags=lanczos,fps={a.fps}",
                    "-an", "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", str(crf),
                    "-pix_fmt", "yuv420p", "-profile:v", "high", 
                    "-movflags", "+faststart", out], check=True)
    size = os.path.getsize(out)
    if size <= BUDGET: break
    crf += 3

png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(pt), "-i", out, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                     capture_output=True, check=True).stdout
im = Image.open(io.BytesIO(png)).convert("RGB")
q = 72
while True:  # resolusi penuh dulu; turunkan kualitas, lalu resolusi, sampai <= 35 KB
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    if buf.tell() <= 35_000: break
    if q > 45: q -= 9
    else: im = im.resize((im.width * 3 // 4, im.height * 3 // 4), Image.LANCZOS); q = 72
poster = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
P = a.path.rstrip("/") + "/"
ld = {"@context": "https://schema.org", "@type": "VideoObject", "name": a.title,
      "description": a.desc or a.title, "thumbnailUrl": "[URL gambar thumbnail — wajib untuk rich result video Google]",
      "uploadDate": "[YYYY-MM-DD]", "duration": f"PT{int(round(DUR))}S", "contentUrl": f"{a.domain}{P}{a.slug}.mp4"}
snippet = f"""<!-- Video {a.slug}: hanya MP4. Pratinjau = poster yang ditanam (data URI); video tidak diunduh sampai tombol putar diklik. -->
<figure class="vmp4" style="position:relative;margin:0;aspect-ratio:{tw}/{th};max-width:{tw}px;width:100%;border-radius:16px;overflow:hidden;background:#f4f6f8">
  <video src="{P}{a.slug}.mp4" preload="none" muted playsinline poster="{poster}" width="{tw}" height="{th}"
         aria-label="{a.title}" style="width:100%;height:100%;object-fit:cover;display:block"></video>
  <button type="button" aria-label="Putar video: {a.title}"
          style="position:absolute;inset:0;margin:auto;width:76px;height:76px;border-radius:50%;border:0;background:rgba(28,37,46,.78);cursor:pointer">
    <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
  </button>
</figure>
<script>
document.querySelectorAll('.vmp4 button').forEach(function(b){{b.addEventListener('click',function(){{
  var v=b.parentNode.querySelector('video');v.controls=true;v.preload='auto';v.play();b.remove();}});}});
</script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>"""

print(f"Poster tertanam: {len(poster)/1024:.0f} KB (WebP q{q})")
print(f"OK {out}\n  {W}x{H} {DUR:.1f}s -> {tw}x{th} @{a.fps}fps, CRF {crf}, {size/1024:.0f} KB (batas {BUDGET/1024:.0f} KB) "
      + ("LOLOS" if size <= BUDGET else "LEWAT ANGGARAN"))
print("\n===== SNIPPET EMBED (tempel ke halaman) =====\n" + snippet)
sys.exit(0 if size <= BUDGET else 2)
