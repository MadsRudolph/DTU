#!/usr/bin/env python3
"""LAN mirror of study.madsrudolph.dev (the Study Bench: hub + one folder per course) for CT 116. Pulls manifest.json from
the public site and refreshes /var/www/analogy-bench when any file hash changed.
Runs from analogy-bench-mirror.timer every 30 min. No credentials needed, so a
lecture added from either PC reaches the LAN copy on its own."""
import hashlib, json, pathlib, sys, tempfile, urllib.request, os
SRC = "https://study.madsrudolph.dev/"
DST = pathlib.Path("/var/www/analogy-bench")
UA = "analogy-bench-mirror/1 (CT 116 study; +https://study.madsrudolph.dev)"  # Cloudflare 403s the default Python-urllib agent
def get(name):
    req = urllib.request.Request(SRC + name, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()
try:
    manifest = json.loads(get("manifest.json"))
except Exception as e:
    print("manifest fetch failed:", e); sys.exit(0)
changed = []
for name, sha in manifest["files"].items():
    local = DST / name
    local.parent.mkdir(parents=True, exist_ok=True)
    if local.exists() and hashlib.sha256(local.read_bytes()).hexdigest() == sha:
        continue
    data = get(name)
    if hashlib.sha256(data).hexdigest() != sha:
        print("hash mismatch, skipping", name); continue
    tmp = tempfile.NamedTemporaryFile(dir=local.parent, delete=False); tmp.write(data); tmp.close()
    os.chmod(tmp.name, 0o644); os.replace(tmp.name, local); changed.append(name)
(DST / "manifest.json").write_bytes(json.dumps(manifest, indent=1).encode())
print("updated" if changed else "up to date", ", ".join(changed))
