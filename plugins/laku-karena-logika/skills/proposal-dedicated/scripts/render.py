import sys,pathlib,base64
from playwright.sync_api import sync_playwright
src=pathlib.Path(sys.argv[1]).resolve();out=sys.argv[2];no=sys.argv[3];pre=sys.argv[4] if len(sys.argv)>4 else 'Penawaran Layanan Dedicated Team'
b64=base64.b64encode(open(src.parent/'paraf.png','rb').read()).decode()
foot=f'''<div style="font-family:sans-serif;font-size:7.5px;color:#6b7072;width:100%;padding:0 12mm;display:flex;justify-content:space-between;align-items:flex-end">
<span>{pre} · {no}</span>
<span style="display:flex;align-items:flex-end;gap:4px">Paraf Venturo: <img src="data:image/png;base64,{b64}" style="height:9mm;margin-bottom:-1mm"> &nbsp;&nbsp; Paraf Klien: <span style="display:inline-block;width:14mm;border-bottom:1px solid #9aa5a8"></span></span>
<span>Halaman <span class="pageNumber"></span> dari <span class="totalPages"></span></span></div>'''
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto(src.as_uri());pg.wait_for_timeout(500)
    pg.pdf(path=out,format='A4',print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template='<span></span>',footer_template=foot)
    b.close()
