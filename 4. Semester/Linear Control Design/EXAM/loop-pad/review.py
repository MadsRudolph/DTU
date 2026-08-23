"""Bridge between the Loop Pad container and this PC, for board review.

The pad now runs on the Proxmox LXC 'loop-pad' (CT 110), so boards are written
there, not here. This pulls them down so they can be read as images, and pushes
the reviewed feedback back so the tablet picks it up within 5 s.

  python review.py pull     copy new boards + current feedback.json down
  python review.py push     upload the local feedback.json to the container
"""
import subprocess
import sys
from pathlib import Path

HOST = "root@192.168.50.147"
REMOTE = "/opt/loop-pad"
HERE = Path(__file__).resolve().parent

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"failed: {' '.join(args)}\n{r.stderr.strip()}")
    return r.stdout

def pull():
    (HERE / "boards").mkdir(exist_ok=True)
    days = run(["ssh", "-o", "BatchMode=yes", HOST,
                f"ls {REMOTE}/boards 2>/dev/null"]).split()
    for day in days:
        local = HERE / "boards" / day
        local.mkdir(parents=True, exist_ok=True)
        have = {p.name for p in local.iterdir()}
        names = run(["ssh", "-o", "BatchMode=yes", HOST,
                     f"ls {REMOTE}/boards/{day}"]).split()
        new = [n for n in names if n not in have]
        for n in new:
            run(["scp", "-q", "-o", "BatchMode=yes",
                 f"{HOST}:{REMOTE}/boards/{day}/{n}", str(local / n)])
        if new:
            print(f"{day}: pulled {len(new)} new file(s)")
    run(["scp", "-q", "-o", "BatchMode=yes",
         f"{HOST}:{REMOTE}/feedback.json", str(HERE / "feedback.json")])
    pngs = sorted(HERE.glob("boards/*/*.png"), key=lambda p: p.stat().st_mtime)
    print("newest board:", pngs[-1] if pngs else "(none)")

def push():
    run(["scp", "-q", "-o", "BatchMode=yes",
         str(HERE / "feedback.json"), f"{HOST}:{REMOTE}/feedback.json"])
    print("feedback.json pushed — the tablet shows it within 5 s")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "pull":
        pull()
    elif cmd == "push":
        push()
    else:
        sys.exit(__doc__)
