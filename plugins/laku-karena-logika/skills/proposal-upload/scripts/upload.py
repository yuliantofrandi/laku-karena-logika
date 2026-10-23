#!/usr/bin/env python3
"""Unggah 3 PDF penawaran (hasil skill proposal-pdf) ke bucket R2 Cloudflare di proposal.venturo.id.

  python3 upload.py domain [--bucket proposal]
  python3 upload.py info   --pdf <folder dan/atau file PDF ...>
  python3 upload.py unggah --pdf <folder dan/atau file PDF ...> [--bucket proposal] [--domain https://proposal.venturo.id]
  python3 upload.py cek    --url <url1> <url2> <url3>

domain : cek custom domain yang tersambung ke bucket. Kosong = semua link akan 404.
info   : baca teks PDF Penawaran → nama project, tanggal dokumen, tanggal berlaku (+14 hari),
         dan ada/tidaknya diskon di ketiga PDF (kata "gratis" tidak dihitung diskon).
unggah : cek domain, lalu unggah set lengkap VEN-<Project>-<Tahun>-<Rev>.pdf, ...-Lampiran-Estimasi.pdf,
         ...-Service-Agreement.pdf (revisi tertinggi) ke akar bucket dengan nama file apa adanya
         (URL = <domain>/<nama file>) lewat `npx wrangler@4 r2 object put --remote`, pasang robots.txt
         (Disallow: /), hapus objek revisi lama project yang sama, lalu catat di log tetap.
cek    : GET tiap URL: harus 200 dan application/pdf; X-Robots-Tag noindex diperiksa sebagai peringatan.

--pdf menerima satu atau beberapa folder dan/atau file PDF (mis. 3 PDF hasil proposal-pdf dari sesi chat
sebelumnya yang tersimpan di lokasi berbeda).
Log unggahan disimpan di lokasi tetap ~/.venturo/proposal-upload.json (ubah dengan env PROPOSAL_UPLOAD_LOG),
karena wrangler tidak bisa menampilkan isi bucket dan revisi lama dikenali dari log ini.
Auth: login wrangler (`npx wrangler@4 login`) atau env CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID.
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, tempfile, urllib.request

POLA = re.compile(r"^(VEN-([A-Za-z0-9]+)-(\d{4})-(\d{3}))(|-Lampiran-Estimasi|-Service-Agreement)\.pdf$")
JENIS = {"": "Penawaran Layanan", "-Lampiran-Estimasi": "Lampiran Estimasi Delivery Point",
         "-Service-Agreement": "Service Agreement"}
LOG = os.environ.get("PROPOSAL_UPLOAD_LOG", os.path.expanduser("~/.venturo/proposal-upload.json"))
LOG_LAMA = ".proposal-upload.json"          # lokasi lama (di folder PDF), tetap dibaca untuk migrasi
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
DISKON = re.compile(r"\b(diskon|potongan|discount|promo)\b", re.I)


# ---------- input ----------
def daftar_pdf(paths):
    """Kumpulkan file PDF dari folder dan/atau file yang diberikan → {nama file: path}."""
    hasil = {}
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            for f in os.listdir(p):
                if f.lower().endswith(".pdf"):
                    hasil.setdefault(f, os.path.join(p, f))
        elif os.path.isfile(p) and p.lower().endswith(".pdf"):
            hasil[os.path.basename(p)] = p
        else:
            print(f"PERINGATAN: {p} bukan folder atau file PDF — dilewati", file=sys.stderr)
    return hasil


def baca_log(files=()):
    log = json.load(open(LOG)) if os.path.exists(LOG) else {}
    for d in {os.path.dirname(f) for f in files}:                       # migrasi log lama di folder PDF
        if os.path.exists(os.path.join(d, LOG_LAMA)):
            for k, v in json.load(open(os.path.join(d, LOG_LAMA))).items():
                log.setdefault(k, v)
    return log


def tulis_log(log):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    json.dump(log, open(LOG, "w"), ensure_ascii=False, indent=2)


def susun(a):
    files = daftar_pdf(a.pdf)
    set_ = {}
    for f, path in files.items():
        m = POLA.match(f)
        if m:
            set_.setdefault(m.group(1), {})[m.group(5)] = path
    for k, v in set_.items():
        if len(v) < 3:
            kurang = [JENIS[x] for x in JENIS if x not in v]
            print(f"PERINGATAN: set {k} tidak lengkap (kurang: {', '.join(kurang)}) — dilewati", file=sys.stderr)
    lengkap = {k: v for k, v in set_.items() if len(v) == 3}
    if not lengkap:
        sys.exit("Tidak ada set lengkap (Penawaran + Lampiran-Estimasi + Service-Agreement) dengan nomor revisi sama di: " + ", ".join(a.pdf))
    proyek = {POLA.match(k + ".pdf").group(2) for k in lengkap}
    if len(proyek) > 1:
        sys.exit("Ada lebih dari satu project yang lengkap: " + ", ".join(sorted(proyek)) + ". Sebutkan satu dengan --pdf berisi satu project.")
    nomor = max(lengkap, key=lambda k: int(k[-3:]))
    _, prj, thn, rev = POLA.match(nomor + ".pdf").groups()[:4]
    kunci_proyek = f"VEN-{prj}-{thn}"
    lama = baca_log(files.values()).get(kunci_proyek, {})
    objek = []
    for akh in ["", "-Lampiran-Estimasi", "-Service-Agreement"]:
        f = os.path.basename(lengkap[nomor][akh])
        objek.append({"jenis": JENIS[akh], "file": lengkap[nomor][akh], "kunci": f,
                      "url": f"{getattr(a, 'domain', 'https://proposal.venturo.id').rstrip('/')}/{f}"})
    hapus = [k for k in lama.get("objek", []) if k not in {o["kunci"] for o in objek}]
    return {"nomor": f"VEN/{prj}/{thn}/{rev}", "nomor_file": nomor, "kunci_proyek": kunci_proyek,
            "bucket": getattr(a, "bucket", "proposal"), "objek": objek, "hapus_revisi_lama": hapus}


# ---------- teks PDF ----------
JXA = ('ObjC.import("PDFKit"); function run(a){var d=$.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(a[0]));'
       ' var s=""; for(var i=0;i<d.pageCount;i++){s+=d.pageAtIndex(i).string.js+"\\n"} return s}')


def teks_pdf(path):
    """PDFKit macOS (bawaan) → pdftotext → pypdf."""
    if shutil.which("osascript"):
        p = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, os.path.abspath(path)], capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout
    if shutil.which("pdftotext"):
        p = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout
    try:
        from pypdf import PdfReader
        return "\n".join(pg.extract_text() or "" for pg in PdfReader(path).pages)
    except ImportError:
        sys.exit("Tidak bisa membaca teks PDF: butuh macOS (PDFKit), pdftotext (poppler), atau pypdf.")


def tanggal(s):
    m = re.search(r"\b(\d{1,2})\s+(" + "|".join(BULAN) + r")\s+(\d{4})\b", s)
    return datetime.date(int(m.group(3)), BULAN.index(m.group(2)) + 1, int(m.group(1))) if m else None


def fmt(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def info(a):
    r = susun(a)
    teks = {o["jenis"]: teks_pdf(o["file"]) for o in r["objek"]}
    utama = teks["Penawaran Layanan"]
    m = re.search(r"Project\s*[:\n ]\s*(.+)", utama)
    project = m.group(1).strip() if m else None
    m = re.search(r"Tanggal\s*[:\n ]\s*(\d{1,2}\s+\w+\s+\d{4})", utama)
    tgl = tanggal(m.group(1)) if m else tanggal(utama)
    temuan = {j: sorted({x.lower() for x in DISKON.findall(t)}) for j, t in teks.items()}
    out = {"nomor": r["nomor"], "project": project,
           "tanggal_dokumen": fmt(tgl) if tgl else None,
           "berlaku_hingga": fmt(tgl + datetime.timedelta(days=14)) if tgl else None,
           "ada_diskon": any(temuan.values()),
           "kata_diskon": {j: v for j, v in temuan.items() if v},
           "url": [o["url"] for o in r["objek"]]}
    if not project or not tgl:
        print("PERINGATAN: nama project/tanggal tidak terbaca otomatis — periksa teks PDF.", file=sys.stderr)
    print(json.dumps(out, ensure_ascii=False, indent=2))


# ---------- R2 ----------
def npx(*args):
    return subprocess.run(["npx", "-y", "wrangler@4", *args], capture_output=True, text=True)


def wr(*args):
    p = npx("r2", "object", *args, "--remote")
    if p.returncode != 0:
        sys.exit(f"GAGAL: wrangler r2 object {' '.join(args)}\n{p.stdout[-800:]}\n{p.stderr[-800:]}")


def cek_domain(bucket):
    p = npx("r2", "bucket", "domain", "list", bucket)
    out = p.stdout + p.stderr
    ada = p.returncode == 0 and "no custom domains" not in out.lower()
    dom = re.findall(r"domain:\s*(\S+)", out)
    return ada, dom, out


def domain(a):
    ada, dom, out = cek_domain(a.bucket)
    print(out.strip()[-1200:])
    print("\nOK: domain tersambung " + ", ".join(dom) if ada else
          "\nBELUM ADA custom domain — semua link proposal.venturo.id akan 404. Lihat setup di SKILL.md §0.")
    sys.exit(0 if ada else 1)


def unggah(a):
    ada, dom, _ = cek_domain(a.bucket)
    if not ada:
        print("PERINGATAN: bucket belum punya custom domain — file tetap diunggah, tapi link akan 404 "
              "sampai proposal.venturo.id disambungkan (SKILL.md §0).", file=sys.stderr)
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
    log = baca_log([o["file"] for o in r["objek"]])
    log[r["kunci_proyek"]] = {"nomor": r["nomor_file"], "bucket": r["bucket"],
                             "objek": [o["kunci"] for o in r["objek"]], "url": [o["url"] for o in r["objek"]]}
    tulis_log(log)
    print(json.dumps({"nomor": r["nomor"], "domain_tersambung": ada, "log": LOG,
                      "unggah": [{"jenis": o["jenis"], "url": o["url"]} for o in r["objek"]],
                      "hapus_revisi_lama": r["hapus_revisi_lama"]}, ensure_ascii=False, indent=2))


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
    if gagal:
        print("Bila PDF 404 tapi robots.txt 200, kemungkinan domain belum tersambung ke R2 (masih ke server lama).")
    sys.exit(1 if gagal else 0)


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = ap.add_subparsers(dest="cmd", required=True)
d = sub.add_parser("domain"); d.add_argument("--bucket", default="proposal")
i = sub.add_parser("info"); i.add_argument("--pdf", nargs="+", required=True)
s = sub.add_parser("unggah"); s.add_argument("--pdf", nargs="+", required=True)
s.add_argument("--bucket", default="proposal"); s.add_argument("--domain", default="https://proposal.venturo.id")
c = sub.add_parser("cek"); c.add_argument("--url", nargs="+", required=True)
a = ap.parse_args()
{"domain": domain, "info": info, "unggah": unggah, "cek": cek}[a.cmd](a)
