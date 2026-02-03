# Home Assignment 2 - Resources

## 📚 Study Materials

### LaTeX Submission Document
**📂 [[Home_Assignment_II_Submission.pdf|Submitted Assignment PDF]]** - Your condensed submission version (3 pages, opens in Obsidian)

### Complete Solution Sheet
**[[Solution_Sheet]]** - Comprehensive descriptive solutions for all 6 exercises (includes link to PDF above)
- Exercise 1: W/L Ratio effects
- Exercise 2: Feedback advantages/disadvantages
- Exercise 3: Second-order system pole placement
- Exercise 4: Bandgap voltage reference
- Exercise 5: Two-stage op-amp analysis
- Exercise 6: CMRR improvement methods

### Quick Formula Reference
**[[FORMULAS]]** - Key equations and formulas for quick lookup

---

## 🔌 LTspice Simulations

### Exercise 5: Two-Stage Op-Amp
**[[Exercise5_README]]** - Complete simulation guide with:
- Circuit analysis and transistor sizing
- DC operating point analysis
- AC frequency response (gain, GBW, phase margin)
- Transient analysis
- Parameter sweep experiments
- Troubleshooting guide

**📂 [Open LTspice Schematic](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise5_TwoStage_OpAmp.asc)**

---

### Exercise 6: Differential Amplifier & CMRR
**[[Exercise6_CMRR_Guide]]** - CMRR measurement and improvement guide with:
- Step-by-step CMRR measurement procedure
- How to measure differential vs. common-mode gain
- Multiple CMRR improvement techniques
- Cascode current source implementation
- Parameter sweep experiments
- Comparison tables and trade-off analysis

**LTspice Schematics:**
- **📂 [Basic Version](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise6_Differential_CMRR.asc)** - Simple tail current source
- **📂 [Improved Version](file:///C:/Users/Mads2/DTU/3.semester/Integrated%20Analog%20Electronics/LTspice/HomeAssignment/II/Exercise6_Cascode_CMRR.asc)** - Cascode tail (+20-30 dB CMRR)

---

## 📁 File Organization

### Obsidian Notes (this directory)
`C:\Users\Mads2\DTU\Obsidian\Courses\Integrated Analog Electronics\Exercises\Home Assignments\2\`
- Solution_Sheet.md
- FORMULAS.md
- Exercise5_README.md
- Exercise6_CMRR_Guide.md
- README.md (this file)

### LTspice Simulations
`C:\Users\Mads2\DTU\3.semester\Integrated Analog Electronics\LTspice\HomeAssignment\II\`
- Exercise5_TwoStage_OpAmp.asc
- Exercise6_Differential_CMRR.asc
- Exercise6_Cascode_CMRR.asc

---

## 🎯 Quick Start Guide

### For Theory & Understanding
1. Read **Solution_Sheet.md** for comprehensive explanations
2. Use **FORMULAS.md** for quick equation reference

### For Simulation & Verification
1. Open **Exercise5_README.md** or **Exercise6_CMRR_Guide.md**
2. Click the embedded links to open LTspice schematics
3. Follow the simulation procedures in the guides
4. Compare simulation results with theoretical predictions

### For Exam Preparation
- **Solution_Sheet.md** - Study all fundamental concepts and trade-offs
- **FORMULAS.md** - Quick formula reference
- **LTspice simulations** - Verify understanding with hands-on analysis

---

## 📊 What Each Exercise Covers

| Exercise | Topic | LTspice Available |
|----------|-------|-------------------|
| 1 | W/L Ratio in MOSFETs | ❌ (Theory only) |
| 2 | Feedback Theory | ❌ (Theory only) |
| 3 | Second-Order Systems | ❌ (Theory only) |
| 4 | Bandgap Reference | ❌ (Theory only) |
| 5 | Two-Stage Op-Amp | ✅ Full simulation |
| 6 | CMRR Analysis | ✅ Two versions |

---

## 💡 Tips

- **Study sequence:** Read theory first (Solution_Sheet) → Simulate (LTspice) → Verify understanding
- **For reports:** Use LTspice plots and screenshots, reference theoretical equations
- **For exams:** Focus on trade-offs and design decisions in Solution_Sheet
- **Customization:** All LTspice circuits are parameterized - experiment with different values!

### About Links
- **PDF links** (📂 with `[[...]]` syntax) - Open inside Obsidian
- **LTspice links** (📂 with `file:///` protocol) - Open in external LTspice application

### Updating the PDF
After recompiling your LaTeX document, run **`sync_pdf.bat`** in this directory to update the PDF in Obsidian, or manually copy `main.pdf` from the LaTeX folder.

---

**Good luck with your studies!** 🚀
