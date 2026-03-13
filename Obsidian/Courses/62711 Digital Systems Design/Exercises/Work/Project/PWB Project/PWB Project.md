---
course: "62711"
course-name: "Digital Systems Design"
type: project
tags: [DSD, PWB, project]
---
# PWB Project -- Microprogram Controller

> [!info] Project Info
> **Phase:** PWB (Project Work B)
> **Goal:** Design and implement the Microprogram Controller (MPC)
> **Deadline:** 09-04-2026 (Week 14)
> **Spec:** [[62711_ProjectWork_B_F2026.pdf|PWB Project Assignment]]
> **Repo:** [GitHub](https://github.com/gigurd/Design-of-digital-systems-62711) &mdash; `team/PWB/`

---

## Top-Level Hierarchy

```
MicroprogramController
├── ProgramCounter           8-bit PC with Hold/Inc/Branch/Jump
├── InstructionRegister      16-bit IR with load-enable
├── SignExtender             6-bit to 8-bit sign extension (combinatorial)
├── ZeroFiller               3-bit to 8-bit zero fill (combinatorial)
└── InstructionDecoderController   State machine (INF, EX0..EX4)
```

---

## Team Split

| Pair | Members | Modules |
|------|---------|---------|
| Pair 1 | Andreas + Jonas | ProgramCounter, InstructionRegister, SignExtender, ZeroFiller |
| Pair 2 | Mads + Sigurd | InstructionDecoderController, MicroprogramController |

---

## Table of Contents

### 1. Program Counter

8-bit register that holds the address of the next instruction. Controlled by PS: Hold (00), Increment (01), Branch (10), Jump (11).

| # | Module | File | Page |
|---|--------|------|------|
| 1.0 | **ProgramCounter** | `ProgramCounter.vhd` | [[ProgramCounter]] |

### 2. Instruction Register

16-bit register that holds the current instruction. Loaded from memory when IL=1 on rising clock edge.

| # | Module | File | Page |
|---|--------|------|------|
| 2.0 | **InstructionRegister** | `InstructionRegister.vhd` | [[InstructionRegister]] |
| 2.1 | SignExtender | `SignExtender.vhd` | [[SignExtender]] |
| 2.2 | ZeroFiller | `ZeroFiller.vhd` | [[ZeroFiller]] |

### 3. Instruction Decoder / Controller

State machine that decodes the 7-bit opcode and produces the 28-bit control word for the MPC and Datapath. Uses two processes: state register (sequential) and control logic (combinatorial case-in-case).

| # | Module | File | Page |
|---|--------|------|------|
| 3.0 | **InstructionDecoderController** | `InstructionDecoderController.vhd` | [[InstructionDecoderController]] |

### 4. Top-Level

Structural wrapper that wires all submodules together.

| # | Module | File | Page |
|---|--------|------|------|
| 4.0 | **MicroprogramController** | `MicroprogramController.vhd` | [[MicroprogramController]] |

---

## Instruction Set Reference

| Opcode | Mnemonic | Operation | Cycles |
|--------|----------|-----------|--------|
| 0000000 | MOVA | R[DR] <- R[SA] | 2 |
| 0000001 | INC | R[DR] <- R[SA] + 1 | 2 |
| 0000010 | ADD | R[DR] <- R[SA] + R[SB] | 2 |
| 0000101 | SUB | R[DR] <- R[SA] - R[SB] | 2 |
| 0000110 | DEC | R[DR] <- R[SA] - 1 | 2 |
| 0001000 | OR | R[DR] <- R[SA] OR R[SB] | 2 |
| 0001001 | AND | R[DR] <- R[SA] AND R[SB] | 2 |
| 0001010 | XOR | R[DR] <- R[SA] XOR R[SB] | 2 |
| 0001011 | NOT | R[DR] <- NOT R[SA] | 2 |
| 0001100 | MOVB | R[DR] <- R[SB] | 2 |
| 0010000 | LD | R[DR] <- M[R[SA]] | 2 |
| 0100000 | ST | M[R[SA]] <- R[SB] | 2 |
| 1001100 | LDI | R[DR] <- zf OP | 2 |
| 1000010 | ADI | R[DR] <- R[SA] + zf OP | 2 |
| 1100000 | BRZ | Branch if Z=1 | 2 |
| 1100001 | BRN | Branch if N=1 | 2 |
| 1110000 | JMP | PC <- R[SA] | 2 |
| 0010001 | LRI | Load Register Indirect | 3 |
| 0001101 | SRM | Shift Right Multiple | 5+ |
| 0001110 | SLM | Shift Left Multiple | 5+ |

---

## Control Word (28 bits)

```
 27-24   23-22  21   20-17  16-13  12-9   8    7-4   3    2    1    0
┌──────┬──────┬────┬──────┬──────┬──────┬────┬──────┬────┬────┬────┬────┐
│  NS  │  PS  │ IL │  DX  │  AX  │  BX  │ MB │  FS  │ MD │ RW │ MM │ MW │
└──────┴──────┴────┴──────┴──────┴──────┴────┴──────┴────┴────┴────┴────┘
  MPC part                          Datapath part
```

| Signal | Width | Description |
|--------|-------|-------------|
| NS | 4 | Next State |
| PS | 2 | Program Counter selector (00=Hold, 01=Inc, 10=Branch, 11=Jump) |
| IL | 1 | Instruction Load enable |
| DX | 4 | Extended DA register (DX3 & IR8 & IR7 & IR6) |
| AX | 4 | Extended AA register (AX3 & IR5 & IR4 & IR3) |
| BX | 4 | Extended BA register (BX3 & IR2 & IR1 & IR0) |
| MB | 1 | MUX B-source selector |
| FS | 4 | Function selector |
| MD | 1 | MUX Destination selector |
| RW | 1 | Register Write |
| MM | 1 | Memory address MUX (1=PC, 0=DP address) |
| MW | 1 | Memory Write |

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]] | [[PWA Project]]
>
> &nbsp;
