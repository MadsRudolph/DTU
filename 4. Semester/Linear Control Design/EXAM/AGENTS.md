# Loop Pad — system notes

The 34722 LCD1 study rig. Three surfaces, one server, now hosted independently of
any PC so the tablet works whether or not the desktop is on.

**Exam:** 34722 Linear Control Design 1, ORAL, Monday 25 August 2026, 15 min, no aids.
Questions in written-exam style, solved and explained at the board. June attempt was
3/20 — every miss a trap distractor (reciprocals, dropped `+1`, sign errors), not a
theory gap. Precision beats breadth.

---

## Where it runs

| | |
|---|---|
| Host | Proxmox `proxmox-1` — https://192.168.50.200:8006 (LAN) / https://100.97.159.115:8006 (Tailscale) |
| Container | **CT 110 `loop-pad`**, Debian 13, `192.168.50.147`, `onboot=1` |
| Services | `loop-pad.service` (the server) and `cloudflared.service` (the tunnel) — both enabled |
| Public | https://pad.madsrudolph.dev — tunnel runs *inside* the container |
| App root | `/opt/loop-pad` · vault mirror `/opt/vault` · course page `/opt/Closed-Loop.html` |

Routes: `/` pad · `/course` Closed Loop · `/notes` the Obsidian vault · `/api/*`.

⚠ `/api/save` is unauthenticated on a public hostname. Put Cloudflare Access in front
of it or tear the tunnel down after the exam.

---

## Reviewing a board ("check my board")

Boards are written on the container, so pull them first:

```bash
python review.py pull      # boards + current feedback.json down to this PC
```

1. Read the newest PNG in `loop-pad/boards/<date>/` as an image.
2. Its sidecar `.json` carries `qid` and `prompt`. Look the `qid` up in
   `questions.json` and grade against that entry's `points` and `answer` — the rubric
   is those key steps, not generic correctness.
3. Append an entry to the local `feedback.json` (valid JSON array, never overwrite):

```json
{"board": "190336_p1-parallel-feedback.png",
 "time": "19:07",
 "verdict": "partly",
 "notes": ["what is right", "what is wrong", "what to say instead"],
 "svg": "<circle cx='812' cy='430' r='60' fill='none' stroke='#B23B3B' stroke-width='7'/>",
 "imgW": 2290, "imgH": 1212}
```

4. `python review.py push` — the tablet shows it within 5 s.

**Coordinates.** The `svg` fragment lives in the **pixel space of that PNG**: (0,0) is
its top-left, (imgW,imgH) its bottom-right. There is no fixed board size — the canvas
is infinite and every export is auto-cropped to the drawing, so each PNG has its own
dimensions. Read the image, note its real size, annotate against it, and pass
`imgW`/`imgH` so the app can rescale if they ever disagree. Getting this wrong is what
put a previous agent's marks in the wrong place. Red `#B23B3B`, `stroke-width` 5–8,
`font-size` 36–48 at typical ~2400 px exports.

Only the newest entry's `svg` is drawn, so put marks on the board still on screen and
give older boards their own entries with `notes` only.

## Reviewing spoken answers ("review my oral session")

`python tools/transcribe-oral.py` in `C:\Users\Mads2\lcd1-exam-suite`, then read
`oral-sessions/<date>/REPORT.md` and grade each transcript against the same question
bank. Verdicts: Good / Almost / Rework.

---

## Grading sources, in trust order

1. `loop-pad/questions.json` — `points`/`answer` are the rubric (38 questions, P1–P7).
2. `Obsidian/Courses/34722 .../Formulas/Exam Formula Cheat-Sheet.md`
3. `.../Exam Prep/W-F26 — Worked Exam (MCQ).md` — all 20 June questions worked, with
   the traps that cost the points.
4. `.../Exam Prep/RE-EXAM — August 2026 Study Plan.md`
5. `Closed-Loop.html` — what he is learning from.

Conventions: lead uses α < 1, phase budget `∠C + ∠G = γ_M − 180°` at crossover,
`t_s = 4/(ζω_n)`. If a formula disagrees with the cheat-sheet, the cheat-sheet wins.

---

## Keeping it fed

```bash
python sync-vault.py     # mirror the 34722 vault notes to /opt/vault
scp app.html server.py root@192.168.50.147:/opt/loop-pad/ && \
  ssh root@192.168.50.147 systemctl restart loop-pad
```

`boards/` and `feedback.json` are gitignored personal data — never commit them, and
never put AI/`Co-Authored-By` mentions in commit messages in this repo.
