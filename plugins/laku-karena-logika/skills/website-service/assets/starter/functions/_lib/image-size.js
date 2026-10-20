// Reads the pixel size of remote images from their first bytes (PNG, JPEG, GIF, WebP) so CMS
// content images get width/height attributes. That lets the browser reserve their space and
// avoids layout shift (CLS) while they load. Results are part of the cached page HTML.

const RANGE = 'bytes=0-131071';
const TIMEOUT_MS = 2500;
const MAX_IMAGES = 24;

function u16be(b, i) { return (b[i] << 8) | b[i + 1]; }
function u32be(b, i) { return ((b[i] << 24) >>> 0) + (b[i + 1] << 16) + (b[i + 2] << 8) + b[i + 3]; }

export function parseSize(b) {
  if (b.length < 30) return null;
  // PNG
  if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return { w: u32be(b, 16), h: u32be(b, 20) };
  // GIF
  if (b[0] === 0x47 && b[1] === 0x49 && b[2] === 0x46) return { w: b[6] | (b[7] << 8), h: b[8] | (b[9] << 8) };
  // WebP
  if (b[0] === 0x52 && b[1] === 0x49 && b[2] === 0x46 && b[3] === 0x46 && b[8] === 0x57 && b[9] === 0x45 && b[10] === 0x42 && b[11] === 0x50) {
    const chunk = String.fromCharCode(b[12], b[13], b[14], b[15]);
    if (chunk === 'VP8 ') return { w: (b[26] | (b[27] << 8)) & 0x3fff, h: (b[28] | (b[29] << 8)) & 0x3fff };
    if (chunk === 'VP8L') return { w: 1 + (((b[22] & 0x3f) << 8) | b[21]), h: 1 + (((b[24] & 0x0f) << 10) | (b[23] << 2) | ((b[22] & 0xc0) >> 6)) };
    if (chunk === 'VP8X') return { w: 1 + (b[24] | (b[25] << 8) | (b[26] << 16)), h: 1 + (b[27] | (b[28] << 8) | (b[29] << 16)) };
    return null;
  }
  // JPEG: walk the markers until a start-of-frame (SOFn) segment
  if (b[0] === 0xff && b[1] === 0xd8) {
    let i = 2;
    while (i + 9 < b.length) {
      if (b[i] !== 0xff) { i++; continue; }
      const m = b[i + 1];
      if (m === 0xff) { i++; continue; }
      if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return { w: u16be(b, i + 7), h: u16be(b, i + 5) };
      if (m === 0xd8 || (m >= 0xd0 && m <= 0xd7)) { i += 2; continue; }
      i += 2 + u16be(b, i + 2);
    }
  }
  return null;
}

async function probe(src) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(src, { headers: { Range: RANGE }, signal: ctrl.signal, cf: { cacheTtl: 86400 } });
    if (!res.ok) return null;
    const buf = new Uint8Array(await res.arrayBuffer());
    const size = parseSize(buf);
    return size && size.w > 0 && size.h > 0 ? size : null;
  } catch (e) {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

/** Add width/height to <img> tags (absolute http(s) src only) that do not have them yet. */
export async function addImageSizes(html) {
  const tags = [...String(html || '').matchAll(/<img\b[^>]*>/gi)].map((m) => m[0]).filter((t) => !/\swidth=/i.test(t));
  const srcs = [...new Set(tags.map((t) => (t.match(/\ssrc=["'](https?:\/\/[^"']+)["']/i) || [])[1]).filter(Boolean))].slice(0, MAX_IMAGES);
  if (!srcs.length) return html;
  const sizes = new Map(await Promise.all(srcs.map(async (s) => [s, await probe(s)])));
  return String(html).replace(/<img\b[^>]*>/gi, (tag) => {
    if (/\swidth=/i.test(tag)) return tag;
    const src = (tag.match(/\ssrc=["'](https?:\/\/[^"']+)["']/i) || [])[1];
    const size = src && sizes.get(src);
    return size ? tag.replace(/^<img/i, `<img width="${size.w}" height="${size.h}"`) : tag;
  });
}
