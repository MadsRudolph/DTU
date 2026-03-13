---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWB, IDC, state-machine]
---
# InstructionDecoderController

> [!info] Module Info
> **Entity:** `InstructionDecoderController`
> **File:** `InstructionDecoderController.vhd`
> **Architecture:** `IDC_Behavorial`
> **Spec:** Section (3), p.2-3

## Purpose

Sequential control circuit (state machine) that decodes the instruction opcode and status flags, then produces the full control word for both the MPC and the Datapath. Two processes: one for the state register (sequential) and one for the next-state/output logic (combinatorial).

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset, returns to INF state |
| `CLK` | in | 1 | Clock, state transitions on rising edge |
| `IR` | in | 16 | Current instruction from Instruction Register |
| `V` | in | 1 | Overflow flag from Datapath |
| `C` | in | 1 | Carry flag from Datapath |
| `N` | in | 1 | Negative flag from Datapath |
| `Z` | in | 1 | Zero flag from Datapath |
| `PS` | out | 2 | Program Counter selector |
| `IL` | out | 1 | Instruction Load enable |
| `DX` | out | 4 | Extended DA register address |
| `AX` | out | 4 | Extended AA register address |
| `BX` | out | 4 | Extended BA register address |
| `FS` | out | 4 | Function selector |
| `MB` | out | 1 | MUX B-source selector |
| `MD` | out | 1 | MUX Destination selector |
| `RW` | out | 1 | Register Write |
| `MM` | out | 1 | Memory address MUX |
| `MW` | out | 1 | Memory Write |

## State Diagram

```
     RESET
       │
       ▼
    ┌─────┐    all opcodes    ┌─────┐
    │ INF │──────────────────►│ EX0 │
    └─────┘                   └──┬──┘
       ▲                         │
       │  2-cycle instructions   │
       │◄────────────────────────┤
       │                         │
       │  LRI, SRM, SLM         ▼
       │                      ┌─────┐
       │◄─────── LRI ────────│ EX1 │
       │                      └──┬──┘
       │                         │ SRM/SLM
       │                         ▼
       │                      ┌─────┐
       │                      │ EX2 │◄──┐
       │                      └──┬──┘   │
       │                         │      │
       │                         ▼      │
       │                      ┌─────┐   │
       │                      │ EX3 │───┘ (Z=0: loop back)
       │                      └──┬──┘
       │                         │ (Z=1)
       │                         ▼
       │                      ┌─────┐
       │◄─────────────────────│ EX4 │
       │                      └─────┘
```

## States

| State | Description |
|-------|-------------|
| INF | Instruction Fetch: IR <- M[PC], IL=1, MM=1 |
| EX0 | Execute cycle 0: decode opcode, produce control word |
| EX1 | Execute cycle 1: used by LRI, SRM, SLM |
| EX2 | Execute cycle 2: SRM/SLM shift operation |
| EX3 | Execute cycle 3: SRM/SLM decrement counter, loop check |
| EX4 | Execute cycle 4: SRM/SLM write result back |

## Design Notes

> [!tip] Implementation
> **Process 1 (state register):** Sequential process with CLK and RESET. On reset go to INF, on rising edge load next_state.
>
> **Process 2 (combinatorial):** Case-in-case structure. Outer case on `current_state`, inner case on `opcode` (IR(15 downto 9)). Set default values for all outputs at the top, then override per state/opcode. Check status flags (V,C,N,Z) for conditional branches (BRZ, BRN) and multi-cycle instructions (SRM, SLM).

> [!warning] DX, AX, BX encoding
> These are 4-bit extended addresses. The MSB (bit 3) comes from the control logic, while bits 2..0 come from the IR fields:
> - DX = DX3 & IR8 & IR7 & IR6
> - AX = AX3 & IR5 & IR4 & IR3
> - BX = BX3 & IR2 & IR1 & IR0
>
> For multi-cycle instructions (SRM/SLM), DX3=1 selects R8/R9 as temporary registers.

---

> [!nav]
> &nbsp;
>
> [[PWB Project]] | [[MicroprogramController]]
>
> &nbsp;
