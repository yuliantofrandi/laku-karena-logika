#!/usr/bin/env python3
"""Audit prapublish / pasca-publish website jasa.

Pakai:
  python3 audit.py https://domain.id                 # halaman diambil dari /sitemap.xml
  python3 audit.py http://localhost:8788 / /harga/   # daftar halaman manual
  python3 audit.py https://domain.id --extra /lama/ /file.pdf   # cek status URL tambahan

Mengecek: status 200, <title> <=65 karakter, meta description <=165, canonical, tepat 1 <h1>,
og:image, JSON-LD valid, <img> punya alt + width, judul ganda, link internal & gambar lokal rusak,
serta teks terlarang (harga "Rp"/"juta", lorem, TODO). Tambah pola terlarang lewat env FORBID (regex).
"""
import re, sys, os, json, html, urllib.request, urllib.error, concurrent.futures as cf

args = sys.argv[1:]
if not args: sys.exit(__doc__)
B = args.pop(0).rstrip('/')
extra = []
if '--extra' in args:
    i = args.index('--extra'); extra = args[i+1:]; args = args[:i]

def get(u, method='GET'):
    try:
        r = urllib.request.urlopen(urllib.request.Request(B+u, method=method, headers={'User-Agent': 'Mozilla/5.0 (site audit)'}), timeout=30)
        return r.status, (r.read().decode('utf-8', 'ignore') if method == 'GET' else '')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return str(e)[:40], ''

pages = args
if not pages:
    _, sm = get('/sitemap.xml')
    pages = [re.sub(r'^https?://[^/]+', '', u) or '/' for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
FORBID = r'(?i)Rp\s?\d|\b\d+[.,]?\d*\s?(juta|jt)\b|lorem|\bTODO\b|\bXXX\b' + ('|' + os.environ['FORBID'] if os.environ.get('FORBID') else '')

titles, links, imgs = {}, set(), set()
for p in pages:
    st, t = get(p); iss = []
    if st != 200: iss.append(f'status {st}')
    title = html.unescape((re.search(r'<title>(.*?)</title>', t, re.S) or [None, ''])[1]).strip()
    desc = html.unescape((re.search(r'<meta name="description" content="([^"]*)"', t) or [None, ''])[1])
    canon = (re.search(r'<link rel="canonical" href="([^"]*)"', t) or [None, ''])[1]
    h1 = len(re.findall(r'<h1[\s>]', t))
    if len(title) > 65: iss.append(f'title {len(title)}ch')
    if not desc: iss.append('no desc')
    elif len(desc) > 165: iss.append(f'desc {len(desc)}ch')
    if not canon: iss.append('no canonical')
    if h1 != 1: iss.append(f'h1={h1}')
    if 'og:image' not in t: iss.append('no og:image')
    titles.setdefault(title, []).append(p)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(b)
        except Exception: iss.append('BAD JSON-LD')
    for im in re.findall(r'<img\b[^>]*>', t):
        src = (re.search(r'src="([^"]*)"', im) or [None, ''])[1]; imgs.add(src)
        if 'alt=' not in im: iss.append('img no alt ' + src[-30:])
        if 'width=' not in im: iss.append('img no width ' + src[-30:])
    for h in re.findall(r'href="(/[^"#]*)', t): links.add(h)
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    flags = set(m.group(0) for m in re.finditer(FORBID, re.sub(r'<[^>]+>', ' ', body)))
    if flags: iss.append('TEXT: ' + ', '.join(flags))
    print(('OK   ' if not iss else 'WARN ') + p + ('' if not iss else '  → ' + ' | '.join(iss)))

print('\nJudul ganda:', [(k, v) for k, v in titles.items() if len(v) > 1] or 'tidak ada')
chk = lambda u: (u, get(u)[0])
with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(chk, sorted(links)))
print('Link internal:', len(res), 'rusak:', [r for r in res if r[1] != 200] or 'tidak ada')
loc = [i for i in imgs if i and i.startswith('/')]
with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(chk, loc))
print('Gambar lokal:', len(loc), 'rusak:', [r for r in res if r[1] != 200] or 'tidak ada')
for u in ['/robots.txt', '/sitemap.xml', '/llms.txt', '/favicon.ico', '/halaman-tidak-ada-xyz/'] + extra:
    print('  ', u, get(u)[0])
