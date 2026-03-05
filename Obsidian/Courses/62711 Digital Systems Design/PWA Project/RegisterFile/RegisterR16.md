---
course: "62711"
course-name: "Digital Systems Design"
type: module
tags: [DSD, PWA, RegisterFile, structural]
---
# RegisterR16

> [!info] Module Info
> **Entity:** `RegisterR16`
> **File:** `RegisterR16.vhd`
> **Architecture:** `R16_Structural`
> **Parent:** [[RegisterFile]]

## Purpose

Structural block containing 16 x 8-bit registers. Each register is an instance of [[Register8bit]], generated using a VHDL `for...generate` loop. The LOAD bus (from [[DestinationDecoder]]) controls which register captures D_Data on the rising clock edge. All 16 register outputs (R0..R15) are exposed for the output MUXes.

## Port Map

| Port | Dir | Width | Description |
|------|-----|-------|-------------|
| `RESET` | in | 1 | Async active-high reset |
| `CLK` | in | 1 | Clock |
| `LOAD` | in | 16 | One-hot load enable per register |
| `D_Data` | in | 8 | Data input (shared by all registers) |
| `R0..R15` | out | 8 each | Individual register outputs |

## How It Works

Uses a custom array type and `for...generate`:

```vhdl
type reg_array is array (15 downto 0) of std_logic_vector(7 downto 0);
signal Rs : reg_array;

R16_Registers: for i in 0 to 15 generate
    Reg_inst: Register8bit port map (
        D => D_Data, Reset => RESET,
        Load => LOAD(i), clk => CLK, Q => Rs(i)
    );
end generate;
```

Each register receives the same D_Data and CLK, but only the one where `LOAD(i) = '1'` will actually capture the data (the MUX inside [[Register8bit]] handles this).

---

> [!nav]
> &nbsp;
>
> [[RegisterFile]] | [[Register8bit]] | [[PWA Project]]
>
> &nbsp;
