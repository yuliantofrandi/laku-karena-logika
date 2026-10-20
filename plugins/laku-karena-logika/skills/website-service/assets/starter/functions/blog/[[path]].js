// /blog/                    → all published CMS articles except the portfolio category
// /blog/?kategori=<slug>    → filtered by category
// /blog/<slug>/             → single article
import { listBlog, getBlog, listCategories, primaryCategory } from '../_lib/cms.js';
import { page, cached, notFoundMain } from '../_lib/render.js';
import { blogListMain, blogListLd, blogDetailMain, blogDetailLd } from '../_lib/render-blog.js';
import { addImageSizes } from '../_lib/image-size.js';

const PER_PAGE = 12;

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const url = new URL(request.url);
  const parts = [].concat(params.path || []).filter(Boolean);
  if (!url.pathname.endsWith('/')) {
    url.pathname += '/';
    return Response.redirect(url.toString(), 301);
  }
  if (parts.length > 1) return notFound(env, request, url.pathname);

  return cached(context, async () => {
    try {
      return parts.length === 0 ? await list(env, request, url) : await detail(env, request, parts[0]);
    } catch (err) {
      console.error(err);
      return page(env, request, { title: 'Blog | Venturo', desc: 'Blog Venturo.', path: '/blog/', status: 503, robots: 'noindex', jsonld: {},
        main: notFoundMain().replace('Portfolio', 'Blog').replace('tidak ditemukan', 'sedang dimuat ulang') });
    }
  });
}

async function list(env, request, url) {
  const cats = await listCategories(env);
  const active = cats.some((c) => c.slug === url.searchParams.get('kategori')) ? url.searchParams.get('kategori') : '';
  const all = await listBlog(env, active);
  const pages = Math.max(1, Math.ceil(all.length / PER_PAGE));
  const current = Math.min(pages, Math.max(1, parseInt(url.searchParams.get('page') || '1', 10) || 1));
  const items = all.slice((current - 1) * PER_PAGE, current * PER_PAGE);
  const catName = active ? cats.find((c) => c.slug === active).name : '';
  return page(env, request, {
    title: catName ? `Artikel ${catName} | Blog Venturo` : 'Blog Software House: Aplikasi, AI &amp; Teknologi | Venturo'.replace('&amp;', '&'),
    desc: 'Artikel dan panduan seputar pembuatan aplikasi, memilih software house, AI, cloud, dan keamanan sistem dari tim engineer Venturo.',
    path: '/blog/' + (active ? `?kategori=${active}` : ''),
    // category/page variants point their canonical at themselves; only page 1 of "all" is the main listing
    jsonld: blogListLd(items, current),
    main: blogListMain(items, cats, active, current, pages),
  });
}

async function detail(env, request, slug) {
  const found = await getBlog(env, slug);
  if (!found) return notFound(env, request, `/blog/${slug}/`);
  const a = { ...found, content: await addImageSizes(found.content) };
  const related = (await listBlog(env, primaryCategory(a) ? primaryCategory(a).slug : '')).filter((x) => x.slug !== slug).slice(0, 3);
  return page(env, request, {
    title: a.title.length > 50 ? a.title : `${a.title} | Venturo`, desc: a.excerpt || a.title, path: `/blog/${a.slug}/`, ogImage: a.cover_url,
    jsonld: blogDetailLd(a), main: blogDetailMain(a, related),
  });
}

function notFound(env, request, path) {
  return page(env, request, { title: 'Artikel tidak ditemukan | Venturo', desc: 'Artikel tidak ditemukan.', path, status: 404, robots: 'noindex', jsonld: {},
    main: notFoundMain().replaceAll('Portfolio', 'Artikel').replace('/portfolio/', '/blog/').replace('Lihat semua portfolio', 'Lihat semua artikel') });
}
