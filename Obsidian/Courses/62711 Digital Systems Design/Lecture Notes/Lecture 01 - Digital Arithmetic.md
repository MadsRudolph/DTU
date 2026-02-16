---
course: "62711"
course-name: "Digital Systems Design"
type: lecture-note
week: 6
date: 2026-02-03
tags: [DSD, lecture]
---
# Lecture 01 - Digital Arithmetic

> [!info] Course Information
> **Course:** 62711 Design af digitale systemer
> **Date:** 2026-02-03
> **Lecturer:** jmgm, osch@dtu.dk
> **Book reference:** Logic & Computer Design Fundamentals, M.M. Mano & C.R. Kime, 5th ed., Pearson, 2016
> **Pages:** p. 135, 143, 144-153, 156-163, 173-

---

## Course Overview

> [!abstract] Course Goals
> - Analyse and implement a digital system
> - Knowledge of digital systems tools and technologies
> - Implement a soft microprocessor using VHDL on FPGA
> - Structured VHDL programming
> - Test and verification

> [!warning] Teaching Method
> - Focus on practical application using VHDL
> - **Project-based** -- 3 parts: **PWA**, **PWB**, **PWF**
> - Preparation slides, video, quiz, and multiple choice in PWA/PWB
> - Lectures (1-1.5 hours per session)
> - Lab work Fridays 9:30-13:00

> [!tip] Project Timeline
> | Lectures | Project Part | Focus |
> |----------|-------------|-------|
> | 1-4 | **PWA** | ALU (DataPath) |
> | 5-8 | **PWB** | MPU (Control Unit) |
> | 9-13 | **PWF** | Microprocessor (Final -- working in hardware!) |
>
> Groups of 4 students with 2x2 subgroups. One development board per 2 students.

![[attachments/lecture01/slide_07.png]]

---

## VHDL Design

> [!note] VHDL -- VHSIC Hardware Design Language
> VHDL stands for **Very High Speed Integrated Circuit Hardware Description Language**.
> When programming with HDL, the abstraction is that **hardware simulates hardware**.

> [!abstract] HDL Abstraction Levels
> The course (62711) focuses on the following levels that **support VHDL**:
>
> | Abstraction Level | VHDL? | Domain |
> |---|---|---|
> | Instruction Set Architecture (ISA) | VHDL | Digital design |
> | Microarchitecture | VHDL | Digital design |
> | **Register Transfer Level (RTL)** | **VHDL** | **Digital design** |
> | Logic Gates | VHDL | Analog/Digital electronics |
>
> Levels **not** covered by VHDL: Programs/Applications, Algorithms, Programming languages, OS/Virtual machines, Transistors, Physical/Materials.

> [!tip] Design Method
> 1. **Top-down / Bottom-up** approach
> 2. Basic functionality for designing n-bit logic devices (decoder 4x16, multiplexer 16x1 of n bits)
> 3. All discussed in the preparation material

---

## Iterative Combinational Circuits

> [!note] Key Concept
> - Arithmetic functions operate on **binary vectors**
> - They use the **same subfunction** in each bit position
> - Design a functional block for a single *cell* (subfunction) and **repeat** to obtain the overall function
> - An *iterative array* (array of interconnected cells) can be **1D** or **multi-dimensional**

> [!example] Why iterative design?
> For n = 32 bits:
> - Number of inputs = 64 (+ carries)
> - Truth table rows = enormous
> - Equations with a huge number of terms -- **design impractical!**
>
> Iterative arrays take advantage of **regularity** to make design feasible.

---

## Combinational Logic Building Blocks

### Enable Circuit

> [!note] Enable Circuit
> The standard enable circuit uses an **AND gate**:
>
> $$F = EN \cdot X$$
>
> | EN | X | F |
> |---|---|---|
> | 0 | any | **0** (disabled) |
> | 1 | X | **X** (enabled) |
>
> > [!warning] An OR gate with inverted EN does **not** work as a standard enable
> > $F = \overline{EN} + X$ -- when EN=1, F=1 regardless of X!

### Decoders

> [!note] n-to-2^n Decoder
> A decoder takes an n-bit input and activates exactly **one** of $2^n$ output lines (one-hot encoding).
>
> **1-to-2 decoder** (n=1):
>
> | A | D0 | D1 |
> |---|---|---|
> | 0 | 1 | 0 |
> | 1 | 0 | 1 |
>
> **2-to-4 decoder** (n=2):
>
> | A1 | A0 | D0 | D1 | D2 | D3 |
> |---|---|---|---|---|---|
> | 0 | 0 | 1 | 0 | 0 | 0 |
> | 0 | 1 | 0 | 1 | 0 | 0 |
> | 1 | 0 | 0 | 0 | 1 | 0 |
> | 1 | 1 | 0 | 0 | 0 | 1 |
>
> Equations: $D_0 = \bar{A_1}\bar{A_0}$, $D_1 = \bar{A_1}A_0$, $D_2 = A_1\bar{A_0}$, $D_3 = A_1 A_0$

> [!tip] Decoder Expansion (n-decoder)
> - **k even:** Use $2^k$ AND gates driven by two decoders of output size $2^{k/2}$
> - **k odd:** Use $2^k$ AND gates driven by a decoder of output size $2^{(k+1)/2}$ and a decoder of output size $2^{(k-1)/2}$, repeat until k=1

#### Decoder in VHDL

> [!example] Structural VHDL -- 2-to-4 Decoder with Enable
> ```vhdl
> library ieee, lcdf_vhdl;
> use ieee.std_logic_1164.all, lcdf_vhdl.func_prims.all;
> entity decoder_2_to_4_w_enable is
>     port (EN, A0, A1: in std_logic;
>           D0, D1, D2, D3: out std_logic);
> end decoder_2_to_4_w_enable;
>
> architecture structural_1 of decoder_2_to_4_w_enable is
>     component NOT1
>         port (in1: in std_logic; out1: out std_logic);
>     end component;
>     component AND2
>         port (in1, in2: in std_logic; out1: out std_logic);
>     end component;
>     signal A0_n, A1_n, N0, N1, N2, N3: std_logic;
> begin
>     g0: NOT1 port map (in1 => A0, out1 => A0_n);
>     g1: NOT1 port map (in1 => A1, out1 => A1_n);
>     g2: AND2 port map (in1 => A0_n, in2 => A1_n, out1 => N0);
>     g3: AND2 port map (in1 => A0,   in2 => A1_n, out1 => N1);
>     g4: AND2 port map (in1 => A0_n, in2 => A1,   out1 => N2);
>     g5: AND2 port map (in1 => A0,   in2 => A1,   out1 => N3);
>     g6: AND2 port map (in1 => EN,   in2 => N0,   out1 => D0);
>     g7: AND2 port map (in1 => EN,   in2 => N1,   out1 => D1);
>     g8: AND2 port map (in1 => EN,   in2 => N2,   out1 => D2);
>     g9: AND2 port map (in1 => EN,   in2 => N3,   out1 => D3);
> end structural_1;
> ```

> [!example] Dataflow VHDL -- 2-to-4 Decoder
> ```vhdl
> architecture dataflow_1 of decoder_2_to_4_w_enable is
>     signal A0_n, A1_n: std_logic;
> begin
>     A0_n <= not A0;
>     A1_n <= not A1;
>     D0 <= A0_n and A1_n and EN;
>     D1 <= A0   and A1_n and EN;
>     D2 <= A0_n and A1   and EN;
>     D3 <= A0   and A1   and EN;
> end dataflow_1;
> ```

> [!example] Behavioral VHDL -- 2-to-4 Decoder (Functional Table)
> ```vhdl
> entity decod_2to4 is
>     Port (i1 : in STD_LOGIC;
>           i2 : in STD_LOGIC;
>           o  : out STD_LOGIC_VECTOR(3 downto 0));
> end decod_2to4;
>
> architecture Behavioral of decod_2to4 is
> begin
>     o <= "0001" when (i1='0' and i2='0') else
>          "0010" when (i1='1' and i2='0') else
>          "0100" when (i1='0' and i2='1') else
>          "1000";
> end Behavioral;
> ```

### Multiplexers

> [!note] Multiplexer (MUX)
> A multiplexer selects **one of several data inputs** and routes it to a single output, controlled by select lines.
>
> **4-to-1 MUX Truth Table:**
>
> | S1 | S0 | Y |
> |---|---|---|
> | 0 | 0 | I0 |
> | 0 | 1 | I1 |
> | 1 | 0 | I2 |
> | 1 | 1 | I3 |
>
> Implementation: **Decoder** + **Enabling Circuits** (AND-OR structure)
>
> A 4-to-1 MUX with 4-bit width requires **4 times more logic** (4 parallel AND-OR blocks).

#### Multiplexer in VHDL

> [!example] Structural VHDL -- 4-to-1 Multiplexer
> ```vhdl
> library ieee, lcdf_vhdl;
> use ieee.std_logic_1164.all, lcdf_vhdl.func_prims.all;
> entity multiplexer_4_to_1_st is
>     port (S: in std_logic_vector(0 to 1);
>           I: in std_logic_vector(0 to 3);
>           Y: out std_logic);
> end multiplexer_4_to_1_st;
>
> architecture structural_2 of multiplexer_4_to_1_st is
>     -- Components: NOT1, AND2, OR4
>     signal S_n: std_logic_vector(0 to 1);
>     signal D, N: std_logic_vector(0 to 3);
> begin
>     g0: NOT1 port map (S(0), S_n(0));
>     g1: NOT1 port map (S(1), S_n(1));
>     -- Decoder
>     g2: AND2 port map (S_n(1), S_n(0), D(0));
>     g3: AND2 port map (S_n(1), S(0),   D(1));
>     g4: AND2 port map (S(1),   S_n(0), D(2));
>     g5: AND2 port map (S(1),   S(0),   D(3));
>     -- Enable
>     g6: AND2 port map (D(0), I(0), N(0));
>     g7: AND2 port map (D(1), I(1), N(1));
>     g8: AND2 port map (D(2), I(2), N(2));
>     g9: AND2 port map (D(3), I(3), N(3));
>     -- OR
>     g10: OR4 port map (N(0), N(1), N(2), N(3), Y);
> end structural_2;
> ```

> [!example] Conditional Dataflow VHDL -- 4-to-1 MUX (When-Else)
> ```vhdl
> library ieee;
> use ieee.std_logic_1164.all;
> entity multiplexer_4_to_1_we is
>     port (S : in std_logic_vector(1 downto 0);
>           I : in std_logic_vector(3 downto 0);
>           Y : out std_logic);
> end multiplexer_4_to_1_we;
>
> architecture function_table of multiplexer_4_to_1_we is
> begin
>     Y <= I(0) when S = "00" else
>          I(1) when S = "01" else
>          I(2) when S = "10" else
>          I(3) when S = "11" else
>          'X';
> end function_table;
> ```

---

## Binary Adders

### Half-Adder

> [!note] Half-Adder (HA)
> A **2-input, 1-bit** binary adder. Adds two bits to produce a **sum bit** (S) and a **carry bit** (C).
>
> | X | Y | C | S |
> |---|---|---|---|
> | 0 | 0 | 0 | 0 |
> | 0 | 1 | 0 | 1 |
> | 1 | 0 | 0 | 1 |
> | 1 | 1 | 1 | 0 |
>
> **Equations (most common -- XOR implementation):**
>
> $$S = X \oplus Y$$
> $$C = X \cdot Y$$

> [!abstract] All Half-Adder Implementations
>
> | Form | S | C |
> |---|---|---|
> | **(a) SOP** | $S = X\bar{Y} + \bar{X}Y$ | $C = XY$ |
> | **(b) POS** | $S = (X+Y)(\bar{X}+\bar{Y})$ | $C = XY$ |
> | **(c) AND-NOR** | $S = \overline{(C + \bar{X}\bar{Y})}$ | $C = XY$ |
> | **(d) POS with C** | $S = (X+Y)\cdot\bar{C}$ | $\bar{C} = \overline{(\bar{X}+\bar{Y})}$ |
> | **(e) XOR** | $S = X \oplus Y$ | $C = X \cdot Y$ |

### Full-Adder

![[attachments/lecture01/slide_15.png]]

> [!note] Full-Adder (FA)
> Similar to a half-adder but with a **carry-in bit** (Z/Cin) from lower stages. Computes a **sum** (S) and a **carry** (C).
>
> | X | Y | Z | C | S |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 0 | 0 |
> | 0 | 0 | 1 | 0 | 1 |
> | 0 | 1 | 0 | 0 | 1 |
> | 0 | 1 | 1 | 1 | 0 |
> | 1 | 0 | 0 | 0 | 1 |
> | 1 | 0 | 1 | 1 | 0 |
> | 1 | 1 | 0 | 1 | 0 |
> | 1 | 1 | 1 | 1 | 1 |
>
> **Equations (from K-Map):**
>
> $$S = X \oplus Y \oplus Z$$
> $$C = XY + (X \oplus Y) \cdot Z$$
>
> > [!tip] Generate and Propagate
> > - **Generate** ($G$): $G = X \cdot Y$ -- carry is *generated* when both inputs are 1
> > - **Propagate** ($P$): $P = X \oplus Y$ -- carry is *propagated* when the sum is 1
> > - **Carry out**: $C_{out} = G + P \cdot C_{in}$

> [!example] Full-Adder in VHDL (Dataflow)
> ```vhdl
> entity FullAdder is
> port(
>     A, B: in std_logic;
>     Cin:  in std_logic;
>     sum:  out std_logic;
>     Cout: out std_logic);
> end entity;
>
> Architecture dataflow of FullAdder is
> begin
>     sum  <= A xor B xor Cin;
>     Cout <= (A and B) or (Cin and (A xor B));
> end Architecture;
> ```

> [!example] Full-Adder using Half-Adders (Structural VHDL)
> ```vhdl
> entity full_add is
>     Port (x, y, ci : in STD_LOGIC;
>           so : out STD_LOGIC;
>           co : out STD_LOGIC);
> end full_add;
>
> architecture Behavioral of full_add is
>     component half_add is
>         Port (x, y : in STD_LOGIC;
>               c, s : out STD_LOGIC);
>     end component;
>     signal co1, co2, s1, z: std_logic;
> begin
>     u1: half_add port map(x=>x, y=>y, s=>s1, c=>co1);
>     u2: half_add port map(x=>s1, y=>ci, s=>so, c=>co2);
>     co <= co1 or co2;
> end Behavioral;
> ```

### 4-bit Ripple-Carry Adder

![[attachments/lecture01/slide_17.png]]

> [!note] Ripple-Carry Adder (RCA)
> Chains multiple full adders together. The **carry out** of cell $i$ becomes the **carry in** of cell $i+1$.
>
> **4-bit example:** Adds A(3:0) and B(3:0) to produce S(3:0) with carry C4.
>
> | Description | Subscript 3 2 1 0 | Name |
> |---|---|---|
> | Carry In | 0 1 1 0 | $C_i$ |
> | Augend | 1 0 1 1 | $A_i$ |
> | Addend | 0 0 1 1 | $B_i$ |
> | **Sum** | **1 1 1 0** | $S_i$ |
> | Carry out | 0 0 1 1 | $C_{i+1}$ |
>
> > [!warning] Propagation Delay
> > The main problem with ripple carry adders is the **long propagation delay** -- the carry must ripple from the LSB to the MSB. The "long path" is from $A_0$ or $B_0$ through the circuit to $S_3$.

---

## Binary Subtraction

### Unsigned Subtraction

> [!note] Unsigned Subtraction Algorithm
> Subtract the subtrahend $N$ from the minuend $M$:
>
> 1. If **no end borrow** occurs: $M \geq N$, result is non-negative and correct
> 2. If **end borrow** occurs: $N > M$, compute $(M - N + 2^n)$, then subtract $2^n$ (borrow at MSB) and append a minus sign
>
> > [!example] Examples
> > **Case 1:** $M \geq N$
> > ```
> >   M:  1001
> > - N:  0111
> > ──────────
> >       0010   (result is positive: +2)
> > ```
> >
> > **Case 2:** $N > M$ (borrow occurs)
> > ```
> >   M:  0100
> > - N:  0111
> > ──────────
> >       1101   (intermediate)
> >  10000       (add 2^n)
> > - 1101
> > ──────────
> > (-) 0011     (result is -3)
> > ```

### Using Complements for Subtraction

![[attachments/lecture01/slide_19.png]]

> [!important] 2's Complement Approach
> Subtraction $A - B$ can be done by **addition of the 2's complement**:
>
> 1. **Complement each bit** of B (1's complement)
> 2. **Add 1** to the result (now you have 2's complement of B)
> 3. **Add** A + (2's complement of B)
>
> This allows shared, simpler logic for **both addition and subtraction**!

### 2's Complement Adder/Subtractor Circuit

![[attachments/lecture01/slide_21.png]]

> [!note] Combined Adder/Subtractor
> A single circuit computes both $A + B$ and $A - B$ using a control signal $S$:
>
> - **S = 0** (Add): B passes through unchanged, $C_0 = 0$
> - **S = 1** (Subtract): B is inverted via **XOR gates** (1's complement), and $C_0 = 1$ (adds the +1 for 2's complement)
>
> Each bit of B is XORed with S before entering the full adder chain.

---

## Signed Number Representations

> [!abstract] Comparison of 4-bit Signed Representations
>
> | Decimal | Unsigned | Signed-Magnitude | 1's Complement | 2's Complement | Biased (offset 7) |
> |---|---|---|---|---|---|
> | +7 | 0111 | 0111 | 0111 | 0111 | 1110 |
> | +6 | 0110 | 0110 | 0110 | 0110 | 1101 |
> | +5 | 0101 | 0101 | 0101 | 0101 | 1100 |
> | +4 | 0100 | 0100 | 0100 | 0100 | 1011 |
> | +3 | 0011 | 0011 | 0011 | 0011 | 1010 |
> | +2 | 0010 | 0010 | 0010 | 0010 | 1001 |
> | +1 | 0001 | 0001 | 0001 | 0001 | 1000 |
> | +0 | 0000 | 0000 | 0000 | 0000 | 0111 |
> | -0 | -- | 1000 | 1111 | -- | -- |
> | -1 | -- | 1001 | 1110 | 1111 | 0110 |
> | -2 | -- | 1010 | 1101 | 1110 | 0101 |
> | -3 | -- | 1011 | 1100 | 1101 | 0100 |
> | -4 | -- | 1100 | 1011 | 1100 | 0011 |
> | -5 | -- | 1101 | 1010 | 1011 | 0010 |
> | -6 | -- | 1110 | 1001 | 1010 | 0001 |
> | -7 | -- | 1111 | 1000 | 1001 | 0000 |
> | -8 | -- | -- | -- | 1000 | -- |
>
> For n bits, the bias offset is $(2^{n-1}) - 1$.

### Signed-Complement Arithmetic

> [!note] Signed 2's Complement Addition
> 1. Add the numbers **including the sign bits**, discarding any carry out of the MSB
> 2. If the sign bits were the **same** for both operands and the sign of the result is **different**, an **overflow** has occurred
> 3. The sign of the result is computed in step 1

> [!note] Signed 2's Complement Subtraction
> Take the **complement** of the number you are subtracting, then follow the rules for addition.

---

## Introduction to PWA -- ALU Design

![[attachments/lecture01/slide_25.png]]

> [!important] Arithmetic Circuit Block Diagram (Function Unit)
> The arithmetic circuit is part of the **Function Unit (FU)** in the ALU:
>
> - **Inputs:** A (n-bit), B (n-bit), $C_{in}$, Select signals ($S_0$, $S_1$)
> - **B Input Logic:** A multiplexer that selects how B is processed (pass through, invert, zero, etc.)
> - **n-bit Parallel Adder:** Computes $G = X + Y + C_{in}$
> - **Output:** G (n-bit), $C_{out}$

---

## Structural Registers and D Flip-Flops

### D Flip-Flop with Asynchronous Reset and Enable

![[attachments/lecture01/slide_27.png]]

> [!note] D-FF Reset Types
> - **Asynchronous reset:** Output goes to 0 **immediately** when reset is asserted, regardless of clock
> - **Synchronous reset:** Output goes to 0 only on the **next clock edge** after reset is asserted

![[attachments/lecture01/slide_28.png]]

> [!example] D Flip-Flop with Async Reset and Enable (VHDL)
> ```vhdl
> entity d_ff_en_reset is
>     Port (D, Reset, load, clk : in STD_LOGIC;
>           Q : inout STD_LOGIC);
> end d_ff_en_reset;
>
> architecture Behavioral of d_ff_en_reset is
> begin
>     process(clk, reset, load) is
>     begin
>         if reset = '1' then
>             q <= '0';                  -- Asynchronous reset
>         elsif rising_edge(clk) then
>             if load = '1' then
>                 q <= d;                -- Load on clock edge
>             end if;
>         end if;
>     end process;
> end Behavioral;
> ```

### Generic Entities and N-bit Registers

> [!note] VHDL Generics
> Generics allow parameterized designs -- reusable components with configurable width.
>
> ```vhdl
> entity EntityName is
>     generic (n : integer := 16; m : integer := 32);
>     port( ... );
> end entity;
> ```
>
> **Instantiation with generic map:**
> ```vhdl
> label : entityname generic map(16) port map(portlist);
> -- Omit generic map if the component is not generic
> ```

> [!example] N-bit Register from 1-bit Flip-Flops
> ```vhdl
> entity nreg is
>     generic (n : integer := 16);
>     port(
>         clk, reset, enable : in std_logic;
>         input  : in  std_logic_vector(n-1 downto 0);
>         output : out std_logic_vector(n-1 downto 0));
> end entity;
>
> architecture my_arch of nreg is
>     component reg is
>         port(clk, reset, input, enable: in std_logic;
>              output : out std_logic);
>     end component;
> begin
>     loop1 : for i in 0 to n-1 generate
>         fx: reg port map (clk, reset, input(i), enable, output(i));
>     end generate;
> end architecture;
> ```

![[attachments/lecture01/slide_33.png]]

> [!example] 16x8-bit Register File (for generate)
> The register file uses nested `for...generate` to create 16 registers of 8 bits each:
> ```vhdl
> entity RegisterR16 is
>     generic (width : integer := 8);
>     Port (Reset : in STD_LOGIC;
>           clk   : in STD_LOGIC;
>           Load  : in STD_LOGIC_vector(15 downto 0);
>           D_data: in STD_LOGIC_vector(width-1 downto 0);
>           R0, R1, ..., R15 : inout std_logic_vector(width-1 downto 0));
> end RegisterR16;
>
> architecture Behavioral of RegisterR16 is
>     Component D_FF_en_reset is
>         Port (D, Reset, load, clk : in STD_LOGIC;
>               Q : inout STD_LOGIC);
>     end component;
> begin
>     RegisterR0 : for i in 0 to (width-1) generate
>         UR0: component d_ff_en_reset
>             port map (D_data(i), Reset, load(0), clk, R0(i));
>     end generate RegisterR0;
>     -- Repeat for R1 through R15...
> end Behavioral;
> ```

---

## Top-Level Entity: Microprocessor (PWF)

> [!abstract] uP Entity Declaration
> ```vhdl
> Entity uP is
> port (
>     CLK:          in  std_logic;              -- Clock input
>     RESET:        in  std_logic;              -- Initializes processor
>     HOLD:         in  std_logic;              -- Suspends processor
>     Data_In:      in  std_logic_vector(..);   -- Data bus (Input)
>     Data_Out:     in  std_logic_vector(..);   -- Data bus (Output)
>     Address:      out std_logic_vector(..);   -- Address bus
>     Memory_MUX:   out std_logic;              -- Selects Program/Data Memory
>     Memory_Write: out std_logic;              -- Memory Map Write
>     Memory_Read:  out std_logic               -- Access RAM/Ports
> );
> end uP;
>
> Architecture uP_Structural of uP is
> ...
> begin
> ...
> end;
> ```

---

## Gate Mapping

> [!note] Mapping to NAND/NOR Gates
> Any combinational circuit can be implemented using only **NAND** or only **NOR** gates:
>
> - **AND** $\rightarrow$ NAND + inverter (NAND followed by NOT)
> - **OR** $\rightarrow$ Inverted inputs into NAND gate
> - **Pushing inverters** through a "dot" (De Morgan's)
> - **Cancelling inverter pairs** simplifies the circuit

---

> [!todo] Preparation for Lecture 2
> **Date:** 14-02-2025
> - Digital Arithmetic, Combinatorial and register logic design -- Video 3
> - Simulation video 3
> - Book sections: 4.2, 4.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.8
> - Continue PWA
> - **Opgave 2 due: 12 February**

---

> [!summary] Key Takeaways
> 1. **Iterative design** makes n-bit arithmetic circuits feasible by repeating a single cell design
> 2. **Half-adder** = 2 inputs (no carry in), **Full-adder** = 3 inputs (with carry in)
> 3. **Ripple carry adders** are simple but slow due to carry propagation delay
> 4. **2's complement** allows a single adder circuit to perform both addition and subtraction
> 5. **VHDL** supports multiple description styles: structural (gate-level), dataflow, and behavioral
> 6. **Generics** and **for...generate** enable scalable, parameterized designs
> 7. The course project builds a complete microprocessor: ALU (PWA) $\rightarrow$ Control Unit (PWB) $\rightarrow$ Full uP (PWF)

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]]
>
> [[Lecture 02 - Arithmetic Circuits & ALU|Lecture 02 →]]
