---
course: "62711"
course-name: "Digital Systems Design"
type: tool-docs
tags: [DSD, PWF, tool, assembler]
---
# dsdasm — PWF Assembler Tool

> [!info] Tool Info
> **What it is:** Custom Python assembler/disassembler/simulator for the PWF microprocessor, written as a streamlined replacement for the Java `Assembler_vX.jar`.
> **File:** [`PWF/tools/asm/dsdasm.py`](https://github.com/gigurd/Design-of-digital-systems-62711/blob/main/PWF/tools/asm/dsdasm.py)
> **Dependencies:** Python 3.8+ standard library only (no pip install)
> **Self-test:** `python dsdasm.py test` → `PASS: 20/20` against PWF spec table

---

## Why not just use the Java tool?

| | Java `Assembler_vX.jar` | **dsdasm.py** |
|---|---|---|
| Runtime | Needs Java JRE | Python 3 stdlib only |
| Whitespace | Breaks silently on 2+ spaces | Any whitespace works |
| Errors | Silently zeros operands | Clear error with line number |
| Labels | Manual address counting | `loop:` / `jmp loop` |
| Comments | Not supported | `;` or `#` |
| Immediates | Decimal only | `42`, `0x2A`, `0b101010` |
| Output | Copy-paste hex into Vivado | **Directly patches** `Ram256x16.vhd` |
| Testing | Run on FPGA | Built-in step simulator |
| Debugging | Waveforms only | Disassembler + trace |
| AND/OR bug | Produces wrong code ⚠️ | Matches our PWB |

> [!warning] AND/OR bug in the Java tool
> The Java reference assembler and lecture-10 slide 9 use `0001000 = AND`, `0001001 = OR`. **Our PWF spec and [[InstructionDecoderController|InstructionDecoderController]] use the opposite** (`0001000 = OR`, `0001001 = AND`). If you assemble `and R0 R1 R2` with the Java tool and run it on our hardware, you get OR behavior — silent bug.
> `dsdasm` matches the PWF spec and PWB (the hardware is authoritative). Use `dsdasm` over the Java tool.

---

## Quick Start

From the team repo root:

```bash
cd PWF/tools/asm

# GUI (recommended for day-to-day work)
python dsdasm_gui.py

# GUI with a file already open
python dsdasm_gui.py examples/countdown.asm

# CLI — useful for CI, scripts, or headless work
python dsdasm.py test                                        # self-test
python dsdasm.py asm examples/countdown.asm --vhdl ../../sources/hdl/Ram256x16.vhd
python dsdasm.py run examples/countdown.asm --trace
```

---

## GUI (`dsdasm_gui.py`)

A Tkinter frontend wrapping the same `dsdasm` module — zero additional dependencies.

```
┌─────────────────────────────────────────────────────────────┐
│ Open  Save │ Assemble  Patch VHDL │ Reset  Step  Run │ idle │
├──────────────────────────────────────┬──────────────────────┤
│  Editor (syntax hi + line nums)      │ Registers  R0..R7    │
│                                      │ PC   V=0 C=0 N=0 Z=0 │
│  loop:                               ├──────────────────────┤
│    dec  R1, R1        ← PC hi-lit    │ Memory (256 words)   │
│    brz  R1, halt                     │ 03:0C48 dec R1,R1    │
│                                      │ 04:C009 brz R1,+1    │
├──────────────────────────────────────┴──────────────────────┤
│ 7-seg:  F 0 0 A    LEDs: ●○●●○○●●                           │
│                    SW:   ▢▣▢▣▢▢▣▢   Buttons:  [U][L][C][R][D]│
├─────────────────────────────────────────────────────────────┤
│ Console                                                     │
│ line 4: offset out of range: 99 (valid -4..+3)              │
└─────────────────────────────────────────────────────────────┘
```

**Panes:**

| Area | Purpose |
|---|---|
| Editor | Syntax-highlighted .asm editing with line numbers, current-PC highlight, and red underline on assembly errors |
| Registers | Live view of R0..R7, PC, and V/C/N/Z flags |
| Memory | All 256 words with disassembled mnemonic. The I/O rows (`0xF8..0xFF`) show the current MR values. The active PC row is highlighted |
| Nexys 4 DDR | 4-digit 7-seg (shows D_Word = MR1:MR0), 8 LEDs (MR2), 8 clickable switches (SW), and the 5 buttons in physical cross layout |
| Console | Results, errors (with **clickable line-N links** that jump the editor to the failing line), sim messages |

**Keyboard shortcuts:**

| Shortcut | Action |
|---|---|
| `Ctrl+N` / `Ctrl+O` / `Ctrl+S` | New / Open / Save |
| `F5` | Assemble (underlines errors, auto-resets CPU) |
| `F10` | Single-step the simulator |
| `F9` | Run / Pause |
| `Ctrl+R` | Reset the simulator (keeps SW state and MR registers) |

**Interacting with the board:**

- **Click a switch** → toggles the corresponding bit in `cpu.sw` (mirrors the physical slide switches)
- **Click a button** → latches the current SW pattern into the corresponding `MR` register, exactly like the physical board (BTNR→MR3, BTNL→MR4, BTND→MR5, BTNU→MR6, BTNC→MR7)
- LEDs and 7-seg update live as the program writes to `0xFA`, `0xF9`, `0xF8`

**Typical workflow:**

1. Open `examples/countdown.asm` → F5 to assemble (labels + word count in console)
2. F10 to step, watch R1 decrement in the register pane and the PC row move in the memory view
3. F9 to run to halt — status bar shows `halted`
4. Click switches + BTNR to seed MR3 for an interactive program
5. `Build → Patch VHDL…` → pick `Ram256x16.vhd` → ready to re-synth

---

## Syntax

### Registers

Always written as `R0` … `R7` (case-insensitive). Position in the instruction determines role — no need for the old `D0 / A1 / B2` prefixes.

```
mova R0 R1        ; R0 <- R1   (R0 = destination, R1 = source)
add  R0 R1 R2     ; R0 <- R1 + R2
st   R0 R1        ; M[R0] <- R1   (R0 = address, R1 = data)
```

> **Don't use R8 / R9** — they're reserved by `LRI`, `SRM`, `SLM` as scratch.

### Immediates

Decimal, hex (`0x`), or binary (`0b`). Also accepts negative for branch offsets.

```
ldi  R0, 7        ; 7 decimal
ldi  R0, 0x05     ; hex
ldi  R0, 0b111    ; binary
brz  R0, -2       ; signed offset
```

Range: immediates `0..7` (3 bits), offsets `-4..+3` (3-bit signed).

### Comments

`;` or `#` — everything after is ignored.

```
inc R0 R1         ; this is a comment
add R2 R3 R4      # so is this
```

### Labels

Any identifier followed by `:`. Labels resolve to instruction addresses.

```
loop:
    dec  R1, R1
    brz  R1, done    ; resolves to signed offset
    jmp  R0          ; R0 pre-loaded with loop's address

done:
    jmp  R7          ; R7 = self address → halt
```

Labels work in three places:
- `brz` / `brn` — computed as signed PC-relative offset
- `ldi` — resolved as **absolute** address (must fit in 0..7)
- `.word` — raw address value

### The `.word` directive

Emits a raw 16-bit value. Useful for embedding constants for `LD` to read:

```
leds_addr:
    .word 0xFA        ; physical address of MR2 (LED register)

start:
    ldi  R0, leds_addr   ; R0 = address where 0xFA is stored
    ld   R1, R0          ; R1 = 0xFA  (now R1 points at the LEDs)
    ...
```

This is the standard workaround for the 3-bit LDI limit when you need to poke memory-mapped I/O addresses like `0xFA` / `0xFB` / ….

### Halt convention

The simulator (and a running FPGA) stop when `jmp R_x` targets the same address as the jmp itself (`R_x == PC`). Pattern:

```
    ldi R7, halt     ; preload R7 with halt's address (must be 0..7)

halt:
    jmp R7           ; jmp-to-self → halt
```

---

## Commands

### `asm` — assemble

```bash
python dsdasm.py asm <file.asm> [flags]
```

| Flag | Effect |
|---|---|
| `-o file.hex` | Write flat hex (one 16-bit word per line) |
| `--bram file.bram` | Write BRAM-packed format (64-char lines, for manual Vivado paste) |
| `--vhdl Ram256x16.vhd` | **Inject `INIT_00`…`INIT_0F` generics directly** into the RAM module |
| `--labels` | Print the symbol table to stderr |
| *(none)* | Print flat hex to stdout |

**VHDL injection is idempotent** — safe to run repeatedly. It looks for the markers:

```vhdl
-- PROGRAM_INIT_BEGIN (managed by dsdasm.py -- do not edit by hand)
...generated INIT lines...
-- PROGRAM_INIT_END
```

If the markers don't exist, `dsdasm` inserts them right after the `INIT => X"0000",` line in the `BRAM_SINGLE_MACRO` generic map. On subsequent runs the content between the markers is regenerated.

### `dasm` — disassemble

```bash
python dsdasm.py dasm <file.hex>
```

Reads any file with 4-char hex words (flat or BRAM-packed order — only flat round-trips cleanly) and prints:

```
00:  0x9803  ldi   R0, 3
01:  0x99C6  ldi   R7, 6
02:  0x9847  ldi   R1, 7
03:  0x0C48  dec   R1, R1
04:  0xC009  brz   R1, +1
...
```

### `run` — simulate

```bash
python dsdasm.py run <file.asm> [flags]
```

| Flag | Effect |
|---|---|
| `--trace` | Print CPU state after each step |
| `--switches 0xA5` | Set physical switch value (8-bit) |
| `--press BTNR` | Simulate a button press (latches SW → MR) — repeatable |
| `--max-steps 10000` | Safety limit for infinite loops (default 10000) |

Prints final register file, flag state, all `MR0..MR7`, the LED pattern, and the 7-seg `D_Word`. Simulator models:

- 8 general registers + R8/R9 scratch
- 256-word memory with memory-mapped I/O at `0xF8..0xFF`
- Button-latched operand registers (BTNR→MR3, BTNL→MR4, BTND→MR5, BTNU→MR6, BTNC→MR7)
- V / C / N / Z flags
- Multi-cycle `LRI`, `SRM`, `SLM` (simplified — executes net effect in one step)

### `test` — self-test

```bash
python dsdasm.py test
```

Assembles a 20-line canonical program (every instruction once) and compares against the PWF spec table byte-for-byte. Should always print `PASS: 20/20`.

---

## Typical Workflow

```bash
# 1. Write a program
vim my_program.asm

# 2. Simulate it
python dsdasm.py run my_program.asm --trace --switches 0xA5 --press BTNR

# 3. Once happy, inject straight into Ram256x16.vhd
python dsdasm.py asm my_program.asm --vhdl ../../sources/hdl/Ram256x16.vhd

# 4. Open Vivado, re-run synthesis → program the board
```

No copy-paste, no counting addresses, no silent operand zeroing.

---

## Example — Countdown Loop

From [`examples/countdown.asm`](https://github.com/gigurd/Design-of-digital-systems-62711/blob/main/PWF/tools/asm/examples/countdown.asm):

```asm
; count R1 from 7 down to 0, then halt.

    ldi  R0, loop       ; R0 <- loop address (3)
    ldi  R7, halt       ; R7 <- halt address (6)
    ldi  R1, 7          ; counter = 7

loop:
    dec  R1, R1         ; R1--
    brz  R1, halt       ; if R1 == 0, branch forward
    jmp  R0             ; else back to loop

halt:
    jmp  R7             ; jmp-to-self → halt
```

Assembles to 7 instructions. Run `python dsdasm.py run examples/countdown.asm --trace` to watch R1 count down and halt.

---

## Full ISA Reference

> The encoding below matches our PWF spec and PWB `InstructionDecoderController`.

| Mnemonic | Opcode | Operands | Effect |
|---|---|---|---|
| `MOVA` | `0000000` | `Rd, Rs` | `Rd ← Rs` |
| `INC` | `0000001` | `Rd, Rs` | `Rd ← Rs + 1` |
| `ADD` | `0000010` | `Rd, Rs, Rt` | `Rd ← Rs + Rt` |
| `SUB` | `0000101` | `Rd, Rs, Rt` | `Rd ← Rs - Rt` |
| `DEC` | `0000110` | `Rd, Rs` | `Rd ← Rs - 1` |
| `OR` | `0001000` | `Rd, Rs, Rt` | `Rd ← Rs OR Rt` |
| `AND` | `0001001` | `Rd, Rs, Rt` | `Rd ← Rs AND Rt` |
| `XOR` | `0001010` | `Rd, Rs, Rt` | `Rd ← Rs XOR Rt` |
| `NOT` | `0001011` | `Rd, Rs` | `Rd ← NOT Rs` |
| `MOVB` | `0001100` | `Rd, Rt` | `Rd ← Rt` |
| `LD` | `0010000` | `Rd, Rs` | `Rd ← M[Rs]` |
| `ST` | `0100000` | `Rs, Rt` | `M[Rs] ← Rt` |
| `LDI` | `1001100` | `Rd, imm` | `Rd ← zf(imm)` (imm 0..7) |
| `ADI` | `1000010` | `Rd, Rs, imm` | `Rd ← Rs + zf(imm)` |
| `BRZ` | `1100000` | `Rs, off` | if Z then `PC ← PC+1+se(off)` |
| `BRN` | `1100001` | `Rs, off` | if N then `PC ← PC+1+se(off)` |
| `JMP` | `1110000` | `Rs` | `PC ← Rs` |
| `LRI` | `0010001` | `Rd, Rs` | `Rd ← M[M[Rs]]` (uses R8) |
| `SRM` | `0001101` | `Rs` | `Rs ← Rs >> R9` (uses R8/R9) |
| `SLM` | `0001110` | `Rs` | `Rs ← Rs << R9` (uses R8/R9) |

**Instruction word layout:**

```
 15       9 | 8 6 | 5 3 | 2 0
┌──────────┬─────┬─────┬─────┐
│  opcode  │ Rd  │ Rs  │ Rt/ │
│  7 bits  │ 3 b │ 3 b │ imm │
└──────────┴─────┴─────┴─────┘
```

---

> [!nav]
> [[PWF Project|← PWF Project]]
>
> [[62711 Digital Systems Design|62711 Home]]
