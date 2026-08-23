"""Push the 34722 Obsidian notes to the Loop Pad container.

Only markdown and images travel - the PDFs in the vault are drive-synced and far
too big to be useful on a tablet mid-derivation. Re-run this whenever the notes
change; it is a full mirror, so deletions propagate too.

  python sync-vault.py
"""
import subprocess
import sys
from pathlib import Path

VAULT = Path(r"C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1")
HOST = "root@192.168.50.147"
REMOTE = "/opt/vault"

def main():
    if not VAULT.is_dir():
        sys.exit(f"vault not found: {VAULT}")
    staged = Path(__file__).resolve().parent / ".vault-stage"
    subprocess.run(["rm", "-rf", str(staged)], capture_output=True)
    n = 0
    for src in VAULT.rglob("*"):
        if not src.is_file() or src.suffix.lower() not in {".md", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
            continue
        dst = staged / src.relative_to(VAULT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        n += 1
    subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, f"rm -rf {REMOTE} && mkdir -p {REMOTE}"], check=True)
    r = subprocess.run(["scp", "-q", "-r", "-o", "BatchMode=yes",
                        str(staged) + "/.", f"{HOST}:{REMOTE}/"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip())
    subprocess.run(["rm", "-rf", str(staged)], capture_output=True)
    print(f"synced {n} files to {HOST}:{REMOTE}")

if __name__ == "__main__":
    main()
