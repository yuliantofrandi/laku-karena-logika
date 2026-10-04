#!/usr/bin/env python3
"""Posting / update artikel dokumentasi ke CMS api.lakukan.id (Python standar, tanpa dependensi).

  python3 posting.py ambil   --slug <slug> [--slug <slug2>] --out artikel.json
  python3 posting.py cek     --data artikel.json [--gambar <folder>] [--slug <slug>]
  python3 posting.py posting --data artikel.json [--gambar <folder>] [--slug <slug>] [--draft]
  python3 posting.py publik  --data artikel.json --company-slug <slug produk>

Mode:
  - Seri panduan   : banyak artikel + kelompok baru dalam satu artikel.json.
  - Satu artikel   : artikel.json berisi satu artikel; kelompoknya boleh rujukan saja.
  - Update artikel : `ambil` artikel dari CMS -> edit artikel.json -> `posting`.
                     Artikel yang slug-nya sudah ada selalu DIPERBARUI, tidak diduplikasi.
  --slug membatasi cek/posting ke artikel tertentu saja (mis. update satu artikel dari file seri).

API key dibaca dari env LAKUKAN_API_KEY (header X-API-Key). Jangan tulis key ke file.
Base URL: env LAKUKAN_API (default https://api.lakukan.id).

Struktur kategori SELALU dua level: level 0 = kategori induk (default "docs"),
level 1 = kelompok tutorial. Artikel ditempel ke kategori level 1.

Format artikel.json:
{
  "kategori_induk": "docs",
  "kelompok": [
    {"slug": "timebase-memulai", "nama": "Memulai", "deskripsi": "...", "urutan": 0},
    {"slug": "timebase-monitoring"}
  ],
  "artikel": [
    {"slug": "mengenal-timebase", "judul": "Mengenal TimeBase & Struktur Menu",
     "ringkasan": "...", "kelompok": "timebase-memulai", "sampul": "01-dashboard.jpg",
     "status": "published",
     "isi": "<p>...</p>{{img:01-dashboard.jpg|Keterangan gambar.}}<h2>...</h2>"}
  ]
}
- Kelompok dengan "nama" dibuat/diperbarui di bawah kategori induk. Kelompok tanpa "nama"
  hanya RUJUKAN ke kategori yang sudah ada dan tidak diubah.
- Field artikel yang tidak ditulis tidak diubah saat update: "ringkasan", "kelompok",
  "sampul" (sampul lama tetap), "status" (default published untuk artikel baru;
  artikel lama tetap pada statusnya).
- {{img:file|keterangan}} diunggah dari --gambar. <img src="https://..."> yang sudah ada
  di isi (hasil `ambil`) dibiarkan, tidak diunggah ulang.
- Urutan "artikel" = urutan baca. Artikel diposting dari belakang agar artikel pertama
  punya published_at terbaru (daftar publik diurutkan published_at desc).
"""
import argparse, html, json, mimetypes, os, re, sys, time, urllib.error, urllib.request, uuid

API = os.environ.get("LAKUKAN_API", "https://api.lakukan.id").rstrip("/")
ADMIN = API + "/core/v1/admin"
UA = "laku-karena-logika-article-docs/1.0 (+https://github.com/yuliantofrandi/laku-karena-logika)"
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

def load(path, only=None):
    d = json.load(open(path))
    d.setdefault("kategori_induk", "docs")
    d.setdefault("kelompok", [])
    if only:
        d["artikel"] = [x for x in d["artikel"] if x["slug"] in only]
        missing = set(only) - {x["slug"] for x in d["artikel"]}
        if missing:
            sys.exit(f"slug tidak ada di {path}: {', '.join(sorted(missing))}")
        pakai = {x.get("kelompok") for x in d["artikel"]}
        d["kelompok"] = [k for k in d["kelompok"] if k["slug"] in pakai]
    return d

SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

# ---------- ambil (untuk update) ----------
def cmd_ambil(a):
    out = {"kategori_induk": "docs", "kelompok": [], "artikel": []}
    for s in a.slug:
        x = must(req("GET", f"{ADMIN}/articles/{s}"), (200,), f"ambil {s}")
        art = {"slug": x["slug"], "judul": x["title"], "ringkasan": x.get("excerpt", ""),
               "status": x["status"], "isi": x.get("content", "")}
        if x.get("category"):
            art["kelompok"] = x["category"]["slug"]
            if all(k["slug"] != art["kelompok"] for k in out["kelompok"]):
                out["kelompok"].append({"slug": art["kelompok"]})   # rujukan, tidak diubah
        out["artikel"].append(art)
        print(f"ambil  {x['status']:<9} {(x.get('category') or {}).get('name', '-'):<18} {x['title']}")
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"Tersimpan di {a.out}. Edit isinya, lalu jalankan 'cek' dan 'posting'.")

# ---------- cek ----------
def validasi(d, gambar):
    err, warn = [], []
    kel = {k["slug"] for k in d["kelompok"]}
    slugs = set()
    for k in d["kelompok"]:
        if not SLUG.fullmatch(k["slug"]):
            err.append(f"slug kelompok tidak URL-safe: {k['slug']}")
    for a in d["artikel"]:
        s = a["slug"]
        if s in slugs:
            err.append(f"slug ganda: {s}")
        slugs.add(s)
        if not SLUG.fullmatch(s) or len(s) > 180:
            err.append(f"slug tidak valid: {s}")
        if re.search(r"(^|-)\d{1,2}(-|$)", s):
            warn.append(f"slug berisi nomor urut (urutan diatur frontend): {s}")
        if not 3 <= len(a.get("judul", "")) <= 160:
            err.append(f"judul harus 3–160 karakter: {s}")
        if re.search(r"#\s*\d|^\s*\d+[.)]\s", a.get("judul", "")):
            err.append(f"judul jangan bernomor seri: {a.get('judul')}")
        if len(a.get("ringkasan") or "") > 280:
            err.append(f"ringkasan > 280 karakter: {s}")
        if a.get("status") not in (None, "draft", "published"):
            err.append(f"status harus draft/published: {s}")
        if a.get("kelompok") and a["kelompok"] not in kel:
            err.append(f"kelompok '{a['kelompok']}' tidak ada di daftar kelompok: {s}")
        if not (a.get("isi") or "").strip():
            err.append(f"isi kosong: {s}")
        for f in [a.get("sampul")] + [m[0] for m in IMG.findall(a.get("isi", ""))]:
            if f and not os.path.exists(os.path.join(gambar, f)):
                err.append(f"gambar tidak ada: {os.path.join(gambar, f)} ({s})")
        if "{{" in IMG.sub("", a.get("isi", "")):
            err.append(f"placeholder rusak di isi: {s}")
        if re.search(r"<script|<iframe|\son\w+=", a.get("isi", ""), re.I):
            err.append(f"isi berisi script/iframe/on*: {s}")
    return err, warn

def cmd_cek(a):
    d = load(a.data, a.slug)
    err, warn = validasi(d, a.gambar)
    nodes = {n["slug"]: (n, p) for n, p in flat(tree())}
    ind = d["kategori_induk"]
    if any("nama" in k for k in d["kelompok"]):
        print(f"Kategori induk '{ind}': {'ada' if ind in nodes else 'BELUM ADA (akan dibuat)'}")
    for k in d["kelompok"]:
        n = nodes.get(k["slug"])
        if "nama" not in k:
            if not n:
                err.append(f"kategori rujukan '{k['slug']}' tidak ada di CMS (tambahkan 'nama' untuk membuatnya)")
            jalur = f"{n[1]['name']} › {n[0]['name']}" if n and n[1] else (n[0]["name"] if n else "?")
            print(f"  kategori {jalur} [{k['slug']}] — rujukan, tidak diubah")
            continue
        st = "baru" if not n else ("ada, diperbarui" if n[1] and n[1]["slug"] == ind else f"ada, dipindah ke '{ind}'")
        print(f"  L1 {k['nama']} [{k['slug']}] — {st}")
    for x in d["artikel"]:
        code, js = req("GET", f"{ADMIN}/articles/{x['slug']}")
        lama = js.get("data") or {}
        aksi = f"update ({lama.get('status')})" if code == 200 else "baru"
        print(f"  {aksi:<19} {x['judul']}  ({len(IMG.findall(x['isi']))} gambar baru diunggah)")
    for w in warn: print("PERINGATAN", w)
    for e in err: print("ERROR", e)
    print("\nOK, siap diposting." if not err else f"\n{len(err)} error — perbaiki dulu.")
    sys.exit(1 if err else 0)

# ---------- posting ----------
def pastikan_kategori(d):
    nodes = {n["slug"]: (n, p) for n, p in flat(tree())}
    ind = d["kategori_induk"]
    induk = None
    ids = {}
    for i, k in enumerate(d["kelompok"]):
        if "nama" not in k:   # rujukan saja
            if k["slug"] not in nodes:
                sys.exit(f"kategori rujukan '{k['slug']}' tidak ada di CMS")
            ids[k["slug"]] = nodes[k["slug"]][0]["id"]
            continue
        if induk is None:
            induk = nodes[ind][0] if ind in nodes else must(
                req("POST", ADMIN + "/article-categories", {"slug": ind, "name": ind.capitalize(), "sort_order": 0}), (201,), "buat induk")
        body = {"name": k["nama"], "description": k.get("deskripsi", ""), "sort_order": k.get("urutan", i), "parent_id": induk["id"]}
        if k["slug"] in nodes:
            ids[k["slug"]] = must(req("PUT", f"{ADMIN}/article-categories/{k['slug']}", body), (200,), f"update kategori {k['slug']}")["id"]
            print(f"kategori  update  {induk['name']} › {k['nama']}")
        else:
            ids[k["slug"]] = must(req("POST", ADMIN + "/article-categories", dict(body, slug=k["slug"])), (201,), f"buat kategori {k['slug']}")["id"]
            print(f"kategori  baru    {induk['name']} › {k['nama']}")
    return ids

def cmd_posting(a):
    d = load(a.data, a.slug)
    err, _ = validasi(d, a.gambar)
    if err:
        sys.exit("Validasi gagal, jalankan 'cek' dulu:\n  " + "\n  ".join(err))
    ids = pastikan_kategori(d)
    banyak = len(d["artikel"]) > 1
    for x in reversed(d["artikel"]):
        s = x["slug"]
        meta = {"title": x["judul"]}
        if "ringkasan" in x:
            meta["excerpt"] = x["ringkasan"] or ""
        if x.get("kelompok"):
            meta["category_id"] = ids[x["kelompok"]]
        code, js = req("GET", f"{ADMIN}/articles/{s}")
        if code == 200:
            lama = js["data"]
            must(req("PUT", f"{ADMIN}/articles/{s}", meta), (200,), f"update {s}")
            aksi = "update"
        else:
            lama = None
            dat = must(req("POST", ADMIN + "/articles", dict(meta, slug=s, content="<p>Menyiapkan konten…</p>", status="draft")), (201,), f"buat {s}")
            if dat["slug"] != s:
                sys.exit(f"slug dinormalisasi CMS menjadi {dat['slug']} — samakan di artikel.json")
            aksi = "baru"
        isi, url = x["isi"], {}
        for f, cap in IMG.findall(isi):
            if f not in url:
                url[f] = must(req("POST", f"{ADMIN}/articles/{s}/content-media", files={"file": os.path.join(a.gambar, f)}), (200,), f"upload {f}")["url"]
            isi = isi.replace(f"{{{{img:{f}|{cap}}}}}", f'<img src="{url[f]}" alt="{html.escape(cap, quote=True)}">\n<p><em>{cap}</em></p>')
        if x.get("sampul"):
            must(req("POST", f"{ADMIN}/articles/{s}/cover", files={"file": os.path.join(a.gambar, x["sampul"])}), (200,), f"sampul {s}")
        if a.draft:
            status = "draft"
        else:
            status = x.get("status") or (lama["status"] if lama else "published")
        body = {"content": isi.strip()}
        if not lama or lama["status"] != status:
            body["status"] = status       # status sama tidak dikirim ulang -> published_at tetap
        dat = must(req("PUT", f"{ADMIN}/articles/{s}", body), (200,), f"simpan {s}")
        print(f"{aksi:<7} {dat['status']:<9} {(dat.get('category') or {}).get('name', '-'):<18} {dat['title']}  ({len(url)} gambar diunggah)")
        if banyak:
            time.sleep(1.2)   # published_at berbeda -> urutan baca terjaga
    print("Selesai.")

def cmd_publik(a):
    d = load(a.data)
    h = {"X-Company-Slug": a.company_slug}
    code, js = req("GET", API + "/api/article-categories", headers=h, auth=False)
    if code != 200:
        sys.exit(f"Company slug '{a.company_slug}' ditolak: HTTP {code} {js.get('message')}")
    ok = True
    for x in d["artikel"]:
        code, js = req("GET", API + f"/api/articles/{x['slug']}", headers=h, auth=False)
        terbit = x.get("status", "published") == "published"
        if code != 200:
            ok &= not terbit
            print(f"{'BELUM TAMPIL' if terbit else 'draft (wajar tidak tampil)'}  {x['slug']}")
            continue
        art = js["data"]
        print(f"tampil  {(art.get('category') or {}).get('name', '-'):<18} {art['title']}")
        for u in re.findall(r'src="([^"]+)"', art.get("content", ""))[:3] + ([art["cover_url"]] if art.get("cover_url") else []):
            try:
                st = urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA}), timeout=30).status
            except urllib.error.HTTPError as e:
                st = e.code
            ok &= st == 200
            if st != 200:
                print(f"   gambar HTTP {st}  {u[:80]}")
    print("Publik OK." if ok else "Ada yang belum tampil di publik.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("ambil"); p.add_argument("--slug", action="append", required=True); p.add_argument("--out", required=True)
    for n in ("cek", "posting"):
        p = sub.add_parser(n); p.add_argument("--data", required=True); p.add_argument("--gambar", default=".")
        p.add_argument("--slug", action="append", help="hanya artikel ini (boleh diulang)")
        if n == "posting":
            p.add_argument("--draft", action="store_true", help="simpan sebagai draft, jangan terbitkan")
    p = sub.add_parser("publik"); p.add_argument("--data", required=True); p.add_argument("--company-slug", required=True)
    a = ap.parse_args()
    {"ambil": cmd_ambil, "cek": cmd_cek, "posting": cmd_posting, "publik": cmd_publik}[a.cmd](a)
