---
tags: [62711, exam-prep, extraction, instruction, JMP, control-flow]
course: 62711 Digital Systems Design
topic: JMP instruction — unconditional jump (PC ← R[SA])
source: PWF
phase: 1
---
# EX — JMP (Jump, register-indirect)

> [!info] What this note is
> The simplest control-flow instruction — exercises the **PC's load mode (PS=11)** and the path from Datapath's `Address_Out` (= A_Data) into the PC's `Address_In` port. Only 2 cycles; no register write, no memory access, no flag changes.

**Backlinks:** [[EX — Microprocessor (top)]] · [[EX — Instruction LD]] · [[InstructionDecoderController]] · [[ProgramCounter]]

---

## 1. Spec & semantics

> `PC ← R[SA]`
> *"Set the program counter to the value in R[SA] on the next clock edge. Execution resumes from that address."*

| Property | Value |
|---|---|
| Opcode (`IR(15:9)`) | `1110000` |
| Cycles | **2** (INF → EX0 → INF) |
| Affected flags | none (combinational FU output is discarded) |
| Affected registers | none — only PC is written |
| Memory access | none |

**Source citations:**
- 62711 PWF spec PDF page 1: `EX0 1110000 XXXX INF 0 11 0IR876 0IR543 X IR210 X 0000 X 0 0 0 JMP`.
- Team VHDL: [`InstructionDecoderController.vhd:175-177`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd):
  ```vhdl
  when "1110000" =>
      next_state <= INF;
      PS  <= "11";
  ```
  Everything else uses defaults: RW=0, MW=0, MD=0, MM=0, IL=0, MB=0, FS=0000.

---

## 2. Encoding

```
 15        9 | 8 6 | 5 3 | 2 0
┌───────────┬─────┬─────┬─────┐
│  1110000  │  -  │ SA  │  -  │
│  opcode   │unused│ 3 b │unused
└───────────┴─────┴─────┴─────┘
```

DR and B-slot are unused — the IDC drives them from IR-defaults but the register file's RW=0 means nothing happens.

**Example word:** `JMP A7` (PC ← R7)
- Opcode `1110000`, DR=`000`, SA=`111`, B=`000`
- Binary: `1110000 000 111 000` = `1110 0000 0011 1000` = `0xE038`

---

## 3. Cycle-by-cycle walkthrough

Setup:
- R7 = `0x05` (the jump target).
- IDC.current_state = INF, PC = `0x14` (the JMP's address).

### Cycle 0 — INF (fetch)

Same as every fetch — `PC=0x14 → MUX M(1) → RAM → MUX MR → Data_Bus_Out = 0xE038 → IR loads`. Next edge: state → EX0.

### Cycle 1 — EX0 (the jump)

```
IR(15:9) = 1110000 → JMP branch

Asserted by IDC:
   PS = 11                          ← PC will LOAD on next edge (not increment, not branch-relative)
   IL = 0
   DX = 0 & IR(8..6)                ← driven but ignored (RW=0)
   AX = 0 & IR(5..3) = "0111"       ← R[SA] = R7 → A_Data path becomes the jump target
   BX = 0 & IR(2..0)                ← driven, ignored
   FS = 0000                        ← ALU passes A through; result ignored
   MB = 0, MD = 0
   RW = 0                           ← NO register write
   MM = 0, MW = 0
```

**Diagram trace:**
1. Register File: AA=`0111` → `A_Data = R7 = 0x05`.
2. `A_Data` is wired straight out of the Datapath as `Address_Out_DP` ([`Datapath.vhd:115`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd)).
3. `Address_Out_DP = 0x05` enters **two** places:
   - MUX M's `(0)` input — irrelevant this cycle (MM=0, so MUX M *would* pick this, but no memory access happens because both RW and MW are 0).
   - The MPC's `Address_In` port ([`Microprocessor.vhd:120`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd)) → routed to the PC's `Address_In` pin.
4. Inside the PC: `PS=11` decodes to `Load=1, Count=0`, and the MUXP selector picks `Address_In` (not `sumOffset`). So when the next rising edge comes, the CounterLogic D-FFs each load their bit of `Address_In`.

**Rising edge ends cycle 1:**
- **PC ← 0x05** (the value that was in R7).
- IDC.state ← INF.
- Nothing else changes — no register file write, no memory.

Cycle 2 (the next INF) then fetches the instruction at address `0x05`. Done.

---

## 4. Path on `architecture.pdf`

```
R7 (register file) ─→ A_Data ─→ Address_Out (Datapath bottom-left pin)
                                          │
                                          ├─→ MUX M (0)  [unused this cycle]
                                          │
                                          └─→ PC.Address_In ───(PS=11, Load=1)──→ PC ← 0x05
```

Two diagram wires you need to be able to point at:
1. The wire from the register file's A read port (top of block "1") out through the Datapath's `Address_Out` pin to the MPC block.
2. The wire entering the PC's `Address_In` port at the top-left of block "2".

---

## 5. Comparison — JMP vs BRZ-taken

Both write the PC, but via different mechanisms:

| Aspect | JMP | BRZ (Z=1) |
|---|---|---|
| PS code | `11` | `10` |
| PC source | `Address_In = R[SA]` (absolute) | `PCsig + Offset` (PC-relative, signed) |
| Condition | unconditional | only if Z=1 (sampled combinationally in EX0) |
| Range | full 8-bit absolute address (0..255) | PC ± 32 (6-bit signed offset; see [[EX — Instruction BRZ]]) |
| Uses ALU? | no (output discarded) | no (output discarded; Z came from the ALU running on R[SA] though) |

The `MUXP` mux inside the PC ([`ProgramCounter.vhd:145-146`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ProgramCounter.vhd)) implements this directly:
```vhdl
MUXP <= ((7 downto 0 => PS(1)) AND ((NOT (7 downto 0 => PS(0))) AND sumOffset))   -- PS=10
     OR ((7 downto 0 => PS(1)) AND      ((7 downto 0 => PS(0)) AND Address_In));  -- PS=11
```
With `Load = PS(1)` either way, so both PS=10 and PS=11 trigger a load — they just feed different sources into the MUXP.

---

## 6. The halt idiom

Because JMP is absolute and `R[SA]` can equal the current PC, you can build a halt:

```asm
    ldi D7 B7         ; R7 = 7  (must fit in 0..7)
halt:                 ; assume the label resolves to address 7
    jmp A7            ; PC ← R7 = 7 = address of this jmp → re-execute forever
```

This is the [[dsdasm]] "halt convention" — `jmp R_x` where `R_x == address_of_jmp` becomes an infinite single-instruction loop. The simulator detects this and stops.

> [!warning] LDI's 3-bit immediate constrains the halt address
> Since `LDI` can only load 0..7, the halt instruction must live at one of those low addresses. Common pattern: put `halt: jmp A7` at the very start of the program and use it as a sentinel everything else falls through to. Or use the `.word` workaround (see [[dsdasm]]).

---

## 7. Gotchas

| Gotcha | Why it matters |
|---|---|
| **JMP's destination comes from `A_Data` (read-port A = R[SA]), not from the instruction encoding.** | You can't write `JMP 0x42` — there is no immediate jump. You first `LDI Rx, addr` then `JMP Ax`. (And `LDI` is 3-bit imm, so absolute addresses > 7 need the `.word` workaround.) |
| **PS=11 is exclusive to JMP; PS=10 is exclusive to BRZ/BRN.** | The PC's load logic uses these to switch source between `Address_In` and `sumOffset`. Mixing them up gives the wrong jump semantics. |
| **The ALU runs in EX0 of JMP (and its flags update!).** | FS=0000 default → pass-A. So V/C/N/Z reflect "is R[SA] zero / negative?". After a JMP, the next instruction's BRZ/BRN sees these flags. Probably not what you wanted — explicitly clear them with an `INC R0 A0` if you need a fresh flag state after a JMP. |
| **PC is loaded directly — no +1 happens.** | Unlike PS=01 (increment), there's no implicit +1 added. The destination address goes straight into PC. |

---

## 8. Source list

- [`team/PWB/sources/hdl/InstructionDecoderController.vhd:175-177`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — JMP case.
- [`team/PWB/sources/hdl/ProgramCounter.vhd:137-146`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ProgramCounter.vhd) — PS decoding & MUXP.
- [`team/PWF/sources/hdl/Microprocessor.vhd:120`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd) — wiring of `Address_Out_DP` to MPC's `Address_In`.
- 62711 PWF spec PDF page 1.
- [[ProgramCounter]] · [[InstructionDecoderController]] §"Kategori 1".
- [[dsdasm]] §"Halt convention".

---

> [!nav]
> &nbsp;
>
> ← [[EX — Instruction ADD]] · → [[EX — Instruction BRZ]] *(next)*
>
> Related: [[ProgramCounter]] · [[InstructionDecoderController]]
