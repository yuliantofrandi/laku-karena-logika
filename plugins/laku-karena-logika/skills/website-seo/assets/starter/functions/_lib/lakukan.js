// Data Blog & Panduan dari API publik Lakukan (tanpa API key), diambil di server (Cloudflare Pages Functions).
// Konfigurasi ditulis build.py ke dist/_templates/lakukan.json (dari site.json → lakukan).
// Setiap respons API disimpan di cache edge CACHE_DETIK, jadi artikel baru/ubahan di CMS tampil ≤ 10 menit tanpa build ulang.

export const CACHE_DETIK = 600;

let CFG = null;
/** Konfigurasi situs dari build (brand, site_url, company_slug, kategori, blog_lead, cta_html, build). */
export async function config(ctx) {
  if (CFG) return CFG;
  const res = await ctx.env.ASSETS.fetch(new URL('/_templates/lakukan.json', ctx.request.url));
  CFG = await res.json();
  return CFG;
}

async function get(ctx, cfg, path) {
  const url = (cfg.api || 'https://api.lakukan.id/api').replace(/\/$/, '') + path;
  const key = new Request(`${url}#${cfg.company_slug}`);
  const cache = caches.default;
  const hit = await cache.match(key);
  if (hit) return (await hit.json()).data;
  const res = await fetch(url, {
    headers: {
      'X-Company-Slug': cfg.company_slug, Accept: 'application/json',
      // Cloudflare di depan API menolak user agent kosong/bawaan
      'User-Agent': `${cfg.brand || 'Website'}/1.0 (+${cfg.site_url || 'pages.dev'})`,
    },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`API Lakukan ${res.status} pada ${path}`);
  const body = await res.text();
  ctx.waitUntil(cache.put(key, new Response(body, {
    headers: { 'Content-Type': 'application/json', 'Cache-Control': `public, max-age=${CACHE_DETIK}` },
  })));
  return JSON.parse(body).data;
}

/** Slug kategori utama artikel. API sekarang mengirim `categories` (array); respons lama memakai `category`. */
export function katSlug(a) {
  const list = Array.isArray(a && a.categories) ? a.categories : a && a.category ? [a.category] : [];
  const c = list[0];
  return c ? (typeof c === 'string' ? c : c.slug) : '';
}

/** Artikel yang tampak uji coba/draf (tanpa ringkasan dan isi < 60 kata) tidak diterbitkan. */
export function draf(a) {
  const kata = (a.content || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
  return !(a.excerpt || '').trim() && kata < 60;
}

/** Pohon kategori + daftar artikel (tanpa isi). Panduan = anak kategori_panduan; Blog = kategori_blog + anaknya. */
export async function data(ctx) {
  const cfg = await config(ctx);
  const kategori = (await get(ctx, cfg, '/article-categories')) || [];
  const daftar = [];
  for (let page = 1; page <= 20; page++) {
    const d = await get(ctx, cfg, `/articles?limit=100&page=${page}`);
    if (!d || !d.length) break;
    daftar.push(...d);
    if (d.length < 100) break;
  }
  const cari = (s) => kategori.find((k) => k.slug === s);
  const urut = (xs) => [...(xs || [])].sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
  const induk = cari(cfg.kategori_panduan || 'docs');
  const anak = induk ? urut(induk.children) : [];
  const blog = cari(cfg.kategori_blog || 'blog');
  const blogKat = blog ? [{ ...blog, children: undefined }, ...urut(blog.children)] : [];
  const terbit = daftar.filter((a) => a.status === 'published');
  // daftar API tidak memuat isi; artikel tanpa ringkasan diambil lengkap supaya aturan draf tetap sama dengan build
  const tanpaRingkas = terbit.filter((a) => !(a.excerpt || '').trim());
  const lengkap = await Promise.all(tanpaRingkas.map((a) => artikel(ctx, a.slug)));
  tanpaRingkas.forEach((a, i) => { a.content = (lengkap[i] && lengkap[i].content) || ''; });
  return { cfg, kategori: anak, blogKat, artikel: terbit };
}

/** Satu artikel lengkap (dengan isi HTML). */
export async function artikel(ctx, slug) {
  const cfg = await config(ctx);
  return get(ctx, cfg, `/articles/${encodeURIComponent(slug)}`);
}

/** 5 artikel Blog terbaru untuk kolom footer: [{judul, url}]. */
export function blogTerbaru(d, n = 5) {
  const slugs = new Set(d.blogKat.map((k) => k.slug));
  return d.artikel
    .filter((a) => slugs.has(katSlug(a)) && !draf(a))
    .sort((a, b) => (b.published_at || '').localeCompare(a.published_at || ''))
    .slice(0, n)
    .map((a) => ({ judul: a.title, url: `/blog/${a.slug}` }));
}

/** Kategori Panduan yang berisi artikel, untuk kolom footer: [{nama, url}]. */
export function panduanFooter(d) {
  return d.kategori
    .filter((k) => d.artikel.some((a) => katSlug(a) === k.slug))
    .map((k) => ({ nama: k.name, url: `/panduan/${slugKat(k, d.cfg)}` }));
}

/** timebase-memulai → memulai (awalan company slug dibuang supaya URL ringkas). */
export function slugKat(k, cfg) {
  const pre = cfg.company_slug + '-';
  return k.slug.startsWith(pre) ? k.slug.slice(pre.length) : k.slug;
}
