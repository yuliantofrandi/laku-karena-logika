// Penyamaran data di tab aplikasi pengguna SEBELUM screenshot diambil.
// Jalankan lewat javascript_tool (Claude in Chrome) di tab aplikasi: tempel seluruh isi
// file ini, lalu panggil  samarkan({ 'Nama Asli': 'Nama Dummy', 'Jabatan Asli': 'Jabatan Dummy', ... })
//
// Aturan privasi pengguna:
//   - Foto profil      → TIDAK diubah, tidak di-blur (gambar tidak disentuh sama sekali)
//   - Nama orang       → diganti nama dummy (lewat peta di atas)
//   - Nama jabatan     → diganti jabatan dummy (lewat peta di atas)
//   - Nomor telepon    → 4 digit terakhir di-blur (otomatis, tanpa peta)
//
// Perubahan hanya di DOM tab ini (tidak disimpan ke server). Muat ulang halaman setelah
// screenshot selesai untuk mengembalikan tampilan asli.
function samarkan(peta = {}) {
  const kunci = Object.keys(peta).filter(Boolean).sort((a, b) => b.length - a.length);
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const reNama = kunci.length ? new RegExp(kunci.map(esc).join('|'), 'g') : null;
  // Nomor HP/telepon Indonesia (HP & kantor): +62 / 62 / 0 / (021), total 9–15 digit, boleh dipisah
  // spasi, titik, atau tanda hubung. Tidak mulai di tengah angka lain (mis. harga "10.000.000").
  const reTelMentah = /(?<![\d.,])(?:\+?62|\(?0\d{1,3}\)?)(?:[\s.-]{0,2}\d){6,12}/g;
  const nDigit = m => (m.match(/\d/g) || []).length;
  const reTel = { lastIndex: 0,
    test(s) { reTelMentah.lastIndex = 0; let m; while ((m = reTelMentah.exec(s))) if (nDigit(m[0]) >= 9) return true; return false; },
    exec(s) { let m; while ((m = reTelMentah.exec(s))) if (nDigit(m[0]) >= 9) return m; reTelMentah.lastIndex = 0; return null; } };
  const gantiTel = (s, f) => s.replace(reTelMentah, m => nDigit(m) >= 9 ? f(m) : m);
  let nGanti = 0, nTel = 0;

  const ganti = s => reNama ? s.replace(reNama, m => (nGanti++, peta[m])) : s;
  // posisi awal 4 digit terakhir di dalam string nomor
  const awalEmpat = m => { let k = 0; for (let i = m.length - 1; i >= 0; i--) if (/\d/.test(m[i]) && ++k === 4) return i; return 0; };

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const tn of nodes) {
    const el = tn.parentElement;
    if (!el || el.closest('script,style,noscript,[data-samar]')) continue;
    const s = ganti(tn.nodeValue);
    if (!reTel.test(s)) { if (s !== tn.nodeValue) tn.nodeValue = s; continue; }
    reTelMentah.lastIndex = 0;
    const frag = document.createDocumentFragment(); let last = 0, m;
    while ((m = reTel.exec(s))) {
      const k = awalEmpat(m[0]);
      frag.append(s.slice(last, m.index) + m[0].slice(0, k));
      const b = document.createElement('span');
      b.dataset.samar = '1'; b.textContent = m[0].slice(k);
      b.style.cssText = 'filter:blur(5px);display:inline-block;user-select:none';
      frag.append(b); last = m.index + m[0].length; nTel++;
    }
    frag.append(s.slice(last));
    tn.replaceWith(frag);
  }
  // Isi kolom form: nama/jabatan diganti; nomor tidak bisa di-blur sebagian di dalam input → 4 digit terakhir jadi ••••
  document.querySelectorAll('input:not([type=password]):not([type=hidden]),textarea').forEach(el => {
    let v = ganti(el.value);
    v = gantiTel(v, m => { nTel++; const k = awalEmpat(m); return m.slice(0, k) + m.slice(k).replace(/\d/g, '•'); });
    if (v !== el.value) el.value = v;
  });
  // Atribut yang bisa tampil sebagai tooltip/teks pengganti
  document.querySelectorAll('[title],[aria-label],[alt]').forEach(el => {
    ['title', 'aria-label', 'alt'].forEach(a => { const v = el.getAttribute(a); if (v) el.setAttribute(a, ganti(v)); });
  });
  return { namaJabatanDiganti: nGanti, nomorDiblur: nTel };
}
