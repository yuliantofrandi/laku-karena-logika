"""Modal langganan di halaman Harga: pilih paket → isi data → bayar QRIS (payment gateway) → akun aktif → login.

Alur jual Timebase: langsung berlangganan (pilih paket → bayar → aktif), bukan demo.
Tombol "Pilih <paket>" di tabel harga diberi class `js-langganan` + data-paket; tanpa JS tetap
menjadi link biasa (fallback ke checkout_url / #pilih-skema).

Konfigurasi di site.json:
  "langganan": {"api": "https://api.domain/langganan", "min_karyawan": 1, "max_karyawan": 999}

Kontrak API (backend; webhook payment gateway diterima backend, BUKAN oleh situs statis ini):
  POST {api}/orders   body JSON {paket, periode, karyawan, addon: [nama], nama, perusahaan, whatsapp}
       → {order_id, amount, expires_at (ISO), qris_image (URL/data URI) ATAU qris_string}
       Nominal dihitung ulang di server; angka di modal hanya perkiraan.
  GET  {api}/orders/{order_id}
       → {status: "pending"|"paid"|"expired"|"failed", login_url?}
  Webhook gateway → backend menandai pesanan "paid" dan mengaktifkan akun. Modal mengecek status
  tiap 3 detik; begitu "paid", tampil langkah sukses + tombol masuk (login_url / site.json signin_url).

`api` kosong = mode sementara: kotak "QRIS belum aktif" + kirim pesanan lewat WhatsApp (build WARNING).
"""
import html
import json


def tombol(S, x, periode, kelas, label, href):
    """Tombol pilih paket yang membuka modal (data-paket = id paket di pricing.json)."""
    return (f'<a class="btn {kelas} btn-sm js-langganan" href="{href}" rel="nofollow" '
            f'data-paket="{x["id"]}" data-periode="{periode}">{html.escape(label)}</a>')


def modal(S, P):
    cfg = S.get("langganan", {})
    data = {
        "brand": S["brand"],
        "wa": S.get("whatsapp", ""),
        "api": cfg.get("api", "").rstrip("/"),
        "login": S.get("signin_url", ""),
        "bulanBayar": P["annual_months_paid"],
        "batas": [20, 50, 100],            # tier: 1–19, 20–49, 50–99, 100+ (sesuai pricing.json tier_labels)
        "tierLabel": P["tier_labels"],
        "paket": [{"id": x["id"], "nama": x["name"], "bulanan": x["monthly"]} for x in P["schemes"]],
        "addon": [{"nama": a["name"], "bulanan": a["monthly"], "desc": a.get("desc", "")} for a in P.get("addons", [])],
        "min": cfg.get("min_karyawan", 1),
        "max": cfg.get("max_karyawan", 999),   # dibatasi ratusan (permintaan user)
    }
    addon = "".join(
        f'<label class="lg-cek"><input type="checkbox" name="addon" value="{i}"><span><strong>{html.escape(a["name"])}</strong>'
        f' <em>+Rp{a["monthly"]:,}'.replace(",", ".") + f'/karyawan/bln</em><small>{html.escape(a.get("desc", ""))}</small></span></label>'
        for i, a in enumerate(P.get("addons", [])))
    # pilihan paket di dalam modal: tombol beli umum (header/hero/CTA) membuka paket unggulan, bisa diganti di sini
    pilih_paket = "".join(
        f'<label><input type="radio" name="paket" value="{x["id"]}"><span><strong>{html.escape(x["name"])}</strong>'
        f'<small>mulai Rp{min(x["monthly"]):,}/bln'.replace(",", ".") + '</small></span></label>' for x in P["schemes"])
    data["unggulan"] = next((x["id"] for x in P["schemes"] if x.get("featured")), P["schemes"][0]["id"])
    privasi = '<a href="/kebijakan-privasi" target="_blank">Kebijakan Privasi</a>'
    syarat = '<a href="/syarat-layanan" target="_blank">Syarat Layanan</a>'
    return f"""<dialog class="lg" id="langganan" aria-labelledby="lg-judul">
<form class="lg-form" method="dialog" novalidate>
<button class="lg-tutup" type="button" aria-label="Tutup" data-tutup>×</button>
<div class="lg-langkah" data-langkah="1">
  <p class="lg-step">Langkah 1 dari 2</p>
  <h2 id="lg-judul">Langganan <span data-nama-paket></span></h2>
  <div class="lg-paket" role="radiogroup" aria-label="Pilih paket">{pilih_paket}</div>
  <div class="lg-periode" role="radiogroup" aria-label="Periode tagihan">
    <label><input type="radio" name="periode" value="bulanan" checked><span>Bulanan</span></label>
    <label><input type="radio" name="periode" value="tahunan"><span>Tahunan <em>Hemat {12 - P["annual_months_paid"]} bulan</em></span></label>
  </div>
  <label class="lg-field"><span>Jumlah karyawan</span>
    <input type="number" name="karyawan" min="{data["min"]}" max="{data["max"]}" step="1" value="10" inputmode="numeric" required></label>
  {f'<div class="lg-addon">{addon}</div>' if addon else ''}
  <div class="lg-ringkas" aria-live="polite">
    <div><span>Harga per karyawan</span><strong data-harga></strong></div>
    <div data-baris-addon hidden><span>Add-on</span><strong data-addon></strong></div>
    <div class="lg-total"><span>Total <small data-periode-label></small></span><strong data-total></strong></div>
  </div>
  <fieldset class="lg-data"><legend>Data untuk aktivasi akun</legend>
    <label class="lg-field"><span>Nama lengkap</span><input name="nama" autocomplete="name" required></label>
    <label class="lg-field"><span>Nama perusahaan</span><input name="perusahaan" autocomplete="organization" required></label>
    <label class="lg-field lg-penuh"><span>No. WhatsApp</span><input name="wa" type="tel" autocomplete="tel" inputmode="numeric" placeholder="08…" pattern="\\+?[0-9]{{9,15}}" maxlength="16" required></label>
  </fieldset>
  <p class="lg-kecil">Dengan melanjutkan, Anda menyetujui {syarat} dan {privasi} {html.escape(S["brand"])}.</p>
  <p class="lg-galat" data-galat hidden></p>
  <button class="btn btn-primary lg-lanjut" type="button" data-lanjut>Lanjut ke pembayaran <span aria-hidden="true">→</span></button>
</div>
<div class="lg-langkah" data-langkah="2" hidden>
  <p class="lg-step">Langkah 2 dari 2</p>
  <h2>Bayar dengan QRIS</h2>
  <div class="lg-bayar">
    <div class="lg-qris" data-qris></div>
    <div class="lg-detail">
      <p class="lg-label">Total pembayaran</p>
      <p class="lg-nominal" data-total2></p>
      <dl>
        <div><dt>No. pesanan</dt><dd data-order></dd></div>
        <div><dt>Paket</dt><dd data-ringkas-paket></dd></div>
        <div><dt>Karyawan</dt><dd data-ringkas-karyawan></dd></div>
      </dl>
      <p class="lg-status" data-status aria-live="polite"></p>
      <ol class="lg-cara" data-cara></ol>
    </div>
  </div>
  <div class="lg-aksi">
    <button class="btn btn-ghost" type="button" data-kembali>← Ubah pesanan</button>
    <button class="btn btn-primary" type="button" data-ulang hidden>Buat QRIS baru</button>
    <a class="btn btn-primary" data-konfirmasi target="_blank" rel="nofollow noopener" hidden>Kirim pesanan via WhatsApp</a>
  </div>
</div>
<div class="lg-langkah lg-sukses" data-langkah="3" hidden>
  <span class="lg-centang" aria-hidden="true"><svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>
  <h2>Pembayaran diterima</h2>
  <p>Akun {html.escape(S["brand"])} untuk <strong data-sukses-perusahaan></strong> sudah aktif. Masuk sekarang untuk mulai memasang agen di perangkat tim.</p>
  <dl class="lg-sukses-dl"><div><dt>No. pesanan</dt><dd data-sukses-order></dd></div><div><dt>Paket</dt><dd data-sukses-paket></dd></div></dl>
  <a class="btn btn-primary lg-lanjut" data-masuk>Masuk ke {html.escape(S["brand"])} <span aria-hidden="true">→</span></a>
  <p class="lg-kecil">Butuh bantuan pemasangan? <a data-bantuan target="_blank" rel="nofollow noopener">Hubungi tim kami</a>.</p>
</div>
</form>
</dialog>
<script>window.LANGGANAN={json.dumps(data, ensure_ascii=False)};</script>
<script>{JS}</script>"""


JS = r"""(function(){
var D=window.LANGGANAN,dlg=document.getElementById('langganan');if(!D||!dlg||!dlg.showModal)return;
var f=dlg.querySelector('form'),q=function(s){return dlg.querySelector(s)},paket=null,pesanan=null,timer=null,detik=null;
var QR_SVG='<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/></svg>';
function rp(n){return 'Rp'+Math.round(n).toLocaleString('id-ID')}
function tier(n){for(var i=0;i<D.batas.length;i++)if(n<D.batas[i])return i;return D.batas.length}
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
function hitung(){
  var n=Math.min(D.max,Math.max(D.min,parseInt(f.karyawan.value,10)||0)),thn=f.periode.value==='tahunan',t=tier(n),
      bln=thn?D.bulanBayar:1,harga=paket.bulanan[t],add=0;
  [].forEach.call(f.querySelectorAll('[name=addon]:checked'),function(c){add+=D.addon[c.value].bulanan});
  var total=(harga+add)*n*bln;
  q('[data-harga]').textContent=rp(harga)+' /bln ('+D.tierLabel[t]+')';
  q('[data-baris-addon]').hidden=!add;q('[data-addon]').textContent=rp(add)+' /karyawan/bln';
  q('[data-periode-label]').textContent=thn?'(12 bulan, bayar '+D.bulanBayar+')':'(per bulan)';
  q('[data-total]').textContent=rp(total);
  return {n:n,thn:thn,total:total,add:add}
}
function berhenti(){clearTimeout(timer);clearInterval(detik);timer=detik=null}
function buka(id,periode){
  paket=D.paket.filter(function(p){return String(p.id)===String(id)})[0];if(!paket)return false;
  q('[data-nama-paket]').textContent=paket.nama;f.paket.value=String(paket.id);
  f.periode.value=periode==='tahunan'?'tahunan':'bulanan';
  langkah(1);hitung();dlg.showModal();setTimeout(function(){f.karyawan.focus()},50);return true
}
function langkah(n){[].forEach.call(dlg.querySelectorAll('[data-langkah]'),function(el){el.hidden=el.getAttribute('data-langkah')!=String(n)})}
function ringkasan(){
  var h=hitung(),addNama=[].map.call(f.querySelectorAll('[name=addon]:checked'),function(c){return D.addon[c.value].nama});
  return {h:h,per:h.thn?'tahunan':'bulanan',addon:addNama,
    teks:paket.nama+' · '+(h.thn?'Tahunan':'Bulanan')+(addNama.length?' + '+addNama.join(', '):'')}
}
function cara(list){q('[data-cara]').innerHTML=list.map(function(t){return '<li>'+t+'</li>'}).join('')}
function status(t,kelas){var s=q('[data-status]');s.innerHTML=t;s.className='lg-status'+(kelas?' '+kelas:'')}
function tombol(ulang,wa){q('[data-ulang]').hidden=!ulang;q('[data-konfirmasi]').hidden=!wa}
function tampilQR(o){
  var box=q('[data-qris]');
  if(o.qris_image){box.innerHTML='<img src="'+esc(o.qris_image)+'" alt="Kode QRIS pembayaran" width="220" height="220">';return}
  box.innerHTML='<div class="lg-qr" role="img" aria-label="Kode QRIS pembayaran"></div>';
  var buat=function(){new QRCode(box.firstChild,{text:o.qris_string,width:220,height:220,correctLevel:QRCode.CorrectLevel.M})};
  if(window.QRCode)return buat();
  var sc=document.createElement('script');sc.src='https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js';sc.onload=buat;
  sc.onerror=function(){gagal('QRIS tidak bisa ditampilkan. Coba lagi.')};document.head.appendChild(sc)
}
function gagal(t){berhenti();q('[data-qris]').innerHTML='<div class="lg-qris-kosong">'+QR_SVG+'<strong>Gagal memuat QRIS</strong></div>';status(esc(t),'galat');tombol(true,false)}
function hitungMundur(exp){
  clearInterval(detik);var akhir=new Date(exp).getTime();if(!akhir)return;
  var jalan=function(){var s=Math.max(0,Math.round((akhir-Date.now())/1000));
    if(!s){kedaluwarsa();return}
    status('<span class="lg-titik"></span>Menunggu pembayaran · berlaku <strong>'+Math.floor(s/60)+':'+String(s%60).padStart(2,'0')+'</strong>')};
  jalan();detik=setInterval(jalan,1000)
}
function kedaluwarsa(){berhenti();q('[data-qris]').classList.add('lg-qris-habis');status('Waktu pembayaran habis. Buat QRIS baru untuk melanjutkan.','galat');tombol(true,false)}
function cek(){
  if(!pesanan||!dlg.open)return;
  fetch(D.api+'/orders/'+encodeURIComponent(pesanan.order_id),{headers:{Accept:'application/json'}})
    .then(function(r){return r.json()}).then(function(o){
      if(o.status==='paid')return sukses(o);
      if(o.status==='expired')return kedaluwarsa();
      if(o.status==='failed')return gagal('Pembayaran gagal. Silakan buat QRIS baru.');
      timer=setTimeout(cek,3000)})
    .catch(function(){timer=setTimeout(cek,5000)})
}
function sukses(o){
  berhenti();var r=ringkasan();
  q('[data-sukses-perusahaan]').textContent=f.perusahaan.value;q('[data-sukses-order]').textContent=pesanan.order_id;q('[data-sukses-paket]').textContent=r.teks;
  var m=q('[data-masuk]'),u=o.login_url||D.login;if(u)m.href=u;else m.hidden=true;
  var b=q('[data-bantuan]');b.href=D.wa?'https://wa.me/'+D.wa+'?text='+encodeURIComponent('Halo '+D.brand+', saya butuh bantuan pemasangan. No. pesanan: '+pesanan.order_id):'#kontak';
  langkah(3);m.focus()
}
function bayar(){
  var r=ringkasan();berhenti();pesanan=null;q('[data-qris]').classList.remove('lg-qris-habis');
  q('[data-ringkas-paket]').textContent=r.teks;q('[data-ringkas-karyawan]').textContent=r.h.n+' karyawan';
  q('[data-total2]').textContent=rp(r.h.total);
  if(!D.api){  // mode sementara: gateway belum tersambung
    var d=new Date(),id='TB-'+d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0')+'-'+Math.random().toString(36).slice(2,6).toUpperCase();
    q('[data-order]').textContent=id;
    q('[data-qris]').innerHTML='<div class="lg-qris-kosong">'+QR_SVG+'<strong>QRIS belum aktif</strong><span>Kirim pesanan lewat WhatsApp, tim kami mengirimkan QRIS pembayaran.</span></div>';
    status('');cara(['Kirim pesanan lewat WhatsApp.','Bayar QRIS yang kami kirimkan.','Akun diaktifkan dan Anda bisa langsung masuk.']);
    var pesan='Halo '+D.brand+', saya ingin berlangganan.\n\nNo. pesanan: '+id+'\nPaket: '+paket.nama+' ('+r.per+')'+(r.addon.length?'\nAdd-on: '+r.addon.join(', '):'')+
      '\nJumlah karyawan: '+r.h.n+'\nTotal: '+rp(r.h.total)+'\n\nNama: '+f.nama.value+'\nPerusahaan: '+f.perusahaan.value+'\nWhatsApp: '+f.wa.value;
    q('[data-konfirmasi]').href=D.wa?'https://wa.me/'+D.wa+'?text='+encodeURIComponent(pesan):'#kontak';
    tombol(false,true);return
  }
  q('[data-order]').textContent='…';tombol(false,false);
  q('[data-qris]').innerHTML='<div class="lg-qris-kosong"><span class="lg-putar" aria-hidden="true"></span><span>Membuat QRIS…</span></div>';status('');
  cara(['Buka aplikasi bank atau e-wallet, pilih <strong>Bayar / Scan QRIS</strong>.','Pindai kode dan bayar sesuai nominal.','Akun aktif otomatis setelah pembayaran diterima.']);
  fetch(D.api+'/orders',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},
    body:JSON.stringify({paket:paket.id,periode:r.per,karyawan:r.h.n,addon:r.addon,nama:f.nama.value.trim(),perusahaan:f.perusahaan.value.trim(),whatsapp:f.wa.value})})
    .then(function(x){if(!x.ok)throw 0;return x.json()}).then(function(o){
      if(!o.order_id||!(o.qris_image||o.qris_string))throw 0;
      pesanan=o;q('[data-order]').textContent=o.order_id;if(o.amount)q('[data-total2]').textContent=rp(o.amount);
      tampilQR(o);hitungMundur(o.expires_at);timer=setTimeout(cek,3000)})
    .catch(function(){gagal('QRIS belum bisa dibuat. Periksa koneksi lalu coba lagi.')})
}
function lanjut(){
  var g=q('[data-galat]'),kosong=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.checkValidity()});
  if(kosong.length){var nama=function(i){return i.closest('label').querySelector('span').textContent},
      belum=kosong.filter(function(i){return !i.value.trim()}),salah=kosong.filter(function(i){return i.value.trim()});
    g.textContent=(belum.length?'Lengkapi: '+belum.map(nama).join(', ')+'. ':'')+(salah.indexOf(f.wa)>-1?'No. WhatsApp harus 9–15 angka.':'');
    g.hidden=false;kosong[0].focus();return}
  g.hidden=true;langkah(2);bayar();q('[data-kembali]').focus()
}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.js-langganan,[data-beli]');if(!b)return;
  var thn=document.querySelector('.periode .p-thn:checked');
  if(buka(b.getAttribute('data-paket')||D.unggulan,thn?'tahunan':(b.getAttribute('data-periode')||'bulanan')))e.preventDefault()
});
f.addEventListener('input',function(e){
  if(e.target===f.wa){var w=f.wa.value,p=w.trim().charAt(0)==='+'?'+':'',d=w.replace(/\D/g,'').slice(0,15);if(p+d!==w)f.wa.value=p+d}
  if(e.target===f.karyawan){var v=f.karyawan.value.replace(/\D/g,'').slice(0,String(D.max).length);if(+v>D.max)v=String(D.max);if(v!==f.karyawan.value)f.karyawan.value=v}
  if(e.target.name==='paket'){paket=D.paket.filter(function(p){return String(p.id)===e.target.value})[0];q('[data-nama-paket]').textContent=paket.nama}
  if(paket)hitung()});
q('[data-lanjut]').addEventListener('click',lanjut);
q('[data-kembali]').addEventListener('click',function(){berhenti();langkah(1)});
q('[data-ulang]').addEventListener('click',bayar);
q('[data-tutup]').addEventListener('click',function(){dlg.close()});
dlg.addEventListener('close',berhenti);
dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
document.addEventListener('visibilitychange',function(){if(!document.hidden&&pesanan&&dlg.open&&q('[data-langkah="2"]').hidden===false){clearTimeout(timer);cek()}});
})();"""
