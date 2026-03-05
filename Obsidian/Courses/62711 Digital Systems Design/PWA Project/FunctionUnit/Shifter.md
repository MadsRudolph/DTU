---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, FunctionUnit, combinational]
---
# Shifter

> [!info] Module Info
> **Entity:** `Shifter`
> **File:** `Shifter.vhd`
> **Architecture:** `Shifter_Behavioral`
> **Parent:** [[FunctionUnit]]

## Purpose

8-bit combinational shifter. Operates only on input B. Controlled by HSel (= FS(1:0)) to perform shift right, shift left, or pass-through. Zeros are shifted in (logical shift, not arithmetic).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `B` | in | 8 | Input data (from register file) |
| `HSel` | in | 2 | Shift select = FS(1:0) |
| `H` | out | 8 | Shifter output |

## Operations

| HSel(1:0) | Operation | Description |
|-----------|-----------|-------------|
| 00 | H = B | Pass-through |
| 01 | H = sr B | Shift right, MSB filled with 0 |
| 10 | H = sl B | Shift left, LSB filled with 0 |
| 11 | H = B | Pass-through |

## How It Works

Uses an internal XOR to detect the "active shift" condition:

```vhdl
HTemp <= HSel(1) XOR HSel(0);  -- '1' when exactly one shift is selected
sl    <= HSel(1) AND HTemp;    -- shift-left enable
sr    <= HSel(0) AND HTemp;    -- shift-right enable
```

The shifted values are pre-computed, then the output MUX selects:

```vhdl
H <= (srB AND sr) OR (slB AND sl) OR (B AND NOT HTemp);
```

### Shift Right (sr)
```
B:   [b7][b6][b5][b4][b3][b2][b1][b0]
srB: [ 0][b7][b6][b5][b4][b3][b2][b1]
```

### Shift Left (sl)
```
B:   [b7][b6][b5][b4][b3][b2][b1][b0]
slB: [b6][b5][b4][b3][b2][b1][b0][ 0]
```

---

> [!nav]
> &nbsp;
>
> [[FunctionUnit]] | [[PWA Project]]
>
> &nbsp;
