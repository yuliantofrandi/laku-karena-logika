#!/usr/bin/env python3
"""Cari klaim yang diulang di elemen sorotan dalam SATU halaman.

Aturan: setiap klaim (angka besar, tahun berdiri, garansi, dll.) cukup tampil SEKALI per halaman
di elemen sorotan (hero, stat, kartu). Pengulangan di FAQ / paragraf boleh, putuskan manual.

Pakai (dari folder dist/ hasil build):
  python3 dupe.py                         # semua */index.html + index.html
  python3 dupe.py jasa-x.html
Ubah PAT di bawah sesuai klaim perusahaan (contoh: klaim Venturo).
"""
import re, glob, sys
PAT = {
    '100+ engineer': r'100\+\s*(?:<[^>]+>\s*)*(?:in-house|engineer|programmer|talent)',
    '200+ proyek': r'200\+\s*(?:<[^>]+>\s*)*(?:proyek|project)',
    'sejak 2013': r'(?:sejak|berdiri|since)[^<]{0,12}2013|<b[^>]*>2013</b>|13\+\s*tahun',
    'garansi 30 hari': r'garansi[^<]{0,25}30\s*hari|30 hari setelah serah',
}
def ctx(s, i):
    m = None
    for m2 in re.finditer(r'class="([^"]+)"', s[max(0, i-1500):i]): m = m2
    return m.group(1).split()[0] if m else '?'
files = sys.argv[1:] or sorted(glob.glob('**/*.html', recursive=True))
for f in files:
    s = open(f).read()
    body = s[s.index('<main'):s.index('</main>')] if '<main' in s else s
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    out = []
    for k, p in PAT.items():
        hits = [(ctx(body, m.start()), re.sub(r'<[^>]+>', ' ', body[m.start():m.start()+60]).strip()[:40]) for m in re.finditer(p, body, re.I)]
        if len(hits) > 1: out.append(f'  {k} ×{len(hits)}: ' + ' | '.join(f'[{c}] {t}' for c, t in hits))
    if out: print(f); print('\n'.join(out))
