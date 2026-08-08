---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz]
---
# Quiz before lection 9 - Memory

## Question 1 (1 point)

> [!question] En 16x1 RAM påtrykkes adressehukommelse 0101 - hvilken celle vælges?
>
> 16x1 RAM organiseret som 4x4 grid med row decoder og column decoder.
>
> - [x] **RAM cell 5**

> [!success] Answer: RAM cell 5

> [!note]- Explanation Adressen 0101 har 4 bits for 16 celler.
>
> > [!abstract] Adresseopdeling
> >
> > | Bits | Værdi | Funktion |
> > |---|---|---|
> > | A3A2 (upper) | 01 | Row Select = 1 |
> > | A1A0 (lower) | 01 | Column Select = 1 |
> >
> > Row 1, Column 1 = RAM cell 5
>
> > [!info] Celle-nummerering
> >
> > Cellerne er nummereret rækkefølge: Row 0 → cells 0-3, Row 1 → cells 4-7, Row 2 → cells 8-11, Row 3 → cells 12-15.
> > Celle = Row × 4 + Column = 1 × 4 + 1 = 5.

---

## Question 2 (1 point)

> [!question] Memory specification - hvor mange bit skal der til for adressere 1K words af 16 bit hver?
>
> - [ ] 2 byte
> - [ ] 9 bit
> - [ ] 1 byte
> - [x] **10 bit**

> [!success] Answer: 10 bit

> [!note]- Explanation 1K = 1024 = 2^10, derfor kræves 10 adressebits.
>
> > [!abstract] Adresseberegning
> >
> > | Parameter | Værdi |
> > |---|---|
> > | Antal words (m) | 1K = 1024 |
> > | Adressebits (k) | log2(1024) = 10 |
> > | Ordstørrelse | 16 bit (irrelevant for adressebredden) |
> >
> > Ordstørrelsen (16 bit) bestemmer databredden, ikke adressebredden.

---

## Question 3 (1 point)

> [!question] SRAM og DRAM er to forskellige typer teknologier - hvilken er en DRAM-celle
>
> To diagrammer vist:
> - (h) D flip-flop med Select og buffer → C output
> - SR-latch med AND-gates, B/B̄ inputs → C/C̄ outputs
>
> - [x] **(h) D flip-flop med Select og buffer**
> - [ ] SR-latch med AND-gates

> [!success] Answer: (h) D flip-flop med Select og buffer

> [!note]- Explanation Den øverste celle (h) med et enkelt lagerelement er den simplere celle, som repræsenterer DRAM. Den nederste med SR-latch og AND-gates er den klassiske SRAM-celle.
>
> > [!abstract] SRAM vs DRAM
> >
> > | Egenskab | SRAM | DRAM |
> > |---|---|---|
> > | Lagerelement | SR-latch (6 transistorer) | Kondensator (1 transistor + 1 kondensator) |
> > | Kompleksitet | Høj | Lav |
> > | Hastighed | Hurtig | Langsommere |
> > | Refresh | Ikke nødvendigt | Kræver periodisk refresh |
> > | Anvendelse | Cache | Hovedhukommelse |

---

## Question 4 (1 point)

> [!question] Hvilken sammenhæng er der mellem antal words (m) der kan gemmes og antal bit k til adressere m
>
> - [x] **2^k >= m**
> - [ ] 2*k >= m
> - [ ] 2^m <= k

> [!success] Answer: 2^k >= m

> [!note]- Explanation Med k adressebits kan man adressere 2^k lokationer, som skal være mindst m (antal words der skal lagres).
>
> > [!abstract] Formel
> >
> > k = ⌈log2(m)⌉
> >
> > Eksempler:
> >
> > | Words (m) | Adressebits (k) | 2^k |
> > |---|---|---|
> > | 256 | 8 | 256 |
> > | 1024 | 10 | 1024 |
> > | 1000 | 10 | 1024 (≥ 1000) |

---

## Summary

> [!tldr] Quick Answers
>
> | Q | Topic | Answer | Key Concept |
> |---|---|---|---|
> | 1 | 16x1 RAM adresse 0101 | RAM cell 5 | Upper bits → row, lower bits → column |
> | 2 | Adressebits for 1K words | 10 bit | 2^10 = 1024, ordstørrelse irrelevant |
> | 3 | DRAM vs SRAM celle | D flip-flop (h) | DRAM = simpel celle, SRAM = SR-latch |
> | 4 | Words vs adressebits | 2^k >= m | k adressebits dækker mindst m words |

---

> [!nav]
> [[Quiz 4|← Quiz 4]] | [[Quiz before lection 9|Current]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
