# Writing Strategy for Assignment 2
## Staying Within 1500 Words / 3 Pages

### Word Budget Allocation

With 6 exercises and ~1500 words total, allocate approximately:
- **Exercise 1 (W/L ratio):** 200-250 words
- **Exercise 2 (Feedback):** 200-250 words  
- **Exercise 3 (Pole placement):** 200-250 words
- **Exercise 4 (Bandgap):** 250-300 words
- **Exercise 5 (Two-stage opamp):** 250-300 words ⭐ (has circuit)
- **Exercise 6 (CMRR):** 250-300 words ⭐ (has circuit)

**Reserve ~200 words for equations, figure captions, and section headers**

### Key Principles for Condensing NotebookLM Content

1. **Be Selective, Not Exhaustive**
   - Don't include everything from NotebookLM
   - Focus on what the question specifically asks
   - Prioritize concepts over derivations

2. **Use Bullet Points Strategically**
   - Convert prose explanations into concise bullet lists
   - Each bullet should be 1-2 lines maximum
   - Use parallel structure (all bullets same format)

3. **Equations Over Words**
   - One equation can replace a paragraph
   - Show key relationships, skip derivations
   - Use inline math ($...$) to save space

4. **Combine Related Concepts**
   - Group advantages together
   - Group disadvantages together
   - Don't repeat similar points

5. **Cut Redundancy**
   - Say things once
   - Don't explain what equations already show
   - Trust the reader's technical background

### Example Transformation

**NotebookLM (Too Long):**
> "The transconductance is given by gm = √(2μCox(W/L)ID). If ID is fixed (by a current source), increasing W increases gm proportional to √W. If VGS is fixed, gm increases linearly with W. The transconductance determines the voltage gain of the amplifier stage."

**Condensed Version:**
> "Increasing W raises gm (∝ √W for fixed ID, ∝ W for fixed VGS), improving voltage gain."

**Savings:** 40 words → 14 words (65% reduction)

### Formatting Tips to Save Space

1. **Use Compact Lists:**
   ```latex
   \textbf{Pros:} Higher gain, better matching, lower noise
   \textbf{Cons:} Larger area, higher power, more parasitics
   ```
   Instead of separate paragraphs for each point.

2. **Combine Short Sections:**
   Don't make a new subsection for 2 sentences. Merge related content.

3. **Use Inline Math:**
   "The gain is $A_v = g_m r_o$" instead of a display equation when possible.

4. **Abbreviate When Clear:**
   Use "TC" for temperature coefficient, "PM" for phase margin after first use.

5. **Skip Obvious Context:**
   Don't write "Based on the analysis above" or "As we can see" - just state facts.

### What to Cut from NotebookLM Responses

For each exercise, prioritize cutting:
1. ❌ Historical context (how models were developed)
2. ❌ Detailed derivations (show result only)
3. ❌ Multiple examples (pick one if any)
4. ❌ Repetitive explanations
5. ❌ "Nice to know" vs "need to know"

Keep:
1. ✅ Direct answers to the question
2. ✅ Key equations (1-3 per exercise)
3. ✅ Concrete trade-offs (pros/cons)
4. ✅ Practical design guidelines
5. ✅ Numerical values when relevant

### Structure Template for Each Exercise

```latex
\section{Exercise X – Title}

[1-2 sentences introducing the concept]

\subsection*{Key Theory/Principle}
[Core equations and definitions - 3-4 lines]

\subsection*{Analysis/Effects}
[Bullet points of main effects]
\textbf{Advantages:} [condensed list]
\textbf{Disadvantages:} [condensed list]

\subsection*{Conclusion/Guidelines}
[1-2 sentences of practical insight]
```

### Circuit Exercises (5 & 6) - Special Considerations

Since these have figures:
- Let the circuit diagram "speak" - don't describe every component
- Focus on analysis and trade-offs
- Reference specific transistors by name (M1, M2, etc.)
- Use the actual W/L ratios shown in the circuit

Example:
❌ "The differential pair consists of transistors M1 and M2, which convert the differential input voltage into a differential current..."
✅ "M1-M2 convert differential voltage to current with gm1 = √(2μCox(W/L)ID)."

### Quality Control Checklist

Before finalizing each exercise, ask:
1. ☐ Did I directly answer what was asked?
2. ☐ Are there any redundant sentences?
3. ☐ Can any prose be converted to equations or bullets?
4. ☐ Did I cut all the "fluff" words?
5. ☐ Is every equation necessary?
6. ☐ Would a technical reader understand this?

### Final Polish

After writing all exercises:
1. Run word count on each section
2. Identify the longest sections and trim 10-20%
3. Ensure parallel structure across similar sections
4. Check that equations use consistent notation
5. Verify all symbols are defined (at least once)

### Example: Before & After

**Before (85 words):**
"Negative feedback is a technique where a fraction of the output signal is fed back to the input and subtracted from the external input signal. This process reduces the overall gain of the system but provides numerous benefits including improved linearity, reduced distortion, better stability of the gain with respect to component variations, and the ability to control input and output impedances. The closed-loop gain is determined primarily by the feedback network rather than the amplifier itself."

**After (32 words):**
"Negative feedback subtracts a fraction β of the output from the input, reducing gain by (1+Aβ) but improving linearity, gain stability, and impedance control. The closed-loop gain ACL ≈ 1/β when Aβ >> 1."

**Savings:** 62% reduction

---

Remember: Your assignment is judged on technical accuracy and understanding, not word count. Quality over quantity!
