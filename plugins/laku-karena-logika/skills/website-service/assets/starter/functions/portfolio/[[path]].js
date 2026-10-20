// /portfolio/            → list of portfolio articles (CMS category "portfolio")
// /portfolio/ai/         → only articles in the "Portfolio AI" category
// /portfolio/<slug>/     → single case study
import { listPortfolio, getPortfolio, catSlugs } from '../_lib/cms.js';
import { page, cached, listMain, listJsonLd, detailMain, detailJsonLd, notFoundMain } from '../_lib/render.js';
import { addImageSizes } from '../_lib/image-size.js';

const PER_PAGE = 12;
const AI_CAT = 'portfolio-ai';
const isAi = (a) => catSlugs(a).includes(AI_CAT);

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const url = new URL(request.url);
  const parts = [].concat(params.path || []).filter(Boolean);

  // Canonical URLs always end with a slash
  if (!url.pathname.endsWith('/')) {
    url.pathname += '/';
    return Response.redirect(url.toString(), 301);
  }
  if (parts.length > 1) return notFound(env, request, url.pathname);

  return cached(context, async () => {
    try {
      if (parts.length === 0) return await renderList(env, request, url, false);
      if (parts[0] === 'ai') return await renderList(env, request, url, true);
      return await renderDetail(env, request, parts[0]);
    } catch (err) {
      console.error(err);
      return page(env, request, {
        title: 'Portfolio | Venturo', desc: 'Portfolio proyek Venturo.', path: '/portfolio/', status: 503, robots: 'noindex',
        jsonld: {}, main: notFoundMain().replace('tidak ditemukan', 'sedang dimuat ulang'),
      });
    }
  });
}

async function renderList(env, request, url, aiOnly) {
  const everything = await listPortfolio(env);
  const aiItems = everything.filter(isAi);
  const all = aiOnly ? aiItems : everything;
  const base = aiOnly ? '/portfolio/ai/' : '/portfolio/';
  const pages = Math.max(1, Math.ceil(all.length / PER_PAGE));
  const current = Math.min(pages, Math.max(1, parseInt(url.searchParams.get('page') || '1', 10) || 1));
  const items = all.slice((current - 1) * PER_PAGE, current * PER_PAGE);
  const suffix = current > 1 ? ` (Hal. ${current})` : '';
  const view = { aiOnly, base, counts: { all: everything.length, ai: aiItems.length }, isAi };
  return page(env, request, {
    title: aiOnly ? `Portfolio AI: Studi Kasus Proyek AI${suffix} | Venturo` : `Portfolio Proyek Software & AI${suffix} | Venturo`,
    desc: aiOnly
      ? 'Studi kasus proyek AI Venturo: machine learning, computer vision, AI agent WhatsApp, voice AI, dan chatbot untuk perusahaan dan instansi di Indonesia.'
      : 'Portfolio dan studi kasus proyek software house Venturo: aplikasi web, mobile, ERP, dan AI untuk perusahaan dan instansi di Indonesia.',
    path: base + (current > 1 ? `?page=${current}` : ''),
    jsonld: listJsonLd(items, current, view),
    main: listMain(items, current, pages, view),
  });
}

async function renderDetail(env, request, slug) {
  const found = await getPortfolio(env, slug);
  if (!found) return notFound(env, request, `/portfolio/${slug}/`);
  const article = { ...found, content: await addImageSizes(found.content) };
  const related = (await listPortfolio(env)).filter((a) => a.slug !== slug).slice(0, 3);
  return page(env, request, {
    title: article.title.length > 45 ? article.title : `${article.title} | Portfolio Venturo`,
    desc: article.excerpt || `Studi kasus proyek ${article.title} oleh Venturo.`,
    path: `/portfolio/${article.slug}/`,
    ogImage: article.cover_url,
    jsonld: detailJsonLd(article),
    main: detailMain(article, related),
  });
}

function notFound(env, request, path) {
  return page(env, request, {
    title: 'Portfolio tidak ditemukan | Venturo', desc: 'Halaman portfolio tidak ditemukan.', path, status: 404, robots: 'noindex',
    jsonld: {}, main: notFoundMain(),
  });
}
