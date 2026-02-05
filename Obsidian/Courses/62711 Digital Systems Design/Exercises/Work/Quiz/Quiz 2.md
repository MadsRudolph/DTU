# Quiz 2 - Number Systems & Digital Circuits

## Question 1 (1 point)

> [!question] Konverter fra unsigned binary 11010 til one's complement negativt nummer
> 
> - [x] **100101**
> - [ ] 000101
> - [ ] 110101

> [!success] Answer: 100101

> [!note]- Explanation **One's complement** representation of a negative number is obtained by simply inverting all bits of the positive number.
> 
> > [!abstract] Step 1: Determine bit width The original number 11010 is 5 bits. For signed representation, we need a sign bit, so we use 6 bits.
> > 
> > Pad with leading zero: `011010`
> 
> > [!abstract] Step 2: Invert all bits
> > 
> > ```
> > 011010  (original +26)
> > ↓ invert
> > 100101  (one's complement -26)
> > ```
> 
> > [!info] One's Complement Properties
> > 
> > - MSB is the sign bit (1 = negative)
> > - Has two representations of zero: `000000` (+0) and `111111` (-0)
> > - Range for n bits: $-(2^{n-1}-1)$ to $+(2^{n-1}-1)$
> > - Simple to compute but problematic for arithmetic

---

## Question 2 (1 point)

> [!question] Konverter fra unsigned binary 11010 til two's complement negativt nummer
> 
> - [ ] 100101
> - [x] **100110**
> - [ ] 000110

> [!success] Answer: 100110

> [!note]- Explanation **Two's complement** is the standard representation for signed integers in digital systems.
> 
> > [!abstract] Method: Invert and Add 1 **Step 1**: Pad to 6 bits and invert all bits
> > 
> > ```
> > 011010  (original +26)
> > ↓ invert
> > 100101  (one's complement)
> > ```
> > 
> > **Step 2**: Add 1
> > 
> > ```
> >   100101
> > +      1
> > ────────
> >   100110  (two's complement -26)
> > ```
> 
> > [!tip] Alternative Method: Copy until first 1, then invert Working from right to left:
> > 
> > 1. Copy all bits up to and including the first '1'
> > 2. Invert all remaining bits
> > 
> > ```
> > 011010
> >     ↑ first 1 from right
> > 
> > Copy:   10
> > Invert: 1001
> > Result: 100110
> > ```
> 
> > [!info] Two's Complement Properties
> > 
> > - Only one representation of zero
> > - Range for n bits: $-2^{n-1}$ to $+(2^{n-1}-1)$
> > - Asymmetric range (one more negative number)
> > - Addition works the same as unsigned (no special handling)

---

## Question 3 (1 point)

> [!question] Repræsenter det decimal tal -76 på Biased form med 8bit repræsentation
> 
> (hints: skim s 527-529)
> 
> - [ ] 10110011
> - [x] **0011 0011**
> - [ ] 10110100
> - [ ] 01001100

> [!success] Answer: 0011 0011 (51 in decimal)

> [!note]- Explanation **Biased (Excess-N) representation** adds a fixed bias value to the number before storing it. For 8-bit representation, the standard bias is **127** (used in IEEE 754 floating point exponents).
> 
> > [!abstract] Conversion Formula $$\text{Biased value} = \text{Actual value} + \text{Bias}$$ $$\text{Biased value} = -76 + 127 = 51$$
> 
> > [!abstract] Convert 51 to binary
> > 
> > |Division|Quotient|Remainder|
> > |---|---|---|
> > |51 ÷ 2|25|1|
> > |25 ÷ 2|12|1|
> > |12 ÷ 2|6|0|
> > |6 ÷ 2|3|0|
> > |3 ÷ 2|1|1|
> > |1 ÷ 2|0|1|
> > 
> > Reading remainders bottom-up: 110011
> > 
> > Pad to 8 bits: **0011 0011**
> 
> > [!info] Why Biased Representation?
> > 
> > - Used primarily for **floating-point exponents** (IEEE 754)
> > - Allows simple comparison of exponents as unsigned integers
> > - Zero is represented as the bias value (127 → 01111111)
> > - No need for separate sign bit handling in comparisons
> 
> > [!example] Bias values
> > 
> > |Format|Bits|Bias|
> > |---|---|---|
> > |8-bit (common)|8|127 ($2^7 - 1$)|
> > |IEEE 754 single|8|127|
> > |IEEE 754 double|11|1023|

---

## Question 4 (1 point)

> [!question] Hvornår er der overflow ved 2's complement addition
> 
> - [ ] andet
> - [ ] Når der er forskelligt fortegn på de 2 operander
> - [ ] Når der samme fortegns bit på de to operander og resultatet får modsat fortegn
> - [x] **Når carry out på sign-bit er forskellig fra carry in på signbit position**

> [!success] Answer: Når carry out på sign-bit er forskellig fra carry in på signbit position

> [!note]- Explanation **Overflow** in 2's complement occurs when the result of an arithmetic operation cannot be represented in the available number of bits.
> 
> > [!abstract] Hardware Overflow Detection The standard hardware method detects overflow by comparing carries at the MSB (sign bit):
> > 
> > $$\text{Overflow} = C_{in,MSB} \oplus C_{out,MSB}$$
> > 
> > Overflow occurs when the **carry into** the sign bit position is **different from** the **carry out** of the sign bit position.
> 
> > [!example] Overflow Example with Carry Analysis
> > 
> > **Case: Positive + Positive = Negative (OVERFLOW)**
> > 
> > ```
> >        C₃ C₂ C₁ C₀
> >         0  1  1  0  ← carries
> >         ↓
> >         0  1  0  1  (+5)
> >       + 0  1  0  0  (+4)
> >       ───────────
> >         1  0  0  1  (-7) ← Wrong!
> > 
> > Cᵢₙ(MSB) = 1, Cₒᵤₜ(MSB) = 0
> > 1 ⊕ 0 = 1 → OVERFLOW!
> > ```
> > 
> > **Case: Positive + Negative = Positive (NO OVERFLOW)**
> > 
> > ```
> >        C₃ C₂ C₁ C₀
> >         1  1  0  0  ← carries
> >         ↓
> >         0  1  0  1  (+5)
> >       + 1  1  0  0  (-4)
> >       ───────────
> >         0  0  0  1  (+1) ← Correct!
> > 
> > Cᵢₙ(MSB) = 1, Cₒᵤₜ(MSB) = 1
> > 1 ⊕ 1 = 0 → NO OVERFLOW
> > ```
> 
> > [!info] Equivalent Detection Methods Two equivalent ways to detect overflow:
> > 
> > |Method|Formula|Used By|
> > |---|---|---|
> > |**Carry-based**|$C_{in,MSB} \oplus C_{out,MSB}$|Hardware (ALU)|
> > |**Sign-based**|$(A_{MSB} = B_{MSB}) \land (A_{MSB} \neq S_{MSB})$|Conceptual|
> > 
> > Both detect the same condition — the carry method is preferred in hardware because it only requires one XOR gate connected to the adder's internal carries.
> 
> > [!warning] Carry Out ≠ Overflow **Carry out** alone does NOT indicate signed overflow!
> > 
> > - Carry out = unsigned overflow indicator
> > - Overflow flag = signed overflow indicator (Cᵢₙ ⊕ Cₒᵤₜ at MSB)

---

## Question 5 (1 point)

> [!question] Udfør regnestykket her - numre format er i 2's complement
> 
> 0110111 + 0101111
> 
> - [ ] 001110
> - [x] **1100110**
> - [ ] 0001000
> - [ ] 00010011

> [!success] Answer: 1100110

> [!note]- Explanation Performing 7-bit 2's complement addition:
> 
> > [!abstract] Binary Addition
> > 
> > ```
> >     111111   ← carries
> >    0110111   (55₁₀)
> >  + 0101111   (47₁₀)
> >  ─────────
> >    1100110   
> > ```
> 
> > [!abstract] Step-by-step
> > 
> > |Pos|A|B|Cᵢₙ|Sum|Cₒᵤₜ|
> > |---|---|---|---|---|---|
> > |0|1|1|0|0|1|
> > |1|1|1|1|1|1|
> > |2|1|1|1|1|1|
> > |3|0|1|1|0|1|
> > |4|1|0|1|0|1|
> > |5|1|1|1|1|1|
> > |6|0|0|1|1|0|
> 
> > [!warning] Interpreting the Result
> > 
> > - As unsigned: 1100110 = 102₁₀
> > - As 7-bit 2's complement: MSB=1 means negative
> >     - Negate: 0011010 = 26₁₀
> >     - So result represents **-26**
> > 
> > But 55 + 47 = 102, not -26! This indicates **overflow**.

---

## Question 6 (1 point)

> [!question] Er der overflow i foregående addition
> 
> - [x] **True**
> - [ ] False

> [!success] Answer: True

> [!note]- Explanation Checking for overflow using the sign bit rule:
> 
> > [!abstract] Overflow Analysis
> > 
> > |Value|Binary|Sign Bit (MSB)|
> > |---|---|---|
> > |A = +55|0110111|0 (positive)|
> > |B = +47|0101111|0 (positive)|
> > |Result|1100110|1 (negative)|
> 
> > [!danger] Overflow Detected!
> > 
> > - Both operands are **positive** (MSB = 0)
> > - Result appears **negative** (MSB = 1)
> > - This matches the overflow condition: same signs in, opposite sign out
> 
> > [!info] Why overflow occurred
> > 
> > - 7-bit 2's complement range: **-64 to +63**
> > - Expected result: 55 + 47 = **102**
> > - 102 > 63 (maximum positive value)
> > - Result wraps around to negative: 102 - 128 = -26
> > 
> > The hardware result 1100110₂ = -26 in 2's complement, which is mathematically incorrect.

---

## Question 7 (1 point)

> [!question] Hvilken funktion har dette kredsløb
> 
> Circuit: 2-to-4 Decoder feeding into 4×2 AND-OR structure with data inputs I₀-I₃
> 
> - [ ] 2 til 4 decoder
> - [ ] 4 til 2 encoder
> - [x] **4 input single bit til 1 output multiplexer**

> [!success] Answer: 4 input single bit til 1 output multiplexer

> [!note]- Explanation This circuit implements a **4-to-1 multiplexer** using a decoder-based architecture.
> 
> > [!abstract] Circuit Analysis
> > 
> > ```
> > S₁,S₀ ──→ [2-to-4 Decoder] ──→ 4 one-hot lines
> >                                    │
> >           I₀ ──────────────────────┼──→ [AND] ──┐
> >           I₁ ──────────────────────┼──→ [AND] ──┼──→ [OR] ──→ Y
> >           I₂ ──────────────────────┼──→ [AND] ──┤
> >           I₃ ──────────────────────┘──→ [AND] ──┘
> > ```
> 
> > [!abstract] How it works
> > 
> > 1. **Decoder**: Converts 2-bit select (S₁S₀) into 4 one-hot signals
> > 2. **AND gates**: Each decoder output enables one data input
> > 3. **OR gate**: Combines all paths (only one is active at a time)
> 
> > [!example] Operation Table
> > 
> > |S₁|S₀|Decoder Output|Y|
> > |---|---|---|---|
> > |0|0|1000|I₀|
> > |0|1|0100|I₁|
> > |1|0|0010|I₂|
> > |1|1|0001|I₃|
> 
> > [!tip] MUX Implementations This is the **decoder + AND-OR** implementation of a MUX. Other implementations:
> > 
> > - Transmission gates
> > - Tristate buffers
> > - CMOS pass transistors

---

## Question 8 (1 point)

> [!question] Hvilken funktion udfører dette kredsløb
> 
> Circuit with truth table showing one-hot outputs and AND gates with inverters
> 
> Truth table: A₁A₀ → D₀D₁D₂D₃ (one-hot pattern)
> 
> Gate equations: D₀ = Ā₁Ā₀, D₁ = Ā₁A₀, D₂ = A₁Ā₀, D₃ = A₁A₀
> 
> - [x] **En 2 til 4 decoder**
> - [ ] En 4 bit fulladder
> - [ ] 4 til en decoder
> - [ ] En 4 til 1 multiplexer

> [!success] Answer: En 2 til 4 decoder

> [!note]- Explanation The truth table and gate structure define a **2-to-4 line decoder**.
> 
> > [!abstract] Truth Table Analysis
> > 
> > |A₁|A₀|D₀|D₁|D₂|D₃|
> > |---|---|---|---|---|---|
> > |0|0|1|0|0|0|
> > |0|1|0|1|0|0|
> > |1|0|0|0|1|0|
> > |1|1|0|0|0|1|
> > 
> > **Key observation**: Exactly one output is HIGH for each input combination (one-hot encoding)
> 
> > [!abstract] Boolean Equations Each output is a **minterm** of the inputs:
> > 
> > - $D_0 = \bar{A_1} \cdot \bar{A_0}$ (minterm 0)
> > - $D_1 = \bar{A_1} \cdot A_0$ (minterm 1)
> > - $D_2 = A_1 \cdot \bar{A_0}$ (minterm 2)
> > - $D_3 = A_1 \cdot A_0$ (minterm 3)
> 
> > [!info] Decoder Properties
> > 
> > - **n inputs → 2ⁿ outputs**
> > - Exactly one output active at any time
> > - Implements all minterms of n variables
> > - Used for: memory address decoding, instruction decoding, MUX building blocks
> 
> > [!tip] Decoder vs Encoder
> > 
> > |Decoder|Encoder|
> > |---|---|
> > |n inputs → 2ⁿ outputs|2ⁿ inputs → n outputs|
> > |Binary to one-hot|One-hot to binary|
> > |AND gates with inverters|OR gates|

---

## Summary

> [!tldr] Quick Answers
> 
> |Q|Topic|Answer|Key Concept|
> |---|---|---|---|
> |1|One's complement|100101|Invert all bits|
> |2|Two's complement|100110|Invert + Add 1|
> |3|Biased form (-76)|0011 0011|Add bias (127): -76+127=51|
> |4|Overflow condition|Cᵢₙ(MSB) ⊕ Cₒᵤₜ(MSB)|Carry-based detection|
> |5|2's comp addition|1100110|Standard binary addition|
> |6|Overflow present?|True|+55 + +47 = "negative"|
> |7|Decoder+AND-OR|4-to-1 MUX|Select one of N inputs|
> |8|One-hot outputs|2-to-4 decoder|Minterm generator|

> [!abstract] Number Representation Comparison
> 
> |Representation|Formula|8-bit Range|Zero|
> |---|---|---|---|
> |Unsigned|Direct binary|0 to 255|00000000|
> |Sign-magnitude|MSB = sign|-127 to +127|±0|
> |One's complement|Invert for negative|-127 to +127|±0|
> |Two's complement|Invert + 1|-128 to +127|Unique|
> |Biased (excess-127)|Value + 127|-127 to +128|01111111|