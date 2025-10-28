import re, sys, pathlib
ROOT = pathlib.Path("Courses/Electromagnetics")
bad = []
for md in ROOT.rglob("*.md"):
    txt = md.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"\[\[([^\]|#]+)(#[^\]]+)?\]\]", txt):
        target = m.group(1).strip()
        hits = [p for p in ROOT.rglob("*.md") if p.stem == target or p.name == target + ".md"]
        if not hits:
            bad.append((str(md), m.group(0)))
if bad:
    for f, lk in bad:
        print(f"Broken link in {f}: {lk}")
    sys.exit(1)
