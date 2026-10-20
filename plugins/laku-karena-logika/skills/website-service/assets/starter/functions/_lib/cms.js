// Lakukan CMS client (public API, no API key).
// Fetched on the server because the API rejects direct browser (cross-origin) requests.

const API = 'https://api.lakukan.id/api';
export const CACHE_SECONDS = 600; // CMS changes appear on the site within 10 minutes

export function category(env) {
  return env.CMS_CATEGORY || 'portfolio';
}

async function get(env, path) {
  const res = await fetch(API + path, {
    headers: {
      'X-Company-Slug': env.CMS_COMPANY_SLUG || 'venturo-web',
      Accept: 'application/json',
      // Cloudflare in front of the API rejects default/empty user agents
      'User-Agent': 'VenturoWebsite/1.0 (+https://venturo.id)',
    },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`CMS ${res.status} on ${path}`);
  return (await res.json()).data;
}

/** Category slugs of an article. The API returns `categories` (array); older responses used `category`. */
export function catSlugs(a) {
  const list = Array.isArray(a && a.categories) ? a.categories : a && a.category ? [a.category] : [];
  return list.map((c) => (typeof c === 'string' ? c : c && c.slug)).filter(Boolean);
}

/** First category object (for labels), normalised to {slug, name}. */
export function primaryCategory(a) {
  const list = Array.isArray(a && a.categories) ? a.categories : a && a.category ? [a.category] : [];
  const c = list[0];
  if (!c) return null;
  return typeof c === 'string' ? { slug: c, name: c } : { slug: c.slug, name: c.name || c.slug };
}

// "portfolio" plus its variants such as "portfolio-ai" all count as portfolio.
const inPortfolio = (a, cat) => catSlugs(a).some((s) => s === cat || s.startsWith(cat + '-'));
const isLive = (a, cat) => a && a.status === 'published' && inPortfolio(a, cat);

/** Published articles in the portfolio category, newest first. */
export async function listPortfolio(env) {
  const cat = category(env);
  const bySlug = new Map();
  // "Portfolio" and "Portfolio AI" are separate CMS categories; fetch both and merge.
  for (const c of [cat, `${cat}-ai`]) {
    for (let page = 1; page <= 10; page++) {
      const data = await get(env, `/articles?category=${encodeURIComponent(c)}&limit=100&page=${page}`);
      if (!data || !data.length) break;
      for (const a of data) bySlug.set(a.slug, a);
      if (data.length < 100) break;
    }
  }
  return [...bySlug.values()]
    .filter((a) => isLive(a, cat))
    .sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
}

/** One published portfolio article, or null. */
export async function getPortfolio(env, slug) {
  if (!/^[a-z0-9-]{1,180}$/.test(slug)) return null;
  const a = await get(env, `/articles/${slug}`);
  return isLive(a, category(env)) ? a : null;
}

// ---------------------------------------------------------------- blog
// Every published article that is NOT in the portfolio category.

// Blog = published, has at least one category, and is not in the portfolio category.
// Articles without any category are treated as unfinished and are not shown.
const isBlog = (a, portfolioCat) => {
  if (!a || a.status !== 'published') return false;
  const cats = catSlugs(a);
  return cats.length > 0 && !inPortfolio(a, portfolioCat);
};

export async function listCategories(env) {
  const data = await get(env, '/article-categories');
  return (data || []).filter((c) => c.slug !== category(env));
}

export async function listBlog(env, cat) {
  const items = [];
  const q = cat ? `category=${encodeURIComponent(cat)}&` : '';
  for (let page = 1; page <= 10; page++) {
    const data = await get(env, `/articles?${q}limit=100&page=${page}`);
    if (!data || !data.length) break;
    items.push(...data);
    if (data.length < 100) break;
  }
  return items
    .filter((a) => isBlog(a, category(env)))
    .sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
}

export async function getBlog(env, slug) {
  if (!/^[a-z0-9-]{1,180}$/.test(slug)) return null;
  const a = await get(env, `/articles/${slug}`);
  return isBlog(a, category(env)) ? a : null;
}
