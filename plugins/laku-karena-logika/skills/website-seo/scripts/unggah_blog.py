#!/usr/bin/env python3
"""Unggah artikel hasil tools/ekspor_blog.py ke kategori Blog di CMS Lakukan (admin API).

Kunci API dibaca dari env LAKUKAN_API_KEY (header X-API-Key) — jangan simpan di file proyek.

Urutan per artikel (artikel tidak pernah tampil setengah jadi):
  1. POST /core/v1/admin/articles           → buat sebagai DRAF
  2. POST …/{slug}/content-media            → unggah gambar isi, dapat URL publik
  3. POST …/{slug}/cover                    → unggah sampul (gambar pertama)
  4. PUT  …/{slug}                          → isi HTML dengan URL gambar CMS + status (default published)
Artikel dengan slug yang sudah ada dilewati (tidak ditimpa) kecuali memakai --perbarui.

Pemakaian:
  LAKUKAN_API_KEY=… python3 tools/unggah_blog.py [--draf] [--perbarui] [slug …]
"""
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "export" / "blog"
BASE = "https://api.lakukan.id/core/v1/admin"


def panggil(method, path, key, body=None, file=None):
    headers = {"X-API-Key": key, "Accept": "application/json", "User-Agent": "website-build"}
    data = None
    if file:
        batas = uuid.uuid4().hex
        tipe = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        data = (f'--{batas}\r\nContent-Disposition: form-data; name="file"; filename="{file.name}"\r\n'
                f"Content-Type: {tipe}\r\n\r\n").encode() + file.read_bytes() + f"\r\n--{batas}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={batas}"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except Exception:
            return e.code, {"message": e.reason}


def kategori_blog(key, slug="blog"):
    st, d = panggil("GET", "/article-categories", key)
    if st != 200:
        sys.exit(f"Gagal membaca kategori ({st}): {d.get('message')}")
    def cari(items):
        for k in items:
            if k["slug"] == slug:
                return k["id"]
            got = cari(k.get("children") or [])
            if got:
                return got
    kid = cari(d["data"])
    if not kid:
        sys.exit(f'Kategori "{slug}" tidak ditemukan di CMS')
    return kid


def main():
    key = os.environ.get("LAKUKAN_API_KEY")
    if not key:
        sys.exit("Set env LAKUKAN_API_KEY dulu (header X-API-Key)")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    status = "draft" if "--draf" in sys.argv else "published"
    perbarui = "--perbarui" in sys.argv
    files = sorted(EXPORT.glob("*.json"))
    if args:
        files = [f for f in files if f.stem in args]
    if not files:
        sys.exit("Tidak ada artikel di export/blog — jalankan tools/ekspor_blog.py dulu")
    kid = kategori_blog(key)
    for f in files:
        a = json.loads(f.read_text(encoding="utf-8"))
        slug = a["slug"]
        st, ada = panggil("GET", f"/articles/{slug}", key)
        if st == 200 and not perbarui:
            print(f"  {slug}: sudah ada di CMS ({ada['data'].get('status')}) → dilewati (pakai --perbarui untuk menimpa)")
            continue
        if st != 200:
            st, d = panggil("POST", "/articles", key, {"title": a["title"], "slug": slug, "excerpt": a["excerpt"][:280],
                                                      "content": "<p>Sedang disiapkan.</p>", "status": "draft", "category_id": kid})
            if st not in (200, 201):
                print(f"  {slug}: GAGAL membuat ({st}) {d.get('message')} {d.get('errors') or ''}")
                continue
        isi = a["content"]
        # sampul = gambar pertama, dan tidak diulang di isi (halaman artikel sudah menampilkan sampul di atas)
        if a.get("cover"):
            st, d = panggil("POST", f"/articles/{slug}/cover", key, file=EXPORT / a["cover"])
            if st != 200:
                print(f"  {slug}: GAGAL unggah sampul ({st}) {d.get('message')}")
                continue
            isi = re.sub(rf'<img src="{re.escape(a["cover"])}"[^>]*>\s*', "", isi, count=1)
        for g in a["images"]:
            if f'src="{g["file"]}"' not in isi:
                continue
            st, d = panggil("POST", f"/articles/{slug}/content-media", key, file=EXPORT / g["file"])
            if st != 200:
                print(f"  {slug}: GAGAL unggah {g['file']} ({st}) {d.get('message')}")
                break
            isi = isi.replace(f'src="{g["file"]}"', f'src="{d["data"]["url"]}"')
        else:
            st, d = panggil("PUT", f"/articles/{slug}", key, {"title": a["title"], "excerpt": a["excerpt"][:280],
                                                             "content": isi, "status": status, "category_id": kid})
            if st == 200:
                print(f"  {slug}: OK → {status}")
            else:
                print(f"  {slug}: GAGAL update ({st}) {d.get('message')} {d.get('errors') or ''}")


if __name__ == "__main__":
    main()
