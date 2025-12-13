# Two-Version LaTeX Project - CONDENSED + DETAILED

## 📁 Project Structure

You now have **TWO versions** of your assignment that can coexist in the same Overleaf project:

```
Assignment_2/
├── main.tex                      # ⭐ CONDENSED VERSION (for submission)
├── main_detailed.tex             # 📚 DETAILED VERSION (for reference)
├── sections/
│   ├── exercise1.tex             # Detailed version (~250 words)
│   ├── exercise1_condensed.tex   # Condensed version (~130 words)
│   ├── exercise2.tex             # Detailed version (~260 words)
│   ├── exercise2_condensed.tex   # Condensed version (~140 words)
│   ├── exercise3.tex             # Detailed version (~270 words)
│   ├── exercise3_condensed.tex   # Condensed version (~150 words)
│   ├── exercise4.tex             # Detailed version (~280 words)
│   ├── exercise4_condensed.tex   # Condensed version (~140 words)
│   ├── exercise5.tex             # Detailed version (~320 words)
│   ├── exercise5_condensed.tex   # Condensed version (~140 words)
│   ├── exercise6.tex             # Detailed version (~310 words)
│   └── exercise6_condensed.tex   # Condensed version (~140 words)
└── images/
    ├── DUT.png
    ├── exercise5_circuit.png
    └── exercise6_circuit.png
```

---

## 🎯 How to Use

### For Submission (3-page version):
1. In Overleaf, set **main.tex** as the main document
2. Click "Recompile"
3. Get ~5 pages total (1 title + 1 TOC + **3 content pages**)
4. Download PDF and submit

### For Reference (detailed version):
1. In Overleaf, set **main_detailed.tex** as the main document
2. Click "Recompile"
3. Get ~17 pages total (1 title + 1 TOC + **15 content pages**)
4. Use for studying, reviewing, or as reference

---

## ⚙️ Switching Between Versions in Overleaf

### Method 1: Change Main Document (Recommended)
1. Click **Menu** (top left in Overleaf)
2. Under "Main document", select either:
   - `main.tex` → Condensed version
   - `main_detailed.tex` → Detailed version
3. Click "Recompile"

### Method 2: Quick Toggle (Advanced)
You can also temporarily edit main.tex to switch:

**Current main.tex (Condensed):**
```latex
\subfile{sections/exercise1_condensed}
\subfile{sections/exercise2_condensed}
...
```

**To get detailed, change to:**
```latex
\subfile{sections/exercise1}
\subfile{sections/exercise2}
...
```

But using main_detailed.tex is cleaner!

---

## 📊 Version Comparison

| Feature | main.tex (Condensed) | main_detailed.tex (Detailed) |
|---------|---------------------|------------------------------|
| **Purpose** | Submission | Reference/Study |
| **Total Pages** | ~5 pages | ~17 pages |
| **Content Pages** | 3 pages ✅ | 15 pages |
| **Word Count** | ~840 words | ~1690 words |
| **Margins** | 2cm (tight) | 2.5cm (normal) |
| **Spacing** | 0.5em (compact) | 1em (comfortable) |
| **Page Breaks** | None (continuous) | Between exercises |
| **Subsections** | No | Yes |
| **Detail Level** | Core concepts only | Full explanations |

---

## 📝 What's Different in Each Exercise

### Exercise 1 (W/L Ratio)
- **Condensed:** 8 lines, single paragraph with inline pros/cons
- **Detailed:** Separate subsections for W and L with bullet lists

### Exercise 2 (Feedback)
- **Condensed:** Single paragraph listing 5 advantages, 4 disadvantages
- **Detailed:** Separate subsections with detailed explanations

### Exercise 3 (Second-Order Systems)
- **Condensed:** Brief damping scenarios in continuous text
- **Detailed:** Separate sections for each damping case with full analysis

### Exercise 4 (Bandgap Reference)
- **Condensed:** Combined implementation/advantages/disadvantages
- **Detailed:** Separate subsections for each topic

### Exercise 5 (Two-Stage Op-Amp)
- **Condensed:** Two compact paragraphs covering parts (a) and (b)
- **Detailed:** Full subcircuit descriptions with separate effects analysis

### Exercise 6 (CMRR)
- **Condensed:** Methods and trade-offs in flowing text
- **Detailed:** Numbered methods with trade-offs table

---

## ✅ Both Versions Are Complete

### Condensed Version:
- ✅ Answers all 6 exercises
- ✅ Addresses all parts (a), (b), etc.
- ✅ Includes key equations
- ✅ Covers pros/cons
- ✅ Circuit diagrams included
- ✅ Fits in 3 pages

### Detailed Version:
- ✅ Everything above PLUS:
- ✅ Detailed explanations
- ✅ Extended analysis
- ✅ Separate subsections
- ✅ Bullet point lists
- ✅ Design guidelines
- ✅ More examples

---

## 🎓 Recommended Workflow

1. **While working/studying:**
   - Use `main_detailed.tex` for full context
   - Read detailed explanations
   - Understand complete derivations

2. **For submission:**
   - Switch to `main.tex` 
   - Compile condensed version
   - Verify fits in 3 pages
   - Download and submit PDF

3. **For exam preparation:**
   - Use `main_detailed.tex` 
   - Has all the details you studied
   - Better for review

---

## 🔧 Customization Options

### If Condensed Version is Still Too Long:
Edit the `*_condensed.tex` files to trim further. See `CONDENSING_NOTES.md` for priority cuts.

### If You Want Medium Detail:
1. Copy `main.tex` to `main_medium.tex`
2. Mix condensed and detailed sections:
   ```latex
   \subfile{sections/exercise1_condensed}  % Use condensed
   \subfile{sections/exercise2}            % Use detailed
   \subfile{sections/exercise3_condensed}  % Use condensed
   ...
   ```

---

## 💾 File Management

### Which Files to Edit:

**For submission version:**
- Edit: `exercise*_condensed.tex` files
- Compile: `main.tex`

**For detailed reference:**
- Edit: `exercise*.tex` files (without _condensed)
- Compile: `main_detailed.tex`

### Both Versions Share:
- Same images folder
- Same DTU logo
- Same title page
- Same table of contents structure

---

## 📤 What to Submit

**For your course submission:**
- Compile `main.tex` (condensed version)
- Download the PDF
- Submit only the PDF

**Keep both versions in Overleaf** for your own reference!

---

## ⚡ Quick Reference

| I want to... | Use this file |
|--------------|---------------|
| Submit assignment | `main.tex` |
| Study for exam | `main_detailed.tex` |
| See full explanations | `main_detailed.tex` |
| Fit in 3 pages | `main.tex` |
| Read detailed theory | `exercise*.tex` |
| Edit for submission | `exercise*_condensed.tex` |

---

## 🎯 Current Status

✅ **Condensed version:** Ready for 3-page submission
✅ **Detailed version:** Complete with full explanations  
✅ **Both versions:** Coexist in same project
✅ **Easy switching:** Just change main document in Overleaf

---

**You now have the best of both worlds!** 🎉

- Condensed version meets the 3-page requirement
- Detailed version preserves all your work
- Both versions available anytime
- Easy to switch between them

Upload to Overleaf and you're all set! 🚀
