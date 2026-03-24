---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, InstructionRegister, sequential]
---
# InstructionRegister

> [!info] Module Info
> **Entity:** `InstructionRegister`
> **File:** `InstructionRegister.vhd`
> **Architecture:** `IR_Behavorial`
> **Spec:** Section (2), p.1

## Purpose

16-bit instruction register that holds the current instruction during an execution cycle. The instruction is loaded from memory when IL=1 on the rising clock edge. When IL=0, the register holds its current value.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset, clears IR to 0x0000 |
| `CLK` | in | 1 | Clock, load occurs on rising edge |
| `Instruction_In` | in | 16 | Instruction data from memory |
| `IL` | in | 1 | Instruction Load enable |
| `IR` | out | 16 | Current instruction value |

## IL Control Table

| IL | CLK | Action | Value of IR |
|----|-----|--------|-------------|
| 0 | rising | No Load | IR |
| 1 | rising | Load | IR <- Instruction_In |
| X | 1 or 0 | Idle | IR |

## Instruction Format (16 bits)

```
 15  14  13  12  11  10   9    8   7   6    5   4   3    2   1   0
┌───────────────────────────┬───────────┬───────────┬───────────┐
│        Opcode (7 bit)     │ 2nd field │ 3rd field │ 4th field │
│   IR15 .. IR9             │ IR8..IR6  │ IR5..IR3  │ IR2..IR0  │
└───────────────────────────┴───────────┴───────────┴───────────┘
```

## Design Notes

> [!tip] Implementation
> This is a sequential module. Use a single process with CLK and RESET in the sensitivity list. Check IL inside the `rising_edge(CLK)` block.

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[ProgramCounter]] | [[SignExtender]]
>
> &nbsp;
