"""Local preview server that mimics GitHub Pages: serves 404.html for missing paths.

Usage: python serve.py [port]
"""
import http.server
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8790


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_error(self, code, message=None, explain=None):
        page = ROOT / "404.html"
        if code != 404 or not page.is_file():
            return super().send_error(code, message, explain)
        body = page.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(ROOT)
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), PagesHandler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/")
        httpd.serve_forever()
