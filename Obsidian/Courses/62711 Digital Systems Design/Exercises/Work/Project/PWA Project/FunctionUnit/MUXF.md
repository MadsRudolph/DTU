---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, combinational]
---
# MUXF

> [!info] Module Info
> **Entity:** `MUXF`
> **File:** `MUX2x1x8.vhd`
> **Architecture:** `Structural`
> **Parent:** [[FunctionUnit]]

## Purpose

8-bit wide 2-to-1 multiplexer that selects between the ALU output (J) and the Shifter output (H) based on the MF signal from [[FunctionSelect]]. The same entity design can be reused for MUXB and MUXD in the datapath.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `J` | in | 8 | ALU result |
| `H` | in | 8 | Shifter result |
| `MF` | in | 1 | Select: 0 = J (ALU), 1 = H (Shifter) |
| `Y` | out | 8 | Selected output |

## Logic

```vhdl
Y <= (J AND NOT MF) OR (H AND MF);
```

| MF | Y |
|----|---|
| 0 | J (ALU output) |
| 1 | H (Shifter output) |

> [!note] Naming
> The file is named `MUX2x1x8.vhd` but the entity is hardcoded as `MUXF`. The file header mentions it can be used for MUXB, MUXD, and MUXF, but separate entities or a generic approach would be needed for actual reuse.

---

> [!nav]
> &nbsp;
>
> [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
