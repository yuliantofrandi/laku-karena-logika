#!/usr/bin/env python3
"""Infografis artikel Blog (1600×900 PNG) bergaya artikel acuan /blog/kerja-wfa-profesional.

Pola visual (disetujui user sebagai acuan):
  - latar putih dengan gradasi lembut ungu (kanan atas) & peach (kiri bawah)
  - label kecil ungu huruf kapital dengan garis gradasi di depannya
  - judul besar Montserrat 800, kata terakhir yang disorot memakai gradasi brand
  - isi: kartu berikon, perbandingan ✗/✓, alur bertahap, atau dua kolom
  - footer: logo + "ACCOUNTABILITY EVERYWHERE" di kiri, keterangan kecil di kanan

Spesifikasi ditulis sebagai JSON (lihat export/blog-v2/infografis.json):
  {"id": "...", "tipe": "kartu|banding|alur|dua", "label": "...", "judul": "...", "sorot": "kata di judul",
   "sub": "opsional", "catatan": "teks footer kanan", ...isi per tipe}

Render memakai Google Chrome headless (font Montserrat dari static/fonts).
Pemakaian:  python3 tools/infografis.py export/blog-v2/infografis.json export/blog-v2/gambar
"""
import base64
import html
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

IKON = {  # ikon garis 24×24
    "cek": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
    "jam": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "timer": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2"/><path d="M10 2h4"/>',
    "tugas": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 12l3 3 5-6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v4"/><path d="M12 17.5h.01"/>',
    "kalender": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "dok": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="M8 13h8M8 17h5"/>',
    "tanda": '<path d="M3 17c3 0 4-6 6-6s1 6 4 6 3-3 5-3"/><path d="M3 21h18"/>',
    "mata": '<path d="M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7z"/><circle cx="12" cy="12" r="3"/>',
    "hapus": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
    "arsip": '<rect x="3" y="4" width="18" height="5" rx="1"/><path d="M5 9v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9"/><path d="M10 13h4"/>',
    "lonceng": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "perisai": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "kunci": '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "orang": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
    "aktivitas": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18"/>',
    "kamera": '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
    "grafik": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "timbang": '<path d="M12 3v18M7 21h10"/><path d="M5 7h14"/><path d="M5 7l-3 6a3 3 0 0 0 6 0z"/><path d="M19 7l-3 6a3 3 0 0 0 6 0z"/>',
    "kilat": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.5 7.2L4 20l1-4.5A8 8 0 1 1 21 12z"/>',
    "gedung": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>',
    "dompet": '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18M16 15h2"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "lokasi": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "kirim": '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
    "rekap": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
}


def svg(nama, w=26, warna="currentColor", tebal=2):
    return (f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="{warna}" stroke-width="{tebal}" '
            f'stroke-linecap="round" stroke-linejoin="round">{IKON.get(nama, IKON["cek"])}</svg>')


def e(t):
    return html.escape(str(t))


def judul(s):
    j, sorot = e(s["judul"]), s.get("sorot")
    if sorot and e(sorot) in j:
        j = j.replace(e(sorot), f'<span class="g">{e(sorot)}</span>', 1)
    return j


def isi_kartu(s):
    k = s["kartu"]
    return '<div class="kartu" style="grid-template-columns:repeat(%d,1fr)">' % len(k) + "".join(
        f'<div class="k"><span class="ik">{svg(x.get("ikon", "cek"))}</span>'
        + (f'<p class="kl">{e(x["label"])}</p>' if x.get("label") else "")
        + f'<h3>{e(x["judul"])}</h3><p class="kd">{e(x["isi"])}</p>'
        + (f'<span class="pill">{e(x["tag"])}</span>' if x.get("tag") else "") + "</div>" for x in k) + "</div>"


def isi_banding(s):
    def kol(c, jenis):
        ik = svg("x" if jenis == "buruk" else "cek", 22, "#fff", 3) if jenis in ("buruk", "baik") else svg(c.get("ikon", "cek"), 22, "#fff", 2.4)
        baris = "".join(f'<div class="b {jenis}"><span class="no">{i}</span><div><strong>{e(r[0])}</strong>'
                        + (f'<span>{e(r[1])}</span>' if len(r) > 1 and r[1] else "") + "</div></div>"
                        for i, r in enumerate(c["baris"], 1))
        return f'<div class="kol"><h3><span class="bul {jenis}">{ik}</span>{e(c["judul"])}</h3>{baris}</div>'
    a, b = s["kiri"], s["kanan"]
    return f'<div class="banding">{kol(a, a.get("jenis", "buruk"))}{kol(b, b.get("jenis", "baik"))}</div>'


def isi_alur(s):
    n = len(s["langkah"])
    titik = "".join(f'<span class="t" style="--c:{c}">{i}</span>' for i, c in enumerate(warna_alur(n), 1))
    kartu = "".join(
        f'<div class="ak{" wajib" if x.get("wajib") else ""}">'
        + (f'<span class="badge">{e(x["wajib"])}</span>' if x.get("wajib") else "")
        + (f'<p class="aw">{e(x["waktu"])}</p>' if x.get("waktu") else "")
        + f'<h3>{e(x["judul"])}</h3><ul>' + "".join(f"<li>{e(p)}</li>" for p in x["poin"]) + "</ul></div>"
        for x in s["langkah"])
    return (f'<div class="alur" style="--n:{n}"><div class="garis">{titik}</div>'
            f'<div class="akol" style="grid-template-columns:repeat({n},1fr)">{kartu}</div></div>')


def warna_alur(n):
    stops = [(0x7B, 0x2C, 0xFF), (0xE8, 0x3A, 0xAE), (0xFF, 0x8A, 0x00)]
    out = []
    for i in range(n):
        t = i / max(1, n - 1) * 2
        a, b = stops[min(int(t), 1)], stops[min(int(t), 1) + 1]
        f = t - min(int(t), 1)
        out.append("#%02x%02x%02x" % tuple(round(a[j] + (b[j] - a[j]) * f) for j in range(3)))
    return out


def isi_dua(s):
    """Dua kolom fitur berdampingan (mis. HRIS vs monitoring aktivitas), baris sejajar."""
    ka, kb = s["kiri"], s["kanan"]
    kepala = (f'<div></div><div class="dh"><span class="bul netral">{svg(ka.get("ikon", "gedung"), 22, "#fff")}</span>{e(ka["judul"])}</div>'
              f'<div class="dh"><span class="bul">{svg(kb.get("ikon", "laptop"), 22, "#fff")}</span>{e(kb["judul"])}</div>')
    baris = "".join(f'<div class="dr">{e(r[0])}</div><div class="dc">{e(r[1])}</div><div class="dc kuat">{e(r[2])}</div>'
                    for r in s["baris"])
    return f'<div class="dua">{kepala}{baris}</div>'


CSS = """
@font-face{font-family:Montserrat;font-weight:800;src:url(data:font/woff2;base64,%(font)s) format('woff2')}
*{box-sizing:border-box}html,body{margin:0}
body{width:1600px;height:900px;overflow:hidden;font-family:-apple-system,"SF Pro Text","Segoe UI",system-ui,sans-serif;color:#1b1626;
 background:radial-gradient(900px 600px at 105%% -10%%,#efe6ff 0%%,rgba(239,230,255,0) 60%%),radial-gradient(800px 520px at -8%% 108%%,#ffeedd 0%%,rgba(255,238,221,0) 60%%),#fff}
.wrap{position:absolute;inset:0;padding:72px 88px 0}
.label{display:flex;align-items:center;gap:12px;margin:0 0 14px;color:#7B2CFF;font-weight:800;font-size:20px;letter-spacing:.09em;text-transform:uppercase}
.label:before{content:"";width:34px;height:4px;border-radius:4px;background:linear-gradient(90deg,#7B2CFF,#E83AAE,#FF8A00)}
h1{margin:0;font-family:Montserrat;font-weight:800;font-size:60px;line-height:1.08;letter-spacing:-.025em;max-width:1420px}
.g{background:linear-gradient(90deg,#7B2CFF,#E83AAE 55%%,#FF8A00);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin:16px 0 0;font-size:24px;line-height:1.45;color:#4a4458;max-width:1320px}
.isi{position:absolute;left:88px;right:88px;top:var(--top,300px);bottom:120px;display:flex;flex-direction:column;justify-content:var(--jc,center)}
.foot{position:absolute;left:88px;right:88px;bottom:58px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:16px}.brand img{height:28px}
.brand span{font-weight:700;font-size:16px;letter-spacing:.22em;color:#4a4458}
.cat{font-size:19px;color:#4a4458}
/* kartu */
.kartu{display:grid;gap:26px}
.k{position:relative;display:flex;flex-direction:column;align-items:flex-start;background:#fff;border:1.5px solid #ece7f4;border-radius:24px;padding:30px 28px 28px;box-shadow:0 22px 44px -32px rgba(60,20,120,.35);overflow:hidden}
.k:before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:linear-gradient(90deg,#7B2CFF,#E83AAE,#FF8A00)}
.ik{display:grid;place-items:center;width:64px;height:64px;border-radius:50%%;background:linear-gradient(135deg,#7B2CFF,#E83AAE 60%%,#FF8A00);color:#fff;margin-bottom:22px;box-shadow:0 12px 24px -12px rgba(123,44,255,.6)}
.kl{margin:0 0 6px;color:#7B2CFF;font-weight:800;font-size:17px;letter-spacing:.08em;text-transform:uppercase}
.k h3{margin:0 0 12px;font-family:Montserrat;font-weight:800;font-size:29px;line-height:1.15;letter-spacing:-.01em}
.kd{margin:0 0 18px;font-size:20px;line-height:1.5;color:#4a4458}
.pill{display:inline-block;margin-top:auto;padding:6px 14px;border-radius:999px;background:#f1eaff;color:#6a22e6;font-weight:700;font-size:16px}
/* banding */
.banding{display:grid;grid-template-columns:1fr 1fr;gap:30px}
.kol h3{display:flex;align-items:center;gap:14px;margin:0 0 18px;font-family:Montserrat;font-weight:800;font-size:27px}
.bul{display:grid;place-items:center;width:42px;height:42px;border-radius:50%%;background:linear-gradient(135deg,#7B2CFF,#E83AAE 60%%,#FF8A00)}
.bul.buruk{background:#e5484d}.bul.baik{background:#1fa463}.bul.netral{background:#5f5870}
.b{display:flex;gap:16px;align-items:flex-start;margin-bottom:14px;padding:18px 22px;border-radius:18px;border:1.5px solid}
.b.buruk{background:#fff5f5;border-color:#f7dada}.b.baik{background:#f1fbf5;border-color:#d3efdf}.b.netral{background:#faf9fc;border-color:#ece7f4}.b.plus{background:#f6f1ff;border-color:#e3d6fb}
.no{flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%%;font-weight:800;font-size:16px;margin-top:2px}
.buruk .no{background:#fde3e3;color:#c4282d}.baik .no{background:#d9f3e4;color:#16804c}.netral .no{background:#ece7f4;color:#4a4458}.plus .no{background:#e8dcff;color:#6a22e6}
.b strong{display:block;font-size:22px;line-height:1.3}.b span{display:block;margin-top:3px;font-size:19px;line-height:1.4;color:#4a4458}
/* alur */
.garis{position:relative;display:grid;grid-template-columns:repeat(var(--n),1fr);margin:0 0 26px}
.garis:before{content:"";position:absolute;left:calc(50%%/var(--n) - 30px);right:calc(50%%/var(--n) - 30px);top:50%%;height:6px;transform:translateY(-50%%);border-radius:6px;background:linear-gradient(90deg,#7B2CFF,#E83AAE 55%%,#FF8A00)}
.t{position:relative;justify-self:center;display:grid;place-items:center;width:66px;height:66px;border-radius:50%%;background:#fff;border:6px solid var(--c);color:var(--c);font-family:Montserrat;font-weight:800;font-size:26px}
.akol{display:grid;gap:20px;align-items:stretch}
.ak{position:relative;background:#fff;border:1.5px solid #ece7f4;border-radius:22px;padding:24px 22px 20px;box-shadow:0 22px 44px -32px rgba(60,20,120,.35)}
.ak.wajib{border:2.5px solid #7B2CFF;background:#fbf8ff}
.badge{display:inline-block;margin-bottom:10px;padding:4px 12px;border-radius:999px;background:#7B2CFF;color:#fff;font-weight:800;font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.aw{margin:0 0 6px;font-family:Montserrat;font-weight:800;font-size:19px;color:#7B2CFF}
.ak h3{margin:0 0 12px;font-family:Montserrat;font-weight:800;font-size:24px;line-height:1.2}
.ak ul{margin:0;padding:0;list-style:none}.ak li{position:relative;padding-left:20px;margin:7px 0;font-size:18.5px;line-height:1.4;color:#4a4458}
.ak li:before{content:"";position:absolute;left:2px;top:9px;width:8px;height:8px;border-radius:50%%;background:#7B2CFF}
/* dua kolom */
.dua{display:grid;grid-template-columns:300px 1fr 1fr;border:1.5px solid #ece7f4;border-radius:24px;background:#fff;overflow:hidden;box-shadow:0 22px 44px -32px rgba(60,20,120,.35)}
.dh{display:flex;align-items:center;gap:14px;padding:22px 26px;font-family:Montserrat;font-weight:800;font-size:26px;border-bottom:2px solid #1b1626}
.dua>div:first-child{border-bottom:2px solid #1b1626}
.dr,.dc{padding:17px 26px;font-size:20px;line-height:1.4;border-top:1px solid #f0ecf6}
.dr{font-weight:800;color:#1b1626}.dc{color:#4a4458}.dc.kuat{color:#1b1626;font-weight:600;background:#fbf8ff}
.dh+.dh{background:#fbf8ff}
"""


def halaman(s, logo_b64, font_b64):
    tipe = s["tipe"]
    isi = {"kartu": isi_kartu, "banding": isi_banding, "alur": isi_alur, "dua": isi_dua}[tipe](s)
    top = s.get("top") or (330 if s.get("sub") else 250)
    jc = "flex-start" if tipe == "kartu" else "center"
    if tipe == "kartu" and not s.get("top"):
        top = 300 if s.get("sub") else 240
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS % {"font": font_b64}}</style></head><body>'
            f'<div class="wrap"><p class="label">{e(s["label"])}</p><h1>{judul(s)}</h1>'
            + (f'<p class="sub">{e(s["sub"])}</p>' if s.get("sub") else "")
            + f'</div><div class="isi" style="--top:{top}px;--jc:{jc}">{isi}</div>'
            f'<div class="foot"><div class="brand"><img src="data:image/png;base64,{logo_b64}" alt=""><span>ACCOUNTABILITY EVERYWHERE</span></div>'
            f'<div class="cat">{e(s.get("catatan", ""))}</div></div></body></html>')


def main():
    spek, keluar = Path(sys.argv[1]), Path(sys.argv[2])
    pilih = set(sys.argv[3:])
    keluar.mkdir(parents=True, exist_ok=True)
    logo = base64.b64encode((ROOT / "static" / "logo-timebase.png").read_bytes()).decode()
    font = base64.b64encode((ROOT / "static" / "fonts" / "montserrat-latin-800-normal.woff2").read_bytes()).decode()
    with tempfile.TemporaryDirectory() as t:
        for s in json.loads(spek.read_text(encoding="utf-8")):
            if pilih and s["id"] not in pilih:
                continue
            f = Path(t) / f'{s["id"]}.html'
            f.write_text(halaman(s, logo, font), encoding="utf-8")
            png = keluar / f'{s["id"]}.png'
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1600,900", f"--screenshot={png}", f.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("  ", png.relative_to(ROOT) if png.is_relative_to(ROOT) else png)


if __name__ == "__main__":
    main()
