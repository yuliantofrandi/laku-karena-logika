import re
T=open('contoh-penawaran-lama.html').read()
CSS=T.split('</style>')[0]+'</style>'
CSS=CSS.replace('</style>','tr.grand td{background:var(--t50);border:0;border-top:.5mm solid var(--teal);padding:3mm;vertical-align:middle}\ntr.grand td:first-child{text-align:left;font-size:8.5pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--t7);border-bottom-left-radius:2.5mm}\ntr.grand td:last-child{font-size:11pt;font-weight:800;color:var(--t8);border-bottom-right-radius:2.5mm}\n@page{size:A4;margin:11mm 12mm 15mm 12mm}\n.hero{margin:-11mm -12mm 0;padding:8mm 12mm 3mm}\n.logo{margin-left:0}\n</style>')
def rp(x): return 'Rp'+f'{int(round(x)):,}'.replace(',','.')
def dp(x):
    s=('%g'%x).replace('.',',');return s
NO='VEN/PolicyLab/2026/016'; PRJ='Platform Pembelajaran Kebijakan'; TGL='22 Oktober 2026'
TARIF=150000
B,M,K,R='Besar','Menengah','Kecil','Ringan'
mods=[
("Fondasi & Administrasi","Web",[
 ("Registrasi & login email/password, verifikasi email, lupa password",8),
 ("SSO Google",4),
 ("Integrasi SSO Sistem Informasi Akademik kampus",10),
 ("Pemetaan akun & role dari data SIAKAD",4),
 ("Role-based Access Control (Mahasiswa/Peserta, Dosen/Mentor, Administrator)",10),
 ("Manajemen akun pengguna oleh Administrator (termasuk impor massal)",8),
 ("Profil pengguna",3),
 ("Manajemen batch kelas",6),
 ("Penempatan peserta & dosen ke batch",3),
 ("Manajemen lisensi",5)]),
("UI/UX","Web & Mobile",[
 ("Pemetaan alur pengguna & wireframe seluruh peran",12),
 ("Design system & komponen UI",12),
 ("Rancangan UI web Mahasiswa/Peserta",18),
 ("Rancangan UI web Dosen/Mentor",10),
 ("Rancangan UI web Administrator",8),
 ("Rancangan UI aplikasi mobile",12)]),
("Kanal 1 – Policy Hackathon & Lab Kebijakan","Web",[
 ("Manajemen event hackathon (jadwal, kuota, tahapan)",8),
 ("Pendaftaran peserta event",4),
 ("Pembentukan tim mandiri (buat, undang, gabung, keluar)",12),
 ("Repository dataset (.csv, .xlsx, .pdf): unggah & unduh",8),
 ("Workspace tim",6),
 ("Unggah luaran Policy Brief/slide + riwayat versi",8),
 ("Pengaturan kriteria & bobot penilaian",6),
 ("Penugasan juri/dosen ke tim",4),
 ("Modul penilaian juri/dosen berdasarkan kriteria",10),
 ("Rekap nilai & leaderboard",8),
 ("Pengumuman hasil evaluasi",3)]),
("Kanal 2 – Micro-Credentials & Sertifikasi (LMS)","Web",[
 ("Manajemen program, kursus & modul",14),
 ("Halaman belajar peserta (navigasi modul, lanjutkan belajar)",10),
 ("Unggah & transcoding video ke HLS",12),
 ("Enkripsi HLS + player terproteksi (anti-unduh, watermark pengguna)",14),
 ("Bahan bacaan PDF (viewer)",4),
 ("Bank soal & kuis interaktif dengan penilaian otomatis",16),
 ("Pengaturan kuis (durasi, jumlah percobaan, nilai minimum)",6),
 ("Tugas: unggah peserta & penilaian dosen",12),
 ("Progress tracker real-time",10),
 ("Jadwal & tautan sesi langsung (input manual Zoom/Google Meet)",3),
 ("Akses sesi langsung & rekap kehadiran",6),
 ("Pengaturan kriteria kelulusan",6),
 ("Template sertifikat (Administrator)",5),
 ("Generator sertifikat digital ber-QR Code otomatis",10),
 ("Halaman verifikasi sertifikat (scan QR)",4)]),
("Kanal 3 – Community of Practice & Policy Clinic","Web",[
 ("Kategori topik forum (Inklusi Keuangan, BUMDes, Perencanaan Daerah, dll.)",3),
 ("Thread & balasan (teks, lampiran)",12),
 ("Suka, mention & langganan thread",6),
 ("Moderasi forum (laporkan, sembunyikan, sematkan)",6),
 ("Kalender kegiatan",8),
 ("Manajemen event, webinar & Policy Clinic",8),
 ("Pendaftaran sesi & kuota peserta",5),
 ("Pengingat otomatis terjadwal (push & email)",5),
 ("Pustaka digital: repositori riset, arsip video bedah kasus, best practices",10),
 ("Pencarian & filter pustaka",8),
 ("Hak akses & unduh dokumen pustaka",3)]),
("Kanal 4 – Proyek Terapan & Micro-Internship","Web",[
 ("Akun & profil mitra daerah",5),
 ("Katalog proyek: posting kebutuhan/isu mitra",8),
 ("Lamaran proyek oleh tim mahasiswa",8),
 ("Seleksi & penetapan tim serta mentor",5),
 ("Digital logbook harian/mingguan",10),
 ("Persetujuan logbook oleh dosen/mentor",5),
 ("Milestone & rekap kemajuan proyek",10),
 ("Dashboard proyek dosen/mentor",8),
 ("Repository luaran proyek (dashboard data, laporan, rekomendasi)",6),
 ("Serah terima luaran & umpan balik mitra",5)]),
("Sistem Notifikasi","Web & Mobile",[
 ("Mesin notifikasi & preferensi pengguna",6),
 ("Notifikasi in-app web",6),
 ("Email transaksi/jadwal via SMTP/SendGrid + template",6),
 ("Push notification (FCM) Android & iOS",8)]),
("Laporan & Analitik","Web",[
 ("Dashboard analitik Administrator",12),
 ("Ekspor laporan keaktifan peserta (Excel/PDF)",5),
 ("Ekspor rekap nilai (Excel/PDF)",5),
 ("Log aktivitas platform & ekspor",8)]),
("Pembayaran (Payment Gateway)","Web & Mobile",[
 ("Integrasi payment gateway (Midtrans/Xendit) & notifikasi status pembayaran",10),
 ("Checkout pendaftaran program/sertifikasi berbayar",6),
 ("Riwayat transaksi & laporan pembayaran Administrator",4),
 ("Alur pembayaran di aplikasi mobile",4)]),
("Aplikasi Mobile (Android & iOS, cross-platform)","Mobile",[
 ("Setup aplikasi, autentikasi & SSO",16),
 ("Beranda & profil",8),
 ("Kanal 2: kursus, video terproteksi, PDF, kuis, tugas, progress, sesi langsung, sertifikat",70),
 ("Kanal 1: event, tim, dataset, unggah luaran, leaderboard",35),
 ("Kanal 3: forum, event & Policy Clinic, pustaka",35),
 ("Kanal 4: katalog proyek, lamaran, logbook, milestone",28),
 ("Fitur Dosen/Mentor: penilaian & persetujuan logbook",20),
 ("Push notification & deep link",6),
 ("Pengujian perangkat & rilis Google Play/App Store",14)]),
("Meeting Review & Pelatihan","1 DP = 1 jam",[
 ("Kickoff & meeting review mingguan (16 minggu × 1 jam)",16),
 ("Pelatihan Administrator (2 jam)",2),
 ("Pelatihan Dosen/Mentor (2 jam)",2)]),
]
opt=[("Integrasi API Zoom/Google Meet: pembuatan sesi otomatis, sesi tersemat di platform, dan sinkronisasi kehadiran (web & mobile). Pada rilis pertama, sesi langsung memakai tautan yang diinput manual.",24),
     ("DRM berlisensi (Widevine/FairPlay) untuk proteksi video tingkat lanjut (web & mobile). Pada rilis pertama, video diproteksi dengan enkripsi HLS dan player terproteksi.",28)]
tot=sum(x[1] for m in mods for x in m[2]); PKG=850; cad=PKG-tot
print('total',tot,'cadangan',cad,[ (m[0],sum(x[1] for x in m[2])) for m in mods])
assert tot<=PKG

hero=lambda eyebrow,title,extra: f'''<section class="hero">
  <img class="logo" src="logo.png" alt="Venturo Expert Programmers">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}<br><span>{PRJ}</span></h1>
  <div class="meta">
    <div class="card"><div class="kv">{extra}</div></div>
    <div class="card soft">
      <div class="lbl">Kepada Yth.</div>
      <div class="to">Bapak/Ibu Pimpinan</div>
      <div>Universitas Sebelas Maret (UNS)</div>
      <div style="color:var(--muted)">Jl. Ir. Sutami No.36A, Surakarta, Jawa Tengah</div>
    </div>
  </div>'''

# ---------- PENAWARAN ----------
P=CSS.replace('<title>Penawaran Layanan Managed Service - Alldila Seats</title>','<title>Penawaran Layanan Managed Service - UNS</title>')+'<body>\n'
P+=hero('Penawaran Layanan &amp; Persetujuan Kerja Sama','Managed Service',
 f'<b>No.</b><span>{NO}</span><b>Project</b><span>{PRJ}</span><b>Tanggal</b><span>{TGL}</span>')
P+='''
  <p class="intro">Melalui penawaran ini, kami menegaskan kesiapan tim IT profesional kami yang berjumlah kurang lebih 100 orang untuk membangun, mengembangkan, dan memelihara aplikasi Klien secara berkelanjutan. Dokumen ini memuat ruang lingkup layanan, output, dan rincian biaya sebagai acuan kesepakatan bersama kedua belah pihak.</p>
</section>

<h2><i>1</i>Lingkup Layanan</h2>
<div class="svc">
  <h3>Setup Awal <small>Sekali bayar, tidak memotong Delivery Point</small></h3>
  <ul>
    <li>Kickoff &amp; Roadmap: menyamakan tujuan dan menyusun roadmap pengembangan</li>
    <li>Setup Core Venturo: boilerplate Venturo sebagai fondasi aplikasi web dan mobile</li>
    <li>Akses &amp; Deployment: penataan repository, staging, dan alur deployment</li>
    <li>Backup &amp; Keamanan: backup, monitoring, dan pengamanan dasar</li>
    <li>Dokumentasi &amp; Transfer Ilmu: sistem didokumentasikan dan dipelajari tim</li>
  </ul>
</div>
<div class="svc">
  <h3>Managed Service <small>Delivery Point-Based Development</small></h3>
  <ul>
    <li>Sistem Delivery Point (DP) berdasarkan bobot dan kompleksitas pekerjaan</li>
    <li>Kategori pekerjaan: ringan (0,25 DP), kecil (0,5 DP), menengah (0,75 DP), dan besar (1 DP)</li>
    <li>Cakupan pekerjaan meliputi pengembangan fitur, aplikasi web dan mobile, rancangan aplikasi, pengelolaan data, meeting review, dan pelatihan pengguna</li>
    <li>Estimasi dan bobot DP setiap fitur tercantum pada Lampiran Estimasi Delivery Point dokumen ini</li>
    <li>Perhitungan DP dapat terdiri dari beberapa pekerjaan dalam satu fitur</li>
    <li>Meeting review dan pelatihan: 1 DP setara dengan 1 jam sesi</li>
    <li>Sisa DP yang tidak terpakai hangus di akhir periode</li>
    <li>Dukungan teknis responsif melalui WhatsApp, dengan prioritas penanganan bug berdasarkan dampak</li>
    <li>Garansi perbaikan bug tanpa biaya tambahan</li>
  </ul>
</div>
'''
PER=[("Bulan 1","1–30 Nov 2026","30 Nov 2026",250,"UI/UX seluruh peran, fondasi &amp; SSO, serta pembangunan Kanal 2 (Micro-Credentials/LMS)."),
("Bulan 2","1–31 Des 2026","31 Des 2026",250,"Penyelesaian Kanal 2, Kanal 1 (Policy Hackathon), Kanal 3 (Community of Practice &amp; Policy Clinic), dan sistem notifikasi."),
("Bulan 3","1–31 Jan 2027","31 Jan 2027",250,"Kanal 4 (Micro-Internship), pembayaran (payment gateway), laporan &amp; analitik, serta pengembangan aplikasi mobile Android &amp; iOS."),
("Bulan 4","1–28 Feb 2027","28 Feb 2027",100,"Penyelesaian aplikasi mobile, rilis ke Google Play/App Store, UAT, pelatihan pengguna, serta cadangan DP untuk penyesuaian hasil UAT.")]
assert sum(p[3] for p in PER)==PKG
GT=10_000_000+PKG*TARIF
brow=''.join(f'<tr><td><b>Managed Service – {p[0]}</b><span class="d">{p[4]}</span></td><td style="white-space:nowrap">{p[1]}</td><td class="c">{p[3]}</td><td class="r">{rp(p[3]*TARIF)}</td></tr>' for p in PER)
prow=''.join(f'<tr><td>{p[1]} – {p[3]} DP</td><td>Termin {i+1}</td><td>{p[2]}</td><td class="r">{rp(p[3]*TARIF)}</td></tr>' for i,p in enumerate(PER))
P+=f'''
<h2><i>2</i>Rincian Biaya</h2>
<table>
  <thead><tr><th>Layanan</th><th>Periode</th><th class="c">DP</th><th class="r">Harga</th></tr></thead>
  <tbody>
    <tr><td><b>Setup Awal</b></td><td>Sekali bayar</td><td class="c">–</td><td class="r">{rp(10_000_000)}</td></tr>
    {brow}
    <tr class="grand"><td colspan="3">Total Investasi</td><td class="r">{rp(GT)}</td></tr>
  </tbody>
</table>

<h3 style="font-size:10.5pt;margin:5mm 0 2mm">Layanan Lanjutan Setelah Go-Live <small style="font-weight:500;color:var(--subtle);font-size:8.5pt;margin-left:2mm">Berlangganan, di luar Total Investasi</small></h3>
<table>
  <thead><tr><th>Layanan</th><th>Periode</th><th class="c">DP</th><th class="r">Harga</th></tr></thead>
  <tbody>
    <tr><td><b>Managed Service – Pemeliharaan &amp; Pengembangan Lanjutan</b>
      <span class="d">Penyesuaian dan pengembangan fitur, dukungan pengelolaan data dan konten, pembaruan aplikasi mobile mengikuti versi Android/iOS, meeting review, serta pemeliharaan keamanan platform. Kuota dapat dinaikkan ke paket 100 DP sesuai kebutuhan.</span></td>
      <td style="white-space:nowrap">Mulai 1 Mar 2027<br>per bulan</td><td class="c">50</td><td class="r">{rp(50*TARIF)}<br><span style="color:var(--subtle);font-size:8pt">/bulan</span></td></tr>
  </tbody>
</table>

<div class="keep">
<h2><i>3</i>Pembayaran</h2>
<ul>
  <li>Harga yang tertulis adalah harga bersih (nett) yang diterima Venturo. PPh 23 (bila ada) ditanggung oleh Klien. PPN tidak ditagihkan.</li>
  <li>Tagihan dikirim sesuai tanggal invoice dan wajib dibayarkan paling lambat H+14 (empat belas) dari tanggal invoice.</li>
  <li>Pekerjaan Setup Awal dimulai setelah pembayaran pertama diterima.</li>
  <li>Apabila Klien tidak melakukan pembayaran sesuai jadwal, maka seluruh aktivitas layanan berhak dihentikan sementara.</li>
  <li>Layanan Lanjutan (bila dipilih pada bagian Persetujuan) ditagihkan setiap akhir bulan mulai 31 Maret 2027 dan berlanjut otomatis setiap bulan hingga salah satu pihak menghentikannya dengan pemberitahuan tertulis 30 (tiga puluh) hari sebelumnya.</li>
</ul>
<div class="bank"><span>Rekening pembayaran</span><span><b>BCA 3680332222</b> a.n. PT Venturo Pro Indonesia</span></div>
<table>
  <thead><tr><th>Periode Kerja</th><th>Termin</th><th>Tgl Invoice</th><th class="r">Nominal</th></tr></thead>
  <tbody>
    <tr><td>Penandatanganan</td><td>Setup Awal</td><td>Saat tanda tangan</td><td class="r">{rp(10_000_000)}</td></tr>
    {prow}
    <tr class="grand"><td colspan="3">Total Pembayaran</td><td class="r">{rp(GT)}</td></tr>
  </tbody>
</table>
</div>
'''
P+='''
<div class="keep">
<h2><i>4</i>Batasan dan Pengecualian</h2>
<p style="margin:0 0 2mm">Harga yang tercantum belum termasuk biaya-biaya tambahan yang akan diajukan terlebih dahulu dan hanya berlaku setelah mendapatkan persetujuan dari Klien, yang meliputi antara lain:</p>
<ul>
  <li>Infrastruktur: server/hosting, penyimpanan dan streaming video (CDN), domain, dan SSL</li>
  <li>Layanan video terproteksi pihak ketiga dan DRM berlisensi (Widevine/FairPlay) bila diperlukan; estimasi menggunakan enkripsi HLS</li>
  <li>Lisensi/akun Zoom atau Google Workspace untuk sesi video conference</li>
  <li>Layanan email (SMTP/SendGrid) dan push notification sesuai volume pemakaian</li>
  <li>Akun Apple Developer Program dan Google Play Console</li>
  <li>Akses API/SSO Sistem Informasi Akademik disediakan Klien; penyesuaian di sisi sistem akademik kampus bukan bagian dari layanan ini</li>
  <li>Integrasi API Zoom/Google Meet dan DRM berlisensi direncanakan pada pengembangan tahap berikutnya setelah rilis fitur utama (lihat Lampiran Estimasi Delivery Point)</li>
  <li>Akun merchant dan biaya transaksi payment gateway (Midtrans/Xendit)</li>
  <li>Konten pembelajaran (video, materi, dataset, data mitra) disediakan oleh Klien</li>
  <li>Out-of-pocket (seperti transportasi dan akomodasi) untuk pekerjaan di lokasi yang dilakukan atas permintaan Klien</li>
  <li>Permintaan pengerjaan mendesak di luar hari dan jam kerja normal (Sabtu, Minggu, dan hari libur nasional) dihitung 2× dari bobot DP normal</li>
  <li>Pemeliharaan setelah periode Februari 2027 mengikuti ketentuan Layanan Lanjutan pada bagian 2</li>
  <li>Permintaan pekerjaan di luar alokasi DP dalam dokumen ini akan dituangkan dalam penawaran atau kontrak baru setelah disetujui kedua belah pihak</li>
</ul>
</div>
'''
sign=T[T.index('<div class="sign">'):T.index('</body>')]
sign=sign.replace('19 Oktober 2026',TGL).replace('Alldila Seats','Universitas Sebelas Maret').replace('<td><b>Candra</b></td>','<td class="blank"></td>').replace('<td>Owner</td>','<td>Pimpinan</td>')
opt_html='''<div class="opt" style="border:1px solid var(--border);border-radius:3mm;padding:3mm 4mm;margin:0 0 4mm"><div style="font-weight:600;margin-bottom:1.5mm">Pilihan Layanan Lanjutan Setelah Go-Live (centang salah satu):</div>
<div style="display:flex;gap:8mm"><span><span style="display:inline-block;width:3.6mm;height:3.6mm;border:1px solid var(--ink);border-radius:.6mm;vertical-align:-.6mm;margin-right:2mm"></span>Lanjutkan Managed Service 50 DP/bulan mulai 1 Maret 2027</span>
<span><span style="display:inline-block;width:3.6mm;height:3.6mm;border:1px solid var(--ink);border-radius:.6mm;vertical-align:-.6mm;margin-right:2mm"></span>Diputuskan kemudian</span></div></div>
'''
sign=sign.replace('<p class="place">',opt_html+'<p class="place">',1)
P+=sign+'</body></html>'
open('penawaran.html','w').write(P)

# ---------- LAMPIRAN ----------
L=CSS.replace('<title>Penawaran Layanan Managed Service - Alldila Seats</title>','<title>Lampiran Estimasi Delivery Point - UNS</title>')
L=L.replace('</style>','''.mh td{background:var(--t50);font-weight:700;color:var(--t8);border:0;padding:2.2mm 3mm}
table.est{break-inside:auto;font-size:8.6pt}table.est td{padding:1.05mm 3mm}table.est td.k{color:var(--subtle);white-space:nowrap}
table.est tr{break-inside:avoid}tr.st td{font-weight:600;border-bottom:0}tr.st td:first-child{text-align:right;color:var(--muted)}
.h1s h1{font-size:21pt}
</style>''')+'<body>\n'
L+=hero('Lampiran Penawaran Layanan','Estimasi Delivery Point',
 f'<b>Lampiran</b><span>{NO}</span><b>Project</b><span>{PRJ}</span><b>Tanggal</b><span>{TGL}</span>').replace('<section class="hero">','<section class="hero h1s">')
L+='''
  <p class="intro">Lampiran ini merinci estimasi Delivery Point (DP) setiap pekerjaan berdasarkan System Requirement Brief Klien, dan merupakan bagian tidak terpisahkan dari dokumen penawaran nomor '''+NO+'''. DP setiap item merupakan akumulasi tugas di dalamnya (backend, frontend, pengujian) dengan bobot per tugas: ringan 0,25 DP · kecil 0,5 DP · menengah 0,75 DP · besar 1 DP.</p>
</section>
'''
# ringkasan
rows=''.join(f'<tr><td>{m[0]}</td><td>{m[1]}</td><td class="r">{dp(sum(x[1] for x in m[2]))}</td></tr>' for m in mods)
L+=f'''<h2><i>1</i>Ringkasan Estimasi</h2>
<table><thead><tr><th>Modul</th><th>Platform</th><th class="r">DP</th></tr></thead><tbody>{rows}
<tr class="sub"><td colspan="2">Total estimasi</td><td class="r">{dp(tot)} DP</td></tr>
<tr class="sub"><td colspan="2">Paket Managed Service (Nov–Jan 3 × 250 DP + Feb 100 DP)</td><td class="r">{PKG} DP</td></tr>
<tr class="sub"><td colspan="2">Cadangan penyesuaian &amp; hasil UAT</td><td class="r">{dp(cad)} DP</td></tr>
</tbody></table>
'''
body=''
n=0
for m in mods:
    body+=f'<tr class="mh"><td colspan="2">{m[0]} <span style="font-weight:500;color:var(--subtle)">· {m[1]}</span></td><td class="r">{dp(sum(x[1] for x in m[2]))} DP</td></tr>'
    for it in m[2]:
        n+=1;body+=f'<tr><td class="c">{n}</td><td>{it[0]}</td><td class="r">{dp(it[1])}</td></tr>'
L+=f'''<h2 style="break-before:page;margin-top:2mm"><i>2</i>Rincian per Item Pekerjaan</h2>
<table class="est"><thead><tr><th class="c" style="width:9mm">No</th><th>Item Pekerjaan</th><th class="r">DP</th></tr></thead><tbody>{body}
<tr class="grand"><td colspan="2">Total Estimasi</td><td class="r">{dp(tot)} DP</td></tr></tbody></table>

<div class="keep">
<h2><i>3</i>Pengembangan Tahap Berikutnya <span style="font-weight:500;color:var(--subtle);font-size:9pt">(setelah rilis fitur utama)</span></h2>
<table><thead><tr><th>Item Pekerjaan</th><th class="r" style="white-space:nowrap">Estimasi DP</th></tr></thead><tbody>
{''.join(f'<tr><td>{o[0]}</td><td class="r">{dp(o[1])}</td></tr>' for o in opt)}
</tbody></table>
<p class="note" style="color:var(--muted)">Fitur di atas sengaja tidak dimasukkan ke rilis pertama agar fitur utama dapat dirilis lebih cepat dengan biaya yang efisien. Fitur ini dapat ditambahkan setelah rilis melalui Layanan Lanjutan atas persetujuan Klien, dan belum termasuk dalam Total Investasi. Estimasi Poin di atas dikonfirmasi ulang saat fitur akan dikerjakan.</p>
</div>

<div class="keep">
<h2><i>4</i>Asumsi &amp; Catatan</h2>
<ul>
  <li>Estimasi disusun dari System Requirement Brief; bobot DP setiap permintaan disepakati di awal sebelum dikerjakan.</li>
  <li>Perubahan atau penambahan lingkup di luar brief dihitung ulang dan memotong cadangan DP, atau dituangkan dalam penawaran baru.</li>
  <li>Integrasi SSO Sistem Informasi Akademik mengasumsikan kampus menyediakan API/OAuth beserta dokumentasinya.</li>
  <li>Mitra daerah diasumsikan memiliki akun sendiri untuk memposting proyek dan menerima luaran.</li>
  <li>Aplikasi mobile mencakup fitur Mahasiswa/Peserta dan Dosen/Mentor; fitur Administrator tersedia di aplikasi web.</li>
  <li>Jaminan kualitas (testing dan garansi bug), keamanan, dukungan, dan dokumentasi sudah termasuk dan tidak memotong DP.</li>
</ul>
</div>
</body></html>'''
open('lampiran.html','w').write(L)
