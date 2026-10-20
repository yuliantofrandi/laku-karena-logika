// sitemap.xml = halaman statis dari build (dist/_templates/sitemap-statis.txt) + semua halaman Blog & Panduan dari API.
import { config, data, katSlug, katSlugs, draf, slugKat } from './_lib/lakukan.js';

export async function onRequestGet(ctx) {
  const cfg = await config(ctx);
  const statis = (await (await ctx.env.ASSETS.fetch(new URL('/_templates/sitemap-statis.txt', ctx.request.url))).text())
    .split('\n').filter(Boolean);
  const urls = [...statis];
  try {
    const d = await data(ctx);
    const blogSet = new Set(d.blogKat.map((k) => k.slug));
    const blog = d.artikel.filter((a) => blogSet.has(katSlug(a)) && !draf(a));
    if (blog.length) {
      urls.push('/blog');
      for (const k of d.blogKat.slice(1)) if (blog.some((a) => katSlug(a) === k.slug)) urls.push(`/blog/kategori/${slugKat(k, cfg)}`);
      for (const a of blog) if (!(cfg.noindex || []).includes(`/blog/${a.slug}`)) urls.push(`/blog/${a.slug}`);
    }
    if (cfg.panduan) {
      const kats = d.kategori.filter((k) => d.artikel.some((a) => katSlug(a) === k.slug));
      if (kats.length) urls.push('/panduan');
      for (const k of kats) {
        urls.push(`/panduan/${slugKat(k, cfg)}`);
        for (const a of d.artikel) if (katSlug(a) === k.slug) urls.push(`/panduan/${slugKat(k, cfg)}/${a.slug}`);
      }
    }
    if (cfg.portfolio) {
      const cat = cfg.kategori_portfolio || 'portfolio';
      const pf = d.artikel.filter((a) => katSlugs(a).some((s) => s === cat || s.startsWith(cat + '-')) && !draf(a));
      if (pf.length) urls.push('/portfolio');
      if (pf.some((a) => katSlugs(a).includes(`${cat}-ai`))) urls.push('/portfolio/ai');
      for (const a of pf) urls.push(`/portfolio/${a.slug}`);
    }
  } catch (e) { /* API gagal: tetap kirim halaman statis */ }
  const base = cfg.site_url || new URL(ctx.request.url).origin;
  const xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + [...new Set(urls)].map((u) => `<url><loc>${base}${u}</loc></url>`).join('') + '</urlset>';
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=600' } });
}
