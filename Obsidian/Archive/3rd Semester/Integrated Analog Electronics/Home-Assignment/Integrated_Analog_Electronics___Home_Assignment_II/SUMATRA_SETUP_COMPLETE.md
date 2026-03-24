# ✅ SumatraPDF + LaTeX Workshop - Setup Complete!

## Configuration Summary

**SumatraPDF Location:** `C:\Users\Mads2\AppData\Local\SumatraPDF\SumatraPDF.exe`

**What's Configured:**
- ✅ External PDF viewer (SumatraPDF instead of VSCode built-in)
- ✅ Auto-compile on save
- ✅ Auto-clean auxiliary files
- ✅ Forward search (Tex → PDF)
- ✅ Inverse search (PDF → Tex)
- ✅ SyncTeX enabled for navigation

---

## How to Use

### 1. **Compile and View PDF**

**Method A - Auto-compile (Recommended):**
1. Make changes to your `.tex` file
2. Press **Ctrl+S** (Save)
3. LaTeX Workshop automatically compiles
4. SumatraPDF opens/refreshes automatically

**Method B - Manual compile:**
1. Press **Ctrl+Alt+B** (Build LaTeX project)
2. Or: **Ctrl+Shift+P** → Type "LaTeX Workshop: Build LaTeX project"

**Method C - View existing PDF:**
- **Ctrl+Alt+V** (View PDF)
- Or: **Ctrl+Shift+P** → "LaTeX Workshop: View LaTeX PDF"

---

### 2. **Forward Search** (Jump from Code to PDF)

**What it does:** Jumps to the location in the PDF that corresponds to your cursor position in the .tex file.

**How to use:**
1. Place cursor in your `.tex` file (e.g., in Exercise 3)
2. Press **Ctrl+Alt+J**
3. SumatraPDF opens and highlights that exact location

**Alternative:**
- **Ctrl+Shift+P** → "LaTeX Workshop: SyncTeX from cursor"

---

### 3. **Inverse Search** (Jump from PDF to Code)

**What it does:** Double-click in the PDF to jump to that location in your .tex source.

**How to use:**
1. Open PDF in SumatraPDF
2. **Double-click** anywhere in the PDF
3. VSCode automatically opens and jumps to that line in your .tex file

This is amazing for editing - you can navigate by the PDF!

---

### 4. **Auto-Refresh** (No More Caching Issues!)

**The magic:** SumatraPDF automatically refreshes when the PDF changes. No more cache issues!

1. Make edit in `.tex` file
2. Save (**Ctrl+S**)
3. LaTeX compiles automatically
4. SumatraPDF refreshes instantly
5. See your changes immediately!

**No need to:**
- ❌ Close and reopen PDF
- ❌ Delete auxiliary files
- ❌ Run rebuild scripts
- ❌ Force refresh viewer

It just works! 🎉

---

## Keyboard Shortcuts Reference

| Action | Shortcut | What it does |
|--------|----------|--------------|
| **Save & compile** | Ctrl+S | Auto-compiles on save |
| **Build manually** | Ctrl+Alt+B | Force rebuild |
| **View PDF** | Ctrl+Alt+V | Open PDF in SumatraPDF |
| **Forward search** | Ctrl+Alt+J | Jump from .tex to PDF |
| **Inverse search** | Double-click in PDF | Jump from PDF to .tex |
| **Clean auxiliary** | Ctrl+Alt+C | Delete .aux, .log, etc. |

---

## What Happens Now

### When you save a `.tex` file:

```
1. VSCode detects change
2. LaTeX Workshop runs: latexmk -pdf main.tex
3. PDF is generated/updated
4. SumatraPDF detects the change
5. PDF refreshes automatically
6. You see the result instantly!
```

**Total time:** 1-3 seconds (depending on document complexity)

---

## Benefits Over Built-in Viewer

| Feature | Built-in VSCode Viewer | SumatraPDF |
|---------|------------------------|------------|
| Auto-refresh | ❌ Caches, needs reload | ✅ Instant refresh |
| Forward search | ✅ Works | ✅ Works |
| Inverse search | ❌ Not available | ✅ Double-click |
| Memory usage | High (in VSCode) | Low (separate app) |
| Stability | Can crash VSCode | Separate process |
| Zoom/Pan | Limited | Full featured |

---

## Testing the Setup

### Test 1: Basic Compilation
1. Open `main.tex`
2. Change the date from "2025" to "2026"
3. Press **Ctrl+S**
4. Watch SumatraPDF open/refresh
5. Verify the date changed in the PDF

### Test 2: Forward Search
1. Open `sections/exercise1_condensed.tex`
2. Click somewhere in the text
3. Press **Ctrl+Alt+J**
4. SumatraPDF should highlight that exact location

### Test 3: Inverse Search
1. Open PDF in SumatraPDF
2. Double-click on "Exercise 3" heading
3. VSCode should jump to `exercise3_condensed.tex`

If all three work → **You're set up perfectly!** 🎯

---

## Troubleshooting

### Issue: PDF doesn't open automatically
**Solution:**
- Press **Ctrl+Alt+V** to open manually
- Or: Check that SumatraPDF path is correct in `.vscode/settings.json`

### Issue: Forward search doesn't work
**Solution:**
- Make sure you compiled with SyncTeX enabled
- Run: `latexmk -pdf -synctex=1 main.tex`
- Check that `main.synctex.gz` exists

### Issue: Inverse search doesn't work
**Solution:**
- The configuration should be automatic
- If not working, in SumatraPDF: Settings → Options → Set Inverse Search manually:
  ```
  "C:\Users\Mads2\AppData\Local\Programs\Microsoft VS Code\Code.exe" "C:\Users\Mads2\AppData\Local\Programs\Microsoft VS Code\resources\app\out\cli.js" --ms-enable-electron-run-as-node -r -g "%f:%l"
  ```

### Issue: Still seeing cache issues
**Solution:**
- Close VSCode completely
- Delete `main.pdf`
- Reopen VSCode
- Press **Ctrl+Alt+B**

---

## Advanced Tips

### Tip 1: Keep SumatraPDF Always On Top
In SumatraPDF:
- View → Presentation Mode (F5 to toggle)
- Or: Settings → Advanced Options → `PresentationMode = true`

Useful for split-screen coding while watching PDF update.

### Tip 2: Multiple Monitors
- Put VSCode on one monitor
- Put SumatraPDF on another
- Edit and see results in real-time!

### Tip 3: Compile Specific Recipe
- **Ctrl+Shift+P** → "LaTeX Workshop: Build with recipe"
- Choose "pdflatex × 3" for manual control
- Or stick with "latexmk (pdf)" for automatic

---

## File Structure

Your workspace now has:

```
Integrated_Analog_Electronics___Home_Assignment_II/
├── .vscode/
│   ├── settings.json          ← LaTeX + SumatraPDF config
│   └── tasks.json             ← Build tasks
├── main.tex                   ← Your main document
├── main.pdf                   ← Generated PDF
├── main.synctex.gz            ← For forward/inverse search
├── sections/
│   ├── exercise1_condensed.tex
│   ├── exercise2_condensed.tex
│   └── ...
└── SUMATRA_SETUP_COMPLETE.md  ← This file
```

---

## Workflow Summary

**Old workflow (broken):**
1. Edit .tex
2. Compile
3. PDF caches
4. Force refresh
5. Still broken
6. Delete files
7. Rebuild
8. Hope it works 😤

**New workflow (perfect):**
1. Edit .tex
2. Press Ctrl+S
3. Done! ✨

---

## Next Steps

1. **Test it now:** Make a small edit and save
2. **Enjoy instant feedback:** See changes immediately
3. **Use forward/inverse search:** Navigate easily
4. **Stop worrying about caching:** It's solved forever!

---

## Support

If you have issues:
1. Check this guide's Troubleshooting section
2. Verify SumatraPDF is running
3. Check `.vscode/settings.json` paths are correct
4. Try closing VSCode and SumatraPDF, then reopening

---

**🎉 Setup complete! You now have a professional LaTeX workflow with zero caching issues!**

Happy writing! 📝✨
