// /sitemap.xml = static pages (website/sitemap.xml) + portfolio & blog articles from the CMS.
import { listPortfolio, listBlog, CACHE_SECONDS } from './_lib/cms.js';
import { cached } from './_lib/render.js';

const entry = (path, a, priority) => {
  const lastmod = a ? (a.updated_at || a.published_at || '').slice(0, 10) : '';
  return `  <url><loc>https://venturo.id${path}</loc>${lastmod ? `<lastmod>${lastmod}</lastmod>` : ''}<priority>${priority}</priority></url>\n`;
};

export async function onRequestGet(context) {
  const { env, request } = context;
  return cached(context, async () => {
    const base = await (await env.ASSETS.fetch(new URL('/sitemap.xml', request.url))).text();
    let extra = entry('/portfolio/', null, 0.8) + entry('/portfolio/ai/', null, 0.8) + entry('/blog/', null, 0.7);
    try {
      for (const a of await listPortfolio(env)) extra += entry(`/portfolio/${a.slug}/`, a, 0.7);
      for (const a of await listBlog(env)) extra += entry(`/blog/${a.slug}/`, a, 0.6);
    } catch (err) {
      console.error(err); // keep serving the static part if the CMS is unreachable
    }
    return new Response(base.replace('</urlset>', extra + '</urlset>'), {
      headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': `public, max-age=300, s-maxage=${CACHE_SECONDS}` },
    });
  });
}
