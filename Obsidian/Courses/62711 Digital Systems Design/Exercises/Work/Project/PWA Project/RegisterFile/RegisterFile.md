---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, structural]
---
# RegisterFile

> [!info] Module Info
> **Entity:** `RegisterFile`
> **File:** `RegisterFile.vhd`
> **Architecture:** `structural`
> **Spec:** Section (1), p.1

## Purpose

Top-level wrapper for the 16x8-bit register file. Provides one write port and two independent read ports (A and B). On the rising clock edge, if RW=1, the register addressed by DA captures D_Data. The read ports are purely combinational -- AA selects which register drives A_Data, BA selects which register drives B_Data.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset, clears all registers |
| `CLK` | in | 1 | Clock, data captured on rising edge |
| `RW` | in | 1 | Register Write enable (1 = write, 0 = hold) |
| `DA` | in | 4 | Destination Address -- selects which register to write |
| `AA` | in | 4 | A Address -- selects register for A_Data output |
| `BA` | in | 4 | B Address -- selects register for B_Data output |
| `D_Data` | in | 8 | Data input to be written |
| `A_Data` | out | 8 | Read port A output |
| `B_Data` | out | 8 | Read port B output |

## Block Diagram

```
         DA + RW
            │
            ▼
    ┌───────────────┐
    │ Destination    │
    │ Decoder        │
    └───────┬───────┘
            │ LOAD(15:0)
            ▼
    ┌───────────────┐
    │               │──── R0..R15 ────┐
    │ RegisterR16   │                 │
    │               │◄── D_Data       │
    └───────────────┘    CLK, RESET   │
            │                         │
       R0..R15                   R0..R15
            │                         │
            ▼                         ▼
    ┌───────────────┐         ┌───────────────┐
    │ MUX16x1x8     │         │ MUX16x1x8     │
    │ (MUX_A)       │         │ (MUX_B)       │
    └───────┬───────┘         └───────┬───────┘
            │ ◄── AA                  │ ◄── BA
            ▼                         ▼
         A_Data                    B_Data
```

## Sub-Components

| Instance | Entity | Description |
|----------|--------|-------------|
| `DD` | [[DestinationDecoder]] | RW + DA -> one-hot LOAD(15:0) |
| `REGS` | [[RegisterR16]] | 16 x 8-bit register block |
| `MUX_A` | [[MUX16x1x8]] | 16:1 mux for A_Data read port |
| `MUX_B` | [[MUX16x1x8]] | 16:1 mux for B_Data read port |

## Testbenches

| File | Description |
|------|-------------|
| `RegisterFile_tb.vhd` | Visual waveform testbench (original) |
| `RegisterFile_tb2.vhd` | Self-checking testbench with 7 assert-based tests |

### RegisterFile_tb2 Test Coverage

| Test | Verifies |
|------|----------|
| 1 | Reset clears all 16 registers to 0x00 |
| 2 | Write unique values to all 16 registers, read back via A and B ports |
| 3 | RW=0 prevents writing (register holds old value) |
| 4 | Simultaneous read of two *different* registers on A and B |
| 5 | Overwrite a register; verify neighbours are unaffected |
| 6 | Reset mid-operation clears all registers |
| 7 | Only the value present at the rising CLK edge is captured |

---

> [!nav]
> &nbsp;
>
> [[PWA Project]] | [[FunctionUnit]]
>
> &nbsp;
