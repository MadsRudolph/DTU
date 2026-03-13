---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, SignExtender, combinatorial]
---
# SignExtender

> [!info] Module Info
> **Entity:** `SignExtender`
> **File:** `SignExtender.vhd`
> **Architecture:** `SE_Behavorial`
> **Spec:** Section (2), p.1

## Purpose

Takes 6 bits from the Instruction Register and sign-extends them into an 8-bit two's complement number. Used as the branch offset for the Program Counter.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `IR` | in | 16 | Full instruction register value |
| `Extended_8` | out | 8 | Sign-extended 8-bit result |

## Logic

| IR(8) | Extended_8 |
|-------|------------|
| 0 | `0.0.0.IR7.IR6.IR2.IR1.IR0` |
| 1 | `1.1.1.IR7.IR6.IR2.IR1.IR0` |

## Design Notes

> [!tip] Implementation
> This is pure combinatorial -- use only concurrent signal assignments (no process needed).

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[InstructionRegister]] | [[ZeroFiller]]
>
> &nbsp;
