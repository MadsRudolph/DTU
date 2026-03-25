# Lecture Note Generation

Use the structured recording data in `34722_untitled_20260325_163722.json` to generate comprehensive
lecture notes for **34722 Linear Control Design 1**, Lesson 8.

## Source Data
- Structured transcript with timestamps: `34722_untitled_20260325_163722.json`
- The lecture slides are: [[Lecture_08_PI_LEAD_design.pdf]]
- The `slide_sections` array groups the transcript by slide — use these as the primary structure

## Instructions
- Organize notes by slide, using the slide_sections from the JSON
- Include timestamps as references (e.g., [00:45])
- Fix obvious transcription errors and expand abbreviations
- Add clear section headings based on slide transitions and content
- Format equations in LaTeX ($...$)
- Use Obsidian-compatible markdown with [[wiki-links]]
- If speaker labels are present, note when students ask questions
- Summarize key takeaways at the end
- Keep the tone academic but accessible

## Output Format
Obsidian markdown note with YAML frontmatter, ready to save as `Lesson 8.md`
