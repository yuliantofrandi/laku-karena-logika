#!/usr/bin/env python3
"""Bangun 2 HTML penawaran Paket Website dari satu file data JSON.

  python3 build.py <data.json> <folder kerja>

Hasil di <folder kerja>: penawaran.html dan sla.html (+ logo, bg, ttd, paraf, fonts).
Render dengan scripts/render.py.

Yang dihitung otomatis (dan di-assert):
- Harga, perpanjangan, waktu kerja, dan isi paket dari PAKET (references/paket-website.md).
- Rincian Biaya: Pembuatan Website (harga paket − perpanjangan) + Hosting, Domain & CMS Tahun ke-1
  (= perpanjangan); Total Investasi = harga paket.
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
# Fitur admin dashboard (CMS) per paket — tampil di Lingkup Layanan bersama ketentuan kepemilikan.
CMS_DASAR = ["Mengubah teks dan gambar di setiap halaman secara mandiri, tanpa bantuan programmer",
             "Mengelola informasi kontak, alamat, jam operasional, serta tautan WhatsApp dan media sosial",
             "Pustaka media untuk mengunggah dan mengelola foto (kapasitas penyimpanan 5 GB)",
             "Pengaturan SEO per halaman: judul, deskripsi, dan gambar saat tautan dibagikan",
             "Akun admin untuk tim Klien"]
CMS = {
    "landing-page": CMS_DASAR,
    "company-profile": CMS_DASAR[:1] + ["Mengelola daftar layanan dan portfolio (tambah, ubah, hapus)"] + CMS_DASAR[1:],
    "company-profile-pro": CMS_DASAR[:1] + ["Mengelola daftar layanan dan portfolio (tambah, ubah, hapus)",
                                           "Modul berita &amp; artikel: menulis, mengatur kategori, dan menjadwalkan terbit"] + CMS_DASAR[1:],
    "toko-katalog": CMS_DASAR[:1] + ["Mengelola produk, kategori, harga, dan foto produk",
                                    "Modul artikel/blog: menulis, mengatur kategori, dan menjadwalkan terbit"] + CMS_DASAR[1:],
    "toko-online-pro": CMS_DASAR[:1] + ["Mengelola produk, kategori, harga, stok, dan foto produk",
                                       "Mengelola pesanan, status pembayaran, dan pengiriman",
                                       "Laporan penjualan",
                                       "Modul artikel/blog: menulis, mengatur kategori, dan menjadwalkan terbit"] + CMS_DASAR[1:],
}


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


def hitung(d):
    p = PAKET[d["paket"]]
    # Harga paket dipecah: pembuatan website + layanan tahun ke-1 (= nilai perpanjangan). Total tetap = harga paket.
    items = [(f'Pembuatan Website — Paket {p["nama"]}', "Desain custom, development, uji coba, dan go-live", f'{p["hari"]} hari kerja', p["harga"] - p["perpanjangan"]),
             ("Hosting, Domain &amp; CMS — Tahun ke-1", f'Hosting, domain, SSL, storage 5 GB, update sistem, backup, support, dan CMS; '
              f'mulai tahun ke-2 diperpanjang {rp(p["perpanjangan"])}/tahun', "1 tahun sejak go-live", p["perpanjangan"])]
    items += [(e(a["nama"]), e(a.get("keterangan", "")), e(a.get("waktu", "–")), a["harga"]) for a in d.get("addon", [])]
    subtotal = sum(x[3] for x in items)
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
                  ("Uji coba disetujui Klien", "Pelunasan 50%", "Sebelum go-live", total - dp)]
    assert abs(sum(t[3] for t in termin) - total) < 1, "Σ termin ≠ Total"
    return p, items, subtotal, total, termin


def penawaran(d):
    k = d["klien"]; tahun = d["tanggal"].split()[-1]
    p, items, subtotal, total, termin = hitung(d)
    h = hero(d, "Penawaran Layanan &amp; Persetujuan Kerja Sama", "Paket Website", "No.")
    h += ('  <p class="intro">Melalui penawaran ini, kami menegaskan kesiapan tim IT profesional kami yang berjumlah kurang lebih 100 orang '
          'untuk membangun, mengembangkan, dan memelihara aplikasi Klien secara berkelanjutan. Dokumen ini memuat ruang lingkup layanan, output, '
          'dan rincian biaya sebagai acuan kesepakatan bersama kedua belah pihak.</p>\n</section>\n')
    # 1. Lingkup Layanan — kotak .svc (judul + keterangan kecil + daftar), gaya sama dengan proposal-managed
    box = lambda judul, ket, isi: (f'<div class="svc"><h3>{judul} <small>{ket}</small></h3><ul>'
                                   + "".join(f"<li>{x}</li>" for x in isi) + "</ul></div>\n")
    halaman = [x for x in p["isi"] if "CMS" not in x]
    buat = halaman + [
        "Desain responsive: rapi di PC, tablet, dan smartphone",
        "Keamanan SSL: terlindungi dari malware dan spam",
        "SEO-ready &amp; cepat: SEO on-page dan loading di bawah 3 detik",
        "Copywriting: naskah persuasif yang mengajak pengunjung menghubungi Klien",
        "Uji coba &amp; go-live: cek kecepatan, keamanan, dan tampilan, lalu tim Klien diajari mengelola website"]
    cms = CMS[d["paket"]] + ["Kepemilikan: CMS adalah platform milik Venturo; seluruh konten website (teks, foto, dan data) milik Klien dan dapat diekspor sewaktu-waktu"]
    host = ["Hosting dengan kapasitas penyimpanan 5 GB",
            "Domain didaftarkan atas nama Klien, termasuk sertifikat SSL",
            "Update sistem dan backup berkala",
            "Dukungan teknis melalui WhatsApp pada hari dan jam kerja"]
    if d.get("punya_domain_hosting"):
        host.append("Sudah punya domain &amp; hosting: domain tetap dipakai dan tampilan website dapat di hosting Klien, CMS tetap di platform Venturo; penyesuaian biaya dibahas terpisah")
    h += '<h2><i>1</i>Lingkup Layanan</h2>\n'
    h += box("Pembuatan Website", f'Paket {p["nama"]}', buat)
    h += box("Admin Dashboard (CMS)", "Layanan berlangganan, kelola konten secara mandiri", cms)
    h += box("Hosting, Domain &amp; Support", "Tahun ke-1 sudah termasuk, diperpanjang setiap tahun", host)
    if d.get("nilai_tambah"):
        h += box("Nilai Tambah", "Tanpa biaya tambahan", [e(x) for x in d["nilai_tambah"]])
    # 2. Rincian Biaya & 3. Pembayaran
    rows = "".join(f'<tr><td><b style="font-weight:600">{n}</b>' + (f'<span class="d">{k_}</span>' if k_ else "") + f'</td><td style="white-space:nowrap">{w}</td><td class="r">{rp(v)}</td></tr>' for n, k_, w, v in items)
    dis = d.get("diskon")
    if dis:
        rows += f'<tr class="sub"><td colspan="2">Total</td><td class="r">{rp(subtotal)}</td></tr><tr class="sub disc"><td colspan="2">{e(dis["nama"])}</td><td class="r">– {rp(dis["nilai"])}</td></tr>'
    trows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class="r">{rp(n)}</td></tr>' for a, b, c, n in termin)
    dperp = d.get("diskon_perpanjangan")
    perp = (f'Perpanjangan mulai tahun ke-2: {rp(p["perpanjangan"])}/tahun'
            + (f'; tahun ke-2 diskon {dperp["persen"]}% menjadi {rp(p["perpanjangan"] * (100 - dperp["persen"]) / 100)} ({e(dperp["imbalan"])})' if dperp else "")
            + ', mencakup hosting, domain, SSL, storage 5 GB, update sistem, backup, support, dan CMS. Ketentuan perpanjangan diatur dalam Service Agreement.')
    h += f'''<div class="keep"><h2><i>2</i>Rincian Biaya</h2>
<table class="cost">
  <thead><tr><th>Layanan</th><th>Periode</th><th class="r">Harga</th></tr></thead>
  <tbody>{rows}<tr class="grand"><td colspan="2">Total Investasi</td><td class="r">{rp(total)}</td></tr></tbody>
</table>
<ul style="margin-top:3mm">
  <li>{perp}</li>
</ul></div>
<div class="keep"><h2><i>3</i>Pembayaran</h2>
<ul style="margin:0 0 3mm">
  <li>Seluruh harga bersifat nett. Venturo belum berstatus Pengusaha Kena Pajak (PKP), sehingga tidak memungut PPN. PPh 23 ditanggung Klien.</li>
  <li>Tagihan dikirim sesuai tanggal invoice dan wajib dibayarkan paling lambat H+14 (empat belas) dari tanggal invoice.</li>
  <li>Waktu pengerjaan dihitung sejak {"pembayaran" if d.get("bayar_lunas") else "Down Payment"} diterima dan materi konten dari Klien (logo, foto, dan informasi bisnis) lengkap; website go-live setelah {"pembayaran" if d.get("bayar_lunas") else "pelunasan"} diterima.</li>
  <li>Apabila Klien tidak melakukan pembayaran sesuai jadwal, maka seluruh aktivitas layanan berhak dihentikan sementara.</li>
  <li>Perpanjangan tahunan ditagihkan 30 (tiga puluh) hari sebelum tanggal jatuh tempo mulai tahun ke-2 dan berlanjut setiap tahun hingga Klien menghentikannya dengan pemberitahuan tertulis sebelum tanggal jatuh tempo.</li>
</ul>
<div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div>
<table class="cost">
  <thead><tr><th>Periode Kerja</th><th>Termin</th><th>Tgl Invoice</th><th class="r">Nominal</th></tr></thead>
  <tbody>{trows}<tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(total)}</td></tr></tbody>
</table></div>
'''
    # 5. Batasan
    bat = ["Biaya transaksi payment gateway dan biaya pengiriman (ongkir) dari penyedia pihak ketiga",
           "Akomodasi dan transportasi untuk meeting di luar Malang",
           f'Halaman atau fitur di luar isi Paket {p["nama"]}, yang akan diajukan dalam penawaran terpisah setelah disetujui Klien',
           "Penambahan kapasitas penyimpanan di atas 5 GB sesuai ketentuan dalam Service Agreement"] + list(d.get("batasan", []))
    h += ('<div class="keep">\n<h2><i>4</i>Batasan dan Pengecualian</h2>\n<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk:</p>\n<ul>\n'
          + "".join(f"  <li>{x}</li>\n" for x in bat) + "</ul>\n</div>\n")
    # 6. Persetujuan
    td = lambda v: f"<td><b>{e(v)}</b></td>" if v else '<td class="blank"></td>'
    h += f'''<div class="sign">
  <h2 style="margin-top:8mm"><i>5</i>Persetujuan</h2>
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
