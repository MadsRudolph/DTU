# Architecture Decision: Single Self-Contained Offline HTML vs. Desktop / Local-Server App

## Context
- **Exam**: 34840 Fundamentals of Acoustics and Noise Control — Friday 11 Dec 2026, 4 hours, individual, all aids allowed, **NO INTERNET**.
- **Environment**: Laptop running Arch Linux + Hyprland (Omarchy). MATLAB R2026a uses online licensing by default and may refuse to start offline.
- **Core Requirement**: Must open instantly and reliably on exam morning with **zero** runtime setup, daemon startup, or fragility after system/package updates.

## Options Evaluated

| Option | Pros | Cons / Exam-Day Risks |
|---|---|---|
| **1. Single self-contained `exam-app.html` (`file://`)** | • **Zero runtime dependencies**: opens in any browser (Chromium/Firefox) via double-click or `chromium exam-app.html` directly from `file://`.<br>• **Immune to OS/library updates**: a rolling Arch Linux update (`pacman -Syu`) the week before the exam cannot break an HTML file.<br>• **Native Print-to-PDF & text copy**: browser `Ctrl+F`, clipboard, and `Ctrl+P` → *Save as PDF* work out of the box for the Part 1 PDF hand-in.<br>• **Portable**: travels via `git pull` or a USB stick as a single 811 KB file. | • All CSS, JS, KaTeX, and `.woff2` math fonts must be bundled/base64-inlined at build time so no `file://` CORS or missing-font issues can occur. |
| **2. Local Node / Python server (`localhost:PORT`)** | • Familiar dev workflow. | • Requires opening a terminal and keeping a background server process alive during a 4-hour exam.<br>• Port conflicts, accidental terminal close, or Node/Python version shim issues (`mise`) add unnecessary failure modes under time pressure. |
| **3. Electron / Tauri / Native Qt desktop app** | • Standalone window chrome. | • **Electron**: ~150+ MB bundle for a 800 KB calculator; slower cold start.<br>• **Tauri / Qt / Python GUI**: dynamically links against system shared libraries (`webkit2gtk`, `icu`, `qt6`); a rolling Arch update between 26 Nov and 11 Dec can break the binary on exam morning.<br>• Worse text-selection/copy ergonomics and harder PDF export than a browser tab sitting right next to the exam PDF viewer. |

## Decision

**Chosen architecture: Single self-contained offline HTML file (`exam-app.html`), with modular source files in `src/` and a zero-dependency Node bundler (`build.js`).**

### Why this is the best fit for the exam
1. **Zero moving parts on exam morning**: No server to start, no port to bind, no dynamic libraries that an Arch update could break. Opening `exam-app.html` over `file://` works every time.
2. **Side-by-side workflow**: During the exam, Mads already has a browser/PDF viewer open for the exam paper and Obsidian/Writer open for the Part 1 hand-in. Keeping the exam app in a browser tab (or `chromium --app="file:///.../exam-app.html"`) makes `Alt+Tab` and copy-pasting worked steps instantaneous.
3. **100% offline math rendering**: `build.js` inlines `katex.min.js`, `katex.min.css`, and all 12 KaTeX `.woff2` math fonts as `data:font/woff2;base64,...` URIs, stripping any external/relative font URLs so zero network or disk requests occur after opening `exam-app.html`.
4. **Testable in both Node and headless Chromium**: Keeping `src/physics.js` as a clean UMD module lets `node test.js` verify all 116 MATLAB toolkit checks directly in Node in <100 ms, while also verifying the bundled `exam-app.html` inside a network-isolated headless Chromium instance (`unshare -rn`).
