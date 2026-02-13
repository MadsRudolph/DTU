# PWA Module Overview

Overview of all VHDL modules in the PWA project and their origin.

## Hierarchy

```
TOP_MODUL (board wrapper)
└── Datapath
    ├── RegisterFile
    │   ├── DestinationDecoder
    │   ├── RegisterR16
    │   │   └── flip_flop (x128)
    │   ├── MUX16x1x8 (A_Data)
    │   └── MUX16x1x8 (B_Data)
    ├── MUX2x1x8 (MUXB: B_Data / ConstantIn)
    ├── FunctionUnit
    │   ├── FunctionSelect (FS3,FS2 → MF)
    │   ├── ALU
    │   │   ├── arithmetic
    │   │   │   ├── b_logic (x8)
    │   │   │   └── full_adder (x8)
    │   │   │       └── half_adder (x2)
    │   │   └── logic_unit
    │   ├── Shifter
    │   ├── MUX2x1x8 (MUXF: ALU / Shifter)
    │   └── NegZero (N, Z flags)
    ├── MUX2x1x8 (MUXD: F / DataIn)
    └── display (7-segment driver)
```

## Modules from the spec

These entities have names and port signatures taken directly from `62711_ProjectWork_A_F2026.pdf`.

| File | Entity | Spec section | Description |
|---|---|---|---|
| `Datapath.vhd` | `Datapath` | p.3, section (4) | Top-level datapath, instantiates RF + FU + MUXB + MUXD |
| `RegisterFile.vhd` | `RegisterFile` | p.1, section (1) | 16x8 Register File wrapper (DD + R16 + 2x MUX16) |
| `DestinationDecoder.vhd` | `DestinationDecoder` | p.1, section (1) | RW + DA(3:0) → LOAD(15:0) one-hot |
| `RegisterR16.vhd` | `RegisterR16` | p.1, section (1) | 16 registers, 8-bit each, structural with flip_flop |
| `MUX16x1x8.vhd` | `MUX16x1x8` | p.1, section (1) | 16-to-1 mux, 8-bit wide, for A_Data/B_Data |
| `FunctionUnit.vhd` | `FunctionUnit` | p.2, section (2) | Wraps ALU + Shifter + Fsel + MUXF + NegZero |
| `FunctionSelect.vhd` | `FunctionSelect` | p.2, section (2) | FS3,FS2 → MF (selects ALU or Shifter output) |
| `ALU.vhd` | `ALU` | p.2, section (2) | Arithmetic + Logic, J_Select(3:0), outputs V and C |
| `Shifter.vhd` | `Shifter` | p.2, section (2) | Shift right / shift left / pass-through on B |
| `MUX2x1x8.vhd` | `MUX2x1x8` | p.2, section (2)+(3) | 2-to-1 mux, 8-bit, used for MUXB, MUXD, MUXF |
| `NegZero.vhd` | `NegZero` | p.2, section (2) | N = sign bit, Z = result is zero |

## Internal building blocks

These are not specified in the project document but are needed as sub-components inside the ALU and RegisterR16. Based on textbook figures and lecture material.

| File | Entity | Used inside | Description |
|---|---|---|---|
| `half_adder.vhd` | `half_adder` | `full_adder` | 2-input adder: S = X xor Y, C = X and Y |
| `full_adder.vhd` | `full_adder` | `arithmetic` | 3-input adder from two half adders |
| `b_logic.vhd` | `b_logic` | `arithmetic` | B input logic, one bit (Figure 8-4) |
| `arithmetic.vhd` | `arithmetic` | `ALU` | n-bit arithmetic circuit (Table 8.1) |
| `logic_unit.vhd` | `logic_unit` | `ALU` | n-bit logic unit, PWA order (OR/AND swapped vs book) |
| `flip_flop.vhd` | `flip_flop` | `RegisterR16` | D-FF with async reset and load enable |

## Board-specific modules

Not part of the PWA spec, but needed for the Nexys 4 DDR board.

| File | Entity | Description |
|---|---|---|
| `TOP_MODUL.vhd` | `TOP_MODUL` | Board-level wrapper (CLK, SW, LED, 7-seg, buttons) |
| `display.vhd` | `display` | 7-segment display driver for board testing |

## Testbench

| File | Entity | Description |
|---|---|---|
| `TOP_MODUL_tb.vhd` | `TOP_MODUL_tb` | Testbench with clock gen and reset sequence |

## Notes

- **PWA logic order is swapped**: OR and AND are in opposite order compared to textbook Table 8.2 (p. 457). In PWA: J1J0 = 00 → OR, 01 → AND.
- **All spec entities are combinatorial** (no process statements) except RegisterR16 which uses processes for register transfer.
- **Flags**: V (overflow = C8 xor C7), C (carry-out C8), N (sign = J7), Z (zero = NOR of all bits).
- **FS encoding**: FS3,FS2 = 00/01 → ALU (MF=0), FS3,FS2 = 10 → logic (MF=0), FS3,FS2 = 11 → Shifter (MF=1).
