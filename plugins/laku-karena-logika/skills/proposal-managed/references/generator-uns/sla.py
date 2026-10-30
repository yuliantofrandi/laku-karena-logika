exec(open('build.py').read().split("hero=lambda")[0].split("mods=[")[0])  # CSS, NO, PRJ, TGL, rp
NO='VEN/PolicyLab/2026/016'
css=CSS.replace('<title>Penawaran Layanan Managed Service - Alldila Seats</title>','<title>Service Agreement Venturo - UNS</title>').replace('</style>','''
ol{margin:0;padding-left:5mm}ol li{margin:.6mm 0;padding-left:1mm}ol li::marker{color:var(--t7);font-weight:600}
ol.a{list-style:lower-alpha;margin-top:.8mm}ul.b{margin-top:.8mm}
p{margin:0 0 2mm}.sec{break-inside:auto}.it{font-style:italic}
li strong,p strong{font-weight:600}
.pp li{margin-bottom:1.5mm}
h2{font-size:10.5pt;margin:5mm 0 1.8mm;gap:2.2mm;line-height:1.2}
h2 i{width:auto;min-width:5.6mm;height:5.6mm;padding:0 1.2mm;border-radius:1.4mm;font-size:8pt;font-weight:700}
.sec p,.sec ol,.sec ul{font-size:9pt}
</style>''')
S=[]
def sec(t,body): S.append((t,body))
sec("Para Pihak",'''<ol class="pp">
<li><strong>PT Venturo Pro Indonesia</strong>, beralamat di Jl. Rinjani No. 26, Oro-oro Dowo, Kecamatan Klojen, Kota Malang, Jawa Timur 65119, dalam hal ini diwakili oleh Yulianto Frandi selaku CEO, selanjutnya dalam perjanjian ini disebut <strong>“Venturo”</strong>.</li>
<li><strong>Universitas Sebelas Maret (UNS)</strong>, beralamat di Jl. Ir. Sutami No. 36A, Surakarta, Jawa Tengah, dalam hal ini diwakili oleh ______________________ selaku Pimpinan, selanjutnya dalam perjanjian ini disebut <strong>“Klien”</strong>.</li></ol>
<p>Venturo dan Klien selanjutnya secara bersama-sama disebut <strong>“Para Pihak”</strong>.</p>''')
sec("Masa Berlaku",'<p>Perjanjian ini berlaku sejak tanggal ditandatangani sampai dengan berakhirnya masa kerja sama, kecuali digantikan oleh Service Agreement baru yang disepakati oleh Para Pihak.</p>')
sec("Lingkup Pengerjaan",f'<p>Perjanjian ini mengatur syarat dan ketentuan umum kerja sama antara Venturo dan Klien dalam penyediaan layanan pengembangan dan pemeliharaan perangkat lunak dengan model Managed Service berbasis Delivery Point (DP). Lingkup kerja, biaya, dan jadwal pembayaran untuk setiap proyek diatur dalam dokumen <span class="it">Penawaran Layanan</span> beserta Lampiran Estimasi Delivery Point (untuk proyek ini nomor {NO}), yang menjadi bagian tidak terpisahkan dari perjanjian ini.</p>')
sec("Support Service",'''<ol>
<li>Pekerjaan dilakukan di kantor Venturo di Jl. Rinjani No. 26, Oro-oro Dowo, Kec. Klojen, Kota Malang.</li>
<li>Hari dan jam kerja operasional yang berlaku yakni Senin – Jumat, 08.00 – 17.00 WIB.</li>
<li>Hari libur nasional dan cuti bersama mengacu pada kalender resmi yang ditetapkan oleh Pemerintah Indonesia, kecuali disepakati lain antara Venturo dan Klien berdasarkan kebutuhan proyek.</li>
<li>Selama jam kerja operasional, Venturo menjamin respons melalui WhatsApp maksimal 15 menit. Untuk dukungan di luar jam kerja, Venturo akan berupaya merespons secepatnya dan memastikan respons tetap diberikan pada hari yang sama, kecuali laporan bug yang ditangani sesuai ketentuan ayat 6.</li>
<li>Setiap kendala teknis atau bug diklasifikasikan berdasarkan dampak operasionalnya pada pengguna sebagai dasar urutan prioritas penanganan:
<ul class="b"><li><strong>Major Bug</strong>: gangguan yang menyebabkan sistem atau fitur utama tidak dapat digunakan; ditangani dengan prioritas pertama.</li>
<li><strong>Minor Bug</strong>: gangguan ringan yang tidak berdampak signifikan terhadap operasional; ditangani setelah Major Bug.</li></ul></li>
<li>Venturo berupaya menyelesaikan setiap Major Bug maupun Minor Bug dalam waktu maksimal 2 (dua) jam sejak laporan diterima, baik di dalam maupun di luar jam kerja operasional. Waktu pukul 21.00–08.00 WIB tidak dihitung; laporan yang diterima pada rentang tersebut mulai dihitung pukul 08.00 WIB.</li>
<li>Apabila karena kompleksitas masalah penyelesaian memerlukan waktu lebih dari 2 (dua) jam, Venturo wajib menyampaikan kepada Klien dalam batas waktu tersebut: penyebab masalah, langkah penanganan, dan estimasi waktu penyelesaian, serta memberikan solusi sementara (<span class="it">workaround</span>) apabila memungkinkan. Venturo terus melaporkan perkembangan penanganan hingga masalah selesai.</li>
<li>Penanganan bug tidak memotong kuota Delivery Point.</li>
<li>Dalam hal terjadi kendala atau bug, Klien wajib memberikan akses dan informasi yang diperlukan untuk mempercepat proses penanganan.</li></ol>''')
sec("Komunikasi",'''<p>Venturo menyediakan platform komunikasi dan kolaborasi berikut untuk koordinasi, diskusi, dan pemantauan perkembangan proyek:</p><ol>
<li><strong>Space (Aplikasi ERP Venturo)</strong> — aplikasi ERP internal Venturo yang mencakup fungsi manajemen tugas, backlog, tiket, hingga monitoring OKR. Seluruh tim mencatat tugas harian dan backlog proyek pada aplikasi ini, dan Klien diberikan akses gratis untuk memantau progres pengembangan secara real-time.</li>
<li><strong>Grup WhatsApp</strong> — untuk setiap proyek dibuatkan grup WhatsApp khusus sebagai sarana komunikasi operasional harian, diskusi, koordinasi, serta penyampaian permintaan oleh Klien. Seluruh permintaan yang disampaikan melalui grup dicatat oleh tim Project Support ke dalam Modul Ticket di Space sebagai bentuk pertanggungjawaban dan pelacakan.</li>
<li><strong>Online Meeting (Google Meet/Discord)</strong> — fasilitas meeting daring untuk diskusi proyek, evaluasi sprint, atau kebutuhan lain sesuai kesepakatan. Jadwal meeting difasilitasi oleh tim Project Support.</li>
<li><strong>GitHub Repository</strong> — seluruh source code hasil pengembangan dikelola melalui repository GitHub untuk kolaborasi, version control, serta audit perkembangan kode.</li></ol>''')
sec("Project Management",'''<p>Venturo menggunakan aplikasi internal yang dirancang untuk mendukung produktivitas, kolaborasi, dan evaluasi tim pengembang perangkat lunak:</p><ol>
<li><strong>Project Development Management</strong> (space.venturo.id) — pengelolaan proyek, sprint, backlog, dan tiket dalam satu platform terintegrasi.</li>
<li><strong>Learning Management System</strong> — pengembangan kompetensi tim melalui pelatihan berkelanjutan dengan kurikulum yang disusun Tim R&amp;D Venturo.</li>
<li><strong>Daily Issue Monitoring</strong> (timebox.venturo.id) — kontrol harian tim; setiap manajer memastikan setiap issue dikerjakan tepat dan dapat diselesaikan di hari yang sama.</li>
<li><strong>Objective and Key Result</strong> — penilaian kinerja setiap programmer untuk menjaga kualitas dan memberikan pelatihan bagi yang belum optimal.</li></ol>''')
sec("Metode Development",'<p>Venturo menerapkan metodologi pengembangan perangkat lunak Scrum (bagian dari kerangka kerja Agile), di mana pengembangan dilakukan secara bertahap dan berulang (<span class="it">iterative development</span>). Pendekatan ini memungkinkan tim lebih adaptif terhadap perubahan kebutuhan dan masukan Klien selama siklus proyek, serta memastikan peningkatan berkelanjutan terhadap kualitas produk yang dikembangkan.</p>')
sec("Deployment Environment",'''<p>Venturo menggunakan tiga (3) lingkungan terpisah untuk menjamin kualitas, keamanan, dan stabilitas aplikasi sebelum digunakan oleh pengguna akhir:</p><ol>
<li><strong>Development Environment</strong> — area kerja tim pengembang untuk proses pemrograman dan eksperimen fitur tanpa memengaruhi sistem lain.</li>
<li><strong>Staging Environment</strong> — area simulasi yang dibuat semirip mungkin dengan sistem produksi untuk pengujian fungsi, integrasi, dan performa sebelum fitur dipindahkan ke produksi. Venturo menyediakan server Staging tanpa biaya tambahan.</li>
<li><strong>Production Environment</strong> — lingkungan final tempat aplikasi digunakan oleh Klien dan pengguna. Seluruh perubahan yang telah lolos pengujian di Staging di-deploy ke Production. Infrastruktur Production disediakan oleh Klien sebagaimana diatur dalam Penawaran Layanan.</li></ol>''')
sec("Laporan Pekerjaan",'''<p>Venturo melaporkan progres pengerjaan kepada Klien melalui Grup WhatsApp, Space, dan meeting review dengan ketentuan sebagai berikut:</p><ol>
<li><strong>Laporan Harian</strong> — ringkasan pekerjaan yang diselesaikan, pekerjaan berjalan, dan kendala (blocker) dikirim setiap hari kerja.</li>
<li><strong>Meeting Review Mingguan</strong> — pembahasan hasil sprint, hasil pengujian (<span class="it">test run</span>) beserta tindak lanjut error, rencana sprint minggu berikutnya, serta backlog dan issue yang perlu konfirmasi Klien.</li>
<li><strong>Laporan Bulanan</strong> — rekap keseluruhan pekerjaan dalam satu periode, termasuk realisasi pemakaian Delivery Point terhadap kuota paket.</li></ol>''')
sec("Biaya Out of Pocket",'''<ol>
<li>Apabila pengerjaan dilakukan di lokasi atas permintaan Klien, maka Klien menanggung dan menyiapkan seluruh biaya akomodasi, transportasi, dan penginapan.</li>
<li>Biaya belum termasuk penggunaan <span class="it">tools</span> atau layanan pihak ketiga, yang hanya digunakan dengan persetujuan tertulis terlebih dahulu dari Klien.</li></ol>''')
sec("Pekerjaan di Luar Jam Kerja",'<p>Permintaan pengerjaan mendesak di luar hari dan jam kerja operasional (Sabtu, Minggu, dan hari libur nasional) dilakukan dengan persetujuan tertulis terlebih dahulu dari Klien dan dihitung 2× (dua kali) dari bobot Delivery Point normal.</p>')
sec("Kerahasiaan",'''<ol>
<li>Para Pihak wajib menjaga dan menyimpan segala informasi dalam rangka pelaksanaan perjanjian ini (selanjutnya disebut <strong>“Informasi”</strong>) sebagai rahasia, dan masing-masing pihak tidak boleh mengungkapkannya kepada pihak lain dengan cara apa pun tanpa persetujuan tertulis dari pihak lainnya, kecuali hal-hal yang merupakan milik umum (<span class="it">public domain</span>) atau untuk keperluan pelaporan sebagaimana diminta oleh pejabat pemerintah yang berwenang.</li>
<li>Para Pihak tidak diperkenankan memberitahukan, membuka, atau memberikan informasi menyangkut isi perjanjian kepada badan hukum maupun perorangan tanpa izin tertulis dari pihak lainnya, kecuali:
<ol class="a"><li>diminta oleh instansi pemerintah yang berwenang mengatur atau mengeluarkan izin tentang hal-hal yang diperjanjikan; atau</li>
<li>diperintah oleh badan peradilan atau instansi pemerintah lain yang berhubungan dengan penegakan hukum secara tertulis, resmi, dan merupakan putusan final.</li></ol></li>
<li>Para Pihak menjamin untuk menyimpan asli maupun salinan dokumen dan/atau surat-surat yang berkaitan dengan perjanjian ini.</li>
<li>Para Pihak wajib memastikan seluruh pimpinan dan staf mematuhi kewajiban menjaga kerahasiaan, baik selama berlangsung maupun setelah perjanjian ini berakhir.</li>
<li>Kewajiban kerahasiaan tetap berlaku sekalipun perjanjian ini berakhir. Apabila terbukti salah satu pihak membocorkan Informasi dan mengakibatkan kerugian bagi pihak lainnya, pihak yang membocorkan dapat dikenakan upaya hukum sesuai peraturan perundang-undangan.</li></ol>''')
sec("Hak Kekayaan Intelektual",'''<ol>
<li>Para Pihak sepakat bahwa Hak atas Kekayaan Intelektual (<strong>“HKI”</strong>) adalah seluruh hak cipta, paten, deskripsi teknis (termasuk <span class="it">source code</span>), merek dagang, merek jasa, hak desain, hak desain industri, hak database, nama dagang, hak yang melindungi rahasia dagang dan informasi rahasia, perangkat lunak, naskah, kode dalam bahasa apa pun, temuan, ide, proses, metode, dokumen, laporan, dan materi lainnya dalam bentuk atau media apa pun yang berkaitan dengan pelaksanaan perjanjian ini, baik yang ada saat ini maupun yang akan diciptakan di kemudian hari.</li>
<li>Para Pihak sepakat bahwa setiap HKI yang timbul atas pelaksanaan perjanjian ini sepenuhnya menjadi milik Klien, dan Venturo berkewajiban menyerahkan HKI tersebut kepada Klien, dengan memperhatikan ketentuan ayat 4.</li>
<li>Seluruh HKI yang berkaitan dengan perangkat lunak diserahkan oleh Venturo kepada Klien pada saat serah terima pekerjaan, setelah seluruh kewajiban pembayaran dinyatakan lunas.</li>
<li>Kepemilikan HKI oleh Klien tidak membatasi hak Venturo untuk menggunakan kembali komponen umum, pustaka kode, kerangka dasar aplikasi (Setup Core Venturo/boilerplate), serta pengetahuan dan metode teknis yang tidak spesifik pada bisnis Klien untuk proyek lain, sepanjang tidak memuat Informasi rahasia, data, maupun fitur dan logika bisnis yang khusus dikembangkan untuk Klien.</li>
<li>Seluruh data dan informasi yang diterbitkan, diperoleh, dan dikumpulkan melalui aplikasi adalah milik Klien.</li></ol>''')
sec("Keterlambatan Pengerjaan",'''<p>Jika pekerjaan mengalami keterlambatan dari batas waktu yang disepakati Para Pihak, penyelesaian dilakukan dengan mekanisme berikut:</p><ol>
<li>Jika keterlambatan diakibatkan oleh Venturo:
<ol class="a"><li>Venturo menambah sumber daya dan/atau waktu kerja tanpa biaya tambahan dan tanpa memotong kuota Delivery Point; dan</li>
<li>Para Pihak menyepakati timeline baru dalam addendum Penawaran, yang wajib segera diselesaikan oleh Venturo.</li></ol></li>
<li>Jika keterlambatan diakibatkan oleh Klien (misalnya keterlambatan persetujuan, data, konten, atau akses pihak ketiga):
<ol class="a"><li>Para Pihak menyepakati timeline baru dalam addendum Penawaran; dan</li>
<li>pekerjaan tambahan yang timbul dihitung sebagai Delivery Point sesuai ketentuan Penawaran.</li></ol></li></ol>''')
sec("Tim Pelaksana",'''<ol>
<li>Venturo menentukan komposisi tim pelaksana (programmer, UI/UX, QA, dan Project Support) sesuai kebutuhan pekerjaan untuk memenuhi lingkup dan jadwal dalam Penawaran.</li>
<li>Seluruh hubungan kerja anggota tim adalah dengan Venturo dan diatur dalam perjanjian kerja tertulis berdasarkan ketentuan perundang-undangan ketenagakerjaan. Seluruh urusan upah, tunjangan, THR, dan kewajiban ketenagakerjaan lainnya menjadi tanggung jawab Venturo.</li>
<li>Apabila anggota tim tidak memenuhi kualifikasi atau melakukan pelanggaran yang dapat merugikan Klien, Klien berhak meminta penggantian dengan memberitahukan alasannya, tanpa biaya tambahan. Penggantian dilakukan paling lambat 7–14 hari.</li>
<li>Apabila anggota tim cuti, sakit, atau berhalangan, Venturo tetap menjamin keberlangsungan pekerjaan dengan menugaskan pengganti tanpa biaya tambahan.</li></ol>''')
sec("Perekrutan",'''<ol>
<li>Klien sepakat untuk tidak melibatkan, merekrut, atau mempekerjakan pegawai Venturo selama masa berlakunya perjanjian ini, serta tidak memberikan insentif atau perjanjian apa pun yang bertujuan mengalihkan pegawai Venturo dari pekerjaannya.</li>
<li>Apabila pegawai yang bersangkutan bersedia direkrut, Klien diperbolehkan merekrutnya dengan dikenakan biaya pengalihan sebesar 6 (enam) kali gaji bulanan terakhir pegawai yang bersangkutan.</li></ol>''')
sec("Terminasi Kontrak",'''<ol>
<li>Klien berhak mengakhiri perjanjian ini atas dasar performa Venturo yang, dengan bukti sah dan tertulis, tidak memenuhi standar layanan secara berturut-turut meskipun telah dilakukan upaya perbaikan, dengan pemberitahuan tertulis paling lambat 30 (tiga puluh) hari sebelum tanggal efektif pengakhiran.</li>
<li>Klien berhak mengakhiri perjanjian ini atas dasar pertimbangan bisnis Klien dengan pemberitahuan tertulis paling lambat 60 (enam puluh) hari sebelum tanggal efektif pengakhiran.</li>
<li>Penghentian Layanan Lanjutan (setelah periode proyek) mengikuti ketentuan pemberitahuan 30 (tiga puluh) hari sebagaimana diatur dalam Penawaran Layanan.</li>
<li>Klien menyelesaikan seluruh kewajiban finansial yang telah jatuh tempo, termasuk tagihan layanan sampai tanggal terminasi.</li>
<li>Seluruh pembayaran yang telah diterima bersifat final dan tidak dapat dikembalikan, dan sisa Delivery Point tidak dapat diuangkan.</li>
<li>Venturo melakukan serah terima pekerjaan sesuai ketentuan Berita Acara Serah Terima.</li></ol>''')
sec("Berita Acara Serah Terima Pekerjaan",'''<ol>
<li>Sebelum masa kontrak berakhir, Venturo melakukan serah terima kepada Klien agar seluruh hasil kerja dapat digunakan Klien secara mandiri, meliputi:
<ol class="a"><li>Source code: file source code dan akses repository;</li>
<li>Dokumentasi teknis: arsitektur sistem, instalasi &amp; deployment, dan integrasi API;</li>
<li>Dokumentasi pengujian: skenario uji dan repository automation test;</li>
<li>Akses environment: staging atau production, serta kredensial akun superadmin aplikasi;</li>
<li>Penghapusan atau pengembalian seluruh informasi rahasia sesuai ketentuan kerahasiaan; dan</li>
<li>Penandatanganan Berita Acara Serah Terima (BAST) oleh Para Pihak.</li></ol></li>
<li>Apabila Klien belum menyelesaikan seluruh kewajiban pembayaran, Venturo berhak menunda serah terima source code, dokumentasi teknis, dokumentasi pengujian, dan akses environment hingga seluruh invoice dinyatakan lunas.</li></ol>''')
sec("Garansi",'''<ol>
<li>Venturo memberikan garansi perbaikan bug tanpa biaya tambahan selama 30 (tiga puluh) hari kalender sejak tanggal rilis setiap fitur ke Production.</li>
<li>Garansi tidak mencakup permintaan perubahan fitur, penambahan fungsi baru, gangguan akibat integrasi atau layanan pihak ketiga, maupun kesalahan penggunaan di luar spesifikasi yang disepakati.</li>
<li>Setelah masa garansi berakhir, perbaikan atau pengembangan lebih lanjut dilakukan melalui Layanan Lanjutan sebagaimana diatur dalam Penawaran Layanan atau melalui penawaran baru.</li></ol>''')
sec("Pembatasan Tanggung Jawab",'<p>Venturo tidak bertanggung jawab atas kerugian tidak langsung, kerugian konsekuensial, atau kerugian pihak ketiga akibat penggunaan perangkat lunak.</p>')
sec("Force Majeure",'<p>Apabila terjadi gempa bumi, bencana alam, tanah longsor, atau kejadian lain yang secara wajar berada di luar kendali Para Pihak sehingga menyebabkan gagal atau tertundanya pelaksanaan kewajiban, Para Pihak sepakat untuk meninjau kembali perjanjian ini.</p>')
sec("Penyelesaian Perselisihan",'''<ol>
<li>Semua perselisihan dan hal-hal yang belum diatur dalam perjanjian ini diselesaikan secara musyawarah untuk mufakat.</li>
<li>Apabila perselisihan tidak dapat diselesaikan secara musyawarah, Para Pihak sepakat menyelesaikannya melalui Badan Arbitrase Nasional Indonesia (BANI) sesuai hukum Republik Indonesia.</li></ol>''')

H=css+'<body>\n'+f'''<section class="hero">
  <img class="logo" src="logo.png" alt="Venturo Expert Programmers">
  <div class="eyebrow">Perjanjian Induk Kerja Sama</div>
  <h1>Service Agreement<br><span>Venturo Managed Service</span></h1>
  <div class="meta">
    <div class="card"><div class="kv"><b>No.</b><span>{NO}</span><b>Penawaran</b><span>{NO}</span><b>Tanggal</b><span>{TGL}</span></div></div>
    <div class="card soft"><div class="lbl">Klien</div><div class="to">Universitas Sebelas Maret (UNS)</div>
      <div style="color:var(--muted)">Jl. Ir. Sutami No.36A, Surakarta, Jawa Tengah</div></div>
  </div>
</section>
'''
for i,(t,b) in enumerate(S,1):
    H+=f'<div class="sec"><h2><i>{i}</i>{t}</h2>{b}</div>\n'
sign=T[T.index('<div class="sign">'):T.index('</body>')]
sign=sign.replace('19 Oktober 2026',TGL).replace('Alldila Seats','Universitas Sebelas Maret').replace('<td><b>Candra</b></td>','<td class="blank"></td>').replace('<td>Owner</td>','<td>Pimpinan</td>')
import re
sign=re.sub(r'<h2[^>]*>.*?</h2>',f'<h2 style="margin-top:8mm"><i>{len(S)+1}</i>Persetujuan</h2>',sign,count=1,flags=re.S)
sign=re.sub(r'<p class="agree">.*?</p>','<p class="agree">Dengan menandatangani dokumen ini, kedua belah pihak menyatakan telah membaca, memahami, dan menyetujui seluruh syarat dan ketentuan yang tercantum di dalamnya. Dokumen ini berfungsi sebagai perjanjian induk (Service Agreement) yang diikuti dengan dokumen Penawaran Layanan untuk setiap proyek.</p>',sign,count=1,flags=re.S)
H+=sign+'</body></html>'
open('sla.html','w').write(H)
print(len(S))
