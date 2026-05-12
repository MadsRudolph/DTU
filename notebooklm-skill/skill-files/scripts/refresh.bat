@echo off
REM Headless cookie refresh — invoked by Windows scheduled task every 3 days.
set PYTHONUTF8=1
"%USERPROFILE%\miniconda3\python.exe" "%~dp0refresh_auth.py" >> "%~dp0..\refresh.log" 2>&1
