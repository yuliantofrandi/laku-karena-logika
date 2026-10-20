"""Server pratinjau dist/ tanpa cache browser, supaya hasil build terbaru selalu tampil.

Hanya halaman statis. Blog & Panduan (Cloudflare Functions) dipratinjau dengan: npx wrangler@4 pages dev dist
"""
import http.server, sys, functools, os

class NoCache(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # sama seperti Cloudflare Pages: /slug → slug.html
        p = super().translate_path(path)
        return p + ".html" if not os.path.exists(p) and os.path.exists(p + ".html") else p

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 4321
root = sys.argv[2] if len(sys.argv) > 2 else "dist"
http.server.ThreadingHTTPServer(("", port), functools.partial(NoCache, directory=root)).serve_forever()
