#!/usr/bin/env python3
"""
Electromagnetics Vault Reorganization Script
Safely migrates files to new hierarchical structure with validation and rollback capability.

Usage:
    python migrate_vault.py --vault-path /path/to/Obsidian/Courses/Electromagnetics [--dry-run] [--backup]

Options:
    --vault-path    Path to Electromagnetics folder (required)
    --dry-run       Show what would be done without making changes
    --backup        Create timestamped backup before migration
"""

import argparse
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import sys

# ============================================================================
# MIGRATION MAP: Old path → New path
# ============================================================================

MIGRATION_MAP = {
    # Foundations
    "Formulas/Coordinate Systems.md": "01-Foundations/Coordinate-Systems.md",
    "Formulas/Vectors using Spherical Components.md": "01-Foundations/Vectors-Spherical-Components.md",
    "Formulas/Differential Vector Operators.md": "01-Foundations/Differential-Operators.md",
    "Formulas/Operator Forms (Cartesian–Cylindrical–Spherical).md": "01-Foundations/Operator-Forms-All-Systems.md",

    # Foundations Examples
    "Formulas/Examples/Gradient Example (Potential).md": "01-Foundations/Examples/Gradient-Potential.md",
    "Formulas/Examples/Divergence Example (E-field).md": "01-Foundations/Examples/Divergence-E-Field.md",
    "Formulas/Examples/Curl Example (B-field).md": "01-Foundations/Examples/Curl-B-Field.md",
    "Formulas/Examples/Cartesian to Cylindrical (Point+Vector).md": "01-Foundations/Examples/Cartesian-to-Cylindrical.md",
    "Formulas/Examples/Gauss Flux (Point Charge).md": "06-Electrostatics/Examples/Gauss-Flux-Point-Charge.md",

    # Waves and Phasors
    "Formulas/Wave Parameters.md": "02-Waves-and-Phasors/Wave-Parameters.md",

    # Transmission Lines
    "Formulas/Transmission_Lines.md": "03-Transmission-Lines/TL-Fundamentals.md",
    "Formulas/Single Terminated TL.md": "03-Transmission-Lines/TL-Single-Terminated.md",
    "Formulas/Single Terminated TL – Special Cases.md": "03-Transmission-Lines/TL-Special-Cases.md",
    "Formulas/Transmission Lines (TLs) – VNA + Power.md": "03-Transmission-Lines/TL-Power-and-VNA.md",
    "Formulas/Lecture 10 – Transmission Lines Power, Matching & Smith Chart.md": "03-Transmission-Lines/TL-Matching-Circuits.md",

    # Transmission Lines Examples
    "Exercises/work/3-3.2.md": "03-Transmission-Lines/Examples/Coaxial-Line-Parameters.md",
    "Exercises/work/3-3.2.pdf": "03-Transmission-Lines/Examples/Coaxial-Line-Parameters.pdf",

    # Plane Waves
    "Formulas/Lecture 11 Plane Waves Lossles.md": "04-Plane-Waves/Plane-Waves-Lossless.md",

    # Quick Reference
    "Formulas/Plane Waves & Power — Quick Formula Sheet.md": "00-Quick-Reference/Plane-Waves-Power-Quick-Sheet.md",

    # Electrostatics
    "Formulas/Electrostatics — Laws.md": "06-Electrostatics/Electrostatics-Laws.md",

    # Exercises
    "Exercises/work/Home Assignment 1.md": "Exercises/Solved/Assignment-01.md",

    # MOCs
    "MOC – Electromagnetics.md": "00-Quick-Reference/MOC – Electromagnetics.md",
    "MOC – Introduction Waves & Phasors.md": "02-Waves-and-Phasors/MOC – Waves-and-Phasors.md",
    "MOC – Transmission Lines.md": "03-Transmission-Lines/MOC – Transmission-Lines.md",
    "MOC – Plane Waves.md": "04-Plane-Waves/MOC – Plane-Waves.md",
    "MOC – Reflections & Transmission.md": "05-Reflections-and-Transmission/MOC – Reflections-and-Transmission.md",
    "MOC – Electrostatics.md": "06-Electrostatics/MOC – Electrostatics.md",
    "MOC – Magnetostatics.md": "07-Magnetostatics/MOC – Magnetostatics.md",
    "MOC – Time-Varying Fields.md": "08-Time-Varying-Fields/MOC – Time-Varying-Fields.md",
    "MOC – Exercises.md": "Exercises/MOC – Exercises.md",

    # Delete (will be split/obsolete)
    "Formulas/Electrostatics & Magnetostatics — MOC.md": None,
}

# Files to delete
DELETE_FILES = [
    "Formulas/Electrostatics & Magnetostatics.md",  # Mega-file
    "MOC – Vector Operators.md",                    # Merged into Foundations
]

# PDF files to move (pattern-based)
PDF_PATTERNS = [
    ("Exercises/work/*.pdf", "Exercises/Solved/"),
]

# Tag mappings for YAML updates
TAG_MAPPINGS = {
    "01-Foundations": ["electromagnetics", "foundations", "formula"],
    "02-Waves-and-Phasors": ["electromagnetics", "waves", "formula"],
    "03-Transmission-Lines": ["electromagnetics", "transmission-lines", "formula"],
    "04-Plane-Waves": ["electromagnetics", "plane-waves", "formula"],
    "05-Reflections-and-Transmission": ["electromagnetics", "reflections", "formula"],
    "06-Electrostatics": ["electromagnetics", "electrostatics", "formula"],
    "07-Magnetostatics": ["electromagnetics", "magnetostatics", "formula"],
    "08-Time-Varying-Fields": ["electromagnetics", "time-varying", "formula"],
    "00-Quick-Reference": ["electromagnetics", "quick-ref"],
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_vault_path(vault_path: Path) -> bool:
    """Check if path looks like Electromagnetics vault."""
    required_markers = ["Formulas", "Exercises", "Slides"]
    return all((vault_path / marker).exists() for marker in required_markers)

def create_backup(vault_path: Path) -> Path:
    """Create timestamped backup of entire vault."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = vault_path.parent / f"Electromagnetics_backup_{timestamp}"
    print(f"📦 Creating backup: {backup_path}")
    shutil.copytree(vault_path, backup_path, symlinks=True)
    return backup_path

def create_folder_structure(vault_path: Path, dry_run: bool = False):
    """Create new folder hierarchy."""
    folders = [
        "00-Quick-Reference",
        "01-Foundations/Examples",
        "02-Waves-and-Phasors",
        "03-Transmission-Lines/Examples",
        "04-Plane-Waves/Examples",
        "05-Reflections-and-Transmission",
        "06-Electrostatics/Examples",
        "07-Magnetostatics/Examples",
        "08-Time-Varying-Fields",
        "Exercises/Solved",
    ]
    for folder in folders:
        path = vault_path / folder
        if dry_run:
            print(f"[DRY RUN] Would create: {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {path}")

def update_yaml_frontmatter(content: str, new_title: str, folder: str) -> str:
    """Update YAML frontmatter with new title and tags."""
    yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not yaml_match:
        print("⚠️  No YAML frontmatter found")
        return content
    yaml_content = yaml_match.group(1)
    rest_content = content[yaml_match.end():]

    # Update title
    yaml_content = re.sub(r'(^|\n)title:\s*.*?(?=\n)', f'\ntitle: "{new_title}"', yaml_content)

    # Update date (add or replace)
    if re.search(r'(^|\n)updated:\s*.*?(?=\n)', yaml_content):
        yaml_content = re.sub(r'(^|\n)updated:\s*.*?(?=\n)', f'\nupdated: "{datetime.now().strftime("%Y-%m-%d")}"', yaml_content)
    else:
        yaml_content += f'\nupdated: "{datetime.now().strftime("%Y-%m-%d")}"'

    # Add/merge tags
    tags_to_add = []
    for topic_folder, tags in TAG_MAPPINGS.items():
        if topic_folder in folder.replace("\\", "/"):
            tags_to_add = tags
            break

    if tags_to_add:
        if re.search(r'(^|\n)tags:\s*\[.*?\]', yaml_content, re.DOTALL):
            existing = re.findall(r'(^|\n)tags:\s*\[(.*?)\]', yaml_content, re.DOTALL)[0][1]
            existing_list = [t.strip() for t in existing.split(",") if t.strip()]
            merged = list(dict.fromkeys(tags_to_add + existing_list))
            yaml_content = re.sub(r'(^|\n)tags:\s*\[.*?\]', f'\ntags: [{", ".join(merged)}]', yaml_content, flags=re.DOTALL)
        else:
            yaml_content += f'\ntags: [{", ".join(tags_to_add)}]'

    yaml_block = yaml_content.strip()
    return f"---\n{yaml_block}\n---\n{rest_content.lstrip()}"

def update_internal_links(content: str, old_path: str, new_path: str, all_moves: Dict[str, str]) -> str:
    """Update [[wikilinks]] where the target filename changes."""
    filename_map = {}
    for old, new in all_moves.items():
        if new is not None:
            old_name = Path(old).stem
            new_name = Path(new).stem
            if old_name != new_name:
                filename_map[old_name] = new_name

    def replace_link(match):
        link_text = match.group(1)
        for old_name, new_name in filename_map.items():
            if link_text == old_name or link_text.startswith(old_name + "|"):
                return f"[[{link_text.replace(old_name, new_name, 1)}]]"
        return match.group(0)

    return re.sub(r'\[\[(.*?)\]\]', replace_link, content)

def migrate_file(vault_path: Path, old_rel: str, new_rel: str, dry_run: bool = False) -> bool:
    """Move and update a single file (idempotent). If source missing but destination exists, treat as success."""
    old_path = vault_path / old_rel
    new_path = vault_path / new_rel

    # Idempotency: if old doesn't exist but new does, treat as success
    if not old_path.exists():
        if new_path.exists():
            print(f"ℹ️  Skipping (already migrated): {old_rel} → {new_rel}")
            return True
        print(f"⚠️  Source not found: {old_path}")
        return False

    if dry_run:
        print(f"[DRY RUN] {old_rel} → {new_rel}")
        return True

    try:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        if old_path.suffix.lower() == ".md":
            content = old_path.read_text(encoding='utf-8')

            # Ensure YAML exists; if not, create minimal YAML
            yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if not yaml_match:
                default_yaml = f'---\ntitle: "{new_path.stem.replace("-", " ")}"\ntags: []\nupdated: "{datetime.now().strftime("%Y-%m-%d")}"\n---\n'
                content = default_yaml + content
                yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)

            # Update YAML title/tags via existing helper
            new_title = new_path.stem.replace('-', ' ')
            content = update_yaml_frontmatter(content, new_title, str(new_path.parent))

            # Add alias for old filename stem so legacy [[links]] still resolve
            old_stem = Path(old_rel).stem
            new_stem = Path(new_rel).stem
            if old_stem != new_stem:
                ym = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                if ym:
                    yml = ym.group(1)
                    body = content[ym.end():]
                    # ensure aliases array includes old_stem
                    if re.search(r'(^|\n)aliases:\s*\[.*?\]', yml, re.DOTALL):
                        existing = re.findall(r'(^|\n)aliases:\s*\[(.*?)\]', yml, re.DOTALL)[0][1]
                        items = [t.strip().strip('"').strip("'") for t in existing.split(',') if t.strip()]
                        if old_stem not in items:
                            items.append(old_stem)
                        alias_items = ", ".join(f'"{i}"' for i in items)
                        yml = re.sub(r'(^|\n)aliases:\s*\[.*?\]', f'\naliases: [{alias_items}]', yml, flags=re.DOTALL)
                    else:
                        yml += f'\naliases: ["{old_stem}"]'
                    content = f"---\n{yml.strip()}\n---\n{body}"

            # Update internal wikilinks for name changes
            content = update_internal_links(content, old_rel, new_rel, MIGRATION_MAP)

            new_path.write_text(content, encoding='utf-8', newline="\n")
        else:
            # Non-markdown: copy bytes (e.g., PDFs)
            shutil.copy2(str(old_path), str(new_path))

        # Remove original after successful write/copy
        old_path.unlink()
        print(f"✅ {old_rel} → {new_rel}")
        return True

    except Exception as e:
        print(f"❌ Error migrating {old_rel}: {e}")
        return False

def delete_file(vault_path: Path, rel_path: str, dry_run: bool = False) -> bool:
    """Delete a file."""
    file_path = vault_path / rel_path
    if not file_path.exists():
        print(f"⚠️  File not found (already deleted?): {rel_path}")
        return True
    if dry_run:
        print(f"[DRY RUN] Would delete: {rel_path}")
        return True
    try:
        file_path.unlink()
        print(f"🗑️  Deleted: {rel_path}")
        return True
    except Exception as e:
        print(f"❌ Error deleting {rel_path}: {e}")
        return False

def cleanup_empty_folders(vault_path: Path, dry_run: bool = False):
    """Remove empty directories after migration."""
    for path in sorted(vault_path.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                next(path.iterdir())
            except StopIteration:
                if dry_run:
                    print(f"[DRY RUN] Would remove empty folder: {path}")
                else:
                    path.rmdir()
                    print(f"🧹 Removed empty folder: {path}")

def generate_report(vault_path: Path, success: List[str], failed: List[str]):
    """Generate migration report."""
    report_path = vault_path / "MIGRATION_REPORT.md"
    report = f"""# Vault Migration Report

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- ✅ Successfully migrated: {len(success)} files
- ❌ Failed: {len(failed)} files

## Successful Migrations
{chr(10).join(f"- {f}" for f in success) if success else "None"}

## Failed Migrations
{chr(10).join(f"- {f}" for f in failed) if failed else "None"}

## Next Steps
1. Verify all files in new locations
2. Check for broken links in Obsidian (Ctrl+P → 'Check for broken links')
3. Update MOCs with Dataview queries
4. Delete old empty folders if not done automatically
5. Git commit changes

---
*Generated by vault migration script*
"""
    report_path.write_text(report, encoding='utf-8', newline="\n")
    print(f"\n📊 Report saved to: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Migrate Electromagnetics vault to new structure")
    parser.add_argument("--vault-path", required=True, help="Path to Electromagnetics folder")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--backup", action="store_true", help="Create backup before migration")
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        print(f"❌ Path does not exist: {vault_path}")
        sys.exit(1)

    if not validate_vault_path(vault_path):
        print(f"❌ Path does not look like Electromagnetics vault: {vault_path}")
        print("Expected folders: Formulas/, Exercises/, Slides/")
        sys.exit(1)

    print(f"🚀 Starting migration for: {vault_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE MIGRATION'}")

    # Quick diagnostic: warn about EN DASH / hyphen mismatches in map keys if sources missing
    missing_candidates = []
    for old_rel, new_rel in MIGRATION_MAP.items():
        if new_rel is None:
            continue
        if not (vault_path / old_rel).exists() and not (vault_path / new_rel).exists():
            # Heuristic: if the path contains an EN DASH, suggest hyphen variant
            if "–" in old_rel or "—" in old_rel:
                missing_candidates.append((old_rel, old_rel.replace("–", "-").replace("—", "-")))
    if missing_candidates:
        print("\n🔎 Potential dash-mismatch sources (consider adding alternate keys):")
        for o, alt in missing_candidates:
            print(f" - {o}  (try also: {alt})")

    # Backup
    if args.backup and not args.dry_run:
        backup_path = create_backup(vault_path)
        print(f"✅ Backup created: {backup_path}")

    # Step 1: Create folder structure
    print("\n📁 Creating folder structure...")
    create_folder_structure(vault_path, args.dry_run)

    # Step 2: Delete files
    print("\n🗑️  Deleting redundant files...")
    for file_path in DELETE_FILES:
        delete_file(vault_path, file_path, args.dry_run)

    # Step 3: Migrate files
    print("\n📦 Migrating files...")
    success, failed = [], []
    for old_rel, new_rel in MIGRATION_MAP.items():
        if new_rel is None:
            continue
        if migrate_file(vault_path, old_rel, new_rel, args.dry_run):
            success.append(f"{old_rel} → {new_rel}")
        else:
            failed.append(f"{old_rel} → {new_rel}")

    # Step 4: Move remaining PDFs
    print("\n📄 Moving PDF files...")
    for pattern_rel, target_dir in PDF_PATTERNS:
        pattern_path = vault_path / pattern_rel
        parent = pattern_path.parent
        if parent.exists():
            for pdf_file in parent.glob(pattern_path.name):
                if pdf_file.name not in [Path(k).name for k in MIGRATION_MAP.keys()]:
                    new_pdf_path = vault_path / target_dir / pdf_file.name
                    if args.dry_run:
                        print(f"[DRY RUN] Would move: {pdf_file.name} → {target_dir}")
                    else:
                        new_pdf_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(pdf_file), str(new_pdf_path))
                        print(f"✅ Moved: {pdf_file.name} → {target_dir}")

    # Step 5: Cleanup
    print("\n🧹 Cleaning up empty folders...")
    cleanup_empty_folders(vault_path, args.dry_run)

    # Step 6: Report
    if not args.dry_run:
        generate_report(vault_path, success, failed)

    print("\n" + "="*60)
    print("✨ Migration complete!")
    print(f"✅ Success: {len(success)}")
    print(f"❌ Failed: {len(failed)}")
    if failed:
        print("\n⚠️  Some files failed to migrate. Check the report for details.")
    if args.dry_run:
        print("\n💡 This was a dry run. Use without --dry-run to apply changes.")
    else:
        print("\n🎯 Next steps:")
        print("1. Open Obsidian and check for broken links")
        print("2. Review MIGRATION_REPORT.md")
        print("3. Update MOCs with new structure")
        print("4. Git commit changes")

if __name__ == "__main__":
    main()
