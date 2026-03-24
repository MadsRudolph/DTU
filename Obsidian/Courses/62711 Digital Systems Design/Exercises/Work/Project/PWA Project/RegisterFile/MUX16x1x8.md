---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, combinational]
---
# MUX16x1x8

> [!info] Module Info
> **Entity:** `MUX16x1x8`
> **File:** `MUX16x1x8.vhd`
> **Architecture:** `dataflow`
> **Parent:** [[RegisterFile]]

## Purpose

16-to-1 multiplexer, 8 bits wide. Two instances are used in the register file: one for the A_Data read port (selected by AA) and one for the B_Data read port (selected by BA). Purely combinational -- read output updates immediately when the select address changes.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `R0..R15` | in | 8 each | 16 register data inputs |
| `D_Select` | in | 4 | Select address (AA or BA) |
| `Y_Data` | out | 8 | Selected register output |

## How It Works

Uses a `for...generate` loop across all 8 data bits. For each bit `i`, the output is the OR of 16 AND-gated terms, one per register:

```vhdl
gen_mux: for i in 0 to 7 generate
    Y_Data(i) <=
       (R0(i)  and minterm_0(D_Select)) or
       (R1(i)  and minterm_1(D_Select)) or
       ...
       (R15(i) and minterm_15(D_Select));
end generate;
```

Each minterm decodes D_Select to select exactly one register input per output bit.

---

> [!nav]
> &nbsp;
>
> [[RegisterFile]] | [[PWA Project]]
>
> &nbsp;
