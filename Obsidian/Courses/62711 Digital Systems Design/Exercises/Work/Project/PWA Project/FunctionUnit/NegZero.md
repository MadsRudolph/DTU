---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, combinational]
---
# NegZero

> [!info] Module Info
> **Entity:** `NegZero`
> **File:** `NegZero.vhd`
> **Architecture:** `dataflow`
> **Parent:** [[FunctionUnit]]

## Purpose

Generates the N (negative) and Z (zero) status flags from the final function unit result. These flags are valid for all operations (arithmetic, logic, and shift), unlike V and C which are only meaningful for arithmetic.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `MUXF` | in | 8 | Function unit result (from [[MUXF]]) |
| `N` | out | 1 | Negative flag |
| `Z` | out | 1 | Zero flag |

## Logic

```vhdl
N <= MUXF(7);
Z <= NOT (MUXF(7) OR MUXF(6) OR MUXF(5) OR MUXF(4)
      OR  MUXF(3) OR MUXF(2) OR MUXF(1) OR MUXF(0));
```

- **N** = bit 7 of the result (the sign bit in two's complement).
- **Z** = NOR of all 8 bits. Z=1 only when the result is exactly 0x00.

| Result | N | Z |
|--------|---|---|
| 0x00 | 0 | 1 |
| 0x01 | 0 | 0 |
| 0x80 | 1 | 0 |
| 0xFF | 1 | 0 |

---

> [!nav]
> &nbsp;
>
> [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
