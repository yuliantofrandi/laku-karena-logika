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


# ---------- Diagram alur sistem (Lampiran bagian 1) ----------
WARNA = dict(teal="#259ead", t7="#1b7a86", t8="#176a74", t50="#eaf6f7", ink="#1f2a2e", muted="#58585a",
             border="#c9d8da", s2="#f4f7f6", amber="#b8741a", amber_bg="#fdf5ea", amber_bd="#e2b46c")


def bungkus(teks, maks):
    """Pecah teks menjadi baris ≤ maks karakter (per kata)."""
    baris, cur = [], ""
    for w in str(teks).split():
        if cur and len(cur) + 1 + len(w) > maks:
            baris.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return baris + ([cur] if cur else [])


def alur_svg(a):
    """SVG alur sistem: lajur (kolom) per aktor/sistem, langkah bernomor berurutan dengan panah,
    lajur eksternal bergaris putus oranye, sumber data di bawah, dan catatan gelap di akhir."""
    C = WARNA; W = 1000; GAP = 14; PAD = 16; HEAD = 54; ROWGAP = 34
    lajur = a["lajur"]; ids = [l["id"] for l in lajur]
    assert 2 <= len(lajur) <= 4, "alur: 2–4 lajur"
    bobot = [l.get("lebar", 0.8 if l.get("eksternal") else 1) for l in lajur]
    tot = sum(bobot); lebar_total = W - GAP * (len(lajur) - 1)
    x0, xs = 0, []
    for b in bobot:
        w = lebar_total * b / tot; xs.append((x0, w)); x0 += w + GAP
    langkah = a["langkah"]
    # baris: default berurutan; `"baris_sama": true` → satu baris dengan langkah sebelumnya
    r = -1
    for i, st in enumerate(langkah):
        assert st["lajur"] in ids, f"alur: lajur tidak dikenal '{st['lajur']}'"
        r = r if (st.get("baris_sama") and i) else r + 1
        st["_r"] = r
    nrow = r + 1
    # ukuran kotak per baris
    def isi(st):
        x, w = xs[ids.index(st["lajur"])]
        bw = w - 2 * PAD
        jt = bungkus(f'{st["_no"]}. {st["judul"]}', int(bw / 9.2))
        kt = bungkus(st.get("ket", ""), int(bw / 6.9)) if st.get("ket") else []
        return x + PAD, bw, jt, kt
    for i, st in enumerate(langkah):
        st["_no"] = i + 1
        st["_x"], st["_w"], st["_jt"], st["_kt"] = isi(st)
    tinggi = [0] * nrow
    for st in langkah:
        tinggi[st["_r"]] = max(tinggi[st["_r"]], 20 + 20 * len(st["_jt"]) + 16 * len(st["_kt"]) + 8)
    ytop = [HEAD + 8]
    for rr in range(1, nrow):
        ytop.append(ytop[-1] + tinggi[rr - 1] + ROWGAP)
    lane_bot = ytop[-1] + tinggi[-1] + 16
    o = []
    # lajur
    for (x, w), l in zip(xs, lajur):
        if l.get("eksternal"):
            o.append(f'<rect x="{x:.0f}" y="0" width="{w:.0f}" height="{lane_bot}" rx="14" fill="{C["amber_bg"]}" stroke="{C["amber_bd"]}" stroke-dasharray="7 6" stroke-width="1.5"/>')
            hc, sc = C["amber"], C["amber"]
        else:
            o.append(f'<rect x="{x:.0f}" y="0" width="{w:.0f}" height="{lane_bot}" rx="14" fill="{C["t50"] if l.get("sistem") else C["s2"]}"/>')
            hc, sc = C["t7"], C["muted"]
        cx = x + w / 2
        o.append(f'<text x="{cx:.0f}" y="25" text-anchor="middle" font-size="14" font-weight="700" letter-spacing="2" fill="{hc}">{e(l["nama"]).upper()}</text>')
        if l.get("ket"):
            o.append(f'<text x="{cx:.0f}" y="43" text-anchor="middle" font-size="11.5" fill="{sc}">{e(l["ket"])}</text>')
    # panah antar langkah berurutan
    def kotak(st):
        y = ytop[st["_r"]]; return st["_x"], y, st["_w"], tinggi[st["_r"]]
    def bebas(lj, r1, r2):  # tidak ada kotak di lajur lj pada baris di antara r1 dan r2 (eksklusif)
        return not any(s["lajur"] == lj and min(r1, r2) < s["_r"] < max(r1, r2) for s in langkah)
    def panah(d_, warna, putus=False, label=None, lx=0, ly=0):
        da = ' stroke-dasharray="6 5"' if putus else ""
        mk = "aa" if warna == C["amber"] else "at"
        o.append(f'<path d="{d_}" fill="none" stroke="{warna}" stroke-width="2.2"{da} marker-end="url(#{mk})"/>')
        if label:
            o.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="11.5" fill="{C["t7"]}">{e(label)}</text>')
    for a_, b_ in zip(langkah, langkah[1:]):
        ax, ay, aw, ah = kotak(a_); bx, by, bw, bh = kotak(b_)
        eks = any(l["id"] in (a_["lajur"], b_["lajur"]) and l.get("eksternal") for l in lajur)
        warna = C["amber"] if eks else C["t7"]; lab = b_.get("label")
        if a_["_r"] == b_["_r"]:
            y = ay + ah / 2
            celah = abs(bx - (ax + aw)) if bx > ax else abs(ax - (bx + bw))
            lab = lab if lab and len(lab) * 6.6 < celah - 6 else None
            if bx > ax:
                panah(f"M{ax + aw:.0f},{y:.0f} H{bx - 2:.0f}", warna, label=lab, lx=ax + aw + 3, ly=y - 7)
            else:
                panah(f"M{ax:.0f},{y:.0f} H{bx + bw + 2:.0f}", warna, label=lab, lx=bx + bw + 3, ly=y - 7)
        elif a_["lajur"] == b_["lajur"]:
            cx = ax + aw / 2
            panah(f"M{cx:.0f},{ay + ah:.0f} V{by - 2:.0f}", warna, label=lab, lx=cx + 8, ly=(ay + ah + by) / 2 + 4)
        else:
            sx = ax + aw / 2; tx = bx + bw / 2
            naik = b_["_r"] < a_["_r"]
            if naik:   # kembali ke atas: keluar dari sisi kotak, naik di celah lajur
                sisi = ax if tx < sx else ax + aw
                gx = sisi - PAD / 2 - GAP / 2 if tx < sx else sisi + PAD / 2 + GAP / 2
                ty = by + bh / 2
                ex = bx + bw + 4 if tx < sx else bx - 4
                panah(f"M{sisi:.0f},{ay + ah / 2:.0f} H{gx:.0f} V{ty:.0f} H{ex:.0f}", warna, putus=True, label=lab, lx=gx + 6, ly=(ay + ty) / 2)
            else:
                ya = ay + ah + ROWGAP / 2; yb = by - ROWGAP / 2
                yt = ya if bebas(b_["lajur"], a_["_r"], b_["_r"]) or not bebas(a_["lajur"], a_["_r"], b_["_r"]) else yb
                panah(f"M{sx:.0f},{ay + ah:.0f} V{yt:.0f} H{tx:.0f} V{by - 2:.0f}", warna, label=lab, lx=min(sx, tx) + 8, ly=yt - 6)
    # kotak langkah
    for st in langkah:
        x, y, w, h = kotak(st)
        eks = next(l for l in lajur if l["id"] == st["lajur"]).get("eksternal")
        if st.get("utama"):
            fill, bd, tc, kc = C["teal"], C["teal"], "#fff", "#eafafc"
        else:
            fill, bd, tc, kc = "#fff", (C["amber_bd"] if eks else C["teal"]), C["ink"], C["muted"]
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="10" fill="{fill}" stroke="{bd}" stroke-width="2"/>')
        isi_h = 20 * len(st["_jt"]) + 16 * len(st["_kt"])
        yy = y + (h - isi_h) / 2 + 14
        for t in st["_jt"]:
            o.append(f'<text x="{x + w / 2:.0f}" y="{yy:.0f}" text-anchor="middle" font-size="15" font-weight="700" fill="{tc}">{e(t)}</text>'); yy += 20
        yy += 2
        for t in st["_kt"]:
            o.append(f'<text x="{x + w / 2:.0f}" y="{yy:.0f}" text-anchor="middle" font-size="12" fill="{kc}">{e(t)}</text>'); yy += 16
    H = lane_bot
    # sumber data
    sumber = a.get("sumber") or []
    if sumber:
        y0 = H + 14; bh = 62; n = len(sumber)
        o.append(f'<rect x="0" y="{y0}" width="{W}" height="{bh + 28}" rx="14" fill="{C["s2"]}" stroke="#a9b5b7" stroke-dasharray="6 5" stroke-width="1.3"/>')
        o.append(f'<text x="22" y="{y0 + 30}" font-size="13" font-weight="700" letter-spacing="2" fill="{C["muted"]}">{e(a.get("sumber_judul", "Sumber data")).upper()}</text>')
        bw = min(300, (W - 200 - 24 * (n - 1)) / n); gx = 190 + ((W - 210) - (bw * n + 24 * (n - 1))) / 2
        for i, sb in enumerate(sumber):
            x = gx + i * (bw + 24); y = y0 + 14
            o.append(f'<rect x="{x:.0f}" y="{y}" width="{bw:.0f}" height="{bh}" rx="10" fill="#fff" stroke="#6b7072" stroke-width="1.8"/>')
            o.append(f'<text x="{x + bw / 2:.0f}" y="{y + 26}" text-anchor="middle" font-size="14" font-weight="700" fill="{C["ink"]}">{e(sb["nama"])}</text>')
            if sb.get("ket"):
                o.append(f'<text x="{x + bw / 2:.0f}" y="{y + 46}" text-anchor="middle" font-size="12" fill="{C["muted"]}">{e(sb["ket"])}</text>')
        H = y0 + bh + 28
    # catatan
    if a.get("catatan"):
        bar = bungkus(a["catatan"], 128); y0 = H + 14; hh = 22 + 19 * len(bar)
        o.append(f'<rect x="0" y="{y0}" width="{W}" height="{hh}" rx="12" fill="{C["ink"]}"/>')
        for i, t in enumerate(bar):
            o.append(f'<text x="24" y="{y0 + 28 + 19 * i}" font-size="13" fill="#fff">{e(t)}</text>')
        H = y0 + hh
    defs = "<defs>" + "".join(f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4.2" markerHeight="4.2" markerUnits="strokeWidth" orient="auto">'
                              f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for i, c in (("at", C["t7"]), ("aa", C["amber"]))) + "</defs>"
    # tinggi maks agar muat di halaman 1 setelah hero; alur panjang diperkecil proporsional
    return (f'<svg viewBox="-2 -2 {W + 4} {H + 4}" width="100%" style="display:block;max-height:{a.get("tinggi_maks_mm", 148)}mm" xmlns="http://www.w3.org/2000/svg" font-family="M, sans-serif">'
            + defs + "".join(o) + "</svg>")


def lampiran(d):
    modul, est, kuota, termin, total = hitung(d)
    h = hero(d, "Lampiran Penawaran Layanan", "Estimasi Fitur", "Lampiran", " h1s")
    h += (f'  <p class="intro">Lampiran ini merinci estimasi ukuran fitur setiap pekerjaan berdasarkan kebutuhan Klien, dan merupakan bagian tidak terpisahkan dari dokumen penawaran nomor {e(d["nomor"])}. '
          'Ukuran fitur: kecil (kurang dari 1 fitur, dinilai desimal) · standar (1 fitur) · besar (2 fitur). Setiap fitur sudah termasuk meeting analisa, rancangan aplikasi, penyesuaian (maksimal 2× revisi), dan dokumentasi.</p>\n</section>\n')
    ring = "".join(f'<tr><td>{e(m["nama"])}</td><td>{e(m.get("kategori", "Pengembangan aplikasi"))} · {e(m.get("platform", "Web"))}</td><td class="r">{fz(m["total"])}</td></tr>' for m in modul)
    pk = " + ".join(f'{b["fitur"]}' for b in d["bulan"])
    al = d["alur"]
    h += (f'<div class="keep"><h2><i>1</i>{e(al.get("judul", "Alur Sistem"))}</h2>\n'
          + (f'<p style="margin:0 0 3mm;color:var(--muted)">{e(al["pengantar"])}</p>\n' if al.get("pengantar") else "")
          + alur_svg(al) + "</div>\n")
    h += f'''<h2 style="break-before:page;margin-top:2mm"><i>2</i>Ringkasan Estimasi</h2>
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
    brk = ""
    h += f'''<h2{brk}><i>3</i>Rincian per Item Pekerjaan</h2>
<table class="est"><thead><tr><th class="c" style="width:9mm">No</th><th>Item Pekerjaan</th><th>Ukuran</th><th class="r">Fitur</th></tr></thead><tbody>{rows}
<tr class="grand"><td colspan="3">Total Estimasi</td><td class="r">{fz(est)} fitur</td></tr></tbody></table>
'''
    uk = "".join(f'<tr><td><b style="font-weight:600">{a}</b></td><td>{b}</td><td>{c}</td><td>{x}</td><td>{y}</td></tr>' for a, b, c, x, y in UKURAN)
    h += f'''<div class="keep">
<h2><i>4</i>Panduan Ukuran Fitur</h2>
<table style="font-size:8pt"><thead><tr><th style="width:24mm">Kategori</th><th>&lt; 1 fitur<br><small style="font-weight:500">Kecil</small></th><th>1 fitur<br><small style="font-weight:500">Standar</small></th><th>2 fitur<br><small style="font-weight:500">Besar</small></th><th>&gt; 2 fitur<br><small style="font-weight:500">Dipecah saat analisa</small></th></tr></thead><tbody>{uk}</tbody></table>
<p class="note" style="color:var(--muted);font-size:8.3pt;margin-top:2mm">Contoh: Modul Cuti lengkap (master + pengajuan + approval + laporan + notifikasi WA) = 1 fitur. Fitur kecil dinilai desimal sesuai besar pekerjaan (mis. tambah 1 field = 0,1 fitur). Pelatihan tambahan di luar rilis fitur: ½ hari = ½ fitur.</p>
</div>
'''
    n = 5
    if d.get("tahap_berikutnya"):
        tb = "".join(f'<tr><td>{e(x["nama"])}{" " + e(x["kondisi"]) if x.get("kondisi") else ""}</td><td class="r">{fz(x["fitur"])}</td></tr>' for x in d["tahap_berikutnya"])
        h += f'''<div class="keep">
<h2><i>5</i>Pengembangan Tahap Berikutnya <span style="font-weight:500;color:var(--subtle);font-size:9pt">(setelah rilis fitur utama)</span></h2>
<table><thead><tr><th>Item Pekerjaan</th><th class="r" style="white-space:nowrap">Estimasi Fitur</th></tr></thead><tbody>{tb}</tbody></table>
<p class="note" style="color:var(--muted)">Fitur di atas sengaja tidak dimasukkan ke rilis pertama agar fitur utama dapat dirilis lebih cepat dengan biaya yang efisien. Fitur ini dapat ditambahkan setelah rilis melalui Layanan Lanjutan atas persetujuan Klien, dan belum termasuk dalam Total Investasi. Estimasi ukuran fitur di atas dikonfirmasi ulang saat fitur akan dikerjakan.</p>
</div>
'''
        n = 6
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
    assert d.get("alur", {}).get("langkah"), "isi `alur` (lajur + langkah) untuk diagram Alur Sistem di Lampiran"
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
