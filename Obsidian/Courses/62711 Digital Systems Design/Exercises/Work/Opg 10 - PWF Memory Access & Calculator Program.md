---
course: "62711"
course-name: "Digital Systems Design"
type: exercise
tags: [DSD, exercise, PWF, timing, RTL]
---
# Opg 10 - PWF Memory Access & Calculator Program

> [!abstract] Exercise Overview
> Timing diagrams for RAM and Port Register accesses through the PWF MUX MR, and an RTL calculator program that adds two button-loaded operands and displays the result on the 7-segment display.
> Reference: Lecture 10 (memory-mapped I/O, slide 12) · [[62711_ProjectWork_F_F2026.pdf|PWF Project Assignment]] · [[Lecture 10 - Floating Point & Assembly Language]]

> [!info] Files
> - Exercise: [[opg10.pdf|Opg 10]]

---

> [!info] PWF Memory Map (Lecture 10, slide 12)
> Address bus 8 bits, data bus 16 bits. The upper 8 addresses (`0xF8`-`0xFF`) are memory-mapped I/O — `MMR` selects port-register output over RAM output on `MUX MR`.
>
> | Address | Name | Access | Function |
> |---|---|---|---|
> | `0x00` - `0xF7` | RAM | R/W | 248 words of program/data |
> | `0xF8` | MR0 | R/W | D\_Word low byte (7-seg) |
> | `0xF9` | MR1 | R/W | D\_Word high byte (7-seg) |
> | `0xFA` | MR2 | R/W | LED0..LED7 |
> | `0xFB` | MR3 | R | Operand latched on BTNR |
> | `0xFC` | MR4 | R | Operand latched on BTNL |
> | `0xFD` | MR5 | R | Operand latched on BTND |
> | `0xFE` | MR6 | R | Operand latched on BTNU |
> | `0xFF` | MR7 | R | Operand latched on BTNC |
>
> `MMR = 1` ⇔ `Address(7:3) = "11111"`. `Data_OutR(7:0)` carries the selected MR; the high byte is zero-padded.

---

## 10.1 Timing Diagrams for Read/Write Sequences

> [!question] Draw a timing diagram (Data\_In, MW, Address, Data\_OutM, Data\_OutR, MMR, D\_Word, LD1-8, SW1-8, BTN1-5, MUX MR output) for the four sequences.

> [!info] Conventions
> - One transaction per clock cycle. Synchronous RAM/PortReg: writes take effect on the rising edge that ends the cycle; the new value is visible on the read port from the next cycle.
> - Initial state: all RAM = `0x0000`, all MRn = `0x00`, all switches/buttons = 0.
> - Data bus is 16 bit; 8-bit values written to MR0-MR2 use the low byte (`Data_In(7:0)`); the high byte is "X" (don't-care) for port writes.
> - "—" means signal is unchanged from the previous row or don't-care for that cycle.

### A.- Read 0x45, Write 0xAA → 0x45, Read 0x45

> [!example] Sequence A — pure RAM accesses (`0x45 < 0xF8`, so `MMR = 0` throughout)
>
> | Signal | Cycle 1: Read 0x45 | Cycle 2: Write 0xAA | Cycle 3: Read 0x45 |
> |---|---|---|---|
> | Address | `0x45` | `0x45` | `0x45` |
> | MW | 0 | **1** | 0 |
> | Data\_In | XXXX | `0x00AA` | XXXX |
> | Data\_OutM | `0x0000` (old) | `0x0000` (latch pending) | **`0x00AA`** |
> | Data\_OutR | `0x00`&MR5 = `0x0000` | `0x0000` | `0x0000` |
> | MMR | 0 | 0 | 0 |
> | MUX MR out | `0x0000` (= Data\_OutM) | `0x0000` | **`0x00AA`** |
> | D\_Word | `0x0000` | `0x0000` | `0x0000` |
> | LD1-8 | `0x00` | `0x00` | `0x00` |
> | SW1-8 | `0x00` | `0x00` | `0x00` |
> | BTN1-5 | 00000 | 00000 | 00000 |
>
```wavedrom
{signal: [
  {name: 'clk',             wave: 'p..'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=..', data: ['0x45']},
    {name: 'MW',            wave: '010'},
    {name: 'Data_In[15:0]', wave: 'x=x', data: ['0x00AA']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: '=.=', data: ['0x0000', '0x00AA']},
    {name: 'Data_OutR[15:0]', wave: '=..', data: ['0x0000']},
    {name: 'MMR',             wave: '0..'},
    {name: 'MUX MR out',      wave: '=.=', data: ['0x0000', '0x00AA']},
  ],
  {},
  ['I/O (idle)',
    {name: 'D_Word[15:0]', wave: '=..', data: ['0x0000']},
    {name: 'LD[7:0]',      wave: '=..', data: ['0x00']},
    {name: 'SW[7:0]',      wave: '=..', data: ['0x00']},
    {name: 'BTN[5:1]',     wave: '=..', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
```

> [!note]- Why MMR stays low and the I/O signals stay quiet
> `0x45 = 01000101` → bits(7:3) = `01000`, not `11111`. So `MMR = 0`, MUX MR forwards Data\_OutM, port registers MR0-MR7 are not addressed. D\_Word, LEDs, button-latched MRs are inert. The write at C2 latches into RAM; the read at C3 returns the freshly written `0x00AA`.

---

### B.- Write 0x55 → 0xF8, Read 0xF8

> [!example] Sequence B — write to MR0 (D\_Word low byte), then read it back
>
> | Signal | Cycle 1: Write 0x55 → 0xF8 | Cycle 2: Read 0xF8 |
> |---|---|---|
> | Address | `0xF8` | `0xF8` |
> | MW | **1** | 0 |
> | Data\_In | `0xXX55` | XXXX |
> | Data\_OutM | M\[0xF8\] (RAM index, unused) | M\[0xF8\] (unused) |
> | Data\_OutR | `0x0000` (MR0 still old) | **`0x0055`** |
> | MMR | **1** | **1** |
> | MUX MR out | `0x0000` (selects Data\_OutR) | **`0x0055`** |
> | D\_Word (MR1:MR0) | `0x0000` | **`0x0055`** |
> | LD1-8 | `0x00` (MR2 unchanged) | `0x00` |
> | SW1-8 | `0x00` | `0x00` |
> | BTN1-5 | 00000 | 00000 |
>
```wavedrom
{signal: [
  {name: 'clk',             wave: 'p.'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=.', data: ['0xF8']},
    {name: 'MW',            wave: '10'},
    {name: 'Data_In[15:0]', wave: '=x', data: ['0x0055']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: 'xx'},
    {name: 'Data_OutR[15:0]', wave: '==', data: ['0x0000', '0x0055']},
    {name: 'MMR',             wave: '1.'},
    {name: 'MUX MR out',      wave: '==', data: ['0x0000', '0x0055']},
  ],
  {},
  ['Port register / I/O',
    {name: 'MR0 (internal)',  wave: '==', data: ['0x00', '0x55']},
    {name: 'D_Word[15:0]',    wave: '==', data: ['0x0000', '0x0055']},
    {name: 'LD[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'SW[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'BTN[5:1]',        wave: '=.', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
```

> [!note]- What changes physically on the board
> - `0xF8 = 11111000` → bits(7:3) = `11111`, so `MMR = 1` for both cycles.
> - During C1, `MW = 1` and `Address(2:0) = "000"` ⇒ `MR0 ← Data_In(7:0) = 0x55` on the rising edge.
> - From C2 onward, `Data_OutR = 0x00 & MR0 = 0x0055`. MUX MR forwards it because MMR=1.
> - `D_Word = MR1 & MR0 = 0x00 & 0x55 = 0x0055`, so the four-digit 7-seg shows "0055".

---

### C.- Write 0xCC → 0xFC, Read 0xFC

> [!example] Sequence C — `0xFC = MR4` is **read-only** from the CPU. The write is silently ignored.
>
> | Signal | Cycle 1: Write 0xCC → 0xFC | Cycle 2: Read 0xFC |
> |---|---|---|
> | Address | `0xFC` | `0xFC` |
> | MW | **1** | 0 |
> | Data\_In | `0xXXCC` | XXXX |
> | Data\_OutM | (unused) | (unused) |
> | Data\_OutR | `0x00` & MR4 = **`0x0000`** | **`0x0000`** |
> | MMR | **1** | **1** |
> | MUX MR out | `0x0000` | `0x0000` |
> | D\_Word | `0x0000` | `0x0000` |
> | LD1-8 | `0x00` | `0x00` |
> | SW1-8 | `0x00` | `0x00` |
> | BTN1-5 | 00000 | 00000 |
>
```wavedrom
{signal: [
  {name: 'clk',             wave: 'p.'},
  {},
  ['Bus',
    {name: 'Address[7:0]',  wave: '=.', data: ['0xFC']},
    {name: 'MW',            wave: '10'},
    {name: 'Data_In[15:0]', wave: '=x', data: ['0x00CC']},
  ],
  {},
  ['Memory output',
    {name: 'Data_OutM[15:0]', wave: 'xx'},
    {name: 'Data_OutR[15:0]', wave: '=.', data: ['0x0000']},
    {name: 'MMR',             wave: '1.'},
    {name: 'MUX MR out',      wave: '=.', data: ['0x0000']},
  ],
  {},
  ['Port register / I/O',
    {name: 'MR4 (read-only)', wave: '=.', data: ['0x00 (write ignored)']},
    {name: 'D_Word[15:0]',    wave: '=.', data: ['0x0000']},
    {name: 'LD[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'SW[7:0]',         wave: '=.', data: ['0x00']},
    {name: 'BTN[5:1]',        wave: '=.', data: ['00000']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
```

> [!note]- Why the write does nothing
> In `PortReg8x8.vhd` the synchronous-write case statement only matches `Address(2:0)` = `"000"`, `"001"`, `"010"` (MR0, MR1, MR2). Address `0xFC` has `(2:0) = "100"` (MR4) which falls into `when others => null`. So even with `MW=1` and `MMR=1`, MR4 keeps its initial `0x00`. The read in C2 simply mirrors this through Data\_OutR.

---

### D.- Set SW = 0xA5, Push BTNL, then Repeat C

> [!example] Sequence D — SW + BTNL latches `MR4`, **then** the read-only path actually returns useful data
>
> | Signal | Cyc 1: SW=A5, BTNL=1 | Cyc 2: BTNL=0 (settle) | Cyc 3: Write 0xCC → 0xFC | Cyc 4: Read 0xFC |
> |---|---|---|---|---|
> | Address | XX (no CPU access) | XX | `0xFC` | `0xFC` |
> | MW | 0 | 0 | **1** | 0 |
> | Data\_In | — | — | `0xXXCC` | XXXX |
> | SW1-8 | **`0xA5`** | `0xA5` | `0xA5` | `0xA5` |
> | BTN1-5 | 00**1**00 (BTNL) | 00000 | 00000 | 00000 |
> | MR4 (internal) | **`0xA5`** (latched) | `0xA5` | `0xA5` (write ignored) | `0xA5` |
> | Data\_OutM | — | — | (unused) | (unused) |
> | Data\_OutR | (depends on Addr) | — | `0x0000` (MR4 not yet on bus) | **`0x00A5`** |
> | MMR | (Addr-dependent) | — | **1** | **1** |
> | MUX MR out | — | — | `0x00A5` (already latched) | **`0x00A5`** |
> | D\_Word | `0x0000` | `0x0000` | `0x0000` | `0x0000` |
> | LD1-8 | `0x00` | `0x00` | `0x00` | `0x00` |
>
```wavedrom
{signal: [
  {name: 'clk',             wave: 'p...'},
  {},
  ['User input',
    {name: 'SW[7:0]',       wave: '=...', data: ['0xA5']},
    {name: 'BTNL',          wave: '10..'},
    {name: 'BTN others',    wave: '0...'},
  ],
  {},
  ['CPU bus (idle in C1-C2, active in C3-C4)',
    {name: 'Address[7:0]',  wave: 'x.=.', data: ['0xFC']},
    {name: 'MW',            wave: '0.10'},
    {name: 'Data_In[15:0]', wave: 'x.=x', data: ['0x00CC']},
  ],
  {},
  ['Memory output',
    {name: 'MR4 (internal)',  wave: '==..', data: ['0x00', '0xA5']},
    {name: 'Data_OutR[15:0]', wave: 'x.=.', data: ['0x00A5']},
    {name: 'MMR',             wave: '0.1.'},
    {name: 'MUX MR out',      wave: 'x.=.', data: ['0x00A5']},
  ],
  {},
  ['I/O',
    {name: 'D_Word[15:0]', wave: '=...', data: ['0x0000']},
    {name: 'LD[7:0]',      wave: '=...', data: ['0x00']},
  ],
],
 config: {hscale: 2},
 head: {tick: 1}}
```

> [!note]- Key observation — read-only ports are not write-protected, they're button-loaded
> The MR3-MR7 registers track SW1-8 while their corresponding button is held (`if BTNL='1' then MR4 <= SW`). So in C1, with BTNL=1 and SW=`0xA5`, MR4 is loaded with `0xA5` on the next rising edge. After BTNL is released, MR4 keeps that value indefinitely.
>
> The write to `0xFC` in C3 still does nothing for the same reason as Sequence C — but now the *read* in C4 returns `0x00A5` instead of `0x0000`, because that's what was latched from the switches earlier. This is exactly how the PWF microprocessor takes operand input: set switches, push button, then a `LD` instruction can fetch the operand from the corresponding address.

---

## 10.2 Calculator Program — Add Two Operands

> [!info] Setup (from assignment)
> - Operand 1 has been loaded via SW1-8 + **BTNU** → latched into **MR6** (address `0xFE`).
> - Operand 2 has been loaded via SW1-8 + **BTNL** → latched into **MR4** (address `0xFC`).
> - `R6 = 0xFE`, `R7 = 0xFD` (operand source addresses, as given).
> - `R4 = 0xF8`, `R5 = 0xF9` (display destination addresses: MR0 = D\_Word low, MR1 = D\_Word high).
>
> > [!warning]- Note on R7 = 0xFD vs. BTNL
> > The assignment text says "BTNU and BTNL for the first and second operand" but specifies `R7 = 0xFD`, which is **MR5 (BTND)** rather than MR4 (BTNL = `0xFC`). We follow the explicit register values given (`R7 = 0xFD`), so the second operand source is the BTND latch. Replace BTND with BTNL in the testbench if you want to match the prose verbatim — the program logic is identical.

### A.- RTL Program — Fetch Operands and Add

> [!example] Three-instruction RTL core (operand fetch + add)
>
> | # | RTL micro-operation | PWF assembly | Hex |
> |---|---|---|---|
> | 1 | `R0 ← M[R6]` (= operand 1, from MR6 / BTNU) | `ld D0 A6` | `0x2030` |
> | 2 | `R1 ← M[R7]` (= operand 2, from MR5 / BTND) | `ld D1 A7` | `0x2078` |
> | 3 | `R2 ← R0 + R1` | `add D2 A0 B1` | `0x040A` |

> [!note]- Decoding the hex (16-bit IR layout: `Opcode(7) | DR(3) | SA(3) | SB(3)`)
>
> **`ld D0 A6`** → opcode `0010000`, DR `000`, SA `110`, SB `000` = `0010000 000 110 000` = `0010 0000 0011 0000` = `0x2030`.
> **`ld D1 A7`** → `0010000 001 111 000` = `0010 0000 0111 1000` = `0x2078`.
> **`add D2 A0 B1`** → opcode `0000010`, DR `010`, SA `000`, SB `001` = `0000010 010 000 001` = `0000 0100 0000 1010` = `0x040A`.

### B.- Display the Result on the Seven-Segment

> [!example] Add two store instructions to drive `D_Word`
>
> | # | RTL micro-operation | PWF assembly | Hex |
> |---|---|---|---|
> | 4 | `M[R4] ← R2` (MR0 ← sum, low byte of D\_Word) | `st A4 B2` | `0x4022` |
> | 5 | `M[R5] ← R0` *(optional: clear high byte if R0 known to be ≤ 0xFF; safest is to write a known-zero register — see note)* | `st A5 B0` | `0x4028` |
>
> The complete program:
>
> ```asm
> ; --- 62711 Calculator: R2 = R0 + R1, displayed on 7-seg ---
> ld  D0 A6     ; R0 <- M[R6] = M[0xFE] = operand 1 (BTNU/MR6)
> ld  D1 A7     ; R1 <- M[R7] = M[0xFD] = operand 2 (BTND/MR5)
> add D2 A0 B1  ; R2 <- R0 + R1     (8-bit sum, carry on FU C flag)
> st  A4 B2     ; M[R4] = MR0 <- R2  -> D_Word(7:0)  = sum  (visible on low 7-seg digits)
> st  A5 B0     ; M[R5] = MR1 <- R0  (high byte; replace with a zeroed register if needed)
> ```

> [!note]- Why the sum still fits — and what about the carry?
> Each operand is 8 bits, so `R2 = R0 + R1` can produce a 9-bit result. The Datapath (PWA) raises the C flag in this case but the register file only stores 8 bits. We keep the visible result as the low 8 bits (MR0). To also show the carry, you can branch on the C flag and set MR1 ← `0x01`; that requires an extra `BRC`/conditional store which is outside the scope of this exercise.
>
> If `R0` is not already zero after the LDs, prefer to load 0 explicitly into a scratch register (`ldi D3` with operand `0`) and store `R3` into MR1.

### B (cont).- Test-Bench and Simulation Walkthrough

> [!example] Komplet VHDL test-bench
>
> ```vhdl
> library IEEE;
> use IEEE.STD_LOGIC_1164.ALL;
>
> entity Calculator_tb is end Calculator_tb;
>
> architecture TB of Calculator_tb is
>     signal CLK    : STD_LOGIC := '0';
>     signal RESET  : STD_LOGIC := '1';
>     signal SW     : STD_LOGIC_VECTOR(7 downto 0) := (others => '0');
>     signal BTNC, BTNU, BTNL, BTNR, BTND : STD_LOGIC := '0';
>     signal LED    : STD_LOGIC_VECTOR(7 downto 0);
>     signal D_Word : STD_LOGIC_VECTOR(15 downto 0);
>     constant T : time := 10 ns;   -- klokperiode (100 MHz)
> begin
>     UUT: entity work.Microprocessor port map (
>         CLK=>CLK, RESET=>RESET, SW=>SW,
>         BTNC=>BTNC, BTNU=>BTNU, BTNL=>BTNL, BTNR=>BTNR, BTND=>BTND,
>         LED=>LED, D_Word=>D_Word);
>
>     clk_gen: process begin
>         CLK <= '0'; wait for T/2;
>         CLK <= '1'; wait for T/2;
>     end process;
>
>     stim: process begin
>         -- Hold reset i 2 cykler, slip derefter
>         RESET <= '1'; wait for 2*T; RESET <= '0';
>
>         -- Indlæs operand 1 = 0x12 via BTNU  -> MR6 (0xFE)
>         SW <= x"12"; BTNU <= '1'; wait for T;
>         BTNU <= '0';              wait for 2*T;
>
>         -- Indlæs operand 2 = 0x34 via BTND  -> MR5 (0xFD)
>         SW <= x"34"; BTND <= '1'; wait for T;
>         BTND <= '0';              wait for 2*T;
>
>         -- Lad CPU'en køre de 5 instruktioner
>         wait for 30*T;
>
>         -- Verificér resultatet på 7-segment
>         assert D_Word(7 downto 0) = x"46"
>             report "Sum skal være 0x46" severity error;
>
>         report "Calculator_tb: FÆRDIG" severity note;
>         wait;
>     end process;
> end TB;
> ```
>
> Simulerings-tidslinje (de centrale overgange i bølgeformen):
>
> | Phase | Stimulus | What to observe | Expected |
> |---|---|---|---|
> | T0 | reset asserted | `PC=0x00`, all `Rn=0x00`, all `MRn=0x00` | clean state |
> | T1 | `SW=0x12`, `BTNU=1` for one cycle | `MR6 ← 0x12` on rising edge while BTNU=1 | `MR6 = 0x12` |
> | T2 | `SW=0x34`, `BTND=1` for one cycle | `MR5 ← 0x34` | `MR5 = 0x34` |
> | T3 | First `ld D0 A6` executes | Address=`0xFE`, `MMR=1`, MUX MR=`0x0012` → `R0 = 0x12` | `R0 = 0x12` |
> | T4 | `ld D1 A7` executes | Address=`0xFD`, `MMR=1`, MUX MR=`0x0034` → `R1 = 0x34` | `R1 = 0x34` |
> | T5 | `add D2 A0 B1` | Function unit `FS=0010`, `R2 ← R0 + R1` | `R2 = 0x46`, C/V/N/Z flags set accordingly |
> | T6 | `st A4 B2` | Address=`0xF8`, `MW=1`, `MMR=1` ⇒ `MR0 ← 0x46` | `MR0 = 0x46`, `D_Word = 0x0046` |
> | T7 | `st A5 B0` | Address=`0xF9`, `MW=1` ⇒ `MR1 ← R0 = 0x12` *(or 0 with scratch reg)* | `D_Word = 0x1246` *(low digit pair "46" is the sum)* |
>
```wavedrom
{signal: [
  {name: 'clk',             wave: 'p.......'},
  {},
  ['Operand input (user)',
    {name: 'SW[7:0]',       wave: '==......', data: ['0x12', '0x34']},
    {name: 'BTNU',          wave: '10......'},
    {name: 'BTND',          wave: '010.....'},
  ],
  {},
  ['CPU bus (per instruction phase)',
    {name: 'Phase',         wave: '========', data: ['BTNU', 'BTND', 'ld A6', 'ld A7', 'add', 'st A4', 'st A5', 'done']},
    {name: 'Address[7:0]',  wave: 'xx==x==x', data: ['0xFE', '0xFD', '0xF8', '0xF9']},
    {name: 'MW',            wave: '0....1.0'},
    {name: 'Data_In[15:0]', wave: 'xxxxx==x', data: ['0x0046', '0x0012']},
    {name: 'MMR',           wave: '0.1.01.0'},
    {name: 'MUX MR out',    wave: 'x.==xxxx', data: ['0x0012', '0x0034']},
  ],
  {},
  ['Port registers',
    {name: 'MR6 (BTNU)',    wave: '==......', data: ['0x00', '0x12']},
    {name: 'MR5 (BTND)',    wave: '=.=.....', data: ['0x00', '0x34']},
    {name: 'MR0 (D_Word lo)', wave: '=.....=.', data: ['0x00', '0x46']},
    {name: 'MR1 (D_Word hi)', wave: '=......=', data: ['0x00', '0x12']},
  ],
  {},
  ['CPU registers',
    {name: 'R0', wave: '=..=....', data: ['0x00', '0x12']},
    {name: 'R1', wave: '=...=...', data: ['0x00', '0x34']},
    {name: 'R2', wave: '=....=..', data: ['0x00', '0x46']},
  ],
  {},
  {name: 'D_Word[15:0]', wave: '=.....==', data: ['0x0000', '0x0046', '0x1246']},
],
 config: {hscale: 2},
 head: {tick: 1},
 foot: {text: 'Each slot abstracts one PWF instruction (= 2 clock cycles: INF + EX0)'}}
```

> [!note]- How the timing diagram explains the program
> 1. **Operand latching is asynchronous to the CPU.** Pushing BTNU loads MR6 from the switches independently of whatever instruction the CPU is executing — that's what makes the buttons usable as input ports.
> 2. **Each `ld` is a memory-mapped read.** Address goes onto the bus, MMR rises (`Address ≥ 0xF8`), MUX MR routes Data\_OutR (= zero-extended MRn) into the Datapath, and MD=1 routes that into the destination register.
> 3. **`add` uses only the function unit** — no memory access, MMR can be anything, MW=0.
> 4. **Each `st` is a memory-mapped write.** Address goes out, MW=1, Data\_In on the bus carries R2 / R0 in the low byte. PortReg8x8 latches the low byte into MR0 / MR1 because Address(2:0) matches "000" / "001".
> 5. **D\_Word updates as soon as MR0/MR1 change.** The 7-seg driver clocks them out; the assertion at the end verifies the result combinationally from the simulation observer.

---

## 10.3 Quick-Reference Summary

> [!tldr] Key takeaways from this exercise
>
> | Topic | One-liner |
> |---|---|
> | Address decoding | `MMR = 1` ⇔ `Address(7:3) = "11111"`, i.e. the top 8 addresses select port registers. |
> | Read-only ports (MR3-MR7) | Writes are silently dropped; values come from SW latched on the matching button. |
> | MUX MR | Selects `Data_OutR` when `MMR=1`, otherwise forwards `Data_OutM` (RAM). |
> | D\_Word | 16-bit concatenation `MR1 & MR0` driving the 4-digit 7-seg display. |
> | Calculator pattern | `LD operand1, LD operand2, ADD, ST result` — four instructions for any binary operation. |
> | Testbench philosophy | Drive SW + buttons to load operands, then let the CPU run; verify by sampling the MR registers / D\_Word. |

---

> [!nav]
> [[Opg 5 - Datapath & MPC Control|← Opg 5]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
