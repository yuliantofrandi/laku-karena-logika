#!/usr/bin/env python3
"""Posting artikel panduan ke CMS api.lakukan.id (Python standar, tanpa dependensi).

  python3 posting.py cek     --data artikel.json --gambar <folder gambar tersamar>
  python3 posting.py posting --data artikel.json --gambar <folder gambar tersamar> [--draft]
  python3 posting.py publik  --data artikel.json --company-slug <slug produk>

API key dibaca dari env LAKUKAN_API_KEY (header X-API-Key). Jangan tulis key ke file.
Base URL: env LAKUKAN_API (default https://api.lakukan.id).

Struktur kategori SELALU dua level: level 0 = kategori induk (default "docs"),
level 1 = kelompok tutorial. Artikel ditempel ke kategori level 1.

Format artikel.json:
{
  "kategori_induk": "docs",
  "kelompok": [
    {"slug": "timebase-memulai", "nama": "Memulai", "deskripsi": "...", "urutan": 0}
  ],
  "artikel": [
    {"slug": "mengenal-timebase", "judul": "Mengenal TimeBase & Struktur Menu",
     "ringkasan": "...", "kelompok": "timebase-memulai", "sampul": "01-dashboard.jpg",
     "isi": "<p>...</p>{{img:01-dashboard.jpg|Keterangan gambar.}}<h2>...</h2>"}
  ]
}
Urutan "artikel" = urutan baca. Artikel diposting dari belakang agar artikel pertama
punya published_at terbaru (daftar publik diurutkan published_at desc).
"""
import argparse, html, json, mimetypes, os, re, sys, time, urllib.error, urllib.request, uuid

API = os.environ.get("LAKUKAN_API", "https://api.lakukan.id").rstrip("/")
ADMIN = API + "/core/v1/admin"
UA = "laku-karena-logika-docs-article/1.0 (+https://github.com/yuliantofrandi/laku-karena-logika)"
IMG = re.compile(r"\{\{img:([^|}]+)\|([^}]*)\}\}")

def key():
    k = os.environ.get("LAKUKAN_API_KEY", "").strip()
    if not k:
        sys.exit("Set env LAKUKAN_API_KEY dulu (minta API key ke user, jangan simpan ke file).")
    return k

def req(method, url, body=None, files=None, headers=None, auth=True):
    h = dict(headers or {})
    h.setdefault("User-Agent", UA)   # Cloudflare menolak UA bawaan urllib (error 1010)
    if auth:
        h["X-API-Key"] = key()
    data = None
    if files:
        b = uuid.uuid4().hex
        parts = []
        for field, path in files.items():
            ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
            parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{field}"; filename="{os.path.basename(path)}"\r\n'
                         f"Content-Type: {ctype}\r\n\r\n".encode() + open(path, "rb").read() + b"\r\n")
        data = b"".join(parts) + f"--{b}--\r\n".encode()
        h["Content-Type"] = f"multipart/form-data; boundary={b}"
    elif body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="replace")
            if e.code >= 500 and attempt < 2:
                time.sleep(2); continue
            try:
                return e.code, json.loads(txt)
            except ValueError:
                return e.code, {"message": txt[:300]}
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(3)

def must(res, ok, what):
    code, js = res
    if code not in ok:
        sys.exit(f"GAGAL {what}: HTTP {code} {js.get('message')} {js.get('errors') or ''}")
    return js.get("data")

def tree():
    return must(req("GET", ADMIN + "/article-categories"), (200,), "ambil kategori")

def flat(nodes, parent=None):
    for n in nodes:
        yield n, parent
        yield from flat(n.get("children") or [], n)

def load(path):
    d = json.load(open(path))
    d.setdefault("kategori_induk", "docs")
    return d

# ---------- cek ----------
def validasi(d, gambar):
    err, warn = [], []
    kel = {k["slug"] for k in d["kelompok"]}
    slugs = set()
    for k in d["kelompok"]:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", k["slug"]):
            err.append(f"slug kelompok tidak URL-safe: {k['slug']}")
    for a in d["artikel"]:
        s = a["slug"]
        if s in slugs:
            err.append(f"slug ganda: {s}")
        slugs.add(s)
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s) or len(s) > 180:
            err.append(f"slug tidak valid: {s}")
        if re.search(r"(^|-)\d{1,2}(-|$)", s):
            warn.append(f"slug berisi nomor urut (urutan diatur frontend): {s}")
        if not 3 <= len(a["judul"]) <= 160:
            err.append(f"judul harus 3–160 karakter: {s}")
        if re.search(r"#\s*\d|^\s*\d+[.)]\s", a["judul"]):
            err.append(f"judul jangan bernomor seri: {a['judul']}")
        if len(a.get("ringkasan", "")) > 280:
            err.append(f"ringkasan > 280 karakter: {s}")
        if a["kelompok"] not in kel:
            err.append(f"kelompok '{a['kelompok']}' tidak ada di daftar kelompok: {s}")
        for f in [a.get("sampul")] + [m[0] for m in IMG.findall(a["isi"])]:
            if f and not os.path.exists(os.path.join(gambar, f)):
                err.append(f"gambar tidak ada: {f} ({s})")
        sisa = IMG.sub("", a["isi"])
        if "{{" in sisa:
            err.append(f"placeholder rusak di isi: {s}")
        if re.search(r"<script|<iframe|\son\w+=", a["isi"], re.I):
            err.append(f"isi berisi script/iframe/on*: {s}")
    return err, warn

def cmd_cek(a):
    d = load(a.data)
    err, warn = validasi(d, a.gambar)
    for w in warn: print("PERINGATAN", w)
    for e in err: print("ERROR", e)
    nodes = {n["slug"]: (n, p) for n, p in flat(tree())}
    ind = d["kategori_induk"]
    print(f"\nKategori induk '{ind}': {'ada' if ind in nodes else 'BELUM ADA (akan dibuat)'}")
    for k in d["kelompok"]:
        n = nodes.get(k["slug"])
        st = "baru" if not n else ("ada" if n[1] and n[1]["slug"] == ind else f"ada, dipindah ke '{ind}'")
        print(f"  L1 {k['nama']} [{k['slug']}] — {st}")
    for x in d["artikel"]:
        code, _ = req("GET", f"{ADMIN}/articles/{x['slug']}")
        print(f"  {'update' if code == 200 else 'baru  '} {x['judul']}  ({len(IMG.findall(x['isi']))} gambar)")
    print("\nOK, siap diposting." if not err else f"\n{len(err)} error — perbaiki dulu.")
    sys.exit(1 if err else 0)

# ---------- posting ----------
def pastikan_kategori(d):
    nodes = {n["slug"]: (n, p) for n, p in flat(tree())}
    ind = d["kategori_induk"]
    if ind in nodes:
        induk = nodes[ind][0]
    else:
        induk = must(req("POST", ADMIN + "/article-categories", {"slug": ind, "name": ind.capitalize(), "sort_order": 0}), (201,), "buat induk")
    ids = {}
    for i, k in enumerate(d["kelompok"]):
        body = {"name": k["nama"], "description": k.get("deskripsi", ""), "sort_order": k.get("urutan", i), "parent_id": induk["id"]}
        if k["slug"] in nodes:
            ids[k["slug"]] = must(req("PUT", f"{ADMIN}/article-categories/{k['slug']}", body), (200,), f"update kategori {k['slug']}")["id"]
            print(f"kategori  update  {induk['name']} › {k['nama']}")
        else:
            ids[k["slug"]] = must(req("POST", ADMIN + "/article-categories", dict(body, slug=k["slug"])), (201,), f"buat kategori {k['slug']}")["id"]
            print(f"kategori  baru    {induk['name']} › {k['nama']}")
    return ids

def cmd_posting(a):
    d = load(a.data)
    err, _ = validasi(d, a.gambar)
    if err:
        sys.exit("Validasi gagal, jalankan 'cek' dulu:\n  " + "\n  ".join(err))
    ids = pastikan_kategori(d)
    status = "draft" if a.draft else "published"
    for x in reversed(d["artikel"]):
        s = x["slug"]
        meta = {"title": x["judul"], "excerpt": x.get("ringkasan", ""), "category_id": ids[x["kelompok"]]}
        code, _ = req("GET", f"{ADMIN}/articles/{s}")
        if code == 200:
            must(req("PUT", f"{ADMIN}/articles/{s}", meta), (200,), f"update {s}")
        else:
            dat = must(req("POST", ADMIN + "/articles", dict(meta, slug=s, content="<p>Menyiapkan konten…</p>", status="draft")), (201,), f"buat {s}")
            if dat["slug"] != s:
                sys.exit(f"slug dinormalisasi CMS menjadi {dat['slug']} — samakan di artikel.json")
        isi, url = x["isi"], {}
        for f, cap in IMG.findall(isi):
            if f not in url:
                url[f] = must(req("POST", f"{ADMIN}/articles/{s}/content-media", files={"file": os.path.join(a.gambar, f)}), (200,), f"upload {f}")["url"]
            isi = isi.replace(f"{{{{img:{f}|{cap}}}}}", f'<img src="{url[f]}" alt="{html.escape(cap, quote=True)}">\n<p><em>{cap}</em></p>')
        if x.get("sampul"):
            must(req("POST", f"{ADMIN}/articles/{s}/cover", files={"file": os.path.join(a.gambar, x["sampul"])}), (200,), f"sampul {s}")
        dat = must(req("PUT", f"{ADMIN}/articles/{s}", {"content": isi.strip(), "status": status}), (200,), f"terbitkan {s}")
        print(f"artikel   {dat['status']:<9} {dat['category']['name']:<18} {dat['title']}  ({len(url)} gambar)")
        time.sleep(1.2)   # published_at berbeda -> urutan baca terjaga
    print("Selesai.")

def cmd_publik(a):
    d = load(a.data)
    h = {"X-Company-Slug": a.company_slug}
    code, js = req("GET", API + "/api/article-categories", headers=h, auth=False)
    if code != 200:
        sys.exit(f"Company slug '{a.company_slug}' ditolak: HTTP {code} {js.get('message')}")
    ok = True
    for k in d["kelompok"]:
        code, js = req("GET", API + f"/api/articles?category={k['slug']}&limit=100", headers=h, auth=False)
        n = len(js.get("data") or [])
        harap = sum(1 for x in d["artikel"] if x["kelompok"] == k["slug"])
        ok &= n >= harap
        print(f"{k['nama']:<20} publik {n} / diharapkan {harap}")
    for x in d["artikel"][:1]:
        code, js = req("GET", API + f"/api/articles/{x['slug']}", headers=h, auth=False)
        for u in re.findall(r'src="([^"]+)"', (js.get("data") or {}).get("content", ""))[:3]:
            try:
                st = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA}), timeout=30).status
            except urllib.error.HTTPError as e:
                st = e.code
            ok &= st == 200
            print(f"gambar HTTP {st}  {u[:80]}")
    print("Publik OK." if ok else "Ada yang belum tampil di publik.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("cek", "posting"):
        p = sub.add_parser(n); p.add_argument("--data", required=True); p.add_argument("--gambar", required=True)
        if n == "posting":
            p.add_argument("--draft", action="store_true", help="simpan sebagai draft, jangan terbitkan")
    p = sub.add_parser("publik"); p.add_argument("--data", required=True); p.add_argument("--company-slug", required=True)
    a = ap.parse_args()
    {"cek": cmd_cek, "posting": cmd_posting, "publik": cmd_publik}[a.cmd](a)
