---
course: "62711"
course-name: "Digital Systems Design"
type: lecture-note
week: 8
date: 2026-02-20
tags: [DSD, lecture]
---
# Lecture 03 - Adders, Multiplication & Micro-operations

> [!info] Course Information
> **Course:** 62711 Design af digitale systemer
> **Date:** 2026-02-20
> **Lecturer:** jmgm, osch@dtu.dk
> **Book reference:** Logic & Computer Design Fundamentals, M.M. Mano & C.R. Kime, 5th ed., Pearson, 2016
> **Pages:** 3.9–3.12, 6.1–6.8, 8.2–8.4
> **Slides:** [[Preparation slides lesson 3.pdf|Preparation slides]] · [[62711_lesson3_f2026.pdf|Lecture slides]]
> **Supplements:** [[05_Carrylookahead_supp4.pdf|Carry-lookahead]] · [[06_Mulitpliers_Dividers_supp4.pdf|Multipliers & Dividers]]

---

## ALU Architecture Recap

![[attachments/lecture03/prep_04.png]]

> [!note] ALU Symbol ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|Figure 8-2, p.437]])
> The ALU is the central computational block of the datapath. It accepts two n-bit operands **A** and **B**, along with control signals, and produces an n-bit result **G** plus status flags.
>
> **Control signals:**
> - $S_2$ — selects between **arithmetic** ($S_2 = 0$) and **logic** ($S_2 = 1$) operations
> - $S_1, S_0$ — select the specific operation within arithmetic or logic mode
> - $C_{in}$ — carry input (only used in arithmetic mode)
>
> **Outputs:**
> - $G$ — n-bit result
> - $C_{out}$ — carry out (from arithmetic unit)
> - $V$ — overflow flag ($V = C_n \oplus C_{n-1}$)
>
> > *Textbook: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|§8-3, Figure 8-2, p.437]]*

---

## Arithmetic Circuit (Figure 8-3)

![[attachments/lecture03/prep_05.png]]

> [!note] Block Diagram ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=455|§8-3, Figure 8-3, p.438]])
> The arithmetic circuit consists of three main blocks:
>
> 1. **B Input Logic** — processes B based on $S_0$, $S_1$ to produce Y
> 2. **n-bit Parallel Adder** — computes $G = A + Y + C_{in}$
> 3. **Output** — G (n-bit result) and $C_{out}$
>
> The key insight is that **a single adder can perform 8 different arithmetic operations** by controlling what value Y is fed alongside A.

### B Input Logic (Figure 8-4)

![[attachments/lecture03/prep_07.png]]

> [!important] B Input Logic — One Stage ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=456|§8-3, Figure 8-4, p.439]])
> The select signals $S_1$ and $S_0$ control what value $Y_i$ is fed to the adder:
>
> | $S_1$ | $S_0$ | $Y_i$ | Description |
> |---|---|---|---|
> | 0 | 0 | $0$ | All zeros |
> | 0 | 1 | $B_i$ | B pass-through |
> | 1 | 0 | $\overline{B_i}$ | B complement |
> | 1 | 1 | $1$ | All ones |
>
> **Karnaugh map derivation:**
>
> | | $S_0 = 0$ | $S_0 = 1$ |
> |---|---|---|
> | **$S_1 = 0$, $B_i = 0$** | 0 | 0 |
> | **$S_1 = 0$, $B_i = 1$** | 0 | 1 |
> | **$S_1 = 1$, $B_i = 0$** | 1 | 1 |
> | **$S_1 = 1$, $B_i = 1$** | 1 | 0 |
>
> Simplified expression:
> $$\boxed{Y_i = S_0 \cdot B_i \oplus S_1}$$
>
> This is equivalent to: $Y_i = B_i \cdot S_0 + \overline{B_i} \cdot S_1$ (when expanded without XOR).

### Function Table (Table 8-1)

![[attachments/lecture03/prep_06.png]]

> [!abstract] Arithmetic Circuit Operations ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=455|§8-3, Table 8-1, p.438]])
>
> | $S_1$ | $S_0$ | $C_{in}$ | $Y$ | $G = A + Y + C_{in}$ | Function |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | $0\ldots0$ | $A$ | **Transfer A** |
> | 0 | 0 | 1 | $0\ldots0$ | $A + 1$ | **Increment A** |
> | 0 | 1 | 0 | $B$ | $A + B$ | **Add** |
> | 0 | 1 | 1 | $B$ | $A + B + 1$ | **Add with carry** |
> | 1 | 0 | 0 | $\overline{B}$ | $A + \overline{B}$ | **A + 1's comp B** |
> | 1 | 0 | 1 | $\overline{B}$ | $A + \overline{B} + 1$ | **Subtract (A − B)** |
> | 1 | 1 | 0 | $1\ldots1$ | $A - 1$ | **Decrement A** |
> | 1 | 1 | 1 | $1\ldots1$ | $A$ | **Transfer A** |
>
> > [!tip] Key insight
> > Subtraction works because $A + \overline{B} + 1 = A + (2^n - 1 - B) + 1 = A - B + 2^n$, and the $2^n$ is the carry-out which is discarded.

### 4-Bit Arithmetic Circuit (Figure 8-5)

![[attachments/lecture03/prep_08.png]]

> [!note] Logic Diagram ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=457|§8-3, Figure 8-5, p.440]])
> The four full-adder (FA) circuits constitute the parallel adder. The carry into the first stage is the input carry $C_{in}$. All other carries are connected internally from one stage to the next. The selection variables $S_1$, $S_0$, and $C_{in}$ control all Y inputs of the full adders according to the B input logic expression $Y_i = B_i S_0 + \overline{B_i} S_1$.

**Annotated lecture version:**

![[attachments/lecture03/slide_05.png]]

---

## Logic Circuit (Figure 8-6)

![[attachments/lecture03/prep_09.png]]

> [!note] Logic Unit Stage ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=458|§8-3, Figure 8-6, p.441]])
> Each bit of the logic unit uses a **4-to-1 MUX** controlled by $S_0$ and $S_1$ to select between four bitwise operations:
>
> | $S_1$ | $S_0$ | Output |
> |---|---|---|
> | 0 | 0 | $A_i \text{ AND } B_i$ |
> | 0 | 1 | $A_i \text{ OR } B_i$ |
> | 1 | 0 | $A_i \text{ XOR } B_i$ |
> | 1 | 1 | $\text{NOT } A_i$ |
>
> > [!warning] I PWA er AND/OR byttet om i forhold til Table 8.2 i bogen!

> [!abstract] Full ALU Function Table ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=458|§8-3, Table 8-2, p.441]])
>
> | $S_2$ | $S_1$ | $S_0$ | $C_{in}$ | Operation | Function |
> |---|---|---|---|---|---|
> | 0 | 0 | 0 | 0 | $G = A$ | Transfer A |
> | 0 | 0 | 0 | 1 | $G = A + 1$ | Increment A |
> | 0 | 0 | 1 | 0 | $G = A + B$ | Addition |
> | 0 | 0 | 1 | 1 | $G = A + B + 1$ | Add with carry |
> | 0 | 1 | 0 | 0 | $G = A + \overline{B}$ | A plus 1s complement of B |
> | 0 | 1 | 0 | 1 | $G = A + \overline{B} + 1$ | Subtraction |
> | 0 | 1 | 1 | 0 | $G = A - 1$ | Decrement A |
> | 0 | 1 | 1 | 1 | $G = A$ | Transfer A |
> | 1 | X | 0 | 0 | $G = A \wedge B$ | AND |
> | 1 | X | 0 | 1 | $G = A \vee B$ | OR |
> | 1 | X | 1 | 0 | $G = A \oplus B$ | XOR |
> | 1 | X | 1 | 1 | $G = \overline{A}$ | NOT (1s complement) |

---

## One Stage of the ALU (Figure 8-7)

![[attachments/lecture03/prep_10.png]]

> [!note] Combined Arithmetic + Logic Unit ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=459|§8-3, Figure 8-7, p.442]])
> A single ALU stage combines:
>
> 1. **B Input Logic** — produces $Y_i$ from $B_i$, $S_0$, $S_1$
> 2. **Full Adder** — computes arithmetic result from $A_i + Y_i + C_i$
> 3. **Logic Unit (4-to-1 MUX)** — computes bitwise logic from $A_i$ and $B_i$
> 4. **Output MUX** — $S_2$ selects between arithmetic result ($S_2 = 0$) and logic result ($S_2 = 1$)
>
> The n-bit ALU is constructed by instantiating n copies of this one-stage design and chaining the carry signals.

---

## Combinatorial Shifter (Figure 8-8)

![[attachments/lecture03/prep_11.png]]

> [!note] 4-Bit Basic Shifter ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=460|§8-4, Figure 8-8, p.443]])
> The combinatorial shifter shifts data by one position using multiplexers:
>
> | Operation | $S$ | Output |
> |---|---|---|
> | **No shift** | 00 | $H_i = B_i$ |
> | **Shift Right** | 01 | $H_3 = I_R$, $H_2 = B_3$, $H_1 = B_2$, $H_0 = B_1$ |
> | **Shift Left** | 10 | $H_3 = B_2$, $H_2 = B_1$, $H_1 = B_0$, $H_0 = I_L$ |
>
> Where:
> - $I_L$ = serial input for left shift (typically 0 for logical shift)
> - $I_R$ = serial input for right shift (typically 0 for logical shift, or $B_3$ for arithmetic shift)
>
> Each output bit $H_i$ is a **3-to-1 MUX** selecting between no-shift, left-shifted, and right-shifted input.
>
> > [!tip] Shift types
> > - **Logical shift:** Fill with 0 ($I_L = 0$ or $I_R = 0$)
> > - **Arithmetic right shift:** Preserve sign ($I_R = B_{n-1}$)
> > - **Rotate:** Wrap around ($I_L = B_{n-1}$ for left, $I_R = B_0$ for right)

---

## Binary Multiplication

![[attachments/lecture03/prep_12.png]]

> [!note] Multiplication by Partial Products ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=194|§3-12, pp.177–182]]; Supplement: [[06_Mulitpliers_Dividers_supp4.pdf]])
> Binary multiplication follows the same principle as decimal long multiplication:
>
> $$\text{Multiplicand} \times \text{Multiplier} = \sum \text{Partial Products}$$
>
> Each partial product is either **the multiplicand** (if the multiplier bit is 1) or **zero** (if the multiplier bit is 0), shifted to the appropriate position.
>
> **Example — 2-bit × 2-bit ($A_1A_0 \times B_1B_0$):**
>
> ```
>         A₁  A₀
>     ×   B₁  B₀
>     ──────────
>       A₁B₀  A₀B₀       (partial product 0: multiplicand AND B₀)
>  A₁B₁  A₀B₁             (partial product 1: multiplicand AND B₁, shifted left)
>  ────────────────
>   C₃   C₂  C₁  C₀       (4-bit product)
> ```
>
> Each partial product bit is simply an **AND gate**: $P_{ij} = A_i \cdot B_j$

### Decimal & Binary Examples

![[attachments/lecture03/prep_13.png]]

### 2×2 Multiplier Array

![[attachments/lecture03/prep_14.png]]

> [!example] 2-Bit Multiplier Implementation
> The 2×2 multiplier produces a 4-bit result $C_3C_2C_1C_0$:
>
> $$C_0 = A_0 \cdot B_0$$
> $$C_1 = A_1 \cdot B_0 \oplus A_0 \cdot B_1$$
> $$C_2 = A_1 \cdot B_1 \oplus \text{carry from } C_1$$
> $$C_3 = \text{carry from } C_2$$
>
> Hardware: **4 AND gates** (for partial products) + **half adders** for summing.

### Cellular Array Multiplier

![[attachments/lecture03/prep_15.png]]

> [!note] n×n Multiplier Array
> For larger multiplications, a **cellular array** (or array multiplier) is used:
>
> - Each cell contains an **AND gate** and a **full adder**
> - The AND gate computes the partial product bit: $P_{ij} = A_i \cdot B_j$
> - The full adder sums the partial product with the accumulated sum and carry from the row above
> - The array has **n rows** and **n columns**, producing a **2n-bit** product
>
> **Advantages:**
> - Regular, systematic structure — ideal for VHDL `generate` statements
> - All partial products computed in parallel (AND gates)
>
> **Disadvantage:**
> - Carry propagation through the array creates significant delay: $O(n^2)$ gate delays
>
> > [!tip] Wide Adders for Partial Product Summation
> > An alternative to the cellular array is to use **wide adders** (e.g., carry-save or Wallace tree adders) to sum the partial products more efficiently. This reduces the critical path from $O(n^2)$ to $O(n \log n)$.

---

## Other Arithmetic Functions (Contraction)

![[attachments/lecture03/prep_16.png]]

> [!note] Contraction — Simplified Circuits for Special Operations ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=194|§3-12, pp.177–182]])
> When one operand is a **constant**, the general multiplier/adder can be drastically simplified:
>
> | Operation | How |
> |---|---|
> | **Increment** ($A + 1$) | Half-adder chain (no B input, $C_0 = 1$) |
> | **Decrement** ($A - 1$) | Add all-ones ($Y = 1\ldots1$, $C_0 = 0$) |
> | **Multiply by constant** | Remove AND gates for zero bits in the constant ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=198|Fig. 3-53, p.181]]) |
> | **Divide by constant** | Similar simplification of the divider array |
> | **Zero fill** | Hardwire specific bits to 0 |
>
> > [!tip] Multiply/Divide by Powers of 2 ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=199|§3-12, p.182]])
> > Multiplication by $2^k$ = **shift left** by $k$ positions (fill with zeros).
> > Division by $2^k$ = **shift right** by $k$ positions (logical or arithmetic).
> >
> > These require **no adder at all** — just wiring (routing), making them essentially free in hardware.

![[attachments/lecture03/prep_18.png]]

---

## Fixed-Point Division

![[attachments/lecture03/prep_17.png]]

> [!note] Binary Division Algorithm (Supplement: [[06_Mulitpliers_Dividers_supp4.pdf]])
> Binary division works similarly to long division in decimal:
>
> 1. **Compare** the divisor with the current partial remainder
> 2. If the partial remainder $\geq$ divisor: subtract and set quotient bit = 1
> 3. If the partial remainder $<$ divisor: do not subtract, set quotient bit = 0
> 4. **Shift** the partial remainder left and bring down the next dividend bit
> 5. Repeat for each bit of the quotient
>
> **Hardware implementation:**
> - Uses a **subtract-and-compare** approach
> - Each stage: subtractor + MUX (select original or subtracted value based on borrow)
> - Can be implemented as a **cellular array** similar to the multiplier
>
> > [!warning] Division is expensive
> > Division requires significantly more hardware and/or clock cycles than multiplication. Many simple processors avoid hardware division entirely and implement it in software.

---

## Registers and Micro-operations

> [!note] Register Notation ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=341|§6-1, pp.324–326]])
> Registers are the basic storage elements in a digital system:
>
> - **R0, R1, ..., R15** — individual registers (e.g., 8-bit wide)
> - **R(0)** — bit 0 of register R
> - **R(7:4)** — bits 7 down to 4 of register R (a sub-field)
>
> Registers are loaded on a clock edge when their **load** (enable) signal is active.

### Control of Register Transfers

> [!important] Register Transfer Language ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=344|§6-2, pp.327–329]])
> A register transfer describes data movement between registers:
>
> $$K_1: \quad R_1 \leftarrow R_2$$
>
> This means: "If control signal $K_1$ is active, load the contents of $R_2$ into $R_1$ on the next clock edge."
>
> **Key principles:**
> - The transfer occurs **synchronously** on the active clock edge
> - $K_1$ is a **condition** (derived from control logic / state machine)
> - The source register ($R_2$) is **not modified** — data is *copied*, not moved
> - Multiple transfers can happen simultaneously if they target different registers

---

## Micro-operations

> [!abstract] Types of Micro-operations ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=349|§6-5, pp.332–337]])
> Micro-operations are the elementary operations performed on data stored in registers:
>
> ### Arithmetic Micro-operations
>
> | Notation | Operation | Description |
> |---|---|---|
> | $R_3 \leftarrow R_1 + R_2$ | Addition | Add contents of R1 and R2, store in R3 |
> | $R_3 \leftarrow R_1 - R_2$ | Subtraction | Subtract R2 from R1 (via 2's complement add) |
> | $R_1 \leftarrow R_1 + 1$ | Increment | Add 1 to R1 |
> | $R_1 \leftarrow R_1 - 1$ | Decrement | Subtract 1 from R1 |
> | $R_1 \leftarrow \overline{R_1} + 1$ | Negate | 2's complement of R1 |
>
> ### Logical Micro-operations
>
> | Notation | Operation | Description |
> |---|---|---|
> | $R_1 \leftarrow R_1 \wedge R_2$ | AND | Bitwise AND |
> | $R_1 \leftarrow R_1 \vee R_2$ | OR | Bitwise OR |
> | $R_1 \leftarrow R_1 \oplus R_2$ | XOR | Bitwise exclusive OR |
> | $R_1 \leftarrow \overline{R_1}$ | NOT | Bitwise complement |
>
> ### Shift Micro-operations
>
> | Notation | Operation | Description |
> |---|---|---|
> | $R_1 \leftarrow sl\;R_1$ | Shift Left | Shift all bits left, fill LSB with 0 |
> | $R_1 \leftarrow sr\;R_1$ | Shift Right | Shift all bits right, fill MSB with 0 |

---

## Register Transfer Structures

> [!note] Multiplexer-Based Transfer ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=354|§6-6, pp.337–339]])
> When multiple sources can write to a single register, a **multiplexer** selects which source is loaded:
>
> ```
>   R1 ──┐
>   R2 ──┤ MUX ──→ R_dest
>   R3 ──┤  ↑
>   R4 ──┘  │
>          SEL
> ```
>
> The select signals come from the **control unit** and determine which register's data reaches the destination on each clock cycle.

> [!note] Bus-Based Transfer ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=376|§6-8, pp.359–363]])
> A **bus** is a shared set of wires that multiple registers can drive (one at a time) or read from:
>
> - **Writing to the bus:** Only one register drives the bus at a time (controlled by tri-state buffers or multiplexer)
> - **Reading from the bus:** Any register with its load signal active captures the bus data on the clock edge
>
> A bus reduces wiring but limits transfers to one source at a time per bus.

---

## VHDL Implementations

### 2-to-4 Decoder — single bit

![[attachments/lecture03/slide_12.png]]

> [!example] Decoder — Dataflow Style (from slide)
> ```vhdl
> entity decoder_2_4 is
>     Port ( i2 : in STD_LOGIC_VECTOR (1 downto 0);
>            en : in std_logic;
>            O4 : out STD_LOGIC_VECTOR (3 downto 0));
> end decoder_2_4;
>
> architecture Behavioral of decoder_2_4 is
>     signal A0n, A1n : std_logic;
> begin
>     A0n <= not I2(0);
>     A1n <= not I2(1);
>     O4(0) <= A0n and A1n and en;
>     O4(1) <= i2(0) and A1n and en;
>     O4(2) <= A0n and i2(1) and en;
>     O4(3) <= I2(0) and I2(1) and en;
> end Behavioral;
> ```
>
> Each output is an AND of the enable signal with the appropriate combination of input bits and their complements. This is a **structural/dataflow** style — no `when-else`, just direct Boolean equations.

### 4-to-1 Multiplexer — structural (using decoder)

![[attachments/lecture03/slide_13.png]]

> [!example] MUX 4×1 — Built from Decoder + AND-OR (from slide)
> The multiplexer instantiates the 2-to-4 decoder and adds AND-OR gates:
>
> ```vhdl
> entity Four_to_one_mux is
>     Port ( I   : in STD_LOGIC_VECTOR (3 downto 0);
>            sel : in STD_LOGIC_VECTOR (1 downto 0);
>            mux_out : out STD_LOGIC);
> end Four_to_one_mux;
>
> architecture Behavioral of Four_to_one_mux is
>     component decoder_2_to_4 is
>         Port ( EN, A0, A1 : in STD_LOGIC;
>                D0, D1, D2, D3 : out STD_LOGIC);
>     end component;
>     signal D0_in, D1_in, D2_in, D3_in : std_logic;
> begin
>     U0 : decoder_2_to_4 port map (
>         en => '1',
>         A0 => sel(0),
>         A1 => sel(1),
>         D0 => D0_in,
>         D1 => D1_in,
>         D2 => D2_in,
>         D3 => D3_in
>     );
>
>     mux_out <= (D0_in and I(0)) or (D1_in and I(1))
>             or (D2_in and I(2)) or (D3_in and I(3));
> end Behavioral;
> ```
>
> > [!tip] Design pattern
> > A MUX = **decoder** (to activate one path) + **AND-OR** (to gate data through). The Vivado hierarchy shows `Four_to_one_mux` containing `decoder_2_to_4` as a sub-component.

### Mux4x1x8 from mux4x1 (generate statement)

![[attachments/lecture03/slide_14.png]]

> [!example] MUX 4×1×8 — 8-Bit Wide using Generate (from slide)
> Uses a `generic` for parameterizable width and a `generate` loop to instantiate 8 single-bit MUXes:
>
> ```vhdl
> entity mux4x1x8 is
>     generic (width : integer := 8);
>     Port ( I0, I1, I2, I3 : in STD_LOGIC_VECTOR (width-1 downto 0);
>            sel : in STD_LOGIC_VECTOR (1 downto 0);
>            Y   : out STD_LOGIC_VECTOR (width-1 downto 0));
> end mux4x1x8;
>
> architecture Behavioral of mux4x1x8 is
>     component Four_to_one_mux is
>         Port ( I       : in STD_LOGIC_VECTOR (3 downto 0);
>                sel     : in STD_LOGIC_VECTOR (1 downto 0);
>                mux_out : out STD_LOGIC);
>     end component;
> begin
>     U_MUX0: for i in 0 to width-1 generate
>         U0: Four_to_one_mux port map (
>             I(0) => I0(i),
>             I(1) => I1(i),
>             I(2) => I2(i),
>             I(3) => I3(i),
>             sel  => sel(1 downto 0),
>             mux_out => Y(i)
>         );
>     end generate;
> end Behavioral;
> ```
>
> > [!tip] Generate statement
> > The `for ... generate` loop creates `width` instances of the 1-bit MUX at elaboration time. Each instance connects one bit from each of the four input vectors. This is the VHDL equivalent of "copy-paste n times" — but parameterizable.

### MUX16x1x8 from 4x1x8

![[attachments/lecture03/slide_15.png]]

> [!example] MUX 16×1×8 — Built from mux4x1x8 (from slide)
> A 16-to-1 multiplexer is constructed hierarchically from five 4-to-1 multiplexers:
>
> ```vhdl
> entity MUX16x1x8 is
>     generic (width : integer := 8);
>     Port ( R0,R1,R2,R3,R4,R5,R6,R7,
>            R8,R9,R10,R11,R12,R13,R14,R15 : in STD_LOGIC_VECTOR (width-1 downto 0);
>            D_select : in STD_LOGIC_VECTOR (3 downto 0);
>            Y_data   : out STD_LOGIC_VECTOR (width-1 downto 0));
> end MUX16x1x8;
>
> architecture Behavioral of MUX16x1x8 is
>     component mux4x1x8 is
>         generic (width : integer := 8);
>         Port ( I0, I1, I2, I3 : in STD_LOGIC_VECTOR (width-1 downto 0);
>                sel : in STD_LOGIC_VECTOR (1 downto 0);
>                Y   : out STD_LOGIC_VECTOR (width-1 downto 0));
>     end component;
>     signal Y0, Y1, Y2, Y3 : std_logic_vector(width-1 downto 0);
> begin
>     -- First level: 4 MUXes, each selecting from 4 of the 16 register inputs
>     U0: mux4x1x8 port map (
>         I0 => R0,  I1 => R1,  I2 => R2,  I3 => R3,
>         sel => D_select(1 downto 0), Y => Y0);
>     U1: mux4x1x8 port map (
>         I0 => R4,  I1 => R5,  I2 => R6,  I3 => R7,
>         sel => D_select(1 downto 0), Y => Y1);
>     U2: mux4x1x8 port map (
>         I0 => R8,  I1 => R9,  I2 => R10, I3 => R11,
>         sel => D_select(1 downto 0), Y => Y2);
>     U3: mux4x1x8 port map (
>         I0 => R12, I1 => R13, I2 => R14, I3 => R15,
>         sel => D_select(1 downto 0), Y => Y3);
>
>     -- Second level: 1 MUX selects among the 4 first-level outputs
>     U4: mux4x1x8 port map (
>         I0 => Y0, I1 => Y1, I2 => Y2, I3 => Y3,
>         sel => D_select(3 downto 2), Y => Y_data);
> end Behavioral;
> ```
>
> > [!tip] Hierarchy
> > The lower 2 select bits (`D_select(1:0)`) choose within each group of 4 registers. The upper 2 select bits (`D_select(3:2)`) choose which group. The `a,b,c,d` signals on the slide correspond to `sel(0), sel(1), sel(2), sel(3)`.

![[attachments/lecture03/slide_16.png]]

### Shifter 8-bit — based upon mux 4-to-1 single bit

![[attachments/lecture03/slide_17.png]]

> [!example] 8-Bit Shifter using MUX instances (from slide)
> Each output bit is a 4-to-1 MUX selecting between: no shift (00), shift right (01), shift left (10):
>
> ```vhdl
> entity Shifter is
>     Port ( B        : in STD_LOGIC_VECTOR (7 downto 0);
>            H_Select : in STD_LOGIC_VECTOR (1 downto 0);
>            H        : out STD_LOGIC_VECTOR (7 downto 0));
> end Shifter;
>
> architecture Behavioral of Shifter is
>     component mux4to1 is
>         Port ( mux_i : in STD_LOGIC_VECTOR (3 downto 0);
>                mux_o : out STD_LOGIC;
>                sel   : in STD_LOGIC_VECTOR (1 downto 0));
>     end component;
>     signal hs : std_logic_vector(1 downto 0);
> begin
>     hs <= "00" when H_Select = "--" else H_Select;
>
>     -- mux_i(0) = no shift, mux_i(1) = shift right, mux_i(2) = shift left, mux_i(3) = no shift
>     U0: mux4to1 port map(mux_i(0)=>B(0), mux_i(1)=>B(1),  mux_i(2)=>'0',  mux_i(3)=>B(0), sel=>hs, mux_o=>H(0));
>     U1: mux4to1 port map(mux_i(0)=>B(1), mux_i(1)=>B(2),  mux_i(2)=>B(0), mux_i(3)=>B(1), sel=>hs, mux_o=>H(1));
>     U2: mux4to1 port map(mux_i(0)=>B(2), mux_i(1)=>B(3),  mux_i(2)=>B(1), mux_i(3)=>B(2), sel=>hs, mux_o=>H(2));
>     U3: mux4to1 port map(mux_i(0)=>B(3), mux_i(1)=>B(4),  mux_i(2)=>B(2), mux_i(3)=>B(3), sel=>hs, mux_o=>H(3));
>     U4: mux4to1 port map(mux_i(0)=>B(4), mux_i(1)=>B(5),  mux_i(2)=>B(3), mux_i(3)=>B(4), sel=>hs, mux_o=>H(4));
>     U5: mux4to1 port map(mux_i(0)=>B(5), mux_i(1)=>B(6),  mux_i(2)=>B(4), mux_i(3)=>B(5), sel=>hs, mux_o=>H(5));
>     U6: mux4to1 port map(mux_i(0)=>B(6), mux_i(1)=>B(7),  mux_i(2)=>B(5), mux_i(3)=>B(6), sel=>hs, mux_o=>H(6));
>     U7: mux4to1 port map(mux_i(0)=>B(7), mux_i(1)=>'0',   mux_i(2)=>B(6), mux_i(3)=>B(7), sel=>hs, mux_o=>H(7));
> end Behavioral;
> ```
>
> > [!note] Shift encoding
> > | `H_Select` | Operation | `mux_i` mapping |
> > |---|---|---|
> > | `00` | No shift | `mux_i(0) = B(i)` → pass-through |
> > | `01` | Shift right | `mux_i(1) = B(i+1)` (or `'0'` for MSB) |
> > | `10` | Shift left | `mux_i(2) = B(i-1)` (or `'0'` for LSB) |
> >
> > Each bit position instantiates a `mux4to1` where the MUX inputs are wired to the appropriate neighbor bits. Serial inputs (`I_R`, `I_L`) are hardcoded to `'0'` for logical shifts.

---

## VHDL Test Benches

### Combinational Test Bench (with loop)

![[attachments/lecture03/slide_18.png]]

> [!example] Test Bench for Combinational Logic (from slide)
> Uses `IEEE.numeric_std.all` for `to_unsigned` and a **loop** to iterate over all inputs:
>
> ```vhdl
> library IEEE;
> use IEEE.Std_logic_1164.all;
> use IEEE.Numeric_Std.all;
>
> -- ... entity/architecture with component instantiation ...
>
> uut: decoder4to16 port map ( A => A,
>                               en => en,
>                               D => D );
>
> stimulus: process
> begin
>     en <= '0';
>     wait for 20ns;
>     en <= '1';
>
>     for i in 0 to 15 loop
>         wait for 20 ns;
>         A <= std_logic_vector(to_unsigned(i, 4));
>         wait for 20 ns;
>     end loop;
>
>     wait for 20 ns;
>     wait;
> end process;
> ```
>
> > [!tip] Key pattern
> > - `to_unsigned(i, 4)` converts integer `i` to a 4-bit unsigned value
> > - `std_logic_vector(...)` converts it to the signal type
> > - The loop systematically tests all 16 input combinations
> > - Start with `en <= '0'` to verify the enable works, then set `en <= '1'`

### Sequential Test Bench (with clock)

![[attachments/lecture03/slide_19.png]]

> [!example] Test Bench for Sequential Logic (from slide)
> Two processes: one for clock, one for asynchronous input. Uses a **time constant** for the clock period:
>
> ```vhdl
> component RegisterFile
>     Port ( RESET : in STD_LOGIC;
>            Clk   : in STD_LOGIC;
>            rw    : in STD_LOGIC;
>            DA,AA,BA : in STD_LOGIC_VECTOR (3 downto 0);
>            D_Data   : in STD_LOGIC_VECTOR (7 downto 0);
>            A_Data,B_Data : out STD_LOGIC_VECTOR (7 downto 0));
> end component;
>
> signal RESET, STD_LOGIC;
> signal Clk : STD_LOGIC;
> signal rw : STD_LOGIC;
> signal DA,AA,BA : STD_LOGIC_VECTOR (3 downto 0);
> signal D_Data : STD_LOGIC_VECTOR (7 downto 0);
> signal A_Data,B_Data : STD_LOGIC_VECTOR (7 downto 0);
>
> constant clk_period : time := 10ns;
> constant end_test : std_logic := '1';
>
> -- Clock process
> clock: process
> begin
>     while end_test = '1' loop
>         Clk <= '0';
>         wait for clk_period*0.5;
>         Clk <= '1';
>         wait for clk_period*0.5;
>     end loop;
>     wait;
> end process;
>
> -- Stimulus process
> stimulus: process
> begin
>     Reset <= '0';
>     rw <= '0';
>     DA <= "0000";
>     AA <= "0000";
>     BA <= "0000";
>     D_data <= x"00";
>
>     wait for clk_period;
>     rw <= '1';
>     D_data <= x"0F";
>     wait for clk_period*2;
>     AA <= "0001";
>     BA <= "0001";
>     wait for clk_period;
>     DA <= "0001";
>     wait for clk_period*2;
>     end_test <= '0';
> end process;
> ```
>
> > [!tip] Key differences from combinational test benches
> > - A **clock process** uses `while end_test = '1' loop` to run continuously until signaled to stop
> > - `constant clk_period : time := 10ns` defines the clock period as a named constant
> > - Stimulus uses `wait for clk_period` and multiples thereof to stay synchronized
> > - The `end_test` signal allows the clock to stop cleanly at the end of simulation

### Using Assert for Self-Checking Test Benches

> [!tip] Assert Statements
> Instead of manually inspecting waveforms, use `assert` to automatically verify outputs:
>
> ```vhdl
> -- Check that output matches expected value
> assert (Y = "10110011")
>     report "ERROR: Y should be 10110011, got " & to_string(Y)
>     severity error;
>
> -- Can also use severity levels: note, warning, error, failure
> assert (C_out = '0')
>     report "Unexpected carry out"
>     severity failure;  -- stops simulation immediately
> ```
>
> **Typical pattern in a stimulus process:**
> ```vhdl
> stim_proc: process
> begin
>     -- Apply inputs
>     A <= "00001111"; B <= "00000001";
>     S1 <= '0'; S0 <= '1'; Cin <= '0';  -- Addition
>     wait for 100 ns;
>     assert (G = "00010000")
>         report "Addition failed" severity error;
>
>     -- Next test vector
>     S1 <= '1'; S0 <= '0'; Cin <= '1';  -- Subtraction
>     wait for 100 ns;
>     assert (G = "00001110")
>         report "Subtraction failed" severity error;
>
>     report "All tests passed" severity note;
>     wait;
> end process;
> ```
>
> **Advantages:**
> - Simulation is **self-checking** — no need to visually inspect waveforms
> - Errors are reported with descriptive messages in the console
> - `severity failure` can halt simulation on critical errors
> - Ideal for regression testing when modifying the design later

---

> [!todo] Preparation for Lecture 4
> **Date:** 27-02-2026
> - Book sections: Chapter 6.2–6.8
> - Topics: Micro-operations, register transfer, shift registers, counters
> - Continue PWA — function unit implementation

---

> [!summary] Key Takeaways
> 1. The **ALU** combines an arithmetic unit, logic unit, and shifter — selected by control signals $S_2$, $S_1$, $S_0$, $C_{in}$
> 2. **B input logic** ($Y_i = S_0 \cdot B_i \oplus S_1$) allows a single adder to perform 8 operations (transfer, increment, add, subtract, decrement, etc.)
> 3. The **combinatorial shifter** uses MUXes per bit to shift left or right by one position
> 4. **Binary multiplication** uses partial products (AND gates) summed by an adder array; multiplying by $2^k$ is just a wire shift
> 5. **Contraction** simplifies hardware when one operand is a known constant (increment, multiply by constant, etc.)
> 6. **Micro-operations** are the atomic register-level actions: arithmetic ($+, -, ++, --$), logical (AND, OR, XOR, NOT), and shift ($sl, sr$)
> 7. **Register transfers** ($K_1: R_1 \leftarrow R_2$) are conditional and synchronous — controlled by the state machine
> 8. Large MUXes (16×1) are built **hierarchically** from smaller MUXes (4×1), matching decoder expansion principles
> 9. **Test benches** for combinational circuits use `wait for`; sequential test benches add a clock process and reset initialization

---

> [!info] Textbook References
> | Topic | Section | Pages | Key Figures |
> |---|---|---|---|
> | Binary Adders | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=174|§3-9]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=174|pp.157–160]] | Fig. 3-39 to 3-43 |
> | Binary Subtraction | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=178|§3-10]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=178|pp.161–164]] | — |
> | Adder-Subtractors | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=182|§3-11]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=182|pp.165–176]] | Fig. 3-44 to 3-50 |
> | Other Arithmetic Functions | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=194|§3-12]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=194|pp.177–183]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=198|Fig. 3-52, 3-53]] |
> | Registers & Load Enable | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=341|§6-1]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=341|pp.324–326]] | — |
> | Register Transfers | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=344|§6-2]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=344|pp.327–329]] | — |
> | Microoperations | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=349|§6-5]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=349|pp.332–337]] | — |
> | Datapaths | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=451|§8-2]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=451|pp.434–437]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|Fig. 8-2 (ALU symbol)]] |
> | Arithmetic/Logic Unit | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|§8-3]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|pp.437–442]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=454|Fig. 8-3 to 8-7, Tables 8-1, 8-2]] |
> | The Shifter | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=460|§8-4]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=460|pp.443–444]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=460|Fig. 8-8]] |

---

> [!nav]
> [[Lecture 02 - Arithmetic Circuits & ALU|← Lecture 02]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> [[Lecture 04 - Function Unit|Lecture 04 →]]
