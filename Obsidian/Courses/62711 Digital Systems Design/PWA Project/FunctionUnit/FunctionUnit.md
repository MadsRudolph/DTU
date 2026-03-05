---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, structural]
---
# FunctionUnit

> [!info] Module Info
> **Entity:** `FunctionUnit`
> **File:** `FunctionUnit.vhd`
> **Architecture:** `FU_Structural`
> **Spec:** Section (2), p.2

## Purpose

Top-level wrapper that combines the ALU, Shifter, output MUX, and flag generation into a single function unit. The 4-bit function select FS3..FS0 controls which operation is performed on inputs A and B. The result F is accompanied by four status flags: V (overflow), C (carry), N (negative), Z (zero).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `A` | in | 8 | Operand A (from register file) |
| `B` | in | 8 | Operand B (from register file) |
| `FS3, FS2, FS1, FS0` | in | 1 each | Function select bits |
| `Cin` | in | 1 | Carry-in to the adder |
| `V` | out | 1 | Overflow flag |
| `C` | out | 1 | Carry-out flag |
| `N` | out | 1 | Negative flag (sign bit) |
| `Z` | out | 1 | Zero flag |
| `F` | out | 8 | Function unit result |

## Block Diagram

```
  A ──────────┐
              ▼
         ┌─────────┐
  B ────►│   ALU   │──► J ──┐          V, C
         │         │        │            ▲
         └─────────┘        │            │
              ▲             ▼            │
              │        ┌─────────┐       │
  FS(3:0) ────┤   MF──►│  MUXF   │──► Res ──► F
              │    ▲   └─────────┘       │
              │    │        ▲            ▼
              ▼    │        │       ┌─────────┐
     ┌────────────┐│   ┌────┘       │ NegZero │──► N, Z
     │ Function   ├┘   │            └─────────┘
     │ Select     │    │
     └────────────┘    │
              │        │
  B ─────────►│   ┌────┘
              ▼   │
         ┌─────────┐
         │ Shifter │──► H
         └─────────┘
```

## Sub-Components

| Instance | Entity | Description |
|----------|--------|-------------|
| `U_ALU` | [[ALU]] | Arithmetic and logic operations |
| `U_Shifter` | [[Shifter]] | Shift left / shift right / pass-through |
| `U_FunctionSelect` | [[FunctionSelect]] | FS3 AND FS2 -> MF select signal |
| `U_MUXF` | [[MUXF]] | 2:1 mux: MF=0 selects ALU, MF=1 selects Shifter |
| `U_NegZero` | [[NegZero]] | N and Z flag generation from result |

## Design Notes

> [!warning] Cin vs FS0
> In the standard Mano/Kime function unit, FS0 serves as the carry-in for arithmetic operations. The current implementation has Cin as a separate port. For every arithmetic operation in the FS table, FS0 equals the required Cin value. Consider wiring FS0 directly as carry-in and removing the separate Cin port if following the textbook design.

> [!note] V and C during logic/shift operations
> When FS3=1, the ALU's B-input logic is zeroed out (masked by `AND NOT JSel(3)`), so the adder computes A + 0 + Cin. The resulting V and C flags are meaningless during logic and shift operations. The higher-level control must only use V and C during arithmetic operations.

---

> [!nav]
> &nbsp;
>
> [[PWA Project]] | [[RegisterFile]]
>
> &nbsp;
