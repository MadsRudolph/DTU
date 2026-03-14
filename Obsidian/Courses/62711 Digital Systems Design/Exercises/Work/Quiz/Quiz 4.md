---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz]
---
# Quiz 4 - Multiple Cycle Architecture & Microprogrammed Control

## Question 1 (1 point)

> [!question] Control word for multiple cycle arkitekturen, Hvorfor indføres der 4 bit på DX, AX, BX
>
> Control word fields: NS | PS | IL | DX | AX | BX | MB | FS | MD | RW | MM | MW
>
> - [ ] så der kan håndteres simplere instruktioner
> - [x] **så der kan benyttes del af functions enheden - der ikke kan benyttes i en cycle arkitektur**
> - [ ] så control enheden kan adressere registrene R8 til R15
> - [ ] for en sikkerhedsskyld

> [!success] Answer: så der kan benyttes del af functions enheden - der ikke kan benyttes i en cycle arkitektur

> [!note]- Explanation In a single-cycle architecture, register addresses come directly from the instruction opcode bits. In a multi-cycle architecture, the control word provides **separate 4-bit fields** for DX, AX, BX.
>
> > [!abstract] Why 4 bits?
> >
> > With 4 bits the control unit can independently specify register operands for the function unit across multiple cycles. This allows:
> >
> > - Using the ALU/function unit for **intermediate calculations** (e.g., address computation)
> > - Performing operations that require **more than one cycle** of ALU usage
> > - Accessing registers for purposes beyond what the instruction encoding directly supports
>
> > [!info] Single-cycle vs Multi-cycle
> >
> > | Property | Single-cycle | Multi-cycle |
> > |---|---|---|
> > | Register selection | From instruction bits | From control word |
> > | ALU usage | One operation per instruction | Multiple operations per instruction |
> > | Flexibility | Limited by instruction format | Control word can specify any register combination |

---

## Question 2 (1 point)

> [!question] Der er farvet en ledning fra register fil ned til muxM - hvorfor kan register indhold føres fra register fil til muxM
>
> Blue wire from register file output to MUX M in the microprogrammed control datapath.
>
> - [ ] Det er den eneste måde at adressere memory på
> - [x] **Fordi register kan indeholde en adresse der skal bruges for at store data i memory**
> - [ ] Fordi der skal kunne lagres konstanter i hukommelsen
> - [ ] For at kunne arbejde med register data i functional unit

> [!success] Answer: Fordi register kan indeholde en adresse der skal bruges for at store data i memory

> [!note]- Explanation MUX M selects the **memory address source**. The wire from the register file allows register content to be used as a memory address.
>
> > [!abstract] Register Indirect Addressing
> >
> > For store instructions like `ST R1, (R2)`, the CPU needs to:
> >
> > 1. Read the **address** from a register (e.g., R2)
> > 2. Route that address to memory via MUX M
> > 3. Write the data from another register (e.g., R1) to that memory location
> >
> > Without this path, the datapath could not support **register indirect memory addressing**.
>
> > [!abstract] MUX M Inputs
> >
> > | MM (select) | Source | Use case |
> > |---|---|---|
> > | 0 | Function unit output | Computed address (e.g., PC + offset) |
> > | 1 | Register file output | Register indirect addressing |

---

## Question 3 (1 point)

> [!question] For multiple cycle architecture har et felt PS, Hvorfor sendes det til PC?
>
> - [x] **PS indeholder adressen**
> - [ ] For at sætte adresse med en offset
> - [ ] For at kun styre program tælleren PC
> - [ ] For at kunne lave indirekte adressering

> [!success] Answer: PS indeholder adressen

> [!note]- Explanation The **PS** (Program Sequence) field in the control word contains a direct address that can be loaded into the Program Counter.
>
> > [!abstract] PS → PC Path
> >
> > In the microprogrammed control unit, the PS field provides an **explicit next address** for branching:
> >
> > - When a branch or jump microinstruction is executed, the address stored in PS is loaded directly into PC
> > - This enables the microprogram to **jump to specific microinstruction addresses**
> > - PS essentially holds the target address for control flow changes
>
> > [!info] Sequencing Control
> >
> > The NS (Next State) and PS fields work together for sequencing:
> >
> > | Field | Purpose |
> > |---|---|
> > | NS | Selects next state logic (increment, branch, etc.) |
> > | PS | Provides the branch target address to load into PC |

---

## Question 4 (1 point)

> [!question] Kontrolordet for multiple cycle architecture har et felt IL, Hvad styrer det?
>
> - [ ] styre om instruktionsregister kan gemme en ny instruktion
> - [ ] enable for program tælleren (PC)
> - [ ] styrer om data kan læses ind og ud af hukommelsen
> - [x] **bruges til at holde værdi i instruction register eller hente ny instruction**

> [!success] Answer: bruges til at holde værdi i instruction register eller hente ny instruction

> [!note]- Explanation **IL** (Instruction Load) controls the instruction register's behavior during multi-cycle execution.
>
> > [!abstract] IL Function
> >
> > | IL | Operation |
> > |---|---|
> > | 0 | **Hold** — Instruction register retains its current value |
> > | 1 | **Load** — A new instruction is fetched and loaded into the instruction register |
>
> > [!info] Why is this needed?
> >
> > In a multi-cycle architecture, a single instruction takes **multiple clock cycles** to execute. During those cycles:
> >
> > - The instruction register must **hold** the current instruction (IL = 0) so the control unit can continue decoding it
> > - Only when the current instruction is fully executed should a **new instruction** be fetched (IL = 1)
> >
> > Without IL, the instruction register would update every cycle, corrupting the multi-cycle execution.

---

## Summary

> [!tldr] Quick Answers
>
> | Q | Topic | Answer | Key Concept |
> |---|---|---|---|
> | 1 | Control word 4-bit fields | Function unit flexibility | Multi-cycle allows ALU reuse across cycles |
> | 2 | Register file → MUX M | Register indirect addressing | Register holds memory address for store ops |
> | 3 | PS field → PC | PS indeholder adressen | Direct branch target address for microprogram |
> | 4 | IL field | Hold or load instruction register | Prevents instruction corruption during multi-cycle execution |

---

> [!nav]
> [[Quiz 3|← Quiz 3]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;