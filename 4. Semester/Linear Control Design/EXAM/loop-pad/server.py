"""Loop Pad — LAN whiteboard server for oral-exam derivation practice.

Serves:
  /            the S-Pen drawing app (app.html)
  /course      the Closed Loop crash-course page (../Closed-Loop.html) with a pad link injected
  POST /api/save      {id,title,png,strokes} -> boards/<date>/<HHMMSS>_<slug>.png + .json
  GET  /api/feedback  -> feedback.json (list; the reviewing Claude session appends entries)
  GET  /api/boards    -> list of saved boards (newest first)

Feedback entry schema (append to feedback.json; the app polls every 5 s):
  {"board": "<png filename>", "time": "HH:MM", "verdict": "correct|partly|wrong",
   "notes": ["..."], "svg": "<optional SVG fragment in the 2000x1400 board space>"}

Run:  python server.py   (allow the Windows-Firewall prompt on first run)
"""
import base64
import json
import re
import socket
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARDS = HERE / "boards"
FEEDBACK = HERE / "feedback.json"
COURSE = HERE.parent / "Closed-Loop.html"
PORT = 8321

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def slug(t):
    return re.sub(r"[^a-z0-9-]+", "-", (t or "board").lower()).strip("-")[:40] or "board"

_icons = {}
def make_icon(size):
    """Amber loop glyph on the app's dark ground — drawn with Pillow, cached."""
    if size in _icons:
        return _icons[size]
    import io
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (size, size), "#0D1220")
    d = ImageDraw.Draw(img)
    m = size // 8
    d.ellipse([m, m, size - m, size - m], outline="#F0A03C", width=size // 10)
    d.ellipse([size // 2 + size // 8, size // 2 - size // 16,
               size // 2 + size // 4, size // 2 + size // 16], fill="#4FC4D4")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    _icons[size] = buf.getvalue()
    return _icons[size]

class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep the console clean

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            html = (HERE / "app.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
        elif self.path.startswith("/course"):
            html = COURSE.read_text(encoding="utf-8")
            inject = ('<a href="/" style="position:fixed;bottom:18px;right:18px;z-index:999;'
                      'background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;text-decoration:none;'
                      'font:700 14px sans-serif;padding:12px 18px;border-radius:99px;'
                      'box-shadow:0 4px 18px rgba(0,0,0,.35)">✍ Loop Pad</a>')
            html = html.replace("</body>", inject + "</body>") if "</body>" in html else html + inject
            self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path.startswith("/api/questions"):
            self._send(200, (HERE / "questions.json").read_bytes())
        elif self.path.startswith("/manifest.json"):
            self._send(200, json.dumps({
                "name": "Loop Pad", "short_name": "LoopPad", "id": "/", "scope": "/", "start_url": "/",
                "display": "standalone", "orientation": "landscape",
                "background_color": "#0D1220", "theme_color": "#0D1220",
                "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}],
            }).encode("utf-8"), "application/manifest+json")
        elif self.path.startswith("/sw.js"):
            self._send(200, b"self.addEventListener('install',e=>self.skipWaiting());"
                            b"self.addEventListener('activate',e=>e.waitUntil(clients.claim()));"
                            b"self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request).catch(()=>new Response('offline - the pad needs the PC server',{status:503})))});",
                       "text/javascript")
        elif self.path.startswith("/icon-"):
            size = 512 if "512" in self.path else 192
            self._send(200, make_icon(size), "image/png")
        elif self.path.startswith("/api/feedback"):
            fb = json.loads(FEEDBACK.read_text(encoding="utf-8")) if FEEDBACK.exists() else []
            self._send(200, fb)
        elif self.path.startswith("/api/boards"):
            out = []
            if BOARDS.exists():
                for p in sorted(BOARDS.rglob("*.json"), reverse=True):
                    try:
                        meta = json.loads(p.read_text(encoding="utf-8"))
                        out.append({"file": p.with_suffix(".png").name,
                                    "title": meta.get("title", ""), "day": p.parent.name})
                    except (OSError, json.JSONDecodeError):
                        pass
            self._send(200, out[:50])
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if not self.path.startswith("/api/save"):
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n).decode("utf-8"))
            day = datetime.now().strftime("%Y-%m-%d")
            d = BOARDS / day
            d.mkdir(parents=True, exist_ok=True)
            base = datetime.now().strftime("%H%M%S") + "_" + slug(payload.get("title"))
            png_b64 = payload["png"].split(",", 1)[1]
            (d / (base + ".png")).write_bytes(base64.b64decode(png_b64))
            meta = {"title": payload.get("title", ""), "id": payload.get("id", ""),
                    "saved": datetime.now().isoformat(timespec="seconds"),
                    "strokes": payload.get("strokes", 0),
                    "qid": payload.get("qid", ""), "prompt": payload.get("prompt", "")}
            (d / (base + ".json")).write_text(json.dumps(meta, indent=1), encoding="utf-8")
            print(f"  saved board: {day}/{base}.png  ('{meta['title']}')")
            self._send(200, {"ok": True, "file": base + ".png"})
        except (KeyError, ValueError, OSError) as e:
            self._send(400, {"ok": False, "error": str(e)})

if __name__ == "__main__":
    BOARDS.mkdir(exist_ok=True)
    if not FEEDBACK.exists():
        FEEDBACK.write_text("[]", encoding="utf-8")
    ip = lan_ip()
    print(f"Loop Pad running:")
    print(f"  tablet  ->  http://{ip}:{PORT}/        (drawing pad)")
    print(f"  tablet  ->  http://{ip}:{PORT}/course  (Closed Loop site)")
    print(f"  boards save to: {BOARDS}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
