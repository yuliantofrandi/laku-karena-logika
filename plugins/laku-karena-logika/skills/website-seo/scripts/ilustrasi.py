#!/usr/bin/env python3
"""Generator ilustrasi SVG placeholder (mockup UI & konsep) dari data/ilustrasi.json.

Setiap entri `"auto": true` dibuatkan SVG 800×500 bergaya design system (warna dari
site.json → ilustrasi_warna). Entri yang sudah diganti gambar asli user diberi
`"auto": false` + `"file": "static/ilustrasi/<id>.webp"` dan tidak disentuh generator.

Komponen (field "jenis"): timeline, bars, grouped, gallery, tasklist, table, chat, doc,
dialog, steps, cards, map, compare, venn, shield, brand, tiers, orang (orang bekerja + kartu UI). Hanya library standar.
"""
import html
from pathlib import Path

W, H = 800, 500
C = {"p": "#7B2CFF", "k": "#E83AAE", "o": "#FF8A00", "ink": "#1b1626", "mut": "#6f6880",
     "line": "#e9e5f0", "soft": "#f8f6fc", "tint": "#f3edff", "ok": "#13a35a", "idle": "#d9d3e6"}
FONT = "system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif"


def e(s):
    return html.escape(str(s), quote=True)


def t(x, y, s, size=18, color=None, weight=500, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or C["ink"]}" '
            f'text-anchor="{anchor}">{e(s)}</text>')


def rect(x, y, w, h, fill, r=8, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{extra}/>'


# ---------- ikon sederhana (24×24, digambar di (x,y), skala s) ----------
ICONS = {
    "chat": '<path d="M3 5h18v11H9l-5 4v-4H3z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "board": '<rect x="3" y="4" width="18" height="16" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M9 4v16M15 4v16" stroke="{c}" stroke-width="2"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="{c}"/>',
    "clock": '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2"/><path d="M12 7v5l3 3" stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round"/>',
    "camera": '<rect x="3" y="7" width="18" height="13" rx="2" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="13.5" r="3.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 7l2-3h4l2 3" stroke="{c}" stroke-width="2" fill="none"/>',
    "app": '<rect x="3" y="3" width="8" height="8" rx="2" fill="{c}"/><rect x="13" y="3" width="8" height="8" rx="2" fill="none" stroke="{c}" stroke-width="2"/><rect x="3" y="13" width="8" height="8" rx="2" fill="none" stroke="{c}" stroke-width="2"/><rect x="13" y="13" width="8" height="8" rx="2" fill="{c}"/>',
    "pin": '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="10" r="2.5" fill="{c}"/>',
    "finger": '<path d="M7 20c-1-3-1-7 1-10a5 5 0 0 1 9 3v4M12 20c-1-2-1-5 0-7M17 19c1-2 1-4 1-6" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "qr": '<rect x="3" y="3" width="7" height="7" fill="none" stroke="{c}" stroke-width="2"/><rect x="14" y="3" width="7" height="7" fill="none" stroke="{c}" stroke-width="2"/><rect x="3" y="14" width="7" height="7" fill="none" stroke="{c}" stroke-width="2"/><path d="M14 14h3v3h-3zM18 18h3v3h-3z" fill="{c}"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M2 19h20" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 12l3 3 5-6" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "doc": '<path d="M6 2h9l5 5v15H6z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M9 11h8M9 15h8M9 19h5" stroke="{c}" stroke-width="2"/>',
    "users": '<circle cx="9" cy="8" r="3.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6" fill="none" stroke="{c}" stroke-width="2"/><circle cx="17" cy="9" r="2.5" fill="{c}"/>',
    "money": '<rect x="2" y="6" width="20" height="12" rx="2" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="{c}"/>',
    "check": '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 12l3 3 5-6" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2s-1-2 0-3h3a4 4 0 0 0 4-4c0-5-4-9-9-9z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="7.5" cy="11" r="1.5" fill="{c}"/><circle cx="11" cy="7" r="1.5" fill="{c}"/><circle cx="16" cy="8.5" r="1.5" fill="{c}"/>',
    "globe": '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" fill="none" stroke="{c}" stroke-width="2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M3 7l9 6 9-6" fill="none" stroke="{c}" stroke-width="2"/>',
    "server": '<rect x="3" y="3" width="18" height="7" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><rect x="3" y="14" width="18" height="7" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="7" cy="6.5" r="1.2" fill="{c}"/><circle cx="7" cy="17.5" r="1.2" fill="{c}"/>',
    "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "support": '<path d="M4 13v-1a8 8 0 0 1 16 0v1" fill="none" stroke="{c}" stroke-width="2"/><rect x="2" y="13" width="5" height="7" rx="2" fill="{c}"/><rect x="17" y="13" width="5" height="7" rx="2" fill="{c}"/>',
    "chart": '<path d="M3 20h18" stroke="{c}" stroke-width="2"/><rect x="5" y="11" width="3" height="7" fill="{c}"/><rect x="10.5" y="6" width="3" height="12" fill="{c}"/><rect x="16" y="9" width="3" height="9" fill="{c}"/>',
    "lock": '<rect x="5" y="10" width="14" height="11" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3" fill="none" stroke="{c}" stroke-width="2"/>',
    "trash": '<path d="M4 6h16M9 6V4h6v2M6 6l1 15h10l1-15" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2" fill="none" stroke="{c}" stroke-width="2"/><path d="M2 10h20" stroke="{c}" stroke-width="2"/>',
}


def icon(name, x, y, s=1.0, c=None):
    body = ICONS.get(name, ICONS["check"]).replace("{c}", c or C["p"])
    return f'<g transform="translate({x},{y}) scale({s})">{body}</g>'


# ---------- bingkai ----------

def frame(judul, body, window=True):
    bg = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["tint"]}"/>'
          f'<stop offset="1" stop-color="#fff4e8"/></linearGradient></defs>'
          f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>')
    if not window:
        return bg + body
    win = (rect(46, 36, 712, 440, "#1b162614", 18) + rect(40, 28, 720, 440, "#fff", 16, f' stroke="{C["line"]}"')
           + f'<path d="M40 44a16 16 0 0 1 16-16h688a16 16 0 0 1 16 16v28H40z" fill="{C["soft"]}"/>'
           + "".join(f'<circle cx="{64 + i * 18}" cy="50" r="5" fill="{col}"/>' for i, col in enumerate(["#ff6b6b", "#ffc04d", "#4cd07d"]))
           + t(400, 56, judul, 15, C["mut"], 600, "middle"))
    return bg + win + body


# ---------- komponen isi (area isi: x 60..740, y 90..450) ----------

def timeline(d):
    rows = d["rows"]
    out, y = [], 110
    gap = min(64, 300 // max(len(rows), 1))
    for r in rows:
        out.append(t(64, y + 22, r["label"], 17, C["ink"], 600))
        x0, total = 230, 400
        out.append(rect(x0, y + 8, total, 20, C["soft"], 10))
        cx = x0
        for kind, frac in r["segs"]:
            w = total * frac
            col = {"a": C["p"], "i": C["idle"], "d": C["o"]}[kind]
            out.append(rect(round(cx, 1), y + 8, round(w, 1), 20, col, 4))
            cx += w
        out.append(t(736, y + 23, r.get("total", ""), 16, C["mut"], 600, "end"))
        if r.get("note"):
            out.append(t(x0, y + 50, r["note"], 13, C["k"], 600))
        y += gap
    ly = 440
    for i, (lab, col) in enumerate([("Active", C["p"]), ("Idle", C["idle"]), ("Distraction", C["o"])]):
        out.append(rect(64 + i * 130, ly - 12, 14, 14, col, 3) + t(84 + i * 130, ly, lab, 14, C["mut"]))
    return "".join(out)


def bars(d):
    """Grafik batang. data: items[{label,value,text,color}], note, animasi (true = batang tumbuh bergantian, loop)."""
    items, out = d["items"], []
    mx = max(i["value"] for i in items)
    y = 104
    step = min(56, 320 // len(items))
    anim = d.get("animasi")
    for i, it in enumerate(items):
        w = 380 * it["value"] / mx
        col = it.get("color") or [C["p"], C["k"], C["o"], C["p"], C["k"], C["o"]][i % 6]
        cls_b = f' class="a-bar" style="animation-delay:{i * .6:.1f}s"' if anim else ""
        cls_t = f' class="a-nilai" style="animation-delay:{i * .6 + .4:.1f}s"' if anim else ""
        out.append(t(64, y + 22, it["label"], 16, C["ink"], 600))
        out.append(rect(250, y + 6, 380, 22, C["soft"], 11) + rect(250, y + 6, round(w * 380 / 400, 1), 22, col, 11, cls_b))
        out.append(f'<g{cls_t}>' + t(736, y + 23, it.get("text", it["value"]), 15, C["mut"], 600, "end") + "</g>")
        y += step
    if d.get("note"):
        out.append(t(64, 445, d["note"], 14, C["mut"]))
    if anim:
        out.insert(0, ANIMASI_BARS)
    return "".join(out)


# Batang tumbuh bergantian dari kiri lalu menghilang bersama (loop 8 detik); diam bila "kurangi animasi".
ANIMASI_BARS = """<style>
.a-bar{transform-box:fill-box;transform-origin:0 50%;animation:tumbuh 8s cubic-bezier(.2,.7,.2,1) infinite both}
.a-nilai{animation:muncul 8s ease-out infinite both}
@keyframes tumbuh{0%{transform:scaleX(0)}10%,85%{transform:scaleX(1)}95%,100%{transform:scaleX(0)}}
@keyframes muncul{0%,4%{opacity:0}12%,85%{opacity:1}95%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.a-bar,.a-nilai{animation:none}}
</style>"""


def grouped(d):
    items, out = d["items"], []
    mx = max(max(i["a"], i["b"]) for i in items)
    base, n = 400, len(items)
    slot = 640 / n
    for k, it in enumerate(items):
        x = 80 + k * slot
        for j, (v, col) in enumerate([(it["a"], C["idle"]), (it["b"], C["p"])]):
            h = 250 * v / mx
            out.append(rect(round(x + j * 44 + 10, 1), round(base - h, 1), 38, round(h, 1), col, 6))
        out.append(t(round(x + 52, 1), base + 26, it["label"], 15, C["ink"], 600, "middle"))
    out.append(f'<path d="M70 {base}H730" stroke="{C["line"]}" stroke-width="2"/>')
    la, lb = d.get("legend", ["Sebelum", "Sesudah"])
    out.append(rect(70, 100, 14, 14, C["idle"], 3) + t(90, 112, la, 14, C["mut"]) +
               rect(230, 100, 14, 14, C["p"], 3) + t(250, 112, lb, 14, C["mut"]))
    return "".join(out)


def gallery(d):
    times, out = d["times"], []
    cols = 3
    for i, tm in enumerate(times[:6]):
        cx, cy = 70 + (i % cols) * 222, 96 + (i // cols) * 170
        out.append(rect(cx, cy, 200, 124, C["soft"], 10, f' stroke="{C["line"]}"'))
        out.append(rect(cx + 12, cy + 14, 60, 96, "#fff", 6) + rect(cx + 82, cy + 14, 106, 14, C["tint"], 4))
        for j in range(4):
            out.append(rect(cx + 82, cy + 40 + j * 16, 106 - j * 18, 8, C["line"], 4))
        out.append(rect(cx + 18, cy + 22, 48, 8, [C["p"], C["k"], C["o"]][i % 3], 4))
        out.append(icon("camera", cx + 4, cy + 132, 0.7, C["mut"]) + t(cx + 26, cy + 146, tm, 14, C["mut"], 600))
    return "".join(out)


def tasklist(d):
    out = [t(64, 112, d.get("head", "Tugas"), 13, C["mut"], 700), t(736, 112, d.get("head2", "Waktu"), 13, C["mut"], 700, "end")]
    y = 128
    for r in d["rows"]:
        run = r.get("status") == "run"
        out.append(rect(60, y, 680, 52, C["tint"] if run else "#fff", 10, f' stroke="{C["line"]}"'))
        out.append(f'<circle cx="88" cy="{y + 26}" r="14" fill="{C["p"] if run else C["soft"]}"/>')
        out.append(f'<rect x="83" y="{y + 21}" width="10" height="10" rx="2" fill="#fff"/>' if run
                   else f'<path d="M84 {y + 19}l10 7-10 7z" fill="{C["mut"]}"/>')
        out.append(t(114, y + 32, r["title"], 16, C["ink"], 600))
        if r.get("tag"):
            out.append(t(520, y + 32, r["tag"], 13, C["k"], 700))
        out.append(t(724, y + 32, r["time"], 17, C["p"] if run else C["ink"], 700, "end"))
        y += 62
    return "".join(out)


def table(d):
    heads, rows, out = d["headers"], d["rows"], []
    n = len(heads)
    cw = 680 / n
    out.append(rect(60, 96, 680, 40, C["soft"], 8))
    for j, h in enumerate(heads):
        out.append(t(round(74 + j * cw, 1), 122, h, 14, C["mut"], 700))
    y = 136
    for r in rows:
        for j, v in enumerate(r):
            out.append(t(round(74 + j * cw, 1), y + 30, v, 15, C["ink"] if j == 0 else C["mut"], 600 if j == 0 else 500))
        out.append(f'<path d="M60 {y + 46}H740" stroke="{C["line"]}"/>')
        y += 46
    if d.get("total"):
        out.append(t(74, y + 32, d["total"][0], 15, C["ink"], 800) + t(726, y + 32, d["total"][1], 16, C["p"], 800, "end"))
    return "".join(out)


def chat(d):
    out, y = [], 100
    for m in d["messages"]:
        me = m.get("me")
        w = min(420, 24 + 8.6 * len(m["text"]))
        x = 740 - w if me else 100
        if not me:
            out.append(f'<circle cx="78" cy="{y + 20}" r="14" fill="{C["tint"]}"/>' + t(78, y + 25, m["who"][0], 13, C["p"], 700, "middle"))
            out.append(t(x + 4, y - 4, m["who"], 12, C["mut"], 600))
        out.append(rect(round(x, 1), y, round(w, 1), 40, C["p"] if me else C["soft"], 14))
        out.append(t(round(x + 14, 1), y + 26, m["text"], 15, "#fff" if me else C["ink"], 500))
        y += 66 if not me else 56
    if d.get("note"):
        out.append(rect(60, 420, 680, 32, "#fff1e3", 8) + t(400, 441, d["note"], 14, C["o"], 700, "middle"))
    return "".join(out)


def doc(d):
    out = [rect(170, 92, 460, 360, "#fff", 12, f' stroke="{C["line"]}"'),
           t(196, 132, d["title"], 20, C["ink"], 800)]
    y = 160
    for ln in d["lines"]:
        if d.get("checks"):
            out.append(f'<rect x="196" y="{y}" width="20" height="20" rx="5" fill="{C["ok"]}"/>'
                       f'<path d="M200 {y + 10}l4 4 8-8" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
            out.append(t(228, y + 16, ln, 15, C["ink"], 500))
        else:
            out.append(t(196, y + 16, ln, 15, C["ink"], 500))
        y += 34
    if d.get("footer"):
        out.append(rect(196, 404, 408, 30, C["tint"], 8) + t(400, 424, d["footer"], 14, C["p"], 700, "middle"))
    return "".join(out)


def dialog(d):
    out = [rect(40, 72, 720, 396, "#1b162622", 0),
           rect(180, 110, 440, 320, "#fff", 16, f' stroke="{C["line"]}"'),
           icon(d.get("icon", "shield"), 206, 136, 1.4, C["p"]),
           t(250, 162, d["title"], 19, C["ink"], 800)]
    y = 206
    for ln in d["lines"]:
        out.append(f'<circle cx="212" cy="{y - 5}" r="4" fill="{C["p"]}"/>' + t(226, y, ln, 15, C["ink"]))
        y += 32
    bx = 596
    for i, b in enumerate(reversed(d["buttons"])):
        w = 24 + 8.4 * len(b)
        bx -= w
        primary = i == 0
        out.append(rect(round(bx, 1), 376, round(w, 1), 36, C["p"] if primary else "#fff", 10,
                        "" if primary else f' stroke="{C["line"]}"'))
        out.append(t(round(bx + w / 2, 1), 399, b, 14, "#fff" if primary else C["ink"], 700, "middle"))
        bx -= 12
    return "".join(out)


def steps(d):
    items, out = d["items"], []
    n = len(items)
    bw = (640 - (n - 1) * 30) / n
    for i, it in enumerate(items):
        x = 80 + i * (bw + 30)
        out.append(rect(round(x, 1), 170, round(bw, 1), 170, "#fff", 14, f' stroke="{C["line"]}"'))
        out.append(f'<circle cx="{round(x + bw / 2, 1)}" cy="214" r="22" fill="{[C["p"], C["k"], C["o"], C["p"]][i % 4]}"/>')
        out.append(icon(it.get("icon", "check"), round(x + bw / 2 - 12, 1), 202, 1, "#fff"))
        words = it["label"].split()
        mid = (len(words) + 1) // 2
        for k, line in enumerate([" ".join(words[:mid]), " ".join(words[mid:])]):
            if line:
                out.append(t(round(x + bw / 2, 1), 270 + k * 22, line, 16, C["ink"], 700, "middle"))
        if i < n - 1:
            ax = x + bw + 4
            out.append(f'<path d="M{round(ax, 1)} 255h20l-6-6m6 6l-6 6" stroke="{C["mut"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    if d.get("note"):
        out.append(t(400, 392, d["note"], 15, C["mut"], 600, "middle"))
    return "".join(out)


def cards(d):
    items, out = d["items"], []
    n = len(items)
    cols = n if n <= 4 else 3
    rows = (n + cols - 1) // cols
    if rows == 1:   # satu baris: kartu mengisi tinggi kanvas (tanpa ruang kosong besar atas-bawah)
        x0, lebar, gap = 44, 712, 18
        cw, ch = (lebar - (cols - 1) * gap) / cols, 280
        for i, it in enumerate(items):
            x, y = x0 + i * (cw + gap), (500 - ch) / 2
            hi = it.get("highlight")
            out.append(rect(round(x, 1), round(y, 1), round(cw, 1), ch, C["tint"] if hi else "#fff", 18,
                            f' stroke="{C["p"] if hi else C["line"]}"' + (' stroke-width="2.5"' if hi else "")))
            out.append(f'<circle cx="{x + cw / 2:.1f}" cy="{y + 92:.1f}" r="46" fill="{"#fff" if hi else C["tint"]}"/>')
            out.append(icon(it.get("icon", "check"), round(x + cw / 2 - 26, 1), round(y + 66, 1), 2.2, C["p"] if hi else C["mut"]))
            out.append(t(round(x + cw / 2, 1), round(y + 190, 1), it["label"], 21, C["ink"], 800, "middle"))
            if it.get("sub"):
                out.append(t(round(x + cw / 2, 1), round(y + 220, 1), it["sub"], 15, C["mut"], 500, "middle"))
        return "".join(out)
    cw, ch = (640 - (cols - 1) * 20) / cols, min(150, (330 - (rows - 1) * 20) / rows)
    for i, it in enumerate(items):
        x = 80 + (i % cols) * (cw + 20)
        y = 100 + (i // cols) * (ch + 20)
        hi = it.get("highlight")
        out.append(rect(round(x, 1), round(y, 1), round(cw, 1), round(ch, 1), C["tint"] if hi else "#fff", 14,
                        f' stroke="{C["p"] if hi else C["line"]}"' + (' stroke-width="2"' if hi else "")))
        out.append(icon(it.get("icon", "check"), round(x + cw / 2 - 18, 1), round(y + 22, 1), 1.5, C["p"] if hi else C["mut"]))
        out.append(t(round(x + cw / 2, 1), round(y + ch - 40, 1), it["label"], 16, C["ink"], 700, "middle"))
        if it.get("sub"):
            out.append(t(round(x + cw / 2, 1), round(y + ch - 18, 1), it["sub"], 13, C["mut"], 500, "middle"))
    return "".join(out)


def map_(d):
    out = [rect(40, 72, 720, 396, "#eef3ee", 0)]
    for i in range(1, 7):
        out.append(f'<path d="M40 {72 + i * 58}H760" stroke="#fff" stroke-width="6"/>')
    for i in range(1, 10):
        out.append(f'<path d="M{40 + i * 80} 72V468" stroke="#fff" stroke-width="6"/>')
    out.append('<path d="M40 380C200 300 360 420 520 250S700 160 760 140" stroke="#ffffffcc" stroke-width="14" fill="none"/>')
    if d.get("fence"):
        f = d["fence"]
        out.append(f'<circle cx="{f["x"]}" cy="{f["y"]}" r="{f["r"]}" fill="{C["p"]}22" stroke="{C["p"]}" stroke-width="2.5" stroke-dasharray="8 6"/>')
        out.append(t(f["x"], f["y"] - f["r"] - 10, f.get("label", ""), 14, C["p"], 700, "middle"))
    for p in d.get("pins", []):
        col = C["ok"] if p.get("ok", True) else C["o"]
        out.append(f'<path d="M{p["x"]} {p["y"]}c-12-16-18-24-18-32a18 18 0 0 1 36 0c0 8-6 16-18 32z" fill="{col}"/>'
                   f'<circle cx="{p["x"]}" cy="{p["y"] - 32}" r="7" fill="#fff"/>')
        if p.get("label"):
            w = 16 + 7.6 * len(p["label"])
            out.append(rect(round(p["x"] - w / 2, 1), p["y"] + 6, round(w, 1), 26, "#fff", 13) +
                       t(p["x"], p["y"] + 24, p["label"], 13, C["ink"], 700, "middle"))
    if d.get("card"):
        c = d["card"]
        out.append(rect(480, 96, 256, 32 + 26 * len(c["lines"]), "#fff", 14, f' stroke="{C["line"]}"'))
        out.append(t(500, 124, c["title"], 16, C["ink"], 800))
        for i, ln in enumerate(c["lines"]):
            out.append(t(500, 150 + i * 26, ln, 14, C["ok"] if ln.startswith("✓") else C["mut"], 600))
    return "".join(out)


def compare(d):
    out = []
    for k, side in enumerate([d["left"], d["right"]]):
        x = 64 + k * 346
        hi = k == 1
        out.append(rect(x, 96, 326, 352, C["tint"] if hi else "#fff", 14, f' stroke="{C["p"] if hi else C["line"]}"'))
        out.append(icon(side.get("icon", "doc"), x + 20, 116, 1.2, C["p"] if hi else C["mut"]))
        out.append(t(x + 56, 138, side["title"], 18, C["ink"], 800))
        y = 186
        for it in side["items"]:
            ok = not it.startswith("-")
            label = it.lstrip("-+ ")
            out.append(f'<circle cx="{x + 30}" cy="{y - 5}" r="10" fill="{C["ok"] if ok else C["idle"]}"/>')
            out.append(f'<path d="M{x + 25} {y - 5}l4 4 6-7" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>' if ok
                       else f'<path d="M{x + 25} {y - 5}h10" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>')
            out.append(t(x + 50, y, label, 15, C["ink"] if ok else C["mut"], 500))
            y += 40
    return "".join(out)


def venn(d):
    return (f'<circle cx="320" cy="270" r="150" fill="{C["p"]}26" stroke="{C["p"]}" stroke-width="2"/>'
            f'<circle cx="480" cy="270" r="150" fill="{C["o"]}26" stroke="{C["o"]}" stroke-width="2"/>'
            + t(250, 220, d["a"], 20, C["p"], 800, "middle")
            + "".join(t(250, 254 + i * 26, s, 14, C["ink"], 500, "middle") for i, s in enumerate(d.get("a_items", [])))
            + t(550, 220, d["b"], 20, C["o"], 800, "middle")
            + "".join(t(550, 254 + i * 26, s, 14, C["ink"], 500, "middle") for i, s in enumerate(d.get("b_items", [])))
            + t(400, 262, d.get("mid", ""), 15, C["ink"], 800, "middle")
            + t(400, 286, d.get("mid2", ""), 13, C["mut"], 600, "middle"))


def shield(d):
    out = ['<g transform="translate(110,110) scale(11)">'
           f'<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z" fill="{C["tint"]}" stroke="{C["p"]}" stroke-width=".5"/>'
           f'<path d="M8 12l3 3 5-6" fill="none" stroke="{C["p"]}" stroke-width="1" stroke-linecap="round"/></g>']
    y = 140
    for ln in d["lines"]:
        out.append(f'<circle cx="424" cy="{y - 5}" r="10" fill="{C["ok"]}"/>'
                   f'<path d="M419 {y - 5}l4 4 6-7" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        out.append(t(444, y, ln, 16, C["ink"], 600))
        y += 46
    return "".join(out)


def brand(d):
    out = [rect(64, 92, 672, 54, C["soft"], 10),
           rect(80, 104, 120, 30, C["ink"], 8) + t(140, 124, d.get("logo", "Logo Anda"), 14, "#fff", 800, "middle"),
           rect(260, 104, 300, 30, "#fff", 15, f' stroke="{C["line"]}"') + icon("lock", 270, 107, 0.75, C["ok"])
           + t(294, 124, d.get("domain", "app.merekanda.id"), 14, C["mut"], 600)]
    sw = d.get("swatches", ["#0f766e", "#2563eb", "#b45309", "#7B2CFF"])
    out.append(t(64, 186, "Warna brand", 14, C["mut"], 700))
    for i, c in enumerate(sw):
        out.append(f'<circle cx="{84 + i * 46}" cy="214" r="16" fill="{c}"' + (f' stroke="{C["ink"]}" stroke-width="3"' if i == 0 else "") + "/>")
    out.append(rect(300, 172, 436, 260, "#fff", 14, f' stroke="{C["line"]}"') + rect(300, 172, 436, 44, sw[0], 14)
               + rect(300, 196, 436, 20, sw[0], 0) + t(320, 200, d.get("app", "Nama Aplikasi Anda"), 16, "#fff", 800))
    for i in range(3):
        out.append(rect(320, 236 + i * 60, 396, 44, C["soft"], 8) + rect(334, 250 + i * 60, 140 - i * 30, 14, C["line"], 6)
                   + rect(640, 248 + i * 60, 60, 18, sw[0] + "33", 9))
    for i, lab in enumerate(d.get("items", ["Logo", "Warna", "Domain", "Email"])):
        out.append(icon("check", 64, 266 + i * 40, 0.9, C["ok"]) + t(94, 284 + i * 40, lab, 15, C["ink"], 600))
    return "".join(out)


def tiers(d):
    out, items = [], d["items"]
    for i, it in enumerate(items):
        h = 120 + i * 80
        x = 110 + i * 200
        col = [C["idle"], C["p"], C["k"]][i % 3]
        out.append(rect(x, 440 - h, 170, h, col if i else "#fff", 14, "" if i else f' stroke="{C["line"]}"'))
        out.append(t(x + 85, 470 - h, it["name"], 17, "#fff" if i else C["ink"], 800, "middle"))
        for k, ln in enumerate(it.get("lines", [])):
            out.append(t(x + 85, 500 - h + k * 24, ln, 13, "#ffffffdd" if i else C["mut"], 600, "middle"))
    return "".join(out)


def orang(d):
    """Adegan orang bekerja di meja (tampak depan, gaya flat tanpa wajah) + kartu UI melayang di kanan.
    data: kulit, rambut (pendek|panjang|hijab), baju (p|k|o), kartu {icon,title,lines,buttons}, animasi (true = motion graphic CSS)."""
    kulit = {"terang": "#f3cfb1", "sedang": "#e3b08b", "gelap": "#c98d66"}.get(d.get("kulit", "sedang"), d.get("kulit", "#e3b08b"))
    baju = C[d.get("baju", "p")]
    hair = "#2b2230"
    out = [f'<circle cx="250" cy="250" r="178" fill="#ffffff" opacity=".55"/>',
           f'<circle cx="250" cy="250" r="128" fill="{C["tint"]}"/>',
           f'<ellipse cx="240" cy="452" rx="190" ry="14" fill="#1b162612"/>']
    # kursi
    out.append(rect(176, 196, 148, 160, "#d9cff3", 28))
    # rambut belakang (panjang/hijab)
    style = d.get("rambut", "pendek")
    if style == "panjang":
        out.append(rect(206, 140, 88, 120, hair, 40))
    # badan & lengan
    out.append(f'<path d="M166 352 Q168 258 250 244 Q332 258 334 352 Z" fill="{baju}"/>')
    out.append(f'<path d="M176 300 Q168 336 214 340" stroke="{baju}" stroke-width="26" fill="none" stroke-linecap="round"/>'
               f'<path d="M324 300 Q332 336 286 340" stroke="{baju}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    kain = C["k"] if d.get("baju", "p") != "k" else C["p"]
    if style != "hijab":
        out.append(rect(236, 214, 28, 40, kulit, 12) + f'<path d="M236 246 L250 262 L264 246" fill="#ffffff" opacity=".85"/>')
    # kepala (bergerak halus saat animasi)
    out.append('<g class="a-kepala">')
    if style == "hijab":
        out.append(f'<path d="M206 176 Q206 126 250 124 Q294 126 294 176 L304 262 Q250 286 196 262 Z" fill="{kain}"/>')
    out.append(f'<ellipse cx="250" cy="182" rx="{30 if style == "hijab" else 34}" ry="{36 if style == "hijab" else 40}" fill="{kulit}"/>')
    fitur = "#00000033"   # garis wajah halus (mata terpejam + senyum), bukan wajah realistis
    out.append(f'<path d="M234 184 q6 5 12 0 M254 184 q6 5 12 0" stroke="{fitur}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
               f'<path d="M242 200 q8 7 16 0" stroke="{fitur}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
               f'<circle cx="230" cy="196" r="5" fill="#ff8a8a" opacity=".25"/><circle cx="270" cy="196" r="5" fill="#ff8a8a" opacity=".25"/>')
    if style != "hijab":
        out.append(f'<circle cx="216" cy="186" r="7" fill="{kulit}"/><circle cx="284" cy="186" r="7" fill="{kulit}"/>')
        out.append(f'<path d="M214 182 Q208 134 250 132 Q292 134 286 182 Q280 156 250 154 Q222 154 214 182 Z" fill="{hair}"/>')
    out.append('</g>')
    # laptop (tampak belakang) & meja
    out.append(rect(186, 252, 128, 86, "#2b2534", 8) + f'<circle class="a-logo" cx="250" cy="295" r="9" fill="url(#lg)"/>')
    out.append(f'<defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["p"]}"/><stop offset="1" stop-color="{C["o"]}"/></linearGradient></defs>')
    out.append(f'<circle class="a-tangan1" cx="208" cy="340" r="9" fill="{kulit}"/><circle class="a-tangan2" cx="292" cy="340" r="9" fill="{kulit}"/>')
    out.append(rect(176, 336, 148, 7, "#4a4358", 3))
    out.append(rect(64, 342, 352, 14, "#ffffff", 7, f' stroke="{C["line"]}"'))
    out.append(rect(84, 356, 10, 92, "#d9cff3", 4) + rect(386, 356, 10, 92, "#d9cff3", 4))
    # tanaman & cangkir
    out.append('<g class="a-daun">' + f'<ellipse cx="112" cy="282" rx="11" ry="26" fill="{C["ok"]}" transform="rotate(-24 112 282)"/>'
               f'<ellipse cx="134" cy="276" rx="11" ry="28" fill="#1fb86a" transform="rotate(18 134 276)"/>'
               f'<ellipse cx="123" cy="270" rx="9" ry="26" fill="{C["ok"]}"/></g>')
    out.append(rect(104, 300, 40, 42, C["o"], 8))
    out.append(rect(340, 314, 28, 28, C["k"], 6) + f'<path d="M368 320 q12 0 12 9 q0 9 -12 9" stroke="{C["k"]}" stroke-width="4" fill="none"/>'
               + "".join(f'<path class="a-uap a-uap{i}" d="M{348 + i * 8} 306 q-5 -8 0 -16 q5 -8 0 -16" stroke="{C["mut"]}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0"/>' for i in range(2)))
    # garis penghubung laptop → kartu
    out.append(f'<path d="M318 262 C 356 238, 376 216, 412 206" stroke="{C["p"]}" stroke-width="2.5" stroke-dasharray="6 6" fill="none" opacity=".6" class="a-alir"/>'
               f'<circle class="a-denyut" cx="318" cy="262" r="5" fill="{C["p"]}"/>')
    # kartu UI
    k = d["kartu"]
    x0, y0, w = 418, 104, 336
    out.append('<g class="a-kartu">' + rect(x0 + 6, y0 + 10, w, 300, "#1b162614", 18) + rect(x0, y0, w, 300, "#fff", 16, f' stroke="{C["line"]}"'))
    out.append(icon(k.get("icon", "eye"), x0 + 22, y0 + 24, 1.25, C["p"]) + t(x0 + 60, y0 + 46, k["title"], 16, C["ink"], 800))
    y = y0 + 90
    for i, ln in enumerate(k["lines"]):
        out.append(f'<g class="a-baris a-baris{i}"><circle cx="{x0 + 28}" cy="{y - 5}" r="4" fill="{C["p"]}"/>' + t(x0 + 42, y, ln, 13.5, C["ink"]) + '</g>')
        y += 30
    bx = x0 + w - 22
    for i, b in enumerate(reversed(k.get("buttons", []))):
        bw = 22 + 7.4 * len(b)
        bx -= bw
        primary = i == 0
        out.append((f'<g class="a-tombol">' if primary else "") + rect(round(bx, 1), y0 + 242, round(bw, 1), 36, C["p"] if primary else "#fff", 10, "" if primary else f' stroke="{C["line"]}"'))
        out.append(t(round(bx + bw / 2, 1), y0 + 265, b, 13, "#fff" if primary else C["ink"], 700, "middle") + ("</g>" if primary else ""))
        bx -= 10
    out.append("</g>")
    if d.get("animasi"):
        out.insert(0, ANIMASI_ORANG)
    return "".join(out)


# Motion graphic ringan di dalam SVG (CSS, jalan juga lewat <img>); diam bila pengunjung memilih "kurangi animasi".
ANIMASI_ORANG = """<style>
[class^="a-"]{transform-box:fill-box;transform-origin:center}
.a-kartu{animation:apung 5s ease-in-out infinite}
.a-kepala{transform-origin:50% 100%;animation:angguk 6s ease-in-out infinite}
.a-tangan1{animation:ketik .5s ease-in-out infinite alternate}
.a-tangan2{animation:ketik .5s ease-in-out .25s infinite alternate}
.a-daun{transform-origin:50% 100%;animation:goyang 4s ease-in-out infinite}
.a-alir{animation:alir 1.2s linear infinite}
.a-denyut{animation:denyut 2s ease-in-out infinite}
.a-logo{animation:denyut 3s ease-in-out infinite}
.a-uap{animation:uap 3s ease-out infinite}.a-uap1{animation-delay:1.5s}
.a-baris{animation:muncul 8s ease-out infinite}
.a-baris1{animation-delay:.4s}.a-baris2{animation-delay:.8s}.a-baris3{animation-delay:1.2s}
.a-tombol{animation:tekan 8s ease-in-out infinite}
@keyframes apung{50%{transform:translateY(-8px)}}
@keyframes angguk{0%,100%{transform:rotate(0)}30%{transform:rotate(-2deg)}60%{transform:rotate(1.5deg)}}
@keyframes ketik{to{transform:translateY(-4px)}}
@keyframes goyang{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}
@keyframes alir{to{stroke-dashoffset:-24}}
@keyframes denyut{50%{transform:scale(1.35);opacity:.7}}
@keyframes uap{0%{opacity:0;transform:translateY(6px)}30%{opacity:.6}100%{opacity:0;transform:translateY(-14px)}}
@keyframes muncul{0%,4%{opacity:0;transform:translateX(-10px)}12%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes tekan{0%,55%,70%,100%{transform:scale(1)}62%{transform:scale(.94)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.a-uap{opacity:0}}
</style>"""


# Chat "hidup": pesan muncul bergantian, gelembung mengetik sebelum pesan tim, lalu berulang (siklus 10 detik).
ANIMASI_WA = """<style>
.a-pesan,.a-ketik{transform-box:fill-box;transform-origin:0 100%}
.a-pesan.a-kanan{transform-origin:100% 100%}
.a-pesan{animation:pesan 10s cubic-bezier(.2,.8,.2,1) infinite both}
.a-ketik{animation:ketik 10s linear infinite both}
.a-titik{animation:titik .9s ease-in-out infinite}
@keyframes pesan{0%{opacity:0;transform:translateY(10px) scale(.94)}4%,88%{opacity:1;transform:none}94%,100%{opacity:0;transform:none}}
@keyframes ketik{0%{opacity:0}1%,9%{opacity:1}10%,100%{opacity:0}}
@keyframes titik{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@media (prefers-reduced-motion:reduce){.a-pesan,.a-ketik,.a-titik{animation:none}.a-ketik{display:none}}
</style>"""


def _bungkus(teks, maks=27):
    baris, cur = [], ""
    for w in teks.split():
        if len(cur) + len(w) + (1 if cur else 0) > maks and cur:
            baris.append(cur); cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    return baris + ([cur] if cur else [])


def wa(d):
    """Percakapan bergaya aplikasi chat populer (header hijau tua, latar krem, gelembung putih/hijau muda, centang biru)
    di dalam ponsel. Tanpa logo/nama merek aplikasi chat. data: kontak, status, messages[{text, me, jam}], animasi."""
    G, KREM, HIJAU_MUDA = "#008069", "#efeae2", "#d9fdd3"
    out = [f'<circle cx="400" cy="250" r="210" fill="#ffffff" opacity=".5"/><circle cx="400" cy="250" r="150" fill="{C["tint"]}"/>',
           '<defs><clipPath id="layar"><rect x="262" y="26" width="276" height="452" rx="26"/></clipPath></defs>',
           rect(250, 14, 300, 476, "#1b1626", 38), f'<g clip-path="url(#layar)">', rect(262, 26, 276, 452, KREM, 0)]
    # pola latar halus
    out.append("".join(f'<circle cx="{280 + (i % 7) * 40}" cy="{110 + (i // 7) * 46}" r="2" fill="#d6cfc4"/>' for i in range(56)))
    # header
    out.append(rect(262, 26, 276, 64, G, 0) + f'<path d="M282 58l8-8M282 58l8 8" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
               + f'<circle cx="318" cy="58" r="16" fill="#dff5ec"/>' + t(318, 64, d.get("kontak", "Tim")[0], 15, G, 800, "middle")
               + t(342, 54, d.get("kontak", "Tim"), 14, "#fff", 700) + t(342, 72, d.get("status", "online"), 11, "#d1f0e6", 500))
    y = 110
    anim = d.get("animasi")
    for idx, m in enumerate(d["messages"]):
        lines = _bungkus(m["text"])
        tunda = .6 + idx * 1.8
        w = max(len(l) for l in lines) * 7.1 + 64
        h = 16 * len(lines) + 24
        me = m.get("me")
        x = 526 - w if me else 274
        if anim and not me:   # gelembung "sedang mengetik" sebelum pesan dari tim
            out.append(f'<g class="a-ketik" style="animation-delay:{tunda - 1:.1f}s">' + rect(274, y, 58, 30, "#fff", 10, ' filter="url(#bayang)"')
                       + "".join(f'<circle class="a-titik" style="animation-delay:{k * .15:.2f}s" cx="{291 + k * 12}" cy="{y + 15}" r="3.2" fill="#8696a0"/>' for k in range(3)) + "</g>")
        if anim:
            out.append(f'<g class="a-pesan{" a-kanan" if me else ""}" style="animation-delay:{tunda:.1f}s">')
        out.append(rect(round(x, 1), y, round(w, 1), h, HIJAU_MUDA if me else "#ffffff", 10, ' filter="url(#bayang)"'))
        tail = (f'<path d="M{526} {y} l10 0 l-10 10z" fill="{HIJAU_MUDA}"/>' if me else f'<path d="M274 {y} l-10 0 l10 10z" fill="#fff"/>')
        out.append(tail)
        for k, l in enumerate(lines):
            out.append(t(round(x + 10, 1), y + 18 + k * 16, l, 12.5, "#111b21", 500))
        jam = m.get("jam", "09.1" + str(len(out) % 10))
        tx = x + w - 10
        if me:
            out.append(t(round(tx - 18, 1), y + h - 6, jam, 9.5, "#667781", 500, "end")
                       + f'<path d="M{tx - 15:.1f} {y + h - 10} l3 3 6-6 M{tx - 10:.1f} {y + h - 10} l3 3 6-6" stroke="#53bdeb" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
        else:
            out.append(t(round(tx, 1), y + h - 6, jam, 9.5, "#667781", 500, "end"))
        if anim:
            out.append("</g>")
        y += h + 10
    # bilah ketik
    out.append(rect(272, 432, 210, 36, "#fff", 18) + t(290, 455, "Ketik pesan", 12.5, "#8696a0", 500)
               + f'<circle cx="510" cy="450" r="18" fill="{G}"/><path d="M510 442v10 M505 448a5 5 0 0 0 10 0 M510 453v4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>')
    out.append("</g>")
    if anim:
        out.insert(0, ANIMASI_WA)
    out.insert(0, '<defs><filter id="bayang" x="-5%" y="-5%" width="110%" height="130%"><feDropShadow dx="0" dy="1" stdDeviation=".6" flood-color="#0b141a" flood-opacity=".13"/></filter></defs>')
    return "".join(out)


JENIS = {"timeline": timeline, "bars": bars, "grouped": grouped, "gallery": gallery, "tasklist": tasklist,
         "table": table, "chat": chat, "doc": doc, "dialog": dialog, "steps": steps, "cards": cards,
         "map": map_, "compare": compare, "venn": venn, "shield": shield, "brand": brand, "tiers": tiers, "orang": orang, "wa": wa}


def render_svg(item, colors=None):
    if colors:
        C.update(colors)
    body = JENIS[item["jenis"]](item.get("data", {}))
    window = item["jenis"] not in ("venn", "shield", "tiers", "steps", "cards", "compare", "orang", "wa")
    inner = frame(item.get("judul", ""), body, window)
    # ilustrasi tanpa jendela tidak diberi judul melayang (user: "tidak perlu ada title di gambarnya");
    # konteks cukup dari judul section + caption. Ilustrasi berjendela tetap punya judul di bilah jendela.
    # komponen berbentuk ponsel dipotong ke kanvas potret selebar ponselnya (user: "areanya terlalu lebar")
    vb, vw, vh = (("230 0 340 500", 340, 500) if item["jenis"] == "wa" else (f"0 0 {W} {H}", W, H))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{vw}" height="{vh}" '
            f'font-family="{FONT}" role="img" aria-label="{e(item["alt"])}">{inner}</svg>\n')


def generate(root: Path, data: dict, colors=None):
    out_dir = root / "static" / "ilustrasi"
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for it in data["gambar"]:
        if it.get("auto", True):
            (out_dir / f'{it["id"]}.svg').write_text(render_svg(it, colors), encoding="utf-8")
            n += 1
    return n
