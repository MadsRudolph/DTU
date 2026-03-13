---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, ZeroFiller, combinatorial]
---
# ZeroFiller

> [!info] Module Info
> **Entity:** `ZeroFiller`
> **File:** `ZeroFiller.vhd`
> **Architecture:** `ZF_Behavorial`
> **Spec:** Section (2), p.1

## Purpose

Takes the 3 lowest bits of the Instruction Register and zero-fills to 8 bits. Used as the immediate constant for LDI and ADI instructions (Constant_Out on the MPC top-level).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `IR` | in | 16 | Full instruction register value |
| `ZeroFilled_8` | out | 8 | Zero-filled 8-bit result |

## Logic

```
ZeroFilled_8 = 0.0.0.0.0.IR2.IR1.IR0
```

## Design Notes

> [!tip] Implementation
> This is pure combinatorial -- use only concurrent signal assignments (no process needed).

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[SignExtender]] | [[InstructionDecoderController]]
>
> &nbsp;
