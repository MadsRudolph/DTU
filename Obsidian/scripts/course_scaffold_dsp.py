#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSP Course Scaffold & Migrator (Obsidian-ready)

CLI:
  python scripts/course_scaffold_dsp.py --course "Courses/DSP" [--dry-run] [--migrate] [--backup]

What it does (idempotent, UTF-8 LF):
- Creates/refreshes numbered topic folders + Examples/ subfolders.
- Creates/updates top-level MOC: "Courses/DSP/MOC – DSP.md".
  * Maintains a Core Topics table strictly between:
    <!-- AUTO-CORE-TOPICS START --> ... <!-- AUTO-CORE-TOPICS END -->
  * Preserves everything else.
- Creates/refreshes sub-MOCs for each numbered topic folder with correct YAML schema.
- Ensures auxiliary folders: Exercises/Solved, Slides, Literature, Images.
- Creates global templates in Templates/Courses/dsp/{Formula.md, Example.md, Lab.md, SlideNotes.md}.
- Optional migration (--migrate):
  * filename?topic heuristics tailored to DSP (see mapping below).
  * --dry-run previews moves; --backup copies originals into a timestamped backup under the course.
  * Writes "Courses/DSP/MIGRATION_REPORT.md".
- Prints JSON summary to stdout:
  { "created_paths":[], "updated":[], "moved":[], "backed_up":[], "skipped":[], "warnings":[], "failed":[], "renamed":[] }
"""

import argparse, json, os, re, shutil, sys, datetime, pathlib, unicodedata

COURSE_SLUG = "dsp"
COURSE_TITLE = "DSP"
AUTO_START = "<!-- AUTO-CORE-TOPICS START -->"
AUTO_END   = "<!-- AUTO-CORE-TOPICS END -->"

TOPICS = [
    "00-Quick-Reference",
    "01-Fundamentals",
    "02-Sampling-and-Quantization",
    "03-Discrete-Time-Systems",
    "04-Convolution-and-LTI",
    "05-Transforms-DTFT-DFT",
    "06-Z-Transform-and-ROC",
    "07-FIR-Filters",
    "08-IIR-Filters",
    "09-Multirate-and-Polyphase",
    "10-Applications-and-Labs",
]

EXTRA_DIRS = [
    "Exercises/Solved",
    "Slides",
    "Literature",
    "Images",
]

def sanitize_name(s: str) -> str:
    # Normalize unicode and replace odd characters
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("�", "–").replace("&", "and")
    # Disallow path separators / \ and reserved characters
    s = s.replace("/", "-").replace("\\", "-").replace(":", " -")
    s = re.sub(r'[<>|?*"]', "", s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s

def lf_write(path, text):
    text = text.replace("\r\n","\n").replace("\r","\n")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def yaml_block(title, typ, tags):
    updated = datetime.date.today().isoformat()
    return (
f"""---
title: {title}
type: {typ}
tags: [{COURSE_SLUG}{(',' if tags else '')}{(', '.join(tags))}]
aliases: []
links: {{"formulas": [], "related": []}}
updated: {updated}
---
"""
    )

def ensure_topic_folders(course_path, summary):
    for t in TOPICS:
        t_dir = os.path.join(course_path, t)
        ex_dir = os.path.join(t_dir, "Examples")
        for p in (t_dir, ex_dir):
            if not os.path.isdir(p):
                os.makedirs(p, exist_ok=True)
                summary["created_paths"].append(p)
        pretty = t.split("-", 1)[1].replace("-", " ") if "-" in t else t
        moc_filename = sanitize_name(f"MOC – {pretty}.md")
        existing_moc = None
        if os.path.isdir(t_dir):
            for cand in os.listdir(t_dir):
                if cand.lower().startswith("moc"):
                    existing_moc = os.path.join(t_dir, cand)
                    break
        moc_path = existing_moc or os.path.join(t_dir, moc_filename)
        if not os.path.exists(moc_path):
            lf_write(moc_path, yaml_block(pretty, "moc", ["topic"]) + f"# {pretty}\n\n- Add notes here.\n")
            summary["created_paths"].append(moc_path)
        else:
            with open(moc_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r"(updated:\s*)(\d{4}-\d{2}-\d{2})", r"\g<1>"+datetime.date.today().isoformat(), content)
            lf_write(moc_path, content)
            summary["updated"].append(moc_path)

def ensure_extra_dirs(course_path, summary):
    for rel in EXTRA_DIRS:
        p = os.path.join(course_path, rel)
        if not os.path.isdir(p):
            os.makedirs(p, exist_ok=True)
            summary["created_paths"].append(p)

def render_core_topics_table():
    rows = ["| # | Topic | Folder | MOC |", "|---:|---|---|---|"]
    for t in TOPICS:
        num, name = t.split("-",1)
        name_hr = name.replace("-", " ")
        folder = f"{t}/"
        moc_rel = f"{t}/MOC – {name_hr}.md"
        rows.append(f"| {num} | {name_hr} | [[{folder}]] | [[{moc_rel}]] |")
    return "\n".join(rows)

def upsert_top_moc(course_path, summary):
    moc_path = os.path.join(course_path, f"MOC – {COURSE_TITLE}.md")
    header = yaml_block(COURSE_TITLE, "moc", ["course"])
    auto_block = "\n".join([AUTO_START, render_core_topics_table(), AUTO_END])

    if not os.path.exists(moc_path):
        body = f"# {COURSE_TITLE}\n\n{auto_block}\n\n> Keep your own notes below."
        lf_write(moc_path, header + body)
        summary["created_paths"].append(moc_path)
        return

    with open(moc_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        content = re.sub(r"(updated:\s*)(\d{4}-\d{2}-\d{2})", r"\g<1>"+datetime.date.today().isoformat(), content)
    if AUTO_START in content and AUTO_END in content:
        pre, rest = content.split(AUTO_START, 1)
        mid, post = rest.split(AUTO_END, 1)
        new_content = pre + AUTO_START + "\n" + render_core_topics_table() + "\n" + AUTO_END + post
        lf_write(moc_path, new_content)
        summary["updated"].append(moc_path)
    else:
        new_content = header + "# " + COURSE_TITLE + "\n\n" + auto_block + "\n\n" + content
        lf_write(moc_path, new_content)
        summary["updated"].append(moc_path)

def ensure_templates(root, summary):
    base = os.path.join(root, "Templates", "Courses", COURSE_SLUG)
    os.makedirs(base, exist_ok=True)
    templates = {
        "Formula.md": ("formula", "# Formula\n\n- Statement:\n- Derivation:\n- Notes:\n"),
        "Example.md": ("example", "# Example\n\n- Problem:\n- Solution:\n- Checks:\n"),
        "Lab.md": ("lab", "# Lab\n\n- Objective:\n- Setup:\n- Procedure:\n- Results:\n- Discussion:\n"),
        "SlideNotes.md": ("slides", "# Slide Notes\n\n- Lecture:\n- Key points:\n- Questions:\n"),
    }
    for fname, (typ, body) in templates.items():
        p = os.path.join(base, fname)
        front = yaml_block(fname.replace(".md",""), typ, ["template"])
        if not os.path.exists(p):
            lf_write(p, front + body)
            summary["created_paths"].append(p)
        else:
            with open(p, "r", encoding="utf-8") as f:
                t = f.read()
            t = re.sub(r"(updated:\s*)(\d{4}-\d{2}-\d{2})", r"\g<1>"+datetime.date.today().isoformat(), t)
            lf_write(p, t)
            summary["updated"].append(p)

def guess_target(course_path, name, is_pdf):
    clean = sanitize_name(name)
    s = clean.lower()
    normalized = s.replace("–", "-")

    special_map = {
        "fiir and iir.md": "08-IIR-Filters",
        "week 3 - thursday.md": "06-Z-Transform-and-ROC",
        "week 3 - tuesday.md": "05-Transforms-DTFT-DFT",
        "week 2 - thursday.md": "05-Transforms-DTFT-DFT",
        "week 2 - tuesday.md": "03-Discrete-Time-Systems",
        "week 1 - thursday.md": "01-Fundamentals",
        "week 1 - tuesday.md": "01-Fundamentals",
    }
    if normalized in special_map:
        return os.path.join(course_path, special_map[normalized], clean)

    # Slides / PDFs
    if is_pdf and any(k in s for k in ("lecture", "slides", "week", "uge")):
        return os.path.join(course_path, "Slides", clean)

    # Heuristics for topic placement (root of topic, not Examples)
    rules = [
        (("fir","kaiser","window","parks-mcclellan","linear phase"), "07-FIR-Filters"),
        (("iir","butterworth","chebyshev","elliptic","bilinear","impulse invariance","fiir"), "08-IIR-Filters"),
        (("z-transform","z transform","roc","region of convergence","stability via poles","z-transform","z- transform"), "06-Z-Transform-and-ROC"),
        (("dtft","dft","fft","spectrum","leakage","zero padding","zero-pad","zeropad","frequency domain"), "05-Transforms-DTFT-DFT"),
        (("sampling","aliasing","quantization","snr","bit depth"), "02-Sampling-and-Quantization"),
        (("lti","impulse response","convolution sum","bibo","superposition"), "04-Convolution-and-LTI"),
        (("difference equation","system function","causality","state-space","difference eq"), "03-Discrete-Time-Systems"),
        (("fundamentals","intro","notation","properties","signals"), "01-Fundamentals"),
    ]

    for keys, topic in rules:
        if any(k in s for k in keys):
            return os.path.join(course_path, topic, clean)

    if any(k in s for k in ("lab","application")):
        return os.path.join(course_path, "10-Applications-and-Labs", clean)
    if any(k in s for k in ("assignment","exercise","opgave")):
        return os.path.join(course_path, "Exercises", "Solved", clean)

    # Default parking for formulas without clear mapping
    return os.path.join(course_path, "00-Quick-Reference", clean)

def perform_migration(course_path, dry_run=False, do_backup=False, summary=None):
    report = []
    candidates = []
    seen = set()

    # Always consider existing Formulas/ as legacy sources
    formulas_dir = os.path.join(course_path, "Formulas")
    if os.path.isdir(formulas_dir):
        for root, _, files in os.walk(formulas_dir):
            for fn in files:
                if fn.startswith("."):
                    continue
                lower_fn = fn.lower()
                if lower_fn.startswith("moc"):
                    continue
                if lower_fn == "migration_report.md":
                    continue
                path = os.path.join(root, fn)
                if path not in seen:
                    candidates.append(path)
                    seen.add(path)
    for d in ("Legacy","legacy","_legacy","."):
        base = os.path.join(course_path, d)
        if not os.path.isdir(base):
            continue
        for root,_,files in os.walk(base):
            for fn in files:
                if fn.startswith("."): continue
                lower_fn = fn.lower()
                if lower_fn.startswith("moc"):
                    continue
                if lower_fn == "migration_report.md":
                    continue
                rel_root = os.path.relpath(root, course_path)
                top_segment = rel_root.split(os.sep)[0]
                if top_segment.startswith("_backup_migration"):
                    continue
                if top_segment in TOPICS + ["Exercises","Slides","Literature","Images","Formulas","Lecture Notes"]:
                    continue
                path = os.path.join(root, fn)
                if path not in seen:
                    candidates.append(path)
                    seen.add(path)
    if not candidates:
        report.append("No legacy files found.")
    backup_dir = None
    if do_backup and candidates:
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = os.path.join(course_path, f"_backup_migration_{stamp}")
        os.makedirs(backup_dir, exist_ok=True)
        summary["created_paths"].append(backup_dir)
        report.append(f"Backup directory: {os.path.relpath(backup_dir, course_path)}")
    for src in candidates:
        rel = os.path.relpath(src, course_path)
        name = os.path.basename(src)
        is_pdf = name.lower().endswith(".pdf")
        dest = guess_target(course_path, name, is_pdf)
        dest = os.path.join(os.path.dirname(dest), sanitize_name(os.path.basename(dest)))
        action = f"{rel} -> {os.path.relpath(dest, course_path)}"
        if dry_run:
            report.append(f"[DRY-RUN] {action}")
            summary["warnings"].append(f"Dry-run: {action}")
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if do_backup and backup_dir:
                bpath = os.path.join(backup_dir, rel)
                os.makedirs(os.path.dirname(bpath), exist_ok=True)
                shutil.copy2(src, bpath)
                summary["backed_up"].append(rel)
            shutil.move(src, dest)
            summary["moved"].append(action)
            report.append(f"MOVED {action}")
    mr_path = os.path.join(course_path, "MIGRATION_REPORT.md")
    lf_write(mr_path, "\n".join(report)+"\n")
    summary["created_paths"].append(mr_path)
    return mr_path

def update_auto_related(course_path, summary):
    # For each topic folder, list .md files (excluding the MOC) as related formulas
    for t in sorted(x for x in os.listdir(course_path) if re.match(r"^\d{2}-", x)):
        t_dir = os.path.join(course_path, t)
        if not os.path.isdir(t_dir):
            continue
        moc = None
        for cand in os.listdir(t_dir):
            if cand.lower().startswith("moc"):
                moc = os.path.join(t_dir, cand)
                break
        if not moc or not os.path.isfile(moc):
            continue
        items = []
        for f in sorted(os.listdir(t_dir)):
            if not f.lower().endswith(".md"):
                continue
            if f.lower().startswith("moc"):
                continue
            items.append(f" - [[{t}/{f}]]")
        with open(moc, "r", encoding="utf-8") as fh:
            content = fh.read()
        related_block = "\n".join([
            "<!-- AUTO-RELATED START -->",
            "## Related formulas",
            *(items or ["_None found_"]),
            "<!-- AUTO-RELATED END -->"
        ])
        if "<!-- AUTO-RELATED START -->" in content and "<!-- AUTO-RELATED END -->" in content:
            pre, rest = content.split("<!-- AUTO-RELATED START -->", 1)
            _, post = rest.split("<!-- AUTO-RELATED END -->", 1)
            new = pre + related_block + post
        else:
            new = content.rstrip() + "\n\n" + related_block + "\n"
        lf_write(moc, new)
        summary["updated"].append(moc)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--course", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--migrate", action="store_true")
    ap.add_argument("--backup", action="store_true")
    args = ap.parse_args()

    course_path = os.path.abspath(args.course)
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    summary = {k: [] for k in ["created_paths","updated","moved","backed_up","skipped","warnings","failed","renamed"]}

    if not os.path.isdir(course_path):
        summary["failed"].append(f"Course path not found: {course_path}")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 1

    ensure_topic_folders(course_path, summary)
    ensure_extra_dirs(course_path, summary)
    upsert_top_moc(course_path, summary)
    # Repair any accidental '�' in filenames under the course (safe rename)
    for walk_root, _, files in os.walk(course_path):
        for fn in files:
            new_name = fn
            if "�" in new_name:
                new_name = new_name.replace("�", "–")
            if new_name.startswith("MOC -"):
                new_name = new_name.replace("MOC -", "MOC –", 1)
            if new_name == fn:
                continue
            src = os.path.join(walk_root, fn)
            dst = os.path.join(walk_root, new_name)
            rel_src = os.path.relpath(src, course_path)
            rel_dst = os.path.relpath(dst, course_path)
            if not os.path.exists(dst):
                os.replace(src, dst)
                summary["renamed"].append(f"{rel_src} -> {rel_dst}")
            else:
                try:
                    if os.path.getmtime(src) > os.path.getmtime(dst):
                        os.replace(src, dst)
                        summary["renamed"].append(f"{rel_src} -> {rel_dst}")
                    else:
                        os.remove(src)
                        summary["warnings"].append(f"Removed duplicate during rename: {rel_src}")
                except Exception as exc:
                    summary["warnings"].append(f"Rename failed for {rel_src}: {exc}")
    ensure_templates(str(repo_root), summary)
    if args.migrate:
        perform_migration(course_path, dry_run=args.dry_run, do_backup=args.backup, summary=summary)
    update_auto_related(course_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
