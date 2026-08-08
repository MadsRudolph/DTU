---
course: "62711"
course-name: "Digital Systems Design"
type: exercise
tags: [DSD, exercise]
---
# Opg 2 - Digital Arithmetic

> [!abstract] Exercise Overview
> Binary number representations and 2's complement arithmetic.
> Reference: [[Lecture 01 - Digital Arithmetic]]

> [!info] Files
> - Exercise description: [opg2.doc](file:///C:/Users/Mads2/DTU/Obsidian/Courses/62711%20Digital%20Systems%20Design/Exercises/Descriptions/opg2.doc)
> - Textbook: [[Logic and Computer Design Fundamentals 5th Edition.pdf|Mano & Ciletti, 5th ed.]]

---

## 2.1 Number Representations

> [!question] Express -56, -177, -1003, and -7586 in Unsigned, Signed-magnitude, Ones-complement, Twos-complement, and Biased representation. Note the number of bits needed.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=184|Textbook, Section 3-11, p. 167-168]]

### -56

| Representation | Binary | Bits |
|----------------|--------|------|
| Unsigned | N/A (negative) | -- |
| Signed-magnitude | 1111000 | 7 |
| Ones-complement | 1000111 | 7 |
| Twos-complement | 1001000 | 7 |
| Biased ($2^6 - 1 = 63$) | 0000111 ($-56 + 63 = 7$) | 7 |

> [!note]- Conversion
> $56 = 32 + 16 + 8 = 111000_2$ (6 bits)
> Need 7 bits for signed representations (sign bit + 6 magnitude bits).
> - Signed-mag: sign=1, magnitude=111000
> - Ones-comp: +56 in 7 bits = 0111000, invert = 1000111
> - Twos-comp: 1000111 + 1 = 1001000
> - Biased: $-56 + 63 = 7 = 0000111_2$

### -177

| Representation | Binary | Bits |
|----------------|--------|------|
| Unsigned | N/A (negative) | -- |
| Signed-magnitude | 1 10110001 | 9 |
| Ones-complement | 101001110 | 9 |
| Twos-complement | 101001111 | 9 |
| Biased ($2^8 - 1 = 255$) | 001001110 ($-177 + 255 = 78$) | 9 |

> [!note]- Conversion
> $177 = 128 + 32 + 16 + 1 = 10110001_2$ (8 bits)
> Need 9 bits for signed representations (sign bit + 8 magnitude bits).
> - Signed-mag: sign=1, magnitude=10110001
> - Ones-comp: +177 in 9 bits = 010110001, invert = 101001110
> - Twos-comp: 101001110 + 1 = 101001111
> - Biased: $-177 + 255 = 78 = 001001110_2$

### -1003

| Representation | Binary | Bits |
|----------------|--------|------|
| Unsigned | N/A (negative) | -- |
| Signed-magnitude | 1 1111101011 | 11 |
| Ones-complement | 10000010100 | 11 |
| Twos-complement | 10000010101 | 11 |
| Biased ($2^{10} - 1 = 1023$) | 00000010100 ($-1003 + 1023 = 20$) | 11 |

> [!note]- Conversion
> $1003 = 512 + 256 + 128 + 64 + 32 + 8 + 2 + 1 = 1111101011_2$ (10 bits)
> Need 11 bits for signed representations.
> - Ones-comp: 01111101011 inverted = 10000010100
> - Twos-comp: 10000010100 + 1 = 10000010101
> - Biased: $-1003 + 1023 = 20 = 00000010100_2$

### -7586

| Representation | Binary | Bits |
|----------------|--------|------|
| Unsigned | N/A (negative) | -- |
| Signed-magnitude | 1 1110110100010 | 14 |
| Ones-complement | 10001001011101 | 14 |
| Twos-complement | 10001001011110 | 14 |
| Biased ($2^{13} - 1 = 8191$) | 00001001011101 ($-7586 + 8191 = 605$) | 14 |

> [!note]- Conversion
> $7586 = 4096 + 2048 + 1024 + 256 + 128 + 32 + 2 = 1110110100010_2$ (13 bits)
> Need 14 bits for signed representations.
> - Ones-comp: 01110110100010 inverted = 10001001011101
> - Twos-comp: 10001001011101 + 1 = 10001001011110
> - Biased: $-7586 + 8191 = 605 = 00001001011101_2$

---

## 2.2 Unsigned Subtraction via 2's Complement

> [!question] Perform the indicated subtraction with unsigned binary numbers by taking the 2's complement of the subtrahend. Use 0-extension to equalize lengths.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=178|Textbook, Section 3-10, p. 161-165]]

> [!tip] Method
> 1. 0-extend the subtrahend B to match the length of the minuend A
> 2. Take the 2's complement of B: invert all bits, add 1
> 3. Add A + (-B)
> 4. If carry out = 1: result is positive and correct
> 5. If carry out = 0: result is negative (borrow occurred)

### a) $11010_2 - 10001_2$ (5 bits)

$A = 11010\ (26),\quad B = 10001\ (17)$

```
Carry:          1 1 1 0 0
Minuend A:      1 1 0 1 0
-B (2's comp):  0 1 1 1 1
              ───────────
A + (-B):    (1)0 1 0 0 1
```

Cout = **1** → result is positive: $01001_2 = 9$

> [!success] $26 - 17 = 9$ ✓

### b) $11110_2 - 110_2$ (5 and 3 bits)

$A = 11110\ (30),\quad B = 110\ (6)$. 0-extend B to 5 bits: $00110$

```
Carry:          1 1 0 0 0
Minuend A:      1 1 1 1 0
-B (2's comp):  1 1 0 1 0
              ───────────
A + (-B):    (1)1 1 0 0 0
```

Cout = **1** → result is positive: $11000_2 = 24$

> [!success] $30 - 6 = 24$ ✓

### c) $1111110_2 - 1111110_2$ (7 bits)

$A = 1111110\ (126),\quad B = 1111110\ (126)$

```
Carry:          1 1 1 1 1 0 0
Minuend A:      1 1 1 1 1 1 0
-B (2's comp):  0 0 0 0 0 1 0
              ─────────────────
A + (-B):    (1)0 0 0 0 0 0 0
```

Cout = **1** → result is positive: $0000000_2 = 0$

> [!success] $126 - 126 = 0$ ✓

### d) $101001_2 - 101_2$ (6 and 3 bits)

$A = 101001\ (41),\quad B = 101\ (5)$. 0-extend B to 6 bits: $000101$

```
Carry:          0 0 0 0 0 0
Minuend A:      1 0 1 0 0 1
-B (2's comp):  1 1 1 0 1 1
              ───────────────
A + (-B):    (1)1 0 0 1 0 0
```

Cout = **1** → result is positive: $100100_2 = 36$

> [!success] $41 - 5 = 36$ ✓

---

## 2.3 Signed (2's Complement) Subtraction

> [!question] Repeat problem 2.2, assuming the numbers are 2's complement signed. Use sign-extension. Indicate overflow for complement operations and overall.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=186|Textbook, Ex. 3-21 & 3-22, p. 169]] | [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=188|Overflow, p. 171-172]]

> [!tip] Method
> - **Sign-extend** (not 0-extend) the shorter operand to match lengths
> - **Overflow** = $C_{out} \oplus C_{out-1}$ (carry out of MSB XOR carry into MSB)
> - Complement overflow only occurs if B = $-2^{n-1}$ (most negative value)

> [!warning] Common mistake: 0-extension vs sign-extension
> Using 0-extension instead of sign-extension changes the value of negative numbers (e.g. $110_2 = -2$ in 3-bit signed, but 0-extended to $00110_2 = +6$ in 5-bit). This leads to computing a completely different subtraction and incorrect overflow answers.
> Per the [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=188|textbook (Mano & Ciletti, 5th ed., p. 171)]]: *"An overflow cannot occur for an addition if one number is positive and the other is negative."* Since $A - B = A + (-B)$, subtracting two negatives always produces a positive+negative addition, which **cannot overflow**.

### a) $11010_2 - 10001_2$ (5-bit signed)

$A = 11010\ (-6),\quad B = 10001\ (-15),\quad -B = 01111\ (+15)$

```
Carry:          1 1 1 0 0
A:              1 1 0 1 0
-B:             0 1 1 1 1
              ───────────
A + (-B):    (1)0 1 0 0 1
```

$C_{out} = 1,\ C_{out-1} = 1 \Rightarrow$ Overflow = $1 \oplus 1 = 0$ — **No overflow**
Complement overflow: No ($-15$ is not $-2^4 = -16$)

> [!success] $-6 - (-15) = -6 + 15 = +9 = 01001_2$ ✓

### b) $11110_2 - 110_2$ (5-bit and 3-bit signed)

$A = 11110\ (-2),\quad B = 110\ (-2)$. Sign-extend B to 5 bits: $11110$
$-B = 00010\ (+2)$

```
Carry:          1 1 1 0 0
A:              1 1 1 1 0
-B:             0 0 0 1 0
              ───────────
A + (-B):    (1)0 0 0 0 0
```

$C_{out} = 1,\ C_{out-1} = 1 \Rightarrow$ Overflow = $0$ — **No overflow**
Complement overflow: No

> [!success] $-2 - (-2) = 0 = 00000_2$ ✓

### c) $1111110_2 - 1111110_2$ (7-bit signed)

$A = 1111110\ (-2),\quad B = 1111110\ (-2),\quad -B = 0000010\ (+2)$

```
Carry:          1 1 1 1 1 0 0
A:              1 1 1 1 1 1 0
-B:             0 0 0 0 0 1 0
              ─────────────────
A + (-B):    (1)0 0 0 0 0 0 0
```

$C_{out} = 1,\ C_{out-1} = 1 \Rightarrow$ Overflow = $0$ — **No overflow**
Complement overflow: No

> [!success] $-2 - (-2) = 0 = 0000000_2$ ✓

### d) $101001_2 - 101_2$ (6-bit and 3-bit signed)

$A = 101001\ (-23),\quad B = 101\ (-3)$. Sign-extend B to 6 bits: $111101$
$-B = 000011\ (+3)$

```
Carry:          0 0 0 0 0 0
A:              1 0 1 0 0 1
-B:             0 0 0 0 1 1
              ───────────────
A + (-B):    (0)1 0 1 1 0 0
```

$C_{out} = 0,\ C_{out-1} = 0 \Rightarrow$ Overflow = $0$ — **No overflow**
Complement overflow: No

> [!success] $-23 - (-3) = -23 + 3 = -20 = 101100_2$ ✓
> Verify: flip $101100 \to 010011$, $+1 \to 010100 = 20$, so $-20$

---

## 2.4 Signed Arithmetic

> [!question] Perform $(+36) + (-24)$ and $(-35) - (-24)$ in binary using 2's complement (7 bits).
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=186|Textbook, Ex. 3-21 & 3-22, p. 169]]

### a) $(+36) + (-24)$

$+36 = 0100100,\quad -24 = 1101000$

> [!note]- Conversion
> $36 = 100100_2$, in 7-bit signed: $0100100$
> $24 = 011000_2$, 2's complement: $0011000 \to 1100111 + 1 = 1101000$

```
Carry:          1 1 0 0 0 0 0
A = +36:        0 1 0 0 1 0 0
B = -24:        1 1 0 1 0 0 0
              ─────────────────
A + B:       (1)0 0 0 1 1 0 0
```

$C_{out} = 1,\ C_{out-1} = 1 \Rightarrow$ Overflow = $0$ — **No overflow**

> [!success] $36 + (-24) = +12 = 0001100_2$ ✓

### b) $(-35) - (-24)$

$-35 = 1011101,\quad -24 = 1101000,\quad -(-24) = 0011000\ (+24)$

> [!note]- Conversion
> $35 = 100011_2$, 2's complement: $0100011 \to 1011100 + 1 = 1011101$
> $-(-24) =$ 2's complement of $1101000 = 0010111 + 1 = 0011000$

```
Carry:          0 0 1 1 0 0 0
A = -35:        1 0 1 1 1 0 1
-B = +24:       0 0 1 1 0 0 0
              ─────────────────
A + (-B):    (0)1 1 1 0 1 0 1
```

$C_{out} = 0,\ C_{out-1} = 0 \Rightarrow$ Overflow = $0$ — **No overflow**

> [!success] $-35 - (-24) = -11 = 1110101_2$ ✓
> Verify: flip $1110101 \to 0001010$, $+1 \to 0001011 = 11$, so $-11$

---

## 2.5 Signed Addition/Subtraction with Overflow Detection

> [!question] The following 6-bit binary numbers have a sign in the leftmost position, negatives in 2's complement. Perform the operations and indicate overflow.
> Reference: [[Logic and Computer Design Fundamentals 5th Edition.pdf#page=188|Textbook, Overflow, p. 171-172]]

> [!important] Overflow Rule
> Overflow = $C_{out} \oplus C_{out-1}$ (carry out of MSB $\neq$ carry into MSB)

### a) $100111 + 111000$

$A = 100111\ (-25),\quad B = 111000\ (-8)$

```
Carry:          1 0 0 0 0 0
A:              1 0 0 1 1 1
B:              1 1 1 0 0 0
              ───────────────
A + B:       (1)0 1 1 1 1 1
```

$C_{out} = 1,\ C_{out-1} = 0 \Rightarrow$ **Overflow = 1**

> [!warning] Overflow!
> $-25 + (-8) = -33$, which is outside the 6-bit range $[-32, +31]$.
> The result $011111 = +31$ is incorrect due to overflow.

### b) $001011 + 100110$

$A = 001011\ (+11),\quad B = 100110\ (-26)$

```
Carry:          0 0 1 1 0 0
A:              0 0 1 0 1 1
B:              1 0 0 1 1 0
              ───────────────
A + B:       (0)1 1 0 0 0 1
```

$C_{out} = 0,\ C_{out-1} = 0 \Rightarrow$ Overflow = $0$ — **No overflow**

> [!success] $11 + (-26) = -15 = 110001_2$ ✓
> One positive + one negative → overflow **cannot** occur ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=188|Mano & Ciletti, p. 171]]).

### c) $110001 - 101110$

$A = 110001\ (-15),\quad B = 101110\ (-18),\quad -B = 010010\ (+18)$

```
Carry:          1 1 0 0 0 0
A:              1 1 0 0 0 1
-B:             0 1 0 0 1 0
              ───────────────
A + (-B):    (1)0 0 0 0 1 1
```

$C_{out} = 1,\ C_{out-1} = 1 \Rightarrow$ Overflow = $0$ — **No overflow**

> [!success] $-15 - (-18) = +3 = 000011_2$ ✓

### d) $101110 - 010101$

$A = 101110\ (-18),\quad B = 010101\ (+21),\quad -B = 101011\ (-21)$

```
Carry:          0 1 1 1 0 0
A:              1 0 1 1 1 0
-B:             1 0 1 0 1 1
              ───────────────
A + (-B):    (1)0 1 1 0 0 1
```

$C_{out} = 1,\ C_{out-1} = 0 \Rightarrow$ **Overflow = 1**

> [!warning] Overflow!
> $-18 - 21 = -39$, which is outside the 6-bit range $[-32, +31]$.
> The result $011001 = +25$ is incorrect due to overflow.
> Both operands in the addition are negative ($-18 + (-21)$), so overflow **can** occur ([[Logic and Computer Design Fundamentals 5th Edition.pdf#page=188|Mano & Ciletti, p. 171]]) — and it does, since $-39 < -32$.

---

## Summary

| Problem | Operation | Result | Overflow |
|---------|-----------|--------|----------|
| 2.2a | $26 - 17$ (unsigned) | 9 | No |
| 2.2b | $30 - 6$ (unsigned) | 24 | No |
| 2.2c | $126 - 126$ (unsigned) | 0 | No |
| 2.2d | $41 - 5$ (unsigned) | 36 | No |
| 2.3a | $-6 - (-15)$ (signed) | +9 | No |
| 2.3b | $-2 - (-2)$ (signed) | 0 | No |
| 2.3c | $-2 - (-2)$ (signed) | 0 | No |
| 2.3d | $-23 - (-3)$ (signed) | -20 | No |
| 2.4a | $36 + (-24)$ | +12 | No |
| 2.4b | $-35 - (-24)$ | -11 | No |
| 2.5a | $-25 + (-8)$ | -33 (overflow!) | **Yes** |
| 2.5b | $11 + (-26)$ | -15 | No |
| 2.5c | $-15 - (-18)$ | +3 | No |
| 2.5d | $-18 - 21$ | -39 (overflow!) | **Yes** |

---

> [!nav]
> &nbsp;
>
> [[62711 Digital Systems Design|62711 Home]]
>
> &nbsp;
