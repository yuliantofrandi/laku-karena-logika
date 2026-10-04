"""Modal langganan di halaman Harga: pilih paket → isi data & jumlah karyawan → bayar dengan QRIS.

Alur jual Timebase: langsung berlangganan (pilih paket → bayar → aktif), bukan demo.
Tombol "Pilih <paket>" di tabel harga diberi class `js-langganan` + data-paket; tanpa JS tetap
menjadi link biasa (fallback ke checkout_url / #pilih-skema).

Konfigurasi di site.json:
  "langganan": {"qris_url": "", "min_karyawan": 1}
  qris_url boleh memuat {order} {total} {paket} {periode} {karyawan}. Kosong = kotak "QRIS sedang
  disiapkan" + konfirmasi pesanan lewat WhatsApp (build memberi WARNING).

Data formulir tidak dikirim ke server mana pun dari halaman ini: hanya dipakai untuk menyusun
ringkasan pesanan dan pesan WhatsApp yang dikirim sendiri oleh pengunjung.
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
        "qris": cfg.get("qris_url", ""),
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
    privasi = '<a href="/kebijakan-privasi" target="_blank">Kebijakan Privasi</a>'
    syarat = '<a href="/syarat-layanan" target="_blank">Syarat Layanan</a>'
    return f"""<dialog class="lg" id="langganan" aria-labelledby="lg-judul">
<form class="lg-form" method="dialog" novalidate>
<button class="lg-tutup" type="button" aria-label="Tutup" data-tutup>×</button>
<div class="lg-langkah" data-langkah="1">
  <p class="lg-step">Langkah 1 dari 2</p>
  <h2 id="lg-judul">Langganan <span data-nama-paket></span></h2>
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
    <label class="lg-field lg-penuh"><span>No. WhatsApp</span><input name="wa" type="tel" autocomplete="tel" inputmode="tel" placeholder="08…" required></label>
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
      <ol class="lg-cara"><li>Buka aplikasi bank atau e-wallet, pilih <strong>Bayar / Scan QRIS</strong>.</li>
      <li>Pindai kode QRIS dan pastikan nominal sesuai.</li><li>Kirim konfirmasi; akun diaktifkan dan tim kami membantu pemasangan.</li></ol>
    </div>
  </div>
  <div class="lg-aksi">
    <button class="btn btn-ghost" type="button" data-kembali>← Ubah pesanan</button>
    <a class="btn btn-primary" data-konfirmasi target="_blank" rel="nofollow noopener">Konfirmasi via WhatsApp</a>
  </div>
</div>
</form>
</dialog>
<script>window.LANGGANAN={json.dumps(data, ensure_ascii=False)};</script>
<script>{JS}</script>"""


JS = r"""(function(){
var D=window.LANGGANAN,dlg=document.getElementById('langganan');if(!D||!dlg||!dlg.showModal)return;
var f=dlg.querySelector('form'),q=function(s){return dlg.querySelector(s)},paket=null,order='';
function rp(n){return 'Rp'+Math.round(n).toLocaleString('id-ID')}
function tier(n){for(var i=0;i<D.batas.length;i++)if(n<D.batas[i])return i;return D.batas.length}
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
function buka(id,periode){
  paket=D.paket.filter(function(p){return String(p.id)===String(id)})[0];if(!paket)return false;
  q('[data-nama-paket]').textContent=paket.nama;
  f.periode.value=periode==='tahunan'?'tahunan':'bulanan';
  langkah(1);hitung();dlg.showModal();setTimeout(function(){f.karyawan.focus()},50);return true
}
function langkah(n){[].forEach.call(dlg.querySelectorAll('[data-langkah]'),function(el){el.hidden=el.getAttribute('data-langkah')!=String(n)})}
function lanjut(){
  var g=q('[data-galat]'),kosong=[].filter.call(f.querySelectorAll('[required]'),function(i){return !i.checkValidity()});
  if(kosong.length){g.textContent='Lengkapi data yang ditandai: '+kosong.map(function(i){return i.closest('label').querySelector('span').textContent}).join(', ')+'.';g.hidden=false;kosong[0].focus();return}
  g.hidden=true;var h=hitung(),d=new Date();
  order='TB-'+d.getFullYear()+String(d.getMonth()+1).padStart(2,'0')+String(d.getDate()).padStart(2,'0')+'-'+Math.random().toString(36).slice(2,6).toUpperCase();
  var per=h.thn?'tahunan':'bulanan',addNama=[].map.call(f.querySelectorAll('[name=addon]:checked'),function(c){return D.addon[c.value].nama});
  q('[data-total2]').textContent=rp(h.total);q('[data-order]').textContent=order;
  q('[data-ringkas-paket]').textContent=paket.nama+' · '+(h.thn?'Tahunan':'Bulanan')+(addNama.length?' + '+addNama.join(', '):'');
  q('[data-ringkas-karyawan]').textContent=h.n+' karyawan';
  var box=q('[data-qris]');
  if(D.qris){var u=D.qris.replace('{order}',order).replace('{total}',Math.round(h.total)).replace('{paket}',paket.id).replace('{periode}',per).replace('{karyawan}',h.n);
    box.innerHTML=/\.(png|jpe?g|svg|webp)(\?|$)/i.test(u)?'<img src="'+u+'" alt="Kode QRIS pembayaran" width="220" height="220">':'<a class="btn btn-primary" href="'+u+'" target="_blank" rel="noopener">Tampilkan QRIS</a>'}
  else box.innerHTML='<div class="lg-qris-kosong"><svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/></svg><strong>QRIS sedang disiapkan</strong><span>Kirim pesanan lewat WhatsApp, tim kami mengirimkan QRIS pembayaran.</span></div>';
  var pesan='Halo '+D.brand+', saya ingin berlangganan.\n\nNo. pesanan: '+order+'\nPaket: '+paket.nama+' ('+per+')'+(addNama.length?'\nAdd-on: '+addNama.join(', '):'')+
    '\nJumlah karyawan: '+h.n+'\nTotal: '+rp(h.total)+'\n\nNama: '+f.nama.value+'\nPerusahaan: '+f.perusahaan.value+'\nWhatsApp: '+f.wa.value;
  var k=q('[data-konfirmasi]');k.href=D.wa?'https://wa.me/'+D.wa+'?text='+encodeURIComponent(pesan):'#kontak';
  k.textContent=D.qris?'Saya sudah bayar — konfirmasi':'Kirim pesanan via WhatsApp';
  langkah(2);dlg.querySelector('[data-langkah="2"] h2').focus&&q('[data-kembali]').focus()
}
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.js-langganan');if(!b)return;
  var thn=document.querySelector('.periode .p-thn:checked');
  if(buka(b.getAttribute('data-paket'),thn?'tahunan':b.getAttribute('data-periode')))e.preventDefault()
});
f.addEventListener('input',function(e){
  if(e.target===f.karyawan){var v=f.karyawan.value.replace(/\D/g,'').slice(0,String(D.max).length);if(+v>D.max)v=String(D.max);if(v!==f.karyawan.value)f.karyawan.value=v}
  if(paket)hitung()});
q('[data-lanjut]').addEventListener('click',lanjut);
q('[data-kembali]').addEventListener('click',function(){langkah(1)});
q('[data-tutup]').addEventListener('click',function(){dlg.close()});
dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
})();"""
