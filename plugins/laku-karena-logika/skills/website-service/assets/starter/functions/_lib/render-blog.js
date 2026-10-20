// /blog pages, built on the same shell and helpers as /portfolio.
import { esc, dateId, cleanHtml } from './render.js';
import { primaryCategory } from './cms.js';

const SITE = 'https://venturo.id';
const ICON = '/assets/img/icons.svg#';
const ico = (n) => `<svg><use href="${ICON}${n}"/></svg>`;
const ORG = { '@type': 'Organization', '@id': SITE + '/#organization', name: 'Venturo', url: SITE + '/', logo: SITE + '/assets/img/logo-venturo.png' };
const minutes = (html) => Math.max(1, Math.round(String(html || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length / 200));

function card(a) {
  const img = a.cover_url
    ? `<img src="${esc(a.cover_url)}" alt="${esc(a.title)}" width="1200" height="675" loading="lazy" decoding="async">`
    : `<div class="pf-card__ph">${ico('i-book')}</div>`;
  return `<article class="pf-card reveal">
          <a href="/blog/${esc(a.slug)}/" class="pf-card__link">
            <div class="pf-card__img">${img}</div>
            <div class="pf-card__body">
              <time datetime="${esc(a.published_at)}">${primaryCategory(a) ? esc(primaryCategory(a).name) + ' · ' : ''}${esc(dateId(a.published_at))}</time>
              <h2>${esc(a.title)}</h2>
              <p>${esc(a.excerpt)}</p>
              <span class="pf-card__more">Baca artikel ${ico('i-arrow')}</span>
            </div>
          </a>
        </article>`;
}

export function blogListMain(items, cats, active, page, pages) {
  const chips = [`<a href="/blog/"${!active ? ' aria-current="page"' : ''}>Semua</a>`]
    .concat(cats.map((c) => `<a href="/blog/?kategori=${esc(c.slug)}"${active === c.slug ? ' aria-current="page"' : ''}>${esc(c.name)}</a>`))
    .join('');
  const qs = (n) => {
    const p = new URLSearchParams();
    if (active) p.set('kategori', active);
    if (n > 1) p.set('page', n);
    const s = p.toString();
    return '/blog/' + (s ? '?' + s : '');
  };
  const pager = pages > 1
    ? `<nav class="pf-pager" aria-label="Halaman blog">${Array.from({ length: pages }, (_, i) => i + 1)
        .map((n) => (n === page ? `<span aria-current="page">${n}</span>` : `<a href="${qs(n)}">${n}</a>`)).join('')}</nav>`
    : '';
  const grid = items.length
    ? `<div class="pf-grid">\n        ${items.map(card).join('\n        ')}\n      </div>`
    : `<div class="pf-empty reveal"><div class="ico">${ico('i-book')}</div><h2>Belum ada artikel</h2><p>Artikel baru segera hadir.</p></div>`;
  return `  <section class="hero pf-hero">
    <div class="container">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">›</span><span>Blog</span></nav>
      <span class="eyebrow">Blog Venturo</span>
      <h1>Insight <span class="hl">Software, AI &amp; Teknologi</span> untuk Bisnis</h1>
      <p class="hero__lead">Panduan praktis seputar pembuatan aplikasi, memilih software house, AI, cloud, dan keamanan sistem, ditulis oleh tim engineer Venturo.</p>
      <nav class="chips-nav" aria-label="Kategori blog">${chips}</nav>
    </div>
  </section>

  <section class="section" id="artikel">
    <div class="container">
      ${grid}
      ${pager}
    </div>
  </section>`;
}

export function blogListLd(items, page) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'Blog', name: 'Blog Venturo', url: SITE + '/blog/', publisher: ORG, inLanguage: 'id-ID',
        blogPost: items.map((a) => ({ '@type': 'BlogPosting', headline: a.title, url: `${SITE}/blog/${a.slug}/`, datePublished: a.published_at })) },
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Beranda', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: 'Blog', item: SITE + '/blog/' }] },
    ],
  };
}

export function blogDetailMain(a, related) {
  const cover = a.cover_url
    ? `<figure class="pf-cover"><img src="${esc(a.cover_url)}" alt="${esc(a.title)}" width="1200" height="675" fetchpriority="high"></figure>` : '';
  const rel = related.length
    ? `  <section class="section section--canvas">
    <div class="container">
      <div class="section-head reveal" style="margin-bottom:36px"><span class="eyebrow">Baca juga</span><h2>Artikel <span class="hl">Lainnya</span></h2></div>
      <div class="pf-grid">
        ${related.map(card).join('\n        ')}
      </div>
    </div>
  </section>` : '';
  return `  <article class="pf-article">
    <header class="pf-head">
      <div class="container pf-narrow">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">›</span><a href="/blog/">Blog</a><span aria-hidden="true">›</span><span>${esc(a.title)}</span></nav>
        ${primaryCategory(a) ? `<a class="eyebrow" href="/blog/?kategori=${esc(primaryCategory(a).slug)}">${esc(primaryCategory(a).name)}</a>` : ''}
        <h1>${esc(a.title)}</h1>
        ${a.excerpt ? `<p class="pf-lead">${esc(a.excerpt)}</p>` : ''}
        <p class="pf-meta"><time datetime="${esc(a.published_at)}">${esc(dateId(a.published_at))}</time> · ${minutes(a.content)} menit baca · ${esc(a.author || 'Tim Venturo')}</p>
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
            <h2>Butuh bantuan tim IT?</h2>
            <p>Diskusikan kebutuhan aplikasi Anda dengan software house Venturo. Konsultasi gratis.</p>
            <a class="btn btn--wa" href="https://wa.me/6285128043814" data-wa="general" data-cta="blog-aside">${ico('i-wa')} Konsultasi Gratis</a>
            <ul>
              <li><a href="/jasa-pembuatan-aplikasi/">Jasa pembuatan aplikasi →</a></li>
              <li><a href="/outsourcing-programmer/">Outsourcing programmer →</a></li>
              <li><a href="/jasa-maintenance-aplikasi/">Maintenance aplikasi →</a></li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </article>

${rel}`;
}

export function blogDetailLd(a) {
  const url = `${SITE}/blog/${a.slug}/`;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'BlogPosting', '@id': url + '#article', headline: a.title, description: a.excerpt || undefined,
        image: a.cover_url ? [a.cover_url] : undefined, datePublished: a.published_at, dateModified: a.updated_at || a.published_at,
        mainEntityOfPage: url, inLanguage: 'id-ID', articleSection: primaryCategory(a) ? primaryCategory(a).name : undefined,
        author: ORG, publisher: ORG },
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Beranda', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: 'Blog', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: a.title, item: url }] },
    ],
  };
}
