---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz, floating-point, instructions]
---
# Quiz 10 - Floating Point & Instruction Set

## Question 1 (1 point)

> [!question] Givet IEEE 32 bit floating point format - vælg det rigtige format
>
> - [ ] s(1) | f(28) | e(3)
> - [ ] s(1) | e(10) | f(21)
> - [ ] s(1) | f(23) | e(8)
> - [x] **s(1) | e(8) | f(23)**

> [!success] Answer: s(1) | e(8) | f(23)

> [!note]- Explanation IEEE 754 single precision har rækkefølgen sign → exponent → fraction, med bit-bredderne 1, 8, 23.
>
> > [!abstract] IEEE 754 Single Precision Layout
> >
> > | Felt | Bits | Position | Beskrivelse |
> > |---|---|---|---|
> > | Sign (s) | 1 | 31 | 0 = positiv, 1 = negativ |
> > | Exponent (e) | 8 | 30-23 | Biased med 127 (excess-127) |
> > | Fraction (f) | 23 | 22-0 | Mantissens brøkdel, implicit leading 1 |
> >
> > Total = 1 + 8 + 23 = 32 bit
> >
> > Værdi = (-1)^s × 1.f × 2^(e-127)

---

## Question 2 (1 point)

> [!question] Instruction format givet som: Opcode | Mode | Address or operand. Hvad er formålet med Mode delen/feltet?
>
> - [ ] det er en data operand
> - [x] **indikator for addresseringsform**
> - [ ] det er en addresse

> [!success] Answer: indikator for addresseringsform

> [!note]- Explanation Mode-feltet specificerer **hvordan** Address/operand-feltet skal fortolkes (addressing mode), ikke selve data eller addressen.
>
> > [!abstract] Typiske addressing modes
> >
> > | Mode | Fortolkning af operand-feltet |
> > |---|---|
> > | Immediate | Operand ER selve værdien |
> > | Direct | Operand ER addressen til data i hukommelsen |
> > | Indirect | Operand peger på en celle der indeholder addressen |
> > | Register | Operand identificerer et register |
> > | Indexed | Operand + indexregister = effektiv addresse |
> > | Relative | Operand + PC = effektiv addresse |
> >
> > Mode-feltet gør det muligt at genbruge samme opcode med forskellige operand-fortolkninger → kompakt instruction set.

---

## Question 3 (1 point)

> [!question] Hvorfor benyttes Biased Exponent ved floating point numre
>
> - [ ] Fordi flaoting point skal repræsenteres som et helttal
> - [ ] Fordi så er alle tal positive
> - [x] **Fordi tallets eksponent er altid positiv**

> [!success] Answer: Fordi tallets eksponent er altid positiv

> [!note]- Explanation Biased representation gør at **eksponentfeltet** altid er et unsigned positivt tal — den faktiske eksponent kan godt være negativ, men den gemte værdi (raw + bias) er altid ≥ 0.
>
> > [!abstract] Bias = 127 for single precision
> >
> > | Actual exponent | Biased (gemt i feltet) |
> > |---|---|
> > | -126 | 1 (0000 0001) |
> > | 0 | 127 (0111 1111) |
> > | +127 | 254 (1111 1110) |
> >
> > Uden bias ville eksponenten kræve sign-magnitude eller two's complement, hvilket ville komplicere hardware-sammenligning. Med bias kan to floating point tal sammenlignes som om de var unsigned integers.
> >
> > Raw 0 (alle 0) og 255 (alle 1) er reserveret til ±0/denormals og ±∞/NaN.

---

## Question 4 (1 point)

> [!question] Givet excess-127 bias, hvad er den mindste og største eksponent (IEEE 754 normale tal)?
>
> - [ ] -127, +127
> - [x] **-126, +127**
> - [ ] -126, 128

> [!success] Answer: -126, +127

> [!note]- Explanation For normale tal er raw exponent-feltet mellem 1 og 254. Actual = raw - 127, så området er -126 til +127.
>
> > [!abstract] Reserverede raw-værdier
> >
> > | Raw exp | Actual exp | Betydning |
> > |---|---|---|
> > | 0 | - | ±0 eller denormal/subnormal tal |
> > | 1 | -126 | Mindste normale eksponent |
> > | 127 | 0 | Bias-offset |
> > | 254 | +127 | Største normale eksponent |
> > | 255 | - | ±∞ eller NaN |
> >
> > Med 8-bit exponent er der 2^8 = 256 mulige raw-værdier, men 2 er reserveret → 254 bruges til normale tal.

---

## Question 5 (1 point)

> [!question] Hvad er dette binære floating point number (single precision) i hex format 0x45587C00 i almindelig decimal tal?
>
> - [ ] 1415,75
> - [x] **3463,75**
> - [ ] 2831,5

> [!success] Answer: 3463,75

> [!note]- Explanation Opdel hex i sign, exponent og fraction, beregn så (-1)^s × (1.f) × 2^(e-127).
>
> > [!abstract] Bit-opdeling af 0x45587C00
> >
> > Binær: `0100 0101 0101 1000 0111 1100 0000 0000`
> >
> > | Felt | Bits | Værdi |
> > |---|---|---|
> > | Sign | `0` | + |
> > | Exponent | `1000 1010` | 138 (raw) → 138 - 127 = **11** |
> > | Fraction | `101 1000 0111 1100 0000 0000` | se nedenfor |
> >
> > Mantisse med implicit leading 1:
> >
> > 1.f = 1 + 2⁻¹ + 2⁻³ + 2⁻⁴ + 2⁻⁹ + 2⁻¹⁰ + 2⁻¹¹ + 2⁻¹² + 2⁻¹³
> > = 1 + 0,5 + 0,125 + 0,0625 + 0,001953125 + 0,0009765625 + 0,00048828125 + 0,000244140625 + 0,0001220703125
> > = **1,6912841796875**
> >
> > Værdi = 1,6912841796875 × 2¹¹ = 1,6912841796875 × 2048 = **3463,75**

---

## Question 6 (1 point)

> [!question] Givet dette tal -9,359375 - hvad er den binære repræsentation i hexadecimal (single precision)?
>
> - [x] **C115C000**
> - [ ] C115E000
> - [ ] C14AE000

> [!success] Answer: C115C000

> [!note]- Explanation Konverter til binær, normaliser, pak sign/exp/fraction, og konverter til hex.
>
> > [!abstract] Konversionstrin
> >
> > **1. Helttalsdel:** 9₁₀ = 1001₂
> >
> > **2. Brøkdel:** 0,359375₁₀
> >
> > | Multiplikation | Resultat | Bit |
> > |---|---|---|
> > | 0,359375 × 2 | 0,71875 | 0 |
> > | 0,71875 × 2 | 1,4375 | 1 |
> > | 0,4375 × 2 | 0,875 | 0 |
> > | 0,875 × 2 | 1,75 | 1 |
> > | 0,75 × 2 | 1,5 | 1 |
> > | 0,5 × 2 | 1,0 | 1 |
> >
> > 0,359375 = 0,010111₂
> >
> > **3. Samlet:** 9,359375 = 1001,010111₂
> >
> > **4. Normaliser:** 1001,010111 = 1,001010111 × 2³
> >
> > **5. Pak felterne:**
> >
> > | Felt | Værdi | Bits |
> > |---|---|---|
> > | Sign | negativ | `1` |
> > | Exponent | 3 + 127 = 130 | `1000 0010` |
> > | Fraction | 001010111 + 14 nuller | `0010 1011 1000 0000 0000 000` |
> >
> > Samlet 32-bit: `1 10000010 00101011100000000000000`
> >
> > Gruppér i nibbler: `1100 0001 0001 0101 1100 0000 0000 0000`
> >
> > = **0xC115C000**

---

## Question 7 (1 point)

> [!question] Giv eksempler på instruktioner indenfor: Arithmetic, Logical, Shift, Move fra PWF

> [!success] Svar
>
> | Kategori | Eksempler |
> |---|---|
> | **Arithmetic** | ADD, SUB, MUL, DIV, INC, DEC, NEG |
> | **Logical** | AND, OR, NOT, XOR, NAND, NOR |
> | **Shift** | SHL, SHR, ASL, ASR, ROL, ROR |
> | **Move** | MOV, MV, LD (load), ST (store) |

> [!note]- Explanation Disse er **data-manipulation** instruktioner — de arbejder på indholdet af registre eller operander uden at ændre programflowet.
>
> > [!abstract] Typisk opdeling
> >
> > | Type | Formål | Eksempel i pseudo-asm |
> > |---|---|---|
> > | Arithmetic | Numeriske operationer | `ADD R1, R2, R3` → R1 ← R2 + R3 |
> > | Logical | Bitvise operationer | `AND R1, R2, R3` → R1 ← R2 AND R3 |
> > | Shift | Bit-forskydning | `SHL R1, #2` → R1 ← R1 << 2 |
> > | Move | Flyt data mellem registre | `MOV R1, R2` → R1 ← R2 |
> >
> > Arithmetic og logical bruger typisk ALU'en, shift kan have dedikeret shifter, move rammer register-filen.

---

## Question 8 (1 point)

> [!question] Giv eksempler på instruktioner der benyttes ved hukommelse/memory

> [!success] Svar
>
> | Instruktion | Funktion |
> |---|---|
> | **LOAD (LD)** | Hent data fra hukommelse til register |
> | **STORE (ST)** | Gem register-indhold i hukommelse |
> | **MOV** | Flyt data mellem register og hukommelse |
> | **PUSH** | Læg register på stakken (SP--) |
> | **POP** | Hent fra stakken til register (SP++) |
> | **XCHG** | Byt indhold mellem register og hukommelse |

> [!note]- Explanation Memory-instruktioner er den eneste måde data går mellem CPU-registre og RAM (load/store-arkitektur).
>
> > [!abstract] Load/Store princip
> >
> > | Operation | Retning |
> > |---|---|
> > | LOAD | Memory → Register |
> > | STORE | Register → Memory |
> > | PUSH | Register → Stack (memory) |
> > | POP | Stack (memory) → Register |
> >
> > I en ren **load/store-arkitektur** (RISC) kan aritmetiske instruktioner kun operere på registre — data skal først hentes ind med LOAD.

---

## Question 9 (1 point)

> [!question] Giv eksempler på instruktioner for Control transfer

> [!success] Svar
>
> | Instruktion | Funktion |
> |---|---|
> | **JMP** | Ubetinget hop til adresse |
> | **BR** | Branch (ofte betinget) |
> | **JZ / JE** | Hop hvis Zero-flag sat (if equal) |
> | **JNZ / JNE** | Hop hvis Zero-flag IKKE sat |
> | **JC / JNC** | Hop hvis Carry sat/ikke sat |
> | **CALL** | Kald subrutine (gem return-adresse på stakken) |
> | **RET** | Returner fra subrutine |
> | **LOOP** | Dekrementér tæller, hop hvis ≠ 0 |
> | **INT** | Software-interrupt |
> | **IRET** | Returner fra interrupt |

> [!note]- Explanation Control transfer-instruktioner ændrer **Program Counter (PC)** ikke-sekventielt og implementerer derved forgreninger, løkker, funktionskald og interrupts.
>
> > [!abstract] To hovedtyper
> >
> > | Type | PC-opførsel | Eksempler |
> > |---|---|---|
> > | **Ubetinget** | Altid hop | JMP, CALL, RET |
> > | **Betinget** | Hop kun hvis flag opfyldt | JZ, JNE, BEQ, BNE |
> >
> > CALL/RET bruger stakken til at gemme return-adressen → muliggør nested/recursive kald.

---

## Summary

> [!tldr] Quick Answers
>
> | Q | Topic | Answer | Key Concept |
> |---|---|---|---|
> | 1 | IEEE 754 format | s(1)\|e(8)\|f(23) | Sign → Exponent → Fraction |
> | 2 | Mode-feltet i instruktion | Indikator for addresseringsform | Hvordan operand fortolkes |
> | 3 | Hvorfor biased exponent | Tallets eksponent er altid positiv | Unsigned exponent-felt |
> | 4 | Excess-127 eksponent-område | -126, +127 | Raw 0 og 255 er reserveret |
> | 5 | 0x45587C00 → decimal | 3463,75 | 1,6912... × 2¹¹ |
> | 6 | -9,359375 → hex | C115C000 | Sign=1, exp=130, f=00101011100... |
> | 7 | Arith/Logic/Shift/Move | ADD, AND, SHL, MOV | Data-manipulation |
> | 8 | Memory-instruktioner | LOAD, STORE, PUSH, POP | Load/store-arkitektur |
> | 9 | Control transfer | JMP, CALL, RET, JZ | Ændrer Program Counter |

---

> [!nav]
> [[Quiz before lection 9|← Quiz before lection 9]] | [[Quiz 10|Current]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
