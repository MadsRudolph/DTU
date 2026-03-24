---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, structural]
---
# full_adder_8_bit

> [!info] Module Info
> **Entity:** `full_adder_8_bit`
> **File:** `full_adder_8_bit.vhd`
> **Architecture:** `Structural`
> **Parent:** [[ALU]]

## Purpose

8-bit ripple-carry adder built from 8 instances of [[full_adder_1_bit]]. Produces the sum, carry-out (C), and overflow (V) flags. The carry chain propagates from bit 0 through to bit 7.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `A` | in | 8 | Operand A |
| `B` | in | 8 | Operand B (modified by ALU's B-input logic) |
| `Cin` | in | 1 | Carry-in |
| `sum` | out | 8 | A + B + Cin result |
| `Cout` | out | 1 | Carry-out from bit 7 (C flag) |
| `V` | out | 1 | Overflow flag |

## How It Works

```
Cin ─► [FA0] ─c1─► [FA1] ─c2─► ... ─c7─► [FA7] ─► carry(8)
        │           │                       │
       sum(0)     sum(1)                  sum(7)
```

Each full adder takes `A(i)`, `B(i)`, and the carry from the previous stage.

### Flag Generation

```vhdl
Cout <= carry(8);          -- carry-out from MSB
V    <= carry(8) XOR carry(7);  -- overflow = C8 XOR C7
```

Overflow (V) detects when the sign of the result is wrong for signed arithmetic. It is set when the carry into the MSB differs from the carry out of the MSB.

## Sub-Components

| Instance | Entity | Count |
|----------|--------|-------|
| `bit_0..bit_7` | [[full_adder_1_bit]] | 8 |

---

> [!nav]
> &nbsp;
>
> [[ALU]] | [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
