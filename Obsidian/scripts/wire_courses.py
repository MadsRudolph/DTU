import re
import sys
import shutil
from datetime import date
from pathlib import Path

VAULT_ROOT = Path('.')

COURSE_CFG = {
    "Electromagnetics": {
        "nav": "> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]\n",
        "qr_formulas": "> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane Waves]] · [[MOC – Transmission Lines]] · [[MOC – EM Loss & Skin Depth]]\n",
        "qr_exercises": "> **Quick refs:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · [[MOC – Plane Waves]] · [[MOC – EM Loss & Skin Depth]]\n",
        "autofix": {}
    },
    "DSP": {
        "nav": "> 🔗 [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]] · [[Formulas/Week 3 – Tuesday]]\n",
        "qr_formulas": "> **Quick refs (DSP):** [[MOC – DSP]] · [[MOC – Lectures (DSP)]] · [[MOC – Exercises (DSP)]]\n",
        "qr_exercises": "> **Quick refs (DSP):** [[Formulas/Week 1 – Tuesday]] · [[Formulas/Week 2 – Tuesday]] · [[Formulas/Week 3 – Tuesday]]\n",
        "autofix": {
            "Formulas/Plane Waves & Power — Quick Formula Sheet": "Formulas/Week 3 – Tuesday",
            "MOC – Electromagnetics": "MOC – DSP",
            "MOC – Lectures": "MOC – Lectures (DSP)",
            "MOC – Exercises": "MOC – Exercises (DSP)"
        }
    },
    "Integrated Analog Electronics": {
        "nav": "> 🔗 [[MOC – IAE]] · [[MOC – Lectures (IAE)]] · [[MOC – Exercises (IAE)]] · [[Lecture Notes/MOS transistor basics]]\n",
        "qr_formulas": "> **Quick refs (IAE):** [[MOC – IAE]] · [[MOC – Lectures (IAE)]] · [[MOC – Exercises (IAE)]]\n",
        "qr_exercises": "> **Quick refs (IAE):** [[Lecture Notes/MOS transistor basics]] · [[Formulas]]\n",
        "autofix": {
            "Formulas/Plane Waves & Power — Quick Formula Sheet": "Lecture Notes/MOS transistor basics",
            "MOC – Electromagnetics": "MOC – IAE",
            "MOC – Lectures": "MOC – Lectures (IAE)",
            "MOC – Exercises": "MOC – Exercises (IAE)"
        }
    }
}


def write_text_if_changed(course_root: Path, p: Path, content: str) -> bool:
    old = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else None
    if old != content:
        # Backup previous content if under course_root
        try:
            if old is not None and course_root in p.resolve().parents:
                ts = date.today().strftime('%Y%m%d')
                backup_root = course_root / '.backups' / ts
                rel = p.resolve().relative_to(course_root)
                backup_path = backup_root / rel
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(old, encoding='utf-8')
        except Exception:
            pass
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return True
    return False


def has_frontmatter(txt: str) -> bool:
    return txt.lstrip().startswith('---\n')


def split_frontmatter(txt: str):
    if not has_frontmatter(txt):
        return None, None, txt
    start = txt.find('---\n')
    if start != 0:
        return None, None, txt
    end_idx = txt.find('\n---\n', 4)
    if end_idx == -1:
        return None, None, txt
    fm = txt[0:end_idx+5]
    rest = txt[end_idx+5:]
    return fm, fm, rest


def detect_type(course_root: Path, md_path: Path) -> str:
    base = course_root.resolve()
    rel = str(md_path.resolve().relative_to(base)).replace('\\', '/')
    name = md_path.name
    if 'Formulas/' in rel:
        return 'formula'
    if 'Lecture Notes/' in rel:
        return 'lecture'
    if 'Exercises/work/' in rel:
        return 'assignment' if 'home assignment' in name.lower() else 'exercise'
    if 'Exercises/LAB/' in rel:
        return 'lab'
    if name.startswith('MOC – '):
        return 'moc'
    return 'lecture'


def guess_topic(md_path: Path) -> str:
    base = md_path.stem.lower()
    for kw, label in [
        ('filter', 'Filters'),
        ('frequency', 'Frequency Response'),
        ('fourier', 'Fourier'),
        ('z-transform', 'Z-Transform'),
        ('mos', 'MOSFET'),
        ('amplifier', 'Amplifiers'),
    ]:
        if kw in base:
            return label
    return 'General'


def build_frontmatter(course_name: str, title: str, ftype: str, topic: str) -> str:
    today = date.today().strftime('%Y-%m-%d')
    fm = (
        '---\n'
        f'title: "{title}"\n'
        f'type: "{ftype}"\n'
        'tags:\n'
        f'- {course_name}\n'
        f'- {ftype}\n'
        f'- {topic}\n'
        'aliases: []\n'
        'links:\n'
        '  formulas: []\n'
        '  related: []\n'
        f'updated: "{today}"\n'
        '---\n'
    )
    return fm


def ensure_top_nav(course_name: str, body: str) -> str:
    nav = f'> 🔗 [[MOC – {course_name}]] · [[MOC – Lectures]] · [[MOC – Exercises]]\n'
    if nav.strip() in body:
        return body
    return nav + '\n' + body.lstrip('\n')


def ensure_footer(course_name: str, txt: str) -> str:
    sig = f'**See also:** [[MOC – {course_name}]]'
    if sig in txt:
        return txt
    return txt.rstrip() + f"\n---\n\n{sig}\n"


def insert_quick_refs(course_name: str, md_path: Path, body: str) -> tuple[str, int]:
    inserted = 0
    rel = str(md_path).replace('\\', '/')
    def insert(block: str, body: str) -> tuple[str, int]:
        if block.strip() in body:
            return body, 0
        # put after top nav if present
        nav = f'> 🔗 [[MOC – {course_name}]]'
        if nav in body:
            body = body.replace(nav + ' · [[MOC – Lectures]] · [[MOC – Exercises]]\n', nav + ' · [[MOC – Lectures]] · [[MOC – Exercises]]\n' + block)
        else:
            body = block + '\n' + body
        return body, 1

    if 'Formulas/' in rel:
        block = f'> **Quick refs:** [[MOC – {course_name}]] · [[MOC – Lectures]] · [[MOC – Exercises]]\n'
        body, n = insert(block, body); inserted += n
    if 'Exercises/work/' in rel:
        block = f'> **Quick refs:** [[MOC – {course_name}]] · [[MOC – Exercises]] · [[MOC – Lectures]]\n'
        body, n = insert(block, body); inserted += n
    return body, inserted


def ensure_top_nav_cfg(course_name: str, body: str) -> str:
    cfg = COURSE_CFG.get(course_name, {})
    nav = cfg.get("nav", f'> 🔗 [[MOC – {course_name}]] · [[MOC – Lectures]] · [[MOC – Exercises]]\n')
    if nav.strip() in body:
        return body
    body = re.sub(r"^> 🔗 \[\[MOC – .*?\]\].*\n\n?", "", body, flags=re.MULTILINE)
    return nav + "\n" + body.lstrip("\n")


def insert_quick_refs_cfg(course_name: str, md_path: Path, body: str) -> tuple[str, int]:
    cfg = COURSE_CFG.get(course_name, {})
    rel = str(md_path).replace('\\', '/')
    inserted = 0

    def insert(block: str, body: str) -> tuple[str, int]:
        if not block or block.strip() in body:
            return body, 0
        lines = body.splitlines(True)
        for idx, line in enumerate(lines):
            if line.startswith("> 🔗 "):
                lines.insert(idx+1, block + "\n")
                return "".join(lines), 1
        return block + "\n" + body, 1

    if 'Formulas/' in rel:
        body, n = insert(cfg.get("qr_formulas", ""), body); inserted += n
    if 'Exercises/work/' in rel:
        body, n = insert(cfg.get("qr_exercises", ""), body); inserted += n
    return body, inserted


def scrub_cross_course_links(course_name: str, txt: str) -> str:
    fixes = COURSE_CFG.get(course_name, {}).get("autofix", {})
    for wrong, right in fixes.items():
        txt = txt.replace(f"[[{wrong}]]", f"[[{right}]]")
    return txt

def normalize_questions_and_solutions(course_root: Path, md_path: Path, body: str) -> tuple[str, int]:
    lines = body.splitlines()
    q_sections = []
    q_re = re.compile(r'^(#+)\s*(?:Q(?:uestion)?\s*(\d+))\b', re.IGNORECASE)
    for i, line in enumerate(lines):
        m = q_re.match(line)
        if m:
            num = int(m.group(2))
            lines[i] = f'## Q{num}'
            q_sections.append((i, num))
    sol_links_added = 0
    for i, num in q_sections:
        target = f'→ Solution: [[Solutions/{md_path.stem} Solutions#Q{num}]]'
        if not any('→ Solution:' in l and f'#Q{num}]' in l for l in lines[i+1:i+4]):
            lines.insert(i+1, target)
            sol_links_added += 1
    new_body = '\n'.join(lines)
    if q_sections:
        # place solution file under Exercises/work/Solutions relative to course
        sol_dir = course_root / 'Exercises' / 'work' / 'Solutions'
        sol_dir.mkdir(parents=True, exist_ok=True)
        sol_file = sol_dir / f'{md_path.stem} Solutions.md'
        existing = sol_file.exists()
        s_lines = (sol_file.read_text(encoding='utf-8', errors='ignore').splitlines() if existing else [f'# {md_path.stem} — Solutions'])
        for _, num in q_sections:
            hdr = f'## Q{num}'
            if not any(line.strip() == hdr for line in s_lines):
                s_lines.append(hdr)
                s_lines.append(f'← Back: [[../{md_path.stem}#Q{num}]]')
                s_lines.append('')
        sol_content = '\n'.join(s_lines).rstrip() + '\n'
        write_text_if_changed(course_root, sol_file, sol_content)
    return new_body, sol_links_added


def append_dataview_hubs(course_name: str, course_root: Path, txt: str) -> tuple[str, int]:
    count = 0
    recent_sig = 'WHERE file.folder = this.file.folder AND file.name != this.file.name'
    outgoing_sig = 'LIST FROM outgoing([[]])'
    need_recent = recent_sig not in txt
    need_out = outgoing_sig not in txt
    if need_recent or need_out:
        parts = []
        if need_recent:
            parts.append(
                'Recent in same folder\n\n'
                '```dataview\n'
                f'LIST FROM "{course_root.as_posix()}"\n'
                'WHERE file.folder = this.file.folder AND file.name != this.file.name\n'
                'SORT file.mtime desc\n'
                'LIMIT 5\n'
                '```\n'
            )
            count += 1
        if need_out:
            parts.append(
                'Outgoing links\n\n'
                '```dataview\n'
                'LIST FROM outgoing([[]])\n'
                f'WHERE contains(file.path,"{course_root.as_posix()}")\n'
                '```\n'
            )
            count += 1
        txt = txt.rstrip() + '\n\n' + '\n\n'.join(parts)
    return txt, count


def create_mocs(course_name: str, course_root: Path) -> list[str]:
    created = []
    moc_root = course_root / f'MOC – {course_name}.md'
    content_root = (
        f'# MOC – {course_name}\n'
        '## Course flow\n'
        '- [[MOC – Lectures]]\n'
        '- [[MOC – Exercises]]\n'
        '- [[MOC – Assignments]]\n'
        '- [[MOC – Lab]]\n\n'
        '## Recently updated (Dataview)\n'
        '```dataview\n'
        f'LIST FROM "{course_root.as_posix()}"\n'
        'WHERE file.mtime >= date(today) - dur(14 days)\n'
        'SORT file.mtime desc\n'
        'LIMIT 12\n'
        '```\n'
    )
    if not moc_root.exists():
        if write_text_if_changed(course_root, moc_root, content_root):
            created.append(str(moc_root))

    mocs = {
        'MOC – Lectures.md': (
            '# MOC – Lectures\n\n'
            '```dataview\n'
            f'LIST FROM "{(course_root / "Lecture Notes").as_posix()}"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Exercises.md': (
            '# MOC – Exercises\n\n'
            '```dataview\n'
            f'LIST FROM "{(course_root / "Exercises").as_posix()}"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Assignments.md': (
            '# MOC – Assignments\n\n'
            '```dataview\n'
            f'LIST FROM "{(course_root / "Exercises").as_posix()}"\n'
            'WHERE contains(file.name, "Home Assignment")\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Lab.md': (
            '# MOC – Lab\n\n'
            '```dataview\n'
            f'LIST FROM "{(course_root / "Exercises" / "LAB").as_posix()}"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
    }
    for fname, content in mocs.items():
        p = course_root / fname
        if p.exists():
            continue
        if write_text_if_changed(course_root, p, content):
            created.append(str(p))
    return created


def image_hygiene(course_root: Path, course_counts: dict) -> int:
    moved = 0
    imgs_dir = course_root / 'Images'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(r'!\[\[([^\]|#]+\.png)\]\]')
    for md in course_root.rglob('*.md'):
        txt = md.read_text(encoding='utf-8', errors='ignore')
        embeds = pattern.findall(txt)
        changed_txt = txt
        for fn in embeds:
            if fn.lower().startswith(course_root.as_posix().lower() + '/images/'):
                continue
            if not fn.lower().startswith('pasted image'):
                continue
            src = VAULT_ROOT / fn
            if src.exists() and src.is_file():
                dest = imgs_dir / src.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(src), str(dest))
                    moved += 1
                except Exception:
                    pass
                changed_txt = changed_txt.replace(f'![[{fn}]]', f'![[{(course_root / "Images" / src.name).as_posix()}]]')
        if changed_txt != txt:
            md.write_text(changed_txt, encoding='utf-8')
            course_counts['md_updated'] += 1
    return moved


def process_course(course_name: str, course_root: Path) -> dict:
    # Ensure dirs
    (course_root / 'Lecture Notes').mkdir(parents=True, exist_ok=True)
    (course_root / 'Exercises' / 'work' / 'Solutions').mkdir(parents=True, exist_ok=True)
    (course_root / 'Images').mkdir(parents=True, exist_ok=True)

    created_mocs = create_mocs(course_name, course_root)
    md_updated = 0
    quick_refs_inserted = 0
    sol_links_added = 0
    hubs_added_total = 0

    for md in course_root.rglob('*.md'):
        if md.name.startswith('MOC – '):
            continue
        orig = md.read_text(encoding='utf-8', errors='ignore')
        txt = orig
        fm, _, body = split_frontmatter(txt)
        if fm is None:
            # title
            m = re.search(r'^#\s+(.+)$', body, flags=re.MULTILINE)
            title = m.group(1).strip() if m else md.stem
            ftype = detect_type(course_root, md)
            topic = guess_topic(md)
            fm_new = build_frontmatter(course_name, title, ftype, topic)
            body = body.lstrip('\n')
            txt = fm_new + body
        else:
            txt = fm + body
        fm2, _, body2 = split_frontmatter(txt)
        if fm2 is not None:
            body2 = ensure_top_nav_cfg(course_name, body2)
            txt = fm2 + body2
        else:
            txt = ensure_top_nav_cfg(course_name, txt)

        # Quick refs
        if fm2 is not None:
            body3 = txt[len(fm2):]
            body3, ins = insert_quick_refs_cfg(course_name, md, body3)
            quick_refs_inserted += ins
            txt = fm2 + body3
        else:
            txt, ins = insert_quick_refs_cfg(course_name, md, txt)
            quick_refs_inserted += ins

        # Exercise links
        base = course_root.resolve()
        rel = str(md.resolve().relative_to(base)).replace('\\', '/')
        if 'Exercises/work/' in rel:
            fm3, _, body4 = split_frontmatter(txt)
            new_body4, added = normalize_questions_and_solutions(course_root, md, body4)
            sol_links_added += added
            txt = (fm3 or '') + new_body4

        # Footer
        txt = ensure_footer(course_name, txt)

        # Hubs
        txt, hubs = append_dataview_hubs(course_name, course_root, txt)
        hubs_added_total += hubs

        # Scrub obvious cross-course links (e.g., EM links inside DSP/IAE)
        txt = scrub_cross_course_links(course_name, txt)

        if txt != orig:
            md.write_text(txt, encoding='utf-8')
            md_updated += 1

    images_moved = image_hygiene(course_root, {'md_updated': md_updated})

    return {
        'course': course_name,
        'mocs': created_mocs,
        'md_updated': md_updated,
        'quick_refs': quick_refs_inserted,
        'sol_links': sol_links_added,
        'images_moved': images_moved,
    }


def main():
    courses = [
        ('DSP', VAULT_ROOT / 'Courses' / 'DSP'),
        ('Integrated Analog Electronics', VAULT_ROOT / 'Courses' / 'Integrated Analog Electronics'),
    ]
    summaries = []
    for name, root in courses:
        if not root.exists():
            print(f'Skipping missing course: {name} ({root})')
            continue
        print(f'Processing course: {name}')
        res = process_course(name, root)
        summaries.append(res)

    print('--- Summary ---')
    for s in summaries:
        print(f"Course: {s['course']}")
        print(f"  Markdown files updated: {s['md_updated']}")
        if s['mocs']:
            print('  MOCs created:')
            for m in s['mocs']:
                print(f'   - {m}')
        else:
            print('  MOCs created: 0')
        print(f"  Quick refs inserted: {s['quick_refs']}")
        print(f"  Q<->A links added: {s['sol_links']}")
        print(f"  Images moved: {s['images_moved']}")


if __name__ == '__main__':
    main()
