# LaTeX Workshop PDF Viewer - Fix Caching Issues

## Problem
LaTeX Workshop's built-in PDF viewer in VSCode sometimes caches old versions of your PDF and doesn't refresh properly after recompiling.

## Solutions

### Solution 1: Force Refresh in VSCode (Quickest)
1. In VSCode, with the PDF tab open
2. Press **Ctrl+Shift+P** (Command Palette)
3. Type: `LaTeX Workshop: View LaTeX PDF`
4. Select it to force reload the PDF

OR

1. **Close the PDF tab** in VSCode
2. **Ctrl+Shift+P** → `LaTeX Workshop: View LaTeX PDF`

---

### Solution 2: Clear Cache and Rebuild
Run this in VSCode terminal:
```bash
rm -f main.aux main.toc main.out main.fls main.fdb_latexmk main.synctex.gz
latexmk -pdf -interaction=nonstopmode main.tex
```

Then refresh the PDF viewer (Solution 1).

---

### Solution 3: Use External PDF Viewer (Recommended)
Configure LaTeX Workshop to use an external viewer instead of the built-in one.

**Add to VSCode settings.json:**
```json
{
    "latex-workshop.view.pdf.viewer": "external",
    "latex-workshop.view.pdf.external.synctex.command": "C:/Program Files/SumatraPDF/SumatraPDF.exe",
    "latex-workshop.view.pdf.external.synctex.args": [
        "-forward-search",
        "%TEX%",
        "%LINE%",
        "-reuse-instance",
        "%PDF%"
    ]
}
```

**Install SumatraPDF (free, lightweight):**
- Download: https://www.sumatrapdfreader.org/
- Automatically refreshes when PDF changes
- No caching issues

---

### Solution 4: Quick Fix Script
Run this when PDF looks broken:
```bash
rm main.pdf && latexmk -pdf main.tex
```

This deletes the old PDF before rebuilding.

---

## Prevention

### Use latexmk for All Compilations
Instead of running `pdflatex` manually:
```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

This automatically:
- Runs pdflatex multiple times (builds TOC correctly)
- Cleans up on errors
- Generates proper cross-references

### VSCode LaTeX Workshop Settings
Add to `.vscode/settings.json` in your project:
```json
{
    "latex-workshop.latex.autoBuild.run": "onSave",
    "latex-workshop.latex.clean.enabled": true,
    "latex-workshop.latex.clean.fileTypes": [
        "*.aux",
        "*.fdb_latexmk",
        "*.fls",
        "*.synctex.gz",
        "*.out",
        "*.toc"
    ],
    "latex-workshop.latex.recipe.default": "latexmk",
    "latex-workshop.latex.recipes": [
        {
            "name": "latexmk",
            "tools": [
                "latexmk"
            ]
        }
    ],
    "latex-workshop.latex.tools": [
        {
            "name": "latexmk",
            "command": "latexmk",
            "args": [
                "-pdf",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        }
    ]
}
```

---

## Current Status

✅ **main.pdf** - Fixed and working (387 KB, 5 pages)
✅ **Home_Assignment_II_Submission.pdf** - Synced to Obsidian

The LaTeX source files are all correct. If you see issues:
1. Try Solution 1 (force refresh)
2. If that doesn't work, use Solution 3 (external viewer)

---

## Why This Happens

LaTeX Workshop caches PDFs in memory and sometimes doesn't detect file changes properly, especially when:
- Auxiliary files (.aux, .toc) get corrupted
- PDF is open when you delete/recreate it
- Multiple rapid recompilations happen
- Windows file locking interferes

External viewers like SumatraPDF handle this better because they reload whenever the file timestamp changes.
