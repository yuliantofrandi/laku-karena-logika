#!/usr/bin/env python3
"""Unggah 3 PDF penawaran (hasil skill proposal-pdf) ke bucket R2 Cloudflare di proposal.venturo.id.

  python3 upload.py unggah --pdf <folder PDF> [--bucket proposal] [--domain https://proposal.venturo.id]
  python3 upload.py cek    --url <url1> <url2> <url3>

unggah  : cari set lengkap VEN-<Project>-<Tahun>-<Rev>.pdf, ...-Lampiran-Estimasi.pdf,
          ...-Service-Agreement.pdf (revisi tertinggi), unggah ke akar bucket dengan nama file
          apa adanya (URL = <domain>/<nama file>) lewat `npx wrangler@4 r2 object put --remote`,
          pasang robots.txt (Disallow: /), hapus objek revisi lama project yang sama,
          lalu catat hasilnya di <folder PDF>/.proposal-upload.json.
          Auth: login wrangler (`npx wrangler@4 login`) atau env CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID.
cek     : GET tiap URL: harus 200 dan application/pdf; X-Robots-Tag noindex diperiksa sebagai peringatan.

Catatan: wrangler tidak bisa menampilkan isi bucket, jadi revisi lama dikenali dari
.proposal-upload.json di folder PDF. Objek yang diunggah dari komputer lain tidak ikut terhapus.
"""
import argparse, json, os, re, subprocess, sys, tempfile, urllib.request

POLA = re.compile(r"^(VEN-([A-Za-z0-9]+)-(\d{4})-(\d{3}))(|-Lampiran-Estimasi|-Service-Agreement)\.pdf$")
JENIS = {"": "Penawaran Layanan", "-Lampiran-Estimasi": "Lampiran Estimasi Delivery Point",
         "-Service-Agreement": "Service Agreement"}
LOG = ".proposal-upload.json"


def baca_log(folder):
    p = os.path.join(folder, LOG)
    return json.load(open(p)) if os.path.exists(p) else {}


def susun(a):
    set_ = {}
    for f in os.listdir(a.pdf):
        m = POLA.match(f)
        if m:
            set_.setdefault(m.group(1), {})[m.group(5)] = os.path.join(a.pdf, f)
    for k, v in set_.items():
        if len(v) < 3:
            kurang = [JENIS[x] for x in JENIS if x not in v]
            print(f"PERINGATAN: set {k} tidak lengkap (kurang: {', '.join(kurang)}) — dilewati", file=sys.stderr)
    lengkap = {k: v for k, v in set_.items() if len(v) == 3}
    if not lengkap:
        sys.exit("Tidak ada set lengkap (Penawaran + Lampiran-Estimasi + Service-Agreement) dengan nomor revisi sama di " + a.pdf)
    proyek = {POLA.match(k + ".pdf").group(2) for k in lengkap}
    if len(proyek) > 1:
        sys.exit("Ada lebih dari satu project yang lengkap: " + ", ".join(sorted(proyek)) + ". Sebutkan satu dengan --pdf berisi satu project.")
    nomor = max(lengkap, key=lambda k: int(k[-3:]))
    _, prj, thn, rev = POLA.match(nomor + ".pdf").groups()[:4]
    log = baca_log(a.pdf)
    kunci_proyek = f"VEN-{prj}-{thn}"
    lama = log.get(kunci_proyek, {})
    objek = []
    for akh in ["", "-Lampiran-Estimasi", "-Service-Agreement"]:
        f = os.path.basename(lengkap[nomor][akh])
        objek.append({"jenis": JENIS[akh], "file": lengkap[nomor][akh], "kunci": f,
                      "url": f"{a.domain.rstrip('/')}/{f}"})
    hapus = [k for k in lama.get("objek", []) if k not in {o["kunci"] for o in objek}]
    return {"nomor": f"VEN/{prj}/{thn}/{rev}", "nomor_file": nomor, "kunci_proyek": kunci_proyek,
            "bucket": a.bucket, "objek": objek, "hapus_revisi_lama": hapus}


def tampil(r):
    return {"nomor": r["nomor"], "bucket": r["bucket"],
            "unggah": [{"jenis": o["jenis"], "url": o["url"]} for o in r["objek"]],
            "hapus_revisi_lama": r["hapus_revisi_lama"]}


def wr(*args):
    cmd = ["npx", "-y", "wrangler@4", "r2", "object", *args, "--remote"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"GAGAL: {' '.join(cmd)}\n{p.stdout[-800:]}\n{p.stderr[-800:]}")


def unggah(a):
    r = susun(a)
    for o in r["objek"]:
        wr("put", f"{r['bucket']}/{o['kunci']}", "--file", o["file"], "--content-type", "application/pdf",
           "--content-disposition", f'inline; filename="{os.path.basename(o["file"])}"',
           "--cache-control", "public, max-age=3600")
        print(f"unggah  {o['url']}")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as t:
        t.write("User-agent: *\nDisallow: /\n")
    wr("put", f"{r['bucket']}/robots.txt", "--file", t.name, "--content-type", "text/plain; charset=utf-8")
    os.unlink(t.name)
    for k in r["hapus_revisi_lama"]:
        wr("delete", f"{r['bucket']}/{k}")
        print(f"hapus   {k}")
    log = baca_log(a.pdf)
    log[r["kunci_proyek"]] = {"nomor": r["nomor_file"], "bucket": r["bucket"],
                             "objek": [o["kunci"] for o in r["objek"]], "url": [o["url"] for o in r["objek"]]}
    json.dump(log, open(os.path.join(a.pdf, LOG), "w"), ensure_ascii=False, indent=2)
    print(json.dumps(tampil(r), ensure_ascii=False, indent=2))


def cek(a):
    gagal = False
    for u in a.url:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 proposal-upload"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                ct, xr = resp.headers.get("Content-Type", ""), resp.headers.get("X-Robots-Tag", "")
                ok = resp.status == 200 and "application/pdf" in ct
                print(f"{'OK  ' if ok else 'GAGAL'} {resp.status} {ct:<16} {u}")
                if ok and "noindex" not in xr:
                    print("      PERINGATAN: tanpa X-Robots-Tag noindex (pasang Transform Rule, lihat SKILL.md)")
                gagal |= not ok
        except Exception as e:
            print(f"GAGAL {e} {u}"); gagal = True
    sys.exit(1 if gagal else 0)


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("unggah"); s.add_argument("--pdf", required=True)
s.add_argument("--bucket", default="proposal"); s.add_argument("--domain", default="https://proposal.venturo.id")
c = sub.add_parser("cek"); c.add_argument("--url", nargs="+", required=True)
a = ap.parse_args()
{"unggah": unggah, "cek": cek}[a.cmd](a)
