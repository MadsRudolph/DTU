# learn-sync

Pulls new DTU Learn material into the Obsidian vault on a schedule, files it by
rules, publishes it through the existing git + drive-sync pipeline, and reports
to Discord. Design: [`docs/superpowers/specs/2026-08-31-learn-sync-design.md`](../../docs/superpowers/specs/2026-08-31-learn-sync-design.md).

## Commands

```bash
learn-sync auth       # open a browser, sign in by hand, save the session
learn-sync discover   # probe the instance, dump payloads into fixtures/discovery/
learn-sync sync       # fetch, file, commit, push, notify
learn-sync sync --dry-run   # print the plan, write nothing
```

## How it decides where a file goes

`rules.yaml` holds ordered per-course rules; the first match wins. `module`
matches the Brightspace module path, `file` matches the filename, both regex, and
a rule listing both requires both. Anything unmatched falls to `_Learn/{module}/`.

Every file lands in **exactly one place**. The full Brightspace tree is
reproduced as `_Learn/INDEX.md` per course, linking to wherever each file
actually went — the tree view without duplicated binaries.

A course with no rules still syncs: standard folder skeleton, everything under
`_Learn/`, and Discord asks you to add rules for it.

## First run

1. `learn-sync auth` — sign in. Do this wherever you have a browser; it writes
   `storageState.json`, which you can copy to the container.
2. `learn-sync discover` — writes `fixtures/discovery/` and prints which
   endpoints answered. Put the calendar feed URL it finds into `LEARN_CALENDAR_FEED`.
3. `learn-sync sync --dry-run` — check the filing decisions before anything is
   written. Tune `rules.yaml` and repeat until the paths look right.
4. `learn-sync sync` — for real.

## Deploying to the Proxmox LXC

Debian 12, unprivileged, 2 GB RAM (Chromium's floor), Docker + Compose installed.

```bash
mkdir -p /srv/learn-sync/{app,repo,session,ssh,rclone}
git clone git@github.com:MadsRudolph/DTU.git /srv/learn-sync/repo
cp -r /srv/learn-sync/repo/tools/learn-sync/* /srv/learn-sync/app/
```

- Put a **deploy key with write access** in `/srv/learn-sync/ssh/` and add its
  public half to the repo on GitHub.
- Copy the working `rclone.conf` (the one with the `gdrive:` remote) into
  `/srv/learn-sync/rclone/`.
- Copy your `storageState.json` into `/srv/learn-sync/session/`.
- `cp .env.example .env`, fill it in, `chmod 600 .env`.

Then:

```bash
cd /srv/learn-sync/app && docker compose build
cp deploy/learn-sync.{service,timer} /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now learn-sync.timer
```

Check on it with `systemctl list-timers learn-sync` and
`journalctl -u learn-sync -f`.

## Credentials

`LEARN_PASS` is **optional**. Without it the service runs on the saved session
alone and Discord-pings you when it expires; with it, it re-runs the ADFS form
login unattended. The password is never logged, never committed, and lives only
in `.env` at mode 600.

If DTU ever puts MFA in front of Learn, the password path stops working by
design — the run aborts before touching git and tells you to re-run
`learn-sync auth`.

## On the vault side

Nothing changes. `git pull` then
`python Obsidian/scripts/drive-sync/download.py`, same as always. Binaries stay
gitignored and travel via Drive; the manifest travels in git.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

No network and no browser in the suite — collectors are parsers over fixtures,
and delivery runs against a real throwaway git repo with a bare origin.

## Status

Verified end to end against the live instance on 2026-08-31, using a scratch
clone with a local bare origin:

- cold run — 30 files downloaded and filed, notes written, one commit, pushed
- second run — no-op, no commit, clean tree
- zero binaries tracked in git; all 30 on disk and correctly gitignored
- `Home.md` injection checked against the real 135-line dashboard: every
  original line preserved, idempotent

**Not yet exercised:** the rclone leg. The scratch repo had no
`Obsidian/scripts/drive-sync/upload.py`, so the run took the documented
"script missing, skipping upload" path. That step runs for the first time on
the container.

Filing decisions worth knowing about:

- 34654's Learn content area is empty (0 modules), so it syncs nothing. That is
  correct, not a failure — its assignment briefs came from elsewhere.
- 62755 datasheets (`IRF540N.pdf`, `IR2110.pdf`, …) land in `Labs/` next to
  `Lab1.pdf`, because they live in the Lab module. Move them to a
  `Literature/Datasheets/` rule if you would rather separate them.
- Only events matching `due|hand-in|deadline|aflever` reach `Home.md`. Right
  now every calendar entry is timetable ("Lecture", "Group work"), so the
  deadlines block stays empty until real hand-ins are posted.
