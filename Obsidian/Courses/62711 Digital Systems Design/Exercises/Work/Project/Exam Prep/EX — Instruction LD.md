---
tags: [62711, exam-prep, extraction, instruction, LD, memory]
course: 62711 Digital Systems Design
topic: LD instruction — register-indirect memory read
source: PWF
phase: 1
---
# EX — LD (Load, register-indirect)

> [!info] What this note is
> The **template** Phase-1 instruction walkthrough. LD is the simplest non-trivial memory operation — 2 cycles, hits MUX M, RAM, MUX MR, and MUX D in a single round trip. Every later instruction walkthrough follows this note's structure.

**Backlinks:** [[EX — Microprocessor (top)]] · [[InstructionDecoderController]] · [[PWF Project]]

---

## 1. Spec & semantics

> `R[DR] ← M[R[SA]]`
> *"Load the word at the address held in R[SA] into R[DR]."*

| Property | Value |
|---|---|
| Opcode (`IR(15:9)`) | `0010000` |
| Cycles | **2** (INF → EX0 → INF) |
| Affected flags | none |
| Affected registers | R[DR] (write) |
| Memory access | one read |

**Source citations:**
- 62711 PWF spec PDF page 1 (top FSM table + bottom mnemonic-explained table). The spec lists LD's EX0 control word as: `PS=01, IL=0, DX=0IR876, AX=0IR543, BX=XIR210, MB=X, FS=XXXX, MD=1, RW=1, MM=0, MW=0`.
- Lecture-10 slide 10 ("LRI and LDI, LD, ST instruction") — agrees with the spec for LD: `EX0 0010000 XXXX INF 0 01 0IR876 0IR543 X IR210 X XXXX 1 1 0 0 LD (*)`.
- Team VHDL: [`InstructionDecoderController.vhd:120-124`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — `when "0010000" => next_state <= INF; PS <= "01"; MD <= '1'; RW <= '1';` (with MM, MW, MB, FS all defaulting from the top-of-process defaults: MM=0, MW=0, MB=0, FS=0000).
- All three sources agree byte-for-byte.

---

## 2. Encoding

```
 15        9 | 8 6 | 5 3 | 2 0
┌───────────┬─────┬─────┬─────┐
│  0010000  │ DR  │ SA  │  -  │
│  opcode   │ 3 b │ 3 b │ unused
└───────────┴─────┴─────┴─────┘
```

The B-slot (`IR(2:0)`) is unused for LD — the IDC still routes it as `BX = '0' & IR(2:0)` per defaults, but no read port consumes it.

**Example concrete instruction word:** `LD D2 A1` (load M[R1] into R2)
- Opcode `0010000`, DR=`010`, SA=`001`, B=`000`
- Binary: `0010000 010 001 000` = `0010 0000 1000 1000` = `0x2088`
- Verify via [[dsdasm]]: `python dsdasm.py asm <(echo "ld D2 A1")` would emit `0x2088` (line `00: 0x2088 ld D2, A1`).

---

## 3. Cycle-by-cycle walkthrough

Setup (preconditions, established by earlier instructions or reset):
- R1 = `0x05` (the address to read from)
- M[5] = `0x0042` (the word stored there — could be set by an earlier `ST` or by a `.word 0x42` in the program)
- Current state: INF (just finished a previous instruction)
- PC = some value, say `0x07` (this LD is at address 7 in the program; whatever loaded into IR last triggered INF→EX0→INF and PC is now sitting at the LD's address).

> [!note] Reading the per-cycle blocks below
> Each cycle shows **(a) the IDC control word**, **(b) what the diagram shows happening this cycle**, **(c) the next-edge effect** (what the next rising edge of CLK_CPU latches).

### Cycle 0 — INF (instruction fetch)

```
IDC.current_state = INF
─────────────────────────────────────────────────────────
Asserted by IDC (combinational):
   IL = 1                  ← IR will load this cycle
   MM = 1                  ← MUX M picks PC
   PS = 00                 ← PC holds (won't advance until EX0)
   DX, AX, BX             ← decoded from current IR (still the previous instruction's — doesn't matter, IR-write hasn't happened yet)
   FS = 0000, MB = 0, MD = 0, RW = 0, MW = 0   (no writes; just reading mem)
```

**Diagram trace** (refer to `architecture.pdf`):
1. `PROGRAM COUNTER` outputs `PC = 0x07` on its `PC` pin (the wire labelled `Address_Out` between the PC block and MUX M).
2. **MUX M** has selector `MM=1`, so it routes its `(1)` input (PC) to its output `Mem_Address = 0x07`. The Datapath's `Address_Out_DP` (input `(0)`) is ignored.
3. `Mem_Address = 0x07` hits both `RAM.Address` and `Port Register.Address` simultaneously.
4. `MMR` is combinational from PortReg's address decoder: `0x07 < 0xF8`, so **MMR = 0**.
5. RAM, clocked on the **negative** `CLK` edge (the trick from [[EX — Microprocessor (top)#5.5]]), reads word at address `0x07`. Its `Data_outM` becomes `0x2088` (our LD encoding) by the time the next `CLK_CPU` rising edge arrives.
6. PortReg's `Data_outR` is whatever (don't care — MMR=0).
7. **MUX MR** with selector `MMR=0` picks RAM → `Data_Bus_Out = 0x2088`.
8. `Data_Bus_Out` fans out to two consumers:
   - Datapath's `DataIn` port sees `0x88` (low byte). Ignored because `MD=0, RW=0`.
   - **IR's `Instruction_In` port sees the full `0x2088`. Because `IL=1`, the next CLK_CPU edge will latch it.**

**Rising edge of `CLK_CPU` ends cycle 0:**
- IR ← `0x2088` (because `IL=1`).
- IDC.current_state ← `EX0` (because INF's next_state is EX0).
- PC unchanged (PS=00).

### Cycle 1 — EX0 (LD execute)

```
IDC.current_state = EX0
IR(15:9) = 0010000  →  LD branch in the case statement
─────────────────────────────────────────────────────────
Asserted by IDC (combinational):
   PS = 01                ← PC will increment next edge
   IL = 0                 ← do NOT reload IR
   DX = 0 & IR(8..6) = 0 & "010" = "0010"   ← R[DR] = R2
   AX = 0 & IR(5..3) = 0 & "001" = "0001"   ← R[SA] = R1
   BX = 0 & IR(2..0) = 0 & "000" = "0000"   ← unused but driven
   FS = 0000              ← don't-care (FS only matters when MD=0)
   MB = 0                 ← don't-care
   MD = 1                 ← MUX D picks DataIn (memory read result), not ALU output
   RW = 1                 ← R[DR] will load next edge
   MM = 0                 ← MUX M picks Datapath, NOT PC
   MW = 0                 ← no memory write
```

**Diagram trace:**
1. Register File reads port A: `DA = 0010` selects R2 — but read port A isn't used for the actual address; **read port A's selector is `AA = AX = 0001`** → `A_Data = R1 = 0x05`. (DA is the write-port selector; AA is the read-port A selector. Easy to confuse; see [[RegisterFile]].)
2. `A_Data = 0x05` flows along the wire labelled `A_Data` to two places: (a) to the ALU's A input (irrelevant this cycle), (b) **directly out of the Datapath as `Address_Out`** ([`Datapath.vhd:115`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd)).
3. `Address_Out = 0x05` enters MUX M at its `(0)` input.
4. **MUX M** with `MM=0` selects `(0)` → `Mem_Address = 0x05`. (Note: the PC also outputs its current value to MUX M's `(1)` input, but it's not selected.)
5. `Mem_Address = 0x05` reaches RAM and PortReg.
6. **MMR = 0** (0x05 < 0xF8) → MUX MR picks RAM.
7. RAM reads address `0x05`, returns `Data_outM = 0x0042` (16-bit, top byte zero because this was written by a prior ST with Zero_Filler_2, or it was put there as `.word 0x42`).
8. **MUX MR** routes `Data_outM` through → `Data_Bus_Out = 0x0042`.
9. `Data_Bus_Out` fans out:
   - IR's `Instruction_In = 0x0042`. **Ignored** because `IL=0`.
   - **Datapath's `DataIn = Data_Bus_Out(7..0) = 0x42`.**
10. Inside the Datapath, `DataIn` enters **MUX D's `(1)` input**. With `MD=1`, MUX D selects `(1)` → `D_Data = 0x42`.
11. `D_Data` is the write-back port to the register file. With `RW=1` and `DA = 0010` (= R2), R2 will be written.
12. Meanwhile the ALU is running: `A=R1=0x05, B=0 (MB=0, B_Data=R0=0)`, FS=0000 (transfer A) → `F=0x05`. Irrelevant — `MD=1` so MUX D ignores it.

**Rising edge of `CLK_CPU` ends cycle 1:**
- **R2 ← 0x42** (because `RW=1, MD=1`, `D_Data=0x42`).
- PC ← PC + 1 = `0x08` (because `PS=01`).
- IDC.current_state ← `INF`.
- IR unchanged (because `IL=0`).

Total: **2 CLK_CPU cycles**, one memory read, one register write.

---

## 4. Path on `architecture.pdf` (the visual story)

For the exam, you should be able to trace the LD's *operand* cycle (cycle 1) onto the diagram with your finger:

```
R1 (register file array) ─── A_Data ─── out of Datapath as Address_Out ─── MUX M (0) ─── Mem_Address
                                                                                              │
                                                                                              ▼
                                                                                          RAM (read addr 0x05)
                                                                                              │
                                                                                              ▼  Data_outM = 0x0042
                                                                                          MUX MR (0)
                                                                                              │
                                                                                              ▼  Data_Bus_Out = 0x0042
                                                              ┌──────────────── back into the Datapath ───────────────┐
                                                              ▼                                                       ▼
                                                     IR.Instruction_In                                  Datapath.DataIn = 0x42
                                                     (ignored, IL=0)                                                   │
                                                                                                                       ▼
                                                                                                              MUX D (1) ─── D_Data ─── R2 (write next edge)
```

If someone draws the LD operand path during the oral exam, those are the **eight diagram blocks/wires you must hit in order**: register file → `A_Data` → `Address_Out` → MUX M → `Mem_Address` → RAM → MUX MR → `Data_Bus_Out` → Datapath `DataIn` → MUX D → `D_Data` → register file write.

---

## 5. A common variation — LD from a port register

If `R[SA] = 0xFB` (= MR3's address, the BTNR-latched switch value):
- Cycle 0 unchanged.
- Cycle 1 step 6: `MMR = 1` (because address is in `0xF8..0xFF`).
- Cycle 1 step 7-8: MUX MR picks PortReg's `Data_outR` instead. The port-register VHDL has presented MR3's 8-bit value (zero-padded to 16 bits internally).
- Cycle 1 step 12: same write-back, R[DR] gets the SW value that was latched on the last BTNR press.

So **LD is the same instruction whether you're reading RAM or memory-mapped I/O** — the only difference is who answers, and that's decided combinationally by MMR.

This is exactly how the [[microcode-program]] test program reads `BTNR→MR3` and writes it to LEDs via `ST`:
```asm
not D2 A4          ; R2 = 0xFF
ldi D4 B4          ; R4 = 4
sub D3 A2 B4       ; R3 = 0xFF - 4 = 0xFB (= MR3 address)
ld  D6 A3          ; R6 = M[0xFB] = MR3 (the latched SW value)  ← THIS is an LD-from-port-register
```

---

## 6. Gotchas worth memorising

| Gotcha | Why it matters |
|---|---|
| **The address comes from R[SA] (read-port A), not R[DR].** | DR is the *destination*. If you swap operands, you'll read from the wrong place. The IDC routes `AX = '0' & IR(5..3)` (the SA slot) to the Datapath's `AA` (port-A address). |
| **`Address_Out = A_Data`, *not* ALU output.** | The Datapath has a direct wire from the register file's A read port to its `Address_Out` pin ([`Datapath.vhd:115`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd)). LD doesn't go through the ALU for address generation. |
| **MD=1 selects DataIn at MUX D — the high byte of memory is discarded.** | RAM is 16-bit wide but the register file is 8-bit. `DataIn => Data_Bus_Out(7 downto 0)` in [`Microprocessor.vhd:103`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd). |
| **PS=01 happens at EX0 → INF, *not* in INF itself.** | INF holds the PC (PS=00); the *increment* is decided in EX0. So the PC advances at the end of cycle 1, not cycle 0. |
| **No flags are set by LD.** | The ALU is still doing something (passing A through, FS=0000), but the flags V/C/N/Z are sampled from this irrelevant ALU op. **For the next instruction, V/C/N/Z reflect a meaningless transfer of R[SA].** If the next instruction is `BRZ` after `LD`, the branch isn't testing what was loaded — it's testing whether R[SA] (the address you just used) was zero. Easy footgun. |

---

## 7. Source list

- [`team/PWB/sources/hdl/InstructionDecoderController.vhd:120-124`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWB/sources/hdl/InstructionDecoderController.vhd) — the LD case in the FSM.
- [`team/PWF/sources/hdl/Microprocessor.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWF/sources/hdl/Microprocessor.vhd) — top-level wiring.
- [`team/PWA/PWA.srcs/sources_1/new/Datapath.vhd`](../../../../../../../4.%20Semester/Digital%20Systems%20Design/team/PWA/PWA.srcs/sources_1/new/Datapath.vhd) — `Address_Out = A_Data`, MUX D location.
- 62711 PWF spec PDF, page 1, both tables.
- Lecture-10 slide 10 ("LRI and LDI, LD, ST instruction") — control-word values verified.
- NotebookLM 62711 — cross-check (notebook-id `eb1f49b9-...`).

---

> [!nav]
> &nbsp;
>
> ← [[EX — Microprocessor (top)]] · → [[EX — Instruction SRM]] · → [[EX — Instruction ADD]] *(next)*
>
> Related: [[InstructionDecoderController]] · [[Datapath]] · [[RegisterFile]]
