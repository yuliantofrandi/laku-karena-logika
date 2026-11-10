#!/usr/bin/env python3
"""Bangun 2 HTML penawaran Paket Website dari satu file data JSON.

  python3 build.py <data.json> <folder kerja>

Hasil di <folder kerja>: penawaran.html dan sla.html (+ logo, bg, ttd, paraf, fonts).
Render dengan scripts/render.py.

Yang dihitung otomatis (dan di-assert):
- Harga, perpanjangan, waktu kerja, dan isi paket dari PAKET (references/paket-website.md).
- Kartu perbandingan: paket satu keluarga (Company Profile atau Toko Online), paket pilihan diberi
  "Rekomendasi kami".
- Pembayaran 50% Down Payment saat tanda tangan + 50% pelunasan sebelum go-live; Total = Σ termin.
- Diskon (hanya bila pemilik/CEO menyebutnya) maksimal 10% dan wajib punya imbalan.
Lihat assets/contoh-data.json untuk format data.
"""
import html, json, os, re, shutil, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL, "assets")

# Daftar harga 2026 (references/paket-website.md). Harga paket sudah termasuk tahun pertama.
PAKET = {
    "landing-page": dict(nama="Landing Page", keluarga="cp", tagline="Untuk promosi produk atau kampanye",
                         harga=2_500_000, perpanjangan=1_000_000, hari=3,
                         isi=["1 halaman dengan alur marketing", "Ajakan aksi jelas ke WhatsApp", "Desain custom sesuai brand"]),
    "company-profile": dict(nama="Company Profile", keluarga="cp", tagline="Untuk bisnis yang ingin tampil lengkap",
                            harga=5_000_000, perpanjangan=2_000_000, hari=5,
                            isi=["Hingga 7 halaman desain custom", "Profil, layanan, portfolio, kontak", "Admin dashboard (CMS)"]),
    "company-profile-pro": dict(nama="Company Profile Pro", keluarga="cp", tagline="Untuk bisnis yang rutin update konten",
                                harga=7_500_000, perpanjangan=3_000_000, hari=7,
                                isi=["Semua fitur Company Profile", "Hingga 15 halaman custom", "Modul berita &amp; artikel"]),
    "toko-katalog": dict(nama="Toko Katalog", keluarga="toko", tagline="Website + katalog, order via WhatsApp",
                         harga=7_500_000, perpanjangan=3_000_000, hari=5,
                         isi=["Desain custom sesuai brand", "Profil bisnis + katalog produk", "Kategori &amp; pencarian produk",
                              "Order langsung ke WhatsApp", "Modul artikel/blog"]),
    "toko-online-pro": dict(nama="Toko Online Pro", keluarga="toko", tagline="Order, bayar, kirim — semua otomatis",
                            harga=15_000_000, perpanjangan=5_000_000, hari=10,
                            isi=["Semua fitur Toko Katalog (termasuk desain custom &amp; artikel)",
                                 "Keranjang, checkout &amp; payment gateway (VA, QRIS, e-wallet)", "Ongkir otomatis &amp; laporan penjualan"]),
}
URUTAN = {"cp": ["landing-page", "company-profile", "company-profile-pro"], "toko": ["toko-katalog", "toko-online-pro"]}
STANDAR = [("Desain responsive", "Rapi di PC, tablet, dan smartphone"), ("Keamanan SSL", "Terlindungi dari malware dan spam"),
           ("SEO-ready &amp; cepat", "SEO on-page &amp; loading di bawah 3 detik, mudah ditemukan di Google"),
           ("Copywriting menjual", "Naskah persuasif yang mengajak pengunjung menghubungi Anda")]
LANGKAH = [("Konsultasi", "Kami gali tujuan bisnis dan kebutuhan fitur Anda"), ("Desain", "Tampilan custom sesuai brand, Anda review dulu"),
           ("Development", "Programmer expert membangun fitur dan konten"), ("Uji coba", "Cek kecepatan, keamanan, dan tampilan di semua layar"),
           ("Go-live", "Website online, tim Anda kami ajari cara mengelolanya")]


def e(s): return html.escape(str(s), quote=False)
BLANK = "______________________"
def garis(v): return e(v) if v else BLANK
def rp(x):
    x = round(x)
    return "Rp" + f"{x:,}".replace(",", ".")
def jt(x):  # 7500000 → "Rp7,5 jt"
    v = x / 1_000_000
    return "Rp" + (f"{v:g}".replace(".", ",")) + " jt"


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
    css = open(os.path.join(ASSETS, "website.css")).read()
    return f'<!doctype html>\n<html lang="id"><head><meta charset="utf-8"><title>{title}</title>\n<style>\n{css}</style></head><body>\n{body}\n</body></html>\n'


def kartu(kode, pilih):
    p = PAKET[kode]; on = kode == pilih
    return (f'<div class="pkc{" on" if on else ""}">' + ('<span class="badge">Rekomendasi kami</span>' if on else "")
            + f'<h3>{p["nama"]}</h3><div class="tg">{p["tagline"]}</div><div class="hg">{jt(p["harga"])}</div><ul>'
            + "".join(f"<li>{x}</li>" for x in p["isi"])
            + f'<li>Perpanjangan mulai tahun ke-2: {jt(p["perpanjangan"])}/thn</li></ul><div class="wk">Selesai {p["hari"]} hari kerja</div></div>')


def hitung(d):
    p = PAKET[d["paket"]]
    items = [(f'Paket {p["nama"]}', "Termasuk hosting, domain, SSL, dan CMS tahun pertama", p["harga"])]
    items += [(e(a["nama"]), e(a.get("keterangan", "")), a["harga"]) for a in d.get("addon", [])]
    subtotal = sum(x[2] for x in items)
    dis = d.get("diskon")
    if dis:
        assert dis.get("imbalan"), "diskon wajib punya imbalan (bayar lunas, kontrak perpanjangan 2 tahun, portfolio/testimoni, referensi)"
        assert dis["nilai"] <= 0.10 * subtotal + 1, "diskon maksimal 10% dari harga"
    total = subtotal - (dis["nilai"] if dis else 0)
    if d.get("bayar_lunas"):
        termin = [("Penandatanganan", "Pembayaran lunas", "Saat tanda tangan", total)]
    else:
        dp = round(total / 2)
        termin = [("Penandatanganan", "Down Payment 50%", "Saat tanda tangan", dp),
                  ("Sebelum go-live", "Pelunasan 50%", "Setelah uji coba disetujui Klien", total - dp)]
    assert abs(sum(t[3] for t in termin) - total) < 1, "Σ termin ≠ Total"
    return p, items, subtotal, total, termin


def penawaran(d):
    k = d["klien"]; tahun = d["tanggal"].split()[-1]
    p, items, subtotal, total, termin = hitung(d)
    h = hero(d, "Penawaran Layanan &amp; Persetujuan Kerja Sama", "Paket Website", "No.")
    h += (f'  <p class="intro">Terima kasih atas kesempatan yang diberikan kepada Venturo. Sejak 2013, lebih dari 200 project telah kami selesaikan '
          f'bersama lebih dari 100 engineer in-house. Melalui penawaran ini, kami merekomendasikan paket website yang paling sesuai untuk {e(d["intro_untuk"])}, '
          f'dengan satu harga di awal yang sudah mencakup desain, CMS, dan hosting tahun pertama.</p>\n</section>\n')
    # 1. Paket
    kel = URUTAN[p["keluarga"]]
    custom = ('<div class="pkc dark"><h3>Custom</h3><div class="tg">Butuh lebih dari website?</div><div class="hg">Sesuai kebutuhan</div>'
              '<ul style="list-style:none;padding:0"><li>Booking, membership, marketplace, integrasi ERP atau sistem internal Anda.</li></ul>'
              '<div class="wk">Timeline dibahas saat konsultasi</div></div>') if len(kel) < 3 else ""
    alasan = "".join(f"<li>{e(x)}</li>" for x in d["alasan"])
    h += f'''<h2><i>1</i>Paket yang Kami Rekomendasikan</h2>
<div class="why"><b>Kenapa {p["nama"]}?</b><ul style="margin-top:1mm">{alasan}</ul></div>
<div class="pk">{"".join(kartu(x, d["paket"]) for x in kel)}{custom}</div>
'''
    nilai = d.get("nilai_tambah", [])
    if nilai:
        h += '<div class="svc"><h3>Nilai tambah untuk Anda <small>Tanpa biaya tambahan</small></h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in nilai) + "</ul></div>\n"
    # 2. Sudah termasuk
    std = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in STANDAR)
    domain = ('<p><b>Sudah punya domain &amp; hosting?</b> Domain tetap dipakai. Tampilan website bisa di hosting Anda, CMS tetap di platform Venturo; '
              'penyesuaiannya dibahas saat konsultasi.</p>') if d.get("punya_domain_hosting") else ""
    h += f'''<div class="keep"><h2><i>2</i>Sudah Termasuk di Setiap Paket</h2>
<div class="std">{std}</div>
<div class="renew"><h3>Perpanjangan tahunan mencakup</h3><div class="tg">Tahun pertama sudah termasuk harga paket</div>
<div class="ck"><span>✓ Hosting, domain, SSL &amp; storage 5 GB</span><span>✓ Update sistem, backup &amp; support</span><span>✓ CMS berlangganan, selalu ter-update</span></div>
<p><b>Kepemilikan:</b> CMS adalah platform milik Venturo. Domain atas nama Anda, konten bisa diekspor.</p>
<p><b>Di luar paket:</b> payment gateway, ongkir &amp; akomodasi meeting luar Malang.</p>{domain}</div></div>
'''
    # 3. Cara kerja
    stp = "".join(f'<div><i>{i:02d}</i><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(LANGKAH, 1))
    h += f'''<div class="keep"><h2><i>3</i>Cara Kerja Kami</h2>
<div class="steps">{stp}</div>
<p style="margin:0 0 2mm;color:var(--muted)">Website <b style="color:var(--ink);font-weight:700">selesai {p["hari"]} hari kerja</b>, dihitung sejak Down Payment diterima dan materi konten dari Klien (logo, foto, dan informasi bisnis) lengkap.</p></div>
'''
    # 4. Investasi & pembayaran
    rows = "".join(f'<tr><td><b style="font-weight:600">{n}</b>' + (f'<span class="d">{k_}</span>' if k_ else "") + f'</td><td class="r">{rp(v)}</td></tr>' for n, k_, v in items)
    dis = d.get("diskon")
    if dis:
        rows += f'<tr class="sub"><td>Total</td><td class="r">{rp(subtotal)}</td></tr><tr class="sub disc"><td>{e(dis["nama"])}</td><td class="r">– {rp(dis["nilai"])}</td></tr>'
    trows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="r">{rp(n)}</td></tr>' for a, b, c, n in termin)
    dp_li = ("Pembayaran dilakukan lunas saat penandatanganan." if d.get("bayar_lunas") else
             "Down Payment 50% dibayar saat penandatanganan; pelunasan 50% dibayar setelah uji coba disetujui Klien, sebelum website go-live.")
    dperp = d.get("diskon_perpanjangan")
    perp = (f'Perpanjangan mulai tahun ke-2: {rp(p["perpanjangan"])}/tahun'
            + (f'; tahun ke-2 diskon {dperp["persen"]}% menjadi {rp(p["perpanjangan"] * (100 - dperp["persen"]) / 100)} ({e(dperp["imbalan"])})' if dperp else "")
            + ', mencakup hosting, domain, SSL, storage 5 GB, update sistem, backup, support, dan CMS. Ketentuan perpanjangan diatur dalam Service Agreement.')
    h += f'''<div class="keep"><h2><i>4</i>Investasi &amp; Pembayaran</h2>
<table class="cost">
  <thead><tr><th>Item</th><th class="r">Harga</th></tr></thead>
  <tbody>{rows}<tr class="grand"><td>Total Investasi</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
<ul style="margin-top:3mm">
  <li>Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien.</li>
  <li>{dp_li}</li>
  <li>{perp}</li>
</ul>
<div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div>
<table class="cost">
  <thead><tr><th>Tahap</th><th>Termin</th><th>Waktu</th><th class="r">Nominal</th></tr></thead>
  <tbody>{trows}<tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(total)}</td></tr></tbody>
</table></div>
'''
    # 5. Batasan
    bat = ["Biaya transaksi payment gateway dan biaya pengiriman (ongkir) dari penyedia pihak ketiga",
           "Akomodasi dan transportasi untuk meeting di luar Malang",
           f'Halaman atau fitur di luar isi Paket {p["nama"]}, yang akan diajukan dalam penawaran terpisah setelah disetujui Klien',
           "Penambahan kapasitas penyimpanan di atas 5 GB sesuai ketentuan dalam Service Agreement"] + list(d.get("batasan", []))
    h += ('<div class="keep">\n<h2><i>5</i>Batasan dan Pengecualian</h2>\n<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk:</p>\n<ul>\n'
          + "".join(f"  <li>{x}</li>\n" for x in bat) + "</ul>\n</div>\n")
    # 6. Persetujuan
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    h += f'''<div class="sign">
  <h2 style="margin-top:8mm"><i>6</i>Persetujuan</h2>
  <p class="agree">Dengan menandatangani dokumen ini, kedua belah pihak menyatakan bahwa mereka telah membaca, memahami, dan menyetujui seluruh syarat dan ketentuan yang tercantum dalam dokumen ini, yang merupakan bagian tidak terpisahkan dari dokumen Service Agreement Paket Website Venturo.</p>
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
    s = open(os.path.join(ASSETS, "sa-website.html")).read()
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    isi = {"FILE": d["file"] + "-Service-Agreement-Website", "NOMOR": e(d["nomor"]), "TANGGAL": e(d["tanggal"]),
           "KLIEN": e(k["instansi"]), "ALAMAT": garis(k.get("alamat")), "TAHUN": d["tanggal"].split()[-1],
           "TTD_NAMA": garis(k.get("ttd_nama")), "TTD_JABATAN": garis(k.get("ttd_jabatan")),
           "TTD_NAMA_TD": td(k.get("ttd_nama")), "TTD_JABATAN_TD": td(k.get("ttd_jabatan")),
           "CSS": open(os.path.join(ASSETS, "website.css")).read()}
    for kk, v in isi.items():
        assert "{{" + kk + "}}" in s, kk
        s = s.replace("{{" + kk + "}}", v)
    assert "{{" not in s, re.findall(r"\{\{\w+\}\}", s)
    return s


def main():
    data, out = sys.argv[1], sys.argv[2]
    d = json.load(open(data))
    assert d["paket"] in PAKET, f"paket tidak dikenal: {d['paket']} (Custom → pakai proposal-managed atau proposal-dedicated)"
    kode = d["nomor"].split("/")[1] if d["nomor"].count("/") >= 3 else ""
    assert re.fullmatch(r"[A-Za-z0-9]+", kode), f"kode project di nomor harus huruf & angka saja: {d['nomor']}"
    assert d.get("alasan"), "isi 'alasan' (kenapa paket ini cocok, dari brief)"
    os.makedirs(out, exist_ok=True)
    p, total = penawaran(d)
    s = sla(d)
    for nama, isi in (("penawaran.html", p), ("sla.html", s)):
        for sisa in d.get("cek_tidak_boleh_ada", []):
            assert sisa not in isi, f"sisa teks '{sisa}' di {nama}"
        # istilah baku: "Perpanjangan", bukan "biaya tahunan"/"sewa"; pajak memakai kalimat PKP
        for larang in (r"PPN tidak ditagihkan", r"biaya tahunan", r"\bsewa\b"):
            assert not re.search(larang, isi, re.I), f"istilah dilarang '{larang}' di {nama}"
        open(os.path.join(out, nama), "w").write(isi)
    for a in ("logo.png", "bg_flat.jpg", "ttd.png", "paraf.png"):
        shutil.copy2(os.path.join(ASSETS, a), out)
    if not os.path.isdir(os.path.join(out, "fonts")):
        shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(out, "fonts"))
    pk = PAKET[d["paket"]]
    print(json.dumps({"nomor": d["nomor"], "paket": pk["nama"], "harga_paket": rp(pk["harga"]),
                      "total_investasi": rp(total), "perpanjangan_tahun_2": rp(pk["perpanjangan"]) + "/tahun",
                      "waktu_kerja": f'{pk["hari"]} hari kerja', "termin": [f"{b}: {rp(n)}" for _, b, _, n in hitung(d)[4]]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
