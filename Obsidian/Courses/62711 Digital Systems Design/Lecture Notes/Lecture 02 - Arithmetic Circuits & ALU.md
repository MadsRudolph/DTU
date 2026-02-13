# Lecture 02 - Arithmetic Circuits & ALU

> [!info] Course Information
> **Course:** 62711 Design af digitale systemer
> **Date:** 2026-02-11
> **Lecturer:** jmgm, osch@dtu.dk
> **Book reference:** Logic & Computer Design Fundamentals, M.M. Mano & C.R. Kime, 5th ed., Pearson, 2016
> **Pages:** 3.1–3.5, 3.7, 3.8, 4.2, 4.3, 8.1–8.6

---

## 2's Complement Representation

> [!note] Forming the 2's Complement
> The **2's complement** of a binary number is equal to the **1's complement (NOT) plus 1**:
>
> $$\text{2's comp}(N) = \overline{N} + 1$$
>
> **Example:** Find the 2's complement of $01110011_2$ ($115_{10}$):
>
> ```
>  01110011   (original, +115)
>  ↓ bit-wise NOT
>  10001100   (1's complement)
> +        1
> ──────────
>  10001101   (2's complement, represents -115)
> ```
>
> The MSB is interpreted as a **sign bit**: $s = 0$ positive, $s = 1$ negative.

---

## Subtraction with 2's Complement

> [!important] Algorithm
> For n-digit unsigned numbers $M$ and $N$, compute $M - N$ in base 2:
>
> 1. Form the 2's complement of the subtrahend $N$
> 2. Add: $M + (2^n - N) = M - N + 2^n$
> 3. **If $M \geq N$:** The sum produces an **end carry** $r_n$ which is discarded — the result $M - N$ remains
> 4. **If $M < N$:** No end carry — the result is $2^n - (N - M)$, i.e. the 2's complement of $(N - M)$. Take its 2's complement and place a minus sign

> [!example] Examples
> **(1)** $01010100_2 - 01000011_2$ ($84 - 67$):
>
> ```
>   01010100
> + 10111101   (2's complement of 01000011)
> ──────────
> 1 00010001   ← carry of 1: no correction needed
>   Result = 00010001 = +17
> ```
>
> **(2)** $01000011_2 - 01010100_2$ ($67 - 84$):
>
> ```
>   01000011
> + 10101100   (2's complement of 01010100)
> ──────────
> 0 11101111   ← carry of 0: correction required
>   2's comp of result = 00010001 = 17
>   Result = -17
> ```

---

## Full-Adder: Generate and Propagate

> [!note] Full-Adder with G and P
> The full adder can be decomposed into **two half-adders** plus an OR gate:
>
> $$S_i = A_i \oplus B_i \oplus C_i$$
> $$C_{i+1} = G_i + P_i \cdot C_i$$
>
> Where:
> - **Generate:** $G_i = A_i \cdot B_i$ — carry is *generated* when both inputs are 1
> - **Propagate:** $P_i = A_i \oplus B_i$ — carry is *propagated* through when exactly one input is 1
>
> This decomposition is the basis for **carry lookahead** optimization.

---

## 2's Complement Adder/Subtractor

![[attachments/lecture02/slide_06.png]]

> [!note] Combined Adder/Subtractor Circuit
> A single circuit computes both $A + B$ and $A - B$ using a control signal $S$:
>
> - **S = 0** (Add): B passes through unchanged, $C_0 = 0$
> - **S = 1** (Subtract): Each bit of B is inverted via **XOR gates** (1's complement), and $C_0 = 1$ (adds +1 to form 2's complement)
>
> $$B_i \oplus S = \begin{cases} B_i & \text{if } S = 0 \\ \overline{B_i} & \text{if } S = 1 \end{cases}$$
>
> The XOR gates + carry-in together form the 2's complement of B when $S = 1$.

---

## Overflow Detection

> [!warning] When Does Overflow Occur?
> Overflow occurs if $n + 1$ bits are required to contain the result from an n-bit operation.
>
> **Unsigned numbers:**
> - Addition: overflow detected from the **carry out** of the MSB
> - Subtraction: overflow is impossible (result ≤ larger operand)
>
> **2's complement (signed) numbers:**
> - An end carry of 1 does **NOT** necessarily indicate overflow
> - Overflow can occur when:
>   - **Adding** two operands with the **same sign**
>   - **Subtracting** operands with **different signs**

> [!important] Hardware Overflow Detection
> $$V = C_n \oplus C_{n-1}$$
>
> Overflow is detected when the **carry into** the sign bit position differs from the **carry out** of the sign bit position.
>
> | $C_n$ (out of MSB) | $C_{n-1}$ (into MSB) | V |
> |---|---|---|
> | 0 | 0 | 0 (no overflow) |
> | 0 | 1 | **1 (overflow)** |
> | 1 | 0 | **1 (overflow)** |
> | 1 | 1 | 0 (no overflow) |

> [!example] Overflow Examples (8-bit)
>
> **Positive + Positive → Negative (OVERFLOW):**
> ```
>  Carries: 01
>    0100 0110   (+70)
>  + 0101 0000   (+80)
>  ───────────
>    1001 0110   (-106, WRONG!)
>  Cₙ=0, Cₙ₋₁=1 → V=1
> ```
>
> **Negative + Negative → Positive (OVERFLOW):**
> ```
>  Carries: 10
>    1011 1010   (-70)
>  + 1011 0000   (-80)
>  ───────────
>    0110 1010   (+106, WRONG!)
>  Cₙ=1, Cₙ₋₁=0 → V=1
> ```

### Overflow Detection Logic (Figure 3-46)

![[attachments/lecture02/slide_08.png]]

---

## Arithmetic Circuit (Function Unit)

![[attachments/lecture02/slide_09.png]]

> [!note] Arithmetic Circuit Block Diagram
> The arithmetic circuit is part of the **Function Unit (FU)** in the ALU:
>
> - **Inputs:** A (n-bit), B (n-bit), $C_{in}$, Select signals ($S_0$, $S_1$)
> - **B Input Logic:** Selects how B is processed before the adder
> - **n-bit Parallel Adder:** Computes $G = X + Y + C_{in}$
> - **Output:** G (n-bit), $C_{out}$

### B Input Logic (Figure 8-4)

![[attachments/lecture02/slide_11.png]]

> [!note] B Input Logic (One Stage)
> The select signals $S_1$ and $S_0$ control what value $Y_i$ is fed to the adder alongside $A_i$:
>
> | $S_1$ | $S_0$ | $Y_i$ | Description |
> |---|---|---|---|
> | 0 | 0 | $0$ | All zeros |
> | 0 | 1 | $B_i$ | B pass-through |
> | 1 | 0 | $\overline{B_i}$ | B complement |
> | 1 | 1 | $1$ | All ones |
>
> Karnaugh map reduction gives: $Y_i = S_0 \cdot B_i \oplus S_1$

### Function Table (Table 8.1)

![[attachments/lecture02/slide_10.png]]

> [!abstract] Arithmetic Circuit Operations
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

### 4-Bit Arithmetic Circuit (Figure 8-5)

![[attachments/lecture02/slide_12.png]]

---

## ALU Function Table (Table 8.2)

![[attachments/lecture02/slide_13.png]]

> [!abstract] Complete ALU Operations
> The full ALU adds a **logic unit** alongside the arithmetic circuit, selected by $S_2$:
>
> | $S_2$ | $S_1$ | $S_0$ | $C_{in}$ | Operation |
> |---|---|---|---|---|
> | 0 | 0 | 0 | 0 | **Transfer A** |
> | 0 | 0 | 0 | 1 | **Increment A** |
> | 0 | 0 | 1 | 0 | **A + B** |
> | 0 | 0 | 1 | 1 | **A + B + 1** |
> | 0 | 1 | 0 | 0 | **A + B̄** |
> | 0 | 1 | 0 | 1 | **A − B** (subtract) |
> | 0 | 1 | 1 | 0 | **A − 1** (decrement) |
> | 0 | 1 | 1 | 1 | **Transfer A** |
> | 1 | 0 | 0 | X | **A AND B** |
> | 1 | 0 | 1 | X | **A OR B** |
> | 1 | 1 | 0 | X | **A XOR B** |
> | 1 | 1 | 1 | X | **NOT A** |
>
> > [!warning] Bemærk: I PWA er rækkefølgen byttet om i forhold til Table 8.2!

---

## Logic Circuit (One Stage)

![[attachments/lecture02/slide_14.png]]

> [!note] Logic Unit Stage (Figure 8-6)
> Each bit of the logic unit uses a **4-to-1 MUX** controlled by $S_0$ and $S_1$ to select between:
>
> | $S_1$ | $S_0$ | Output |
> |---|---|---|
> | 0 | 0 | $A_i \text{ AND } B_i$ |
> | 0 | 1 | $A_i \text{ OR } B_i$ |
> | 1 | 0 | $A_i \text{ XOR } B_i$ |
> | 1 | 1 | $\text{NOT } A_i$ |
>
> The final ALU output MUX uses $S_2$ to select between the **arithmetic result** and the **logic result**.
>
> > [!warning] Omvendt i PWA

---

## Iterative Combinational Circuits

> [!note] Key Concept
> - Arithmetic functions operate on **binary vectors** using the **same subfunction** in each bit position
> - Design a single **cell** and **repeat** it to build the overall function
> - For $n = 32$: a direct truth table approach is impractical ($2^{64+}$ rows!)
> - Iterative arrays exploit **regularity** to make design feasible

---

## VHDL: Generate Statement for Adders

> [!example] 8-bit Full-Adder using `for...generate`
> The `generate` statement creates a structural array of full adders:
>
> ```vhdl
> entity adder_8bit is
>     port (
>         A, B : in  std_logic_vector(7 downto 0);
>         Cin  : in  std_logic;
>         S    : out std_logic_vector(7 downto 0);
>         Cout : out std_logic);
> end adder_8bit;
>
> architecture structural of adder_8bit is
>     component full_add is
>         port (x, y, ci : in std_logic;
>               so, co   : out std_logic);
>     end component;
>     signal c : std_logic_vector(8 downto 0);
> begin
>     c(0) <= Cin;
>     gen: for i in 0 to 7 generate
>         fa: full_add port map (A(i), B(i), c(i), S(i), c(i+1));
>     end generate;
>     Cout <= c(8);
> end structural;
> ```
>
> > [!tip] The `for...generate` statement is evaluated at **synthesis time** — it unrolls into 8 parallel full adder instances connected by the carry chain.

---

## Combinational Building Blocks (Recap)

### Enable Circuit

> [!note] Enable Circuit
> Uses an **AND gate**: $F = EN \cdot X$
>
> | EN | X | F |
> |---|---|---|
> | 0 | any | **0** (disabled) |
> | 1 | X | **X** (enabled) |

### 2-to-4 Decoder with Enable (Figure 3-16)

![[attachments/lecture02/slide_18.png]]

> [!note] Decoder with Enable
> The enable input acts as a **master switch** — when $EN = 0$, all outputs are 0.
>
> This allows **decoder expansion**: a 4-to-16 decoder can be built from **five** 2-to-4 decoders with enable (one as the top-level selector, four as output stages).

### Decoder Expansion: 4-to-16

![[attachments/lecture02/slide_19.png]]

> [!note] Building a 4-to-16 Decoder
> Two approaches:
>
> **Method 1 — Cascaded decoders with enable:**
> - Use the upper 2 address bits ($A_3, A_2$) in a 2-to-4 decoder to generate 4 enable signals
> - Each enable drives a 2-to-4 sub-decoder using the lower bits ($A_1, A_0$)
> - Result: 16 one-hot outputs
>
> **Method 2 — Two decoders ANDed together:**
> - One 2-to-4 decoder for $A_3, A_2$ → 4 outputs
> - One 2-to-4 decoder for $A_1, A_0$ → 4 outputs
> - $4 \times 4 = 16$ AND gates produce the 16 one-hot outputs

### Multiplexer Expansion

![[attachments/lecture02/slide_20.png]]

> [!note] Building Larger Multiplexers
>
> | MUX Size | Built From |
> |---|---|
> | 4-to-1 | 2-to-4 decoder + 4 AND gates + OR gate |
> | 8-to-1 | 3-to-8 decoder + 8 AND gates + OR gate |
> | 16-to-1 | 4-to-16 decoder + 16 AND gates + OR gate |
>
> For **n-bit wide** data: the AND and OR gates must be **n bits wide** (parallel planes).
>
> A 16×n×1 MUX = 4-to-16 decoder + 16 n-bit AND gates + n-bit OR gate.

---

## Structural Registers

### D Flip-Flop with Asynchronous Reset and Enable

![[attachments/lecture02/slide_23.png]]

> [!example] D-FF Component (VHDL)
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
>
> This is the **component** used in the iterative register file.

### N-bit Register using Generate

> [!example] 8-bit Register from 1-bit Flip-Flops
> ```vhdl
> gen_reg: for i in 0 to (width-1) generate
>     ff: d_ff_en_reset
>         port map (D_data(i), Reset, load, clk, Q(i));
> end generate;
> ```
>
> With `width = 8`, this creates 8 parallel D flip-flops sharing the same clock, reset, and load signals.

---

> [!todo] Preparation for Lecture 3
> **Date:** 18-02-2026
> - Book sections: 3.9, 3.10, 3.11, 3.12, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8
> - Registers and Register Transfer — Video
> - Continue PWA

---

> [!summary] Key Takeaways
> 1. **2's complement subtraction** reuses the adder: invert B with XOR gates and set $C_0 = 1$
> 2. **Overflow** in signed arithmetic is detected by $V = C_n \oplus C_{n-1}$ — carry out ≠ overflow!
> 3. The **Arithmetic Circuit** uses B input logic ($S_0$, $S_1$) and $C_{in}$ to select 8 operations from a single adder
> 4. The **ALU** adds a logic unit ($S_2 = 1$) for AND, OR, XOR, NOT alongside arithmetic operations
> 5. **Decoder expansion**: build large decoders (4-to-16) by cascading smaller decoders with enable
> 6. **MUX = Decoder + AND-OR** network; scale by using wider gates for n-bit data
> 7. **`for...generate`** in VHDL creates iterative hardware structures at synthesis time
