---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz, PWA]
---
# PWA Quiz - Datapath & Function Unit

## Question 1 (1 point)

> [!question] Hvilken mikrooperation vælges, når "Function Selector" har værdierne FS₃=0, FS₂=1, FS₁=0, FS₀=1?
>
> - [ ] F = A
> - [ ] F = A exor B
> - [x] **F = A + not B + 1**
> - [ ] F = sr B

> [!success] Answer: F = A + not B + 1

> [!note]- Explanation Fra ALU koden i projektet: Når `JSel(3)=0` er vi i **aritmetisk mode**.
>
> > [!abstract] B-input logik (fra ALU.vhd)
> >
> > ```
> > BSig(i) = ((B(i) AND JSel(1)) OR ((NOT B(i)) AND JSel(2))) AND (NOT JSel(3))
> > ```
> >
> > Med JSel = "0101": JSel(1)=0, JSel(2)=1, JSel(3)=0:
> >
> > - BSig(i) = ((B(i) AND 0) OR (NOT B(i) AND 1)) AND 1 = **NOT B(i)**
> > - Cin = FS₀ = 1
> >
> > Resultat: **F = A + NOT(B) + 1** (2's complement subtraktion)
>
> > [!info] FS Tabel (Aritmetisk, FS₃=0)
> >
> > | FS₂ | FS₁ | FS₀ | Cin | Operation |
> > |---|---|---|---|---|
> > | 0 | 0 | 0 | 0 | F = A (Transfer) |
> > | 0 | 0 | 1 | 1 | F = A + 1 (Increment) |
> > | 0 | 1 | 0 | 0 | F = A + B (Addition) |
> > | 0 | 1 | 1 | 1 | F = A + B + 1 |
> > | 1 | 0 | 0 | 0 | F = A + NOT B |
> > | 1 | 0 | 1 | 1 | F = A + NOT B + 1 (Subtraction) |
> > | 1 | 1 | 0 | 0 | F = A - 1 (Decrement) |
> > | 1 | 1 | 1 | 1 | F = A (Transfer) |

---

## Question 2 (1 point)

> [!question] I funktionsenheden indgår en ALU (Arithmetic Logic Unit). I ALU'en anvendes en række funktionelle blokke til at lægge tal sammen og til at trække tal fra hinanden
>
> - [ ] Full-addere, 9 stk.
> - [x] **Full-addere, 8 stk**
> - [ ] half addere 8 stk
> - [ ] Half-addere, 9 stk.

> [!success] Answer: Full-addere, 8 stk

> [!note]- Explanation Fra `full_adder_8_bit.vhd` i PWA projektet:
>
> > [!abstract] Adder struktur
> >
> > ALU'en bruger **8 full-addere** (bit_0 til bit_7), kædet sammen som en ripple-carry adder:
> >
> > ```
> > carry(0) <= Cin;
> > bit_0: full_adder_1_bit port map(A(0), B(0), carry(0) → sum(0), carry(1));
> > bit_1: full_adder_1_bit port map(A(1), B(1), carry(1) → sum(1), carry(2));
> > ...
> > bit_7: full_adder_1_bit port map(A(7), B(7), carry(7) → sum(7), carry(8));
> > ```
> >
> > - En full-adder per bit → 8-bit ALU kræver **8 full-addere**
> > - Cin kommer udefra (fra FS₀), så der er ikke brug for en ekstra adder
> > - Half-addere er forkert fordi der er brug for carry-in på alle positioner

---

## Question 3 (1 point)

> [!question] Hvad anvendes "H Select" til?
>
> - [ ] Til at styre mikrooperationer i ALU'en
> - [ ] Til at styre multiplekseren i funktions-enheden
> - [x] **Til at styre shifteren**
> - [ ] Til at styre funktions-dekoderen (eng: Function dekoder)

> [!success] Answer: Til at styre shifteren

> [!note]- Explanation Fra `FunctionUnit.vhd`:
>
> > [!abstract] H Select forbindelse
> >
> > ```vhdl
> > U_Shifter: entity work.Shifter
> > port map(
> >     B    => B,
> >     HSel => FS(1 downto 0),  -- H Select = FS₁ & FS₀
> >     H    => HSig
> > );
> > ```
> >
> > HSel styrer shifterens operation:
> >
> > | HSel(1) | HSel(0) | Operation |
> > |---|---|---|
> > | 0 | 0 | H = B (pass-through) |
> > | 0 | 1 | H = sr B (shift right) |
> > | 1 | 0 | H = sl B (shift left) |
> > | 1 | 1 | H = B (pass-through) |
>
> > [!info] Navngivning
> >
> > - **H Select** → Shifter control
> > - **MF** → MUX select (ALU vs Shifter)
> > - **FS** → Function Select (samlet kontrolsignal)

---

## Question 4 (1 point)

> [!question] Hvad opgave udføres af Decoderen i Registerfilen
>
> - [ ] at udvælge relevante register der kan skrives ud samtidigt
> - [ ] udvælge hvilke indput data der skal gemmes
> - [ ] at udvælge multiplexer A og B
> - [x] **at udvælge hvilket register der skal skrives til i registerfilen**

> [!success] Answer: at udvælge hvilket register der skal skrives til i registerfilen

> [!note]- Explanation Fra `DestinationDecoder.vhd` i PWA projektet:
>
> > [!abstract] Decoder funktion
> >
> > Destination Decoder er en **4-til-16 one-hot decoder** der:
> >
> > 1. Modtager et 4-bit register-nummer (DR / DX)
> > 2. Genererer et 16-bit one-hot enable-signal
> > 3. Kun det **valgte register** får load-enable = 1
> >
> > Uden decoderen ville alle 16 registre opdateres samtidigt.
>
> > [!info] Register File skrivelogik
> >
> > ```
> > DR (4-bit) → DestinationDecoder → Enable(0..15) → Register(0..15)
> > ```
> >
> > Multiplexer A og B bruges til **læsning** (SA, SB vælger), mens decoderen styrer **skrivning**.

---

## Question 5 (1 point)

> [!question] Hvad er resultatet, på 2'c complement form, af følgende aritmetiske decimaltalsopgave?
>
> X = (+36) + (-24)
>
> - [ ] X = 1101000
> - [ ] X = 011000
> - [ ] X = 0100100
> - [x] **X = 0001100**

> [!success] Answer: X = 0001100

> [!note]- Explanation
>
> > [!abstract] Beregning
> >
> > (+36) + (-24) = **+12**
> >
> > Konvertering til 7-bit 2's complement:
> >
> > | Tal | Binær |
> > |---|---|
> > | +36 | 0100100 |
> > | -24 | 1101000 (NOT(0011000) + 1) |
> >
> > ```
> >   0100100  (+36)
> > + 1101000  (-24)
> > ---------
> >  10001100  → 0001100 (carry out ignoreres)
> > ```
> >
> > 12₁₀ = **0001100₂** ✓

---

## Question 6 (1 point)

> [!question] Hvad anvendes "MF" til?
>
> - [ ] Til at styre mikrooperationer i ALU'en
> - [ ] Til at styre mikrooperationer i shifteren
> - [x] **Til at styre multiplekseren, der henter data fra ALU'en eller fra shifteren**
> - [ ] Til nulstilling af Function Decoder

> [!success] Answer: Til at styre multiplekseren, der henter data fra ALU'en eller fra shifteren

> [!note]- Explanation Fra `FunctionSelect.vhd` og `FunctionUnit.vhd`:
>
> > [!abstract] MF signal
> >
> > ```vhdl
> > -- FunctionSelect.vhd
> > MF <= FS(3) AND FS(2);
> >
> > -- FunctionUnit.vhd - MUXF vælger mellem ALU (J) og Shifter (H)
> > U_MUXF: entity work.MUX2x1x8
> > port map(J => JSig, H => HSig, MF => MFsig, Y => Res);
> > ```
> >
> > | MF | Kilde | Betingelse |
> > |---|---|---|
> > | 0 | ALU output (J) | FS₃=0 eller FS₃=1 & FS₂=0 |
> > | 1 | Shifter output (H) | FS₃=1 & FS₂=1 |

---

## Question 7 (1 point)

> [!question] På hvilken måde repræsenteres tal ved implementering af subtraktion i ALU'en?
>
> - [ ] Biased
> - [ ] one complement
> - [x] **2's complement**
> - [ ] Signed binary

> [!success] Answer: 2's complement

> [!note]- Explanation Fra `ALU.vhd` i projektet:
>
> > [!abstract] Subtraktion via 2's complement
> >
> > ALU'en beregner subtraktion som: **A + NOT(B) + 1**
> >
> > - `JSel(2)=1` → BSig = NOT B (1's complement)
> > - `Cin=1` (FS₀=1) → adderer 1 for at få 2's complement
> >
> > ```
> > NOT(B) + 1 = -B  (2's complement negation)
> > A + NOT(B) + 1 = A + (-B) = A - B
> > ```
> >
> > Dette svarer til FS = "0101" → F = A + NOT B + 1

---

## Question 8 (1 point)

> [!question] Hvad er værdien af de enkelte bit i J Select, når FS₃=0, FS₂=0, FS₁=1, FS₀=0?
>
> - [ ] J₃=0, J₂=0, J₁=0, J₀=0
> - [ ] J₃=1, J₂=1, J₁=1, J₀=1
> - [x] **J₃=0, J₂=0, J₁=1, J₀=0**
> - [ ] J₃=1, J₂=0, J₁=1, J₀=0

> [!success] Answer: J₃=0, J₂=0, J₁=1, J₀=0

> [!note]- Explanation J Select **er** FS (Function Select) — de samme 4 bit.
>
> > [!abstract] Forbindelse fra FunctionUnit.vhd
> >
> > ```vhdl
> > FS <= FS3 & FS2 & FS1 & FS0;
> >
> > U_ALU: entity work.ALU
> > port map(
> >     JSel => FS(3 downto 0),  -- JSel = FS direkte
> >     ...
> > );
> > ```
> >
> > Så når FS = "0010":
> > - J₃=0, J₂=0, J₁=1, J₀=0
> > - JSel(1)=1 → BSig = B (passerer igennem)
> > - Cin = FS₀ = 0
> > - **Operation: F = A + B (Addition)**

---

## Question 9 (1 point)

> [!question] Statusflaget for Overflow, V, dannes ved at anvende en boolsk operation på den mest betydende og den næstmest betydende bit. Hvilken boolsk operation er det?
>
> - [ ] NOR
> - [ ] AND
> - [x] **XOR**
> - [ ] OR

> [!success] Answer: XOR

> [!note]- Explanation Fra `full_adder_8_bit.vhd` i projektet:
>
> > [!abstract] Overflow detection
> >
> > ```vhdl
> > V <= Carry(8) XOR Carry(7);
> > ```
> >
> > - **Carry(8)** = carry ud af MSB (bit 7)
> > - **Carry(7)** = carry ind i MSB (bit 7)
> >
> > Overflow opstår når carry ind i og ud af MSB er **forskellige** — præcis hvad XOR detekterer.
> >
> > | Carry(8) | Carry(7) | V | Betydning |
> > |---|---|---|---|
> > | 0 | 0 | 0 | Ingen overflow |
> > | 0 | 1 | 1 | Overflow (positiv + positiv → negativ) |
> > | 1 | 0 | 1 | Overflow (negativ + negativ → positiv) |
> > | 1 | 1 | 0 | Ingen overflow |

---

## Question 10 (1 point)

> [!question] Tallene der indgår i den følgende beregning er binære tal på 2s komplementære form.
>
> X = 100111 + 111000
>
> Hvad er resultatet, og forekommer der Overflow?
>
> - [ ] X = 1011111, Nej der er ikke overflow
> - [ ] X = 1011111, Ja der er overflow
> - [x] **X = 011111, Ja der er overflow**
> - [ ] X = 011111, Nej der er ikke overflow

> [!success] Answer: X = 011111, Ja der er overflow

> [!note]- Explanation
>
> > [!abstract] Beregning
> >
> > ```
> >   100111  (-25 i 6-bit 2's complement)
> > + 111000  (-8 i 6-bit 2's complement)
> > --------
> > 1011111  → 011111 (6-bit resultat), carry out = 1
> > ```
> >
> > **Overflow check (V = Carry_out XOR Carry_in_MSB):**
> >
> > - Bit 4: 0+1 = 1, carry = 0
> > - Bit 5 (MSB): 1+1+0 = 0, carry out = 1
> > - Carry ind i MSB = **0**, Carry ud af MSB = **1**
> > - V = 1 XOR 0 = **1 → Overflow!**
> >
> > **Verifikation:** Begge operander er negative (MSB=1), men resultatet 011111 er positivt (MSB=0). To negative tal kan aldrig give et positivt resultat → overflow bekræftet.
> >
> > Forventet resultat: -25 + (-8) = -33, men 6-bit 2's complement rækkevidde er [-32, 31], så -33 kan ikke repræsenteres.

---

## Summary

> [!tldr] Quick Answers
>
> | Q | Emne | Svar | Nøglekoncept |
> |---|---|---|---|
> | 1 | Function Selector FS=0101 | F = A + not B + 1 | 2's complement subtraktion |
> | 2 | ALU addere | Full-addere, 8 stk | En per bit i 8-bit ripple-carry |
> | 3 | H Select | Styre shifteren | HSel = FS(1:0) |
> | 4 | Decoder i RegisterFile | Vælge skriveregistre | 4-til-16 one-hot decoder |
> | 5 | (+36) + (-24) | X = 0001100 | 12₁₀ i 2's complement |
> | 6 | MF | MUX mellem ALU og Shifter | MF = FS₃ AND FS₂ |
> | 7 | Subtraktionsrepræsentation | 2's complement | A + NOT(B) + 1 |
> | 8 | J Select ved FS=0010 | J₃=0, J₂=0, J₁=1, J₀=0 | JSel = FS direkte |
> | 9 | Overflow flag V | XOR | V = Carry(8) XOR Carry(7) |
> | 10 | 100111 + 111000 | 011111, overflow | Negativ + negativ → positiv = overflow |

---

> [!nav]
> [[Quiz 4|← Quiz 4]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
