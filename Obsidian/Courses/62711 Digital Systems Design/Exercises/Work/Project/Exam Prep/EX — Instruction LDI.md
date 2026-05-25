---
tags: [62711, exam-prep, extraction, instruction, LDI, immediate]
course: 62711 Digital Systems Design
topic: LDI instruction — load immediate (R[DR] ← zf(IR(2:0)))
source: PWF
phase: 1
---
# EX — LDI (Load Immediate)

> [!info] What this note is
> The immediate-load walkthrough. LDI exercises the **ZeroFiller → MUX B (MB=1) → ALU pass-B (FS=1100) → MUX D (MD=0) → R[DR]** path. Only the Datapath and MPC are touched — no memory access. Hard-constrained to 3-bit immediates (0..7).

**Backlinks:** [[EX — Microprocessor (top)]] · [[EX — Instruction ADD]] · [[InstructionDecoderController]] · [[ZeroFiller]]

---

## 1. Spec & semantics

> `R[DR] ← zf(OP)`
> *"Load the zero-extended 3-bit immediate (from IR(2:0)) into R[DR]."*

| Property | Value |
|---|---|
| Opcode (`IR(15:9)`) | `1001100` |
| Cycles | **2** (INF → EX0 → INF) |
| Affected flags | V=0, C=0, N=0; **Z=1 iff imm=0** (the ALU is doing pass-B with B=imm, so the NegZero block sees `imm` as the result) |
| Affected registers | R[DR] (write) |
| Memory access | none |
| Immediate range | **0..7** (3 bits, zero-filled — no negative values possible) |

**Source citations:**
- 62711 PWF spec PDF page 1: `EX0 1001100 XXXX INF 0 01 0IR876 X IR543 X IR210 1 1100 0 1 0 0 LDI`.
- Team VHDL: [`InstructionDecoderController.vhd:148-154`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd):
  ```vhdl
  when "1001100" =>
      next_state <= INF;
      PS  <= "01";
      FS  <= "1100";        -- pass-B through the Shifter (FS3=1, FS2=1, FS1=0, FS0=0)
      MB  <= '1';           -- MUX B picks ConstantIn (= ZeroFiller output), not B_Data
      RW  <= '1';
  ```
- [`team/PWB/sources/hdl/ZeroFiller.vhd:14-15`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ZeroFiller.vhd):
  ```vhdl
  ZeroFilled_8 <= (7 downto 3 => '0') & IR(2 downto 0);
  ```
- Lecture-10 slide 10: `EX0 ... LDI` row, MD=0, MB=1, FS=1100 — agrees with VHDL.

---

## 2. Encoding

```
 15        9 | 8 6 | 5 3 | 2 0
┌───────────┬─────┬─────┬─────┐
│  1001100  │ DR  │  -  │ imm │
│  opcode   │ 3 b │unused│ 3 b │
└───────────┴─────┴─────┴─────┘
```

The SA slot is unused — driven by IDC defaults from `IR(5..3)` but not connected to anything that matters (the register file's port A reads it, but the ALU doesn't consume A_Data when MB=1 and FS=1100).

**Example word:** `LDI D2 B5` (R2 ← 5)
- Opcode `1001100`, DR=`010`, SA=`000`, imm=`101`
- Binary: `1001100 010 000 101` = `1001 1000 1000 0101` = `0x9885`

---

## 3. Cycle-by-cycle walkthrough

Setup:
- R2 = `0x00` (we'll overwrite).
- IDC.current_state = INF, PC = `0x04` (the LDI's address).

### Cycle 0 — INF (fetch)

Same as always — `PC=0x04 → MUX M(1) → RAM → 0x9885 → MUX MR → Data_Bus_Out → IR loads`. Next state → EX0.

### Cycle 1 — EX0 (the immediate load)

```
IR(15:9) = 1001100 → LDI branch

Asserted by IDC:
   PS = 01                          ← PC will increment
   IL = 0
   DX = 0 & IR(8..6) = "0010"       ← R[DR] = R2
   AX = 0 & IR(5..3) = "0000"       ← driven (R0 read), ignored
   BX = 0 & IR(2..0) = "0101"       ← driven (R5 read), ignored (MB=1)
   FS = "1100"                      ← Shifter pass-B mode
   MB = 1                           ← MUX B picks ConstantIn = ZeroFiller output
   MD = 0                           ← MUX D picks F = ALU/Shifter result
   RW = 1                           ← R[DR] writes next edge
   MM = 0, MW = 0
```

**Diagram trace:**
1. ZeroFiller (combinational): IR(2..0) = `101` → `ZeroFilled_8 = 0000_0101 = 0x05`. Output → `Constant_Out` (8 bits) → wire labelled `cconstant_In` on the diagram → MUX B's `(1)` input.
2. MUX B: MB=1 → picks `(1)` = `ConstantIn = 0x05`. Output `Bus_B = 0x05` → Function Unit's B input.
3. Function Unit:
   - ALU still runs: A=A_Data (= R0 = irrelevant), B=0x05, FS=1100. The ALU itself with FS=1100 produces something, but we don't care.
   - Shifter runs: B input = 0x05, FS=1100 → "pass-through" (no shift). Output = 0x05.
   - FunctionSelect: `MF = FS3 AND FS2 = 1 AND 1 = 1` → MUX F picks Shifter output.
   - F_Out = 0x05.
4. NegZero: F=0x05 → N=0 (bit-7 clear), Z=0 (nonzero).
5. MUX D: MD=0 → picks F_Out = 0x05 → D_Data = 0x05.
6. Register file: DA=`0010` selects R2. RW=1.

**Rising edge ends cycle 1:**
- **R2 ← 0x05.**
- PC ← PC + 1 = `0x05`.
- State ← INF.
- Flags: V=0, C=0 (don't-care from the unused ALU), N=0, Z=0.

---

## 4. Why FS=1100 (Shifter pass-through), not FS=1000 (OR with B)?

Both *would* produce F=B (since A=0 would make OR a pass-through too — but A isn't reliably 0; it's R[SA]). FS=1100 routes through the Shifter, whose "pass-through" mode is unconditional on A.

So the team's choice of FS=1100 for LDI is **defensive against the SA field being non-zero**. It works regardless of what R[SA] happens to hold.

Alternative consideration: FS=0000 (ALU pass-A) wouldn't work because that would put R[SA] into R[DR] instead of the immediate. You need pass-B, and the only "pass-B" mode that's robust against A is the Shifter's pass-through (FS=1100).

---

## 5. The 3-bit immediate limit — and its consequence

LDI can load **0..7 only**. To put any other value in a register, you need a multi-instruction sequence.

### Common workaround: subtract from 0xFF

The team's [[microcode-program]] addsub_calc example uses this idiom:

```asm
not  D2 A4         ; R4 = 0 (after reset) → R2 = NOT 0 = 0xFF
ldi  D4 B5         ; R4 = 5
sub  D3 A2 B4      ; R3 = 0xFF - 5 = 0xFA  ← now R3 can address MR2 (LED at 0xFA)
```

Three instructions to get 0xFA into a register. Variations: for 0xF8..0xFF, subtract 7..0 from 0xFF. The 0xFF "anchor" is established once via `NOT R2 R4` (assuming R4 was reset to 0).

### Alternative: `.word` directive

[[dsdasm]] supports a `.word` directive that emits a literal 16-bit value into the program. You can store the address you want there, then LDI a small index that locates that `.word`, then LD through it:

```asm
leds_addr:
    .word 0xFA          ; at program address e.g. 0x00, this 16-bit cell holds 0x00FA
start:
    ldi  D0 B0           ; R0 = 0 (= address of leds_addr)
    ld   D1 A0           ; R1 = M[0] = 0x00FA
    ; R1 now holds 0xFA — use it as an address with ST/LD
```

Slower at runtime (one extra LD) but cleaner; [[dsdasm]]'s recommended approach for high addresses.

---

## 6. Path on `architecture.pdf`

```
IR(2..0) ─→ Zero Filler (under IR block) ─→ Constant_Out (= cconstant_In on diagram)
                                                  │
                                                  ▼
                                          MUX B (1)
                                                  │
                                                  ▼
                                          FU.B → Shifter (pass-through) → MUX F (1) → F_Out
                                                                                       │
                                                                                       ▼
                                                                              MUX D (0) → D_Data → R[DR] (write)
```

Pure intra-Datapath path. The Address bus, memory, and MUX MR are not involved.

---

## 7. ADI is LDI's sibling

`ADI` (Add Immediate, opcode `1000010`) is structurally similar but uses the ALU's add instead of the Shifter's pass-through:

```vhdl
when "1000010" =>
    next_state <= INF;
    PS  <= "01";
    FS  <= "0010";        -- ADD (A + B)
    MB  <= '1';           -- MUX B picks ConstantIn
    RW  <= '1';
```

Effect: `R[DR] ← R[SA] + zf(imm)`. So you can do `ADI D2 A1 B3` → `R2 = R1 + 3`. Useful when you want to bump a register by a small constant without burning a register slot on the constant.

| Aspect | LDI | ADI |
|---|---|---|
| `R[SA]` value used? | no (MB=1 ignores A; FS=1100 pass-B ignores A too) | **yes** — added to imm |
| FS | 1100 (Shifter pass-B) | 0010 (ALU add) |
| Flags | reflect imm | reflect R[SA]+imm |

---

## 8. Gotchas

| Gotcha | Why it matters |
|---|---|
| **Immediate range is 0..7 only.** | No signed immediates; no negative LDI. You must construct other values via NOT+SUB sequences or `.word` indirection. |
| **The SA field in the encoding is ignored.** | But the IDC still drives `AX = '0' & IR(5..3)` — so the register file's read port A *is* used (just discarded). If you debug-trace `A_Data` during LDI, you'll see R[SA]'s value floating around even though it doesn't affect the result. |
| **Z flag reflects the immediate, not the destination's old value.** | `LDI D2 B0` (load 0) → Z=1; `LDI D2 B7` (load 7) → Z=0. After an LDI of 0, a subsequent BRZ-on-the-just-loaded-register would also see Z=1 (because BRZ's EX0 pass-A on R[DR] also produces zero). |
| **FS=1100 is the Shifter's pass-through, not the ALU's MOVB.** | Note that "MOVB" the *instruction* (opcode `0001100`, FS=`1100`) lives in the ALU-region's `when` clause but the FS encoding routes it through the Shifter's pass-through. Same FS=1100 is also used by LDI internally. Two instructions sharing the same FS-driven datapath. |
| **PC advances even though no real arithmetic happened.** | PS=01 — same as any 2-cycle instruction. Counter ticks the PC by 1. |

---

## 9. Source list

- [`team/PWB/sources/hdl/InstructionDecoderController.vhd:148-154`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — LDI case.
- [`team/PWB/sources/hdl/ZeroFiller.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/ZeroFiller.vhd) — 3→8 zero-fill.
- [`team/PWA/PWA.srcs/sources_1/new/Shifter.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Shifter.vhd) — pass-through mode.
- 62711 PWF spec PDF page 1 (LDI row + mnemonic table).
- Lecture-10 slide 10 — control word verified.
- [[microcode-program]] — the addsub_calc example uses LDI extensively.
- [[dsdasm]] §"Immediates" + §"The `.word` directive" — workarounds for >7 values.

---

> [!nav]
> &nbsp;
>
> ← [[EX — Instruction BRZ]] · → [[EX — Microcode program]] *(next, walkthrough of the team's actual demo programs)*
>
> Related: [[ZeroFiller]] · [[Shifter]] · [[FunctionSelect]]
