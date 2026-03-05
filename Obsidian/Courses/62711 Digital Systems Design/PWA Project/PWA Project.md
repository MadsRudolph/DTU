---
course: "62711"
course-name: "Digital Systems Design"
type: project
tags: [DSD, PWA, project]
---
# PWA Project -- ALU & Datapath

> [!info] Project Info
> **Phase:** PWA (Project Work A)
> **Goal:** Design and implement the ALU and Register File as part of the Datapath
> **Deadline:** 05-03-2026 (Week 9)
> **Spec:** [[62711_ProjectWork_A_F2026.pdf|PWA Project Assignment]]
> **Repo:** [GitHub](https://github.com/gigurd/Design-of-digital-systems-62711) &mdash; `team/PWA/`

---

## Top-Level Hierarchy

```
Datapath
├── RegisterFile          16x8-bit register file with dual read ports
│   ├── DestinationDecoder    4-to-16 one-hot decoder, gated by RW
│   ├── RegisterR16           16 registers built from flip-flops
│   │   └── Register8bit      8-bit register (MUX + D-FF per bit)
│   │       ├── MUX2x1        2:1 mux for load-enable
│   │       └── flip_flop     D flip-flop with async reset
│   ├── MUX16x1x8 (MUX_A)    16:1 mux for A_Data output
│   └── MUX16x1x8 (MUX_B)    16:1 mux for B_Data output
│
└── FunctionUnit          ALU + Shifter with flag generation
    ├── ALU                   Arithmetic & logic operations
    │   └── full_adder_8_bit  8-bit ripple-carry adder
    │       └── full_adder_1_bit  1-bit full adder (P/G style)
    ├── Shifter               Shift left / shift right / pass-through
    ├── FunctionSelect        FS3 AND FS2 -> MF select signal
    ├── MUXF                  2:1 mux selecting ALU or Shifter output
    └── NegZero               N (sign) and Z (zero) flag generation
```

---

## Table of Contents

### 1. Register File

The register file stores 16 general-purpose 8-bit registers with one write port and two independent read ports. Written on the rising clock edge when RW=1.

| # | Module | File | Page |
|---|--------|------|------|
| 1.0 | **RegisterFile** (top) | `RegisterFile.vhd` | [[RegisterFile]] |
| 1.1 | DestinationDecoder | `DestinationDecoder.vhd` | [[DestinationDecoder]] |
| 1.2 | RegisterR16 | `RegisterR16.vhd` | [[RegisterR16]] |
| 1.3 | Register8bit | `8bit_Register.vhd` | [[Register8bit]] |
| 1.4 | MUX2x1 | `MUX2x1.vhd` | [[MUX2x1]] |
| 1.5 | flip_flop | `flip_flop.vhd` | [[flip_flop]] |
| 1.6 | MUX16x1x8 | `MUX16x1x8.vhd` | [[MUX16x1x8]] |

### 2. Function Unit

The function unit performs all arithmetic, logic, and shift operations. Controlled by the 4-bit function select (FS3..FS0) and produces the result F along with status flags V, C, N, Z.

| # | Module | File | Page |
|---|--------|------|------|
| 2.0 | **FunctionUnit** (top) | `FunctionUnit.vhd` | [[FunctionUnit]] |
| 2.1 | ALU | `ALU.vhd` | [[ALU]] |
| 2.2 | full_adder_8_bit | `full_adder_8_bit.vhd` | [[full_adder_8_bit]] |
| 2.3 | full_adder_1_bit | `full_adder.vhd` | [[full_adder_1_bit]] |
| 2.4 | Shifter | `Shifter.vhd` | [[Shifter]] |
| 2.5 | FunctionSelect | `FunctionSelect.vhd` | [[FunctionSelect]] |
| 2.6 | MUXF | `MUX2x1x8.vhd` | [[MUXF]] |
| 2.7 | NegZero | `NegZero.vhd` | [[NegZero]] |

---

## FS Encoding Reference

### Arithmetic operations (FS3 = 0, MF = 0 -> ALU selected)

| FS3 | FS2 | FS1 | FS0 | Cin | Operation |
|-----|-----|-----|-----|-----|-----------|
| 0 | 0 | 0 | 0 | 0 | F = A (transfer) |
| 0 | 0 | 0 | 1 | 1 | F = A + 1 (increment) |
| 0 | 0 | 1 | 0 | 0 | F = A + B (add) |
| 0 | 0 | 1 | 1 | 1 | F = A + B + 1 |
| 0 | 1 | 0 | 0 | 0 | F = A + B' (subtract - 1) |
| 0 | 1 | 0 | 1 | 1 | F = A - B (subtract) |
| 0 | 1 | 1 | 0 | 0 | F = A - 1 (decrement) |
| 0 | 1 | 1 | 1 | 1 | F = A (transfer) |

### Logic operations (FS3 = 1, FS2 = 0, MF = 0 -> ALU selected)

| FS3 | FS2 | FS1 | FS0 | Operation |
|-----|-----|-----|-----|-----------|
| 1 | 0 | 0 | 0 | F = A OR B |
| 1 | 0 | 0 | 1 | F = A AND B |
| 1 | 0 | 1 | 0 | F = A XOR B |
| 1 | 0 | 1 | 1 | F = NOT A |

### Shift operations (FS3 = 1, FS2 = 1, MF = 1 -> Shifter selected)

| FS3 | FS2 | FS1 | FS0 | Operation |
|-----|-----|-----|-----|-----------|
| 1 | 1 | 0 | 0 | F = B (pass-through) |
| 1 | 1 | 0 | 1 | F = sr B (shift right) |
| 1 | 1 | 1 | 0 | F = sl B (shift left) |
| 1 | 1 | 1 | 1 | F = B (pass-through) |

---

## Status Flags

| Flag | Meaning | Source | Valid for |
|------|---------|--------|-----------|
| **V** | Overflow (C8 XOR C7) | full_adder_8_bit | Arithmetic ops only |
| **C** | Carry-out (C8) | full_adder_8_bit | Arithmetic ops only |
| **N** | Negative (bit 7 of result) | NegZero | All ops |
| **Z** | Zero (NOR of all result bits) | NegZero | All ops |

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
