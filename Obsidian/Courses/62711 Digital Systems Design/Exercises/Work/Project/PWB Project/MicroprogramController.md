---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, MicroprogramController, structural]
---
# MicroprogramController

> [!info] Module Info
> **Entity:** `MicroprogramController`
> **File:** `MicroprogramController.vhd`
> **Architecture:** `MCU_Behavorial`
> **Spec:** Section (4), p.4

## Purpose

Top-level structural wrapper that wires together the Program Counter, Instruction Register, Sign Extender, Zero Filler, and Instruction Decoder/Controller into the complete Microprogram Controller unit.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset |
| `CLK` | in | 1 | System clock |
| `Address_In` | in | 8 | Jump target address (from Datapath) |
| `Address_Out` | out | 8 | PC output to memory address bus |
| `Instruction_In` | in | 16 | Instruction data from memory |
| `Constant_Out` | out | 8 | Zero-filled immediate constant to Datapath |
| `V, C, N, Z` | in | 1 each | Status flags from Datapath |
| `DX, AX, BX, FS` | out | 4 each | Register addresses and function select to Datapath |
| `MB, MD, RW, MM, MW` | out | 1 each | MUX selectors and write enables |

## Block Diagram

```
CLK ──────────────────────────────────────────────────┐
                                                      │
Address_In ──►┌──────────────────────┐                │
              │   PROGRAM COUNTER    │◄── PS          │
         PC ◄─┤   (1)               │◄── Offset      │
              └──────────────────────┘    (from SE)   │
                                                      │
Instruction_In ──►┌──────────────────────┐            │
                  │  INSTRUCTION         │◄── IL      │
             IR ◄─┤  REGISTER (2)        │            │
                  └────────┬─────────────┘            │
                           │ IR (16 bits)             │
                     ┌─────┴─────┐                    │
                     ▼           ▼                    │
              ┌────────────┐ ┌────────────┐           │
              │ Sign       │ │ Zero       │           │
              │ Extender   │ │ Filler     │──► Constant_Out
              └─────┬──────┘ └────────────┘           │
                    │ Offset (to PC)                  │
                    │                                 │
[V,C,N,Z] ──►┌──────────────────────┐                │
              │  INSTRUCTION DECODER │◄── IR          │
              │  / CONTROLLER (3)    │                │
              └──────────┬───────────┘                │
                         │                            │
          DX AX BX MB FS MD RW MM MW                  │
           │  │  │  │  │  │  │  │  │                  │
           ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                │
```

## Sub-Components

| Instance | Entity | Description |
|----------|--------|-------------|
| `PC_inst` | [[ProgramCounter]] | 8-bit program counter |
| `IR_inst` | [[InstructionRegister]] | 16-bit instruction register |
| `SE_inst` | [[SignExtender]] | Sign extension for branch offset |
| `ZF_inst` | [[ZeroFiller]] | Zero fill for immediate constants |
| `IDC_inst` | [[InstructionDecoderController]] | State machine control logic |

## Internal Signals

| Signal | Width | Connects |
|--------|-------|----------|
| `IR_sig` | 16 | IR output -> SE, ZF, IDC inputs |
| `PS_sig` | 2 | IDC PS output -> PC PS input |
| `IL_sig` | 1 | IDC IL output -> IR IL input |
| `SE_out` | 8 | Sign Extender output -> PC Offset input |
| `ZF_out` | 8 | Zero Filler output -> Constant_Out |

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[InstructionDecoderController]]
>
> &nbsp;
