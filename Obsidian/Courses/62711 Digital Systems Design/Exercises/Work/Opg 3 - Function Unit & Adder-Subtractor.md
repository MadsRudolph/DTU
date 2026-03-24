---
course: "62711"
course-name: "Digital Systems Design"
type: exercise
tags: [DSD, exercise]
---
# Opg 3 - Function Unit & Adder-Subtractor

> [!abstract] Exercise Overview
> Register file timing, function unit operations with flags, and adder-subtractor circuits.
> Reference: [[Lecture 02 - Arithmetic Circuits & ALU]] · [[Lecture 03 - Adders]]

> [!info] Files
> - Exercise: [[opg3.pdf|Opg 3]]
> - Solution: [[opg3_solution_opdateret.pdf|Opg 3 solution]]
> - PWA spec: [[62711_ProjectWork_A_F2026.pdf|PWA Project Assignment]]
> - PWA module hierarchy: [[PWA_MODULES]]

---

## 3.1 Register File Timing Diagram

> [!question] The datapath of the PWA has a register file which uses the **rising edge** of the clock. Complete which registers are modified according to the controlling and address lines, as well as the value of A_Data and B_Data.

> [!important] Key Rule
> Data is written to a register **only** when:
> 1. **W = 1** (write enable is active)
> 2. The corresponding **LOAD** bit is active (decoded from DA0-3)
> 3. These conditions hold **before the rising clock edge**
>
> Reading (A_Data, B_Data) is **combinational** — it updates immediately when the address changes.

### Timing Analysis

> [!note] Solution — step by step
> The signals are (reading from the timing diagram):
>
> | Signal | Values over time →|
> |---|---|
> | **CLK** | Rising edges at each transition |
> | **W** | Low → High → Low → High → Low |
> | **DA0-3** | 0x1 → 0x7 → 0xA |
> | **LOAD0-15** | 0x0000 → (active when W=1) → 0x0000 |
> | **D_Data** | 0xXX → 0x56 → 0x01 → 0xF1 |
> | **AA0-3** | 0x1 → 0x7 → 0x2 → 0xF → 0xD |
> | **BA0-3** | 0x1 → 0x1 → 0xA |
>
> **Which registers get written:**
> - When W=1 and DA=0x7: **R7** ← D_Data = **0x01** (at the rising edge where LOAD[7] is active)
> - When W=1 and DA=0xA: **R10** ← D_Data (at the rising edge where LOAD[10] is active)
>
> **A_Data** (combinational read, addressed by AA0-3):
> - AA=0x1 → A_Data = contents of **R1**
> - AA=0x7 → A_Data = contents of **R7**
> - AA=0x2 → A_Data = contents of **R2**
> - AA=0xF → A_Data = contents of **R15**
> - AA=0xD → A_Data = contents of **R13**
>
> **B_Data** (combinational read, addressed by BA0-3):
> - BA=0x1 → B_Data = contents of **R1**
> - BA=0x1 → B_Data = contents of **R1** (unchanged)
> - BA=0xA → B_Data = contents of **R10**

---

## 3.2 Function Unit Operations

> [!question] Complete the output of the function unit and flags (V, C, N, Z) for each of the following input pairs.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|§8-3, pp.437–442]]

> [!info] PWA Function Unit Encoding
> | Operation | Jselect | Hselect | MF | Description |
> |---|---|---|---|---|
> | $F = A + B$ | 0010 | xx | 0 | Addition (arithmetic) |
> | $F = A + \overline{B} + 1$ | 0101 | xx | 0 | Subtraction (arithmetic) |
> | $F = A \oplus B$ | 1x10 | xx | 0 | XOR (logic) |
> | $F = sl\;B$ | xxxx | 10 | 1 | Shift left B (shifter) |
>
> **Flags:**
> - **V** = $C_8 \oplus C_7$ (overflow — only meaningful for arithmetic)
> - **C** = $C_8$ (carry out — only meaningful for arithmetic)
> - **N** = MSB of result (negative / sign bit)
> - **Z** = 1 if result is all zeros
>
> For logic and shift operations, V and C are don't-cares: **X(0)**

---

### A1 = 10010001, B1 = 01100100 (Unsigned: 145, 100)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **11110101** | 0010 | xx | 0 | 0 | 0 | 1 | 0 |
| $F = A + \overline{B} + 1$ | **00101101** | 0101 | xx | 0 | 1 | 1 | 0 | 0 |
| $F = A \oplus B$ | **11110101** | 1x10 | xx | 0 | X(0) | X(0) | 1 | 0 |
| $F = sl\;B$ | **11001000** | xxxx | 10 | 1 | X(0) | X(0) | 1 | 0 |

> [!note]- Calculations
> **A + B:** `10010001 + 01100100 = 11110101` (245). C8=0, C7=0 → V=0, C=0
>
> **A + notB + 1:** notB = `10011011`
> `10010001 + 10011011 + 1 = 1_00101101` → C8=1, C7=0 → V=1, C=1
> (Unsigned: 145 − 100 = 45 = `00101101` ✓)
>
> **A xor B:** `10010001 ⊕ 01100100 = 11110101`
>
> **sl B:** `01100100` shifted left = `11001000` (fill LSB with 0)

---

### A2 = 10010001, B2 = 10100011 (Unsigned: 145, 163)

| Operation                  | Function Unit Output | Jselect | Hselect | MF  | V     | C    | N   | Z   |
| -------------------------- | -------------------- | ------- | ------- | --- | ----- | ---- | --- | --- |
| $F = A + B$                | **00110100**         | 0010    | xx      | 0   | **1** | 1    | 0   | 0   |
| $F = A + \overline{B} + 1$ | **11101110**         | 0101    | xx      | 0   | 0     | 0    | 1   | 0   |
| $F = A \oplus B$           | **00110010**         | 1x10    | xx      | 0   | X(0)  | X(0) | 0   | 0   |
| $F = sl\;B$                | **01000110**         | xxxx    | 10      | 1   | X(0)  | X(0) | 0   | 0   |

> [!note]- Calculations
> **A + B:** `10010001 + 10100011 = 1_00110100` (308).
> ```
>   10010001
> + 10100011
> ----------
> 1 00110100
> ```
> Carry chain: c0→c1→c2 propagates through bits 0-1, then dies at bit 2.
> C7=0 (carry into bit 7), C8=1 (carry out of bit 7: 1+1+0=0, c=1).
> V = C8 ⊕ C7 = 1 ⊕ 0 = **1** (signed: −111 + (−93) = −204, overflows [-128,127]). C=1
>
> **A - B:** notB = `01011100`
> `10010001 + 01011100 + 1 = 11101110`. C8=0, C7=0 → V=0, C=0
>
> **A xor B:** `10010001 ⊕ 10100011 = 00110010`
>
> **sl B:** `10100011` shifted left = `01000110`

---

### A3 = 00001000, B3 = 11111000 (Unsigned: 8, 248)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **00000000** | 0010 | xx | 0 | 0 | 1 | 0 | **1** |
| $F = A + \overline{B} + 1$ | **00010000** | 0101 | xx | 0 | 0 | 0 | 0 | 0 |
| $F = A \oplus B$ | **11110000** | 1x10 | xx | 0 | X(0) | X(0) | 1 | 0 |
| $F = sl\;B$ | **11110000** | xxxx | 10 | 1 | X(0) | X(0) | 1 | 0 |

> [!note]- Calculations
> **A + B:** `00001000 + 11111000 = 1_00000000` (8 + 248 = 256, wraps to 0).
> Carry propagates through all five 1-bits of B (bits 3-7): C7=1, C8=1.
> V = C8 ⊕ C7 = 1 ⊕ 1 = 0. C=1, Z=1 ✓
>
> **A − B:** notB = `00000111`, `00001000 + 00000111 + 1 = 00010000` (= 16).
> Carry propagates through bits 0-3, then stops: C7=0, C8=0.
> V = 0 ⊕ 0 = 0 (signed: 8 − (−8) = 16, fits in [−128,127] → no overflow). C=0
>
> **A xor B:** `00001000 ⊕ 11111000 = 11110000`
>
> **sl B:** `11111000` shifted left = `11110000`

---

### A4 = 00011000, B4 = 00100111 (2's Complement: +24, +39)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **00111111** | 0010 | xx | 0 | 0 | 0 | 0 | 0 |
| $F = A + \overline{B} + 1$ | **11110001** | 0101 | xx | 0 | 0 | 0 | 1 | 0 |
| $F = A \oplus B$ | **00111111** | 1x10 | xx | 0 | X(0) | X(0) | 0 | 0 |
| $F = sl\;B$ | **01001110** | xxxx | 10 | 1 | X(0) | X(0) | 0 | 0 |

> [!note]- Calculations
> **A + B:** `00011000 + 00100111 = 00111111` (24 + 39 = 63). C8=0, C7=0 → V=0 ✓
>
> **A - B:** notB = `11011000`, `00011000 + 11011000 + 1 = 11110001` (24 − 39 = −15).
> Signed: −15 in 2's comp = `11110001` ✓. C8=0 → C=0, V=0
>
> **A xor B:** `00011000 ⊕ 00100111 = 00111111`
>
> **sl B:** `00100111` shifted left = `01001110`

---

### A5 = 00011000, B5 = 00011000 (2's Complement: +24, +24)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **00110000** | 0010 | xx | 0 | 0 | 0 | 0 | 0 |
| $F = A + \overline{B} + 1$ | **00000000** | 0101 | xx | 0 | 0 | 1 | 0 | **1** |
| $F = A \oplus B$ | **00000000** | 1x10 | xx | 0 | X(0) | X(0) | 0 | **1** |
| $F = sl\;B$ | **00110000** | xxxx | 10 | 1 | X(0) | X(0) | 0 | 0 |

> [!note]- Calculations
> **A + B:** `00011000 + 00011000 = 00110000` (24 + 24 = 48). C8=0, V=0 ✓
>
> **A - B:** `00011000 + 11100111 + 1 = 1_00000000` (24 − 24 = 0). C8=1 → C=1, result = 0 → Z=1 ✓
>
> **A xor B:** `00011000 ⊕ 00011000 = 00000000` (identical values → all zeros) → Z=1 ✓
>
> **sl B:** `00011000` shifted left = `00110000`

---

### A6 = 10011000, B6 = 10100111 (2's Complement: −104, −89)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **00111111** | 0010 | xx | 0 | **1** | 1 | 0 | 0 |
| $F = A + \overline{B} + 1$ | **11110001** | 0101 | xx | 0 | 0 | 0 | 1 | 0 |
| $F = A \oplus B$ | **00111111** | 1x10 | xx | 0 | X(0) | X(0) | 0 | 0 |
| $F = sl\;B$ | **01001110** | xxxx | 10 | 1 | X(0) | X(0) | 0 | 0 |

> [!note]- Calculations
> **A + B:** `10011000 + 10100111 = 1_00111111` (−104 + −89 = −193, doesn't fit!).
> C8=1, C7=0 → V=1 ✓ (negative + negative = positive → **overflow**)
>
> **A - B:** notB = `01011000`, `10011000 + 01011000 + 1 = 11110001` (−104 − (−89) = −15).
> C8=0, C7=0 → V=0, C=0 ✓
>
> **A xor B:** `10011000 ⊕ 10100111 = 00111111`
>
> **sl B:** `10100111` shifted left = `01001110`

---

### A7 = 01010011, B7 = 01110110 (Binary: 83, 118)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **11001001** | 0010 | xx | 0 | **1** | 0 | 1 | 0 |
| $F = A + \overline{B} + 1$ | **11011101** | 0101 | xx | 0 | 0 | 0 | 1 | 0 |
| $F = A \oplus B$ | **00100101** | 1x10 | xx | 0 | X(0) | X(0) | 0 | 0 |
| $F = sl\;B$ | **11101100** | xxxx | 10 | 1 | X(0) | X(0) | 1 | 0 |

> [!note]- Calculations
> **A + B:** `01010011 + 01110110 = 11001001` (83 + 118 = 201).
> C8=0, C7=1 → V=1 (positive + positive = negative → **overflow** in signed)
>
> **A - B:** notB = `10001001`, `01010011 + 10001001 + 1 = 11011101` (83 − 118 = −35).
> C8=0, C7=0 → V=0, C=0
>
> **A xor B:** `01010011 ⊕ 01110110 = 00100101`
>
> **sl B:** `01110110` shifted left = `11101100`

---

### A8 = 01010010, B8 = 01010101 (Binary: 82, 85)

| Operation | Function Unit Output | Jselect | Hselect | MF | V | C | N | Z |
|---|---|---|---|---|---|---|---|---|
| $F = A + B$ | **10100111** | 0010 | xx | 0 | **1** | 0 | 1 | 0 |
| $F = A + \overline{B} + 1$ | **11111101** | 0101 | xx | 0 | 0 | 0 | 1 | 0 |
| $F = A \oplus B$ | **00000111** | 1x10 | xx | 0 | X(0) | X(0) | 0 | 0 |
| $F = sl\;B$ | **10101010** | xxxx | 10 | 1 | X(0) | X(0) | 1 | 0 |

> [!note]- Calculations
> **A + B:** `01010010 + 01010101 = 10100111` (82 + 85 = 167).
> C8=0, C7=1 → V=1 (positive + positive = negative → **overflow**)
>
> **A - B:** notB = `10101010`, `01010010 + 10101010 + 1 = 11111101` (82 − 85 = −3).
> C8=0, C7=0 → V=0, C=0
>
> **A xor B:** `01010010 ⊕ 01010101 = 00000111`
>
> **sl B:** `01010101` shifted left = `10101010`

---

> [!tip] Use this content to test the FU in the PWA!
> These input pairs and expected outputs can be directly used as test vectors in a VHDL test bench for the Function Unit. Use `assert` statements to verify each case automatically.

---

## 3.3 Adder-Subtractor (Book 3.11)

> [!question] The adder-subtractor has input select S and data inputs A and B. Determine the values of outputs S3, S2, S1, S0 and C4.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=182|§3-11, pp.165–170]]

> [!info] Adder-Subtractor Operation
> - **S = 0** → Addition: $\text{Result} = A + B$, $C_0 = 0$
> - **S = 1** → Subtraction: $\text{Result} = A + \overline{B} + 1$, $C_0 = 1$
>
> Each $B_i$ is XORed with S before entering the full adder. When S=1, B is complemented and the carry-in of 1 completes the 2's complement.

| Case | S | A | B | $B \oplus S$ | S3 S2 S1 S0 | C4 |
|---|---|---|---|---|---|---|
| **A** | 0 | 0111 | 0111 | 0111 | **1110** | **0** |
| **B** | 1 | 0100 | 0111 | 1000 | **1101** | **0** |
| **C** | 1 | 1101 | 1010 | 0101 | **0011** | **1** |
| **D** | 0 | 0111 | 1010 | 1010 | **0001** | **1** |
| **E** | 1 | 0001 | 1000 | 0111 | **1001** | **0** |

> [!note]- Detailed Calculations
>
> **Case A** (S=0, Addition): $0111 + 0111 = 1110$, C4=0
> ```
>   0111
> + 0111
> ------
>   1110   C4=0
> ```
>
> **Case B** (S=1, Subtraction): $0100 + \overline{0111} + 1 = 0100 + 1000 + 1$
> ```
>   0100
> + 1000
> +    1
> ------
>   1101   C4=0
> ```
> (4 − 7 = −3, in 2's comp 4-bit: `1101` ✓)
>
> **Case C** (S=1, Subtraction): $1101 + \overline{1010} + 1 = 1101 + 0101 + 1$
> ```
>   1101
> + 0101
> +    1
> ------
> 1 0011   C4=1
> ```
> (13 − 10 = 3 unsigned, or −3 − (−6) = 3 signed ✓)
>
> **Case D** (S=0, Addition): $0111 + 1010 = 10001$
> ```
>   0111
> + 1010
> ------
> 1 0001   C4=1
> ```
> (7 + 10 = 17, overflow in 4 bits)
>
> **Case E** (S=1, Subtraction): $0001 + \overline{1000} + 1 = 0001 + 0111 + 1$
> ```
>   0001
> + 0111
> +    1
> ------
>   1001   C4=0
> ```
> (1 − 8 = −7, in 2's comp 4-bit: `1001` ✓)

---

> [!nav]
> [[Opg 2 - Digital Arithmetic|← Opg 2]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
