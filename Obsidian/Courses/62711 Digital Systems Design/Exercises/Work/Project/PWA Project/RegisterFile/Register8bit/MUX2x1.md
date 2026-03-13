---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, combinational]
---
# MUX2x1

> [!info] Module Info
> **Entity:** `MUX2x1`
> **File:** `MUX2x1.vhd`
> **Architecture:** `Structural`
> **Parent:** [[Register8bit]]

## Purpose

1-bit 2-to-1 multiplexer used as the load-enable mux inside each bit of the 8-bit register. When Enable=0, the output feeds back the current flip-flop value (hold). When Enable=1, it passes through the new data (load).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `D` | in | 1 | New data input |
| `Q` | in | 1 | Feedback from flip-flop output |
| `Enable` | in | 1 | Select: 0 = Q (hold), 1 = D (load) |
| `Y` | out | 1 | MUX output to flip-flop D input |

## Logic

```vhdl
Y <= (Q AND NOT Enable) OR (D AND Enable);
```

| Enable | Y |
|--------|---|
| 0 | Q (hold current value) |
| 1 | D (load new value) |

---

> [!nav]
> &nbsp;
>
> [[Register8bit]] | [[RegisterFile]] | [[PWA Project]]
>
> &nbsp;
