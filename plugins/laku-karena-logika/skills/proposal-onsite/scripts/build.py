#!/usr/bin/env python3
"""Bangun 2 HTML penawaran Onsite Engineer dari satu file data JSON.

  python3 build.py <data.json> <folder kerja>

Hasil di <folder kerja>: penawaran.html dan sla.html (+ logo, bg, ttd, paraf, fonts).
Render dengan scripts/render.py.

Yang dihitung otomatis (dan di-assert):
- Komponen biaya per talent dari PRESET (references/pricelist-onsite.md) atau `komponen` dari pemilik.
- Tarif per talent / bulan = (biaya talent + biaya penempatan) × (1 + management fee sesuai durasi kontrak).
- Engineering Kick-off 1× tarif bulanan per talent sebagai Down Payment; invoice bulanan di awal bulan.
- Venturo Cloud (opsional) per bulan; diskon hanya bila pemilik menyebutnya, disebar rata ke invoice bulanan.
- Total Investasi = Σ termin = Total Pembayaran.
Lihat assets/contoh-data.json untuk format data.
"""
import html, json, os, re, shutil, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, "assets")

# Simulasi harga 2026 (deck slide 9). Gaji pokok = rekomendasi; kandidat lain → `komponen` dari pemilik.
PRESET = {
    "jakarta-intermediate": dict(kota="Jakarta", level="Intermediate", gaji=6_500_000, bpjs=675_000, thr=550_000, pkwt=550_000),
    "jakarta-senior": dict(kota="Jakarta", level="Senior", gaji=10_000_000, bpjs=935_000, thr=760_000, pkwt=760_000),
    "surabaya": dict(kota="Surabaya", level="Intermediate", gaji=6_500_000, bpjs=630_000, thr=510_000, pkwt=510_000),
    "malang": dict(kota="Malang", level="Intermediate", gaji=4_500_000, bpjs=440_000, thr=360_000, pkwt=360_000),
}
PENEMPATAN = [("AI Engineering Platform", 500_000), ("Laptop kerja", 500_000), ("Training &amp; sertifikasi", 150_000)]
CLOUD = {
    "shared-mini": ("Shared Hosting Mini", "1 CPU · 2 GB RAM · 5 GB storage", 200_000),
    "shared-small": ("Shared Hosting Small", "2 CPU · 3 GB RAM · 5 GB storage", 350_000),
    "shared-medium": ("Shared Hosting Medium", "2 CPU · 4 GB RAM · 5 GB storage", 600_000),
    "vps-mini": ("VPS Cloud Server Mini", "2 vCPU · 4 GB RAM · 32 GB storage", 800_000),
    "vps-small": ("VPS Cloud Server Small", "4 vCPU · 4 GB RAM · 32 GB storage", 900_000),
    "vps-medium": ("VPS Cloud Server Medium", "4 vCPU · 8 GB RAM · 32 GB storage", 1_050_000),
    "vps-large": ("VPS Cloud Server Large", "6 vCPU · 8 GB RAM · 32 GB storage", 1_150_000),
}
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
ALASAN_GANTI = ["Ketidakcocokan budaya kerja atau komunikasi dengan tim",
                "Sering absen, terlambat, atau izin tanpa keterangan",
                "Melanggar tata tertib, disiplin, atau sopan santun di lokasi Klien",
                "Memanipulasi absensi atau timesheet",
                "Membocorkan data atau menyalahgunakan akses sistem",
                "Tidak jujur atau melakukan tindak pidana"]


def e(s): return html.escape(str(s), quote=False)
BLANK = "______________________"
def garis(v): return e(v) if v else BLANK
def rp(x):
    x = round(x)
    return "Rp" + f"{x:,}".replace(",", ".")
def pct(f): return f"{f * 100:g}".replace(".", ",") + "%"


def fee(bulan):
    assert bulan >= 3, "durasi kontrak minimal 3 bulan"
    return 0.10 if bulan >= 12 else 0.125 if bulan >= 6 else 0.15


def bulan_ke(mulai, i):  # mulai "Januari 2027" → (indeks bulan, tahun) untuk bulan ke-i (0-based)
    nm, th = mulai.split()
    b = BULAN.index(nm) + i
    return b % 12, int(th) + b // 12


def hero(d, eyebrow, judul, label_no):
    k = d["klien"]
    return f'''<section class="hero">
  <img class="logo" src="logo.png" alt="Venturo Expert Programmers">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{judul}<br><span>{e(d["project"])}</span></h1>
  <div class="meta">
    <div class="card"><div class="kv"><b>{label_no}</b><span>{e(d["nomor"])}</span><b>Project</b><span>{e(d["project"])}</span><b>Tanggal</b><span>{e(d["tanggal"])}</span></div></div>
    <div class="card soft"><div class="lbl">Kepada Yth.</div><div class="to">{garis(k.get("penerima"))}</div><div>{e(k["instansi"])}</div><div style="color:var(--muted)">{garis(k.get("alamat"))}</div></div>
  </div>
'''


def dokumen(title, body):
    css = open(os.path.join(ASSETS, "onsite.css")).read()
    return f'<!doctype html>\n<html lang="id"><head><meta charset="utf-8"><title>{title}</title>\n<style>\n{css}</style></head><body>\n{body}\n</body></html>\n'


def talent(d):
    """Lengkapi setiap talent dengan komponen biaya, biaya dasar, dan tarif bulanan."""
    n, f = d["durasi_bulan"], fee(d["durasi_bulan"])
    out = []
    for t in d["talent"]:
        if t.get("komponen"):
            k = dict(t["komponen"]); assert t.get("kota") and t.get("level"), "talent dengan `komponen` wajib punya kota & level"
            k.update(kota=t["kota"], level=t["level"])
        else:
            assert t.get("preset") in PRESET, f"preset tidak dikenal: {t.get('preset')} (kota/level lain → isi `komponen` dari pemilik)"
            k = dict(PRESET[t["preset"]])
        for x in ("gaji", "bpjs", "thr", "pkwt"):
            assert k.get(x, 0) > 0, f"komponen {x} kosong untuk {t['posisi']}"
        dasar = k["gaji"] + k["bpjs"] + k["thr"] + k["pkwt"] + sum(v for _, v in PENEMPATAN)
        out.append(dict(t, **k, dasar=dasar, fee=f, tarif=round(dasar * (1 + f)), jumlah=t.get("jumlah", 1)))
    return out


def hitung(d):
    n = d["durasi_bulan"]; ts = talent(d)
    cloud = [(CLOUD[c["paket"]], c.get("jumlah", 1), c.get("keterangan", "")) for c in (d.get("venturo_cloud") or [])]
    bulanan = sum(t["tarif"] * t["jumlah"] for t in ts) + sum(c[2] * j for c, j, _ in cloud)
    kickoff = sum(t["tarif"] * t["jumlah"] for t in ts)
    subtotal = kickoff + bulanan * n
    dis = d.get("diskon")
    total = subtotal - (dis["nilai"] if dis else 0)
    # Diskon disebar rata ke invoice bulanan; sisa pembulatan masuk bulan terakhir.
    per = round(dis["nilai"] / n) if dis else 0
    termin = [("Penandatanganan", "Engineering Kick-off (Down Payment)", "Saat tanda tangan", kickoff)]
    for i in range(n):
        b, th = bulan_ke(d["mulai"], i)
        pot = (dis["nilai"] - per * (n - 1)) if (dis and i == n - 1) else per
        termin.append((f"{BULAN[b]} {th}", f"Bulan ke-{i + 1}", f"1 {BLN[b]} {th}", bulanan - pot))
    assert abs(sum(t[3] for t in termin) - total) < 1, "Σ termin ≠ Total"
    return ts, cloud, bulanan, kickoff, subtotal, total, termin


def periode(d):
    n = d["durasi_bulan"]; b0, t0 = bulan_ke(d["mulai"], 0); b1, t1 = bulan_ke(d["mulai"], n - 1)
    return f"{BLN[b0]} {t0} – {BLN[b1]} {t1}"


def penawaran(d):
    k = d["klien"]; tahun = d["tanggal"].split()[-1]; n = d["durasi_bulan"]
    ts, cloud, bulanan, kickoff, subtotal, total, termin = hitung(d)
    f = ts[0]["fee"]; orang = sum(t["jumlah"] for t in ts)
    h = hero(d, "Penawaran Layanan &amp; Persetujuan Kerja Sama", "Onsite Engineer", "No.")
    h += ('  <p class="intro">Melalui penawaran ini, kami menegaskan kesiapan tim IT profesional kami yang berjumlah kurang lebih 100 orang '
          'untuk menempatkan engineer di lokasi Klien, dengan rekrutmen, monitoring, dan pengelolaan talent sepenuhnya menjadi tanggung jawab Venturo. '
          'Dokumen ini memuat ruang lingkup layanan dan rincian biaya sebagai acuan kesepakatan bersama kedua belah pihak.</p>\n</section>\n')
    box = lambda judul, ket, isi: (f'<div class="svc"><h3>{judul} <small>{ket}</small></h3><ul>'
                                   + "".join(f"<li>{x}</li>" for x in isi) + "</ul></div>\n")
    # 1. Lingkup Layanan
    trow = "".join(f'<tr><td><b style="font-weight:600">{e(t["posisi"])}</b>' + (f'<span class="d">{e(t["keahlian"])}</span>' if t.get("keahlian") else "")
                   + f'</td><td>{e(t["level"])}</td><td>{e(t["kota"])}</td><td class="r">{t["jumlah"]}</td></tr>' for t in ts)
    h += f'''<h2><i>1</i>Lingkup Layanan</h2>
<div class="keep"><table class="cost" style="margin-bottom:3mm">
  <thead><tr><th>Talent yang Ditempatkan</th><th>Level</th><th>Kota</th><th class="r">Orang</th></tr></thead>
  <tbody>{trow}<tr class="grand"><td colspan="3">Total Talent</td><td class="r">{orang} orang</td></tr></tbody>
</table></div>
'''
    h += box("Penempatan &amp; Jam Kerja", f'{n} bulan, {periode(d)}', [
        f'Lokasi kerja: {garis(d.get("lokasi"))}',
        "8 jam per hari atau 40 jam per minggu, jadwal ditentukan Klien; talent mengikuti SOP dan peraturan perusahaan Klien",
        "Klien menyediakan meja kerja, internet, dan akses sistem",
        "Talent hanya mengerjakan pekerjaan yang berkaitan dengan pengembangan software"])
    h += box("Dikelola Venturo", "Sudah termasuk dalam tarif", [
        "Seleksi kandidat: screening dan tes teknis oleh Venturo, Klien cukup interview akhir",
        "Monitoring harian lewat Engineering ERP Venturo: pekerjaan, kendala, dan aktivitas kerja tercatat setiap hari",
        "Supervisor mendampingi secara berkala, membantu saat ada kendala, dan menjaga kualitas kode",
        "Laporan bulanan kehadiran dan kinerja, dengan penilaian KPI 360°",
        "Account Manager sebagai satu pintu komunikasi dengan Klien",
        "Talent cadangan: pengganti sementara saat talent cuti atau sakit panjang",
        "Payroll, BPJS, THR, kompensasi PKWT, dan pajak penghasilan talent diurus Venturo",
        "Pelatihan dan upskilling bila proyek membutuhkan skill baru, tanpa biaya tambahan",
        "Hubungan kerja talent hanya dengan Venturo; Klien dibebaskan dari tuntutan hubungan industrial talent"])
    h += box("Penggantian Talent", "Klien berhak meminta pengganti bila terjadi salah satu kondisi berikut",
             ALASAN_GANTI + ["Permintaan disampaikan secara tertulis kepada Account Manager Venturo; biaya rekrutmen dan onboarding pengganti sepenuhnya ditanggung Venturo",
                             "Talent yang resign langsung disiapkan penggantinya oleh Venturo"])
    # 2. Rincian Biaya — komponen per talent (kolom) lalu tabel biaya
    col = "".join(f'<th class="r">{e(t["posisi"])}<br><small style="font-weight:500;opacity:.85">{e(t["kota"])} · {e(t["level"])}</small></th>' for t in ts)
    cg = '<colgroup><col style="width:62mm">' + "<col>" * len(ts) + "</colgroup>"
    rk = lambda nama, vals, cls="": f'<tr{cls}><td>{nama}</td>' + "".join(f'<td class="r">{rp(v)}</td>' for v in vals) + "</tr>"
    komp = (rk("Gaji pokok", [t["gaji"] for t in ts]) + rk("BPJS Ketenagakerjaan &amp; Kesehatan", [t["bpjs"] for t in ts])
            + rk("Provisi THR", [t["thr"] for t in ts]) + rk("Provisi kompensasi PKWT", [t["pkwt"] for t in ts])
            + "".join(rk(nm, [v] * len(ts)) for nm, v in PENEMPATAN)
            + rk("<b>Total Biaya Dasar</b>", [t["dasar"] for t in ts], ' style="font-weight:600;background:var(--s2)"')
            + rk(f"Management Fee {pct(f)}", [t["tarif"] - t["dasar"] for t in ts]))
    h += f'''<div class="keep"><h2><i>2</i>Rincian Biaya</h2>
<table class="cost" style="table-layout:fixed">{cg}
  <thead><tr><th>Komponen per Talent / Bulan</th>{col}</tr></thead>
  <tbody>{komp}<tr class="grand"><td>Tarif per Talent / Bulan</td>{"".join(f'<td class="r">{rp(t["tarif"])}</td>' for t in ts)}</tr></tbody>
</table>
<p style="margin:2mm 0 4mm;color:var(--muted);font-size:8.3pt">Management Fee {pct(f)} untuk kontrak {n} bulan (3–5 bulan 15%, 6–11 bulan 12,5%, 12 bulan atau lebih 10%). Gaji pokok adalah rekomendasi; harga final mengikuti kandidat yang dipilih Klien.</p></div>
'''
    grp = lambda judul, ket: f'<tr class="grp"><td colspan="5">{judul}<small>{ket}</small></td></tr>'
    row = lambda nama, ket, tarif, jml, bln: (f'<tr><td><b style="font-weight:600">{nama}</b>' + (f'<span class="d">{ket}</span>' if ket else "")
                                             + f'</td><td class="r">{rp(tarif)}</td><td class="r">{jml}</td><td class="r">{bln}</td><td class="r">{rp(tarif * jml * bln)}</td></tr>')
    body = (grp("Engineering Kick-off", "Sekali bayar sebagai Down Payment: rekrutmen &amp; seleksi, onboarding, setup kerja, garansi penggantian talent")
            + "".join(row(e(t["posisi"]), "", t["tarif"], t["jumlah"], 1) for t in ts)
            + grp("Talent Onsite", f"{n} bulan, {periode(d)}")
            + "".join(row(e(t["posisi"]), f'{e(t["kota"])} · {e(t["level"])}', t["tarif"], t["jumlah"], n) for t in ts))
    if cloud:
        body += grp("Venturo Cloud", "Server per bulan") + "".join(
            row(c[0], e(ket) or c[1], c[2], j, n) for c, j, ket in cloud)
    dis = d.get("diskon")
    if dis:
        body += f'<tr class="sub"><td colspan="4">Total</td><td class="r">{rp(subtotal)}</td></tr><tr class="sub disc"><td colspan="4">{e(dis["nama"])}</td><td class="r">– {rp(dis["nilai"])}</td></tr>'
    h += f'''<table class="cost">
  <thead><tr><th>Layanan</th><th class="r">Tarif/Bulan</th><th class="r">Orang</th><th class="r">Bulan</th><th class="r">Total</th></tr></thead>
  <tbody>{body}<tr class="grand"><td colspan="4">Total Investasi</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
'''
    # 3. Pembayaran
    trows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="r">{rp(x)}</td></tr>' for a, b, c, x in termin)
    h += f'''<div class="keep"><h2><i>3</i>Pembayaran</h2>
<ul style="margin:0 0 3mm">
  <li>Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien.</li>
  <li>Engineering Kick-off sebesar 1× tarif bulanan per talent dibayar sekali sebagai Down Payment saat penandatanganan, sebelum proses seleksi dimulai.</li>
  <li>Invoice bulanan dikirim di awal bulan dan wajib dibayarkan paling lambat 14 (empat belas) hari kalender dari tanggal invoice.</li>
  <li>Apabila Klien tidak melakukan pembayaran sesuai jadwal, maka seluruh aktivitas layanan berhak dihentikan sementara.</li>
  <li>Tarif disesuaikan apabila terdapat perubahan UMP/UMK atau regulasi ketenagakerjaan, dengan pemberitahuan tertulis kepada Klien.</li>
  <li>Perpanjangan kontrak dikonfirmasi secara tertulis paling lambat 2 (dua) bulan sebelum kontrak berakhir.</li>
</ul>
<div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div></div>
<table class="cost">
  <thead><tr><th>Periode Kerja</th><th>Termin</th><th>Tgl Invoice</th><th class="r">Nominal</th></tr></thead>
  <tbody>{trows}<tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
'''
    # 4. Batasan
    bat = ["Lembur, dihitung per jam sesuai formulir perintah lembur tertulis dari Klien",
           f'Perjalanan dinas di luar kota penempatan',
           "Lisensi software, server, atau hardware khusus permintaan Klien" + ("" if cloud else ", termasuk server aplikasi"),
           "Sertifikasi vendor di luar program training Venturo"] + list(d.get("batasan", []))
    h += ('<div class="keep">\n<h2><i>4</i>Batasan dan Pengecualian</h2>\n<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk:</p>\n<ul>\n'
          + "".join(f"  <li>{x}</li>\n" for x in bat)
          + '</ul>\n<p style="margin:2mm 0 0">Seluruh item di atas tetap dapat disediakan Venturo, ditagih sesuai biaya aktual ditambah biaya layanan, atas persetujuan tertulis Klien.</p>\n</div>\n')
    # 5. Persetujuan
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    h += f'''<div class="sign">
  <h2 style="margin-top:8mm"><i>5</i>Persetujuan</h2>
  <p class="agree">Dengan menandatangani dokumen ini, kedua belah pihak menyatakan bahwa mereka telah membaca, memahami, dan menyetujui seluruh syarat dan ketentuan yang tercantum dalam dokumen ini, yang merupakan bagian tidak terpisahkan dari dokumen Service Agreement Onsite Engineer Venturo.</p>
<p class="place">Ditandatangani di Malang, pada tanggal ____________________ {tahun}.</p>
  <div class="sg">
    <div class="sbox"><div class="party">Penyedia Layanan</div><div class="co">PT Venturo Pro Indonesia</div>
      <div class="area"><img class="ttd" src="ttd.png" alt=""></div>
      <table class="f"><tr><td>Nama</td><td><b>Yulianto Frandi</b></td></tr><tr><td>Jabatan</td><td>CEO</td></tr><tr><td>Tanggal</td><td>{e(d["tanggal"])}</td></tr></table></div>
    <div class="sbox"><div class="party">Klien</div><div class="co">{e(k["instansi"])}</div>
      <div class="area"><span class="stamp">Tanda tangan &amp; stempel</span></div>
      <table class="f"><tr><td>Nama</td>{td(k.get("ttd_nama"))}</tr><tr><td>Jabatan</td>{td(k.get("ttd_jabatan"))}</tr><tr><td>Tanggal</td><td class="blank"></td></tr></table></div>
  </div>
</div>'''
    return dokumen(d["file"], h), total


def sla(d):
    k = d["klien"]
    s = open(os.path.join(ASSETS, "sa-onsite.html")).read()
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    alasan = "".join(f"<li>{x}</li>" for x in ALASAN_GANTI)
    isi = {"FILE": d["file"] + "-Service-Agreement-Onsite", "NOMOR": e(d["nomor"]), "TANGGAL": e(d["tanggal"]),
           "KLIEN": e(k["instansi"]), "ALAMAT": garis(k.get("alamat")), "TAHUN": d["tanggal"].split()[-1],
           "TTD_NAMA": garis(k.get("ttd_nama")), "TTD_JABATAN": garis(k.get("ttd_jabatan")),
           "TTD_NAMA_TD": td(k.get("ttd_nama")), "TTD_JABATAN_TD": td(k.get("ttd_jabatan")),
           "ALASAN_GANTI": alasan, "CSS": open(os.path.join(ASSETS, "onsite.css")).read()}
    for kk, v in isi.items():
        assert "{{" + kk + "}}" in s, kk
        s = s.replace("{{" + kk + "}}", v)
    assert "{{" not in s, re.findall(r"\{\{\w+\}\}", s)
    return s


def main():
    data, out = sys.argv[1], sys.argv[2]
    d = json.load(open(data))
    kode = d["nomor"].split("/")[1] if d["nomor"].count("/") >= 3 else ""
    assert re.fullmatch(r"[A-Za-z0-9]+", kode), f"kode project di nomor harus huruf & angka saja: {d['nomor']}"
    assert d["mulai"].split()[0] in BULAN, f"`mulai` harus '<Bulan> <Tahun>', mis. 'Januari 2027': {d['mulai']}"
    assert 1 <= len(d["talent"]) <= 4, "1–4 baris talent (tabel komponen per talent maksimal 4 kolom; gabungkan posisi sejenis dengan `jumlah`)"
    for c in d.get("venturo_cloud") or []:
        assert c["paket"] in CLOUD, f"paket Venturo Cloud tidak dikenal: {c['paket']}"
    if d.get("diskon"):
        assert d["diskon"].get("nama") and d["diskon"].get("nilai"), "diskon = {nama, nilai}, hanya atas instruksi pemilik"
    os.makedirs(out, exist_ok=True)
    p, total = penawaran(d)
    s = sla(d)
    for nama, isi in (("penawaran.html", p), ("sla.html", s)):
        for sisa in d.get("cek_tidak_boleh_ada", []):
            assert sisa not in isi, f"sisa teks '{sisa}' di {nama}"
        assert not re.search(r"PPN tidak ditagihkan", isi, re.I), f"pakai kalimat pajak baku di {nama}"
        open(os.path.join(out, nama), "w").write(isi)
    for a in ("logo.png", "bg_flat.jpg", "ttd.png", "paraf.png"):
        shutil.copy2(os.path.join(ASSETS, a), out)
    if not os.path.isdir(os.path.join(out, "fonts")):
        shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(out, "fonts"))
    ts, cloud, bulanan, kickoff, *_ = hitung(d)
    print(json.dumps({"nomor": d["nomor"], "durasi": f'{d["durasi_bulan"]} bulan ({periode(d)})', "management_fee": pct(ts[0]["fee"]),
                      "tarif_per_talent": {f'{t["posisi"]} ({t["kota"]} · {t["level"]})': rp(t["tarif"]) for t in ts},
                      "talent": sum(t["jumlah"] for t in ts), "kickoff_dp": rp(kickoff), "tagihan_bulanan": rp(bulanan),
                      "total_investasi": rp(total)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
