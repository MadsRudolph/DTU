---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz]
---
# Quiz 3 - Micro-operations, Counters & Shift Registers

## Question 1 (1 point)

> [!question] Hvilken micro operation udfører dette
>
> (K1 + K2): R1 ← R1 ∨ R3
>
> - [x] **R1 eller R3 indhold overføres til R1 når K1 eller K2 er 1**
> - [ ] R1 eller R3 indhold overføres til R1 når K1 og K2 er 1
> - [ ] R1 og R3 indhold overføres til R1 når K1 eller K2 er 1
> - [ ] R1 og R3 indhold overføres til R1 når K1 og K2 er 1

> [!success] Answer: R1 eller R3 indhold overføres til R1 når K1 eller K2 er 1

> [!note]- Explanation The micro-operation has two parts: a **condition** and a **transfer**.
>
> > [!abstract] Condition: (K1 + K2)
> >
> > The `+` symbol in control conditions means **OR**:
> >
> > $$\text{Condition} = K1 + K2 = K1 \lor K2$$
> >
> > The transfer executes when **K1 or K2** (or both) is 1.
>
> > [!abstract] Transfer: R1 ← R1 ∨ R3
> >
> > The `∨` symbol is the **bitwise OR** operation on data:
> >
> > $$R1 \leftarrow R1 \lor R3$$
> >
> > The result of OR'ing R1 and R3 is stored in R1. The phrasing "R1 **eller** R3 indhold" refers to the OR operation — content from R1 or R3 (bitwise) is transferred to R1.
>
> > [!info] Key Distinction: `+` vs `∨`
> >
> > |Symbol|Context|Meaning|
> > |---|---|---|
> > |`+`|Control condition|OR (when to execute)|
> > |`∨`|Data operation|Bitwise OR (what to compute)|
> >
> > - "R1 **eller** R3 indhold" — the OR operation selects bits from either R1 or R3
> > - "når K1 **eller** K2 er 1" — the condition triggers on either control signal

---

## Question 2 (1 point)

> [!question] Der ønskes udført 2's complement addition mellem R1 og R2 i følgende kredsløb og resultatet skal gemmes i R1 - hvilket logisk niveau skal X og K1 have for at det kan udføres
>
> Circuit: Adder-Subtractor with Select(S) ← X, R1 with Load ← K1, R2 as input
>
> - [ ] X=0 og K1=0
> - [x] **X=1 og K1=1**
> - [ ] X=1 og K1=0
> - [ ] X=0 og K1=1

> [!success] Answer: X=1 og K1=1

> [!note]- Explanation The circuit is an **Adder-Subtractor** with a parallel load register. The question asks for **2's complement addition**, which uses the complement-and-add method.
>
> > [!abstract] Select Signal (X → S)
> >
> > The Select (S) input controls the operation:
> >
> > |S (= X)|Operation|How|
> > |---|---|---|
> > |0|Regular addition: R1 + R2|B input passed unchanged, Cᵢₙ = 0|
> > |1|**2's complement addition**: R1 + R2̄ + 1|B input complemented, Cᵢₙ = 1|
> >
> > For **2's complement addition** (subtraction via complement): **X = 1**
>
> > [!abstract] Load Signal (K1)
> >
> > The Load input on R1 controls whether the result is stored:
> >
> > |K1 (Load)|Effect|
> > |---|---|
> > |0|R1 holds its current value (no update)|
> > |1|R1 loads the result from the adder-subtractor|
> >
> > To **store the result**: **K1 = 1**
>
> > [!tip] Micro-operation notation
> >
> > $$X = 1, \; K1 = 1: \quad R1 \leftarrow R1 + \bar{R2} + 1$$

---

## Question 3 (1 point)

> [!question] Givet dette kredsløb - hvad kan det udføre af operationer
>
> Circuit: 4-bit counter with Load, Count inputs, D flip-flops, AND/OR logic, and Carry Output CO
>
> - [ ] Det er en 4 bit tæller
> - [x] **Det er en 4 bit tæller med hold, load og count**
> - [ ] Det er et 4 bit register med load og reset
> - [ ] Det er et 4 bit skifteregister med load og hold

> [!success] Answer: Det er en 4 bit tæller med hold, load og count

> [!note]- Explanation The circuit is a **4-bit binary counter with parallel load** — one of the most versatile sequential building blocks.
>
> > [!abstract] Control Inputs
> >
> > The circuit has two control inputs that determine the operation:
> >
> > |Count|Load|Operation|
> > |---|---|---|
> > |0|0|**Hold** — outputs unchanged|
> > |0|1|**Load** — parallel data D₀-D₃ loaded|
> > |1|0|**Count** — increment by 1|
> > |1|1|**Load** — parallel load (Load has priority)|
>
> > [!abstract] Circuit Structure
> >
> > - **D flip-flops**: 4 flip-flops store the current count
> > - **AND/OR logic**: Multiplexes between hold, load, and count operations at each D input
> > - **Carry Output (CO)**: Goes high when all outputs are 1 and Count is active — enables cascading multiple counters
>
> > [!info] Three Operations
> >
> > 1. **Hold**: When both controls are 0, the current value feeds back to D inputs — no change
> > 2. **Load**: External data is routed to D inputs — synchronous parallel load
> > 3. **Count**: XOR-based increment logic feeds D inputs — counts up by 1 each clock edge

---

## Question 4 (1 point)

> [!question] Vælg den rigtige sandhedstabel for kredsløbet her
>
> Same circuit as Question 3: 4-bit counter with Load and Count
>
> - [ ] Count=0/Load=0: hold, Count=0/Load=1: hold, Count=1/Load=0: count, Count=1/Load=1: Load data
> - [ ] Count=0/Load=0: reset, Count=0/Load=1: Load data, Count=1/Load=0: count, Count=1/Load=1: Load data
> - [ ] Count=0/Load=0: hold, Count=0/Load=1: Load data, Count=1/Load=0: count, Count=1/Load=1: reset
> - [x] **Count=0/Load=0: hold, Count=0/Load=1: Load data, Count=1/Load=0: count, Count=1/Load=1: Load data**

> [!success] Answer: Count=0/Load=0: hold, Count=0/Load=1: Load data, Count=1/Load=0: count, Count=1/Load=1: Load data

> [!note]- Explanation The truth table defines the counter's behavior for all control input combinations.
>
> > [!abstract] Function Table
> >
> > |Count|Load|Operation|Description|
> > |---|---|---|---|
> > |0|0|**Hold**|Output unchanged, D inputs recirculate current state|
> > |0|1|**Load data**|Parallel inputs D₀-D₃ loaded into flip-flops|
> > |1|0|**Count**|Counter increments by 1|
> > |1|1|**Load data**|**Load takes priority** over count|
>
> > [!info] Why Load has priority
> >
> > In the AND/OR logic at each flip-flop input, the Load signal gates the external data path **before** the Count logic is considered. This design choice ensures:
> >
> > - Deterministic behavior when both controls are active
> > - The ability to force a known state regardless of Count
> > - Safe initialization and preset operations
>
> > [!warning] Why the other options are wrong
> >
> > - **Option 1**: 01 = hold is wrong — Load=1 must load data
> > - **Option 2**: 00 = reset is wrong — no reset functionality with Count=0/Load=0
> > - **Option 3**: 11 = reset is wrong — Load has priority, so it loads data

---

## Question 5 (1 point)

> [!question] Hvilken funktion udfører dette kredsløb
>
> Circuit: 4 D flip-flops in cascade, Clock pulse to first stage, each Q̄ feeds back to own D, each Q feeds to next clock, shared Reset line
>
> - [ ] 4 bit register
> - [ ] Synkron 4 bit binær tæller
> - [x] **4 bit ripple tæller**
> - [ ] 4 bit skifteregister

> [!success] Answer: 4 bit ripple tæller

> [!note]- Explanation This is a **4-bit asynchronous (ripple) counter**.
>
> > [!abstract] Circuit Analysis
> >
> > Each flip-flop has its **Q̄ (complement) output** connected back to its own **D input**:
> >
> > $$D = \bar{Q}$$
> >
> > This makes each flip-flop **toggle** on every rising clock edge (functionally a T flip-flop).
>
> > [!abstract] Clocking Structure
> >
> > ```
> > Clock ──→ [FF₀] ──Q₀──→ [FF₁] ──Q₁──→ [FF₂] ──Q₂──→ [FF₃]
> >            ↺ Q̄→D      ↺ Q̄→D      ↺ Q̄→D      ↺ Q̄→D
> > ```
> >
> > - **FF₀**: Clocked by external Clock pulse
> > - **FF₁**: Clocked by Q₀ output of FF₀
> > - **FF₂**: Clocked by Q₁ output of FF₁
> > - **FF₃**: Clocked by Q₂ output of FF₂
> >
> > Each stage toggles at **half the frequency** of the previous stage.
>
> > [!abstract] Count Sequence
> >
> > |Clock|Q₃|Q₂|Q₁|Q₀|Decimal|
> > |---|---|---|---|---|---|
> > |0|0|0|0|0|0|
> > |1|0|0|0|1|1|
> > |2|0|0|1|0|2|
> > |3|0|0|1|1|3|
> > |...|...|...|...|...|...|
> > |15|1|1|1|1|15|
>
> > [!info] Ripple vs Synchronous Counter
> >
> > |Property|Ripple (Async)|Synchronous|
> > |---|---|---|
> > |Clock distribution|Cascaded (Q→C)|Shared (common clock)|
> > |Propagation delay|Accumulates through stages|Single stage delay|
> > |Speed|Slower (delay ripples)|Faster|
> > |Complexity|Simpler (fewer gates)|More gates needed|
> > |Glitches|Possible during ripple|Clean transitions|
>
> > [!tip] Reset
> >
> > The shared Reset line clears all flip-flops simultaneously, returning the counter to 0000.

---

## Question 6 (1 point)

> [!question] Vælg den micro-operation dette kredsløb udfører
>
> Circuit: 4-bit Shift Register with Parallel Load (SHR 4), with Shift, Load, and Serial Input (SI) controls
>
> - [x] **Shift: Q←slQ, Shift̄·Load: Q←D**
> - [ ] Load·Shift: Q←srQ, Shift̄·Load: Q←D
> - [ ] Shift: Q←srQ, Shift̄·Load: Q←D
> - [ ] Load·Shift: Q←slQ, Shift·Load: Q←D

> [!success] Answer: Shift: Q←slQ, Shift̄·Load: Q←D

> [!note]- Explanation The circuit is a **4-bit Shift Register with Parallel Load** (SHR 4). Despite the name SHR, examining the circuit shows the data shifts **left**.
>
> > [!abstract] Control Logic
> >
> > |Shift|Load|Operation|Micro-operation|
> > |---|---|---|---|
> > |0|0|**Hold**|Q ← Q (no change)|
> > |0|1|**Load**|Q ← D (parallel load)|
> > |1|X|**Shift left**|Q ← slQ (shift left, SI enters Q₃)|
>
> > [!abstract] Shift Left Operation
> >
> > When **Shift = 1**:
> >
> > ```
> > Before: [Q₀] [Q₁] [Q₂] [Q₃]
> >           ↓    ↓    ↓    ↓
> > After:  [Q₁] [Q₂] [Q₃] [SI]   (Q₀ shifted out)
> > ```
> >
> > $$Q \leftarrow slQ$$
> >
> > - Each bit shifts one position to the left
> > - Serial Input (SI) enters at Q₃ (LSB side)
> > - Q₀ is lost (shifted out)
>
> > [!abstract] Parallel Load Operation
> >
> > When **Shift = 0** and **Load = 1** ($\overline{Shift} \cdot Load$):
> >
> > $$Q \leftarrow D$$
> >
> > External data D₀-D₃ is loaded into all flip-flops simultaneously.
>
> > [!info] Why "Shift" has priority
> >
> > The condition for load is $\overline{Shift} \cdot Load$ — Shift must be 0 for Load to take effect. This means:
> >
> > - **Shift = 1** always causes shift left (regardless of Load)
> > - **Load** only works when Shift = 0
> >
> > This is reflected in the circuit's MUX-like AND/OR structure at each flip-flop input.

---

## Summary

> [!tldr] Quick Answers
>
> |Q|Topic|Answer|Key Concept|
> |---|---|---|---|
> |1|Micro-operation|R1 eller R3 OR'd, K1 eller K2|`+` = OR (condition), `∨` = OR (data)|
> |2|Adder-Subtractor|X=1, K1=1|S=1 for 2's complement add, Load=1 to store|
> |3|Counter circuit|4-bit tæller med hold/load/count|Versatile counter building block|
> |4|Truth table|Hold, Load, Count, Load|Load has priority over Count|
> |5|Ripple counter|4 bit ripple tæller|Async: Q̄→D toggle, Q→next clock|
> |6|Shift register|Shift: slQ, Shift̄·Load: Q←D|Shift left with parallel load|

> [!abstract] Register Transfer Notation
>
> |Symbol|In Condition|In Transfer|
> |---|---|---|
> |`+`|OR|Addition|
> |`·`|AND|Multiplication|
> |`∨`|—|Bitwise OR|
> |`⊕`|—|Bitwise XOR|
> |`←`|—|Transfer (assign)|
> |`:`|Separator|—|

---

> [!nav]
> [[Quiz 2|← Quiz 2]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;