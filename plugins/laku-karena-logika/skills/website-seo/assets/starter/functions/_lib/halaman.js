// Isi halaman Panduan & Blog (port dari lakukan.py, markup & class CSS sama persis dengan versi build lama).
// Setiap fungsi mengembalikan {page, body, index} atau null (404). page = data hero/SEO untuk shell.
import { data, artikel, katSlug, draf, slugKat } from './lakukan.js';

const CUR = ' aria-current="page"';
const PER_HALAMAN = 12;
export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

export function bersihkan(isi) {
  isi = String(isi || '');
  isi = isi.replace(/<(script|style|iframe|object|embed)\b[\s\S]*?<\/\1>/gi, '');
  isi = isi.replace(/<(script|iframe|object|embed)\b[^>]*\/?>/gi, '');
  isi = isi.replace(/\s+on\w+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '');
  isi = isi.replace(/(href|src)\s*=\s*"\s*javascript:[^"]*"/gi, '$1="#"');
  isi = isi.replace(/<img(?![^>]*\bloading=)/g, '<img loading="lazy" decoding="async"');
  // tabel dibungkus wadah geser-samping: di HP hanya tabelnya yang bisa digeser, bukan seluruh halaman
  isi = isi.replace(/(<div class="table-wrap">)?(<table\b[\s\S]*?<\/table>)/gi, (m, w, t) => (w ? m : `<div class="table-wrap">${t}</div>`));
  return isi;
}

const BLN = 'Januari Februari Maret April Mei Juni Juli Agustus September Oktober November Desember'.split(' ');
export function tanggal(iso) {
  const [y, m, d] = String(iso).slice(0, 10).split('-');
  return `${parseInt(d, 10)} ${BLN[parseInt(m, 10) - 1]} ${y}`;
}

const IKON_KAT = {
  mulai: '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  navigasi: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
  akun: '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
  monitor: '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
  manajemen: '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
  referensi: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5"/><path d="M9 8h6"/>',
};
function ikonKat(k, cfg) {
  const s = slugKat(k, cfg);
  const key = Object.keys(IKON_KAT).find((x) => s.includes(x));
  return '<span class="ikon-bulat" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" '
    + `stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${IKON_KAT[key || 'referensi']}</svg></span>`;
}

function daftarIsi(isi) {
  const toc = []; const dipakai = new Set();
  const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&nbsp;/g, ' ');
  isi = isi.replace(/<h2((?:(?!\bid=)[^>])*)>([\s\S]*?)<\/h2>/g, (m, attr, inner) => {
    const judul = inner.replace(/<[^>]+>/g, '').trim();
    const dasar = judul.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'bagian';
    let id = dasar; let n = 2;
    while (dipakai.has(id)) { id = `${dasar}-${n}`; n += 1; }
    dipakai.add(id);
    toc.push([id, unesc(judul)]);
    return `<h2${attr} id="${id}">${inner}</h2>`;
  });
  return [isi, toc];
}

const TOC_JS = `<script>(function(){var l=[].slice.call(document.querySelectorAll('.bl-toc a'));if(!l.length)return;
var h=l.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}),t=0;
function u(){t=0;var k=0;for(var i=0;i<h.length;i++){if(h[i]&&h[i].getBoundingClientRect().top<130)k=i}
l.forEach(function(a,i){a.classList.toggle('aktif',i===k)})}
addEventListener('scroll',function(){if(!t)t=requestAnimationFrame(u)},{passive:true});u()})()</script>`;

function diperbarui(a) {
  const iso = a.updated_at || a.published_at || a.created_at;
  return `<p class="pd-meta">Terakhir diperbarui <time datetime="${iso.slice(0, 10)}">${tanggal(iso)}</time></p>`;
}

function kartu(a, url) {
  const cover = a.cover_url
    ? `<img class="pd-cover" src="${esc(a.cover_url)}" alt="" loading="lazy" decoding="async">`
    : '<span class="pd-cover pd-cover-kosong" aria-hidden="true"></span>';
  return `<a class="pd-kartu" href="${url}">${cover}<span class="pd-isi">`
    + `<span class="pd-judul">${esc(a.title)}</span>`
    + `<span class="pd-ringkas">${esc(a.excerpt || '')}</span></span></a>`;
}

// ---------------- Panduan ----------------

export async function panduan(ctx, segs) {
  const d = await data(ctx);
  const { cfg } = d; const brand = cfg.brand;
  const kats = d.kategori.filter((k) => d.artikel.some((a) => katSlug(a) === k.slug));
  const perKat = Object.fromEntries(kats.map((k) => [k.slug, d.artikel.filter((a) => katSlug(a) === k.slug)]));
  const urlKat = Object.fromEntries(kats.map((k) => [k.slug, `/panduan/${slugKat(k, cfg)}`]));
  const urlArt = {};
  for (const a of d.artikel) if (urlKat[katSlug(a)]) urlArt[a.slug] = `${urlKat[katSlug(a)]}/${a.slug}`;
  const jumlah = kats.reduce((n, k) => n + perKat[k.slug].length, 0);
  if (!kats.length) return null;

  const chips = (aktif) => '<nav class="pd-chips" aria-label="Kategori panduan">'
    + `<a href="/panduan"${aktif ? '' : CUR}>Semua <span>${jumlah}</span></a>`
    + kats.map((k) => `<a href="${urlKat[k.slug]}"${aktif === k.slug ? CUR : ''}>${esc(k.name)} <span>${perKat[k.slug].length}</span></a>`).join('')
    + '</nav><script>(function(n){var a=n&&n.querySelector("[aria-current]");if(a)n.scrollLeft=a.offsetLeft-20})(document.currentScript.previousElementSibling)</script>';
  const grid = (arts) => '<div class="pd-grid">' + arts.map((a) => kartu(a, urlArt[a.slug])).join('') + '</div>';

  if (segs.length === 0) {
    const kartuKat = (k) => {
      const items = perKat[k.slug].map((a) => `<li><a href="${urlArt[a.slug]}">${esc(a.title)}</a></li>`).join('');
      return `<section class="pd-katkartu" id="${slugKat(k, cfg)}">${ikonKat(k, cfg)}`
        + `<h2><a href="${urlKat[k.slug]}">${esc(k.name)}</a></h2>`
        + `<p>${esc(k.description || '')}</p><ul>${items}</ul>`
        + `<a class="pd-lihat" href="${urlKat[k.slug]}">${perKat[k.slug].length} panduan <span aria-hidden="true">→</span></a></section>`;
    };
    return {
      page: { slug: '/panduan', title: `Panduan ${brand}: Cara Memakai ${brand}`,
        meta: `Panduan memakai ${brand} per kategori: memulai, navigasi & akun, monitoring, manajemen, dan referensi istilah.`,
        h1: `Panduan ${brand}`, eyebrow: 'Pusat bantuan', lead: esc(`Langkah demi langkah memakai ${brand}, dikelompokkan per kategori.`),
        crumbs: [['Panduan', '/panduan']] },
      body: `<section class="band pd-band"><div class="wrap">${chips()}<div class="pd-katgrid">${kats.map(kartuKat).join('')}</div></div></section>`,
      index: true,
    };
  }

  const k = kats.find((x) => slugKat(x, cfg) === segs[0]);
  if (!k) return null;
  if (segs.length === 1) {
    return {
      page: { slug: urlKat[k.slug], title: `${k.name} — Panduan ${brand}`,
        meta: k.description || `Panduan ${brand} kategori ${k.name}.`, h1: k.name, eyebrow: 'Panduan',
        lead: esc(k.description || ''), crumbs: [['Panduan', '/panduan'], [k.name, urlKat[k.slug]]] },
      body: `<section class="band pd-band"><div class="wrap">${chips(k.slug)}${grid(perKat[k.slug])}</div></section>`,
      index: true,
    };
  }
  if (segs.length !== 2) return null;
  const arts = perKat[k.slug];
  const i = arts.findIndex((x) => x.slug === segs[1]);
  if (i < 0) return null;
  const a = await artikel(ctx, arts[i].slug);
  if (!a) return null;
  const nav = kats.map((kk) => {
    const cur = kk.slug === k.slug;
    const items = perKat[kk.slug].map((x) => `<li><a href="${urlArt[x.slug]}"${x.slug === a.slug ? CUR : ''}>${esc(x.title)}</a></li>`).join('');
    return `<details class="dok-grup${cur ? ' aktif' : ''}"${cur ? ' open' : ''}><summary>${esc(kk.name)}</summary><ol>${items}</ol></details>`;
  }).join('');
  const navHtml = `<aside class="dok-nav" aria-label="Daftar panduan">${nav}</aside>`
    + `<details class="dok-toc-hp"><summary>Daftar panduan</summary>${nav}</details>`;
  const pn = [[arts[i - 1], 'prev', '← Sebelumnya'], [arts[i + 1], 'next', 'Berikutnya →']]
    .filter(([x]) => x).map(([x, cls, lab]) => `<a class="pd-pn ${cls}" href="${urlArt[x.slug]}"><span>${lab}</span>${esc(x.title)}</a>`).join('');
  const pnNav = pn ? `<nav class="pd-pn-wrap" aria-label="Panduan lain">${pn}</nav>` : '';
  const cover = a.cover_url ? `<img class="pd-hero-img" src="${esc(a.cover_url)}" alt="" decoding="async" fetchpriority="high">` : '';
  return {
    page: { slug: urlArt[a.slug], title: `${a.title} — Panduan ${brand}`, meta: a.excerpt || a.title, h1: a.title,
      eyebrow: k.name, lead: esc(a.excerpt || ''),
      crumbs: [['Panduan', '/panduan'], [k.name, urlKat[k.slug]], [a.title, urlArt[a.slug]]],
      artikel: { published: a.published_at, updated: a.updated_at || a.published_at, author: a.author || brand, image: a.cover_url } },
    body: `<section class="band dok-band"><div class="wrap"><div class="dok-grid">${navHtml}`
      + `<div class="dokumen pd-artikel">${diperbarui(a)}${cover}${bersihkan(a.content)}${pnNav}</div></div></div></section>`,
    index: true,
  };
}

// ---------------- Blog ----------------

export async function blog(ctx, segs) {
  const d = await data(ctx);
  const { cfg } = d; const brand = cfg.brand;
  const bk = d.blogKat;
  const slugsBlog = new Set(bk.map((k) => k.slug));
  const arts = d.artikel.filter((a) => slugsBlog.has(katSlug(a)) && !draf(a))
    .sort((a, b) => (b.published_at || '').localeCompare(a.published_at || ''));
  const sub = bk.slice(1).filter((k) => arts.some((a) => katSlug(a) === k.slug));
  const urlSub = Object.fromEntries(sub.map((k) => [k.slug, `/blog/kategori/${slugKat(k, cfg)}`]));
  const namaKat = Object.fromEntries(bk.map((k) => [k.slug, k.name]));
  const url = (a) => `/blog/${a.slug}`;
  const lead = (cfg.blog_lead || 'Artikel dan wawasan terbaru dari {brand}.').replace('{brand}', brand);

  const chips = (aktif) => (!sub.length ? '' : '<nav class="pd-chips" aria-label="Kategori blog">'
    + `<a href="/blog"${aktif ? '' : CUR}>Semua <span>${arts.length}</span></a>`
    + sub.map((k) => `<a href="${urlSub[k.slug]}"${aktif === k.slug ? CUR : ''}>${esc(k.name)} <span>${arts.filter((a) => katSlug(a) === k.slug).length}</span></a>`).join('')
    + '</nav>');
  const metaBaris = (a) => `${esc(namaKat[katSlug(a)] || 'Blog')} · ${tanggal(a.published_at || a.created_at)}`;
  const kartuBlog = (a, utama) => {
    const cover = a.cover_url
      ? `<img class="pd-cover" src="${esc(a.cover_url)}" alt="" loading="${utama ? 'eager' : 'lazy'}" decoding="async">`
      : '<span class="pd-cover pd-cover-kosong" aria-hidden="true"></span>';
    return `<a class="pd-kartu${utama ? ' bl-utama' : ''}" href="${url(a)}">${cover}<span class="pd-isi">`
      + `<span class="bl-meta">${metaBaris(a)}</span><span class="pd-judul">${esc(a.title)}</span>`
      + `<span class="pd-ringkas">${esc(a.excerpt || '')}</span></span></a>`;
  };
  const daftar = (list, aktif, base, n) => {
    const total = Math.max(1, Math.ceil(list.length / PER_HALAMAN));
    if (n < 1 || n > total) return null;
    const isi = list.slice((n - 1) * PER_HALAMAN, n * PER_HALAMAN);
    let grid;
    if (isi.length) {
      const utama = n === 1 ? kartuBlog(isi[0], true) : '';
      const sisa = n === 1 ? isi.slice(1) : isi;
      grid = utama + (sisa.length ? '<div class="pd-grid">' + sisa.map((a) => kartuBlog(a)).join('') + '</div>' : '');
    } else {
      const linkPd = d.kategori.length ? ` Sementara itu, baca <a href="/panduan">panduan memakai ${brand}</a>.` : '';
      grid = '<div class="bl-kosong"><span class="ikon-bulat" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26" '
        + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        + '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></span>'
        + `<h2>Artikel pertama segera terbit</h2><p>Kami sedang menyiapkan tulisan pertama.${linkPd}</p></div>`;
    }
    const link = (i) => (i === 1 ? base : `${base}/halaman/${i}`);
    const pag = total > 1 ? '<nav class="bl-pag" aria-label="Halaman">'
      + Array.from({ length: total }, (_, j) => `<a href="${link(j + 1)}"${j + 1 === n ? CUR : ''}>${j + 1}</a>`).join('') + '</nav>' : '';
    return { body: `<section class="band pd-band"><div class="wrap">${chips(aktif)}${grid}${pag}</div></section>`, ada: isi.length > 0 };
  };
  const halamanKe = (s) => (s && /^[1-9]\d*$/.test(s) ? parseInt(s, 10) : NaN);

  // /blog · /blog/halaman/N
  if (segs.length === 0 || (segs[0] === 'halaman' && segs.length === 2)) {
    const n = segs.length ? halamanKe(segs[1]) : 1;
    if (n === 1 && segs.length) return { redirect: '/blog' };
    const r = daftar(arts, null, '/blog', n);
    if (!r) return null;
    return {
      page: { slug: n === 1 ? '/blog' : `/blog/halaman/${n}`, title: `Blog ${brand}` + (n > 1 ? ` — Halaman ${n}` : ''),
        meta: lead, h1: `Blog ${brand}`, eyebrow: cfg.blog_eyebrow || 'Pusat edukasi', lead: esc(lead), crumbs: [['Blog', '/blog']] },
      body: r.body, index: r.ada,
    };
  }
  // /blog/kategori/<k> · /blog/kategori/<k>/halaman/N
  if (segs[0] === 'kategori' && (segs.length === 2 || (segs.length === 4 && segs[2] === 'halaman'))) {
    const k = sub.find((x) => slugKat(x, cfg) === segs[1]);
    if (!k) return null;
    const n = segs.length === 4 ? halamanKe(segs[3]) : 1;
    if (n === 1 && segs.length === 4) return { redirect: urlSub[k.slug] };
    const r = daftar(arts.filter((a) => katSlug(a) === k.slug), k.slug, urlSub[k.slug], n);
    if (!r) return null;
    return {
      page: { slug: n === 1 ? urlSub[k.slug] : `${urlSub[k.slug]}/halaman/${n}`, title: `${k.name} — Blog ${brand}`,
        meta: k.description || `Artikel ${brand} kategori ${k.name}.`, h1: k.name, eyebrow: 'Blog',
        lead: esc(k.description || ''), crumbs: [['Blog', '/blog'], [k.name, urlSub[k.slug]]] },
      body: r.body, index: r.ada,
    };
  }
  // /blog/<artikel>
  if (segs.length !== 1) return null;
  const ringkas = arts.find((x) => x.slug === segs[0]);
  if (!ringkas) return null;
  const a = await artikel(ctx, ringkas.slug);
  if (!a || draf(a)) return null;
  const [isi, toc] = daftarIsi(bersihkan(a.content));
  // kolom kanan (sticky): daftar isi saja; artikel terbaru sudah ada di footer (permintaan user)
  const blokToc = toc.length >= 2 ? '<nav class="bl-toc" aria-label="Di artikel ini"><p class="bl-samping-judul">Di artikel ini</p><ol>'
    + toc.map(([id, t]) => `<li><a href="#${id}">${esc(t)}</a></li>`).join('') + '</ol></nav>' : '';
  const samping = blokToc ? `<aside class="bl-samping">${blokToc}</aside>` : '';
  const cover = a.cover_url ? `<img class="pd-hero-img" src="${esc(a.cover_url)}" alt="" decoding="async" fetchpriority="high">` : '';
  const kat = namaKat[katSlug(a)] || 'Blog';
  const crumbs = [['Blog', '/blog'], ...(urlSub[katSlug(a)] ? [[kat, urlSub[katSlug(a)]]] : []), [a.title, url(a)]];
  return {
    page: { slug: url(a), title: `${a.title} — Blog ${brand}`, meta: a.excerpt || a.title, h1: a.title, eyebrow: kat,
      lead: esc(a.excerpt || ''), crumbs,
      artikel: { tipe: 'BlogPosting', published: a.published_at || a.created_at, updated: a.updated_at || a.created_at,
        author: a.author || brand, image: a.cover_url } },
    body: `<section class="band dok-band"><div class="wrap"><div class="bl-grid${samping ? '' : ' tunggal'}"><div class="bl-artikel dokumen">`
      + `${diperbarui(a)}${cover}${isi}</div>${samping}</div></div></section>${blokToc ? TOC_JS : ''}${cfg.cta_html || ''}`,
    // artikel asal halaman hukum yang belum direview tetap noindex (site.json legal_reviewed, diteruskan build)
    index: !(cfg.noindex || []).includes(url(a)),
  };
}
