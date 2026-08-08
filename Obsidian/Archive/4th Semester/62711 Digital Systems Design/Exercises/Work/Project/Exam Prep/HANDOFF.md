---
tags: [62711, exam-prep, handoff]
course: 62711 Digital Systems Design
purpose: Bootstrap a fresh Claude Code session for 62711 oral exam prep
updated: 2026-05-27
---
# HANDOFF — 62711 Exam Prep (paste me into a fresh Claude session)

## TL;DR

Mads has his **62711 Digital Systems Design oral exam on Thursday 28-May-2026** (i.e. tomorrow as of this writing). He is in final prep. Your job: help him rehearse, answer architecture questions, and fix any last issues. Be **hints-first** unless he says "walk me through it" or "do it for me".

Everything lives in:
`Obsidian/Courses/62711 Digital Systems Design/Exercises/Work/Project/Exam Prep/`

The single entry point is **`00 PWF System — Exam Hub.md`**.

---

## What the project is

An **8-bit microprocessor** built in structural VHDL on a Digilent Nexys 4 DDR FPGA, in three sub-projects:
- **PWA** = Datapath (16×8 Register File + Function Unit: ALU + Shifter + flags)
- **PWB** = Microprogram Controller (Program Counter + Instruction Register + Sign Extender + Zero Filler + the IDC state machine)
- **PWF** = the final integrated system (PWA + PWB + 256×16 RAM + 8×8 memory-mapped Port Register + the MUX M / MUX MR / Zero Filler 2 glue + 7-seg driver)

Instructions are 16-bit words. The 7-bit opcode is `IR(15:9)`. The IDC is a **Mealy FSM** (states INF, EX0, EX1, EX2, EX3, EX4) that emits a 28-bit control word each cycle.

**VHDL truth source** (separate git repo): `C:\Users\Mads2\DTU\4. Semester\Digital Systems Design\team\` — `gigurd/Design-of-digital-systems-62711`. For any VHDL question this is canonical; spec + lecture slides come second.

---

## The exam plan

- **Format:** 5-minute presentation, then Q&A on the rest of the project.
- **Presentation topic:** the IDC state machine + signal flow for a **BRZ** (Branch on Zero) instruction. Trace: RAM → IR → IDC (sees opcode + Z flag) → PS signal → PC. Show the Mealy decision logic (Z=1 → PS=10 → branch; Z=0 → PS=01 → PC+1).
- **Presentation aid:** `disposition_idc_regfile.tex` (1-page LaTeX, BRZ-focused). Compile with `pdflatex disposition_idc_regfile.tex` (twice for cross-refs).
- **Q&A script:** Hub §6 "Discrepancies & gotchas" + the disposition's talking-points section.

---

## Assets (all in the Exam Prep folder)

| File | What it is |
|---|---|
| `00 PWF System — Exam Hub.md` | **Master doc.** System overview, block-by-block architecture, instruction-set table, 6 worked microcode walkthroughs (all mermaid diagrams), §6 discrepancies/gotchas, §8 exam-readiness checklist. |
| `disposition_idc_regfile.tex` | 1-page LaTeX presentation disposition. BRZ-focused: FSM mini-diagram + RAM→IR→IDC→PC signal flow + 2-cycle walkthrough + 6 talking points. (Filename is legacy — content is IDC FSM, not Register File.) |
| `STUDY — 01 PWA.md` | The "explain it simply" Datapath note. Three-things-in-a-loop, MUX B = immediate gate, MUX D = memory gate, plus the two-cycle "where does an immediate come from?" deep-dive. |
| `EX — Microprocessor (top).md` | Full top-level VHDL + diagram trace. Every walkthrough references it. |
| `EX — Instruction {ADD,LD,JMP,BRZ,LDI,SRM}.md` | Cycle-by-cycle per instruction. SRM §9 has the `b899da1` fix dissected. |
| `EXAM_PREP_INVENTORY.md` | Phase-0 inventory + per-note trust assessment. |
| `FACT_CHECK_REPORT.md` | 5 confirmed errors + 5 ambiguities, cross-checked vs VHDL + spec + lecture-10 + NotebookLM. |

---

## The three exam gotchas (he WILL be asked about these)

1. **AND/OR opcode swap.** Team hardware: `OR = 0001000`, `AND = 0001001`. Textbook (Mano/Kime pp.490,493) + Java assembler + lecture-10 slide 9 use the opposite. The PWF spec footnote (page 1) acknowledges the textbook discrepancy. **Use `dsdasm`** (the team's Python assembler), not the Java tool, to assemble programs.

2. **3-bit LDI immediate limit.** `LDI` loads only 0..7. For bigger values (e.g. 0xFA for the LED port):
   ```asm
   NOT R2 R4         ; R2 = NOT 0 = 0xFF  (R4 is 0 after reset)
   LDI R4 5          ; R4 = 5
   SUB R3 R2 R4      ; R3 = 0xFF - 5 = 0xFA
   ```

3. **BRZ/BRN test R[SA], NOT the previous instruction's flag.** Z/N are *combinational* outputs of the Function Unit. In BRZ's EX0, the IDC defaults route R[SA] through the ALU (pass-A, FS=0000), and the resulting Z is what gets sampled. So `BRZ A1, off` means "if R1 == 0, branch", NOT "if the previous result was 0". To branch on an earlier op's result, put that destination in BRZ's SA slot: `add D2 A1 B3 ; brz A2, target`.

---

## Two deep design-story talking points

### The b899da1 IDC fix (Jonas, 13-May-2026)
A real late correctness fix. (a) EX2 had BX defaulted to the imm-field instead of R8, so the Shifter shifted the wrong register → SRM produced garbage. Fix: explicit `BX <= "1000"` in EX2. (b) EX1 had no Z-check, so `srm Rd Rs 0` looped ~256 extra cycles. Fix: add Z-check. Same commit changed the default `next_state <= INF` to `next_state <= current_state` to force explicit per-state transitions. Full story: Hub §6.11 + `EX — Instruction SRM.md §9`.

### The PortReg8x8 MR1 hardware bug (found 27-May)
`team/PWF/sources/hdl/PortReg8x8.vhd:71` writes MR1 from `Data_In(15 downto 8)`, but `Zero_Filler_2` always pads those bits to 0. **So any `ST` to address 0xF9 always writes 0 — the left two 7-seg digits can't show non-zero data on the as-submitted hardware.** One-line fix: change to `Data_In(7 downto 0)` like MR0/MR2. The team's `addsub_calc.asm` comment cryptically notes this (*"MR1 er reelt altid 0 pga. Zero_Filler_2"*) but never fixed it. Great answer to "tell me about a design decision that turned out wrong". Discovered while testing `show_a_b.asm` (a program that tries to show two independent bytes on all 4 digits).

---

## Open items / where you might pick up

- [ ] **Verify the disposition compiles + looks right.** Mads had TikZ render issues earlier (fixed by removing `\\`-without-`align=center` and trapezium+rotate). Confirm `pdflatex disposition_idc_regfile.tex` produces a clean 1-page PDF with both diagrams visible.
- [ ] **Rehearse the 5-min presentation.** Time it. If long, cut the b899da1 anecdote and compress the fetch-cycle description.
- [ ] **(Optional) Decide on the MR1 bug:** fix the VHDL (one line) + re-synth, or just keep it as a Q&A talking point. Mads leaned toward keeping it as a talking point.
- [ ] **(Optional) More STUDY notes.** Only PWA has a simple `STUDY — 01 PWA.md`. PWB (the MPC/FSM) and PWF (memory subsystem) don't have simple companions yet. We were mid-way through walking the PWA components when this handoff was written (covered: Datapath overview, all ports, the immediate path; not yet deep-dived: Register File internals, Function Unit internals).
- [ ] **(Optional) Team repo .asm files.** `show_a_b.asm` and `btnl_test.asm` are uncommitted in the team repo (`PWF/tools/asm/examples/`). Commit there separately if wanted — they're not in the DTU umbrella repo.

---

## How Mads works (conventions — follow these)

- **Hints-first.** "Let's go through X" → give a small hint, then STOP and wait. Full walkthroughs only on explicit "walk me through it / do it for me".
- **Mermaid > ASCII** in Obsidian notes. He can't see ASCII art well; mermaid renders in Obsidian. Use `stateDiagram-v2`, `flowchart`, `sequenceDiagram` where they help.
- **Language:** conversational **English** in Obsidian study notes; **Danish** in the LaTeX disposition and team `.asm` comments (matches the exam target + the team's report).
- **Commits:** NEVER add `Co-Authored-By: Claude` or any AI mention. Commit messages read like a developer wrote them. He commits direct to `main` on the DTU umbrella repo (personal repo).
- **Ask before large/destructive actions.** Use AskUserQuestion for genuine forks. Don't blanket-commit; he has unrelated dirty files in the DTU repo — stage by explicit path.

---

## Tools & references

- **NotebookLM (62711 course material):**
  `C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id eb1f49b9-61a5-4494-8a3e-9821f8514324`
  Use for fact-checking claims against ingested course material. Re-`login` if `auth-status` says NOT AUTHENTICATED; it intermittently read-times-out — just retry. (Note: lecture *slide decks* are NOT all ingested — verify slide claims by reading the PDFs in `Slides/` directly.)
- **dsdasm** (team's Python assembler): `team/PWF/tools/asm/dsdasm.py`. `python dsdasm.py asm prog.asm --vhdl ../../sources/hdl/Ram256x16.vhd` patches a program into the RAM. `python dsdasm.py run prog.asm --trace` simulates. GUI: `python dsdasm_gui.py`.
- **Architecture diagram:** `Obsidian/Courses/62711 Digital Systems Design/Exercises/Work/Project/architecture.pdf`. The canonical visual. Has 3 red-numbered super-blocks: 1 = Datapath, 2 = MPC, 3 = memory subsystem.
- **Spec PDFs:** same Project folder — `62711_ProjectWork_{A,B,F}_F2026.pdf`.
- **DTU umbrella repo:** `C:\Users\Mads2\DTU` (this repo). Has the auto-loaded `CLAUDE.md` with the same context.
- **Known repo issue:** a broken nested git repo under `Obsidian/Courses/34722 .../regbot/Report` makes repo-wide `git add -A` abort. Stage 62711 work by explicit path.

---

## First thing to do in a new session

1. Read `00 PWF System — Exam Hub.md` (the master doc).
2. Skim `disposition_idc_regfile.tex` (what he'll present).
3. Ask Mads what he wants to work on — most likely: rehearse the BRZ presentation, drill a specific component, or compile/polish the disposition.
4. Stay hints-first.
