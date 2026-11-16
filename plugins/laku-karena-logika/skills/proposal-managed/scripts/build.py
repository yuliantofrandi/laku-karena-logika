#!/usr/bin/env python3
"""Bangun 3 HTML penawaran Managed Service (berbasis kuota fitur) dari satu file data JSON.

  python3 build.py <data.json> <folder kerja>

Hasil di <folder kerja>: penawaran.html, lampiran.html, sla.html (+ logo, bg, ttd, paraf, fonts).
Render dengan scripts/render.py.

Yang dihitung otomatis (dan di-assert):
- Harga paket bulanan dari PAKET (references/paket-fitur.md); Setup Awal Rp10.000.000 sekali bayar.
- Ukuran setiap item: < 1 fitur Kecil (desimal), 1 Standar, > 1 s.d. 2 Besar; > 2 wajib dipecah.
- Total estimasi ≤ kuota paket; cadangan = kuota − estimasi (peringatan bila < 5%).
- Periode bulan kalender mulai tanggal 1, invoice akhir bulan; Total Investasi = Σ termin.
- Layanan Lanjutan (default 2 fitur/bulan) mulai bulan setelah periode terakhir; Venturo Cloud
  (opsional) mulai bulan terakhir periode (1 bulan sebelum go-live).
Lihat assets/contoh-data.json untuk format data.
"""
import calendar, html, json, os, re, shutil, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, "assets")

PAKET = {2: 7_500_000, 4: 14_000_000, 6: 19_500_000, 8: 24_000_000, 10: 27_500_000}   # kuota fitur/bulan → harga
SETUP = 10_000_000
CLOUD = {
    "shared-mini": ("Shared Hosting Mini", "1 CPU · 2 GB RAM · 5 GB", 200_000),
    "shared-small": ("Shared Hosting Small", "2 CPU · 3 GB RAM · 5 GB", 350_000),
    "shared-medium": ("Shared Hosting Medium", "2 CPU · 4 GB RAM · 5 GB", 600_000),
    "vps-mini": ("VPS Cloud Server Mini", "2 vCPU · 4 GB RAM · 32 GB", 800_000),
    "vps-small": ("VPS Cloud Server Small", "4 vCPU · 4 GB RAM · 32 GB", 900_000),
    "vps-medium": ("VPS Cloud Server Medium", "4 vCPU · 8 GB RAM · 32 GB", 1_050_000),
    "vps-large": ("VPS Cloud Server Large", "6 vCPU · 8 GB RAM · 32 GB", 1_150_000),
}
KATEGORI = ["Pengembangan aplikasi", "Otomasi & AI", "Integrasi sistem", "Pengelolaan data"]
# Panduan ukuran fitur (deck "Ukuran Fitur – Contoh per Kategori")
UKURAN = [
    ("Pengembangan aplikasi", "Tambahan pada modul yang ada: laporan baru, field, atau alur approval",
     "1 modul utuh: master + transaksi + approval + laporan + notifikasi (mis. Modul Cuti)",
     "Beberapa transaksi saling terkait (mis. PO → penerimaan → stok)", "Sistem besar (mis. akuntansi, payroll)"),
    ("Otomasi &amp; AI", "Tambahan pada otomasi yang ada: notifikasi WA baru, ubah prompt",
     "1 otomasi utuh: workflow n8n / pengingat terjadwal (mis. reminder tagihan)",
     "Chatbot AI untuk 1 alur bisnis (mis. cek status pesanan)", "AI agent multi-alur yang terhubung ke beberapa sistem"),
    ("Integrasi sistem", "Tambahan pada integrasi yang ada / webhook ke 1 endpoint",
     "1 integrasi utuh: API pihak ketiga, login SSO, atau payment gateway",
     "Integrasi dua arah dengan 1 sistem (mis. marketplace)", "Integrasi ERP / sinkronisasi real-time banyak sistem"),
    ("Pengelolaan data", "Tambahan pada data yang ada: import Excel, koreksi &amp; rapikan data",
     "1 migrasi utuh: data 1 modul dari sistem lama", "Migrasi beberapa modul + validasi data", "Migrasi seluruh sistem lama"),
]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def e(s): return html.escape(str(s), quote=False)
BLANK = "______________________"
def garis(v): return e(v) if v else BLANK
def rp(x):
    x = round(x)
    return "Rp" + f"{x:,}".replace(",", ".")
def jt(x):
    return "Rp" + f"{x / 1_000_000:g}".replace(".", ",") + " jt"
def fz(x):  # 0.5 → "0,5"; 12.0 → "12"
    return f"{round(x, 2):g}".replace(".", ",")
def ukuran(f):
    assert 0 < f <= 2, f"ukuran item {f} fitur: item di atas 2 fitur dipecah menjadi beberapa item"
    return "Kecil" if f < 1 else "Standar" if f == 1 else "Besar"


def bulan_ke(mulai, i):
    nm, th = mulai.split()
    b = BULAN.index(nm) + i
    return b % 12, int(th) + b // 12


def periode(mulai, i):
    b, th = bulan_ke(mulai, i)
    return f"1–{calendar.monthrange(th, b + 1)[1]} {BLN[b]} {th}", f"{calendar.monthrange(th, b + 1)[1]} {BLN[b]} {th}", b, th


def hero(d, eyebrow, judul, label_no, kelas=""):
    k = d["klien"]
    return f'''<section class="hero{kelas}">
  <img class="logo" src="logo.png" alt="Venturo Expert Programmers">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{judul}<br><span>{e(d["project"])}</span></h1>
  <div class="meta">
    <div class="card"><div class="kv"><b>{label_no}</b><span>{e(d["nomor"])}</span><b>Project</b><span>{e(d["project"])}</span><b>Tanggal</b><span>{e(d["tanggal"])}</span></div></div>
    <div class="card soft"><div class="lbl">Kepada Yth.</div><div class="to">{garis(k.get("penerima"))}</div><div>{e(k["instansi"])}</div><div style="color:var(--muted)">{garis(k.get("alamat"))}</div></div>
  </div>
'''


def dokumen(title, body):
    css = open(os.path.join(ASSETS, "managed.css")).read()
    return f'<!doctype html>\n<html lang="id"><head><meta charset="utf-8"><title>{title}</title>\n<style>\n{css}</style></head><body>\n{body}\n</body></html>\n'


def hitung(d):
    for b in d["bulan"]:
        assert b["fitur"] in PAKET, f"paket {b['fitur']} fitur tidak ada (pilihan: {sorted(PAKET)})"
    kuota = sum(b["fitur"] for b in d["bulan"])
    modul = []
    for m in d["modul"]:
        for it in m["item"]:
            ukuran(it["fitur"])
        modul.append(dict(m, total=sum(it["fitur"] for it in m["item"])))
    est = round(sum(m["total"] for m in modul), 2)
    assert est <= kuota, f"estimasi {fz(est)} fitur melebihi kuota paket {kuota} fitur — tambah bulan/naikkan paket"
    termin = [("Penandatanganan", "Setup Awal", "Saat tanda tangan", SETUP)]
    for i, b in enumerate(d["bulan"]):
        per, inv, *_ = periode(d["mulai"], i)
        termin.append((f'{per} – {b["fitur"]} fitur', f"Termin {i + 1}", inv, PAKET[b["fitur"]]))
    total = sum(t[3] for t in termin)
    return modul, est, kuota, termin, total


def lanjutan(d):
    """(fitur, harga, tanggal mulai Layanan Lanjutan, tanggal invoice pertama) dan Venturo Cloud."""
    n = len(d["bulan"])
    ll = d.get("layanan_lanjutan") or {}
    fl = ll.get("fitur", 2); assert fl in PAKET
    b, th = bulan_ke(d["mulai"], n)
    ll_mulai = (f"1 {BULAN[b]} {th}", f"{calendar.monthrange(th, b + 1)[1]} {BULAN[b]} {th}", f"1 {BLN[b]} {th}")
    vc = d.get("venturo_cloud")
    vc_info = None
    if vc:
        assert vc["paket"] in CLOUD, f"paket Venturo Cloud tidak dikenal: {vc['paket']}"
        b, th = bulan_ke(d["mulai"], n - 1)
        vc_info = (CLOUD[vc["paket"]], f"1 {BULAN[b]} {th}", f"{calendar.monthrange(th, b + 1)[1]} {BULAN[b]} {th}", f"1 {BLN[b]} {th}", vc.get("keterangan", ""))
    return fl, PAKET[fl], ll_mulai, ll.get("keterangan", ""), vc_info


def penawaran(d):
    k = d["klien"]; tahun = d["tanggal"].split()[-1]
    modul, est, kuota, termin, total = hitung(d)
    fl, hl, ll_mulai, ll_ket, vc = lanjutan(d)
    h = hero(d, "Penawaran Layanan &amp; Persetujuan Kerja Sama", "Managed Service", "No.")
    h += ('  <p class="intro">Melalui penawaran ini, kami menegaskan kesiapan tim IT profesional kami yang berjumlah kurang lebih 100 orang '
          'untuk membangun, mengembangkan, dan memelihara aplikasi Klien secara berkelanjutan. Dokumen ini memuat ruang lingkup layanan, output, '
          'dan rincian biaya sebagai acuan kesepakatan bersama kedua belah pihak.</p>\n</section>\n')
    box = lambda judul, ket, isi: (f'<div class="svc"><h3>{judul} <small>{ket}</small></h3><ul>'
                                   + "".join(f"<li>{x}</li>" for x in isi) + "</ul></div>\n")
    fondasi = ("Audit Sistem: kode, database, dan server ditinjau agar tim memahami kondisi aplikasi Klien" if d.get("aplikasi_berjalan")
               else "Setup Core Venturo: boilerplate Venturo sebagai fondasi aplikasi")
    h += '<h2><i>1</i>Lingkup Layanan</h2>\n'
    h += box("Setup Awal", "Sekali bayar, tidak memotong kuota fitur", [
        "Kickoff &amp; Roadmap: menyamakan tujuan dan menyusun roadmap pertama bersama Klien", fondasi,
        "Akses &amp; Deployment: repository, staging, dan alur deployment ditata agar setiap rilis lebih aman",
        "Backup &amp; Keamanan: backup, monitoring, dan pengamanan dasar disiapkan sejak awal",
        "Dokumentasi &amp; Transfer Ilmu: sistem didokumentasikan dan dipelajari tim, tidak bergantung pada satu orang"])
    h += box("Managed Service", "Paket kuota fitur bulanan", [
        "Setiap permintaan diukur dalam satuan fitur, dan ukurannya disepakati sebelum mulai dikerjakan",
        "Ukuran fitur: kecil (kurang dari 1 fitur, dinilai desimal, mis. tambah 1 field = 0,1 fitur), standar (1 fitur, mis. 1 modul utuh: master, transaksi, approval, laporan, dan notifikasi), dan besar (2 fitur, mis. beberapa transaksi yang saling terkait); kebutuhan di atas 2 fitur dipecah saat meeting analisa",
        "1 fitur sudah termasuk meeting analisa, rancangan aplikasi, penyesuaian (maksimal 2× revisi), dan dokumentasi",
        "Kuota fitur dapat dipakai untuk pengembangan aplikasi, otomasi &amp; AI, integrasi sistem, dan pengelolaan data",
        "Ukuran setiap fitur tercantum pada Lampiran Estimasi Fitur dokumen ini",
        "Apabila pengerjaan melebihi ukuran yang disepakati, selisihnya ditanggung Venturo dan tidak memotong kuota",
        "Pelatihan tambahan di luar rilis fitur: ½ hari setara ½ fitur; pelatihan onsite ditambah biaya perjalanan",
        "Progres dilaporkan setiap hari dan direkap setiap bulan beserta pemakaian kuota fitur",
        "Sisa kuota fitur yang tidak terpakai hangus di akhir periode"])
    h += box("Sudah Termasuk di Semua Paket", "Tanpa memotong kuota fitur", [
        "Garansi perbaikan bug tanpa biaya", "Testing dan UAT di staging setiap rilis",
        "Bantuan penggunaan aplikasi dan help desk grup WhatsApp khusus", "Pelatihan pengguna saat rilis fitur",
        "Penanganan isu kritis sebagai prioritas utama", "Koordinasi dengan vendor pihak ketiga", "Dokumentasi aplikasi"])
    # 2. Rincian Biaya
    rows = f'<tr><td><b>Setup Awal</b></td><td>Sekali bayar</td><td class="c">–</td><td class="r">{rp(SETUP)}</td></tr>'
    for i, b in enumerate(d["bulan"]):
        per = periode(d["mulai"], i)[0]
        rows += (f'<tr><td><b>Managed Service – Bulan {i + 1}</b><span class="d">{e(b["ringkasan"])}</span></td>'
                 f'<td style="white-space:nowrap">{per}</td><td class="c">{b["fitur"]}</td><td class="r">{rp(PAKET[b["fitur"]])}</td></tr>')
    sub = (f'<tr><td><b>Managed Service – Pemeliharaan &amp; Pengembangan Lanjutan</b><span class="d">{e(ll_ket) or "Penyesuaian dan pengembangan fitur, dukungan pengelolaan data, pembaruan sistem, serta pemeliharaan keamanan aplikasi."} Paket dapat dinaikkan atau diturunkan mengikuti kebutuhan.</span></td>'
           f'<td style="white-space:nowrap">Mulai {ll_mulai[2]}<br>per bulan</td><td class="c">{fl}</td><td class="r">{rp(hl)}<br><span style="color:var(--subtle);font-size:8pt">/bulan</span></td></tr>')
    if vc:
        (nama, spek, harga), mulai, _, mulai_s, ket = vc
        devops = ", termasuk dukungan tim DevOps: monitoring, konfigurasi, optimasi, dan patching" if nama.startswith("VPS") else ""
        sub += (f'<tr><td><b>Venturo Cloud – {nama}</b><span class="d">{e(ket) or "Server production aplikasi"} ({spek}){devops}. Paket dapat di-upgrade sesuai pertumbuhan pengguna. Dimulai satu bulan sebelum go-live.</span></td>'
                f'<td style="white-space:nowrap">Mulai {mulai_s}<br>per bulan</td><td class="c">–</td><td class="r">{rp(harga)}<br><span style="color:var(--subtle);font-size:8pt">/bulan</span></td></tr>')
    pk = " · ".join(f"{f} fitur {jt(v)}" for f, v in PAKET.items())
    h += f'''<h2><i>2</i>Rincian Biaya</h2>
<table>
  <thead><tr><th>Layanan</th><th>Periode</th><th class="c">Fitur</th><th class="r">Harga</th></tr></thead>
  <tbody>{rows}<tr class="grand"><td colspan="3">Total Investasi</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
<p style="margin:2mm 0 0;color:var(--muted);font-size:8.3pt">Harga paket per bulan: {pk}. Paket dapat disesuaikan setiap bulan mengikuti fase bisnis Klien.</p>
<h3 style="font-size:10.5pt;margin:5mm 0 2mm">Layanan Berlangganan Bulanan <small style="font-weight:500;color:var(--subtle);font-size:8.5pt;margin-left:2mm">Di luar Total Investasi</small></h3>
<table>
  <thead><tr><th>Layanan</th><th>Periode</th><th class="c">Fitur</th><th class="r">Harga</th></tr></thead>
  <tbody>{sub}</tbody>
</table>
'''
    # 3. Pembayaran
    trows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="r">{rp(x)}</td></tr>' for a, b, c, x in termin)
    vc_li = (f'<li>Venturo Cloud (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai {vc[2]} dengan ketentuan perpanjangan dan penghentian yang sama dengan Layanan Lanjutan.</li>' if vc else "")
    h += f'''<h2><i>3</i>Pembayaran</h2>
<ul>
  <li>Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien.</li>
  <li>Tagihan dikirim sesuai tanggal invoice dan wajib dibayarkan paling lambat H+14 (empat belas) dari tanggal invoice.</li>
  <li>Pekerjaan Setup Awal dimulai setelah pembayaran pertama diterima.</li>
  <li>Apabila Klien tidak melakukan pembayaran sesuai jadwal, maka seluruh aktivitas layanan berhak dihentikan sementara.</li>
  <li>Layanan Lanjutan (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai {ll_mulai[1]} dan berlanjut otomatis setiap bulan hingga salah satu pihak menghentikannya dengan pemberitahuan tertulis 30 (tiga puluh) hari sebelumnya.</li>
  {vc_li}
</ul>
<div class="keep"><div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div>
<table>
  <thead><tr><th>Periode Kerja</th><th>Termin</th><th>Tgl Invoice</th><th class="r">Nominal</th></tr></thead>
  <tbody>{trows}<tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
</div>
'''
    # 4. Batasan
    akhir_b, akhir_t = bulan_ke(d["mulai"], len(d["bulan"]) - 1)
    bat = ["Server production di luar Venturo Cloud (apabila Klien memilih menyediakan server sendiri), serta domain"] + list(d.get("batasan", []))
    if d.get("tahap_berikutnya"):
        nama = ", ".join(x.get("singkat", x["nama"]) for x in d["tahap_berikutnya"])
        bat.append(f"{e(nama)} direncanakan pada pengembangan tahap berikutnya setelah rilis fitur utama (lihat Lampiran Estimasi Fitur)")
    bat += ["Out-of-pocket (seperti transportasi dan akomodasi) untuk pekerjaan atau pelatihan di lokasi yang dilakukan atas permintaan Klien",
            "Permintaan pengerjaan mendesak di luar hari dan jam kerja normal (Sabtu, Minggu, dan hari libur nasional) dihitung 2× dari ukuran fitur normal",
            f"Pemeliharaan setelah periode {BULAN[akhir_b]} {akhir_t} mengikuti ketentuan Layanan Lanjutan pada bagian 2",
            "Permintaan pekerjaan di luar kuota fitur dalam dokumen ini akan dituangkan dalam penawaran atau kontrak baru setelah disetujui kedua belah pihak"]
    h += ('<div class="keep">\n<h2><i>4</i>Batasan dan Pengecualian</h2>\n<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk biaya-biaya tambahan yang akan diajukan terlebih dahulu dan hanya berlaku setelah mendapatkan persetujuan dari Klien, yang meliputi antara lain:</p>\n<ul>\n'
          + "".join(f"  <li>{x}</li>\n" for x in bat) + "</ul>\n</div>\n")
    # 5. Persetujuan
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    opsi = (f'<div style="display:grid;grid-template-columns:118mm auto"><span><span class="box"></span>Lanjutkan Managed Service {fl} fitur/bulan mulai {ll_mulai[0]}</span>'
            f'<span><span class="box"></span>Diputuskan kemudian</span></div>')
    if vc:
        opsi += (f'<div style="display:grid;grid-template-columns:118mm auto;margin-top:1.5mm"><span><span class="box"></span>Venturo Cloud {vc[0][0].replace("Cloud Server ", "")} {rp(vc[0][2])}/bulan mulai {vc[1]}</span>'
                 f'<span><span class="box"></span>Server disediakan Klien</span></div>')
    h += f'''<div class="sign">
  <h2 style="margin-top:8mm"><i>5</i>Persetujuan</h2>
  <p class="agree">Dengan menandatangani dokumen ini, kedua belah pihak menyatakan bahwa mereka telah membaca, memahami, dan menyetujui seluruh syarat dan ketentuan yang tercantum dalam dokumen ini, yang merupakan bagian tidak terpisahkan dari dokumen Service Agreement Venturo.</p>
  <div class="opt" style="border:1px solid var(--border);border-radius:3mm;padding:3mm 4mm;margin:0 0 4mm"><div style="font-weight:600;margin-bottom:1.5mm">Pilihan Layanan Berlangganan Bulanan (centang salah satu pada tiap baris):</div>
{opsi}</div>
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


def lampiran(d):
    modul, est, kuota, termin, total = hitung(d)
    h = hero(d, "Lampiran Penawaran Layanan", "Estimasi Fitur", "Lampiran", " h1s")
    h += (f'  <p class="intro">Lampiran ini merinci estimasi ukuran fitur setiap pekerjaan berdasarkan kebutuhan Klien, dan merupakan bagian tidak terpisahkan dari dokumen penawaran nomor {e(d["nomor"])}. '
          'Ukuran fitur: kecil (kurang dari 1 fitur, dinilai desimal) · standar (1 fitur) · besar (2 fitur). Setiap fitur sudah termasuk meeting analisa, rancangan aplikasi, penyesuaian (maksimal 2× revisi), dan dokumentasi.</p>\n</section>\n')
    ring = "".join(f'<tr><td>{e(m["nama"])}</td><td>{e(m.get("kategori", "Pengembangan aplikasi"))} · {e(m.get("platform", "Web"))}</td><td class="r">{fz(m["total"])}</td></tr>' for m in modul)
    pk = " + ".join(f'{b["fitur"]}' for b in d["bulan"])
    h += f'''<h2><i>1</i>Ringkasan Estimasi</h2>
<table><thead><tr><th>Modul</th><th>Kategori · Platform</th><th class="r">Fitur</th></tr></thead><tbody>{ring}
<tr class="sub"><td colspan="2">Total estimasi</td><td class="r">{fz(est)} fitur</td></tr>
<tr class="sub"><td colspan="2">Kuota paket Managed Service ({len(d["bulan"])} bulan: {pk} fitur)</td><td class="r">{kuota} fitur</td></tr>
<tr class="sub"><td colspan="2">Cadangan penyesuaian &amp; hasil UAT</td><td class="r">{fz(kuota - est)} fitur</td></tr>
</tbody></table>
'''
    rows = ""; no = 0
    for m in modul:
        rows += f'<tr class="mh"><td colspan="3">{e(m["nama"])} <span style="font-weight:500;color:var(--subtle)">· {e(m.get("platform", "Web"))}</span></td><td class="r">{fz(m["total"])} fitur</td></tr>'
        for it in m["item"]:
            no += 1
            rows += f'<tr><td class="c">{no}</td><td>{e(it["nama"])}</td><td class="k">{ukuran(it["fitur"])}</td><td class="r">{fz(it["fitur"])}</td></tr>'
    brk = ' style="break-before:page;margin-top:2mm"' if no > 12 else ""
    h += f'''<h2{brk}><i>2</i>Rincian per Item Pekerjaan</h2>
<table class="est"><thead><tr><th class="c" style="width:9mm">No</th><th>Item Pekerjaan</th><th>Ukuran</th><th class="r">Fitur</th></tr></thead><tbody>{rows}
<tr class="grand"><td colspan="3">Total Estimasi</td><td class="r">{fz(est)} fitur</td></tr></tbody></table>
'''
    uk = "".join(f'<tr><td><b style="font-weight:600">{a}</b></td><td>{b}</td><td>{c}</td><td>{x}</td><td>{y}</td></tr>' for a, b, c, x, y in UKURAN)
    h += f'''<div class="keep">
<h2><i>3</i>Panduan Ukuran Fitur</h2>
<table style="font-size:8pt"><thead><tr><th style="width:24mm">Kategori</th><th>&lt; 1 fitur<br><small style="font-weight:500">Kecil</small></th><th>1 fitur<br><small style="font-weight:500">Standar</small></th><th>2 fitur<br><small style="font-weight:500">Besar</small></th><th>&gt; 2 fitur<br><small style="font-weight:500">Dipecah saat analisa</small></th></tr></thead><tbody>{uk}</tbody></table>
<p class="note" style="color:var(--muted);font-size:8.3pt;margin-top:2mm">Contoh: Modul Cuti lengkap (master + pengajuan + approval + laporan + notifikasi WA) = 1 fitur. Fitur kecil dinilai desimal sesuai besar pekerjaan (mis. tambah 1 field = 0,1 fitur). Pelatihan tambahan di luar rilis fitur: ½ hari = ½ fitur.</p>
</div>
'''
    n = 4
    if d.get("tahap_berikutnya"):
        tb = "".join(f'<tr><td>{e(x["nama"])}{" " + e(x["kondisi"]) if x.get("kondisi") else ""}</td><td class="r">{fz(x["fitur"])}</td></tr>' for x in d["tahap_berikutnya"])
        h += f'''<div class="keep">
<h2><i>4</i>Pengembangan Tahap Berikutnya <span style="font-weight:500;color:var(--subtle);font-size:9pt">(setelah rilis fitur utama)</span></h2>
<table><thead><tr><th>Item Pekerjaan</th><th class="r" style="white-space:nowrap">Estimasi Fitur</th></tr></thead><tbody>{tb}</tbody></table>
<p class="note" style="color:var(--muted)">Fitur di atas sengaja tidak dimasukkan ke rilis pertama agar fitur utama dapat dirilis lebih cepat dengan biaya yang efisien. Fitur ini dapat ditambahkan setelah rilis melalui Layanan Lanjutan atas persetujuan Klien, dan belum termasuk dalam Total Investasi. Estimasi ukuran fitur di atas dikonfirmasi ulang saat fitur akan dikerjakan.</p>
</div>
'''
        n = 5
    asumsi = ["Estimasi disusun dari kebutuhan Klien; ukuran setiap permintaan disepakati di awal sebelum dikerjakan.",
              "Perubahan atau penambahan lingkup di luar kebutuhan awal dihitung ulang dan memotong cadangan kuota, atau dituangkan dalam penawaran baru.",
              "Apabila pengerjaan melebihi ukuran yang disepakati, selisihnya ditanggung Venturo dan tidak memotong kuota."] + list(d.get("asumsi", [])) + [
              "Jaminan kualitas (testing, UAT, dan garansi bug), dukungan, pelatihan saat rilis, dan dokumentasi sudah termasuk dan tidak memotong kuota fitur."]
    h += f'<div class="keep">\n<h2><i>{n}</i>Asumsi &amp; Catatan</h2>\n<ul>\n' + "".join(f"  <li>{e(x)}</li>\n" for x in asumsi) + "</ul>\n</div>\n"
    return dokumen(d["file"] + "-Lampiran-Estimasi", h)


def sla(d):
    k = d["klien"]
    s = open(os.path.join(ASSETS, "sa-managed.html")).read()
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    isi = {"FILE": d["file"] + "-Service-Agreement", "NOMOR": e(d["nomor"]), "TANGGAL": e(d["tanggal"]),
           "KLIEN": e(k["instansi"]), "ALAMAT": garis(k.get("alamat")), "TAHUN": d["tanggal"].split()[-1],
           "TTD_NAMA": garis(k.get("ttd_nama")), "TTD_JABATAN": garis(k.get("ttd_jabatan")),
           "TTD_NAMA_TD": td(k.get("ttd_nama")), "TTD_JABATAN_TD": td(k.get("ttd_jabatan")),
           "CSS": open(os.path.join(ASSETS, "managed.css")).read()}
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
    assert d["mulai"].split()[0] in BULAN, f"`mulai` harus '<Bulan> <Tahun>', mis. 'November 2026': {d['mulai']}"
    for m in d["modul"]:
        assert m.get("kategori", KATEGORI[0]) in KATEGORI, f"kategori tidak dikenal: {m.get('kategori')} (pilihan: {KATEGORI})"
    os.makedirs(out, exist_ok=True)
    p, total = penawaran(d)
    docs = (("penawaran.html", p), ("lampiran.html", lampiran(d)), ("sla.html", sla(d)))
    for nama, isi in docs:
        for sisa in d.get("cek_tidak_boleh_ada", []):
            assert sisa not in isi, f"sisa teks '{sisa}' di {nama}"
        for larang in (r"PPN tidak ditagihkan", r"Delivery Point", r"\bPoin\b", r"GitLab", r"lebih dari 100 orang", r"\bMVP\b"):
            assert not re.search(larang, isi), f"istilah lama/dilarang '{larang}' di {nama}"
        open(os.path.join(out, nama), "w").write(isi)
    for a in ("logo.png", "bg_flat.jpg", "ttd.png", "paraf.png"):
        shutil.copy2(os.path.join(ASSETS, a), out)
    if not os.path.isdir(os.path.join(out, "fonts")):
        shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(out, "fonts"))
    modul, est, kuota, termin, total = hitung(d)
    fl, hl, ll_mulai, _, vc = lanjutan(d)
    cad = kuota - est
    print(json.dumps({"nomor": d["nomor"], "estimasi_fitur": fz(est), "kuota_fitur": kuota, "cadangan_fitur": fz(cad),
                      "peringatan_cadangan": (f"cadangan {fz(cad)} fitur < 5% kuota" if cad < 0.05 * kuota else None),
                      "per_modul": {m["nama"]: fz(m["total"]) for m in modul},
                      "termin": [f"{b}: {rp(x)}" for _, b, _, x in termin], "total_investasi": rp(total),
                      "layanan_lanjutan": f"{fl} fitur {rp(hl)}/bulan mulai {ll_mulai[0]}",
                      "venturo_cloud": (f"{vc[0][0]} {rp(vc[0][2])}/bulan mulai {vc[1]}" if vc else None)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
