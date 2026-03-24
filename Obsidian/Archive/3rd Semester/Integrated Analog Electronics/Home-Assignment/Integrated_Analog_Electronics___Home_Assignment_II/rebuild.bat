@echo off
echo ========================================
echo Rebuilding PDF (Fixes Viewer Cache)
echo ========================================
echo.
echo Deleting old files...
del /Q main.pdf main.aux main.toc main.out main.fls main.fdb_latexmk 2>nul
echo.
echo Compiling LaTeX (this may take a moment)...
latexmk -pdf -interaction=nonstopmode main.tex
echo.
if exist main.pdf (
    echo ========================================
    echo SUCCESS! PDF rebuilt and ready.
    echo ========================================
    echo.
    echo In VSCode: Close PDF tab and reopen
    echo Ctrl+Shift+P ^> "LaTeX Workshop: View LaTeX PDF"
) else (
    echo ERROR: PDF compilation failed
    echo Check main.log for errors
)
echo.
pause
