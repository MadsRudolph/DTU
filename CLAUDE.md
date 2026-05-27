# CLAUDE.md — repo handoff

Auto-loaded by Claude Code, travels with `git pull`. Records **where to pick up** so a fresh session on any PC continues seamlessly.

---

## ACTIVE WORK: 62711 Digital Systems Design — oral exam Thu 28-May-2026

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

Broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` makes repo-wide `git add -A` abort. **Stage 62711 work by explicit path** (typically the whole `Obsidian/Courses/62711 .../Exam Prep/` folder + `CLAUDE.md`). Do not fix the broken submodule without explicit go-ahead.

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
