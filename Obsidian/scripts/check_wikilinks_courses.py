import re, sys, unicodedata
from pathlib import Path

VAULT = Path(".").resolve()
COURSES = {
    "Electromagnetics": VAULT / "Courses" / "Electromagnetics",
    "DSP": VAULT / "Courses" / "DSP",
    "Integrated Analog Electronics": VAULT / "Courses" / "Integrated Analog Electronics",
}
VALID_EXTS = {".md", ".pdf", ".png", ".jpg", ".jpeg", ".gif"}
LINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]]+)?\]\]")

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return s.replace("–", "-").strip()

def resolve_in_course(course_root: Path, target: str):
    target = norm(target)
    p = course_root / target
    if p.exists():
        return p
    for ext in VALID_EXTS:
        if (p.with_suffix(ext)).exists():
            return p.with_suffix(ext)
    name = Path(target).name
    for cand in course_root.rglob("*"):
        if cand.is_file() and cand.suffix.lower() in VALID_EXTS:
            if norm(cand.stem) == norm(Path(name).stem) or norm(cand.name) == norm(name):
                return cand
    return None

def which_course(path: Path):
    for cname, root in COURSES.items():
        try:
            path.relative_to(root)
            return cname
        except ValueError:
            continue
    return None

def main():
    broken, cross = [], []
    for cname, root in COURSES.items():
        for md in root.rglob("*.md"):
            txt = md.read_text(encoding="utf-8", errors="ignore")
            for m in LINK_RE.finditer(txt):
                raw = m.group(1)
                target = norm(raw)
                if target.startswith("Courses/"):
                    tgt_path = (VAULT / target)
                    if not tgt_path.exists():
                        broken.append((md, f"[[{raw}]] (missing absolute path)"))
                        continue
                    src_course = which_course(md)
                    dst_course = which_course(tgt_path)
                    if src_course and dst_course and src_course != dst_course:
                        cross.append((md, raw, src_course, dst_course))
                    continue
                tgt = resolve_in_course(root, target)
                if tgt is None:
                    dst = None
                    dst_course_name = None
                    for oname, oroot in COURSES.items():
                        if oname == cname:
                            continue
                        cand = resolve_in_course(oroot, target)
                        if cand:
                            dst, dst_course_name = cand, oname
                            break
                    if dst:
                        cross.append((md, raw, cname, dst_course_name))
                    else:
                        broken.append((md, f"[[{raw}]]"))
    if cross:
        print("\nCROSS-COURSE LINKS (likely mistakes):")
        for md, raw, src, dst in cross:
            print(f"- {md}: [[{raw}]]  ({src} → {dst})")
    if broken:
        print("\nBROKEN LINKS:")
        for md, raw in broken:
            print(f"- {md}: {raw}")
        sys.exit(1)
    else:
        print("\nAll links OK within courses.")

if __name__ == "__main__":
    main()
