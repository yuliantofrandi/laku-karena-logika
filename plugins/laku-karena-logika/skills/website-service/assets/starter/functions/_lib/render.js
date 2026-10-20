// HTML rendering for /portfolio pages. The page shell (head, header, footer) comes from
// website/_templates/portfolio.html so it stays identical to the static pages.

import { CACHE_SECONDS, catSlugs } from './cms.js';

const SITE = 'https://venturo.id';
// Keep in sync with the ?v= asset version: a new deploy then never serves cached HTML that
// still points at the previous stylesheet/script.
const ASSET_VERSION = 'v=20261021u';
const DEFAULT_OG = SITE + '/assets/img/og-image.jpg';
const ICON = '/assets/img/icons.svg#';
const MONTHS = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];

export const esc = (s) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export const dateId = (iso) => {
  const d = new Date(iso);
  return isNaN(d) ? '' : `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
};

const ico = (name) => `<svg><use href="${ICON}${name}"/></svg>`;

/** Defensive clean-up of CMS HTML: drop scripts, inline handlers and javascript: URLs. */
export function cleanHtml(html) {
  return String(html || '')
    .replace(/<(script|style|iframe|object|embed)[\s\S]*?<\/\1>/gi, '')
    .replace(/\son\w+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '')
    .replace(/(href|src)\s*=\s*(["'])\s*javascript:[^"']*\2/gi, '$1="#"')
    .replace(/<img(?![^>]*\bloading=)/gi, '<img loading="lazy" decoding="async"');
}

/** Plain-text word count for reading time. */
const readMinutes = (html) => Math.max(1, Math.round(String(html || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length / 200));

async function shell(env, request) {
  const res = await env.ASSETS.fetch(new URL('/_templates/portfolio.html', request.url));
  return res.text();
}

export async function page(env, request, { title, desc, path, ogImage, jsonld, main, status = 200, robots }) {
  const html = (await shell(env, request))
    .replaceAll('{{TITLE}}', esc(title))
    .replaceAll('{{DESC}}', esc(desc))
    .replaceAll('{{PATH}}', esc(path))
    .replaceAll('{{OG_IMAGE}}', esc(ogImage || DEFAULT_OG))
    .replaceAll('{{ROBOTS}}', robots || 'index, follow, max-image-preview:large')
    .replace('{{JSONLD}}', JSON.stringify(jsonld, null, 2).replace(/</g, '\\u003c'))
    .replace('{{MAIN}}', main);
  return new Response(html, {
    status,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': status === 200 ? `public, max-age=60, s-maxage=${CACHE_SECONDS}` : 'no-store',
    },
  });
}

/** Serve from the edge cache when possible (cuts TTFB and CMS load). */
export async function cached(context, render) {
  const cache = caches.default;
  const url = new URL(context.request.url);
  url.searchParams.set('__asset', ASSET_VERSION);
  const key = new Request(url.toString(), { method: 'GET' });
  const hit = await cache.match(key);
  if (hit) return hit;
  const res = await render();
  if (res.status === 200) context.waitUntil(cache.put(key, res.clone()));
  return res;
}

const breadcrumbLd = (items) => ({
  '@type': 'BreadcrumbList',
  itemListElement: items.map(([name, url], i) => ({ '@type': 'ListItem', position: i + 1, name, item: SITE + url })),
});

const ORG = { '@type': 'Organization', '@id': SITE + '/#organization', name: 'Venturo', url: SITE + '/', logo: SITE + '/assets/img/logo-venturo.png' };

function card(a, ai = false) {
  const img = a.cover_url
    ? `<img src="${esc(a.cover_url)}" alt="${esc(a.title)}" width="1200" height="675" loading="lazy" decoding="async">`
    : `<div class="pf-card__ph">${ico('i-code')}</div>`;
  return `<article class="pf-card reveal">
          <a href="/portfolio/${esc(a.slug)}/" class="pf-card__link">
            <div class="pf-card__img">${img}${ai ? '<span class="pf-card__badge">AI</span>' : ''}</div>
            <div class="pf-card__body">
              <time datetime="${esc(a.published_at)}">${esc(dateId(a.published_at))}</time>
              <h2>${esc(a.title)}</h2>
              <p>${esc(a.excerpt)}</p>
              <span class="pf-card__more">Lihat studi kasus ${ico('i-arrow')}</span>
            </div>
          </a>
        </article>`;
}

const ctaBand = (text) => `  <section class="section section--tight pf-cta">
    <div class="container pf-cta__inner reveal">
      <div>
        <h2>Punya Proyek Serupa?</h2>
        <p>${text}</p>
      </div>
      <a class="btn btn--white btn--lg" href="https://wa.me/6285128043814" data-wa="general" data-cta="portfolio-cta">
        <svg style="color:var(--wa)"><use href="${ICON}i-wa"/></svg> Konsultasi Gratis
      </a>
    </div>
  </section>`;

export function listMain(items, page, pages, view = { aiOnly: false, base: '/portfolio/', counts: null, isAi: () => false }) {
  const { aiOnly, base, counts, isAi } = view;
  const grid = items.length
    ? `<div class="pf-grid">\n        ${items.map((a) => card(a, !aiOnly && isAi(a))).join('\n        ')}\n      </div>`
    : `<div class="pf-empty reveal">
        <div class="ico">${ico('i-board')}</div>
        <h2>Studi kasus sedang kami siapkan</h2>
        <p>Sambil menunggu, kami bisa menceritakan proyek yang relevan dengan kebutuhan Anda secara langsung.</p>
        <a class="btn btn--wa" href="https://wa.me/6285128043814" data-wa="general" data-cta="portfolio-empty">${ico('i-wa')} Minta Contoh Proyek</a>
      </div>`;
  const nav = pages > 1
    ? `<nav class="pf-pager" aria-label="Halaman portfolio">${Array.from({ length: pages }, (_, i) => i + 1)
        .map((n) => (n === page ? `<span aria-current="page">${n}</span>` : `<a href="${base}${n > 1 ? `?page=${n}` : ''}">${n}</a>`))
        .join('')}</nav>`
    : '';
  return `  <section class="hero pf-hero">
    <div class="container">
      ${aiOnly
        ? `<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">›</span><a href="/portfolio/">Portfolio</a><span aria-hidden="true">›</span><span>Portfolio AI</span></nav>
      <span class="eyebrow">Portfolio AI</span>
      <h1>Studi Kasus <span class="hl">Proyek AI</span> Venturo</h1>
      <p class="hero__lead">Solusi AI yang sudah berjalan di perusahaan klien: machine learning, computer vision, AI agent WhatsApp, voice AI, dan chatbot, lengkap dengan tantangan, solusi, dan hasilnya.</p>`
        : `<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">›</span><span>Portfolio</span></nav>
      <span class="eyebrow">Portfolio &amp; studi kasus</span>
      <h1>Portfolio Proyek <span class="hl">Software &amp; AI</span> Venturo</h1>
      <p class="hero__lead">Kumpulan proyek yang telah kami selesaikan untuk perusahaan dan instansi di Indonesia, lengkap dengan tantangan, solusi, dan keunggulan setiap proyek.</p>`}
      <div class="stats stats--3" role="list">
        <div class="stat" role="listitem"><b>200+</b><span>Proyek berhasil di-deliver</span></div>
        <div class="stat" role="listitem"><b>100+</b><span>In-house engineer</span></div>
        <div class="stat" role="listitem"><b>2013</b><span>Berdiri, 13+ tahun pengalaman</span></div>
      </div>
    </div>
  </section>

  <section class="section" id="daftar-portfolio">
    <div class="container">
      ${counts && counts.ai ? `<nav class="chips-nav pf-filter" aria-label="Filter portfolio"><a href="/portfolio/"${!aiOnly ? ' aria-current="page"' : ''}>Semua Proyek <span>${counts.all}</span></a><a href="/portfolio/ai/"${aiOnly ? ' aria-current="page"' : ''}>${ico('i-ai')} Portfolio AI <span>${counts.ai}</span></a></nav>` : ''}
      ${grid}
      ${nav}
    </div>
  </section>

${ctaBand('Ceritakan kebutuhan Anda. Kami tunjukkan pengalaman yang paling relevan dan cara kami mengerjakannya, lalu jelaskan detailnya saat meeting online maupun offline.')}`;
}

export function listJsonLd(items, page, view = { aiOnly: false, base: '/portfolio/' }) {
  const { aiOnly, base } = view;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'CollectionPage',
        name: aiOnly ? 'Portfolio AI: Studi Kasus Proyek AI Venturo' : 'Portfolio Proyek Software & AI Venturo',
        url: SITE + base + (page > 1 ? `?page=${page}` : ''),
        isPartOf: { '@id': SITE + '/#website' },
        publisher: ORG,
        mainEntity: {
          '@type': 'ItemList',
          itemListElement: items.map((a, i) => ({ '@type': 'ListItem', position: i + 1, url: `${SITE}/portfolio/${a.slug}/`, name: a.title })),
        },
      },
      breadcrumbLd(aiOnly ? [['Beranda', '/'], ['Portfolio', '/portfolio/'], ['Portfolio AI', '/portfolio/ai/']] : [['Beranda', '/'], ['Portfolio', '/portfolio/']]),
    ],
  };
}

export function detailMain(a, related) {
  const waText = `Halo Venturo, saya tertarik dengan proyek "${a.title}" dan ingin membuat solusi serupa.`;
  const cover = a.cover_url
    ? `<figure class="pf-cover"><img src="${esc(a.cover_url)}" alt="${esc(a.title)}" width="1200" height="675" fetchpriority="high"></figure>`
    : '';
  const rel = related.length
    ? `  <section class="section section--canvas">
    <div class="container">
      <div class="section-head reveal" style="margin-bottom:36px"><span class="eyebrow">Portfolio lainnya</span><h2>Proyek <span class="hl">Lainnya</span></h2></div>
      <div class="pf-grid">
        ${related.map((a) => card(a, catSlugs(a).includes('portfolio-ai'))).join('\n        ')}
      </div>
    </div>
  </section>`
    : '';
  return `  <article class="pf-article">
    <header class="pf-head">
      <div class="container pf-narrow">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">›</span><a href="/portfolio/">Portfolio</a><span aria-hidden="true">›</span><span>${esc(a.title)}</span></nav>
        <span class="eyebrow">Studi kasus</span>
        <h1>${esc(a.title)}</h1>
        ${a.excerpt ? `<p class="pf-lead">${esc(a.excerpt)}</p>` : ''}
        <p class="pf-meta"><time datetime="${esc(a.published_at)}">${esc(dateId(a.published_at))}</time> · ${readMinutes(a.content)} menit baca · Venturo</p>
      </div>
    </header>
    <div class="container pf-narrow">
      ${cover}
      <div class="pf-layout">
        <div class="prose">
${cleanHtml(a.content)}
        </div>
        <aside class="pf-aside">
          <div class="pf-aside__card">
            <h2>Butuh solusi serupa?</h2>
            <p>Diskusikan kebutuhan Anda dengan tim kami. Konsultasi gratis, tanpa komitmen.</p>
            <a class="btn btn--wa" href="https://wa.me/6285128043814" data-wa="general" data-wa-text="${esc(waText)}" data-cta="portfolio-aside">${ico('i-wa')} Konsultasi Gratis</a>
            <ul>
              <li><span class="check">${ico('i-check')}</span>Garansi bug 30 hari</li>
              <li><span class="check">${ico('i-check')}</span>Free Proof of Concept</li>
              <li><span class="check">${ico('i-check')}</span>100+ in-house engineer</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </article>

${rel}

${ctaBand('Kami bisa membangun solusi serupa, disesuaikan dengan proses dan kebutuhan bisnis Anda.')}`;
}

export function detailJsonLd(a) {
  const url = `${SITE}/portfolio/${a.slug}/`;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        '@id': url + '#article',
        headline: a.title,
        description: a.excerpt || undefined,
        image: a.cover_url ? [a.cover_url] : undefined,
        datePublished: a.published_at,
        dateModified: a.updated_at || a.published_at,
        mainEntityOfPage: url,
        inLanguage: 'id-ID',
        articleSection: 'Portfolio',
        author: ORG,
        publisher: ORG,
      },
      breadcrumbLd([['Beranda', '/'], ['Portfolio', '/portfolio/'], [a.title, `/portfolio/${a.slug}/`]]),
    ],
  };
}

export function notFoundMain() {
  return `  <section class="hero pf-hero">
    <div class="container">
      <span class="eyebrow">404</span>
      <h1>Portfolio <span class="hl">tidak ditemukan</span></h1>
      <p class="hero__lead">Studi kasus yang Anda cari mungkin sudah dipindahkan atau belum dipublikasikan.</p>
      <div class="hero__ctas"><a class="btn btn--primary" href="/portfolio/">Lihat semua portfolio ${ico('i-arrow')}</a></div>
    </div>
  </section>`;
}
