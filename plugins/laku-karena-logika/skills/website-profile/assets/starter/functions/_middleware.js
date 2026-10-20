// Kolom footer "Blog" (5 artikel terbaru) dan "Panduan" di SEMUA halaman HTML selalu mengikuti CMS,
// tanpa build ulang. build.py menandai daftarnya dengan <ul data-blog-foot> / <ul data-panduan-foot>.
// Bila API gagal, daftar hasil build tetap tampil.
import { data, blogTerbaru, panduanFooter } from './_lib/lakukan.js';
import { esc } from './_lib/halaman.js';

const pendek = (t) => t.split(':')[0].trim();   // judul ringkas 1 baris (sama dengan judul_pendek di build.py)

export async function onRequest(ctx) {
  const res = await ctx.next();
  if (ctx.request.method !== 'GET' || !(res.headers.get('Content-Type') || '').includes('text/html')) return res;
  let d;
  try { d = await data(ctx); } catch (e) { return res; }
  const blog = blogTerbaru(d).map((x) => `<li><a href="${x.url}" title="${esc(x.judul)}">${esc(pendek(x.judul))}</a></li>`).join('')
    + '<li><a href="/blog">Semua artikel <span aria-hidden="true">→</span></a></li>';
  const pd = panduanFooter(d).map((x) => `<li><a href="${x.url}">${esc(x.nama)}</a></li>`).join('')
    + '<li><a href="/panduan">Semua panduan <span aria-hidden="true">→</span></a></li>';
  return new HTMLRewriter()
    .on('ul[data-blog-foot]', { element(e) { e.setInnerContent(blog, { html: true }); } })
    .on('ul[data-panduan-foot]', { element(e) { e.setInnerContent(pd, { html: true }); } })
    .transform(res);
}
