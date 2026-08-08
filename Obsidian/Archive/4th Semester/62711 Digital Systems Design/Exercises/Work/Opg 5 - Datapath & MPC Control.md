---
course: "62711"
course-name: "Digital Systems Design"
type: exercise
tags: [DSD, exercise]
---
# Opg 5 - Datapath & MPC Control

> [!abstract] Exercise Overview
> Datapath control word encoding (16-bit), micro-operation decoding, Program Counter timing, and Instruction Register submodule outputs.
> Reference: Lecture 5 (slide 12) · [[62711_ProjectWork_B_F2026.pdf|PWB Project Assignment]]

> [!info] Files
> - Exercise: [[opg5.pdf|Opg 5]]

---

> [!info] 16-bit Control Word Format (Lecture 5, slide 12)
> ![[Datapath_Block_Diagram.png]]
>
> | DA (3) | AA (3) | BA (3) | MB (1) | FS (4) | MD (1) | RW (1) |
> |--------|--------|--------|--------|--------|--------|--------|
>
> ![[encoding.png]]

---

## 5.1 Micro-operation Control Word Tables

> [!question] Complete the table symbolically and in binary for each RTL micro-operation.

### Symbolic Table

| Micro-operation | DA | AA | BA | MB | FS | MD | RW |
|---|---|---|---|---|---|---|---|
| R1 ← R2 − R3 | R1 | R2 | R3 | Register | F = A + B̄ + 1 | Function | Write |
| R4 ← sl R6 | R4 | — | R6 | Register | F = sl B | Function | Write |
| R7 ← R7 + 1 | R7 | R7 | — | — | F = A + 1 | Function | Write |
| R1 ← R0 + 2 | R1 | R0 | — | Constant | F = A + B | Function | Write |
| Data out ← R3 | — | — | R3 | Register | — | — | No Write |
| R4 ← Data in | R4 | — | — | — | — | Data in | Write |
| R5 ← 0 | R5 | R[X] | R[X] | Register | F = A + B̄ + 1 | Function | Write |

### Binary Table

| Micro-operation | DA | AA | BA | MB | FS | MD | RW |
|---|---|---|---|---|---|---|---|
| R1 ← R2 − R3 | 001 | 010 | 011 | 0 | 0101 | 0 | 1 |
| R4 ← sl R6 | 100 | XXX | 110 | 0 | 1110 | 0 | 1 |
| R7 ← R7 + 1 | 111 | 111 | XXX | X | 0001 | 0 | 1 |
| R1 ← R0 + 2 | 001 | 000 | XXX | 1 | 0010 | 0 | 1 |
| Data out ← R3 | XXX | XXX | 011 | 0 | XXXX | X | 0 |
| R4 ← Data in | 100 | XXX | XXX | X | XXXX | 1 | 1 |
| R5 ← 0 | 101 | XYZ | XYZ | 0 | 0101 | 0 | 1 |

> [!note]- Explanations
> **R4 ← sl R6:** Shift left operates on B input. R6 goes to port B (BA=110). AA is don't-care since only B is used by the shifter.
>
> **R7 ← R7 + 1:** Increment uses only the A input (FS=0001). BA and MB are don't-care.
>
> **R1 ← R0 + 2:** The constant 2 comes through Constant\_In (MB=1). BA is don't-care when MB selects constant.
>
> **Data out ← R3:** Data out is driven by the MUX B output (register B port). No register write needed (RW=0). All other fields are don't-care.
>
> **R4 ← Data in:** MD=1 routes Data\_In to the register instead of the function unit output. FS/MB/AA/BA are all don't-care.
>
> **R5 ← 0:** Any register subtracted from itself gives 0: R[X] − R[X] = 0. AA and BA must be the **same** register (denoted XYZ). Alternative: use F = A ⊕ B (FS=1010) with AA=BA=same.

---

## 5.2 Specify 16-bit Control Words

> [!question] Give the 16-bit control word for each micro-operation.
> Format: `DA(3) AA(3) BA(3) MB(1) FS(4) MD(1) RW(1)`

| | Micro-operation | Control Word |
|---|---|---|
| a) | R5 ← 0 | `101 XYZ XYZ 0 0101 0 1` |
| b) | R4 ← sl R5 | `100 XXX 101 0 1110 0 1` |
| c) | R7 ← Data\_In | `111 XXX XXX X XXXX 1 1` |
| d) | R3 ← sr R3 | `011 XXX 011 0 1101 0 1` |
| e) | R1 ← R3 − Constant\_In | `001 011 XXX 1 0101 0 1` |
| f) | R1 ← R1 + 1 | `001 001 XXX X 0001 0 1` |
| g) | R2 ← R1 xor R3 | `010 001 011 0 1010 0 1` |
| h) | R4 ← R3 + R5 | `100 011 101 0 0010 0 1` |

> [!note]- Explanations
> **a)** R5 ← R[X] − R[X] = 0. AA=BA=same register (XYZ). FS=0101 (subtract).
>
> **b)** Shift left of R5: BA=101 selects R5 onto B port. FS=1110 (sl B). AA don't-care.
>
> **c)** MD=1 selects Data\_In. Everything else is don't-care. RW=1 to write R7.
>
> **d)** Shift right of R3: BA=011 selects R3 onto B port. FS=1101 (sr B). Result stored in DA=R3.
>
> **e)** FS=0101 (A + B̄ + 1 = subtract). AA=R3 on A port. MB=1 selects Constant\_In on B port.
>
> **f)** FS=0001 (A + 1). AA=R1 on A port. BA/MB don't-care (B not used by increment).
>
> **g)** FS=1010 (XOR). AA=R1, BA=R3, MB=0.
>
> **h)** FS=0010 (A + B). AA=R3, BA=R5, MB=0.

---

## 5.3 Decode Control Words to Micro-operations

> [!question] Given 16-bit control words, determine the micro-operation and the register change.
> **Initial conditions:** Rn = n (R0=0x00, R1=0x01, ..., R7=0x07). Constant = 0x06, Data\_in = 0x1B.

| | Control Word | Decode | Micro-operation | Register Change |
|---|---|---|---|---|
| a) | `101 100 101 0 1000 0 1` | DA=R5, AA=R4, BA=R5, MB=0, FS=OR, MD=0, RW=1 | F ← A or B | R5 ← R4 or R5 = 0x05 |
| b) | `110 010 100 0 0101 0 1` | DA=R6, AA=R2, BA=R4, MB=0, FS=SUB, MD=0, RW=1 | F ← A + B̄ + 1 | R6 ← R2 − R4 = 0xFE |
| c) | `101 110 000 0 1100 0 1` | DA=R5, AA=R6, BA=R0, MB=0, FS=MOVB, MD=0, RW=1 | F ← B | R5 ← R0 = 0x00 |
| d) | `101 000 000 0 0000 0 1` | DA=R5, AA=R0, BA=R0, MB=0, FS=MOVA, MD=0, RW=1 | F ← A | R5 ← R0 = 0x00 |
| e) | `100 100 000 1 1101 0 1` | DA=R4, AA=R4, BA=-, MB=1, FS=sr B, MD=0, RW=1 | F ← sr B | R4 ← sr(Constant) = 0x03 |
| f) | `011 000 000 0 0000 1 1` | DA=R3, AA=R0, BA=R0, MB=0, FS=A, MD=1, RW=1 | R[DA] ← Data\_In | R3 ← 0x1B |

> [!note]- Calculations
> **a)** R4 OR R5 = 0x04 OR 0x05 = `00000100` OR `00000101` = `00000101` = 0x05
> (R5 stays at 0x05 — no effective change)
>
> **b)** R2 − R4 = 0x02 − 0x04 = 0x02 + NOT(0x04) + 1 = 0x02 + 0xFB + 1 = 0xFE (= −2 signed)
>
> **c)** FS=1100 = MOVB (F = B). B = R0 = 0x00. R5 ← 0x00.
>
> **d)** FS=0000 = MOVA (F = A). A = R0 = 0x00. R5 ← 0x00.
>
> **e)** MB=1 so B = Constant = 0x06 = `00000110`. sr(0x06) = `00000011` = 0x03.
>
> **f)** MD=1 bypasses the function unit. R3 ← Data\_In = 0x1B. FS output is ignored.

---

## 5.4 Program Counter Timing Diagram

> [!question]
> A) Find PC values for each clock cycle. Initial PC = 0x45.
> B) Specify the RTL operation for each cycle.

| Cycle | PS | Offset | Addr\_In | RTL Operation | PC |
|---|---|---|---|---|---|
| — | — | — | — | Initial value | **0x45** |
| 1 | 00 | 0xF1 | 0xXX | PC ← PC | **0x45** |
| 2 | 00 | 0xF1 | 0xXX | PC ← PC | **0x45** |
| 3 | 01 | 0x7 | 0x55 | PC ← PC + 1 | **0x46** |
| 4 | 01 | 0x7 | 0x55 | PC ← PC + 1 | **0x47** |
| 5 | 01 | 0x7 | 0x55 | PC ← PC + 1 | **0x48** |
| 6 | 01 | 0x7 | 0x01 | PC ← PC + 1 | **0x49** |
| 7 | 10 | 0xE8 | 0x01 | PC ← PC + Offset | **0x31** |
| 8 | 10 | 0xE8 | 0x01 | PC ← PC + Offset | **0x19** |
| 9 | 01 | 0xE8 | 0xF1 | PC ← PC + 1 | **0x1A** |
| 10 | 11 | 0xE8 | 0xF1 | PC ← Addr\_In | **0xF1** |

> [!note]- Calculations
> **PS=00 (Hold):** PC unchanged = 0x45
>
> **PS=01 (Increment):** 0x45→0x46→0x47→0x48→0x49
>
> **PS=10 (Branch), Offset=0xE8 (= −24 signed):**
> - Cycle 7: 0x49 + 0xE8 = 0x131, mod 256 = **0x31** (73 − 24 = 49)
> - Cycle 8: 0x31 + 0xE8 = 0x119, mod 256 = **0x19** (49 − 24 = 25)
>
> **PS=01 (Increment):** 0x19 + 1 = **0x1A**
>
> **PS=11 (Jump):** PC ← Address\_In = **0xF1**

---

## 5.5 Zero-Filler and Sign-Extender Outputs

> [!question] For each 16-bit instruction, find the Zero-filler and Extended-sign module outputs.

> [!info] Module Definitions
> **Zero-Filler:** `ZF = "00000" & IR(2) & IR(1) & IR(0)`
>
> **Sign-Extender:**
> - If IR(8) = 0: `SE = "000" & IR(7) & IR(6) & IR(2) & IR(1) & IR(0)`
> - If IR(8) = 1: `SE = "111" & IR(7) & IR(6) & IR(2) & IR(1) & IR(0)`

| | Instruction (IR) | IR(8) | IR(7:6) | IR(2:0) | Zero-Filler | Sign-Extender |
|---|---|---|---|---|---|---|
| a) | `1011001010100001` | 0 | 10 | 001 | **00000001** | **00010001** |
| b) | `1100101000010101` | 0 | 00 | 101 | **00000101** | **00000101** |
| c) | `1011100100110001` | 1 | 00 | 001 | **00000001** | **11100001** |
| d) | `1010000000000001` | 0 | 00 | 001 | **00000001** | **00000001** |
| e) | `1001000101110101` | 1 | 01 | 101 | **00000101** | **11101101** |
| f) | `0110000100000011` | 1 | 00 | 011 | **00000011** | **11100011** |

> [!note]- Calculations
> **Bit indexing:** Position 15 (MSB, leftmost) down to 0 (LSB, rightmost).
>
> **a)** IR = `1 0 1 1 0 0 1 | 0 | 1 0 | 1 0 0 | 0 0 1`
> IR(8)=0, IR(7:6)=10, IR(2:0)=001
> ZF = 00000\_001 = 0x01
> SE = 000\_10\_001 = 0x11 (positive, prefix 000)
>
> **b)** IR = `1 1 0 0 1 0 1 | 0 | 0 0 | 0 1 0 | 1 0 1`
> IR(8)=0, IR(7:6)=00, IR(2:0)=101
> ZF = 00000\_101 = 0x05
> SE = 000\_00\_101 = 0x05
>
> **c)** IR = `1 0 1 1 1 0 0 | 1 | 0 0 | 1 1 0 | 0 0 1`
> IR(8)=1, IR(7:6)=00, IR(2:0)=001
> ZF = 00000\_001 = 0x01
> SE = 111\_00\_001 = 0xE1 (negative, prefix 111)
>
> **d)** IR = `1 0 1 0 0 0 0 | 0 | 0 0 | 0 0 0 | 0 0 1`
> IR(8)=0, IR(7:6)=00, IR(2:0)=001
> ZF = 00000\_001 = 0x01
> SE = 000\_00\_001 = 0x01
>
> **e)** IR = `1 0 0 1 0 0 0 | 1 | 0 1 | 1 1 0 | 1 0 1`
> IR(8)=1, IR(7:6)=01, IR(2:0)=101
> ZF = 00000\_101 = 0x05
> SE = 111\_01\_101 = 0xED
>
> Wait — `11101101` = 0xED, not what I wrote. Let me recheck...
> 111\_01\_101 = 11101101 = 0xED ✓
>
> **f)** IR = `0 1 1 0 0 0 0 | 1 | 0 0 | 0 0 0 | 0 1 1`
> IR(8)=1, IR(7:6)=00, IR(2:0)=011
> ZF = 00000\_011 = 0x03
> SE = 111\_00\_011 = 0xE3

---

> [!nav]
> [[Opg 3 - Function Unit & Adder-Subtractor|← Opg 3]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
