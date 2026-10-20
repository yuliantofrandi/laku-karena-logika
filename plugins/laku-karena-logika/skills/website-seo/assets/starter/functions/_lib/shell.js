// Membungkus isi halaman CMS dengan kerangka buatan build.py (dist/_templates/shell-<bagian>.html):
// header, menu, CSS inline, footer, dan tombol WA identik dengan halaman statis.
import { config, CACHE_DETIK } from './lakukan.js';
import { esc } from './halaman.js';

function jsonld(cfg, page) {
  const base = cfg.site_url || '';
  const url = base + page.slug;
  const graph = [
    { '@type': 'Organization', '@id': `${base}/#org`, name: cfg.brand, slogan: cfg.tagline, ...(base ? { url: base + '/' } : {}) },
    { '@type': 'WebPage', name: page.title, description: page.meta, inLanguage: 'id-ID', ...(base ? { url } : {}), publisher: { '@id': `${base}/#org` } },
    { '@type': 'BreadcrumbList', itemListElement: [[cfg.brand, '/'], ...page.crumbs].map(([n, u], i) => (
      { '@type': 'ListItem', position: i + 1, name: n, ...(base ? { item: base + u } : {}) })) },
  ];
  if (page.artikel) {
    const a = page.artikel;
    graph.push({ '@type': a.tipe || 'Article', headline: page.h1, description: page.meta, inLanguage: 'id-ID',
      datePublished: a.published, dateModified: a.updated, author: { '@type': 'Organization', name: a.author },
      publisher: { '@id': `${base}/#org` }, ...(a.image ? { image: a.image } : {}), ...(base ? { mainEntityOfPage: url } : {}) });
  }
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }).replace(/</g, '\\u003c');
}

async function isi(ctx, bagian, r) {
  const cfg = await config(ctx);
  const tpl = await (await ctx.env.ASSETS.fetch(new URL(`/_templates/shell-${bagian}.html`, ctx.request.url))).text();
  const p = r.page;
  const ganti = {
    '%%TITLE%%': esc(p.title), '%%META%%': esc(p.meta), '%%PATH%%': p.slug, '%%ROBOTS%%': r.index ? 'index,follow' : 'noindex,follow',
    '%%EYEBROW%%': esc(p.eyebrow), '%%H1%%': esc(p.h1), '%%JSONLD%%': jsonld(cfg, p),
  };
  let html = tpl.replace(/<h1>%%H1%%<\/h1>/, p.h1.length > 55 ? '<h1 class="long">%%H1%%</h1>' : '$&');
  html = p.lead ? html.replace('%%LEAD%%', p.lead) : html.replace(/<p class="lead">%%LEAD%%<\/p>\n?/, '');
  html = html.replace(/%%(TITLE|META|PATH|ROBOTS|EYEBROW|H1|JSONLD)%%/g, (m) => ganti[m]);
  return html.replace('%%BODY%%', () => r.body);
}

async function notFound(ctx) {
  const res = await ctx.env.ASSETS.fetch(new URL('/404', ctx.request.url));
  return new Response(await res.text(), { status: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}

/** Handler bersama /blog & /panduan: URL tanpa garis miring akhir, cache edge, 404 dari 404.html. */
export async function tangani(ctx, bagian, fn) {
  const url = new URL(ctx.request.url);
  if (url.pathname.length > 1 && url.pathname.endsWith('/')) {
    url.pathname = url.pathname.replace(/\/+$/, '');
    return Response.redirect(url.toString(), 301);
  }
  const cfg = await config(ctx);
  // kunci cache memuat id build: setiap deploy baru otomatis memakai kerangka (CSS/menu) terbaru
  const key = new Request(`${url.origin}${url.pathname}?b=${cfg.build}`);
  const hit = await caches.default.match(key);
  if (hit) return hit;
  const segs = (ctx.params.path || []).filter(Boolean);
  let r;
  try {
    r = await fn(ctx, segs);
  } catch (e) {
    return new Response('Konten sedang tidak bisa dimuat. Coba beberapa saat lagi.', { status: 503, headers: { 'Retry-After': '60' } });
  }
  if (r && r.redirect) return Response.redirect(url.origin + r.redirect, 301);
  if (!r) return notFound(ctx);
  const res = new Response(await isi(ctx, bagian, r), {
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': `public, max-age=0, s-maxage=${CACHE_DETIK}` },
  });
  ctx.waitUntil(caches.default.put(key, res.clone()));
  return res;
}
