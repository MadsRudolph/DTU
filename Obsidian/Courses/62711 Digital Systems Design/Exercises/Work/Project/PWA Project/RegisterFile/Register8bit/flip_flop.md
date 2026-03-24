---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, sequential, behavioral]
---
# flip_flop

> [!info] Module Info
> **Entity:** `flip_flop`
> **File:** `flip_flop.vhd`
> **Architecture:** `Behavioral`
> **Parent:** [[Register8bit]]

## Purpose

Basic D flip-flop with asynchronous active-high reset. This is the only behavioral entity in the register file hierarchy -- all other components are structural or dataflow. It is the fundamental storage element; 128 instances (16 registers x 8 bits) form the register file's memory.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `D` | in | 1 | Data input |
| `Reset` | in | 1 | Async active-high reset (Q -> 0 immediately) |
| `clk` | in | 1 | Clock |
| `Q` | out | 1 | Stored output |

## Behavior

```vhdl
process(clk, Reset)
begin
    if Reset = '1' then
        Q <= '0';               -- async reset, immediate
    elsif rising_edge(clk) then
        Q <= D;                 -- capture D on rising edge
    end if;
end process;
```

- **Reset=1:** Q is forced to 0 immediately (asynchronous, no clock needed).
- **Rising edge of clk:** Q captures the current value of D.
- **All other times:** Q holds its value.

---

> [!nav]
> &nbsp;
>
> [[Register8bit]] | [[RegisterFile]] | [[PWA Project]]
>
> &nbsp;
