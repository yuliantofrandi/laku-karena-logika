"""Server pratinjau dist/ tanpa cache browser, supaya hasil build terbaru selalu tampil."""
import http.server, sys, functools

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 4321
root = sys.argv[2] if len(sys.argv) > 2 else "dist"
http.server.ThreadingHTTPServer(("", port), functools.partial(NoCache, directory=root)).serve_forever()
