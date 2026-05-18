#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_pretty.py  --  Pretty exam-submission renderer for MATLAB scripts.

One command:  drives MATLAB `publish` (which RUNS the code, captures all
command-window output and saves the figures), then re-renders that output
into a clean, modern, single-file HTML + PDF suitable for handing in.

    python publish_pretty.py F25_new.m --name "Mads ..." --studentid s######

What it fixes vs. raw `publish`:
  * real MATLAB syntax highlighting (not all-green)
  * white-background figures (forced via groot defaults before publish)
  * collapsed RCOND / "matrix singular" warning spam -> one muted note
  * "% - a  - b" comment lists -> real bullet lists
  * strips internal scaffolding (paths to the solution PDF, self-score, ...)
  * modern typography, numbered sections, framed figures, A4 print CSS

Nothing here executes MATLAB code in Python -- MATLAB does the running,
Python only does the looks.
"""

from __future__ import annotations

import argparse
import base64
import datetime as _dt
import glob
import html as _html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Missing dependency. Run:  "
             '"%s" -m pip install beautifulsoup4 pygments' % sys.executable)

from pygments import highlight
from pygments.lexers import MatlabLexer
from pygments.formatters import HtmlFormatter

# --------------------------------------------------------------------------- #
#  Locating MATLAB / a Chromium browser
# --------------------------------------------------------------------------- #

def find_matlab() -> str | None:
    if os.environ.get("MATLAB_EXE") and Path(os.environ["MATLAB_EXE"]).exists():
        return os.environ["MATLAB_EXE"]
    cands = sorted(glob.glob(r"C:\Program Files\MATLAB\R20*\bin\matlab.exe"),
                   reverse=True)
    if cands:
        return cands[0]
    return shutil.which("matlab")


def find_browser() -> str | None:
    if os.environ.get("EDGE_EXE") and Path(os.environ["EDGE_EXE"]).exists():
        return os.environ["EDGE_EXE"]
    for p in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ):
        if Path(p).exists():
            return p
    return shutil.which("msedge") or shutil.which("chrome")


# --------------------------------------------------------------------------- #
#  Step 1 -- run MATLAB publish (white figures, eval code, html output)
# --------------------------------------------------------------------------- #

def run_publish(m_file: Path, matlab_exe: str) -> Path:
    """Publish m_file -> <dir>/html/<stem>.html and return that path."""
    work = m_file.parent
    # Force light/white figures globally BEFORE the published run so the
    # captured PNGs are white-background regardless of the MATLAB theme.
    # R2025a: the figure GraphicsTheme overrides groot colour defaults and
    # InvertHardcopy is ignored, so the *settings* light theme is the only
    # reliable lever. groot figure colour kept as a harmless fallback.
    groot = (
        "try, ss=settings; "
        "ss.matlab.appearance.figure.GraphicsTheme.TemporaryValue='light'; "
        "catch, end; "
        "set(groot,'defaultFigureColor','w');"
    )
    opts = ("struct('format','html','evalCode',true,'showCode',true,"
            "'maxHeight',[],'maxWidth',[],'imageFormat','png',"
            "'figureSnapMethod','print','catchError',true)")
    cmd = (
        "try, cd('%s'); %s "
        "f = publish('%s', %s); "
        "fprintf('PUBLISHED:%%s\\n', f); "
        "catch e, disp(getReport(e)); exit(1); end; exit(0);"
        % (str(work).replace("\\", "\\\\"), groot, m_file.name, opts)
    )
    print(f"  [1/3] MATLAB publish  ({m_file.name}) ... this takes ~20-40s")
    res = subprocess.run([matlab_exe, "-batch", cmd],
                         capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stdout + "\n" + res.stderr + "\n")
        raise RuntimeError("MATLAB publish failed (see output above).")
    out = work / "html" / (m_file.stem + ".html")
    if not out.exists():
        sys.stderr.write(res.stdout + "\n")
        raise RuntimeError(f"Expected {out} but it was not created.")
    return out


# --------------------------------------------------------------------------- #
#  Step 2 -- parse publish HTML and re-render
# --------------------------------------------------------------------------- #

# intro / heading lines that must never appear in a handed-in document
_SCAFFOLD = re.compile(
    r"(solution pdf|exam pdf\s*:|self-score|time target|date attempted|"
    r"filter-first|working script)", re.I)

_WARN_START = re.compile(r"^\s*Warning:", re.I)
_RCOND = re.compile(r"^\s*RCOND\s*=", re.I)


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s or "sec"


def parse_heading(raw: str):
    """-> (level, eyebrow, title, badge).  level 2 = Problem, 3 = sub."""
    raw = raw.strip()
    badge = ""
    m = re.search(r"\[([^\]]+)\]\s*$", raw)
    if m:
        badge = m.group(1).strip()
        raw = raw[:m.start()].strip()
    raw = re.sub(r"^[-\s]+|[-\s]+$", "", raw)  # strip --- wrappers

    m = re.match(r"^Problem\s+(\d+)\s*(?:--|—)?\s*(.*)$", raw, re.I)
    if m:
        return 2, f"Problem {m.group(1)}", m.group(2).strip() or raw, badge
    m = re.match(r"^(\d+)\s*-\s*(\d+)\s+(.*)$", raw)
    if m:
        return 3, f"{m.group(1)}.{m.group(2)}", m.group(3).strip(), badge
    if raw.lower().startswith("appendix"):
        rest = re.sub(r"^Appendix\s*(?:--|—)?\s*", "", raw, flags=re.I)
        return 3, "Appendix", rest.strip() or "Appendix", badge
    return 3, "", raw, badge


def bulletify(text: str):
    """'- a  - b  - c' style comment -> <ul> ; else return None."""
    t = text.strip()
    if not t.startswith("- ") and t.count(" - ") < 1:
        return None
    if not t.startswith("- "):
        return None
    parts = [p.strip() for p in re.split(r"(?:^|\s)-\s+", t) if p.strip()]
    if len(parts) < 2:
        return None
    lis = "".join(f"<li>{_html.escape(p)}</li>" for p in parts)
    return f'<ul class="task">{lis}</ul>'


def split_warnings(text: str):
    """Yield ('text', str) / ('warn', collapsed-str) segments in order."""
    lines = text.split("\n")
    i, n = 0, len(lines)
    buf = []
    while i < n:
        if _WARN_START.match(lines[i]):
            if buf:
                yield ("text", "\n".join(buf)); buf = []
            warn = []
            while i < n:
                warn.append(lines[i].strip())
                stop = _RCOND.match(lines[i])
                i += 1
                if stop:
                    break
                if i < n and lines[i].strip() == "":
                    break
            # collapse consecutive identical warnings
            count = 1
            sig = " ".join(warn)
            while i < n:
                j, blk = i, []
                if not _WARN_START.match(lines[j]):
                    break
                while j < n:
                    blk.append(lines[j].strip())
                    stop = _RCOND.match(lines[j]); j += 1
                    if stop:
                        break
                    if j < n and lines[j].strip() == "":
                        break
                if " ".join(blk) == sig:
                    count += 1; i = j
                else:
                    break
            rc = re.search(r"RCOND\s*=\s*([0-9.]+(?:[eE][+-]?\d+)?)", sig)
            msg = re.sub(r"\s+", " ", warn[0]).rstrip(".")
            extra = f" (RCOND ≈ {float(rc.group(1)):.2e})" if rc else ""
            times = f" ×{count}" if count > 1 else ""
            yield ("warn", f"{msg}{extra}{times}")
        else:
            buf.append(lines[i]); i += 1
    if buf:
        yield ("text", "\n".join(buf))


def render(html_path: Path, meta: dict, keep_intro: bool) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"),
                         "html.parser")
    content = soup.find("div", class_="content") or soup.body or soup
    img_dir = html_path.parent

    blocks = []          # rendered body fragments
    toc = []             # (level, num, title, anchor)
    fig_no = 0
    cur_section = ""
    seen_h1 = False

    for node in content.find_all(recursive=False):
        name = node.name
        cls = node.get("class") or []

        if name == "h1":
            seen_h1 = True
            continue  # replaced by the banner

        if name == "h2" and node.get_text(strip=True) == "Contents":
            continue  # we regenerate the TOC
        if name == "div" and not cls and toc == [] and not blocks:
            continue  # the original TOC container

        if name in ("h1", "h2", "h3"):
            htxt = node.get_text()
            if not keep_intro and _SCAFFOLD.search(htxt):
                continue  # the "... Working Script" title cell -> banner
            level, eyebrow, title, badge = parse_heading(htxt)
            if not title or re.fullmatch(r"(scratch|sandbox|scratch / sandbox)",
                                         title, re.I):
                cur_section = title or cur_section
                continue
            anchor = _slug(f"{eyebrow}-{title}")
            num = eyebrow if re.match(r"^\d", eyebrow) else ""
            cur_section = f"{num + ' ' if num else ''}{title}".strip()
            toc.append((level, eyebrow, title, anchor))
            b = ['<span class="badge">%s</span>' % _html.escape(badge)
                 ] if badge else []
            eb = ('<div class="eyebrow">%s</div>' % _html.escape(eyebrow)
                  ) if eyebrow else ""
            tag = "h2" if level == 2 else "h3"
            blocks.append(
                f'<section class="lvl{level}"><{tag} id="{anchor}">'
                f'{eb}<span class="htext">{_html.escape(title)}</span>'
                f'{"".join(b)}</{tag}></section>')
            continue

        if name in ("p", "ul", "ol"):
            txt = node.get_text(" ", strip=True)
            if not txt:
                continue
            if not keep_intro and _SCAFFOLD.search(txt):
                continue  # drop scaffolding: solution-PDF path, self-score…
            m = re.match(r"^\s*Svar\s*([^:]*):\s*(.*)$", txt, re.S | re.I)
            if m and name == "p":
                lead = m.group(1).strip()
                lead_html = f'<b>{_html.escape(lead)}</b> ' if lead else ""
                blocks.append(
                    '<div class="answer"><span class="atag">&#10003; Svar'
                    '</span><span class="abody">%s%s</span></div>'
                    % (lead_html, _html.escape(m.group(2))))
                continue
            ul = bulletify(txt) if name == "p" else None
            blocks.append(ul if ul else
                          f'<p class="prose">{_html.escape(txt)}</p>')
            continue

        if name == "pre" and "codeinput" in cls:
            code = node.get_text()
            code = re.sub(r"\n{3,}", "\n\n", code).strip("\n")
            if not code.strip():
                continue
            hl = highlight(code, MatlabLexer(),
                           HtmlFormatter(nowrap=True, classprefix="pg-"))
            blocks.append(
                '<div class="codecard"><div class="cap">MATLAB</div>'
                f'<pre class="code"><code>{hl}</code></pre></div>')
            continue

        if name == "pre" and "codeoutput" in cls:
            raw = node.get_text()
            if not raw.strip():
                continue
            frag = ['<div class="outcard">'
                    '<div class="cap">&#9656; output</div>']
            for kind, seg in split_warnings(raw):
                if kind == "text":
                    seg = re.sub(r"\n{3,}", "\n\n", seg).strip("\n")
                    if seg.strip():
                        frag.append('<pre class="out">%s</pre>'
                                    % _html.escape(seg))
                else:
                    frag.append('<div class="warn">&#9888; %s</div>'
                                % _html.escape(seg))
            frag.append("</div>")
            blocks.append("".join(frag))
            continue

        if name == "img" or (name == "p" and node.find("img")):
            img = node if name == "img" else node.find("img")
            src = img.get("src", "")
            f = img_dir / src
            if not f.exists():
                continue
            fig_no += 1
            b64 = base64.b64encode(f.read_bytes()).decode()
            cap = f"Figur {fig_no}"
            if cur_section:
                cap += f" &mdash; {_html.escape(cur_section)}"
            blocks.append(
                '<figure class="fig"><img src="data:image/png;base64,%s">'
                '<figcaption>%s</figcaption></figure>' % (b64, cap))
            continue

    # ---- table of contents ------------------------------------------------ #
    toc_items = []
    for level, eyebrow, title, anchor in toc:
        cls = "toc2" if level == 2 else "toc3"
        label = (f'<span class="tnum">{_html.escape(eyebrow)}</span> '
                 if eyebrow else "")
        toc_items.append(
            f'<li class="{cls}"><a href="#{anchor}">{label}'
            f'{_html.escape(title)}</a></li>')
    toc_html = ("<nav class=\"toc\"><div class=\"toc-h\">Indhold</div><ul>"
                + "".join(toc_items) + "</ul></nav>") if toc_items else ""

    return PAGE.format(
        course=_html.escape(meta["course"]),
        subtitle=_html.escape(meta["subtitle"]),
        name=_html.escape(meta["name"]),
        sid=_html.escape(meta["studentid"]),
        date=_html.escape(meta["date"]),
        toc=toc_html,
        body="\n".join(blocks),
        pg=PYGMENTS_CSS,
    )


# --------------------------------------------------------------------------- #
#  Modern-technical template
# --------------------------------------------------------------------------- #

PYGMENTS_CSS = """
.pg-k,.pg-kc,.pg-kd,.pg-kn,.pg-kp,.pg-kr,.pg-kt{color:#0b69c7;font-weight:600}
.pg-s,.pg-s1,.pg-s2,.pg-sb,.pg-sc,.pg-sd,.pg-se,.pg-sx{color:#b3261e}
.pg-c,.pg-c1,.pg-cm,.pg-cs,.pg-cp{color:#6a737d;font-style:italic}
.pg-m,.pg-mi,.pg-mf,.pg-mh,.pg-mo,.pg-il{color:#1a7f37}
.pg-o,.pg-ow{color:#7c4dff}
.pg-nf,.pg-nb,.pg-bp{color:#8250df}
.pg-err{color:#1f2328}
"""

PAGE = """<!DOCTYPE html><html lang="da"><head><meta charset="utf-8">
<title>{course} — {subtitle}</title><style>
:root{{--accent:#2563eb;--ink:#1f2328;--muted:#6a737d;--line:#e3e6ea;
--codebg:#f6f8fb;--outbg:#f4f6f8;--warnbg:#fff7e6;--warnbd:#f0c36d;}}
*{{box-sizing:border-box}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:"Segoe UI",-apple-system,Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);line-height:1.62;margin:0;font-size:13.5px;
background:#fff;font-feature-settings:"liga" 1,"kern" 1;}}
.wrap{{max-width:920px;margin:0 auto;padding:0 6mm}}
.banner{{border-left:6px solid var(--accent);background:#f3f7ff;
padding:18px 22px;margin:0 0 26px;border-radius:0 8px 8px 0}}
.banner .c{{font-size:22px;font-weight:700;letter-spacing:-.01em}}
.banner .s{{color:var(--muted);font-size:14px;margin-top:2px}}
.banner .m{{margin-top:12px;font-size:12.5px;color:#384049;
display:flex;gap:22px;flex-wrap:wrap}}
.banner .m b{{color:var(--ink);font-weight:600}}
.toc{{border:1px solid var(--line);border-radius:8px;padding:14px 20px;
margin:0 0 30px;background:#fafbfc}}
.toc-h{{font-weight:700;font-size:13px;text-transform:uppercase;
letter-spacing:.06em;color:var(--muted);margin-bottom:8px}}
.toc ul{{list-style:none;margin:0;padding:0}}
.toc li{{margin:3px 0}}.toc a{{color:var(--ink);text-decoration:none}}
.toc a:hover{{color:var(--accent)}}
.toc .toc2{{font-weight:600;margin-top:8px}}
.toc .toc3{{padding-left:20px;font-size:12.5px;color:#444}}
.toc .tnum{{color:var(--accent);font-variant-numeric:tabular-nums}}
section.lvl2 h2{{font-size:21px;margin:38px 0 4px;padding-bottom:8px;
border-bottom:2px solid var(--line);font-weight:700;letter-spacing:-.01em}}
section.lvl3 h3{{font-size:16.5px;margin:30px 0 4px;font-weight:650;
padding-left:12px;border-left:3px solid var(--accent)}}
.eyebrow{{font-size:11.5px;font-weight:700;text-transform:uppercase;
letter-spacing:.09em;color:var(--accent);margin-bottom:1px}}
.htext{{display:inline}}
.badge{{display:inline-block;margin-left:10px;font-size:10.5px;
font-weight:700;letter-spacing:.05em;color:#fff;background:var(--accent);
padding:2px 9px;border-radius:999px;vertical-align:middle;
text-transform:uppercase}}
p.prose{{margin:10px 0}}
ul.task{{margin:10px 0;padding-left:20px}}
ul.task li{{margin:4px 0}}
.answer{{margin:14px 0;padding:11px 16px 11px 14px;
background:#ecfdf3;border:1px solid #b7ebc6;
border-left:4px solid #18a957;border-radius:0 7px 7px 0}}
.answer .atag{{display:inline-block;font-size:10.5px;font-weight:700;
letter-spacing:.06em;text-transform:uppercase;color:#0f7a3d;
margin-right:10px;white-space:nowrap}}
.answer .abody{{color:#14532d}}
.answer .abody b{{color:#0f7a3d}}
.codecard{{margin:14px 0;border:1px solid var(--line);border-radius:8px;
overflow:hidden;background:var(--codebg)}}
.outcard{{margin:14px 0;border:1px solid var(--line);
border-left:3px solid #94a3b8;border-radius:6px;background:var(--outbg)}}
.cap{{font-size:10.5px;font-weight:700;letter-spacing:.07em;
text-transform:uppercase;color:var(--muted);padding:6px 14px;
border-bottom:1px solid var(--line);background:rgba(0,0,0,.015)}}
pre.code,pre.out{{margin:0;padding:13px 16px;overflow-x:auto;
font-family:"Cascadia Mono","Consolas",ui-monospace,monospace;
font-size:12px;line-height:1.55;white-space:pre;tab-size:4}}
pre.code code{{font-family:inherit}}
pre.out{{color:#262b30}}
.warn{{margin:0;padding:9px 14px;font-size:12px;color:#7a5b00;
background:var(--warnbg);border-top:1px dashed var(--warnbd);
border-bottom:1px dashed var(--warnbd);font-family:"Cascadia Mono",
"Consolas",monospace}}
.warn:first-child{{border-top:0}}
figure.fig{{margin:20px 0;text-align:center;background:#fff;
border:1px solid var(--line);border-radius:8px;padding:14px;
box-shadow:0 1px 3px rgba(16,24,40,.06)}}
figure.fig img{{max-width:100%;height:auto;border-radius:4px}}
figure.fig figcaption{{margin-top:9px;font-size:12px;color:var(--muted);
font-style:italic}}
.footer{{display:none}}
@page{{size:A4;margin:17mm 15mm}}
@media print{{
 body{{font-size:11.5px}} .wrap{{max-width:none;padding:0}}
 .toc a{{color:var(--ink)}}
 section.lvl2,section.lvl3{{break-after:avoid}}
 .codecard,.outcard,figure.fig,ul.task{{break-inside:avoid}}
 .toc{{break-inside:avoid}}
}}
{pg}
</style></head><body><div class="wrap">
<header class="banner">
<div class="c">{course}</div>
<div class="s">{subtitle}</div>
<div class="m"><span><b>{name}</b></span><span>{sid}</span>
<span>{date}</span></div>
</header>
{toc}
<main>
{body}
</main>
</div></body></html>"""


# --------------------------------------------------------------------------- #
#  Step 3 -- HTML -> PDF via headless Edge/Chrome
# --------------------------------------------------------------------------- #

def _free_target(pdf_file: Path) -> Path:
    """Return a writable PDF path. If the canonical one is locked (open in a
    viewer / held by Defender), fall back to a timestamped name so we never
    leave a stale file or hard-fail."""
    try:
        if pdf_file.exists():
            pdf_file.unlink()
        return pdf_file
    except (PermissionError, OSError):
        alt = pdf_file.with_name(
            f"{pdf_file.stem}_{_dt.datetime.now():%H%M%S}{pdf_file.suffix}")
        print(f"  !  {pdf_file.name} is locked (open in a viewer?) "
              f"-> writing {alt.name} instead")
        return alt


def to_pdf(html_file: Path, pdf_file: Path, browser: str) -> Path | None:
    tmp = tempfile.mkdtemp(prefix="pp_edge_")
    try:
        r = None
        for flag in ("--headless=new", "--headless"):
            target = _free_target(pdf_file)   # re-resolve each attempt
            cmd = [browser, flag, "--disable-gpu", "--no-first-run",
                   "--no-default-browser-check", f"--user-data-dir={tmp}",
                   "--no-pdf-header-footer", "--print-to-pdf-no-header",
                   "--virtual-time-budget=12000",
                   f"--print-to-pdf={target}", html_file.as_uri()]
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=120)
            if target.exists() and target.stat().st_size > 1000:
                return target
        sys.stderr.write(((r.stdout or "") + (r.stderr or "")) if r else "")
        return None
    except Exception as e:                       # noqa: BLE001
        sys.stderr.write(f"PDF step failed: {e}\n")
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
#  CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render a MATLAB script into a pretty submission "
                    "(HTML + PDF) via MATLAB publish.")
    ap.add_argument("script", help="path to the .m file (e.g. F25_new.m)")
    ap.add_argument("--name", default="Mads Rudolph", help="your full name")
    ap.add_argument("--studentid", default="s246132", help="study number")
    ap.add_argument("--course", default="", help="override course banner")
    ap.add_argument("--subtitle", default="",
                    help="override subtitle (default: derived from filename)")
    ap.add_argument("--no-matlab", action="store_true",
                    help="skip publish, reuse existing html/<stem>.html")
    ap.add_argument("--no-pdf", action="store_true", help="HTML only")
    ap.add_argument("--keep-intro", action="store_true",
                    help="keep the leading scaffolding comment block")
    ap.add_argument("--open", action="store_true",
                    help="open the resulting PDF when done")
    a = ap.parse_args()

    src = Path(a.script)
    if not src.is_absolute():
        for cand in (Path.cwd() / src,
                     Path(__file__).parent / src,
                     Path(__file__).parent / "EXAMS" / src):
            if cand.exists():
                src = cand
                break
    src = src.resolve()
    if not src.exists():
        return _err(f"Script not found: {src}")

    pub = src.parent / "html" / (src.stem + ".html")

    if a.no_matlab:
        if not pub.exists():
            return _err(f"--no-matlab set but {pub} does not exist. "
                        "Run MATLAB publish first.")
        print(f"  [1/3] Reusing existing publish output: {pub.name}")
    else:
        mexe = find_matlab()
        if not mexe:
            return _err("Could not find matlab.exe. Set MATLAB_EXE or use "
                        "--no-matlab after publishing manually.")
        try:
            pub = run_publish(src, mexe)
        except RuntimeError as e:
            if pub.exists():
                print(f"  !  {e}\n     Falling back to existing {pub.name}")
            else:
                return _err(str(e))

    course = a.course or "62743 Digital Signal Processing"
    subtitle = a.subtitle or f"{src.stem.split('_')[0].upper()} eksamen — kommenteret aflevering"
    meta = {
        "course": course,
        "subtitle": subtitle,
        "name": a.name,
        "studentid": a.studentid,
        "date": _dt.date.today().strftime("%d. %B %Y"),
    }

    print("  [2/3] Re-rendering (Pygments + modern template)")
    pretty_html = pub.parent / (src.stem + "_pretty.html")
    pretty_html.write_text(render(pub, meta, a.keep_intro), encoding="utf-8")

    if a.no_pdf:
        print(f"\n  Done.  ->  {pretty_html}")
        return 0

    browser = find_browser()
    pdf = pub.parent / (src.stem + "_pretty.pdf")
    if not browser:
        print(f"\n  HTML written: {pretty_html}")
        print("  No Edge/Chrome found for PDF. Open the HTML and Ctrl+P -> "
              "Save as PDF (the print stylesheet is A4-ready).")
        return 0
    print(f"  [3/3] PDF via {Path(browser).stem}")
    out_pdf = to_pdf(pretty_html, pdf, browser)
    if out_pdf:
        print(f"\n  Done.\n   HTML : {pretty_html}\n   PDF  : {out_pdf}")
        if a.open:
            os.startfile(out_pdf)        # noqa: SLF001  (Windows-only)
    else:
        print(f"\n  HTML written ({pretty_html}) but PDF export failed.")
        print("  Open the HTML and Ctrl+P -> Save as PDF instead.")
    return 0


def _err(msg: str) -> int:
    sys.stderr.write(f"\n  ERROR: {msg}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
