# Lecture Note Generation — Lesson 8 - Position Controller Design

Create comprehensive, study-ready lecture notes for **34722 Linear Control Design 1**, Lesson 8 - Position Controller Design.

## Source Data (read ALL of these)
- **Transcript**: `transcript.txt` — the full lecture transcription
- **Structured data**: `structured.json` — transcript with timestamps and slide markers
- **Lecture slides PDF**: [[Lecture_08_PI_LEAD_design.pdf]]
  - Read the PDF slides FIRST to understand the structure, formulas, and exact numerical values
  - The slides are the authoritative source for equations, variable names, and notation
  - Embed key slides in the notes using `![[Lecture_08_PI_LEAD_design.pdf#page=N]]` for visual reference
- **Style reference**: Read `Lesson 2 - Block Diagrams and Control Concepts.md` in the Lecture Notes folder for formatting conventions

## Critical Instructions

### 1. Use BOTH transcript AND slides
- Read the **transcript** for the lecturer's explanations, intuitions, analogies, and verbal emphasis
- Read the **PDF slides** for precise equations, exact numerical values, variable notation, and Bode plot data
- The transcript captures WHAT the lecturer said; the slides capture the EXACT math
- When the transcript says approximate numbers, prefer the exact values from slides

### 2. Organize by TOPIC, not by slide
- Group content into logical conceptual sections (e.g., "P Controller Design", "PI Controller Design")
- Do NOT create one section per slide — slides often span the same topic across multiple pages
- Use the lecturer's verbal transitions ("now let's move to...", "the next thing is...") to identify topic boundaries
- Number sections hierarchically: `## 1. Topic`, `### 1.1 Subtopic`

### 3. Include the lecturer's intuition and emphasis
- Capture WHY things work, not just the formulas
- Include the lecturer's analogies, physical interpretations, and "how to think about this"
- Note when the lecturer says something is "important", "the key point", "remember this for the exam"
- Include practical advice and engineering rules of thumb

### 4. Worked examples with exact values
- Include ALL worked examples from the lecture with step-by-step solutions
- Use the **exact numerical values** from the slides (e.g., $\omega_c = 5.29484$ rad/s, not "about 5.3")
- Show the complete calculation chain: specification → phase balance → Bode lookup → parameter calculation
- Include intermediate results

### 5. Formatting requirements
- **YAML frontmatter**:
  ```yaml
  ---
  course: "34722"
  course-name: "Linear Control Design 1"
  type: lecture-note
  lesson: 8
  tags: [LCD, lecture]
  date: YYYY-MM-DD
  ---
  ```
- **Obsidian callout boxes** — use these extensively:
  - `> [!abstract]` for lecture overview at the top
  - `> [!tip]` for practical advice, MATLAB tips, analogies
  - `> [!warning]` for common mistakes, unit confusion, exam pitfalls
  - `> [!important]` for key results and theorems
  - `> [!info]` for supplementary context or teasers for future lectures
  - `> [!example]` for related materials (slides, exercises, previous lectures)
- **LaTeX equations**: use `$$...$$` for display math, `$...$` for inline
- **Tables** for comparing concepts, parameter effects, numerical results
- **Embedded slides**: `![[Lecture_08_PI_LEAD_design.pdf#page=N]]` for key visual content (Bode plots, block diagrams, step responses)
- **MATLAB code blocks** when the lecturer shows MATLAB commands
- **Bold key terms** on first introduction

### 6. Structure template
```
# Lesson 8 - Position Controller Design

> [!abstract] Lecture Overview
> Lesson N/13 — Teacher: ...
> Topics: ...

> [!example] Related Materials
> - Slides: [[...pdf]]
> - Exercise: [[...]]
> - Previous: [[...]]

---

## 1. First Major Topic
### 1.1 Subtopic
[Content with equations, explanations, callouts]

## 2. Second Major Topic
[...]

## N. Summary / Key Takeaways
[Concise summary table or bullet points]

## N+1. MATLAB Workflow
[Practical code for the lecture's design procedures]

## N+2. Exercise Preview
[What today's exercise covers]
```

### 7. What NOT to do
- Do NOT organize by slide number
- Do NOT include timestamps in the notes (they clutter the reading experience)
- Do NOT reproduce the transcript verbatim — synthesize and restructure
- Do NOT skip the lecturer's verbal explanations in favor of just copying slide content
- Do NOT use generic placeholder text — every section should have real content
- Do NOT add emojis

## Output
Save as: `Lesson 8 - Position Controller Design.md`
