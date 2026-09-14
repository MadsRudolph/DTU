#!/usr/bin/env python3
"""Build dist/ from src/: inline the KaTeX stylesheet with its fonts as data
URIs so the page is a self-contained bundle (index.html + style.css + app.js +
katex.min.js) that works from a plain file://, from nginx, and as a Claude
artifact, with no external font or stylesheet requests."""
import base64, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent
SRC, DIST, KATEX = ROOT / "src", ROOT / "dist", ROOT / "vendor" / "katex"

css = (KATEX / "katex.min.css").read_text()
# keep only the woff2 sources we vendored; drop woff/ttf fallbacks entirely
def font_src(m):
    name = m.group(1)
    f = KATEX / "fonts" / f"KaTeX_{name}.woff2"
    if not f.exists():
        return "src:local('KaTeX_missing')"
    b64 = base64.b64encode(f.read_bytes()).decode()
    return f"src:url(data:font/woff2;base64,{b64}) format('woff2')"
css = re.sub(r"src:url\(fonts/KaTeX_([A-Za-z0-9-]+)\.woff2\) format\(\"woff2\"\)(,url\([^)]*\) format\(\"[a-z]+\"\))*", font_src, css)

DIST.mkdir(exist_ok=True)
html = (SRC / "index.html").read_text()
html = html.replace("<!-- KATEX_CSS -->", f"<style>{css}</style>")
(DIST / "index.html").write_text(html)
# artifact flavour: the Claude Artifact host wraps the file in its own
# doctype/html/head/body skeleton, so strip ours and keep only what goes inside
inner = re.search(r"<head>(.*?)</head>\s*<body>(.*)</body>", html, re.S)
head = re.sub(r"<meta (charset|name=\"viewport\")[^>]*>", "", inner.group(1))
(DIST / "artifact.html").write_text(head.strip() + "\n" + inner.group(2).strip() + "\n")
for name in ("style.css", "app.js", "benches.js", "labs.js", "problems.js", "diagrams.js", "quiz.js"):
    shutil.copy(SRC / name, DIST / name)
shutil.copy(KATEX / "katex.min.js", DIST / "katex.min.js")
(DIST / ".assetsignore").write_text("artifact.html\n")  # Cloudflare upload skips the artifact flavour
# manifest: the served files, so the LAN mirror (CT 116) can pull the public site
import json, hashlib, time
served = ["index.html", "style.css", "app.js", "benches.js", "labs.js", "problems.js", "diagrams.js", "quiz.js", "katex.min.js"]
(DIST / "manifest.json").write_text(json.dumps({"built": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "files": {f: hashlib.sha256((DIST / f).read_bytes()).hexdigest() for f in served}}, indent=1))
print("built", DIST, "index.html", (DIST / "index.html").stat().st_size // 1024, "KB")
