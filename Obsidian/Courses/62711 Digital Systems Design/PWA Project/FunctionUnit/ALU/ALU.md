---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, structural]
---
# ALU

> [!info] Module Info
> **Entity:** `ALU`
> **File:** `ALU.vhd`
> **Architecture:** `ALU_Structural`
> **Parent:** [[FunctionUnit]]

## Purpose

Combined arithmetic and logic unit. JSel(3) selects the mode: JSel(3)=0 for arithmetic (adder-based), JSel(3)=1 for logic (gate-based). The B-input logic modifies operand B before the adder according to JSel(2:1). The logic unit uses JSel(1:0) to select between OR, AND, XOR, and NOT.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `A` | in | 8 | Operand A |
| `B` | in | 8 | Operand B |
| `JSel` | in | 4 | Operation select = FS(3:0) |
| `Cin` | in | 1 | Carry-in to adder |
| `V` | out | 1 | Overflow flag |
| `C` | out | 1 | Carry-out flag |
| `J` | out | 8 | ALU result |

## Internal Structure

### B-Input Logic (Arithmetic Mode)

When JSel(3)=0, BSig is computed per bit:

```vhdl
BSig(i) = ((B(i) AND JSel(1)) OR (NOT B(i) AND JSel(2))) AND NOT JSel(3)
```

| JSel(2:1) | BSig | Adder computes |
|-----------|------|----------------|
| 00 | 00000000 | A + 0 + Cin |
| 01 | B | A + B + Cin |
| 10 | NOT B | A + B' + Cin |
| 11 | 11111111 | A + FF + Cin |

### Logic Unit (Logic Mode)

When JSel(3)=1, BSig is zeroed and JLO is computed:

| JSel(1:0) | JLO |
|-----------|-----|
| 00 | A OR B |
| 01 | A AND B |
| 10 | A XOR B |
| 11 | NOT A |

### Output Selection

```vhdl
J = (JLO AND JSel(3)) OR (JAdd AND NOT JSel(3))
```

- JSel(3)=0: J = adder result (arithmetic)
- JSel(3)=1: J = logic result

## Sub-Components

| Instance | Entity | Description |
|----------|--------|-------------|
| `full_adder` | [[full_adder_8_bit]] | 8-bit ripple-carry adder with V and C |

---

> [!nav]
> &nbsp;
>
> [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
