"""Loop Pad — LAN whiteboard server for oral-exam derivation practice.

Serves:
  /            the S-Pen drawing app (app.html)
  /course      the Closed Loop crash-course page (../Closed-Loop.html) with a pad link injected
  POST /api/save      {id,title,png,strokes} -> boards/<date>/<HHMMSS>_<slug>.png + .json
  GET  /api/feedback  -> feedback.json (list; the reviewing Claude session appends entries)
  GET  /api/boards    -> list of saved boards (newest first)

Feedback entry schema (append to feedback.json; the app polls every 5 s):
  {"board": "<png filename>", "time": "HH:MM", "verdict": "correct|partly|wrong",
   "notes": ["..."],
   "svg": "<optional SVG fragment in the PIXEL COORDINATES OF THAT BOARD PNG>",
   "imgW": <width of the png you annotated>, "imgH": <height>}

  The svg fragment is placed in the coordinate system of the exported PNG itself:
  (0,0) is its top-left corner, (imgW,imgH) its bottom-right. Read the png, note its
  real pixel size, annotate against that, and pass imgW/imgH so the app can rescale
  if it ever differs. There is NO fixed board size - the canvas is infinite and every
  export is auto-cropped to the drawing, so each png has its own dimensions.

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
from urllib.parse import quote, unquote

HERE = Path(__file__).resolve().parent
BOARDS = HERE / "boards"
FEEDBACK = HERE / "feedback.json"
COURSE = HERE.parent / "Closed-Loop.html"
BLOCKS = HERE.parent / "blocks.html"
# the vault: /opt/vault on the container, the real folder when run from the repo
def _find_vault():
    if Path("/opt/vault").is_dir():
        return Path("/opt/vault")
    for base in HERE.parents:                      # walk up to the repo root
        cand = base / "Obsidian" / "Courses" / "34722 Linear Control Design 1"
        if cand.is_dir():
            return cand
    return Path("/opt/vault")                      # missing: /notes just 404s
VAULT = _find_vault()
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


# Same stacked-fraction typesetter the course page uses, so the vault notes read
# as real maths instead of "x/(s+1)" strings.
FRAC_JS = """<script>
(function(){
var MATHY=/[0-9∂ωζθτγπφΩαβ²³√]/;
var TOKEN_END=/[\\w·√ζωθτγπφΩαβ⁰¹²³⁴⁵⁶⁷⁸⁹.'*]+$/;
function bF(s,i){var d=0;for(var k=i;k<s.length;k++){if(s[k]==="(")d++;else if(s[k]===")"){d--;if(!d)return k;}}return -1;}
function bB(s,i){var d=0;for(var k=i;k>=0;k--){if(s[k]===")")d++;else if(s[k]==="("){d--;if(!d)return k;}}return -1;}
function subify(frag,text){
  var re=/([A-Za-z0-9ωζθτγπφΩ])_([A-Za-z0-9]{1,3})(?![\\w])/g,last=0,m;
  while((m=re.exec(text))){frag.appendChild(document.createTextNode(text.slice(last,m.index)+m[1]));
    var sb=document.createElement("sub");sb.className="msub";sb.textContent=m[2];frag.appendChild(sb);last=re.lastIndex;}
  frag.appendChild(document.createTextNode(text.slice(last)));}
function transform(text){
  var i=text.indexOf("/(");if(i<0)return null;
  var close=bF(text,i+1);if(close<0)return null;
  var den=text.slice(i+2,close),numStart,num;
  if(text[i-1]===")"){var open=bB(text,i-1);if(open<0)return null;numStart=open;num=text.slice(open+1,i-1);}
  else{var mm=TOKEN_END.exec(text.slice(0,i));if(!mm||!mm[0])return null;numStart=i-mm[0].length;num=mm[0];}
  if(!num.trim()||!den.trim())return null;
  var frag=document.createDocumentFragment(),before=text.slice(0,numStart);
  var r1=transform(before);if(r1)frag.appendChild(r1);else subify(frag,before);
  var f=document.createElement("span");f.className="frac";
  var n=document.createElement("span");n.className="fnum";
  var d=document.createElement("span");d.className="fden";
  subify(n,num);subify(d,den);f.appendChild(n);f.appendChild(d);frag.appendChild(f);
  var after=text.slice(close+1),r2=transform(after);
  if(r2)frag.appendChild(r2);else subify(frag,after);
  return frag;}
function run(){
  var w=document.createTreeWalker(document.querySelector("main")||document.body,NodeFilter.SHOW_TEXT,{
    acceptNode:function(n){var p=n.parentNode;if(!p)return NodeFilter.FILTER_REJECT;
      var t=p.nodeName;if(t==="SCRIPT"||t==="STYLE"||t==="CODE"||t==="PRE")return NodeFilter.FILTER_REJECT;
      if(n.nodeValue.indexOf("$")>=0)return NodeFilter.FILTER_REJECT;
      if(p.closest&&p.closest(".katex,details.tex"))return NodeFilter.FILTER_REJECT;
      if(p.closest&&p.closest(".frac"))return NodeFilter.FILTER_REJECT;
      return (n.nodeValue.indexOf("/(")>=0&&MATHY.test(n.nodeValue))?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP;}});
  var nodes=[],n;while((n=w.nextNode()))nodes.push(n);
  nodes.forEach(function(tn){try{var f=transform(tn.nodeValue);if(f)tn.parentNode.replaceChild(f,tn);}catch(e){}});}
window.addEventListener("load",function(){setTimeout(run,60)});
})();
</script>"""

KATEX = ("<link rel=stylesheet "
         "href='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css'>"
         "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>"
         "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js' "
         "onload=\"renderMathInElement(document.body,{delimiters:["
         "{left:'$$',right:'$$',display:true},"
         "{left:'$',right:'$',display:false}],throwOnError:false})\"></script>")

NOTE_CSS = """
:root{--bg:#0D1220;--panel:#151C2E;--line:#2A3450;--ink:#E4E9F1;--sub:#8E9BAE;--amber:#F0A03C;--cyan:#4FC4D4}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,sans-serif}
.top{position:sticky;top:0;display:flex;gap:10px;align-items:center;padding:10px 16px;
     background:var(--panel);border-bottom:1px solid var(--line);z-index:5}
.top a{color:var(--cyan);text-decoration:none;font-weight:700;white-space:nowrap}
.top input{flex:1;min-width:90px;background:var(--bg);border:1px solid var(--line);
           border-radius:8px;color:var(--ink);padding:8px 11px;font:15px system-ui}
main{max-width:820px;margin:0 auto;padding:22px 18px 80px}
h1,h2,h3{line-height:1.25}h1{font-size:27px;margin:.2em 0 .6em}
h2{font-size:21px;margin:1.5em 0 .5em;color:var(--amber)}h3{font-size:17px;margin:1.2em 0 .4em}
a{color:var(--cyan)}code{background:#0a0f1a;padding:1px 5px;border-radius:5px;font-size:.92em}
pre{background:#0a0f1a;padding:12px 14px;border-radius:10px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{border-left:3px solid var(--amber);margin:1em 0;padding:.2em 0 .2em 14px;color:var(--sub)}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;font-size:14.5px}
th{background:var(--panel)}
img{max-width:100%;height:auto;border-radius:8px}
ul.idx{list-style:none;padding:0}ul.idx li{border-bottom:1px solid var(--line)}
ul.idx a{display:block;padding:11px 4px;text-decoration:none}
ul.idx li.fold{color:var(--sub);font-size:12.5px;padding:14px 4px 4px;border:0}
.frac{display:inline-flex;flex-direction:column;align-items:center;vertical-align:-.35em;
      margin:0 .18em;line-height:1.15;font-size:.95em;text-align:center}
.frac>.fden{border-top:1px solid currentColor;padding:0 .25em}
.frac>.fnum{padding:0 .25em}
sub.msub{font-size:.72em}
blockquote.cal{border-left:3px solid var(--cyan);background:rgba(79,196,212,.07);
  border-radius:0 10px 10px 0;padding:10px 14px;color:var(--ink)}
blockquote.cal .calh{font-weight:700;color:var(--cyan);text-transform:uppercase;
  letter-spacing:.6px;font-size:12.5px;margin-bottom:4px}
blockquote.cal-warning{border-color:var(--amber);background:rgba(240,160,60,.07)}
blockquote.cal-warning .calh{color:var(--amber)}
details.tex{margin:12px 0;border:1px solid var(--line);border-radius:10px;padding:8px 12px}
details.tex summary{cursor:pointer;color:var(--sub);font-size:13.5px}
details.tex pre{margin-top:8px}
.katex{font-size:1.03em}
"""


def html_escape(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace("'", "&#39;").replace('"', "&quot;"))


def note_page(title, body):
    return ("<!DOCTYPE html><html lang=en><head><meta charset=UTF-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            "<title>" + html_escape(title) + "</title>" + KATEX + "<style>" + NOTE_CSS + "</style></head><body>"
            "<div class=top><a href='/'>&#9997; Pad</a><a href='/course'>&#128216; Course</a>"
            "<a href='/blocks'>&#129513; Blocks</a>"
            "<a href='/notes'>&#128218; Notes</a>"
            "<input id=q placeholder='filter notes'></div>"
            "<main>" + body + "</main>"
            "<script>var q=document.getElementById('q');"
            "if(document.querySelector('ul.idx')){q.addEventListener('input',function(){"
            "var v=q.value.toLowerCase();document.querySelectorAll('ul.idx li').forEach(function(li){"
            "li.style.display=li.textContent.toLowerCase().indexOf(v)<0?'none':''})})}"
            "else{q.style.display='none'}</script>" + FRAC_JS + "</body></html>")



CALLOUT_RE = re.compile(r"<blockquote>\s*<p>\[!(\w+)\][ ]*([^\n<]*)")
TEX_RE = re.compile(
    r"<pre><code class=\"language-(tikz|latex|tex)\">(.*?)</code></pre>", re.S)

def polish(html):
    """Make vault-flavoured markdown readable: Obsidian callouts become real
    callout boxes, and TikZ/LaTeX source (which we cannot draw) folds away
    instead of burying the note in backslashes."""
    def cal(m):
        kind = m.group(1).lower()
        cls = "cal cal-warning" if kind in ("warning", "danger", "caution", "attention") else "cal"
        head = m.group(2).strip() or kind
        return ('<blockquote class="' + cls + '"><p class="calh">' + head + "</p><p>")
    html = CALLOUT_RE.sub(cal, html)
    html = TEX_RE.sub(
        lambda m: ('<details class="tex"><summary>LaTeX source (' + m.group(1)
                   + ") - not drawn here</summary><pre><code>" + m.group(2)
                   + "</code></pre></details>"), html)
    return html

def vault_notes():
    if not VAULT.is_dir():
        return []
    return sorted(VAULT.rglob("*.md"), key=lambda p: p.relative_to(VAULT).as_posix().lower())


def wikilinks(md, notes):
    """Resolve [[Note]] and ![[image.png]] into real links before markdown runs."""
    by_stem = {p.stem.lower(): p for p in notes}

    def img(m):
        name = m.group(1).split("|")[0].strip()
        return "![" + name + "](/notes/raw/" + quote(name) + ")"

    def link(m):
        target, _, label = m.group(1).partition("|")
        target = target.split("#")[0].strip()
        text = (label or target).strip()
        hit = by_stem.get(target.lower())
        if not hit:
            return text
        return "[" + text + "](/notes/" + quote(hit.relative_to(VAULT).as_posix()) + ")"

    md = re.sub(r"!\[\[([^\]]+)\]\]", img, md)
    return re.sub(r"\[\[([^\]]+)\]\]", link, md)


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
        elif self.path.startswith("/blocks"):
            self._send(200, BLOCKS.read_bytes(), "text/html; charset=utf-8")
        elif self.path.startswith("/notes"):
            self.serve_notes()
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
        elif self.path.startswith("/api/board?"):
            name = unquote(self.path.split("file=", 1)[1]) if "file=" in self.path else ""
            hit = None
            if name and "/" not in name and "\\" not in name and BOARDS.exists():
                for p in BOARDS.rglob(Path(name).stem + ".json"):
                    hit = p
                    break
            if not hit:
                return self._send(404, {"error": "no such board"})
            self._send(200, json.loads(hit.read_text(encoding="utf-8")))
        elif self.path.startswith("/api/boards"):
            out = []
            if BOARDS.exists():
                for p in sorted(BOARDS.rglob("*.json"), reverse=True):
                    try:
                        meta = json.loads(p.read_text(encoding="utf-8"))
                        out.append({"file": p.with_suffix(".png").name,
                                    "title": meta.get("title", ""), "day": p.parent.name,
                                    "qid": meta.get("qid", ""), "saved": meta.get("saved", ""),
                                    "strokes": meta.get("strokes", 0),
                                    "reopenable": bool(meta.get("vec"))})
                    except (OSError, json.JSONDecodeError):
                        pass
            self._send(200, out[:50])
        else:
            self._send(404, {"error": "not found"})

    def serve_notes(self):
        notes = vault_notes()
        rel = unquote(self.path[len("/notes"):]).lstrip("/").split("?")[0]
        if not rel:
            items, last = [], None
            for p in notes:
                r = p.relative_to(VAULT)
                fold = r.parent.as_posix()
                fold = "" if fold == "." else fold
                if fold != last:
                    items.append("<li class=fold>" + html_escape(fold or "top level") + "</li>")
                    last = fold
                items.append("<li><a href='/notes/" + quote(r.as_posix()) + "'>"
                             + html_escape(p.stem) + "</a></li>")
            body = ("<h1>34722 notes</h1><p style='color:#8E9BAE'>" + str(len(notes))
                    + " notes straight from the vault - filter them with the box above.</p>"
                    "<ul class=idx>" + "".join(items) + "</ul>")
            return self._send(200, note_page("34722 notes", body).encode("utf-8"),
                              "text/html; charset=utf-8")
        if rel.startswith("raw/"):
            name = rel[4:]
            for cand in VAULT.rglob("*"):
                if cand.is_file() and cand.name == name:
                    ext = cand.suffix.lower().lstrip(".")
                    ctype = "image/jpeg" if ext in ("jpg", "jpeg") else "image/" + (ext or "png")
                    return self._send(200, cand.read_bytes(), ctype)
            return self._send(404, {"error": "no such asset"})
        target = (VAULT / rel).resolve()
        if not str(target).startswith(str(VAULT.resolve())) or not target.is_file():
            return self._send(404, {"error": "no such note"})
        raw = target.read_text(encoding="utf-8")
        if raw.startswith("---"):
            end = raw.find("\n---", 3)
            if end > 0:
                raw = raw[end + 4:]
        try:
            import markdown as _md
            body = polish(_md.markdown(wikilinks(raw, notes),
                                       extensions=["tables", "fenced_code", "sane_lists"]))
        except ImportError:
            body = "<pre>" + html_escape(raw) + "</pre>"
        page = "<h1>" + html_escape(target.stem) + "</h1>" + body
        self._send(200, note_page(target.stem, page).encode("utf-8"), "text/html; charset=utf-8")

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
            vec = payload.get("vec") or []
            meta = {"title": payload.get("title", ""), "id": payload.get("id", ""),
                    "saved": datetime.now().isoformat(timespec="seconds"),
                    "strokes": payload.get("strokes", 0),
                    "qid": payload.get("qid", ""), "prompt": payload.get("prompt", ""),
                    "vec": vec}
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
