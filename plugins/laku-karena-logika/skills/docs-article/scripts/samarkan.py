#!/usr/bin/env python3
"""Samarkan screenshot panduan sebelum diposting ke CMS.

Dua langkah:
  1. ocr       — baca semua teks di gambar (Vision macOS), tandai gambar placeholder,
                 tulis daftar teks per gambar untuk menyusun peta penyamaran.
  2. terapkan  — ganti nama asli -> nama dummy (font & ukuran menyesuaikan teks asli),
                 ganti email, blur 4 digit terakhir nomor telepon yang terbaca,
                 dan blur area manual dari peta. Foto profil TIDAK diblur.

Contoh:
  python3 samarkan.py ocr --src <folder gambar> --kerja <folder kerja>
  python3 samarkan.py terapkan --src <folder gambar> --kerja <folder kerja> \
      --peta <folder kerja>/peta.json --out <folder hasil>

Format peta.json:
  {
    "nama":      {"Nama Asli Lengkap": "Nama Dummy", ...},
    "alias_ocr": {"Teks salah baca OCR": "Nama Asli Lengkap", ...},
    "email":     {"asli@domain.com": "dummy@contoh.id", ...},
    "blur":      {"25-daftar-user.jpg": [[x0, y0, x1, y1], ...], ...}
  }
Butuh: macOS (swiftc + Vision), Python Pillow.
"""
import argparse, difflib, json, os, re, subprocess, sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = (".jpg", ".jpeg", ".png", ".webp")
PLACEHOLDER = re.compile(r"ganti dengan screenshot|placeholder|screenshot baru", re.I)
TIME = re.compile(r"\s*\d+\s?[j/i1]?\s?\d+\s?m\s*$")          # durasi "8j 20m" yang menempel di nama
PHONE = re.compile(r"(?:\+?62|0)\s?8[\d\s\-.]{7,14}\d")

FONT_DIRS = ["/System/Library/Fonts/Supplemental", "/Library/Fonts", "/usr/share/fonts/truetype/dejavu"]
def _font(names):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    sys.exit("Font tidak ditemukan (butuh Arial atau DejaVu Sans).")
BOLD = _font(["Arial Bold.ttf", "DejaVuSans-Bold.ttf"])
REG = _font(["Arial.ttf", "DejaVuSans.ttf"])

# ---------- OCR ----------
def ocr_bin(kerja):
    exe = os.path.join(kerja, "ocr-vision")
    if not os.path.exists(exe):
        subprocess.run(["swiftc", "-O", os.path.join(HERE, "ocr.swift"), "-o", exe], check=True)
    return exe

def images(src):
    return sorted(f for f in os.listdir(src) if f.lower().endswith(EXT))

def cmd_ocr(a):
    os.makedirs(os.path.join(a.kerja, "ocr"), exist_ok=True)
    exe = ocr_bin(a.kerja)
    ph, teks = [], []
    for f in images(a.src):
        out = subprocess.run([exe, os.path.join(a.src, f)], capture_output=True, text=True).stdout
        open(os.path.join(a.kerja, "ocr", f + ".tsv"), "w").write(out)
        lines = [l.split("\t")[5] for l in out.splitlines() if l.startswith("T\t")]
        if any(PLACEHOLDER.search(l) for l in lines):
            ph.append(f)
            continue
        teks.append(f"## {f}\n" + "\n".join(f"  {l}" for l in lines))
        for l in lines:
            if PHONE.search(l):
                teks.append(f"  !! nomor telepon terbaca: {l}")
    open(os.path.join(a.kerja, "teks.txt"), "w").write("\n".join(teks) + "\n")
    open(os.path.join(a.kerja, "placeholder.txt"), "w").write("\n".join(ph) + ("\n" if ph else ""))
    print(f"{len(images(a.src))} gambar, {len(ph)} placeholder (dilewati).")
    print(f"Teks per gambar: {a.kerja}/teks.txt  -> susun peta.json dari nama orang di sini.")

# ---------- pencocokan nama ----------
def norm(s):
    return re.sub(r"[^a-z]", "", s.lower().replace("l", "i"))

class Peta:
    def __init__(self, path):
        p = json.load(open(path))
        self.nama = p.get("nama", {})
        self.alias = p.get("alias_ocr", {})
        self.email = {k.lower(): v for k, v in p.get("email", {}).items()}
        self.blur = p.get("blur", {})
        self.nn = [(norm(k), k) for k in self.nama]

    def match(self, s):
        raw = s.strip()
        if raw in self.alias:
            real = self.alias[raw]
            return real, raw, False, False
        has_time = bool(TIME.search(raw))
        raw = TIME.sub("", raw)
        raw = re.sub(r"\s+[vO®•]$", "", raw).strip()
        trunc = "..." in raw or "…" in raw
        core = raw.replace("...", "").replace("…", "").strip()
        n = norm(core)
        if len(n) < 6:
            return None
        best = None
        for nk, k in self.nn:
            r = 1.0 if (nk.startswith(n) or n.startswith(nk)) else difflib.SequenceMatcher(None, n, nk[:len(n)]).ratio()
            if best is None or r > best[0]:
                best = (r, k)
        if best and best[0] >= 0.8:
            return best[1], core, trunc, has_time
        return None

    def dummy(self, real, core, trunc):
        d = self.nama[real]
        if not trunc and len(norm(core)) < len(norm(real)) - 1:
            d = d[:max(4, len(core))].rstrip()      # nama terpotong overlay/panel
        return d

# ---------- util piksel ----------
def diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

def bg_color(img, box):
    x, y, w, h = box
    px = [img.getpixel((xx, yy)) for xx in range(max(0, x - 3), min(img.width, x + w + 3))
          for yy in (max(0, y - 4), min(img.height - 1, y + h + 3))]
    px.sort(key=sum)
    return px[len(px) // 2]

def fg_color(img, box):
    x, y, w, h = box
    px = [img.getpixel((xx, yy)) for xx in range(x, min(img.width, x + w)) for yy in range(y, min(img.height, y + h))]
    px.sort(key=sum)
    return px[max(0, len(px) // 50)]

def ink_cols(img, box, bg):
    x, y, w, h = box
    return [any(diff(img.getpixel((xx, yy)), bg) > 90 for yy in range(y, min(img.height, y + h)))
            for xx in range(x, min(img.width, x + w))]

def ink_rows(img, box, bg):
    x, y, w, h = box
    return [any(diff(img.getpixel((xx, yy)), bg) > 90 for xx in range(x, min(img.width, x + w)))
            for yy in range(y, min(img.height, y + h))]

def split_time(img, box, bg):
    """Potong bagian durasi bila OCR menggabungkan nama + durasi."""
    x, y, w, h = box
    best, cur, start = (0, None), 0, None
    for i, c in enumerate(ink_cols(img, box, bg)):
        if not c:
            start = i if cur == 0 else start
            cur += 1
            if cur > best[0] and i > w * 0.4:
                best = (cur, start)
        else:
            cur = 0
    return box if best[1] is None else (x, y, best[1], h)

def first_line(img, box, bg):
    x, y, w, h = box
    rows = ink_rows(img, box, bg)
    if not any(rows):
        return box
    a = rows.index(True); b = a; gap = 0
    for i in range(a, len(rows)):
        if rows[i]:
            b, gap = i, 0
        else:
            gap += 1
            if gap > 1:
                break
    return (x, y + a - 1, w, b - a + 3)

def tight(img, box, bg):
    box = first_line(img, box, bg)
    x, y, w, h = box
    cols = ink_cols(img, box, bg)
    if not any(cols):
        return box
    l = cols.index(True); r = len(cols) - cols[::-1].index(True)
    return (x + l, y, r - l, h)

def avail_right(img, box, bg, limit=400):
    x, y, w, h = box
    start = x + w + 6
    for xx in range(start, min(img.width, start + limit)):
        if any(diff(img.getpixel((xx, yy)), bg) > 90 for yy in range(y, y + h)):
            return xx - x - 10
    return min(img.width - x - 8, w + limit)

# ---------- tulis ulang teks ----------
SNAP = []   # tinggi huruf kapital yang paling sering di gambar ini, agar ukuran seragam

def font_cap(cap_h, path):
    for c in SNAP:
        if abs(c - cap_h) <= 2:
            cap_h = c
            break
    best = 8
    for size in range(6, 40):
        bb = ImageFont.truetype(path, size).getbbox("H")
        if bb[3] - bb[1] <= cap_h:
            best = size
    return ImageFont.truetype(path, best)

def cap_height(img, box, bg):
    x, y, w, h = box
    rows = ink_rows(img, (x, y, min(w, 9), h), bg)       # huruf kapital pertama
    if not any(rows):
        return None, y
    a = rows.index(True); b = len(rows) - rows[::-1].index(True)
    return b - a, y + a

def tulis_nama(img, orig, box, text, max_w, trunc):
    bg, fg = bg_color(orig, box), fg_color(orig, box)
    ch, top = cap_height(orig, box, bg)
    f = font_cap(ch or box[3], BOLD)
    d = ImageDraw.Draw(img)
    x, y, w, h = box
    d.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], fill=bg)
    if f.getlength(text) > max_w:
        t = text.rstrip(".")
        while t and f.getlength(t.rstrip() + "...") > max_w:
            t = t[:-1]
        text = t.rstrip() + "..."
    d.text((x, (top if ch else y) - f.getbbox("H")[1]), text, font=f, fill=fg)

def tulis_email(img, orig, box, text):
    bg, fg = bg_color(orig, box), fg_color(orig, box)
    rows = ink_rows(orig, box, bg)
    x, y, w, h = box
    ih = len(rows) - rows[::-1].index(True) - rows.index(True) if any(rows) else h
    a = rows.index(True) if any(rows) else 0
    f = ImageFont.truetype(REG, 8)
    for size in range(6, 30):
        bb = ImageFont.truetype(REG, size).getbbox("dg")
        if bb[3] - bb[1] <= ih:
            f = ImageFont.truetype(REG, size)
    d = ImageDraw.Draw(img)
    d.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], fill=bg)
    d.text((x, y + a - f.getbbox("d")[1]), text, font=f, fill=fg)

def blur_rect(img, b, radius=10):
    x0, y0, x1, y1 = [int(v) for v in b]
    reg = img.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(radius))
    reg = reg.resize((max(1, (x1 - x0) // 6), max(1, (y1 - y0) // 6)), Image.BILINEAR).resize((x1 - x0, y1 - y0), Image.BILINEAR)
    img.paste(reg, (x0, y0))

def blur_phone(img, x, y, w, h, s):
    """Blur 4 digit terakhir nomor telepon (posisi diperkirakan dari proporsi karakter)."""
    m = None
    for m in PHONE.finditer(s):
        pass
    if not m:
        return False
    digits = [i for i in range(m.start(), m.end()) if s[i].isdigit()]
    start = digits[-4]
    cw = w / max(1, len(s))
    x0 = x + int(start * cw) - 3
    x1 = x + int(m.end() * cw) + 4
    blur_rect(img, (max(0, x0), max(0, y - 3), min(img.width, x1), min(img.height, y + h + 3)), radius=6)
    return True

# ---------- terapkan ----------
def proses(src, kerja, nama, peta, out):
    img = Image.open(os.path.join(src, nama)).convert("RGB")
    orig = img.copy()
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(kerja, "ocr", nama + ".tsv")) if l.startswith("T\t")]
    log = []
    cnt = Counter()
    for r in rows:
        if peta.match(r[5]):
            x, y, w, h = map(int, r[1:5])
            bb = tight(orig, (x, y, w, h), bg_color(orig, (x, y, w, h)))
            ch, _ = cap_height(orig, bb, bg_color(orig, bb))
            if ch:
                cnt[ch] += 1
    SNAP[:] = [c for c, _ in cnt.most_common()]
    for r in rows:
        x, y, w, h = map(int, r[1:5]); s = r[5]
        key = s.strip().lower()
        if key in peta.email:
            box = tight(orig, (x, y, w, h), bg_color(orig, (x, y, w, h)))
            tulis_email(img, orig, box, peta.email[key])
            log.append(f"email  {s} -> {peta.email[key]}")
            continue
        if PHONE.search(s) and blur_phone(img, x, y, w, h, s):
            log.append(f"telp   {s} -> 4 digit terakhir diblur")
            continue
        m = peta.match(s)
        if not m:
            continue
        real, core, trunc, has_time = m
        box = (x, y, w, h)
        bg = bg_color(orig, box)
        if has_time or re.search(r"\s[vO®•]$", s.strip()):
            box = split_time(orig, box, bg)
        box = tight(orig, box, bg)
        dm = peta.dummy(real, core, trunc)
        tulis_nama(img, orig, box, dm, box[2] + 2 if trunc else avail_right(orig, box, bg), trunc)
        log.append(f"nama   {s!r} -> {dm!r}")
    for b in peta.blur.get(nama, []):
        blur_rect(img, b)
        log.append(f"blur   area {b}")
    ext = os.path.splitext(nama)[1].lower()
    img.save(os.path.join(out, nama), **({"quality": 90} if ext in (".jpg", ".jpeg") else {}))
    return log

def cmd_terapkan(a):
    os.makedirs(a.out, exist_ok=True)
    peta = Peta(a.peta)
    ph = set(open(os.path.join(a.kerja, "placeholder.txt")).read().split())
    for f in images(a.src):
        if f in ph:
            print(f"## {f}: placeholder, dilewati")
            continue
        print(f"## {f}")
        for l in proses(a.src, a.kerja, f, peta, a.out):
            print("  ", l)
    print(f"Selesai -> {a.out}. WAJIB periksa visual tiap gambar sebelum diposting.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("ocr"); o.add_argument("--src", required=True); o.add_argument("--kerja", required=True)
    t = sub.add_parser("terapkan"); t.add_argument("--src", required=True); t.add_argument("--kerja", required=True)
    t.add_argument("--peta", required=True); t.add_argument("--out", required=True)
    a = ap.parse_args()
    {"ocr": cmd_ocr, "terapkan": cmd_terapkan}[a.cmd](a)
