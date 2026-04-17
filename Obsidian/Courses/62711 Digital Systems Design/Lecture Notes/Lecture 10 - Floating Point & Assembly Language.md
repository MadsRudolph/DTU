---
course: "62711"
course-name: "Digital Systems Design"
type: lecture-note
week: 16
date: 2026-04-17
tags: [DSD, lecture, floating-point, assembly, ISA]
---
# Lecture 10 - Floating Point & Assembly Language Programming

> [!info] Course Information
> **Course:** 62711 Design af digitale systemer
> **Date:** 2026-04-17 (Week 16)
> **Lecturer:** jmgm, osch@dtu.dk
> **Book reference:** Logic & Computer Design Fundamentals, M.M. Mano & C.R. Kime, 5th ed., Pearson, 2016
> **Pages:** 9.1–9.5, 9.6–9.9 (pp. ~490, 493, 512–516, 528)
> **Slides:** [[Preparation_slides_lecture 10_floating_point_aritmetic_and Instructions.pdf|Preparation slides]] · [[62711_lesson10_F2026.pdf|Lecture slides]]
> **Supplements:** [[Converting decimal number to floating point and floating point to decimal.pdf|Conversion guide]] · [[kapitel2Og3_fra e-bookThe Atmel AVR microcontroller.pdf|AVR microcontroller (ch. 2–3)]] · [[Assembler mockup guide_v4.pdf|Assembler mockup guide]]

---

## Part 1 — Floating Point Numbers

> [!cite] PWF connection — theory only
> PWF does **not** implement floating-point hardware. The microprocessor uses 16-bit instruction words with 8-bit data (low byte) on an 8-bit address bus. This half of the lecture is pensum for the oral exam; the quiz in [[Quiz 10]] covers the IEEE-754 mechanics likely to appear there.

### Scientific Notation Recap

> [!note] Floating-point is just scientific notation in binary
> A floating-point number is represented as two independent fields — a **fraction** (mantissa) and an **exponent** — together with a sign:
>
> $$\text{value} = F \cdot \beta^{E}$$
>
> - **Decimal example:** $+0.54367 \cdot 10^{+4}$ → fraction $+.54367$, exponent $+04$
> - **Binary example:** $+1001.11_2$ → normalised as $+0.100111_2 \cdot 2^{4}$, generalised to $F \cdot 2^{E}$
>
> A number is **normalised** when the most significant digit is non-zero (e.g. $0.350$ is normalised, $0.0350$ is not). Normalisation removes redundancy in the representation: each value has exactly one encoding.
>
> **Range extension:** a 48-bit fixed point register covers roughly $\pm 2^{47}$. Split instead into 1 sign + 35 fraction + 12 exponent and the range becomes $\pm (1 - 2^{-35}) \cdot 2^{+2047}$ — a dramatic improvement at the cost of relative precision.

---

### Biased Exponent

> [!important] Why bias the exponent?
> The fraction is stored as **signed magnitude** — easy. The exponent, however, is a signed number that would otherwise require two's complement. Storing it with a **bias (excess) offset** turns it into an unsigned integer:
>
> $$e_{\text{stored}} = E_{\text{actual}} + \text{bias}$$
>
> - Decimal example: exponents in the range $-99 \ldots +99$, bias $= 99$ → stored range $0 \ldots 198$
> - Result: the stored exponent field is always $\geq 0$, enabling **unsigned comparators** and **unsigned sorting** of floating-point values.
>
> > [!tip] Comparison insight
> > Because sign, exponent, and fraction are packed MSB-to-LSB with *biased* exponent, two IEEE 754 numbers of the same sign can be compared as plain unsigned integers — no float hardware needed.

#### Exercise 1 — Bias Examples

| Value | Bias ($2^{k-1} - 1$) | Biased decimal | Biased binary |
|---|---|---|---|
| $+56$ | $2^6 - 1 = 63$ | $56 + 63 = 119$ | `1110111` (7-bit) |
| $+178$ | $2^8 - 1 = 255$ | $178 + 127 = 305$ | `110110001` (9-bit) |
| $+1002$ | $2^{10} - 1 = 1023$ | $1002 + 1023 = 2025$ | `11111101001` (11-bit) |
| $+7586$ | $2^{13} - 1 = 8191$ | $7586 + 8191 = 15777$ | `11110110100001` (14-bit) |
| $-56$ | 63 | $63 - 56 = 7$ | `0000111` |
| $-178$ | 255 | $255 - 178 = 77$ | `001001110` |
| $-1002$ | 1023 | $1023 - 1002 = 21$ | `000000010100` |
| $-7586$ | 8191 | $8191 - 7586 = 605$ | `00001001011101` |

---

### IEEE 754 Single Precision

> [!abstract] 32-bit Single Precision Layout ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=545|§9-7, p.528]])
>
> ```
>  31  30 ─── 23  22 ──────────────── 0
> ┌─┬──────────┬───────────────────────┐
> │s│    e     │          f            │
> └─┴──────────┴───────────────────────┘
>  1     8              23           bits
> ```
>
> | Field | Bits | Role |
> |---|---|---|
> | **s** (sign) | 1 | 0 = positive, 1 = negative |
> | **e** (biased exponent) | 8 | excess-127, valid range 1 … 254 for normals |
> | **f** (fraction) | 23 | mantissa without the implicit leading 1 |
>
> **Value formula:**
>
> $$\boxed{\text{value} = (-1)^{s} \cdot 2^{(e - 127)} \cdot \left(1 + \sum_{i=1}^{23} b_{23-i} \cdot 2^{-i}\right)}$$
>
> The `1 + ...` term is the **significand** — the leading `1.` is implicit (never stored) because normalised numbers always begin with 1. Hardware inserts it back during computation.

> [!warning] Reserved encodings
> - $e = 0$  → ±0 (if f = 0) or **denormal/subnormal** numbers (if f ≠ 0)
> - $e = 255$ → ±∞ (if f = 0) or **NaN** (if f ≠ 0)
>
> Valid exponent range for **normal** numbers: $E \in [-126, +127]$.

#### Range of Single Precision

> [!note] Largest and smallest positive normals
>
> | | Bits | $E$ | Significand | Value |
> |---|---|---|---|---|
> | **Largest** | `0 11111110 11…1` | $254 - 127 = 127$ | $1 + (1 - 2^{-23}) = 2 - 2^{-23}$ | $(2 - 2^{-23}) \cdot 2^{127} \approx 3.4 \cdot 10^{38}$ |
> | **Smallest normal** | `0 00000001 00…0` | $1 - 127 = -126$ | $1.0$ | $2^{-126} \approx 1.18 \cdot 10^{-38}$ |

#### Worked Example — 0x3E200000 → 0.15625

> [!example] Decoding `0 01111100 01000000000000000000000` ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=545|Fig. 9-14, p.528]])
>
> | Step | Result |
> |---|---|
> | Sign bit $s = 0$ | $(-1)^0 = +1$ |
> | Exponent $e = 01111100_2 = 124$ | $E = 124 - 127 = -3$ |
> | Fraction: only $b_{21} = 1$ | $1.f = 1 + 2^{-2} = 1.25$ |
> | Combine | $+1 \cdot 2^{-3} \cdot 1.25 = 0.125 \cdot 1.25 = 0.15625$ |

> [!tip] Conversion workflow — decimal → IEEE 754
> 1. Separate sign and absolute value.
> 2. Convert the absolute value to pure binary (integer part by divide-by-2, fraction by multiply-by-2).
> 3. Normalise to `1.xxx × 2^E`.
> 4. Biased exponent $e = E + 127$.
> 5. Take the 23 bits after the leading `1.` as the fraction field.
> 6. Pack `[s | e | f]` and regroup into nibbles for hex.
>
> Reverse direction: split the hex into sign/exponent/fraction, subtract 127, re-insert the implicit leading 1, and sum $1 + \sum b_{23-i} 2^{-i}$.
>
> Detailed walkthroughs live in [[Converting decimal number to floating point and floating point to decimal.pdf|Converting decimal number to floating point and floating point to decimal]].

---

## Part 2 — Assembly Language Programming

> [!cite] PWF connection — this half IS PWF
> Everything in Part 2 maps directly onto the [[PWF Project|PWF microprocessor]]. The lecture's assembly model, opcode table, addressing modes, control-word states, datapath diagram, memory-mapped I/O table and the Java assembler are all the pieces you need for step 6 of the project (*"Implement step-by-step the microcode of the program to perform a task"*, [[62711_ProjectWork_F_F2026.pdf|spec p.3]]).

### Assembly Language Model

> [!note] Stored-program machine ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=509|§9-3, p.492]])
> Instructions live in memory. The **Program Counter (PC)** points to the next instruction to fetch; the CPU fetches, decodes, and executes one instruction at a time, then advances the PC.
>
> ```
>      ┌────┐     ┌──────────────┐
>      │ PC │ ──▶ │  Instruction │
>      └────┘     │    stream    │
>                 │  ADD  R1,R2,R3
>                 │  SUB  R4,R5,R6
>                 │  JMP  R3
>                 │  LDI  R4, LRI
>                 │      R2, R5
>                 │  BRZ  R6, -6
>                 └──────┬───────┘
>                        ▼
>     ┌──────┐   ┌───────────┐   ┌────────┐
>     │ ALU  │◀─▶│ Registers │◀─▶│ Memory │
>     └──────┘   └───────────┘   └────────┘
> ```
>
> Assembly is **one step up from machine language** — a symbolic mnemonic for each opcode and operand. Originally a programmer-friendly notation, today mostly a compiler target.

> [!cite] PWF connection — this is the PWF top-level
> The block on the right — **PC + IR + Registers + ALU + Memory** — is literally the `Microprocessor` entity in PWF:
>
> - **PC + IR + Instruction Decoder/Controller** = `MicroprogramController` (from PWB)
> - **Registers + ALU + Shifter** = `Datapath` (from PWA)
> - **Memory** = `Ram256x16` + `PortReg8x8` (new in PWF)
>
> See [[PWF Project#Top-Level Hierarchy]] and the block diagram on [[62711_ProjectWork_F_F2026.pdf|PWF spec p.4]].

---

### Instruction Anatomy

> [!important] Two-piece instructions
> Every assembly instruction consists of an **opcode** (what to do — an ALU operation or control action) and one or more **operands** (what to do it to).
>
> ```
>     ADD    R1, R3, R2
>     ↑       ↑    ↑  ↑
>   Opcode  Dest  Src1 Src2
> ```
>
> Convention in this course: **destination first**, followed by source operands.

> [!cite] PWF connection — 16-bit instruction layout
> In PWF every instruction is a **16-bit word** stored in `Ram256x16`. The Instruction Register splits it into four fields used by the controller:
>
> | Bits | Field | Typical meaning |
> |---|---|---|
> | 15–9 | **Opcode** (7 bits) | ALU op, memory op, or control transfer — see table below |
> | 8–6 | **IR876** (3 bits) | Destination register `DA` (0..7) |
> | 5–3 | **IR543** (3 bits) | A-source register `AA` (0..7) |
> | 2–0 | **IR210** (3 bits) | B-source register `BA` **or** zero-filled immediate |
>
> The controller routes these bits into `DA`, `AA`, `BA` via the `DX`, `AX`, `BX` selectors. See the PWF instruction table on [[62711_ProjectWork_F_F2026.pdf|spec p.1]].

---

### Types of Opcodes

> [!abstract] Opcode Families (from lecture slide 4)
>
> | Family | Examples | Purpose |
> |---|---|---|
> | **Arithmetic / Logical / Shift / Move** | `ADD`, `SUB`, `INC`, `DEC`, `ADI`, `LDI`, `AND`, `OR`, `XOR`, `NOT`, `SHR`, `SHL`, `MOVA`, `MOVB` | ALU-level data manipulation |
> | **Memory load / store** | `LD`, `ST` | Transfer between registers and memory |
> | **Control transfer** | `JMP`, `BRZ`, `BRN` | Modify Program Counter |
> | **Complex** | `LRI`, `SRM`, … | Multi-step / indirect operations |
> | **Advanced** | `CALL`, `RET`, `JA/JB` (unsigned), `JG/JL` (signed), `JE/JNE`, `JC/JV`, `LOOP`, `LOOPE`, `LOONE`, `INT`, `INTV` | Subroutines, conditional jumps by flag, loops, interrupts |
>
> Flags referenced:
>
> | Flag | Meaning |
> |---|---|
> | Z | Zero result |
> | N | Negative result |
> | C | Carry out |
> | V | Overflow |

> [!cite] PWF connection — implemented opcodes
> PWF implements a concrete subset of the general opcode families — the ones listed below with their 7-bit encodings (from [[62711_ProjectWork_F_F2026.pdf|PWF spec p.1]]):
>
> | Family | PWF opcodes | Encoding (binary) |
> |---|---|---|
> | Move / arithmetic / logical | `MOVA`, `INC`, `ADD`, `SUB`, `DEC`, `OR`, `AND`, `XOR`, `NOT`, `MOVB` | `0000000` … `0001100` |
> | Memory load/store | `LD`, `ST` | `0010000`, `0100000` |
> | Immediate | `LDI`, `ADI` | `1001100`, `1000010` |
> | Control transfer | `BRZ` (branch if Z), `BRN` (branch if N), `JMP` | `1100000`, `1100001`, `1110000` |
> | Complex (multi-state) | `LRI` (indirect load), `SRM`, `SLM` (shift right/left multiple) | `0010001`, `0001101`, `0001110` |
>
> Advanced opcodes (`CALL`/`RET`/`LOOP`/`INT`, signed/unsigned compare jumps) are **not** implemented in PWF — they are shown for context only.
>
> Reminder: `LRI`, `SRM`, `SLM` reserve **R8 and R9** as internal scratch registers, so those cannot be used as operands.

---

### Operands & Addressing Modes

> [!note] Each operand comes from a specific **register** or encodes a memory access ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=509|pp. 490, 493, 512–516]])
>
> | Mode | Example | Effect |
> |---|---|---|
> | **Register** | `ADD R1, R2, R3` | $R[1] \leftarrow R[2] + R[3]$ |
> | **Immediate** | `ADI R1, R2, 4` | $R[1] \leftarrow R[2] + \text{zf}(4)$ — constant baked into the instruction word |
> | **Direct** (register indirect) | `LD R1, R4` | $R[1] \leftarrow M[R[4]]$ — R4 holds the memory address |
> | **Indirect** | `LRI R1, R7` | $R[1] \leftarrow M[M[R[7]]]$ — double dereference |
> | **Offset** (PC-relative) | `BRZ R1, offset` | if Z then $PC \leftarrow PC + \text{zf}(\text{offset})$ |
> | **PC Jump** | `JMP R3` | $PC \leftarrow R[3]$ — register holds the target address |
>
> Addressing modes **reflect the processor's data pathways** — each mode maps to a specific sequence of control-word states in the datapath.
>
> More info: [osdata — assembly addressing](http://www.osdata.com/topic/language/asm/address.htm)

> [!cite] PWF connection — each mode is a real instruction
> Every addressing mode in the table corresponds to a specific PWF instruction you must support:
>
> | Mode | PWF instruction | What to test on the board |
> |---|---|---|
> | Register | `ADD D0 A1 B2`, `SUB`, `AND`, `OR`, … | Compute `R[0] ← R[1] + R[2]` and display on LEDs |
> | Immediate | `ADI`, `LDI` | `R[0] ← R[1] + 4` — immediate baked into IR210, MB mux picks the zero-filler |
> | Direct (register indirect) | `LD`, `ST` | Load from `M[R[SA]]` — used when accessing `MR3`-`MR7` via buttons |
> | Indirect | `LRI` | Double-dereference — uses scratch register R8 |
> | Offset (PC-relative) | `BRZ`, `BRN` | `PC ← PC + offset` when flag condition holds |
> | PC Jump | `JMP` | `PC ← R[SA]` — unconditional jump |
>
> These are the instructions you write in step 6 of the PWF assignment. Test each mode with a minimal program before combining them.

---

### Control-Word States for LRI, LDI, LD, ST

> [!example] Multi-state instructions in the PWF datapath
> Some instructions take more than one clock cycle because they require multiple memory accesses. The control word sequences (from lecture slide 10) are:
>
> **LRI — Load via Register Indirect** (`R[DR] ← M[M[R[SA]]]`, two memory reads)
>
> | State | Opcode | NS | IL | PS | DX | AX | BX | MB | FS | MD | RW | MM | MW |
> |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
> | EX0 | `0010001` | EX1 | 0 | 00 | `1000` | `0IR543` | `XIR210` | X | `0000` | 1 | 1 | 0 | 0 |
> | EX1 | `0010001` | INF | 0 | 01 | `0IR876` | `1000` | `XIR210` | X | `0000` | 1 | 1 | 0 | 0 |
>
> **ADI — Add Immediate** (`R[DR] ← R[SA] + zf(BX)`, single cycle)
>
> | State | DX | AX | BX | MB | FS | MD | RW | MM | MW |
> |---|---|---|---|---|---|---|---|---|---|
> | EX0 | `0 IR876` | `0IR543` | `XIR210` | 1 | `0010` | 0 | 1 | 0 | 0 |
>
> **LD (\*)** — Load Direct (`R[DR] ← M[R[SA]]`)
>
> | State | DX | AX | BX | MB | FS | MD | RW | MM | MW |
> |---|---|---|---|---|---|---|---|---|---|
> | EX0 | `0IR876` | `0IR543` | `X IR210` | X | `XXXX` | 1 | 1 | 0 | 0 |
>
> **ST (\*)** — Store Direct (`M[R[DR]] ← R[SA]`)
>
> | State | DX | AX | BX | MB | FS | MD | RW | MM | MW |
> |---|---|---|---|---|---|---|---|---|---|
> | EX0 | `XIR876` | `0IR543` | `0IR210` | 0 | `XXXX` | X | 0 | 0 | 1 |
>
> > [!tip] Reading the table
> > **MD** (MUX D) selects what gets written back to the register file — 0 = ALU result, 1 = memory data. **MM** (MUX M) and **MW** (Memory Write) together gate the RAM/IO side. For LRI, two states are required because the first state fetches the pointer and the second dereferences it.

> [!cite] PWF connection — this IS the controller truth table
> The rows above are literally the ones your `MicroprogramController` must emit for the `LRI`, `ADI`, `LD`, `ST` opcodes. The full truth table for all 20 PWF opcodes is on [[62711_ProjectWork_F_F2026.pdf|PWF spec p.1]]. Cross-check your control-word ROM contents against it.
>
> Multi-state opcodes and their state transitions in PWF:
>
> | Opcode | States needed | Why |
> |---|---|---|
> | `LRI` | EX0 → EX1 → INF | Two memory reads (pointer, then data) |
> | `SRM` / `SLM` | EX0 → EX1 → EX2 → EX3 → EX4 → INF | Shift-multiple loops using R8, R9 |
> | all single-cycle ops | EX0 → INF | Standard fetch-execute |
>
> Every opcode ends with `NS = INF` (next state = instruction fetch), which also increments PC.

---

### Full Datapath with Memory & I/O

> [!note] Lecture-slide 11 block diagram
> The PWF system integrates the PWA function unit with:
>
> - **Program Counter (PC)** — drives instruction fetch, updated by `PS` (PC Source) and `IL` (Instruction Load)
> - **Instruction Register (IR)** — latched opcode/operand bits: `IR876` (destination), `IR543` (A source), `IR210` (B source / offset)
> - **Sign Extender** & **Zero Filler** — widen the immediate/offset field to the ALU width
> - **Instruction Decoder / Controller** — the state machine producing the control word (DX, AX, BX, MB, FS, MD, RW, MM, MW, NS, PS, IL)
> - **Register File (16 × 8)** — general-purpose registers, two read ports (A, B) and one write port (D)
> - **Function Unit** — the PWA ALU + shifter, plus status flags `V, C, N, Z`
> - **RAM Module / Controller** — 256 × 16-bit main memory (248 addressable + 8 memory-mapped I/O slots)
> - **Port Register Module (8 × 8)** — memory-mapped I/O registers `MR0 … MR7`
>
> Buses: `Data_In`, `Data_Out`, `Address_In`, `Address_Out`, `Data_Bus_Out` and the multiplexers `MUX B`, `MUX D`, `MUX F`, `MUX M`, `MUX MR` that stitch everything together.

> [!cite] PWF connection — this is the `Microprocessor` wrapper
> Slide 11 is the same block diagram as [[62711_ProjectWork_F_F2026.pdf|PWF spec p.4]], numbered boxes **①** (Datapath = PWA), **②** (MicroprogramController = PWB), **③** (RAM + PortReg = new in PWF).
>
> Entity signatures to implement (from spec p.2):
>
> ```vhdl
> entity Ram256X16 is
>   Port ( clk, Reset : in  STD_LOGIC;
>          Data_in    : in  STD_LOGIC_VECTOR(15 downto 0);
>          Address_in : in  STD_LOGIC_VECTOR(7 downto 0);
>          MW         : in  STD_LOGIC;
>          Data_out   : out STD_LOGIC_VECTOR(15 downto 0));
> end Ram256X16;
>
> entity PortReg8x8 is
>   Port ( clk, MW     : in  STD_LOGIC;
>          Data_In     : in  STD_LOGIC_VECTOR(7 downto 0);
>          Address_in  : in  STD_LOGIC_VECTOR(7 downto 0);
>          SW          : in  STD_LOGIC_VECTOR(7 downto 0);
>          BTNC, BTNU, BTNL, BTNR, BTND : in  STD_LOGIC;
>          MMR         : out STD_LOGIC;
>          D_word      : out STD_LOGIC_VECTOR(15 downto 0);
>          Data_outR   : out STD_LOGIC_VECTOR(15 downto 0);
>          LED         : out STD_LOGIC_VECTOR(7 downto 0));
> end PortReg8x8;
> ```
>
> Implement `Ram256X16` using the Xilinx `BRAM_SINGLE_MACRO` primitive (see `ug953-vivado-7series-libraries.pdf` pp. 203–209, or [[PWF Project#RAM]]).

---

### Memory-Mapped I/O Layout

> [!abstract] Register8x8 IO Module (lecture slide 12)
> The upper 8 addresses of the 256-word memory space are **not RAM** — they access the I/O port register module. Reads and writes of these addresses talk to switches, buttons, LEDs and the 7-segment driver rather than to the RAM block.
>
> | Address | Write behaviour | Read behaviour | Memory space |
> |---|---|---|---|
> | `0000.0000` … `1111.0111` (248 words) | `M[Address] ← Data_In` | `Data_Bus_Out ← M[Address]` | RAM, 16-bit words |
> | `1111.1000` | `MR0 ← Data_In` | `Data_Bus_Out ← 0x00 + MR0` | **D_Word low byte** — 8 bits |
> | `1111.1001` | `MR1 ← Data_In` | `Data_Bus_Out ← 0x00 + MR1` | **D_Word high byte** — 8 bits |
> | `1111.1010` | `MR2 ← Data_In` | `Data_Bus_Out ← 0x00 + MR2` | **LED0–7** — 8 bits |
> | `1111.1011` | — (read-only) | `Data_Bus_Out ← 0x00 + MR3` | **Operand 4 — BTNR** — 8 bits |
> | `1111.1100` | — | `Data_Bus_Out ← 0x00 + MR4` | **Operand 3 — BTNL** |
> | `1111.1101` | — | `Data_Bus_Out ← 0x00 + MR5` | **Operand 2 — BTND** |
> | `1111.1110` | — | `Data_Bus_Out ← 0x00 + MR6` | **Operand 1 — BTNU** |
> | `1111.1111` | — | `Data_Bus_Out ← 0x00 + MR7` | **Operand 0 — BTNS** |
>
> The control signals `MW` (memory write enable) and `MM` (MUX M select) drive this address decode; `Data_in = Data_out` outside the I/O window so ordinary load/store instructions "just work" for memory-mapped peripherals.

> [!cite] PWF connection — the `PortReg8x8` entity
> This table *is* the PWF Port Register module. Points to remember when implementing `PortReg8x8.vhd`:
>
> - **Address decode:** assert `MMR = 1` whenever `Address_in(7 downto 3) = "11111"` (i.e. `0xF8`-`0xFF`). `MMR` drives `MUX_MR` to select port-register output over RAM output.
> - **MR0, MR1, MR2** are read/write (D_Word low, D_Word high, LEDs).
> - **MR3-MR7** are read-only from the CPU side. They latch the **switch value (SW)** on the rising edge of the corresponding **button** (BTNR→MR3, BTNL→MR4, BTND→MR5, BTNU→MR6, BTNC→MR7).
> - **D_Word** (16-bit concat of MR1 & MR0) drives the 4-digit 7-segment display via `SevenSegDriver`.
> - PWF step 4 requires timing diagrams for exactly the sequences `read 0x45 / write 0xAA / read 0x45`, `write 0x55→0xF8 / read 0xF8`, `write 0xCC→0xFC / read 0xFC`, and the BTNL + switches scenario. Plan your simulation around these.

---

### Types of Assembly Languages

> [!abstract] Architecture families — Assembly is tied to the processor
>
> | | **CISC** | **RISC** | **DSP** | **VLIW** |
> |---|---|---|---|---|
> | Opcodes | Many, complex | Few, simple | Few, complex | Few, simple |
> | Registers | Few, special | Many, general | Few, special | Many, general |
> | Addressing modes | Many | Few | Special | Few |
> | Instr.-level parallelism | None | None | Restricted | Plenty |
> | Written by | Humans (historically) | Compilers | Humans (hand-tuned) | Compilers |
> | Example | x86 | ARM, MIPS, RISC-V | TI C6x | Itanium, Transmeta |

> [!note] Key trade-offs
> - **CISC** — developed when people still wrote assembly by hand. Complex, specialised instructions (string move, procedure enter/leave) with many side effects and addressing modes. Often internally decoded into *microcode*. Example: x86.
> - **RISC** — response to the rise of compilers. Uniform, easy-to-target instruction set. *Load/store architecture*: ALU operations only on registers; memory touched only by `LD` / `ST`. Pipelines nicely. "Make the most common operations as fast as possible."
> - **DSP** — specialised for signal processing: lots of regular arithmetic on vectors (FIR/FFT). Irregular architectures to save power/area. Substantial ILP via specialised buses and multiply-accumulate hardware. Often written by hand.
> - **VLIW** — response to growing desire for ILP. Many parallel ALUs; each "instruction word" bundles multiple operations scheduled by the compiler. Heavily pipelined; very hard to hand-program; looks like "parallel RISC".

> [!cite] PWF connection — where does the PWF CPU fit?
> PWF is a **minimal RISC-like load/store architecture**: fixed-width (16-bit) instruction words, arithmetic only between registers (except `ADI`/`LDI`), memory touched only by `LD`/`ST`/`LRI`, few addressing modes, single-cycle execution for most opcodes. Classify it as RISC when discussing in the report (introduction section, PWF step 1).

---

### Assembler Tool in PWF

> [!tip] Workflow (`Assembler_v3.zip` on Learn → `ISAassembler`)
> 1. **Write** `asm-test.txt` — one instruction per line: opcode followed by up to three operands `Dy Ay By` (y ∈ 0…7). Omitted operands default to 0. See `asm-test.txt` for a reference of all supported mnemonics.
> 2. **Run** `java -jar Assembler_vX_jreY.jar` (must be launched from the directory containing the jar).
> 3. Pick the source `.txt` when prompted; pick a destination directory for the output.
> 4. **Outputs:**
>    - `machine_output.txt` — one binary machine word per line (0/1)
>    - `hex_output.txt` — hex string(s) ready to paste into the Xilinx block-RAM `INIT_xx` templates
> 5. Every hex string is ≤ 64 chars (16 instructions). **Right-justify** shorter strings by padding the *left* with `0`.
>
> > [!warning] One-space rule (feature!)
> > The current Java assembler parses with **exactly one space** between mnemonic and operands. Multiple spaces cause trailing operands to be silently zeroed. Matches: `add D0 A1 B2` ✅  Breaks: `add  D0 A1 B2` ❌.
> >
> > Also: **no trailing space after the last operand.**

> [!example] Reference mnemonics (from `asm-test.txt`, lecture slide 9)
>
> | Mnemonic | Example | Machine output (16-bit) |
> |---|---|---|
> | `mova` | `mova D0 A1` | `0000000000001000` |
> | `inc` | `inc D0 A1` | `0000001000001000` |
> | `add` | `add D0 A1 B2` | `0000010000001010` |
> | `sub` | `sub D0 A1 B2` | `0000101000001010` |
> | `dec` | `dec D0 A1` | `0000110000001000` |
> | `and` | `and D0 A1 B2` | `0001000000001010` |
> | `or` | `or D0 A1 B2` | `0001001000001010` |
> | `xor` | `xor D0 A1 B2` | `0001010000001010` |
> | `not` | `not D0 A1` | `0001011000001000` |
> | `movb` | `movb D0 B1` | `0001100000000001` |
> | `ld` | `ld D0 A1` | `0010000000001000` |
> | `st` | `st A0 B1` | `0100000000000001` |
> | `ldi` | `ldi D0` | `1001100000000000` |
> | `adi` | `adi D0 A1` | `1000010000001000` |
> | `brz` | `brz A0` | `1100000000000000` |
> | `brn` | `brn A0` | `1100001000000000` |
> | `jmp` | `jmp A0` | `1110000000000000` |
> | `lri` | `lri A0` | `0010001000000000` |
> | `srm` | `srm A0` | `0001101000000000` |
> | `slm` | `slm A0` | `0001110000000000` |
>
> Full `hex_output.txt` for this program:
> ```
> C200C0008408980040012008180116081408140A120A100A0C080A0A040A02080008
> 1C001A002200E000
> ```
>
> In the VHDL block-RAM template:
> ```vhdl
> INIT_00 => X"C200C0008408980040012008180116081408140A120A100A0C080A0A040A02080008",
> INIT_01 => X"000000000000000000000000000000000000000000000000000001C001A002200E000",
> ```

> [!cite] PWF connection — the workflow for step 6
> This is exactly the assembler-to-Block-RAM pipeline you will use to run a program on the PWF board:
>
> 1. **Register-transfer-language** (RTL pseudo-code): write the algorithm as `R[0] ← M[0xFB]`, `R[1] ← R[0] + R[2]`, … (PWF spec step 6 insists on this before translating).
> 2. **Assembly** (`program.txt`): translate RTL into PWF mnemonics using the table on spec p.1 — one instruction per line, one space separator.
> 3. **Assemble:** run `Assembler_vX_jreY.jar`, picking `program.txt` as source.
> 4. **Paste** the generated `hex_output.txt` into the `INIT_00`, `INIT_01`, … `INIT_3F` generics of `BRAM_SINGLE_MACRO` inside your `Ram256x16.vhd`. Remember the right-justify-with-left-pad-zeros rule.
> 5. **Simulate first** (testbench on `Microprocessor` entity) — PWF step 6: *"Do a simulation for the assembly-program in RAM, before testing the program running in the FPGA."*
> 6. **Program the board** and verify with switches/buttons/LEDs/7-seg.
>
> A good first program: read `MR3` (BTNR operand) and `MR4` (BTNL operand), add them, write the result to `MR2` (LEDs) and `MR0`/`MR1` (7-seg). That exercises `LD`, `ADD`, `ST`, all the memory-mapped I/O paths, and demonstrates the whole pipeline in ~10 instructions.

---

> [!todo] Preparation for Lecture 11 (24-04-2026)
> - **Topic:** I/O, Interfaces & Memory Systems
> - **Book sections:** 11.1–11.8, 12.1–12.4
> - **Deliverable reminder:** **MC test PWB before 25 Apr**
> - Assembly language programming continues in lesson 11 (see last prep slide, *"To be continued in lesson 11"*)

> [!todo] PWF action items from this lecture
> - [ ] Implement `Ram256x16.vhd` with BRAM_SINGLE_MACRO (see [[PWF Project#RAM]])
> - [ ] Implement `PortReg8x8.vhd` with `MMR` address decode + button-latched operand registers
> - [ ] Cross-check your `MicroprogramController` control-word ROM against the full PWF opcode table (spec p.1)
> - [ ] Draw the 4 timing diagrams required by PWF step 4 (addresses 0x45, 0xF8, 0xFC, BTNL scenario)
> - [ ] Write a simple RTL program → assemble → simulate → run on board (suggested: BTNR+BTNL → LEDs+7seg)

---

> [!summary] Key Takeaways
> 1. Floating point = **fraction × base^exponent**, normalised so the leading digit is non-zero.
> 2. **Biased exponent** stores the signed exponent as an unsigned integer → enables unsigned comparators.
> 3. **IEEE 754 single:** 1 sign + 8 biased-127 exponent + 23 fraction; value = $(-1)^s \cdot 2^{e-127} \cdot 1.f$.
> 4. Normal-number range: $|x| \in [2^{-126}, (2 - 2^{-23}) \cdot 2^{127}]$. Biased $e = 0$ and $e = 255$ are reserved.
> 5. An **assembly instruction** = opcode + operands; the operand field's addressing mode decides how it is interpreted (register, immediate, direct, indirect, offset, PC-jump).
> 6. Opcode families: arithmetic/logic/shift/move, memory load/store, control transfer, complex, advanced (CALL/RET, conditional jumps, LOOP, INT).
> 7. The PWF datapath adds **PC**, **IR**, **Instruction Decoder/Controller**, RAM and memory-mapped I/O on top of the PWA function unit. Multi-state opcodes (e.g. `LRI`) produce a sequence of control words.
> 8. **CISC vs RISC vs DSP vs VLIW** — assembly is closely tied to the processor; each family reflects a different trade-off between compiler-friendliness, instruction-level parallelism, and specialisation.
> 9. The PWF **Java assembler** emits binary + hex outputs ready for the Xilinx block-RAM `INIT_xx` fields — mind the one-space parsing rule.

---

> [!info] Textbook References
> | Topic | Section | Pages | Key Figures |
> |---|---|---|---|
> | Floating-point representation | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=542\|§9-7]] | pp. 524–530 | Table 9-6, Fig. 9-14 |
> | Instruction formats | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=509\|§9-2]] | pp. 490–493 | — |
> | Addressing modes | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=529\|§9-4]] | pp. 512–516 | — |
> | CISC / RISC / DSP / VLIW | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=525\|§9-6 – 9-9]] | pp. 508–523 | — |

---

> [!nav]
> [[Lecture 03 - Adders|← Lecture 03]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> [[Lecture 11 - I-O Interfaces and Memory Systems|Lecture 11 →]]
