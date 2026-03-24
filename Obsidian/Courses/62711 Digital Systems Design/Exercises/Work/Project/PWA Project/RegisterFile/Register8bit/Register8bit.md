---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, structural]
---
# Register8bit

> [!info] Module Info
> **Entity:** `Register8bit`
> **File:** `8bit_Register.vhd`
> **Architecture:** `Structural`
> **Parent:** [[RegisterR16]]

## Purpose

8-bit parallel register with async reset and load enable. Built structurally from 8 instances of [[MUX2x1]] + [[flip_flop]] pairs using `for...generate`. The MUX feeds back the current flip-flop output when Load=0 (hold), or passes new data D when Load=1 (capture).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `D` | in | 8 | Data input |
| `Reset` | in | 1 | Async active-high reset |
| `Load` | in | 1 | Load enable (1 = capture D, 0 = hold Q) |
| `clk` | in | 1 | Clock |
| `Q` | out | 8 | Register output |

## How It Works

For each bit `i` (0 to 7):

```
          Load
           │
    D(i) ──┤
           ▼
      ┌─────────┐       ┌──────────┐
      │ MUX2x1  │──Ys──►│ flip_flop│──► Q_reg(i) ──► Q(i)
      │         │       │          │        │
      └─────────┘       └──────────┘        │
           ▲                                │
           └── Q_reg(i) ◄──────────────────┘
               (feedback)
```

- **Load=0:** MUX selects Q_reg (feedback), flip-flop reloads its own value = hold.
- **Load=1:** MUX selects D, flip-flop captures new data on rising edge.

## Sub-Components

| Instance | Entity | Description |
|----------|--------|-------------|
| `MUX_inst` (x8) | [[MUX2x1]] | Load-enable mux per bit |
| `Dflip_inst` (x8) | [[flip_flop]] | D flip-flop per bit |

---

> [!nav]
> &nbsp;
>
> [[RegisterR16]] | [[RegisterFile]] | [[PWA Project]]
>
> &nbsp;
