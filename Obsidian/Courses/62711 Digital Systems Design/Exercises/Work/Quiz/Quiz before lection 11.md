---
course: "62711"
course-name: "Digital Systems Design"
type: quiz
tags: [DSD, quiz, DMA, cache]
---
# Quiz before lection 11 - DMA & Cache Memory

## Question 1 (1 point)

> [!question] Hvad betyder DMA
>
> - [x] **Direct memory Access**
> - [ ] Data memory Access
> - [ ] Data management Access
> - [ ] Direct module Access

> [!success] Answer: Direct memory Access

> [!note]- Explanation DMA = **D**irect **M**emory **A**ccess. Det er en hardware-mekanisme, der gør det muligt for periferi-enheder (disk, netværk, lyd, etc.) at overføre data direkte til/fra hovedhukommelsen uden CPU'ens medvirken på hver enkelt overførsel.
>
> > [!abstract] Begrebet "Direct"
> >
> > Det "direkte" i DMA refererer til, at dataoverførslen går direkte mellem I/O-enheden og hukommelsen — uden at gå "gennem" CPU'en. Uden DMA ville CPU'en være tvunget til at køre en programmeret I/O-loop og kopiere hver byte/word fra enheden til hukommelsen, hvilket er meget ressourcekrævende.

---

## Question 2 (1 point)

> [!question] Forklar princippet i DMA

> [!success] Princip
>
> En **DMA-controller** overtager systembussen midlertidigt fra CPU'en og udfører hukommelses-til-enhed- eller enhed-til-hukommelses-overførsler direkte. CPU'en programmerer DMA-controlleren med kilde-adresse, destinations-adresse og antal bytes/words, og giver derefter "go". Når overførslen er færdig, signalerer DMA-controlleren CPU'en med et **interrupt**.

> [!note]- Detaljeret forklaring
>
> > [!abstract] Trin i en DMA-overførsel
> >
> > | Trin | Hvem | Handling |
> > |---|---|---|
> > | 1. Setup | CPU | Skriver kilde-adresse, destinations-adresse og længde til DMA-controllerens registre |
> > | 2. Start | CPU | Skriver "GO" til control-registret og kan herefter udføre andet arbejde |
> > | 3. Bus request | DMA | Anmoder om systembussen via BR (Bus Request) signalet |
> > | 4. Bus grant | CPU | Frigiver bussen og bekræfter med BG (Bus Grant) |
> > | 5. Transfer | DMA | Læser fra kilde, skriver til destination, dekrementerer tæller — gentages indtil tælleren er 0 |
> > | 6. Done | DMA | Afgiver bussen og udløser et interrupt for at fortælle CPU'en, at overførslen er færdig |
>
> > [!info] Fordele ved DMA
> >
> > - **Aflaster CPU'en**: CPU kan udføre andet arbejde mens overførslen sker
> > - **Højere gennemstrømning**: DMA-controlleren er specialiseret til hurtig hukommelses-overførsel
> > - **Bulk-overførsel**: Hele blokke flyttes i ét stræk, ikke én byte/word ad gangen via CPU-instruktioner
>
> > [!warning] Cycle stealing vs. burst mode
> >
> > | Mode | Bus-brug | Effekt på CPU |
> > |---|---|---|
> > | **Cycle stealing** | DMA tager én bus-cyklus ad gangen, deler med CPU | CPU bremses lidt |
> > | **Burst mode** | DMA holder bussen indtil hele blokken er overført | CPU er låst ude indtil færdig |

---

## Question 3 (1 point)

> [!question] Cache-system: 32-bit data, direct mapping. 512 words i main memory, der mappes til 64 word-locations i cachen. Cache-linje = 4 bytes (1 word). Question a: I hvilken cache-adresse mappes det 0'te word i main memory?
>
> - [ ] indeks 1111
> - [ ] indeks 1000
> - [x] **indeks 0000**

> [!success] Answer: indeks 0000

> [!note]- Explanation Ved direct mapping er cache-indekset bestemt af de **lave bits** af hukommelses-adressen: `cache_index = memory_address mod cache_size`.
>
> > [!abstract] Beregning for word 0
> >
> > | Parameter | Værdi |
> > |---|---|
> > | Memory-adresse | 0 |
> > | Cache-størrelse | 64 linjer |
> > | Cache-indeks | 0 mod 64 = **0** |
> > | Binært | `0000` (eller `000000` med 6 bit) |
> >
> > Word 0 i main memory mappes altid direkte til linje 0 i cachen.
>
> > [!info] Direct mapping princip
> >
> > Adressen opdeles i tre felter:
> >
> > ```
> > | Tag | Index | Offset |
> > ```
> >
> > - **Offset**: vælger byte/word inden for en cache-linje
> > - **Index**: vælger hvilken cache-linje (uden for valg — direkte mappet)
> > - **Tag**: lagres sammen med data i cachen og sammenlignes ved opslag for at afgøre, om det er den rigtige memory-adresse

---

## Question 4 (1 point)

> [!question] Samme cache-specifikation som spørgsmål a. Question b: Hvilke andre words fra main memory mappes til samme cache-lokation som word 0?
>
> - [x] **words at address 64, 128, 192.....448**
> - [ ] words at address 128, 256, 384
> - [ ] words at address 16, 32, 48.....448

> [!success] Answer: words at address 64, 128, 192.....448

> [!note]- Explanation Alle hukommelses-adresser, der har samme rest ved division med cache-størrelsen (64), mappes til samme cache-linje.
>
> > [!abstract] Adresser der mapper til cache-linje 0
> >
> > `address mod 64 = 0` ⇒ adresse er multiplum af 64
> >
> > | Adresse | mod 64 | Cache-linje |
> > |---|---|---|
> > | 0 | 0 | **0** |
> > | 64 | 0 | **0** |
> > | 128 | 0 | **0** |
> > | 192 | 0 | **0** |
> > | 256 | 0 | **0** |
> > | 320 | 0 | **0** |
> > | 384 | 0 | **0** |
> > | 448 | 0 | **0** |
> >
> > Med 512 words i main memory og 64 cache-linjer er der præcis 512 / 64 = **8 words** der konkurrerer om hver cache-linje.
>
> > [!warning] Konsekvens — collision
> >
> > Hvis programmet skiftevis bruger to adresser, der mappes til samme linje (fx 0 og 64), opstår der en **collision**: hver gang det ene word loades, smides det andet ud af cachen. Det giver dårlig cache-performance og er argumentet for **set-associative** eller **fully-associative** mapping.

---

## Question 5 (1 point)

> [!question] Samme cache-specifikation. Question c: Forklar betydningen af udsagnet "at any time, the cache contains only a copy of a portion of the main memory"

> [!success] Forklaring
>
> Cachen er **meget mindre** end hovedhukommelsen (her: 64 words vs. 512 words = 1/8). Den kan derfor kun rumme en **delmængde** af hovedhukommelsen ad gangen — typisk de senest brugte data, som programmet sandsynligvis vil bruge igen (lokalitetsprincip). Når CPU'en læser fra cachen, læses i virkeligheden en **kopi** af det data, der ligger i hovedhukommelsen; selve "originalen" bliver i hovedhukommelsen, og ved opdatering skal de to holdes synkrone (write-through eller write-back).

> [!note]- Detaljeret forklaring
>
> > [!abstract] Tre konsekvenser af udsagnet
> >
> > | Konsekvens | Forklaring |
> > |---|---|
> > | **Replacement** | Når cachen er fuld og en ny linje skal hentes ind, skal en eksisterende linje smides ud (LRU, FIFO, random). |
> > | **Cache miss** | Hvis det ønskede data ikke er i cachen, skal det først hentes fra hovedhukommelsen — det er langsommere. |
> > | **Coherence** | Hvis cache-linjen er blevet skrevet til og adskiller sig fra hovedhukommelsen, skal de bringes i overensstemmelse igen (write-back på eviction eller write-through ved hver skrivning). |
>
> > [!info] Lokalitetsprincippet — hvorfor cachen virker
> >
> > | Type | Beskrivelse | Eksempel |
> > |---|---|---|
> > | **Temporal locality** | Data, der lige er blevet brugt, bliver sandsynligvis brugt igen snart | Loop-tæller, flag-variabel |
> > | **Spatial locality** | Naboer til netop læste data bliver sandsynligvis også læst snart | Array-traversal, instruktions-fetch |
> >
> > Cachen udnytter begge: den henter en hel linje (ikke kun ét word) ind ved et miss, og den beholder data, der lige er blevet brugt.
>
> > [!warning] Hit ratio
> >
> > Cachens effektivitet måles ved **hit ratio** = (antal cache hits) / (antal hukommelses-adgange). En typisk L1-cache rammer 95-99% af adgangene — derfor virker cachen, selvom den kun holder en lille del af hovedhukommelsen.

---

## Summary

> [!tldr] Quick Answers
>
> | Q | Topic | Answer | Key Concept |
> |---|---|---|---|
> | 1 | DMA forkortelse | Direct Memory Access | I/O-overførsel uden om CPU'en |
> | 2 | DMA-princip | DMA-controller overtager bussen, CPU programmerer + får interrupt | Aflaster CPU, bulk-overførsel |
> | 3 | Word 0 → cache-indeks | indeks 0000 | `address mod cache_size` |
> | 4 | Andre words på samme linje som word 0 | 64, 128, 192...448 | Multipla af cache-størrelsen (64) |
> | 5 | "Kun en kopi af en del" | Cachen rummer en delmængde med replacement, miss og coherence | Lokalitetsprincippet driver hit ratio |

---

> [!nav]
> [[Quiz 10|← Quiz 10]] | [[Quiz before lection 11|Current]]
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
