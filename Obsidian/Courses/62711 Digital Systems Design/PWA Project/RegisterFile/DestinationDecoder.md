---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, combinational]
---
# DestinationDecoder

> [!info] Module Info
> **Entity:** `DestinationDecoder`
> **File:** `DestinationDecoder.vhd`
> **Architecture:** `dataflow`
> **Parent:** [[RegisterFile]]

## Purpose

4-to-16 one-hot decoder gated by the WRITE enable signal. Converts the 4-bit destination address DA into a 16-bit LOAD bus where exactly one bit is high (the addressed register). When WRITE=0, all LOAD bits are 0 and no register is written.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `WRITE` | in | 1 | Write enable (from RW) |
| `DA` | in | 4 | Destination address |
| `LOAD` | out | 16 | One-hot load enable for each register |

## How It Works

Each LOAD output is the AND of WRITE with the corresponding minterm of DA:

```
LOAD(i) = WRITE AND minterm_i(DA)
```

For example:
- `LOAD(0) = WRITE AND (NOT DA3)(NOT DA2)(NOT DA1)(NOT DA0)` -- DA = 0000
- `LOAD(5) = WRITE AND (NOT DA3)(DA2)(NOT DA1)(DA0)` -- DA = 0101
- `LOAD(15) = WRITE AND (DA3)(DA2)(DA1)(DA0)` -- DA = 1111

When WRITE=0, all LOAD bits are forced to 0 regardless of DA.

---

> [!nav]
> &nbsp;
>
> [[RegisterFile]] | [[PWA Project]]
>
> &nbsp;
