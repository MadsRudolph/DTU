---
tags: [62711, exam-prep, extraction, instruction, ADD, arithmetic, alu]
course: 62711 Digital Systems Design
topic: ADD instruction — register-register arithmetic
source: PWF
phase: 1
---
# EX — ADD (Add, register-register)

> [!info] What this note is
> The canonical arithmetic-op walkthrough — exercises the ALU, the flag-generation logic, and the most common control-word pattern (`RW=1, MD=0, MM=0`, FS taken straight from `IR(12..9)`).

**Backlinks:** [[EX — Microprocessor (top)]] · [[EX — Instruction LD]] · [[InstructionDecoderController]] · [[PWA Project]]

---

## 1. Spec & semantics

> `R[DR] ← R[SA] + R[SB]`
> Standard two-source addition, all eight flag bits (V, C, N, Z) updated.

| Property | Value |
|---|---|
| Opcode (`IR(15:9)`) | `0000010` |
| Cycles | **2** (INF → EX0 → INF) |
| Affected flags | V, C, N, Z (V = C8 ⊕ C7; C = C8; N = bit-7 of result; Z = result==0) |
| Affected registers | R[DR] (write) |
| Memory access | none |

**Source citations:**
- 62711 PWF spec PDF page 1: `EX0 0000010 XXXX INF 0 01 0IR876 0IR543 0IR210 X 0010 X 1 0 0 ADD (*)`.
- Team VHDL: [`InstructionDecoderController.vhd:80-93`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — ADD is one of the unified ALU `when` branches:
  ```vhdl
  when "0000000" | "0000001" | "0000010" | "0000101" | "0000110"
     | "0001000" | "0001001" | "0001010" | "0001011" | "0001100" =>
      next_state <= INF;
      PS  <= "01";
      FS  <= IR(12 downto 9);    -- = "0010" for ADD
      RW  <= '1';
  ```
  The `FS = IR(12 downto 9)` trick: bits 12-9 of an ALU-op opcode are *already* the right FS code. ADD's opcode is `0000010` → bits 12-9 are `0010` → FS=0010 = "F = A + B" per the PWA encoding table.
- Lecture-10 doesn't separately enumerate ADD's control word — it's covered by the same "all ALU ops" row in the spec FSM table.

---

## 2. Encoding

```
 15        9 | 8 6 | 5 3 | 2 0
┌───────────┬─────┬─────┬─────┐
│  0000010  │ DR  │ SA  │ SB  │
│  opcode   │ 3 b │ 3 b │ 3 b │
└───────────┴─────┴─────┴─────┘
```

**Example word:** `ADD D2 A1 B0` (R2 ← R1 + R0)
- Opcode `0000010`, DR=`010`, SA=`001`, SB=`000`
- Binary: `0000010 010 001 000` = `0000 0100 1000 1000` = `0x0488`

---

## 3. Cycle-by-cycle walkthrough

Setup:
- R1 = `0x03`, R0 = `0x04`, R2 = `0x00`.
- IDC.current_state = INF, PC = `0x02` (the ADD's address).

### Cycle 0 — INF (fetch)

Identical to [[EX — Instruction LD#cycle-0-inf-instruction-fetch|LD cycle 0]]. PC drives MUX M(1), RAM returns the ADD word `0x0488`, IR loads it, state → EX0.

### Cycle 1 — EX0 (the add)

```
IR(15:9) = 0000010 → ADD branch (unified ALU when-clause)

Asserted by IDC:
   PS = 01                          ← PC will increment
   IL = 0
   DX = 0 & IR(8..6) = "0010"       ← R[DR] = R2
   AX = 0 & IR(5..3) = "0001"       ← R[SA] = R1
   BX = 0 & IR(2..0) = "0000"       ← R[SB] = R0
   FS = IR(12..9)  = "0010"         ← ADD (F = A + B)
   MB = 0                           ← MUX B picks B_Data (not ConstantIn)
   MD = 0                           ← MUX D picks F (the ALU output)
   RW = 1                           ← R[DR] writes next edge
   MM = 0, MW = 0
```

> [!note] Cin comes from FS0
> The Datapath's `Cin` port is wired to `FS_sig(0)` at the top level ([`Microprocessor.vhd:102`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd)). For ADD (FS=0010), `Cin=0` — exactly right. For SUB (FS=0101), `Cin=1` — also exactly right, because SUB is implemented as `A + B' + 1` (two's-complement subtraction). See [[EX — Microprocessor (top)#5.3]] for the trick.

**Diagram trace:**
1. Register File: AA=`0001` → `A_Data = R1 = 0x03`. BA=`0000` → `B_Data = R0 = 0x04`.
2. MUX B: MB=0 → picks `B_Data = 0x04`. Output `Bus_B = 0x04` → ALU's B input.
3. Function Unit / ALU: A=0x03, B=0x04, Cin=0, FS=0010 → 8-bit ripple-carry adder produces `F = 0x07`. Internal carry bits set C8=0, C7=0 → V = 0, C = 0. NegZero block sees F=0x07 → N=0 (bit-7 clear), Z=0 (nonzero).
4. MUX F: FS3=0 → MF=0 → picks ALU output. F_Out = 0x07.
5. MUX D: MD=0 → picks F_Out = 0x07 → D_Data = 0x07.
6. Register File: DA=`0010` selects R2. RW=1 will write on next edge.
7. Flags V, C, N, Z are driven out of the Datapath to the IDC (and would be available to a subsequent `BRZ`/`BRN`).

**Rising edge ends cycle 1:**
- R2 ← 0x07.
- PC ← PC + 1 = 0x03.
- IDC.state ← INF.
- Flags V=0, C=0, N=0, Z=0 are *not registered* — they're combinational outputs of the FU. They reflect "the most recent ALU op" continuously, so they remain at 0/0/0/0 only until the next ALU op changes them.

---

## 4. Path on `architecture.pdf`

The ribbon to trace with your finger during the oral exam:

```
R1 ─┬→ A_Data ─→ FU.A ─┐
    │                  ├→ ALU (FS=0010, Cin=0) ─→ F ─→ MUX F (0) ─→ F_Out ─→ MUX D (0) ─→ D_Data ─→ R2 (write)
R0 ─→ B_Data ─→ MUX B (0) ─→ Bus_B ─→ FU.B ───┘                                     │
                                                                                    │
                                NegZero (combinational on F) ─→ N, Z ──────────────┘ (to IDC)
                                ALU.C8, C7        ─→ V, C ────────────────────────── (to IDC)
```

All inside the Datapath block ("1" on the diagram) — no external memory traffic.

---

## 5. The flag generation — exam-trivia worth memorising

| Flag | Source | Set on |
|---|---|---|
| **V** (overflow) | `full_adder_8_bit.C7 XOR C8` | Arithmetic ops only (FS3=0). For ADD: V=1 iff signed overflow (both operands same sign, result opposite sign). |
| **C** (carry-out) | `full_adder_8_bit.C8` | Arithmetic ops only. For ADD: C=1 iff unsigned overflow (`0xFF + 0x01 → C=1`). |
| **N** (negative) | `NegZero` block — bit 7 of F | All ops, including logic/shift. |
| **Z** (zero) | `NegZero` block — NOR of all F bits | All ops. |

For ADD specifically: all four are meaningful. Compare to LD where V/C are set by an irrelevant ALU operation; or to BRZ where no flags are touched.

> [!tip] Quick sanity check: 0xFF + 0x01 with ADD
> A=0xFF, B=0x01 → F=0x00 (wrap), C8=1, C7=1, so C=1, V=0 (no signed overflow; -1 + 1 = 0 is correct in two's complement). N=0, Z=1. So the next `BRZ` *would* branch.

---

## 6. Other ALU ops share this exact cycle pattern

The unified `when` clause means ADD, SUB, INC, DEC, MOVA, OR, AND, XOR, NOT, MOVB all have **identical** control words in EX0 — only `FS = IR(12..9)` changes:

| Mnemonic | Opcode | FS=IR(12..9) | ALU op |
|---|---|---|---|
| MOVA | `0000000` | `0000` | F = A |
| INC | `0000001` | `0001` | F = A + 1 (Cin=FS0=1) |
| ADD | `0000010` | `0010` | F = A + B |
| SUB | `0000101` | `0101` | F = A − B (Cin=FS0=1) |
| DEC | `0000110` | `0110` | F = A − 1 |
| OR | `0001000` | `1000` | F = A ∨ B |
| AND | `0001001` | `1001` | F = A ∧ B |
| XOR | `0001010` | `1010` | F = A ⊕ B |
| NOT | `0001011` | `1011` | F = ¬A |
| MOVB | `0001100` | `1100` | F = B |

> [!warning] OR/AND mnemonic-vs-opcode mismatch with textbook
> Per the PWF spec page 1: OR=`0001000`, AND=`0001001` (and FS=1000 in PWA encoding maps to OR, FS=1001 to AND). The **Mano/Kime textbook pp.490, 493 and lecture-10 slide 9** have these swapped. The team's VHDL uses the spec ordering. **The Java assembler matches the textbook**, so writing `and` with the Java tool produces an opcode that the team's hardware will execute as OR. Use [[dsdasm]] instead. See [[EXAM_PREP_INVENTORY]] §4.2 for the full conflict matrix.

---

## 7. Gotchas

| Gotcha | Why it matters |
|---|---|
| **Cin = FS0** is a hard-wired trick — not separately controlled. | If you ever wonder why the IDC doesn't drive a "Cin" signal, this is why. The FS encoding *was designed* so that FS0 happens to be the right carry-in for each arithmetic op. |
| **Flag V is only meaningful for arithmetic ops.** | The PWA `NegZero` block always sets N and Z, but V and C come from the adder's internal carry bits. For logic ops, the carry bits exist (the adder is always running) but they're meaningless. |
| **The ALU output mux MUX F picks ALU when FS3=0.** | FS=0000-0111 → ALU output. FS=1000-1011 → ALU output (logic ops). FS=1100-1111 → Shifter output. The `FunctionSelect` block computes `MF = FS3 AND FS2`. |
| **All four flags are combinational, not registered.** | They reflect *this cycle's* ALU op, not "the last time we did an arithmetic op". If the next instruction is `BRZ`, BRZ sees the flags from the very ALU operation that the BRZ's own EX0 caused — and BRZ's EX0 default is `FS=0000` (transfer A). So `ADD ... ; BRZ ... ` works because the BRZ doesn't have time to overwrite the flag before sampling — but only because Z is combinational and the IDC samples it within EX0 *before* the next edge. Subtle. |

The last gotcha is a non-trivial timing point. The flags are combinational outputs of the FU. In EX0 of BRZ, the FU is also running (with default FS=0000 acting on garbage), so its V/C/N/Z is recomputed for that ALU op. **But the IDC's combinational process samples Z combinationally during the same cycle — so the Z it sees is the BRZ's own ALU output, NOT the prior ADD's.** This means BRZ alone doesn't work — you'd test the wrong Z.

> [!important] Wait — does BRZ actually work then?
> Looking at the spec FSM row again: in EX0, BRZ defaults FS=0000 → ALU does "pass A" where A=R[SA]. So Z reflects whether R[SA] is zero, not whether the prior instruction's result was zero.
>
> **In practice this means `BRZ Rs, off` tests "is R[SA] currently zero?", not "did the previous ALU operation produce zero?"** Many lecture problems implicitly assume the latter; the actual hardware does the former. This is a real exam gotcha and we should walk through it explicitly in the [[EX — Instruction BRZ]] note.

---

## 8. Source list

- [`team/PWB/sources/hdl/InstructionDecoderController.vhd:80-93`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — unified ALU when-clause.
- [`team/PWA/PWA.srcs/sources_1/new/Datapath.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd) — internal wiring.
- [`team/PWA/PWA.srcs/sources_1/new/ALU.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/ALU.vhd) — operation table.
- 62711 PWF spec PDF page 1.
- [[PWA Project]] §"FS Encoding Reference" — the FS↔operation table.
- [[InstructionDecoderController]] §"Kategori 1: 2-cyklus" — confirms unified ALU treatment.

---

> [!nav]
> &nbsp;
>
> ← [[EX — Instruction LD]] · ← [[EX — Instruction SRM]] · → [[EX — Instruction JMP]] *(next)*
>
> Related: [[Datapath]] · [[ALU]] · [[NegZero]] · [[FunctionSelect]]
