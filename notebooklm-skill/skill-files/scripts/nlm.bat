@echo off
REM Wrapper: invokes nlm.py via conda Python with UTF-8 enforced.
REM Usage: nlm.bat list | nlm.bat ask "question" --notebook-id ID | etc.
set PYTHONUTF8=1
"%USERPROFILE%\miniconda3\python.exe" "%~dp0nlm.py" %*
