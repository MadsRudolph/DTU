# CLAUDE.md — repo handoff

Auto-loaded by Claude Code, travels with `git pull`. Records **where to pick up** so a fresh session on any PC continues seamlessly.

> ⚠️ **Path change:** all 4th-semester course folders live in `Obsidian/Archive/4th Semester/` (34315, 34620, 34655, 62711, 62768, 62743-Reexam, the dropped 62999 — and since **26-Aug-2026 also 34722 LCD1**, whose re-exam is passed). Old paths in the archived sections below need that prefix.

---

## ACTIVE WORK: 5th semester — autumn 2026, starts Mon 31-Aug

**Enrolled:** 34870 Electroacoustics (10, E2) · 62755 Power Electronics (5, E1A) · 34840 Fundamentals of Acoustics and Noise Control (5, E3A) · 34654 Circuit Technology and EMC (5, E4A) = **25 ECTS autumn**; 34871 Nonlinear Transducers (5) in **January 2027**.

### ▶️ FIRST ACTION ON A FRESH PC
1. `git pull` in `C:\Users\Mads2\DTU`, then `python Obsidian/scripts/drive-sync/download.py` for the PDFs (all course material is gitignored + drive-synced).
2. Open the dashboard: `Obsidian/Home.md` — weekly timetable, every deadline, every exam date.
3. Per course: `Obsidian/Courses/<code> <name>/<code> <name>.md` — each index note carries the real DTU course data (staff, rooms, exam form, full lecture plan, assignment briefs).

### 📅 The term at a glance

| | Mon | Tue | Thu |
|---|---|---|---|
| **Morning** | 62755 · 8–12 · **Ballerup** | 34840 · 8–12 · Lyngby b.358 r.063 | 34870 · 8:30–12 · Lyngby |
| **Afternoon** | 34870 · 13–17 · Lyngby b.352 r.019 | 34654 · 13–17 · Lyngby b.341 r.023 | — |

Wed/Fri free — that is where 34654 group work and the 34870 labs/project have to go.

**Exams:** 34870 oral **9–10 Dec** · 34840 written **11 Dec** · 62755 written 4 h (**placement unconfirmed**) · 34654 **no exam** (4 reports, pass/fail, 3 of 4 must pass) · 34871 oral in January, **no aids**.

### 🚩 Open questions / gotchas
- **62755 exam placement conflict:** the DTU course page says **E1A**, slide 8 of `Lecture 1 Introduction.pdf` says **E2B**. E2B would collide with the 34870 oral on 9–10 Dec. Confirm with Ashraf in week 1 and fix `62755 Power Electronics.md`.
- **Monday is two campuses:** 62755 Ballerup 8–12 → 34870 Lyngby 13–17.
- **34840 is a formal prerequisite for 34870** but they run in parallel; the 34870 staff hand out an acoustics background note to bridge it.
- **34654 group deadline:** sign up in DTU Learn (groups of 5) before **Tue 8-Sep 14:00** or you get auto-assigned. Also: opening quiz + Discord before the first lecture.
- **34870 needs LTspice installed before the first lecture** (Mon 31-Aug); groups of 3 for labs + project.
- **62755 slides for weeks 9 and 12** (multilevel inverters, AC voltage controllers) not handed out yet.
- **34654 learning reflections go into a DTU form** — write equations in plain text, not LaTeX.

### 📂 Where the 5th-semester material lives
- **Obsidian** `Obsidian/Courses/<code> …/` — each has `Lecture Notes/ Slides/ Exercises/ Formulas/ Literature/ Images/` plus per-course extras (`Labs/`, `Project/`, `Projects/`).
  - **34870:** `Literature/00 - Basic Material/` (course plan, acoustics note, LTspice quick guide) + `Literature/Metrology - BIPM/` (SI Brochure 9th ed + concise + FAQs + appendix 3, pulled from bipm.org — required for the 17-Sep metrology lecture). Books (Leach, Beranek, Lenk, Peters) are **behind the DTU library login — not in the vault**; links are in the index note.
  - **34840:** `Literature/` (main text, loudspeaker intro, lecture plan) + `Literature/00 - Prerequisites/` (complex numbers + signals refreshers; video lectures stay on DTU Learn).
  - **62755:** `Slides/` — Lectures 1–7 as handed out.
  - **34654:** `Projects/` — the 4 assignment briefs (Passives, PCB, EMC, Environmental) + `Literature/Reference Designs/` (the two PCB schematic options and the TI TPS40200EVM-001 user guide).
- **Repo working folders:** `5. Semester/{Electroacoustics, Power Electronics, Acoustics and Noise Control, Circuit Technology and EMC, Nonlinear Transducers}` — tool-oriented subfolders (LTspice, Matlab, Simulink, PSCAD, C2000, KiCad, Labs, per-assignment folders).
- Planning truth: `Obsidian/Notes/DTU Study Path.md` (§5.1–5.5) + dashboard `Obsidian/Home.md`.

---

## REPO CONVENTIONS (apply everywhere)

### Drive-sync — large binaries are NOT in git
PDFs, pptx, zip and video are gitignored and mirrored to Google Drive via `rclone` (remote `gdrive:`), keyed by repo-relative path in `Obsidian/scripts/drive-sync/manifest.json`.
- **Fetch:** `python Obsidian/scripts/drive-sync/download.py`
- **Push new files:** `python Obsidian/scripts/drive-sync/upload.py --sync` — uploads anything new and rebuilds the manifest; commit the manifest alongside.
- ⚠️ A plain `git push` does **not** carry the binaries. Use the `drive-sync-push` skill before pushing.
- ⚠️ `download.py` tries rclone first and falls back to `gdown` by driveId — but **gdown is not installed on this PC**, so rclone is effectively the only path. If a folder is moved locally, the Drive-side folder must move too or the manifest path must stay in sync.

### Writing conventions
- **Mermaid > ASCII art** in Obsidian notes.
- **Conversational English** in study notes; **Danish** in LaTeX dispositions and team `.asm`/report comments when the group's output is Danish.
- **Plain-text equations** (no LaTeX `$...$`) when the text goes into a Microsoft Form / DTU learning-reflection form.
- **Hints-first** when Mads is studying: "let's go through X" → small hint, then stop and wait. Full walkthrough only on an explicit "walk me through it".

### Commits
- **NEVER** add `Co-Authored-By: Claude` or any mention of Claude/AI. Commit messages read like a developer wrote them.

### Nested repos
`git add -A` works repo-wide as of 26-Aug-2026 (the old broken submodule under the LCD1 `regbot/Report` path is gone). Three nested repos remain but are gitignored: `34655 …/Report/`, `62711 …/PWA Project/Report/`, `62711 …/Report-PWB/`. The 62711 and 62768 **team repos** are separate git repos with their own remotes — `cd` into them to work.

### NotebookLM
`C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id <id>` — shortnames `lcd1`, `dsp`; 62711 = `eb1f49b9-61a5-4494-8a3e-9821f8514324`, DSP = `5bd40a62-b09c-406d-b854-2ed2be6d894c`. Re-`login` if `auth-status` says NOT AUTHENTICATED; intermittent read-timeouts, retry.

---

## ARCHIVED: 34722 Linear Control Design 1 — RE-EXAM PASSED (oral, 25 August 2026) ✅

Course folder moved to `Obsidian/Archive/4th Semester/34722 Linear Control Design 1/` on 26-Aug-2026.

- **The story:** 3/20 on the June F26 written exam — not a theory gap, every miss was the trap distractor (reciprocals, dropped `+1`, marginal-gain-vs-inequality, non-physical signs). The re-exam was a **15-minute oral** at the board; prep was blank-sheet derivations, sketch drills and explain-aloud rather than solver drilling. Passed.
- **Assets** (all under the archived folder): `Exam Prep/` — `00 LCD1 — Exam Hub.md`, `RE-EXAM — August 2026 Study Plan.md`, `P1`–`P7` topic notes, `W-F26 — Worked Exam (MCQ).md` (all 20 worked), `Walkthroughs/`. Plus `Formulas/Exam Formula Cheat-Sheet.md` and `LCD1_Bible.md`.
- **🚩 Gotcha:** the previous-student helper scripts `4. Semester/Linear Control Design/EXAM/Helpers/bandwidth_second_order.m` and `crossover_frequency2bandwidth.m` use `4*zeta`/`4*zeta^2` where it must be `4*zeta^4`. The corrected formula is in the cheat-sheet §4.
- **Still live for 62755:** DTU lists 34722 as a prerequisite route into Power Electronics — the Bode / phase-margin / PI-lead material comes straight back for converter control loops.
- **The tool: lcd1-exam-suite (JS/Electron)** — `C:\Users\Mads2\lcd1-exam-suite`, own git. Launch `Launch-Desktop-App.bat` (warm) / `Double-Click-To-Run.bat` (cold). Tests `npm test` (453 green as of 8-Aug). ⚠️ `Launch-Desktop-App.bat` does **not** rebuild — after ANY source edit run `npm run build` or it silently runs old code. `C:\Users\Mads2\lcd1-solver` (Python) and `DTU/block-diagram-reducer` are **superseded predecessors** — don't develop there.
- MATLAB material: `4. Semester/Linear Control Design/EXAM/` → `Scripts/`, `Maple solutions/`, `Helpers/`, `Regbot/`. Past exams + quiz solutions: `Exercises/Solutions/Past Exams/` and `Exercises/Work/Quiz/Solutions/` under the archived folder.
- NotebookLM: `nlm.bat ask "..." --notebook-id lcd1`.

---

## ARCHIVED: 62768 Electrical Energy Systems — project DONE (June 2026)

### ▶️ FIRST ACTION ON A FRESH PC
1. `git pull` in `C:\Users\Mads2\DTU`.
2. PDFs in the **Obsidian course folder** are gitignored (drive-sync) — fetch with `python Obsidian/scripts/drive-sync/download.py`. (The **team repo** below carries its own binaries directly in git — see note.)
3. Open the course index: `Obsidian/Courses/62768 Electrical Energy Systems/62768 Electrical Energy Systems.md` (system block diagram + 18-requirement table + asset links).
4. **Clone the team repo if not present** (see below).

### 📌 Course format
**Project-based (CDIO), no written exam** — assessment = group report + working functional model. Groups of up to 6. Intro: Mon 8-June-2026 09:00, room **X2.70**. Lab work in **V1.01-04**. Lecturers: Ashraf (ashka@dtu.dk), Sam (samro@dtu.dk), Audrey (auddel@dtu.dk).

**The product:** complete electrical energy system per the *Kravspecifikation* — AC-generator → 3× transformer → rectifier → self-built buck; solar + MPPT → 1F energy store → self-built boost → pulsing load; Arduino PID + monitoring. Converters & current sensing must use **discrete components** (op-amps OK).

### 🔧 THE TEAM REPO (shared with 6 teammates — separate git repo)
- **GitHub:** `github.com/MadsRudolph/62768-energy-system` — **private**, owner MadsRudolph.
- **On disk:** `4. Semester/Electrical Energy Systems/team/` — its own git repo (HTTPS remote). Mirrors the 62711 team-repo pattern.
- **Gitignored from the umbrella** (`.gitignore` ~line 106: `4. Semester/Electrical Energy Systems/team/`) so the nested repo can't trigger the `git add` nested-repo failure. To work on it: `cd` into `team/` and use its own git.
- **Layout:** `firmware/` (Arduino), `simulation/` (Simulink .slx + param .m — seeded with course buck/boost + 3-phase models), `hardware/{schematics,bom}/`, `docs/` (spec, lab guides, `docs/datasheets/`), `measurements/`.
- ⚠️ Unlike the umbrella, **the team repo tracks PDFs/.docx/.xlsx/.slx directly in git** (no drive-sync) — it's a self-contained shared product repo.
- **TODO — invite teammates:** `gh api -X PUT repos/MadsRudolph/62768-energy-system/collaborators/USERNAME -f permission=push` (per teammate), then fill the team table in the repo README.

### Where the 62768 course materials live (personal, in umbrella repo)
- **Obsidian** `Obsidian/Courses/62768 Electrical Energy Systems/` — `Slides/` (6 lectures + intro), `Labs/`, `Literature/` (spec + `Datasheets/`), empty `Lecture Notes/Formulas/Images/` for own notes.
- **Code** `4. Semester/Electrical Energy Systems/` — `Three Phase Transformer/` + `DC-DC Converters/` Simulink models (the personal copies; team repo has copies too).

---

## ARCHIVED: 62711 Digital Systems Design — DONE (oral exam 28-May-2026, grade 4)

### ▶️ FIRST ACTION ON A FRESH PC (do this, in order)

1. `git pull` in `C:\Users\Mads2\DTU` (you just did — that's how you got this).
2. **Open the master exam hub:** `Obsidian/Courses/62711 Digital Systems Design/Exercises/Work/Project/Exam Prep/00 PWF System — Exam Hub.md`. ~9 mermaid diagrams + full per-instruction walkthroughs + discrepancies section. Single entry point.
3. **Open the LaTeX disposition for the oral presentation:** same folder, `disposition_idc_regfile.tex`. Currently focused on **BRZ** (Branch on Zero) — traces RAM → IR → IDC FSM → PC for one BRZ instruction. Compile: `pdflatex disposition_idc_regfile.tex` (twice for cross-refs).
4. **The simple intuition note:** same folder, `STUDY — 01 PWA.md`. The "explain it like I'm new to this" version of the Datapath — three things in a loop, MUX B = immediate gate, MUX D = memory gate.

If Mads is still prepping: hints-first (see workflow conventions below). If it's exam-time: the hub + disposition are everything needed.

### ✅ EXAM-PREP ASSET VERIFICATION (confirm these exist after pull)

All in `Obsidian/Courses/62711 Digital Systems Design/Exercises/Work/Project/Exam Prep/`:

| Asset | File | Role |
|---|---|---|
| Master hub | `00 PWF System — Exam Hub.md` | Single entry — overview, block-by-block, instruction set, 6 worked microcode walkthroughs (all mermaid), §6 discrepancies, §8 exam-readiness checklist |
| LaTeX disposition (BRZ) | `disposition_idc_regfile.tex` | 1-page for 5-min oral presentation. FSM mini-diagram + signal-flow block diagram + 2-cycle walkthrough + 6 talking points |
| Simple study companion | `STUDY — 01 PWA.md` | Conversational Datapath intuition, with the two-cycle "where does an immediate come from?" deep-dive |
| Phase-0 inventory | `EXAM_PREP_INVENTORY.md` | What existed at start of exam prep + trust assessment per note |
| Fact-check report | `FACT_CHECK_REPORT.md` | 5 confirmed errors + 5 ambiguities cross-checked against VHDL + spec + lecture-10 + NotebookLM |
| Top-level wiring extraction | `EX — Microprocessor (top).md` | Full top-level VHDL + diagram trace. Every walkthrough references this. |
| Per-instruction walkthroughs | `EX — Instruction {ADD,LD,JMP,BRZ,LDI,SRM}.md` | Cycle-by-cycle each. SRM has the `b899da1` fix dissected in §9. |

If any missing after pull: the commit didn't reach this PC. Re-pull.

### 📌 Exam format

Oral exam, 5 min presentation + Q&A. Mads's plan:
- **Present:** the IDC state machine + signal flow for **BRZ**, using the LaTeX disposition. Trace RAM → IR → IDC (sees opcode + Z flag) → PS-signal → PC. Show the Mealy decision logic explicitly.
- **Q&A:** questions about the rest of the project (Datapath, FU, memory subsystem, microcode programs, design decisions).

Hub §6 ("Discrepancies & gotchas") + the disposition's §5 talking points are the script for Q&A.

### 🚩 THREE EXAM GOTCHAS (always worth memorising — these come up)

1. **AND/OR opcode swap.** Team's hardware: `OR = 0001000, AND = 0001001`. Textbook (Mano/Kime pp.490, 493) + Java assembler + lecture-10 slide 9: opposite. **The PWF spec footnote on page 1 acknowledges the textbook discrepancy.** Use `dsdasm` (team's Python assembler), NOT the Java tool — Java emits wrong opcodes for AND/OR.

2. **3-bit LDI immediate limit.** `LDI` can only load 0..7 (3-bit field zero-extended). For higher values (e.g. 0xFA = MR2/LEDs), use:
   ```asm
   NOT R2 R4         ; R2 = NOT 0 = 0xFF (R4 is 0 after reset)
   LDI R4 5          ; R4 = 5
   SUB R3 R2 R4      ; R3 = 0xFF - 5 = 0xFA → addresses LEDs
   ```

3. **BRZ/BRN test R[SA], NOT the previous instruction's flag.** Z/N are *combinational* outputs of the FU. In BRZ's EX0, the IDC defaults route `R[SA]` through the ALU (pass-A, FS=0000), and the resulting Z is what the IDC samples. So `BRZ A1, off` literally means "if R1 == 0, branch" — NOT "if the previous result was 0". To branch on an earlier op's result, put the destination in BRZ's SA slot: `add D2 A1 B3 ; brz A2, target`.

### 🚩 The hardware bug discovered 27-May-2026

`team/PWF/sources/hdl/PortReg8x8.vhd:71` writes MR1 from `Data_In(15 downto 8)`, but `Zero_Filler_2` always pads those bits to 0. **So any `ST` to address 0xF9 always writes 0 — the left two 7-seg digits cannot show non-zero data on the as-submitted hardware.** The team's `addsub_calc.asm` comment notes this cryptically (*"MR1 er reelt altid 0 pga. Zero_Filler_2"*) but never fixed it. One-line fix: change `Data_In(15 downto 8)` to `Data_In(7 downto 0)` matching MR0/MR2. Documented in detail in chat history (was found while testing a `show_a_b.asm` program). Good exam talking-point: "tell me about a design decision that turned out to be wrong".

### 🚩 The b899da1 IDC fix (Jonas, 13-May-2026, in team repo)

A real correctness fix late in the project. Two bugs:
- **EX2 had `BX` defaulted to the imm-field** instead of pointing at R8 — the Shifter was shifting the wrong register, SRM produced garbage. Fix: explicit `BX <= "1000"` in EX2.
- **EX1 had no Z-check** — `srm Rd Rs 0` (shift by 0) would decrement R9 from 0 to 0xFF and loop 256 extra cycles before terminating. Fix: add Z-check, exit to INF when imm=0.

Same commit enforced a "be explicit per state" discipline: changed default `next_state <= INF` to `next_state <= current_state`, so forgotten transitions get stuck visibly instead of silently falling through to fetch. Hub §6.11 + `EX — Instruction SRM.md §9` have the full story.

### Memory pointers

- [`project_62711_exam_prep_hub`](.claude/projects/.../memory/) — index of where the exam-prep folder lives, decisions locked in
- [`reference_notebooklm_ids`](.claude/projects/.../memory/) — 62711 notebook UUID = `eb1f49b9-61a5-4494-8a3e-9821f8514324`
- [`feedback_use_mermaid`](.claude/projects/.../memory/) — prefer mermaid diagrams over ASCII art in Obsidian notes

### Workflow conventions (follow these)

- **Hints-first.** "let's go through X" → small hint, STOP, wait. Full walkthrough only on explicit "walk me through it / do it for me".
- **Mermaid > ASCII** in Obsidian notes (per `feedback_use_mermaid` memory).
- **Conversational English** in Obsidian study notes. **Danish** in the LaTeX disposition and team .asm comments (matches the team's report and oral exam target).
- **NotebookLM:** `C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id eb1f49b9-61a5-4494-8a3e-9821f8514324` for fact-checking against ingested 62711 course material. Re-`login` if `auth-status` says NOT AUTHENTICATED; intermittent read-timeouts — retry.
- **VHDL truth source:** `C:\Users\Mads2\DTU\4. Semester\Digital Systems Design\team\` — separate git repo (see "Team repo" below). For VHDL questions, this is the canonical source; the spec and lecture slides come second.
- **Commits:** NEVER add `Co-Authored-By: Claude` or any AI mention. Commit messages read like a developer wrote them.

### Team repo (separate git repo, not part of DTU umbrella)

`C:\Users\Mads2\DTU\4. Semester\Digital Systems Design\team\` is the team's VHDL repo (`gigurd/Design-of-digital-systems-62711` on GitHub). Separate from this DTU umbrella repo.

Branch state (as of 27-May-2026): on `feature/tb-asm-examples`, fully merged into `origin/main` (PR #36). Local `main` fast-forwarded to match.

**Uncommitted in team repo (might or might not need pushing depending on what you want):**
- `PWF/tools/asm/examples/show_a_b.asm` — demo program writing A to MR0 and B to MR1. Exposes the PortReg8x8 MR1 bug (the left 2 digits stay at 00 even with this program because of the Zero_Filler_2 / PortReg(15:8) mismatch).
- `PWF/tools/asm/examples/btnl_test.asm` — diagnostic that echoes BTNL latch (MR4) to the LEDs. Verifies BTNL hardware path independently.
- `PWF/sources/hdl/Ram256x16.vhd` — patched `INIT_00` (with whichever .asm was last loaded via `dsdasm.py asm --vhdl`).

If you want these on the other PC: `cd` into the team repo and `git add` them explicitly, then commit + push.

### Known repo issue

~~Broken nested git repo under the LCD1 `regbot/Report` path made repo-wide `git add -A` abort.~~ **Resolved 26-Aug-2026** — that folder no longer exists and `git add -A` works repo-wide. See REPO CONVENTIONS above.

---

## ARCHIVED: 62743 DSP Re-exam — DONE (exam Wed 20-May-2026, code E2-B)

Still relevant as workflow reference. Assets live in:
- Hub: `Obsidian/Courses/62743 Digital Signal Processing (Reexam)/62743 Digital Signal Processing (Reexam).md`
- Exam skeleton: `3.semester/DSP/EXAMS/F26.m`
- Reference solutions: `3.semester/DSP/EXAMS/{E25_new,F24,F25_new,F23,F20,E19,E20,E22,F21}.m`
- Q1 cookbook: `Obsidian/.../Notes/Reference/Q1 via MATLAB cookbook.md`
- Helpers: `3.semester/DSP/Helpers/` (FIR_fourier, FIR_window, MK_values, …)
- Publisher: `3.semester/DSP/pretty.bat` (+ `publish_pretty.py`)

DSP-specific conventions still in force if returning to DSP material:
- MATLAB comments in Danish with real `øæå`. Answers as bare `%%` then `% *Svar N-M:* …`.
- DTU notation: `Ω`=analog rad/s, `ω`=digital rad/sample, `f`=normalized `F/Fs`. `freqs`→rad/s; `bilinear`/`freqz`→Hz.
- NotebookLM for DSP: same `nlm.bat` script, `--notebook-id 5bd40a62-b09c-406d-b854-2ed2be6d894c` (or shortname `dsp`).
- Official `*student solutions*.pdf` = absolute truth (supersedes NotebookLM).
