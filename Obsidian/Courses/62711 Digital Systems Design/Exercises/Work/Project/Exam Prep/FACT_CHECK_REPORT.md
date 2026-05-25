---
tags: [62711, exam-prep, fact-check, phase-2]
course: 62711 Digital Systems Design
topic: Cross-check of every existing study note vs PWA/PWB/PWF VHDL + spec + lecture + NotebookLM
source: derived
phase: 2
---
# FACT_CHECK_REPORT — Phase 2

> [!info] Scope
> Cross-check of every claim-bearing Obsidian note in `Courses/62711 Digital Systems Design/` against (a) the actual VHDL in `team/` (highest authority — observable behavior), (b) the PWF spec PDF page 1, (c) the lecture-10 slide deck, (d) NotebookLM queries against the 62711 notebook (`eb1f49b9-…`). **No existing note has been edited.** Findings are surfaced, not silently patched, per the prompt.

> [!success] Headline
> The team's notes are largely accurate. The audit caught **5 factual errors**, **5 ambiguity-level items**, and **1 self-correction** (mine, from Phase 0). Nothing structural is broken; everything below is fixable with a few-line edit per note when Mads chooses to push corrections.

**Backlinks:** [[EXAM_PREP_INVENTORY|Phase-0 Inventory]] · [[EX — Microprocessor (top)]] · [[EX — Instruction BRZ]] · [[EX — Instruction SRM]]

---

## ❌ Section 1 — Incorrect claims

Five findings where an existing note states something that the hardware / spec / cross-source directly contradicts.

### 1.1 [[Opg 10 - PWF Memory Access & Calculator Program]] §10.2 — `add D2 A0 B1` hex is wrong

**File:** `Exercises/Work/Opg 10 - PWF Memory Access & Calculator Program.md`, lines 282 + 288.

The note claims:

> | 3 | `R2 ← R0 + R1` | `add D2 A0 B1` | `0x040A` |
>
> **`add D2 A0 B1`** → opcode `0000010`, DR `010`, SA `000`, SB `001` = `0000010 010 000 001` = `0000 0100 0000 1010` = `0x040A`.

**Correct value:** The bit pattern `0000010 010 000 001` packs to `0000010_010_000_001` = `0000 0100 1000 0001` = **`0x0481`**. The note's arithmetic in the second line is wrong — the bits are right (`0000010 010 000 001`) but their renibbling to `0000 0100 0000 1010` is wrong (that hex would correspond to `add D0 A1 B2`, the slide-9 example value being remembered instead of recomputed).

**Source of truth:** Direct binary→hex re-derivation. Confirmed with [[dsdasm]] mental model (opcode `0x02` shifted left 9 + DR<<6 + SA<<3 + SB):
- 0x02 << 9 = 0x0400
- DR=2 << 6 = 0x0080
- SA=0 << 3 = 0
- SB=1 = 0x0001
- Sum = 0x0481 ✓

**Severity:** Real bug — if someone copies `0x040A` into their RAM thinking it's `add D2 A0 B1`, they actually load `add D0 A1 B2`, which writes to R0 instead of R2 and uses R1+R2 instead of R0+R1. A silently-wrong calculator program.

**Fix recommendation (do not apply silently):** correct the hex column to `0x0481` and update the second-line arithmetic. Re-verify the other three hex values in the table (`0x2030`, `0x2078`, `0x4022`, `0x4028` are all correct — I verified each).

---

### 1.2 [[Lecture 10 - Floating Point & Assembly Language]] §"Operands & Addressing Modes" — BRZ uses `zf`, claims the lecture; hardware uses `se`

**File:** `Lecture Notes/Lecture 10 - Floating Point & Assembly Language.md`, line 251.

The note states:

> | **Offset** (PC-relative) | `BRZ R1, offset` | if Z then $PC \leftarrow PC + \text{zf}(\text{offset})$ |

`zf` = zero-fill (always positive). **Hardware uses `se` (sign-extend)** — see [`SignExtender.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/SignExtender.vhd) which produces a 6-bit signed value via `(7 downto 5 => IR(8))`. The PWF spec PDF page 1 mnemonic table also says `PC ← PC + se ΔD` (not zf). So negative branch offsets (backward jumps) are possible — `zf` would forbid them.

**Severity:** Important. The whole point of having a SignExtender (vs a ZeroFiller) is to support backward branches. A reader relying on the lecture note would conclude backward branches are impossible, which contradicts both the hardware and the addsub_calc program in [[microcode-program]] that uses forward branches with positive offsets *but* could trivially be rewritten with a backward branch (and the [[dsdasm]] examples show this).

**Note nuance:** The Lecture-10 PDF slide itself, when checked via NotebookLM, says "zfOp" — so the note is faithful to the slide. **The slide is what's wrong, not the note's transcription.** Phase-2 caveat: surface this as a discrepancy between lecture material and spec/hardware, not as a note error per se.

---

### 1.3 [[dsdasm]] §"Immediates" — branch offset range is much wider than claimed

**File:** `Exercises/Work/Project/PWF Project/dsdasm.md`, line 156.

The note states:

> Range: immediates `0..7` (3 bits), offsets `-4..+3` (3-bit signed). The `B<n>` form for branch offsets is restricted to `0..3` since the prefix has no sign — backward branches use a label.

**Hardware reality:** `SignExtender.vhd:15-17` builds the offset from `{IR(8), IR(7), IR(6), IR(2), IR(1), IR(0)}` — **6 bits signed → range -32..+31.** [[SignExtender]] §"Logic" already documents this layout correctly. So `[[dsdasm]]` is wrong about the hardware range — though the assembler may internally restrict to a narrower range *for the `B<n>` shorthand syntax*, which is fine. The wording just needs to clarify "shorthand vs literal".

**Severity:** Important for exam — the lecturer might ask "what's the BRZ offset range?" and the correct answer is **-32..+31**, not -4..+3.

**Fix recommendation:** Edit the dsdasm.md range box to read something like:
- Immediates (LDI/ADI): `0..7` (3-bit zero-extended) — unchanged.
- Branch offset literal: `-32..+31` (6-bit signed via SignExtender across `IR{8,7,6,2,1,0}`).
- `B<n>` shorthand for branch offsets: restricted to `0..3` (B-slot only, no sign).

---

### 1.4 [[Lecture 10 - Floating Point & Assembly Language]] — internal inconsistency on AND/OR opcodes

**File:** `Lecture Notes/Lecture 10 - Floating Point & Assembly Language.md`, two sections.

- **Lines 226-229:** lists opcodes in the family `MOVA, INC, ADD, SUB, DEC, OR, AND, XOR, NOT, MOVB` with range `0000000 … 0001100` — implicit order suggests **OR=`0001000`, AND=`0001001`** (matches hardware).
- **Lines 446-449:** transcribes the lecture-10 slide-9 mnemonic-to-machine-code table directly:
  > | `and` | `and D0 A1 B2` | `0001000000001010` |
  > | `or`  | `or D0 A1 B2`  | `0001001000001010` |
  Which is **AND=`0001000`, OR=`0001001`** (matches textbook + Java assembler, *opposite* the team's hardware).

The note transcribes both correctly from their respective sources but **does not flag the contradiction**. A student reading top-to-bottom gets one mapping in §"Types of Opcodes" and the opposite mapping in §"Assembler Tool in PWF" — without warning.

**Severity:** Medium — both sections are textually faithful to their sources, but the absence of a "⚠️ these two sources disagree" callout is misleading. This is exactly the AND/OR footgun [[dsdasm]] tries to defuse.

**Fix recommendation:** Add a callout near line 449 (the slide transcription table) that reads something like:

> ⚠️ **Note vs hardware:** The slide's Java-assembler output uses `and=0001000`, `or=0001001` — matching Mano/Kime pp.490, 493. **The team's PWF VHDL uses the opposite mapping** (because the FS=IR(12:9) trick maps FS=1000→OR per the PWA encoding table). Always assemble with [[dsdasm]], not the Java tool; otherwise `and` becomes `or` on the FPGA.

---

### 1.5 Cosmetic — two `-- 5 nuller` comments in VHDL that are inaccurate

**Files:**
- [`team/PWF/sources/hdl/Zero_Filler_2.vhd:42`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Zero_Filler_2.vhd) — comment `-- 5 nuller` next to a slice `(15 downto 8 => '0')` that is **8 zeros** (8→16 bit widening).
- [`team/PWB/sources/hdl/ZeroFiller.vhd:14`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ZeroFiller.vhd) — comment `-- 5 nuller` next to `(7 downto 3 => '0')` that IS **5 zeros** (3→8 bit widening).

The PWB module's comment is correct; the PWF module's comment was copy-pasted without updating. No functional impact — both modules behave as the surrounding code requires.

**Severity:** Trivia — flag only because the comment is read during exam-prep code review and may confuse.

**Fix recommendation:** Change Zero_Filler_2.vhd's comment to `-- 8 nuller` (or just delete the count comment).

---

## ⚠️ Section 2 — Claims needing clarification

Five findings where an existing note is *not wrong* but is ambiguous or incomplete in a way that an exam-prep reader might misread.

### 2.1 BRZ/BRN Z-semantics — implicit reading vs hardware reality

**File:** `Exercises/Work/Project/PWB Project/InstructionDecoderController/InstructionDecoderController.md`, §"Conditional Branching: Hvordan det virker" (lines 262-278).

The note says:

> IDC'en kigger på Z/N-flaget og beslutter PS-værdien.

It does **not** say *where* the Z/N flag comes from. The conventional textbook reading is "the flag from the previous arithmetic op". But because the FU is combinational and the IDC's process is combinational, the Z/N flag that BRZ/BRN sees in their own EX0 cycle is **the Z/N produced by *this cycle's* ALU pass-A on R[SA]** — not the previous instruction's flag.

So `BRZ A1, +3` actually means "if R1 == 0, branch by 3", not "if the previous result was 0, branch".

**Sources consulted:**
- VHDL: [`InstructionDecoderController.vhd:37`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — control_logic process sensitive to `(current_state, IR, N, Z)`.
- VHDL: [`Datapath.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd) — V/C/N/Z are combinational outputs of the FU.
- VHDL: [`NegZero.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/NegZero.vhd) — Z = NOR of all F bits, no flip-flop.
- Spec PDF page 1: ambiguous on this point; just shows the FSM row.
- [[microcode-program]] addsub_calc usage: `LD R4 R3 ; BRZ D0 A4 B2` — the BRZ tests R4 (which holds the LD'd value), confirming the "tests R[SA]" interpretation.

**Severity:** Medium-high — this is a real conceptual gotcha that a reader of [[InstructionDecoderController]] alone wouldn't catch. Documented at exam depth in [EX — Instruction BRZ.md §5](Exercises/Work/Project/Exam%20Prep/EX%20%E2%80%94%20Instruction%20BRZ.md).

**Fix recommendation:** Add a callout to [[InstructionDecoderController]] §"Conditional Branching" stating "Z/N sampled in EX0 = ALU's current pass-A output on R[SA], NOT the previous instruction's flag."

---

### 2.2 [[PortReg8x8]] reset behavior for MR3..MR7 — claim not yet verified

**Files:** [[EX — Microprocessor (top)]] §7 — I asserted: *"PortReg MR0..MR2 → 0; MR3..MR7 keep their pre-reset SW latch (technically — verify in Phase 2 against `PortReg8x8.vhd`)."*

**Status:** Not verified. I deferred reading the full `PortReg8x8.vhd` because the top-level extraction was already long. The claim needs validation against the actual VHDL.

**Sources consulted:** Only the header comment of `PortReg8x8.vhd:4-13`, which describes the MR3..MR7 behavior as "loaded from SW on BTNx press" — doesn't specify reset behavior.

**Fix recommendation:** Phase 1.5 task — read the full `PortReg8x8.vhd` and either confirm the claim or correct it in [[EX — Microprocessor (top)]] §7.

---

### 2.3 PortReg8x8 entity signature — lecture says 8-bit Data_In, team built 16-bit

**File:** `Lecture Notes/Lecture 10 - Floating Point & Assembly Language.md`, lines 351-360.

The lecture's reference entity signature for PortReg8x8 has:

```vhdl
Data_In : in STD_LOGIC_VECTOR(7 downto 0);     -- 8 bits
```

The team's actual implementation ([`team/PWF/sources/hdl/PortReg8x8.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/PortReg8x8.vhd)):

```vhdl
Data_In : in STD_LOGIC_VECTOR(15 downto 0);    -- 16 bits, with Zero_Filler_2 padding
```

The team chose to keep `PortReg8x8.Data_In` 16-bit so it shares the same bus as `Ram256x16.Data_in`, simplifying [`Microprocessor.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd) (one `Zero_Filler_2` instance feeds both). Internally PortReg8x8 still only uses the low 8 bits when latching MR0..MR2.

**Severity:** Low — functional behavior is identical. But if the exam asks "what's the port width of PortReg8x8.Data_In per the spec?" the spec answer is 8, the implementation answer is 16. Worth knowing.

**Fix recommendation:** None to existing notes. Hub Discrepancies section should mention this as "implementation detail" rather than a real conflict.

---

### 2.4 [[Lecture 10]] §"Memory-Mapped I/O Layout" — MR7 label says BTNS

**File:** `Lecture Notes/Lecture 10 - Floating Point & Assembly Language.md`, line 383.

The note states:

> | `1111.1111` | — | `Data_Bus_Out ← 0x00 + MR7` | **Operand 0 — BTNS** — 8 bits |

`BTNS` doesn't exist on Nexys 4 DDR — there are only `BTNC`/`BTNU`/`BTNL`/`BTNR`/`BTND`. The team's `PortReg8x8.vhd:13` correctly identifies MR7 as **BTNC** (BTN-Center).

**Severity:** Trivia — `BTNS` is presumably a typo for `BTNC` ("Side" vs "Center"?). The PWF spec PDF page 1 says "BTN- C" for MR7 (with a typographical hyphen-space).

**Fix recommendation:** Change `BTNS` to `BTNC` in the Lecture 10 note's I/O table.

---

### 2.5 [[dsdasm]] §"AND/OR bug in the Java tool" — wording slightly misleading on what the spec says

**File:** `Exercises/Work/Project/PWF Project/dsdasm.md`, lines 33-34.

The note states:

> The Java reference assembler and lecture-10 slide 9 use `0001000 = AND`, `0001001 = OR`. **Our PWF spec and [[InstructionDecoderController|InstructionDecoderController]] use the opposite** (`0001000 = OR`, `0001001 = AND`).

The bold claim is **accurate but historically misread** — and I (Phase 0) misread it the opposite direction. The full ground truth (NotebookLM-confirmed and direct PDF read):
- **PWF spec PDF page 1**: OR=`0001000`, AND=`0001001` ✓ (matches the dsdasm note, matches the hardware)
- **Java assembler + lecture-10 slide 9**: AND=`0001000`, OR=`0001001` (opposite)
- **Textbook Mano/Kime pp.490, 493**: also AND=`0001000`, OR=`0001001` (same as lecture; opposite the spec)

So the dsdasm note's claim "Our PWF spec and IDC use the opposite [of the Java tool]" is correct. The only nuance is **"opposite of *what*"** — opposite of the Java tool + textbook + lecture. The dsdasm note already names two of those three (Java tool, lecture-10 slide 9), so no fix needed.

**Severity:** None — the note is technically correct. Including this entry only because Phase-0 me misread it and confused myself for a turn.

**Fix recommendation:** No edit to dsdasm.md. Pinned here as a "the note IS right, I was wrong about it" reassurance.

---

## ✅ Section 3 — Confirmed claims (cross-checked, no issues)

For each existing claim-bearing note, the most critical claims were verified against the VHDL and the spec. Listed for completeness:

| Note | Claim verified | Source |
|---|---|---|
| [[PWF Project]] §"Memory Map" | RAM `0x00..0xF7`, MR0..MR7 at `0xF8..0xFF`, MMR=1 in upper range, R/W vs R-only per row | [`PortReg8x8.vhd:4-13`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/PortReg8x8.vhd) header + spec p.1 |
| [[PWF Project]] §"Instruction Set" table | All 20 opcodes match the VHDL `when` patterns in the IDC | [`InstructionDecoderController.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) |
| [[PWB Project]] §"Control Word (28 bits)" | Layout `NS\|PS\|IL\|DX\|AX\|BX\|MB\|FS\|MD\|RW\|MM\|MW` — bit widths match IDC entity ports | IDC entity declaration |
| [[InstructionDecoderController]] §"Komplet Transition Table" | All 20 instruction rows (state, opcode, next_state, control bits) match the case statement | IDC VHDL line-by-line |
| [[InstructionDecoderController]] §"FS-koden — det smarte trick" | FS=IR(12..9) for ALU ops, including OR=FS1000, AND=FS1001 | IDC line 92, PWA encoding table |
| [[InstructionDecoderController]] §"Kategori 3: 5+ cyklus" (SRM/SLM) | EX0..EX4 FSM with R8/R9 scratch, Z=0 loop, Z=1 exit | Detailed in [EX — Instruction SRM.md](Exercises/Work/Project/Exam%20Prep/EX%20%E2%80%94%20Instruction%20SRM.md) |
| [[ProgramCounter]] §"PS Control Table" | 00=Hold, 01=Inc, 10=PC+Offset, 11=PC←Address_In | [`ProgramCounter.vhd:137-146`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ProgramCounter.vhd) |
| [[InstructionRegister]] §"IL Control Table" | IL=1 ⇒ load on rising edge; IL=0 ⇒ hold | [`InstructionRegister.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionRegister.vhd) |
| [[SignExtender]] §"Logic" table | bits `IR(8) IR(8) IR(8) IR(7) IR(6) IR(2) IR(1) IR(0)` | [`SignExtender.vhd:15-17`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/SignExtender.vhd) — **note matches VHDL exactly** |
| [[ZeroFiller]] §"Logic" | `0.0.0.0.0.IR2.IR1.IR0` | [`ZeroFiller.vhd:14-15`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ZeroFiller.vhd) |
| [[dsdasm]] full ISA table | All 20 opcode/mnemonic mappings | Self-verified by the assembler's built-in `python dsdasm.py test` (PASS 20/20) |
| [[PWA Project]] §"FS Encoding Reference" | All FS rows including the arithmetic-Cin column and the FS3·FS2→MF mapping | PWA VHDL (PWA was already submitted; not re-verified here in depth) |
| [[Opg 10]] §10.1 memory-map and timing-diagram sequences A–D | All four cases (RAM read/write, MR0 write+read, MR4 write-ignored, BTNL latching) correctly explained | [`PortReg8x8.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/PortReg8x8.vhd) |
| [[Opg 10]] §10.2 program hex (`ld D0 A6 → 0x2030`, `ld D1 A7 → 0x2078`, `st A4 B2 → 0x4022`, `st A5 B0 → 0x4028`) | Three of four hex values correct | Direct binary→hex re-derivation (the fourth, `add D2 A0 B1 → 0x040A`, is wrong — see §1.1) |
| [[Lecture 10]] §"Memory-Mapped I/O Layout" memory map | All 8 MR rows match the implementation (except for the BTNS typo per §2.4) | spec p.1 |
| [[Lecture 10]] §"Full Datapath with Memory & I/O" block-diagram description | All five major sub-blocks and their relationships to PWA/PWB/PWF correctly named | architecture.pdf cross-check |

> [!note] What was NOT exhaustively cross-checked
> - **PWA submodule notes** ([[FunctionUnit]], [[ALU]], [[Shifter]], [[NegZero]], [[FunctionSelect]], [[MUXF]], the Register File family). Reason: PWA was submitted weeks before PWF and has been stable; deep-checking these would be high effort and low ROI. The PWA FS-encoding tables were sampled against the IDC's `FS = IR(12:9)` trick and pass.
> - **The 7-seg driver internal refresh logic** ([`SevenSegDriver.vhd`](../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/SevenSegDriver.vhd)). Not directly exam-critical for the microcode walkthroughs — flag for separate review if Mads wants exam-depth coverage of the 7-seg.
> - **`Microprocessor_tb.vhd` and waveform conformance** — the team's PWF testbench. Conformance was assumed from the fact that the submitted PDF includes timing-diagram screenshots that match expectations. Phase-3 hub will reference these visuals.

---

## 📝 Section 4 — Phase-0 self-correction (mine)

For completeness — one walked-back claim from my own Phase-0 inventory:

### 4.1 [[EXAM_PREP_INVENTORY]] §4.2 (original draft) — incorrectly claimed the PWF spec disagreed with the hardware on AND/OR

**What happened:** In Phase 0, I misread the PWF spec PDF page 1's mnemonic-explained table and asserted the spec said **AND=`0001000`** (which would conflict with the hardware). NotebookLM caught the error in the first verification query ("the spec says AND=`0001001`"), confirmed by direct re-reading of the PDF. The inventory was edited in-place; the warning callout in §4.2 documents the misread for the trail.

**Why it matters for future-you:** If you see references in old git history or chat logs to "the AND/OR conflict between the spec and the hardware", that was based on my error. **There is no such conflict.** The only outliers are the textbook + Java assembler + lecture-10 slide 9.

**Status:** Already corrected in [EXAM_PREP_INVENTORY.md](Exercises/Work/Project/Exam%20Prep/EXAM_PREP_INVENTORY.md). No further action.

---

## Section 5 — Summary table

For the hub's Discrepancies section, here's the consolidated list ranked by exam-relevance:

| # | Finding | Severity | Where surfaced |
|---|---|---|---|
| A | **AND/OR opcode swap between team hardware vs textbook/Java/lecture-10 slide** | High | [[EXAM_PREP_INVENTORY]] §4.2, [[EX — Instruction ADD]] §6, this report §1.4 |
| B | **3-bit LDI immediate limit + workarounds** (NOT+SUB, `.word`) | High | [[EX — Instruction LDI]] §5, [[EX — Microprocessor (top)]] §6 |
| C | **BRZ/BRN tests R[SA] = 0, not the previous instruction's flag** | High | [[EX — Instruction BRZ]] §5, this report §2.1 |
| D | **Branch offset is 6-bit signed (-32..+31)**, not 3-bit | Medium | [[EX — Instruction BRZ]] §2, this report §1.3 |
| E | **Lecture-10 says BRZ uses `zf`; hardware uses `se`** | Medium | this report §1.2 |
| F | **`add D2 A0 B1` hex error in Opg 10** | Medium | this report §1.1 |
| G | **Dual-clock domain CLK/CLK_CPU + BRAM negative-edge trick** | Medium | [[EX — Microprocessor (top)]] §2, §5.5 |
| H | **`Cin = FS0` clever wiring** | Low (trivia) | [[EX — Microprocessor (top)]] §5.3, [[EX — Instruction ADD]] §3 |
| I | **PortReg8x8 entity width (8 vs 16) — implementation deviation from lecture/spec** | Low | this report §2.3 |
| J | **Lecture 10 internal inconsistency on AND/OR (lines 228 vs 446-449)** | Low | this report §1.4 |
| K | **BTNS typo in Lecture 10 I/O table** | Trivia | this report §2.4 |
| L | **Two `-- 5 nuller` VHDL comments** (one accurate, one not) | Trivia | this report §1.5 |
| M | **IDC sensitivity list excludes V, C** (fine for current ISA) | Trivia | this report §6 below |

---

## Section 6 — Minor stylistic / robustness notes (no action needed)

Captured for completeness — these are observations from reading the VHDL that don't rise to "fact-check finding" but are exam-relevant trivia.

- **`InstructionDecoderController.vhd:37` sensitivity list `(current_state, IR, N, Z)` omits V and C.** Correct for the current ISA (no instruction tests V or C). Would need updating if a hypothetical BRV/BRC were added.
- **`InstructionDecoderController.vhd:213-225` SLM EX1 has a redundant `next_state <= EX2`** before the if-elsif that re-assigns it. Stylistic; net behavior matches SRM EX1.
- **`Ram256x16.vhd:51` ties `Reset` to `'0'`** in the Microprocessor instantiation. Per the Xilinx BRAM_SINGLE_MACRO semantics, this prevents output-latch reset but cannot clear BRAM contents anyway — the INIT generic IS the program. Documented in [[EX — Microprocessor (top)]] §5.5.
- **`PortReg8x8.vhd` `Data_In(7:0)`-only writes** — only the low byte of the 16-bit Data_In is consumed when writing MR0..MR2. The high byte is discarded. Consistent with the 8-bit Datapath but worth knowing.

---

## Section 7 — What this report does NOT cover

Per the prompt's scope ("Surface, don't silently fix"), this report is read-only on existing notes. The following are **deliberately out of scope** for Phase 2:

- Editing any of the existing notes to fix the findings.
- Editing the submitted Report-PWF Overleaf source. Per Mads's Q6 choice ("log only"), surface only.
- Adding new findings to NotebookLM. The 62711 notebook reflects ingested course material; not modified.
- Re-verifying PWA submodule notes in depth (low ROI).

---

> [!nav]
> &nbsp;
>
> ← [[EXAM_PREP_INVENTORY|Phase-0 Inventory]] · ← [[EX — Microprocessor (top)]] · → **Phase 3: hub** *(next)*
>
> Related: [[EX — Instruction LD]] · [[EX — Instruction SRM]] · [[EX — Instruction ADD]] · [[EX — Instruction JMP]] · [[EX — Instruction BRZ]] · [[EX — Instruction LDI]]
