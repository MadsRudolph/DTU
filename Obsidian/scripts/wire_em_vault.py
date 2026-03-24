import re
import sys
import shutil
from datetime import date
from pathlib import Path

VAULT_ROOT = Path('.')
COURSE_ROOT = VAULT_ROOT / 'Courses' / 'Electromagnetics'


def ensure_dirs():
    (COURSE_ROOT / 'Lecture Notes').mkdir(parents=True, exist_ok=True)
    (COURSE_ROOT / 'Exercises' / 'work' / 'Solutions').mkdir(parents=True, exist_ok=True)
    (COURSE_ROOT / 'Images').mkdir(parents=True, exist_ok=True)


def read_text(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def write_text_if_changed(p: Path, content: str) -> bool:
    old = p.read_text(encoding='utf-8', errors='ignore') if p.exists() else None
    if old != content:
        # Backup previous content if under COURSE_ROOT
        try:
            if old is not None and COURSE_ROOT in p.resolve().parents:
                ts = date.today().strftime('%Y%m%d')
                backup_root = COURSE_ROOT / '.backups' / ts
                rel = p.resolve().relative_to(COURSE_ROOT)
                backup_path = backup_root / rel
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_path.write_text(old, encoding='utf-8')
        except Exception:
            pass
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return True
    return False


def detect_type(md_path: Path) -> str:
    pstr = str(md_path).replace('\\', '/')
    name = md_path.name
    if 'Formulas/' in pstr:
        return 'formula'
    if 'Lecture Notes/' in pstr:
        return 'lecture'
    if 'Exercises/work/' in pstr:
        return 'assignment' if 'home assignment' in name.lower() else 'exercise'
    if 'Exercises/LAB/' in pstr:
        return 'lab'
    if name.startswith('MOC – '):
        return 'moc'
    return 'lecture'


TOPIC_KEYWORDS = [
    ('plane waves', 'Plane Waves'),
    ('transmission', 'Transmission Lines'),
    ('polarization', 'Polarization'),
    ('skin depth', 'Skin Depth'),
    ('loss', 'EM Loss & Skin Depth'),
]


def guess_topic(md_path: Path) -> str:
    base = md_path.stem.lower()
    for kw, label in TOPIC_KEYWORDS:
        if kw in base:
            return label
    pstr = str(md_path).lower().replace('\\', '/')
    for kw, label in TOPIC_KEYWORDS:
        if kw in pstr:
            return label
    return 'General'


def has_frontmatter(txt: str) -> bool:
    return txt.lstrip().startswith('---\n')


def split_frontmatter(txt: str):
    if not has_frontmatter(txt):
        return None, None, txt
    start = txt.find('---\n')
    if start != 0:
        return None, None, txt
    # find closing --- on its own line
    end_idx = txt.find('\n---\n', 4)
    if end_idx == -1:
        # frontmatter not closed properly; treat as none
        return None, None, txt
    fm = txt[0:end_idx+5]
    rest = txt[end_idx+5:]
    return fm, fm, rest


def build_frontmatter(title: str, ftype: str, topic: str) -> str:
    today = date.today().strftime('%Y-%m-%d')
    tags_line = f'- Electromagnetics\n  - {ftype}\n  - {topic}'
    fm = (
        '---\n'
        f'title: "{title}"\n'
        f'type: "{ftype}"\n'
        'tags:\n'
        f'{tags_line}\n'
        'aliases: []\n'
        'links:\n'
        '  formulas: []\n'
        '  related: []\n'
        f'updated: "{today}"\n'
        '---\n'
    )
    return fm


TOP_NAV = (
    '> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · '
    '[[Formulas/Plane Waves & Power — Quick Formula Sheet]]\n'
)

FOOTER_BLOCK = (
    '\n---\n\n**See also:** [[MOC – Electromagnetics]] · '
    '[[Formulas/Plane Waves & Power — Quick Formula Sheet]]\n'
)


def ensure_top_nav(txt_after_fm: str) -> str:
    if TOP_NAV.strip() in txt_after_fm:
        return txt_after_fm
    return TOP_NAV + '\n' + txt_after_fm.lstrip('\n')


def ensure_footer(txt: str) -> str:
    if '**See also:** [[MOC – Electromagnetics]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]' in txt:
        return txt
    return txt.rstrip() + FOOTER_BLOCK


def insert_quick_refs(md_path: Path, body: str) -> tuple[str, int]:
    inserted = 0
    pstr = str(md_path).replace('\\', '/')
    # Choose the block based on type/path
    if 'Formulas/' in pstr:
        block = (
            '> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane Waves]] · '
            '[[MOC – Transmission Lines]] · [[MOC – EM Loss & Skin Depth]]\n'
        )
        if block.strip() not in body:
            # insert after TOP_NAV if present else at top
            if TOP_NAV.strip() in body:
                body = body.replace(TOP_NAV, TOP_NAV + block)
            else:
                body = block + '\n' + body
            inserted += 1
    if 'Exercises/work/' in pstr:
        block = (
            '> **Quick refs:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · '
            '[[MOC – Plane Waves]] · [[MOC – EM Loss & Skin Depth]]\n'
        )
        if block.strip() not in body:
            if TOP_NAV.strip() in body:
                body = body.replace(TOP_NAV, TOP_NAV + block)
            else:
                body = block + '\n' + body
            inserted += 1
    if 'Lecture Notes/Untitled.md' in pstr.replace('\\', '/'):
        l1 = '> **This lecture uses:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · [[Formulas/Wave Parameters]]\n'
        l2 = '> **Try next:** [[Exercises/work/Home Assignment 1]] · [[Exercises/work/3-3.2]]\n'
        if l1.strip() not in body:
            if TOP_NAV.strip() in body:
                body = body.replace(TOP_NAV, TOP_NAV + l1 + l2)
            else:
                body = l1 + l2 + '\n' + body
            inserted += 2
    return body, inserted


def normalize_questions_and_solutions(md_path: Path, body: str, solutions_dir: Path):
    # Find question sections: headings starting with ## and containing Q or Question + number
    lines = body.splitlines()
    q_sections = []  # list of (idx, level, qnum)
    q_re = re.compile(r'^(#+)\s*(?:Q(?:uestion)?\s*(\d+))\b', re.IGNORECASE)
    for i, line in enumerate(lines):
        m = q_re.match(line)
        if m:
            lvl = len(m.group(1))
            num = int(m.group(2))
            # Normalize heading to '## Q<num>' at level 2
            lines[i] = '## Q{}'.format(num)
            q_sections.append((i, 2, num))

    # Insert solution link after each question heading
    sol_links_added = 0
    for i, lvl, num in q_sections:
        target = f'→ Solution: [[Solutions/{md_path.stem} Solutions#Q{num}]]'
        insert_pos = i + 1
        if insert_pos < len(lines) and target in lines[insert_pos]:
            continue
        # If immediate next line already contains a Solution link, skip
        found_existing = any('→ Solution:' in l and f'#Q{num}]' in l for l in lines[i+1:i+4])
        if not found_existing:
            lines.insert(insert_pos, target)
            sol_links_added += 1

    new_body = '\n'.join(lines)

    # Ensure Solutions file exists and has sections
    if q_sections:
        sol_file = solutions_dir / f'{md_path.stem} Solutions.md'
        existing = sol_file.exists()
        s_txt = read_text(sol_file)
        if not existing:
            s_lines = [f'# {md_path.stem} — Solutions']
        else:
            s_lines = s_txt.splitlines()

        for _, _, num in q_sections:
            hdr = f'## Q{num}'
            if not any(line.strip() == hdr for line in s_lines):
                s_lines.append(hdr)
                s_lines.append(f'← Back: [[../{md_path.stem}#Q{num}]]')
                s_lines.append('')
        s_new = '\n'.join(s_lines).rstrip() + '\n'
        write_text_if_changed(sol_file, s_new)

    return new_body, sol_links_added


def standardize_q9_polarization(body: str) -> tuple[str, int]:
    # Heuristic: If a section includes the phrase 'linear polarization' and contains list items with vectors,
    # replace that list with the specified table.
    lines = body.splitlines()
    changed = 0
    i = 0
    while i < len(lines):
        if re.match(r'^##+\s+.*', lines[i]):
            # scan section until next heading
            j = i + 1
            mentions = False
            list_start, list_end = None, None
            while j < len(lines) and not re.match(r'^##+\s+.*', lines[j]):
                if 'linear polarization' in lines[j].lower():
                    mentions = True
                if re.match(r'\s*[-\d][\).]\s*\(?[-0-9jJi,\s]+\)?', lines[j]):
                    if list_start is None:
                        list_start = j
                    list_end = j
                j += 1
            if mentions and list_start is not None and list_end is not None:
                table = [
                    '| Option | $\\mathbf E_0$ | $E_x=0$? | Linear? | Conclusion |',
                    '|:--:|:--|:--:|:--:|:--|',
                    '| 1 | $(0,1+j,0)$ | Yes | Single component | ✅ Valid |',
                    '| 2 | $(0,1,-j)$ | Yes | Phase shift → elliptical | ❌ |',
                    '| 3 | $(0,0,-2)$ | Yes | Single component | ✅ Valid |',
                    '| 4 | $(0,-j,j2)$ | Yes | Ratio $(-j)/(j2)=-\\tfrac12$ real | ✅ Valid |',
                    '| 5 | $(-1,0,2)$ | No | — | ❌ |',
                    '| 6 | $(1,0,0)$ | No (parallel) | — | ❌ |',
                ]
                lines[list_start:list_end+1] = table
                changed += 1
                i = list_start + len(table)
            else:
                i = j
        else:
            i += 1
    return '\n'.join(lines), changed


def append_dataview_hubs(txt: str) -> tuple[str, int]:
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
                'LIST FROM "Courses/Electromagnetics"\n'
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
                'WHERE contains(file.path,"Courses/Electromagnetics")\n'
                '```\n'
            )
            count += 1
        txt = txt.rstrip() + '\n\n' + '\n\n'.join(parts)
    return txt, count


def create_mocs() -> list[str]:
    created = []
    # MOC – Electromagnetics (exact content per spec)
    moc_root = COURSE_ROOT / 'MOC – Electromagnetics.md'
    moc_root_content = (
        '# MOC – Electromagnetics\n'
        '## Core topic maps\n'
        '- [[MOC – Plane Waves]]\n'
        '- [[MOC – Transmission Lines]]\n'
        '- [[MOC – Polarization]]\n'
        '- [[MOC – EM Loss & Skin Depth]]\n\n'
        '## Quick access\n'
        '- [[Formulas/Plane Waves & Power — Quick Formula Sheet]]\n\n'
        '## Course flow\n'
        '- [[MOC – Lectures]]\n'
        '- [[MOC – Exercises]]\n'
        '- [[MOC – Assignments]]\n'
        '- [[MOC – Lab]]\n\n'
        '## Recently updated (Dataview)\n'
        '```dataview\n'
        'LIST FROM "Courses/Electromagnetics"\n'
        'WHERE file.mtime >= date(today) - dur(14 days)\n'
        'SORT file.mtime desc\n'
        'LIMIT 12\n'
        '```\n'
    )
    if not moc_root.exists():
        if write_text_if_changed(moc_root, moc_root_content):
            created.append(str(moc_root))

    # Reasonable templates for other MOCs (since exact content not provided)
    mocs = {
        'MOC – Lectures.md': (
            '# MOC – Lectures\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics/Lecture Notes"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Exercises.md': (
            '# MOC – Exercises\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics/Exercises/work"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Assignments.md': (
            '# MOC – Assignments\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics/Exercises/work"\n'
            'WHERE contains(file.name, "Home Assignment")\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Lab.md': (
            '# MOC – Lab\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics/Exercises/LAB"\n'
            'SORT file.name asc\n'
            '```\n'
        ),
        'MOC – Plane Waves.md': (
            '# MOC – Plane Waves\n\n'
            '- [[Formulas/Plane Waves & Power — Quick Formula Sheet]]\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics"\n'
            'WHERE contains(file.name, "Plane") or contains(file.path, "Plane Waves")\n'
            '```\n'
        ),
        'MOC – Polarization.md': (
            '# MOC – Polarization\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics"\n'
            'WHERE contains(file.name, "Polarization")\n'
            '```\n'
        ),
        'MOC – EM Loss & Skin Depth.md': (
            '# MOC – EM Loss & Skin Depth\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics"\n'
            'WHERE contains(file.name, "Skin Depth") or contains(file.name, "Loss")\n'
            '```\n'
        ),
        'MOC – Transmission Lines.md': (
            '# MOC – Transmission Lines\n\n'
            '```dataview\n'
            'LIST FROM "Courses/Electromagnetics"\n'
            'WHERE contains(file.name, "Transmission")\n'
            '```\n'
        ),
    }
    for fname, content in mocs.items():
        p = COURSE_ROOT / fname
        if p.exists():
            # Do not overwrite existing MOCs; preserve user content.
            continue
        if write_text_if_changed(p, content):
            created.append(str(p))
    return created


def image_hygiene(notes_changed_counter: dict) -> int:
    moved = 0
    pattern = re.compile(r'!\[\[([^\]|#]+\.png)\]\]')
    for md in COURSE_ROOT.rglob('*.md'):
        txt = read_text(md)
        embeds = pattern.findall(txt)
        changed_txt = txt
        for fn in embeds:
            if fn.lower().startswith('courses/electromagnetics/images/'):
                continue
            # Only move root-level pasted images
            if not fn.lower().startswith('pasted image'):
                continue
            src = VAULT_ROOT / fn
            if src.exists():
                dest = COURSE_ROOT / 'Images' / src.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(src), str(dest))
                    moved += 1
                except Exception:
                    # If move fails (e.g., already moved), continue to relink
                    pass
                changed_txt = changed_txt.replace(f'![[{fn}]]', f'![[Courses/Electromagnetics/Images/{src.name}]]')
        if changed_txt != txt:
            md.write_text(changed_txt, encoding='utf-8')
            notes_changed_counter['md_updated'] += 1
    return moved


def process_notes():
    md_updated = 0
    quick_refs_inserted = 0
    sol_links_added_total = 0
    q9_tables = 0
    solutions_dir = COURSE_ROOT / 'Exercises' / 'work' / 'Solutions'

    for md in COURSE_ROOT.rglob('*.md'):
        # Skip MOCs normalization: they will be overwritten by create_mocs()
        if md.name.startswith('MOC – '):
            continue
        orig = read_text(md)
        txt = orig

        # Frontmatter
        fm, _, body = split_frontmatter(txt)
        if fm is None:
            # Build frontmatter
            # Title from first H1 or filename
            title_match = re.search(r'^#\s+(.+)$', body, flags=re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md.stem
            ftype = detect_type(md)
            topic = guess_topic(md)
            new_fm = build_frontmatter(title, ftype, topic)
            body = body.lstrip('\n')
            txt = new_fm + body
        else:
            txt = fm + body

        # Ensure Top nav after frontmatter
        fm2, _, body2 = split_frontmatter(txt)
        if fm2 is not None:
            body2 = ensure_top_nav(body2)
            txt = fm2 + body2
        else:
            txt = ensure_top_nav(txt)

        # Insert Quick refs blocks
        txt_body_only = txt
        quick_before = quick_refs_inserted
        if fm2 is not None:
            # only body after fm
            body3 = txt[len(fm2):]
            body3, ins = insert_quick_refs(md, body3)
            quick_refs_inserted += ins
            txt = fm2 + body3
        else:
            txt, ins = insert_quick_refs(md, txt)
            quick_refs_inserted += ins

        # Cross-links for exercises
        if 'Exercises/work/' in str(md).replace('\\', '/'):
            fm3, _, body4 = split_frontmatter(txt)
            new_body4, links_added = normalize_questions_and_solutions(md, body4, solutions_dir)
            sol_links_added_total += links_added
            txt = (fm3 or '') + new_body4

        # Standardize Q9 polarization tables
        body_for_q9 = txt[len(fm2):] if fm2 else txt
        new_body_q9, changed = standardize_q9_polarization(body_for_q9)
        if changed:
            q9_tables += changed
            txt = (fm2 or '') + new_body_q9

        # Ensure footer
        txt = ensure_footer(txt)

        # Append Dataview hubs
        txt2, hubs_added = append_dataview_hubs(txt)
        txt = txt2

        if txt != orig:
            md.write_text(txt, encoding='utf-8')
            md_updated += 1

    return {
        'md_updated': md_updated,
        'quick_refs': quick_refs_inserted,
        'sol_links': sol_links_added_total,
        'q9_tables': q9_tables,
    }


def main():
    ensure_dirs()
    mocs = create_mocs()
    results = process_notes()
    images_moved = image_hygiene(results)

    # Print summary
    print('Number of Markdown files updated:', results['md_updated'])
    print('MOCs created/updated (list):')
    for m in mocs:
        print(' -', m)
    print('Quick refs blocks inserted (count):', results['quick_refs'])
    print('Question <-> Solution links added (count):', results['sol_links'])
    print('Q9 polarization tables standardized (count):', results['q9_tables'])
    print('Number of images moved/relinked:', images_moved)


if __name__ == '__main__':
    main()
