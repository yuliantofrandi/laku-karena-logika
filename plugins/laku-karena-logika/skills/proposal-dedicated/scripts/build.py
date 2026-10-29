#!/usr/bin/env python3
"""Bangun 3 HTML penawaran Dedicated Team dari satu file data JSON.

  python3 build.py <data.json> <folder kerja>

Hasil di <folder kerja>: penawaran.html, lampiran.html, sla.html (+ aset yang dibutuhkan:
logo, bg, ttd, paraf, fonts). Render dengan scripts/render.py.

Yang dihitung otomatis (dan di-assert):
- Skema per posisi: Short Term bila rentang keterlibatan < 2 bulan (dari awal fase pertama sampai
  akhir fase terakhir ia terlibat), selain itu Long Term (bisa dipaksa dengan "skema" di data).
- Tarif dari PRICELIST (Long/Short Term), Engineering Kick-off = tarif Kick-off × alokasi tertinggi
  (hanya Long Term), biaya fase = tarif × orang × bulan.
- Timeline: satuan ½ bulan (tanggal 1–15 dan 16–akhir bulan); fase harus berurutan tanpa celah.
- Termin per bulan kalender (fase dengan "annual_support": true → "Maintenance n"), perjalanan dinas
  dibagi rata ke bulan tagih. Total Investasi = Kick-off + Σ fase + perjalanan = Total Pembayaran.
Lihat assets/contoh-data.json untuk format data.
"""
import datetime as dt, html, json, math, os, re, shutil, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, "assets")

# Pricelist (references/pricelist-dedicated.md). Senior & Pentester/DevOps memakai tarif yang sama,
# begitu juga Intermediate & UI/UX/QA/BA.
GRUP = {"Senior": "S", "Pentester/DevOps": "S", "Intermediate": "I", "UI/UX/QA/BA": "I"}
LABEL_LEVEL = {"Senior": "Senior", "Pentester/DevOps": "Pentester / DevOps",
               "Intermediate": "Intermediate", "UI/UX/QA/BA": "UI/UX / QA / BA"}
KICKOFF = {"S": 11_550_000, "I": 9_550_000}
TARIF = {("S", "Long Term"): 11_550_000, ("S", "Short Term"): 16_170_000,
         ("I", "Long Term"): 9_550_000, ("I", "Short Term"): 13_370_000}
KOMPONEN = [("Development Squad", 6_800_000, 5_500_000), ("Technical Lead", 1_030_000, 1_675_000),
            ("AI Subscription &amp; RND", 500_000, 500_000), ("Engineering Workspace", 500_000, 500_000),
            ("Engineering Management", 2_720_000, 1_375_000)]
ENABLEMENT = {"S": 4_620_000, "I": 3_820_000}
TRAVEL_TARIF = {"tiket": 3_500_000, "penginapan": 3_000_000, "uang_saku": 3_000_000}
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
BULAN_P = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
           "Oktober", "November", "Desember"]


def e(s): return html.escape(str(s), quote=False)
def rp(x):
    x = round(x * 2) / 2
    return "Rp" + (f"{int(x):,}" if x == int(x) else f"{x:,.1f}").replace(",", "#").replace(".", ",").replace("#", ".")
def frac(x):
    if x == 0: return "–"
    w, f = int(x), round(x - int(x), 2)
    s = {0: "", 0.25: "¼", 0.5: "½", 0.75: "¾"}.get(f)
    assert s is not None, f"pecahan tidak didukung: {x}"
    return (str(w) if w else "") + s if s else str(w)
def bold_prefix(t):  # "Judul: isi" → <b>Judul:</b> isi
    m = re.match(r"^([^:]{2,60}):\s(.+)$", t)
    return f"<b>{e(m.group(1))}:</b> {e(m.group(2))}" if m else e(t)


# ---------- waktu (slot ½ bulan) ----------
def slot_dari(tgl):
    d = dt.date.fromisoformat(tgl)
    assert d.day in (1, 16), f"fase harus mulai tanggal 1 atau 16: {tgl}"
    return (d.year * 12 + d.month - 1) * 2 + (0 if d.day == 1 else 1)
def slot_info(s):
    y, m = divmod(s // 2, 12)
    m += 1
    akhir = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return y, m, (1, 15) if s % 2 == 0 else (16, akhir)
def periode(s0, s1):  # slot awal s0 .. slot akhir s1 (inklusif)
    y0, m0, (a, _) = slot_info(s0); y1, m1, (_, b) = slot_info(s1)
    if (y0, m0) == (y1, m1): return f"{a}–{b} {BULAN[m0-1]} {y0}"
    if y0 == y1: return f"{a} {BULAN[m0-1]} – {b} {BULAN[m1-1]} {y1}"
    return f"{a} {BULAN[m0-1]} {y0} – {b} {BULAN[m1-1]} {y1}"
def periode_bulan(y, m):
    akhir = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return f"1–{akhir} {BULAN[m-1]} {y}", f"{akhir} {BULAN[m-1]} {y}"


def hitung(d):
    pos = {p["id"]: p for p in d["posisi"]}
    fase, slot = [], None
    for i, f in enumerate(d["fase"]):
        s0 = slot_dari(f["mulai"]); n = round(f["bulan"] * 2)
        assert abs(n - f["bulan"] * 2) < 1e-9, f"durasi fase harus kelipatan ½ bulan: {f['nama']}"
        assert slot is None or s0 == slot, f"fase {i+1} harus mulai tepat setelah fase sebelumnya"
        for pid in f["alokasi"]: assert pid in pos, f"posisi {pid} tidak dikenal"
        fase.append(dict(f, no=i + 1, s0=s0, s1=s0 + n - 1)); slot = s0 + n
    for p in d["posisi"]:
        assert p["level"] in GRUP, f"level tidak dikenal: {p['level']}"
        ikut = [f for f in fase if f["alokasi"].get(p["id"], 0) > 0]
        assert ikut, f"posisi {p['nama']} tidak dipakai di fase mana pun"
        rentang = (ikut[-1]["s1"] - ikut[0]["s0"] + 1) / 2
        p["skema"] = p.get("skema") or ("Short Term" if rentang < 2 else "Long Term")
        p["rentang"] = rentang
        p["maks"] = max(f["alokasi"].get(p["id"], 0) for f in fase)
        g = GRUP[p["level"]]
        p["tarif"] = TARIF[(g, p["skema"])]
        p["kickoff"] = KICKOFF[g] * p["maks"] if p["skema"] == "Long Term" else 0
    for f in fase:
        f["baris"] = [(pos[pid], a, pos[pid]["tarif"] * a * f["bulan"]) for pid, a in f["alokasi"].items() if a > 0]
        f["biaya"] = sum(x[2] for x in f["baris"])
        f["orang"] = sum(x[1] for x in f["baris"])
    kick = sum(p["kickoff"] for p in d["posisi"])
    tr = d.get("perjalanan") or {}
    items = []
    for it in tr.get("items", []):
        tarif = it.get("tarif", TRAVEL_TARIF.get(it["jenis"]))
        qty = math.ceil(it["orang"] / 2) if it["jenis"] == "penginapan" else it["orang"]
        items.append(dict(it, tarif=tarif, qty=qty, total=tarif * qty * it["unit"]))
    travel = sum(i["total"] for i in items)
    # termin per bulan kalender
    bulan = {}
    for f in fase:
        for s in range(f["s0"], f["s1"] + 1):
            y, m, _ = slot_info(s)
            b = bulan.setdefault((y, m), {"biaya": 0.0, "fase": [], "annual": False})
            b["biaya"] += sum(p["tarif"] * a * 0.5 for p, a, _ in f["baris"])
            if f["no"] not in b["fase"]: b["fase"].append(f["no"])
            b["annual"] = b["annual"] or bool(f.get("annual_support"))
    tagih = [tuple(map(int, x.split("-"))) for x in tr.get("bulan_tagih", [])]
    for k in tagih: assert k in bulan, f"bulan tagih perjalanan {k} di luar periode"
    termin, nt, nm = [], 0, 0
    for (y, m) in sorted(bulan):
        b = bulan[(y, m)]
        nominal = b["biaya"] + (travel / len(tagih) if (y, m) in tagih else 0)
        if b["annual"] and len(b["fase"]) == 1:
            nm += 1; label = f"Maintenance {nm}"
        else:
            nt += 1
            fs = b["fase"]; label = f"Termin {nt} – Fase " + (" &amp; ".join(map(str, fs)) if len(fs) > 1 else str(fs[0]))
            if (y, m) in tagih: label += " + perjalanan dinas"
        per, inv = periode_bulan(y, m)
        termin.append((per, label, inv, nominal))
    total = kick + sum(f["biaya"] for f in fase) + travel
    assert abs(total - (kick + sum(t[3] for t in termin))) < 1, "Total Investasi ≠ Total Pembayaran"
    return fase, kick, items, travel, termin, total


def hero(d, eyebrow, judul, label_no):
    k = d["klien"]
    return f'''<section class="hero">
  <img class="logo" src="logo.png" alt="Venturo Expert Programmers">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{judul}<br><span>{e(d["project"])}</span></h1>
  <div class="meta">
    <div class="card"><div class="kv"><b>{label_no}</b><span>{e(d["nomor"])}</span><b>Project</b><span>{e(d["project"])}</span><b>Tanggal</b><span>{e(d["tanggal"])}</span></div></div>
    <div class="card soft"><div class="lbl">Kepada Yth.</div><div class="to">{e(k["penerima"])}</div><div>{e(k["instansi"])}</div><div style="color:var(--muted)">{e(k["alamat"])}</div></div>
  </div>
'''


def dokumen(title, body):
    css = open(os.path.join(ASSETS, "dedicated.css")).read()
    return f'<!doctype html>\n<html lang="id"><head><meta charset="utf-8"><title>{title}</title>\n<style>\n{css}</style></head><body>\n{body}\n</body></html>\n'


SATUAN = ('<div class="unit"><b>Satuan.</b> Orang: 1 = penuh waktu (8 jam per hari kerja), ½ = 4 jam per hari kerja, '
          '¼ = 2 jam per hari kerja. Bulan: 1 = 4 minggu kerja, ½ = 2 minggu, ¼ = 1 minggu. Total = tarif per bulan × '
          'orang × bulan. Posisi Short Term hanya dilibatkan pada fase tertentu, memakai tarif short term, dan tanpa '
          'Engineering Kick-off.</div>')


def penawaran(d, fase, kick, items, travel, termin, total):
    k = d["klien"]; vc = d.get("venturo_cloud")
    tahun = d["tanggal"].split()[-1]
    h = hero(d, "Penawaran Layanan &amp; Persetujuan Kerja Sama", "Dedicated Team", "No.")
    h += f'  <p class="intro">Melalui penawaran ini, kami menegaskan kesiapan tim IT profesional kami yang berjumlah kurang lebih 100 orang untuk menyediakan tim pengembang yang bekerja khusus untuk {e(d["intro_untuk"])}. Jumlah orang dan lamanya keterlibatan setiap posisi disesuaikan dengan kebutuhan setiap fase, sehingga biaya mengikuti beban kerja yang sebenarnya.</p>\n</section>\n'
    # 1. Lingkup & timeline
    rows = "".join(
        f'<tr><td><span class="ph">Fase {f["no"]}</span> · <b>{e(f["nama"])}</b><ul class="sc">'
        + "".join(f"<li>{bold_prefix(x)}</li>" for x in f["lingkup"])
        + f'</ul></td><td style="white-space:nowrap">{periode(f["s0"], f["s1"])}<br><span style="color:var(--subtle);font-size:8pt">'
        + f'{frac(f["bulan"])} bulan{" (2 minggu)" if f["bulan"] == 0.5 else ""} · {frac(f["orang"])} orang</span></td></tr>'
        for f in fase)
    h += f'''<h2><i>1</i>Lingkup Pekerjaan &amp; Timeline</h2>
<table style="break-inside:auto">
  <thead><tr><th>Fase &amp; Lingkup Pekerjaan</th><th>Timeline</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="note" style="color:var(--muted)">{e(d.get("catatan_lingkup", "Rincian fitur per fase tercantum di Lampiran Rincian Biaya & Rencana Kerja."))} Urutan fitur dapat disesuaikan dengan prioritas Klien selama total alokasi tim pada fase tersebut tetap.</p>
'''
    # 2. Rincian biaya
    def row(nama, tarif, orang, bulan, tot):
        return (f'<tr><td>{nama}</td><td class="r">{rp(tarif)}</td><td class="c">{orang}</td>'
                f'<td class="c{" z" if bulan == "–" else ""}">{bulan}</td><td class="r">{rp(tot)}</td></tr>')
    st = lambda p: e(p["nama"]) + (" (short term)" if p["skema"] == "Short Term" else "")
    grp = lambda t, sm: f'<tr class="grp"><td colspan="5">{t} <small>{sm}</small></td></tr>'
    body = '<tbody style="break-inside:avoid">' + grp("Engineering Kick-off", "sekali bayar saat tanda tangan, posisi Long Term") + "".join(
        row(e(p["nama"]), KICKOFF[GRUP[p["level"]]], frac(p["maks"]), "–", p["kickoff"]) for p in d["posisi"] if p["kickoff"]) + "</tbody>"
    for f in fase:
        body += '<tbody style="break-inside:avoid">' + grp(f"Fase {f['no']} · {e(f['nama'])}", periode(f["s0"], f["s1"])) + "".join(
            row(st(p), p["tarif"], frac(a), frac(f["bulan"]), t) for p, a, t in f["baris"]) + "</tbody>"
    if items:
        tr = d["perjalanan"]
        body += '<tbody style="break-inside:avoid">' + grp("Perjalanan Dinas", e(tr["judul"]) + "; kolom Bulan = jumlah unit") + "".join(
            row(e(i["nama"]), i["tarif"], frac(i["qty"]), frac(i["unit"]), i["total"]) for i in items) + "</tbody>"
    if d.get("diskon"):
        body += f'<tbody><tr class="sub"><td colspan="4">Total</td><td class="r">{rp(total)}</td></tr><tr class="sub disc"><td colspan="4">{e(d["diskon"]["nama"])}</td><td class="r">– {rp(d["diskon"]["nilai"])}</td></tr></tbody>'
        total_akhir = total - d["diskon"]["nilai"]
    else:
        total_akhir = total
    body += f'<tbody><tr class="grand"><td colspan="4">Total Investasi</td><td class="r">{rp(total_akhir)}</td></tr></tbody>'
    h += f'''<h2><i>2</i>Rincian Biaya</h2>
<table class="cost">
  <thead><tr><th>Posisi / Item</th><th class="r">Tarif/Bulan</th><th class="c">Orang</th><th class="c">Bulan</th><th class="r">Total</th></tr></thead>
  {body}
</table>
{SATUAN}
<div class="svc">
  <h3>Sudah termasuk dalam biaya</h3>
  <ul>
    <li><b>Engineering Kick-off:</b> onboarding tim, kickoff &amp; roadmap, setup core Venturo, akses &amp; environment, serta transfer ilmu</li>
    <li>Tim bekerja khusus untuk proyek Klien sesuai alokasi setiap fase dan prioritas backlog Klien, didampingi Technical Lead dan Engineering Management Venturo</li>
    <li><b>Jaminan target:</b> bila target yang telah disepakati bersama tidak tercapai karena kendala dari sisi Venturo, Venturo menambah anggota tim dan/atau melakukan lembur tanpa biaya tambahan</li>
    <li>Penggantian anggota tim yang tidak sesuai kualifikasi tanpa biaya tambahan, serta dukungan teknis melalui WhatsApp</li>
    <li>Seluruh source code, basis data, konfigurasi, dan dokumentasi hasil pekerjaan menjadi milik Klien</li>
    <li>Gaji, BPJS, PPh 21, AI Subscription, dan Engineering Workspace tim ditanggung Venturo (rincian di Lampiran, bagian Sudah Ditangani Venturo)</li>
  </ul>
</div>
'''
    if vc:
        h += f'''<h3 style="font-size:10.5pt;margin:5mm 0 2mm;break-after:avoid">Layanan Berlangganan Bulanan <small style="font-weight:500;color:var(--subtle);font-size:8.5pt;margin-left:2mm">Di luar Total Investasi</small></h3>
<table>
  <thead><tr><th>Layanan</th><th>Periode</th><th class="r">Harga</th></tr></thead>
  <tbody><tr><td><b>Venturo Cloud – {e(vc["paket"])}</b><span class="d">{e(vc["deskripsi"])}</span></td><td style="white-space:nowrap">Mulai {e(vc["mulai"])}<br>per bulan</td><td class="r">{rp(vc["harga"])}<br><span style="color:var(--subtle);font-size:8pt">/bulan</span></td></tr></tbody>
</table>
'''
    # 3. Pembayaran
    ada_travel = " Biaya perjalanan dinas termasuk dalam termin bulan kunjungan." if items else ""
    vc_li = (f'  <li>Venturo Cloud (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai {e(vc["tagih_mulai"])} dan berlanjut otomatis setiap bulan hingga salah satu pihak menghentikannya dengan pemberitahuan tertulis 30 (tiga puluh) hari sebelumnya.</li>\n' if vc else "")
    dp, dp_label, termin = kick, "Down Payment – Engineering Kick-off", list(termin)
    if d.get("diskon"):  # diskon dipotong dari Down Payment; bila lebih besar, disebar rata ke termin
        nilai = d["diskon"]["nilai"]
        if nilai <= dp:
            dp -= nilai; dp_label += " (setelah diskon)"
        else:
            per = nilai / len(termin)
            termin = [(a, b + " (setelah diskon)", c, n - per) for a, b, c, n in termin]
    assert abs(dp + sum(t[3] for t in termin) - total_akhir) < 1, "Σ termin ≠ Total Pembayaran"
    trows = "".join(f'<tr><td>{p}</td><td>{l}</td><td>{i}</td><td class="r">{rp(n)}</td></tr>' for p, l, i, n in termin)
    h += f'''<h2><i>3</i>Pembayaran</h2>
<ul>
  <li>Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien.</li>
  <li>Engineering Kick-off dibayar sebagai Down Payment saat penandatanganan, sebelum periode kerja pertama dimulai.</li>
  <li>Tagihan dikirim di akhir setiap bulan sesuai alokasi tim pada bulan tersebut dan wajib dibayarkan paling lambat H+14 (empat belas) dari tanggal invoice.{ada_travel}</li>
  <li>Apabila Klien tidak melakukan pembayaran sesuai jadwal, maka seluruh aktivitas pengembangan berhak dihentikan sementara, yang dapat berdampak pada mundurnya jadwal pekerjaan.</li>
{vc_li}</ul>
<div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div>
<table class="cost">
  <thead><tr><th>Periode Kerja</th><th>Termin</th><th>Tgl Invoice</th><th class="r">Nominal</th></tr></thead>
  <tbody><tr><td>Penandatanganan</td><td>{dp_label}</td><td>Saat tanda tangan</td><td class="r">{rp(dp)}</td></tr>{trows}
  <tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(total_akhir)}</td></tr></tbody>
</table>
'''
    # 4. Batasan
    bat = list(d.get("batasan", []))
    if vc:
        bat.insert(0, "Server production di luar Venturo Cloud (apabila Klien memilih menyediakan server sendiri), serta domain")
    else:
        bat.insert(0, f"Server, perangkat keras, sistem operasi, jaringan, lisensi perangkat lunak pendukung, domain, dan sertifikat SSL untuk environment Testing/UAT dan Production disediakan {k['singkatan']} (on-premise). Environment Development dan staging memakai ekosistem Venturo")
    if items:
        bat.append("Perjalanan dinas di luar yang telah dianggarkan pada Rincian Biaya")
    bat += ["Lembur atas permintaan percepatan di luar hari dan jam kerja normal (Sabtu, Minggu, dan hari libur nasional), dengan biaya yang diajukan dan disetujui Klien sebelum pekerjaan dilakukan",
            "Tambahan waktu kerja atau perubahan alokasi tim akibat penambahan fitur, perubahan lingkup, atau perubahan timeline atas permintaan Klien akan dituangkan dalam penawaran atau addendum baru setelah disetujui kedua belah pihak"]
    h += ('<div class="keep">\n<h2><i>4</i>Batasan dan Pengecualian</h2>\n<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk biaya-biaya tambahan yang akan diajukan terlebih dahulu dan hanya berlaku setelah mendapatkan persetujuan dari Klien, yang meliputi antara lain:</p>\n<ul>\n'
          + "".join(f"  <li>{e(b)}</li>\n" for b in bat) + "</ul>\n</div>\n")
    # 5. Persetujuan
    cb = '<span style="display:inline-block;width:3.6mm;height:3.6mm;border:1px solid var(--ink);border-radius:.6mm;vertical-align:-.6mm;margin-right:2mm"></span>'
    opt = (f'<div class="opt" style="border:1px solid var(--border);border-radius:3mm;padding:3mm 4mm;margin:0 0 4mm"><div style="font-weight:600;margin-bottom:1.5mm">Pilihan Layanan Berlangganan Bulanan (centang salah satu):</div>'
           f'<div style="display:grid;grid-template-columns:118mm auto"><span>{cb}Venturo Cloud {e(vc["paket_singkat"])} {rp(vc["harga"])}/bulan mulai {e(vc["mulai_panjang"])}</span><span>{cb}Server disediakan Klien</span></div></div>\n' if vc else "")
    ttd_n = k.get("ttd_nama"); ttd_j = k.get("ttd_jabatan")
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    h += f'''<div class="sign">
  <h2 style="margin-top:8mm"><i>5</i>Persetujuan</h2>
  <p class="agree">Dengan menandatangani dokumen ini, kedua belah pihak menyatakan bahwa mereka telah membaca, memahami, dan menyetujui seluruh syarat dan ketentuan yang tercantum dalam dokumen ini, yang merupakan bagian tidak terpisahkan dari dokumen Service Agreement Venturo.</p>
{opt}<p class="place">Ditandatangani di Malang, pada tanggal ____________________ {tahun}.</p>
  <div class="sg">
    <div class="sbox"><div class="party">Penyedia Layanan</div><div class="co">PT Venturo Pro Indonesia</div>
      <div class="area"><img class="ttd" src="ttd.png" alt=""></div>
      <table class="f"><tr><td>Nama</td><td><b>Yulianto Frandi</b></td></tr><tr><td>Jabatan</td><td>CEO</td></tr><tr><td>Tanggal</td><td>{e(d["tanggal"])}</td></tr></table></div>
    <div class="sbox"><div class="party">Klien</div><div class="co">{e(k["instansi"])}</div>
      <div class="area"><span class="stamp">Tanda tangan &amp; stempel</span></div>
      <table class="f"><tr><td>Nama</td>{td(ttd_n)}</tr><tr><td>Jabatan</td>{td(ttd_j)}</tr><tr><td>Tanggal</td><td class="blank"></td></tr></table></div>
  </div>
</div>'''
    return dokumen(d["file"], h), total_akhir


def lampiran(d, fase):
    pos = d["posisi"]
    h = hero(d, "Lampiran Penawaran Layanan", "Rincian Biaya &amp; Rencana Kerja", "Lampiran")
    h += f'  <p class="intro">Lampiran ini merinci komponen biaya setiap posisi, alokasi tim pada setiap fase, serta fitur dan pekerjaan yang ditargetkan pada setiap fase{e(d.get("lampiran_intro_tambahan", ""))}.</p>\n</section>\n'
    grup = [g for g in ("S", "I") if any(GRUP[p["level"]] == g for p in pos)]
    nama_g = {"S": "Senior · Pentester / DevOps", "I": "Intermediate · UI/UX / QA / BA"}
    th1 = "".join(f'<th class="c" colspan="2">{nama_g[g]}</th>' for g in grup)
    th2 = "".join('<th class="r">Long Term</th><th class="r">Short Term</th>' for g in grup)
    kos = "<td></td>" * (2 * len(grup))
    def baris(n, f):
        return f"<tr><td>{n}</td>" + "".join(f(g) for g in grup) + "</tr>"
    rows = (f'<tr class="sub"><td style="text-align:left;color:var(--ink)">Sekali bayar</td>{kos}</tr>'
            + baris("Engineering Kick-off", lambda g: f'<td class="r">{rp(KICKOFF[g])}</td><td class="r z">–</td>')
            + f'<tr class="sub"><td style="text-align:left;color:var(--ink)">Biaya bulanan</td>{kos}</tr>'
            + "".join(baris(n, lambda g, s=s, i=i: f'<td class="r">{rp(s if g == "S" else i)}</td>' * 2) for n, s, i in KOMPONEN)
            + baris("Project Enablement Fee", lambda g: f'<td class="r z">–</td><td class="r">{rp(ENABLEMENT[g])}</td>')
            + '<tr class="grand"><td>Biaya Bulanan per Orang</td>' + "".join(f'<td class="r">{rp(TARIF[(g, "Long Term")])}</td><td class="r">{rp(TARIF[(g, "Short Term")])}</td>' for g in grup) + "</tr>")
    h += f'''<h2><i>1</i>Komponen Biaya per Orang</h2>
<table>
  <thead><tr><th rowspan="2">Komponen</th>{th1}</tr><tr>{th2}</tr></thead>
  <tbody>{rows}</tbody>
</table>
<p class="note" style="color:var(--muted)"><b>Long Term</b> untuk posisi yang terlibat 2 bulan atau lebih (dengan Engineering Kick-off). <b>Short Term</b> untuk posisi yang dibutuhkan kurang dari 2 bulan: tanpa Kick-off, dengan Project Enablement Fee untuk onboarding cepat ke proyek berjalan.</p>
{SATUAN}
'''
    kom = "".join(f'<tr><td>{e(p["nama"])}</td><td>{LABEL_LEVEL[p["level"]]} · {p["skema"]}</td><td class="c">{frac(p["maks"])}</td><td>{e(p["peran"])}</td></tr>' for p in pos)
    h += f'''<h2><i>2</i>Komposisi Tim &amp; Peran</h2>
<table style="break-inside:auto">
  <thead><tr><th>Posisi</th><th>Level &amp; Skema</th><th class="c">Alokasi Maks.</th><th>Peran</th></tr></thead>
  <tbody>{kom}</tbody>
</table>
'''
    fh = "".join(f'<th class="c">F{f["no"]}</th>' for f in fase)
    mat = "".join(f'<tr><td>{e(p["nama"])}</td>' + "".join(
        f'<td class="c">{frac(f["alokasi"].get(p["id"], 0))}</td>' if f["alokasi"].get(p["id"], 0) else '<td class="c z">–</td>' for f in fase) + "</tr>" for p in pos)
    mat += '<tr class="sub"><td style="text-align:left">Durasi (bulan)</td>' + "".join(f'<td class="c">{frac(f["bulan"])}</td>' for f in fase) + "</tr>"
    mat += '<tr class="grand"><td>Total Tim (orang)</td>' + "".join(f'<td class="c">{frac(f["orang"])}</td>' for f in fase) + "</tr>"
    leg = " · ".join(f'F{f["no"]} {e(f.get("singkat", f["nama"]))}' for f in fase)
    h += f'''<div class="keep">
<h2><i>3</i>Alokasi Tim per Fase</h2>
<table class="sm">
  <thead><tr><th>Posisi (orang)</th>{fh}</tr></thead>
  <tbody>{mat}</tbody>
</table>
<p class="note" style="color:var(--muted);font-size:8pt">{leg}.</p>
</div>
'''
    h += f'<h2 style="break-before:page"><i>4</i>Rencana Kerja &amp; Fitur per Fase</h2>\n<p style="margin:0 0 2mm;color:var(--muted)">{e(d.get("catatan_kode", "Kode F dan NF mengikuti dokumen kebutuhan Klien; LP merujuk butir Lingkup Pekerjaan."))}</p>\n'
    for f in fase:
        rows = "".join(f'<tr><td style="white-space:nowrap"><b>{e(k)}</b></td><td><b>{e(j)}</b><span class="d">{e(r)}</span></td></tr>' for k, j, r in f.get("fitur", []))
        h += (f'<div style="margin-bottom:4mm"><h3 style="font-size:10.5pt;margin:4mm 0 1mm;break-after:avoid"><span class="ph">Fase {f["no"]}</span> · {e(f["nama"])} '
              f'<small style="font-weight:500;color:var(--subtle);font-size:8.5pt;margin-left:2mm">{periode(f["s0"], f["s1"])} · {frac(f["bulan"])} bulan · {frac(f["orang"])} orang</small></h3>\n'
              f'<table class="sm" style="break-inside:auto"><thead><tr><th style="width:16mm">Kode</th><th>Fitur / Pekerjaan</th></tr></thead><tbody>{rows}</tbody></table></div>\n')
    st = [p for p in pos if p["skema"] == "Short Term"]
    st_txt = "; ".join(f'{e(p["nama"])} ({frac(p["rentang"])} bulan)' for p in st) or "tidak ada"
    h += f'''<div class="keep">
<h2><i>5</i>Sudah Ditangani Venturo</h2>
<p style="margin:0 0 2mm">Seluruh hal berikut sudah termasuk dalam biaya bulanan, sehingga Klien tidak perlu mengelolanya:</p>
<ul><li>Basic Salary &amp; THR</li><li>Benefits &amp; Allowances</li><li>BPJS Kesehatan &amp; Ketenagakerjaan</li><li>Income Tax (PPh 21) &amp; kompensasi PKWT</li><li>Employee Engagement Program</li><li>Talent Development &amp; Performance Management</li></ul>
</div>
<div class="keep">
<h2><i>6</i>Asumsi &amp; Catatan</h2>
<ul>
  <li>Komposisi dan alokasi tim disusun dari kebutuhan pada dokumen Klien dan dapat disesuaikan bersama sebelum penandatanganan.</li>
  <li>Engineering Kick-off ditagih sekali untuk setiap posisi Long Term sesuai alokasi tertingginya (mis. alokasi tertinggi ½ orang = ½ × tarif Kick-off).</li>
  <li>Posisi Short Term: {st_txt}.</li>
  <li>Urutan fitur dapat disesuaikan dengan prioritas Klien selama total alokasi tim pada fase tersebut tetap.</li>
{"".join(f"  <li>{e(x)}</li>{chr(10)}" for x in d.get("asumsi", []))}</ul>
</div>'''
    return dokumen(d["file"] + "-Lampiran-Rincian-Biaya", h)


def sla(d):
    k = d["klien"]; vc = d.get("venturo_cloud")
    s = open(os.path.join(ASSETS, "sa-dedicated.html")).read()
    blank = "______________________"
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    isi = {"FILE": d["file"], "NOMOR": e(d["nomor"]), "TANGGAL": e(d["tanggal"]), "KLIEN": e(k["instansi"]),
           "ALAMAT": e(k["alamat"]), "TAHUN": d["tanggal"].split()[-1],
           "TTD_NAMA": e(k.get("ttd_nama") or blank), "TTD_JABATAN": e(k.get("ttd_jabatan") or blank),
           "TTD_NAMA_TD": td(k.get("ttd_nama")), "TTD_JABATAN_TD": td(k.get("ttd_jabatan")),
           "PRODUCTION_VC": ", atau melalui layanan Venturo Cloud apabila dipilih Klien pada Penawaran Layanan." if vc else ".",
           "TERMINASI_VC": "<li>Penghentian Venturo Cloud mengikuti ketentuan pemberitahuan 30 (tiga puluh) hari sebagaimana diatur dalam Penawaran Layanan.</li>" if vc else ""}
    for kk, v in isi.items():
        assert "{{" + kk + "}}" in s, kk
        s = s.replace("{{" + kk + "}}", v)
    assert "{{" not in s, re.findall(r"\{\{\w+\}\}", s)
    return s


def main():
    data, out = sys.argv[1], sys.argv[2]
    d = json.load(open(data))
    os.makedirs(out, exist_ok=True)
    fase, kick, items, travel, termin, total = hitung(d)
    p, total_akhir = penawaran(d, fase, kick, items, travel, termin, total)
    l = lampiran(d, fase); s = sla(d)
    for nama, isi in (("penawaran.html", p), ("lampiran.html", l), ("sla.html", s)):
        for sisa in d.get("cek_tidak_boleh_ada", []):
            assert sisa not in isi, f"sisa teks '{sisa}' di {nama}"
        assert "PPN tidak ditagihkan" not in isi
        open(os.path.join(out, nama), "w").write(isi)
    for a in ("logo.png", "bg_flat.jpg", "ttd.png", "paraf.png"):
        shutil.copy2(os.path.join(ASSETS, a), out)
    if not os.path.isdir(os.path.join(out, "fonts")):
        shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(out, "fonts"))
    print(json.dumps({"nomor": d["nomor"], "kickoff": rp(kick), "tim": rp(sum(f["biaya"] for f in fase)),
                      "perjalanan_dinas": rp(travel), "total_investasi": rp(total_akhir),
                      "fase": [f"F{f['no']} {f['nama']}: {periode(f['s0'], f['s1'])} · {frac(f['orang'])} orang · {rp(f['biaya'])}" for f in fase],
                      "short_term": [f"{p['nama']} ({frac(p['rentang'])} bln)" for p in d["posisi"] if p["skema"] == "Short Term"],
                      "termin": len(termin)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
