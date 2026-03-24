---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, combinational]
---
# FunctionSelect

> [!info] Module Info
> **Entity:** `FunctionSelect`
> **File:** `FunctionSelect.vhd`
> **Architecture:** `Structural`
> **Parent:** [[FunctionUnit]]

## Purpose

Decodes FS3 and FS2 into the MF (MUX-F select) signal that controls whether the function unit output comes from the ALU or the Shifter.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `FS` | in | 4 | Function select bus |
| `MF` | out | 1 | MUX-F select: 0 = ALU, 1 = Shifter |

## Logic

```vhdl
MF <= FS(3) AND FS(2);
```

| FS3 | FS2 | MF | Output Source |
|-----|-----|----|--------------|
| 0 | 0 | 0 | ALU (arithmetic) |
| 0 | 1 | 0 | ALU (arithmetic) |
| 1 | 0 | 0 | ALU (logic) |
| 1 | 1 | **1** | **Shifter** |

The shifter is only selected when both FS3=1 and FS2=1.

---

> [!nav]
> &nbsp;
>
> [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
