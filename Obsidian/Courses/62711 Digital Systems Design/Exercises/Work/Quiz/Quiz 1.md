# Quiz - VHDL Digital Design

## Question 1 (1 point)

> [!question] Hvilket af disse VHDL beskrivelser er for et multiplexer kredsløb
> 
> - [ ] `o<="0001" when i2='0' and i1='0' else "0010" when i2='0' and i1='1' else "0100" when i2='1' and i1='0' else "1000";`
> - [x] **`O<=i0 when sel="00" else i1 when sel="01" else i2 when sel="10" else i3;`**
> - [ ] `g<=not ((b and c) and (not(a and b and c)) and (not(not b and c)));`

> [!success] Answer: `O<=i0 when sel="00" else i1 when sel="01" else i2 when sel="10" else i3;`

> [!note]- Explanation This is a **4-to-1 multiplexer**. It selects one of four data inputs (`i0`, `i1`, `i2`, `i3`) based on the 2-bit `sel` signal and routes it to output `O`.
> 
> |sel|Output|
> |---|---|
> |00|i0|
> |01|i1|
> |10|i2|
> |11|i3|
> 
> > [!info] Why the others are wrong
> > 
> > - **Option 1** is a **2-to-4 decoder** — takes 2-bit input, produces one-hot 4-bit output
> > - **Option 3** is a **combinational logic circuit** — just implements a Boolean function with AND/NOT gates

---

## Question 2 (1 point)

> [!question] Hvilken af disse VHDL beskrivelser beskriver 2 til 4 line-decoderens funktion
> 
> - [x] **`o<="0001" when i2='0' and i1='0' else "0010" when i2='0' and i1='1' else "0100" when i2='1' and i1='0' else "1000";`**
> - [ ] 4-to-1 MUX entity with architecture
> - [ ] Boolean logic expression
> - [ ] Another MUX description

> [!success] Answer: `o<="0001" when i2='0' and i1='0' else ...`

> [!note]- Explanation This is a **2-to-4 line decoder**. It takes two single-bit inputs (`i1`, `i2`) and produces a 4-bit one-hot output.
> 
> |i2|i1|Output|
> |---|---|---|
> |0|0|0001|
> |0|1|0010|
> |1|0|0100|
> |1|1|1000|
> 
> Exactly one output bit is high for each input combination — this is the defining characteristic of a decoder (one-hot encoding).

---

## Question 3 (1 point)

> [!question] Hvilken funktion udfører dette kredsløb beskrevet med sandhedstabel og gates
> 
> Truth table: A₁A₀ → D₀D₁D₂D₃ with one-hot outputs
> 
> Gate equations: D₀ = Ā₁·Ā₀, D₁ = Ā₁·A₀, D₂ = A₁·Ā₀, D₃ = A₁·A₀
> 
> - [ ] register
> - [ ] adder
> - [ ] multiplexer
> - [x] **2 til 4 line decoder**

> [!success] Answer: 2 til 4 line decoder

> [!note]- Explanation The truth table and gate equations confirm this is a **2-to-4 decoder**:
> 
> |A₁|A₀|Active Output|
> |---|---|---|
> |0|0|D₀ = 1|
> |0|1|D₁ = 1|
> |1|0|D₂ = 1|
> |1|1|D₃ = 1|
> 
> Each output is the AND of the appropriate combination of inputs (inverted or not):
> 
> - $D_0 = \bar{A_1} \cdot \bar{A_0}$
> - $D_1 = \bar{A_1} \cdot A_0$
> - $D_2 = A_1 \cdot \bar{A_0}$
> - $D_3 = A_1 \cdot A_0$
> 
> This is the standard decoder implementation using AND gates with inverters.

---

## Question 4 (1 point)

> [!question] Hvilken af disse a) eller b) er et enable kredsløb
> 
> Circuit (a): AND gate with inputs X and EN → F
> 
> Circuit (b): OR gate with inputs X and inverted EN → F
> 
> - [x] **a**
> - [ ] b

> [!success] Answer: a

> [!note]- Explanation **Circuit (a)** is the standard enable circuit using an AND gate:
> 
> $$F = X \cdot EN$$
> 
> |EN|X|F|
> |---|---|---|
> |0|X|0 (disabled)|
> |1|X|X (enabled)|
> 
> - When EN = 0: Output is forced to 0 (disabled)
>     
> - When EN = 1: Output follows input X (enabled)
>     
> 
> > [!info] Why (b) is not the standard enable Circuit (b): $F = X + \bar{EN}$
> > 
> > - When EN = 0: F = 1 (forced high)
> > - When EN = 1: F = X
> > 
> > While this also gates the signal, the **standard enable circuit** uses an AND gate where disabling forces the output **low**, not high.

---

## Question 5 (1 point)

> [!question] Hvilken funktion udfører dette kredsløb
> 
> Circuit with inputs Aᵢ, Bᵢ, Cᵢ and outputs Sᵢ, Cᵢ₊₁
> 
> - [ ] multiplier
> - [ ] half adder
> - [x] **full adder**
> - [ ] propagator

> [!success] Answer: full adder

> [!note]- Explanation The circuit has **three inputs** (Aᵢ, Bᵢ, Cᵢ) and **two outputs** (Sᵢ, Cᵢ₊₁):
> 
> > [!abstract] Signal Analysis
> > 
> > - **Gᵢ** = Aᵢ · Bᵢ (AND gate) — _Generate_ signal
> > - **Pᵢ** = Aᵢ ⊕ Bᵢ (XOR gate) — _Propagate_ signal
> > - **Sᵢ** = Pᵢ ⊕ Cᵢ = Aᵢ ⊕ Bᵢ ⊕ Cᵢ — _Sum_ output
> > - **Cᵢ₊₁** = Gᵢ + (Pᵢ · Cᵢ) — _Carry out_
> 
> These are the standard **full adder equations**. The presence of a carry input (Cᵢ) distinguishes it from a half adder, which only adds two bits without carry in.
> 
> |Aᵢ|Bᵢ|Cᵢ|Sᵢ|Cᵢ₊₁|
> |---|---|---|---|---|
> |0|0|0|0|0|
> |0|0|1|1|0|
> |0|1|0|1|0|
> |0|1|1|0|1|
> |1|0|0|1|0|
> |1|0|1|0|1|
> |1|1|0|0|1|
> |1|1|1|1|1|

---

## Question 6 (1 point)

> [!question] Hvilken funktion udfører dette gate kredsløb
> 
> Circuit: 2-to-4 Decoder feeding into 4×2 AND-OR structure with data inputs I₀-I₃
> 
> - [x] **multiplexer 4 til 1 bit med 2 select signaler**
> - [ ] 2 til 4 line decoder
> - [ ] 4 bit full adder
> - [ ] 4 til 2 encoder

> [!success] Answer: multiplexer 4 til 1 bit med 2 select signaler

> [!note]- Explanation This is a **4-to-1 multiplexer** built using a decoder and AND-OR logic:
> 
> > [!abstract] How it works
> > 
> > 1. **Decoder stage**: S₁ and S₀ select one of four decoder outputs (one-hot)
> > 2. **AND gates**: Each decoder output is ANDed with a data input (I₀, I₁, I₂, I₃). Only the selected line passes its data — the rest are masked to 0.
> > 3. **OR gate**: Combines all four AND outputs into final output Y.
> 
> |S₁|S₀|Y|
> |---|---|---|
> |0|0|I₀|
> |0|1|I₁|
> |1|0|I₂|
> |1|1|I₃|
> 
> This is the classic **decoder + AND-OR implementation** of a multiplexer.

---

## Question 7 (1 point)

> [!question] Hvad er den binære sum af disse to binære tal
> 
> A = 01010101, B = 00000111
> 
> - [ ] 01011101
> - [ ] 01011000
> - [x] **01011100**

> [!success] Answer: 01011100

> [!note]- Explanation Binary addition with carry propagation:
> 
> ```
>   01010101  (A = 85₁₀)
> + 00000111  (B = 7₁₀)
> ──────────
>   01011100  (92₁₀)
> ```
> 
> > [!abstract] Step-by-step (right to left)
> > 
> > |Position|A|B|Cᵢₙ|Sum|Cₒᵤₜ|
> > |---|---|---|---|---|---|
> > |0|1|1|0|0|1|
> > |1|0|1|1|0|1|
> > |2|1|1|1|1|1|
> > |3|0|0|1|1|0|
> > |4|1|0|0|1|0|
> > |5|0|0|0|0|0|
> > |6|1|0|0|1|0|
> > |7|0|0|0|0|0|

---

## Question 8 (1 point)

> [!question] Givet dette positive binære tal 01010101 på 2's complement form, omdan det til det negative tal på 2's complement form
> 
> - [x] **10101011**
> - [ ] 11101011
> - [ ] 10101010
> - [ ] 11010101

> [!success] Answer: 10101011

> [!note]- Explanation To convert to 2's complement (negate the number):
> 
> > [!abstract] Step 1: Invert all bits
> > 
> > ```
> > 01010101 → 10101010
> > ```
> 
> > [!abstract] Step 2: Add 1
> > 
> > ```
> >   10101010
> > +        1
> > ──────────
> >   10101011
> > ```
> 
> > [!tip] Verification
> > 
> > - Original: 01010101 = +85₁₀
> > - Result: 10101011 = -85₁₀ in 8-bit 2's complement
> > 
> > Check: 01010101 + 10101011 = 100000000 (overflow discarded = 0) ✓

---

## Question 9 (1 point)

> [!question] Hvad gør dette kredsløb
> 
> Circuit: Two inputs feeding both an XOR gate and an AND gate in parallel
> 
> - [ ] en full adder
> - [ ] en decoder
> - [x] **en half adder**

> [!success] Answer: en half adder

> [!note]- Explanation The circuit has two inputs feeding both gates in parallel:
> 
> - **XOR gate** → Sum output: $S = A \oplus B$
> - **AND gate** → Carry output: $C = A \cdot B$
> 
> |A|B|Sum (A⊕B)|Carry (A·B)|
> |---|---|---|---|
> |0|0|0|0|
> |0|1|1|0|
> |1|0|1|0|
> |1|1|0|1|
> 
> > [!info] Half Adder vs Full Adder
> > 
> > - **Half adder**: 2 inputs (A, B), 2 outputs (Sum, Carry) — no carry input
> > - **Full adder**: 3 inputs (A, B, Cᵢₙ), 2 outputs (Sum, Cₒᵤₜ) — includes carry input
> 
> A half adder can only add the least significant bit of a multi-bit addition. Full adders are needed for subsequent bits to handle carry propagation.

---

## Summary

> [!tldr] Quick Answers
> 
> |Q|Topic|Answer|Key Concept|
> |---|---|---|---|
> |1|VHDL MUX|`when sel="00" else...`|Select 1 of N inputs|
> |2|VHDL Decoder|One-hot output pattern|2-bit in → 4-bit one-hot out|
> |3|Gate decoder|2-to-4 line decoder|AND gates with inverters|
> |4|Enable circuit|AND gate (a)|EN=0 → output forced low|
> |5|Adder circuit|Full adder|3 inputs including Cᵢₙ|
> |6|Decoder+AND-OR|4-to-1 MUX|Classic MUX implementation|
> |7|Binary addition|01011100|Carry propagation|
> |8|2's complement|10101011|Invert + Add 1|
> |9|XOR+AND circuit|Half adder|No carry input|