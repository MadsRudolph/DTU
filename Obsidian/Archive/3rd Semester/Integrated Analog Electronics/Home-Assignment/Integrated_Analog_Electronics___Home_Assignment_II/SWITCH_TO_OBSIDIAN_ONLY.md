# Switch to Obsidian-Only Viewing

If you want to **disable SumatraPDF** and only view in Obsidian:

## Steps:

1. Open `.vscode/settings.json`
2. Change this line:
   ```json
   "latex-workshop.view.pdf.viewer": "external",
   ```
   To:
   ```json
   "latex-workshop.view.pdf.viewer": "none",
   ```

3. After building, manually open in Obsidian using the link

## Trade-offs:

**Pros:**
- ✅ Everything in one app (Obsidian)
- ✅ PDF alongside your notes

**Cons:**
- ❌ No auto-open after compilation
- ❌ No forward/inverse search
- ❌ Manual refresh needed in Obsidian sometimes

## Recommended: Keep SumatraPDF

Use SumatraPDF when editing LaTeX, Obsidian when studying!
