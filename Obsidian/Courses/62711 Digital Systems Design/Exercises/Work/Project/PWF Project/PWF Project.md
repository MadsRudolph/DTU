---
course: "62711"
course-name: "Digital Systems Design"
type: project
tags: [DSD, PWF, project]
---
# PWF Project -- Microprocessor System

> [!info] Project Info
> **Phase:** PWF (Project Work F) -- Final project
> **Goal:** Design, implement and test a complete microprocessor system by combining the Datapath (PWA) and Microprogram Controller (PWB) with RAM, Port Register and a microcode program
> **Deadline:** 17-05-2026 (Week 20)
> **Spec:** [[62711_ProjectWork_F_F2026.pdf|PWF Project Assignment]]
> **Repo:** [GitHub](https://github.com/gigurd/Design-of-digital-systems-62711) &mdash; `team/PWF/`
> **Previous:** [[PWB Project]]

---

## Top-Level Hierarchy

```
TOP_MODUL_F                       Board wrapper for Nexys 4 DDR
├── Microprocessor                Core CPU system
│   ├── Datapath                  from PWA (register file + FU)
│   ├── MicroprogramController    from PWB (PC + IR + IDC + SE + ZF)
│   ├── Ram256x16                 256 x 16-bit Block RAM (program + data)
│   ├── PortReg8x8                8 x 8-bit port registers (I/O mapped)
│   └── MUX_MR                    Selects RAM vs Port Register output
└── SevenSegDriver                4-digit multiplexed hex display
```

---

## Memory Map

The address bus is 8 bits, giving 256 addresses. The space is split between RAM (248 addresses) and port-register segment (8 addresses).

| Address | Name | Access | Function |
|---------|------|--------|----------|
| `0x00` -- `0xF7` | RAM | R/W | 248 words of program/data |
| `0xF8` | MR0 | R/W | `D_Word` low byte -- 7-seg low |
| `0xF9` | MR1 | R/W | `D_Word` high byte -- 7-seg high |
| `0xFA` | MR2 | R/W | LED0..LED7 |
| `0xFB` | MR3 | R | Operand loaded on BTNR press |
| `0xFC` | MR4 | R | Operand loaded on BTNL press |
| `0xFD` | MR5 | R | Operand loaded on BTND press |
| `0xFE` | MR6 | R | Operand loaded on BTNU press |
| `0xFF` | MR7 | R | Operand loaded on BTNC press |

The `MMR` signal is high when `Address_in` is in the range `0xF8..0xFF` and selects the Port Register output on the output MUX.

---

## Team Split

| Pair | Members | Modules |
|------|---------|---------|
| Pair 1 | TBD | Ram256x16, PortReg8x8 |
| Pair 2 | TBD | MUX_MR, Microprocessor, TOP_MODUL_F, SevenSegDriver |
| Joint | All | Microcode program, testing, report |

---

## Table of Contents

### 1. RAM

256 x 16-bit single-port Block RAM using the Xilinx Artix-7 `BRAM_SINGLE_MACRO` primitive. Holds the program and data segment (addresses `0x00..0xF7`).

| # | Module | File | Page |
|---|--------|------|------|
| 1.0 | **Ram256x16** | `Ram256x16.vhd` | [[Ram256x16]] |

### 2. Port Register

8 x 8-bit port registers mapping the Nexys 4 DDR peripherals (switches, buttons, LEDs, 7-seg) into the microprocessor's memory space at addresses `0xF8..0xFF`.

| # | Module | File | Page |
|---|--------|------|------|
| 2.0 | **PortReg8x8** | `PortReg8x8.vhd` | [[PortReg8x8]] |

### 3. MUX MR

16-bit 2:1 multiplexer that selects between the RAM output (`MMR=0`) and the Port Register output (`MMR=1`). Drives the common data bus to the CPU.

| # | Module | File | Page |
|---|--------|------|------|
| 3.0 | **MUX_MR** | `MUX_MR.vhd` | [[MUX_MR]] |

### 4. Seven-Segment Driver

Time-multiplexed driver for the 4-digit hex display on the Nexys 4 DDR. Shows `D_Word` (MR1:MR0) as 4 hex digits.

| # | Module | File | Page |
|---|--------|------|------|
| 4.0 | **SevenSegDriver** | `SevenSegDriver.vhd` | [[SevenSegDriver]] |

### 5. Microprocessor (Core)

Structural top-level wiring the PWA Datapath, PWB MicroprogramController, RAM, Port Register and MUX MR into a complete CPU.

| # | Module | File | Page |
|---|--------|------|------|
| 5.0 | **Microprocessor** | `Microprocessor.vhd` | [[Microprocessor]] |

### 6. Board-Level Top

Wraps the Microprocessor core and the Seven-Segment Driver, mapping signals to the physical pins on the Nexys 4 DDR board via the constraint file.

| # | Module | File | Page |
|---|--------|------|------|
| 6.0 | **TOP_MODUL_F** | `TOP_MODUL_F.vhd` | [[TOP_MODUL_F]] |

### 7. Microcode Program

A small assembly program loaded into RAM that reads operands from the button-triggered input registers, performs a computation (e.g. addition), and writes the result to the LED / 7-seg output registers.

Assembled using [[dsdasm|dsdasm]] — our custom Python assembler (replaces the Java `Assembler_vX.jar`).

### 8. Tooling

| # | Tool | Purpose | Page |
|---|--------|------|------|
| 8.0 | **dsdasm** | Assembler / disassembler / simulator — converts `.asm` → `INIT_xx` in `Ram256x16.vhd` | [[dsdasm]] |

---

## Instruction Set (reused from PWB)

| Opcode | Mnemonic | Operation | Cycles |
|--------|----------|-----------|--------|
| 0000000 | MOVA | R[DR] <- R[SA] | 2 |
| 0000001 | INC | R[DR] <- R[SA] + 1 | 2 |
| 0000010 | ADD | R[DR] <- R[SA] + R[SB] | 2 |
| 0000101 | SUB | R[DR] <- R[SA] - R[SB] | 2 |
| 0000110 | DEC | R[DR] <- R[SA] - 1 | 2 |
| 0001000 | OR | R[DR] <- R[SA] OR R[SB] | 2 |
| 0001001 | AND | R[DR] <- R[SA] AND R[SB] | 2 |
| 0001010 | XOR | R[DR] <- R[SA] XOR R[SB] | 2 |
| 0001011 | NOT | R[DR] <- NOT R[SA] | 2 |
| 0001100 | MOVB | R[DR] <- R[SB] | 2 |
| 0010000 | LD | R[DR] <- M[R[SA]] | 2 |
| 0100000 | ST | M[R[SA]] <- R[SB] | 2 |
| 1001100 | LDI | R[DR] <- zf OP | 2 |
| 1000010 | ADI | R[DR] <- R[SA] + zf OP | 2 |
| 1100000 | BRZ | Branch if Z=1 | 2 |
| 1100001 | BRN | Branch if N=1 | 2 |
| 1110000 | JMP | PC <- R[SA] | 2 |
| 0010001 | LRI | Load Register Indirect | 3 |
| 0001101 | SRM | Shift Right Multiple | 5+ |
| 0001110 | SLM | Shift Left Multiple | 5+ |

> R8 and R9 are reserved as scratch registers for the multi-cycle instructions LRI / SRM / SLM.

---

## Signal Flow

```
Instruction_In    ┌─────────────────────────────┐
◄──────────────── │   MicroprogramController    │
                  │   (PC, IR, SE, ZF, IDC)     │
                  └──────┬──────────────┬───────┘
                         │ Address_Out  │ Control word
                         ▼              ▼
                  ┌──────────────────────────────┐
                  │  MUX M (MM=1 PC, 0 DP addr)  │
                  └──────┬───────────────────────┘
                         │ Mem_Address
             ┌───────────┴───────────┐
             ▼                       ▼
       ┌──────────┐            ┌─────────────┐
       │ Ram256x16│            │ PortReg8x8  │
       └─────┬────┘            └─────┬───────┘
             │ Data_outM             │ Data_outR, MMR
             └────────┐    ┌─────────┘
                      ▼    ▼
                    ┌─────────┐
                    │ MUX MR  │  <- MMR
                    └────┬────┘
                         │ Data_Bus_Out (16b)
                         ▼
                  ┌─────────────────┐
                  │    Datapath     │  <- Control word
                  │  (RF + FU)      │
                  └─┬───────────┬───┘
                    │ Data_Out  │ Address_Out
                    ▼           ▼
                  (to Ram/Port) (to MUX M)
```

---

## PWF-Specific Tasks

- [ ] Implement `Ram256x16` using `BRAM_SINGLE_MACRO` primitive  ✅
- [ ] Implement `PortReg8x8` with button-driven input loads
- [ ] Implement `MUX_MR`
- [ ] Implement `SevenSegDriver` with refresh counter
- [ ] Implement `Microprocessor` top-level structural wiring
- [ ] Implement `TOP_MODUL_F` board wrapper
- [ ] Write timing diagrams for RAM and Port Register (report requirement)
- [ ] Write timing diagram for A/B/C/D read/write sequences (report requirement)
- [ ] Design microcode program in register-transfer notation
- [ ] Translate microcode to machine code and load into RAM
- [ ] Simulate program execution in testbench
- [ ] Test program on Nexys 4 DDR hardware
- [ ] Write final combined PWA+PWB+PWF report

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]] | [[PWB Project|<- PWB Project]]
>
> &nbsp;
