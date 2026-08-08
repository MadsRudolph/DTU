---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, structural]
---
# full_adder_1_bit

> [!info] Module Info
> **Entity:** `full_adder_1_bit`
> **File:** `full_adder.vhd`
> **Architecture:** `structural`
> **Parent:** [[full_adder_8_bit]]

## Purpose

1-bit full adder using propagate/generate signals. Computes the sum and carry-out for a single bit position in the ripple-carry adder chain.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `A` | in | 1 | Operand A bit |
| `B` | in | 1 | Operand B bit |
| `Ci` | in | 1 | Carry-in from previous stage |
| `res` | out | 1 | Sum bit |
| `Co` | out | 1 | Carry-out to next stage |

## Logic

Uses propagate (P) and generate (G) signals:

```vhdl
Pi  <= A XOR B;          -- propagate
Gi  <= A AND B;          -- generate
res <= Pi XOR Ci;        -- sum = A XOR B XOR Ci
Co  <= (Pi AND Ci) OR Gi; -- carry = generate OR (propagate AND carry-in)
```

| A | B | Ci | res | Co |
|---|---|----|----|-----|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

---

> [!nav]
> &nbsp;
>
> [[full_adder_8_bit]] | [[ALU]] | [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
