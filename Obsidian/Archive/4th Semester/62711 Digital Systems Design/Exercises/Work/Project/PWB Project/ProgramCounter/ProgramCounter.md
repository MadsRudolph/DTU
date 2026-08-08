---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, ProgramCounter, sequential]
---
# ProgramCounter

> [!info] Module Info
> **Entity:** `ProgramCounter`
> **File:** `ProgramCounter.vhd`
> **Architecture:** `PC_Behavorial`
> **Spec:** Section (1), p.1

## Purpose

8-bit program counter register that holds the address of the next instruction to be fetched. On each rising clock edge, the PS control word determines the action: hold the current value, increment by one, branch by adding a signed offset, or jump to an absolute address.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset, clears PC to 0x00 |
| `CLK` | in | 1 | Clock, actions occur on rising edge |
| `Address_In` | in | 8 | Jump target address |
| `PS` | in | 2 | Program counter selector |
| `Offset` | in | 8 | Branch offset (two's complement, from Sign Extender) |
| `PC` | out | 8 | Current program counter value (= Address_Out) |

## PS Control Table

| PS | CLK | Action | Value of PC |
|----|-----|--------|-------------|
| 00 | rising | Hold | PC |
| 01 | rising | Increment | PC <- PC + 1 |
| 10 | rising | Branch | PC <- PC + Offset |
| 11 | rising | Jump | PC <- Address_In |
| XX | 1 or 0 | Idle | PC |

## Design Notes

> [!tip] Implementation
> This is a sequential module. Use a single process with CLK and RESET in the sensitivity list. Use a `case` statement on PS inside the `rising_edge(CLK)` block.

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[InstructionRegister]]
>
> &nbsp;
