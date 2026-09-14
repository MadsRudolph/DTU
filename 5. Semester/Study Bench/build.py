#!/usr/bin/env python3
"""Build dist/ for the Study Bench: a hub page at the root and one self-contained
site per course under dist/<code>/ (core toolkit + KaTeX inlined with data-URI
fonts + the course's own files). Also writes dist/<code>/artifact.html (no
html/head/body skeleton, for publishing as a Claude artifact), dist/.assetsignore
and dist/manifest.json (for the LAN mirror on CT 116)."""
import base64, hashlib, json, pathlib, re, shutil, time

ROOT = pathlib.Path(__file__).resolve().parent
CORE, COURSES, HUB, DIST, KATEX = ROOT / "core", ROOT / "courses", ROOT / "hub", ROOT / "dist", ROOT / "vendor" / "katex"

css = (KATEX / "katex.min.css").read_text()
def font_src(m):
    f = KATEX / "fonts" / f"KaTeX_{m.group(1)}.woff2"
    if not f.exists():
        return "src:local('KaTeX_missing')"
    return f"src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2')"
css = re.sub(r"src:url\(fonts/KaTeX_([A-Za-z0-9-]+)\.woff2\) format\(\"woff2\"\)(,url\([^)]*\) format\(\"[a-z]+\"\))*", font_src, css)
KATEX_STYLE = f"<style>{css}</style>"

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

# hub
shutil.copy(HUB / "index.html", DIST / "index.html")

# courses
for cdir in sorted(p for p in COURSES.iterdir() if p.is_dir()):
    out = DIST / cdir.name
    out.mkdir()
    for f in ("app.js", "style.css"):
        shutil.copy(CORE / f, out / f)
    shutil.copy(KATEX / "katex.min.js", out / "katex.min.js")
    for f in cdir.iterdir():
        if f.suffix in (".js", ".css", ".svg", ".png") and f.name != "index.html":
            shutil.copy(f, out / f.name)
    html = (cdir / "index.html").read_text().replace("<!-- KATEX_CSS -->", KATEX_STYLE)
    (out / "index.html").write_text(html)
    inner = re.search(r"<head>(.*?)</head>\s*<body>(.*)</body>", html, re.S)
    head = re.sub(r"<meta (charset|name=\"viewport\")[^>]*>", "", inner.group(1))
    (out / "artifact.html").write_text(head.strip() + "\n" + inner.group(2).strip() + "\n")
    print("built", cdir.name, (out / "index.html").stat().st_size // 1024, "KB")

(DIST / ".assetsignore").write_text("artifact.html\n")  # Cloudflare upload skips the artifact flavour
served = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file() and p.name not in ("artifact.html", ".assetsignore", "manifest.json"))
(DIST / "manifest.json").write_text(json.dumps({"built": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "files": {f: hashlib.sha256((DIST / f).read_bytes()).hexdigest() for f in served}}, indent=1))
print("manifest:", len(served), "files")
