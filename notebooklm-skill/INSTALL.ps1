# NotebookLM skill installer for a second Windows PC.
# Run from PowerShell in this folder:    .\INSTALL.ps1
# Assumes: miniconda Python at $env:USERPROFILE\miniconda3\python.exe (same layout as source PC).

$ErrorActionPreference = "Stop"
$PYTHON = "$env:USERPROFILE\miniconda3\python.exe"
$SKILL_DIR = "$env:USERPROFILE\.claude\skills\notebooklm"
$BUNDLE_DIR = $PSScriptRoot
$SKILL_SRC = Join-Path $BUNDLE_DIR "skill-files"

Write-Host "`n=== NotebookLM skill — transfer install ===" -ForegroundColor Cyan
Write-Host "Source bundle: $SKILL_SRC"
Write-Host "Target skill:  $SKILL_DIR"
Write-Host "Python:        $PYTHON`n"

# --- 1. Verify Python ---
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
if (-not (Test-Path $PYTHON)) {
    Write-Host "ERROR: Miniconda Python not found at $PYTHON" -ForegroundColor Red
    Write-Host "If your miniconda is elsewhere, edit the `\$PYTHON variable at the top of this script."
    Write-Host "If you don't have miniconda, install it from https://docs.conda.io/projects/miniconda/"
    exit 1
}
$pyver = & $PYTHON --version
Write-Host "  Found: $pyver"

# --- 2. Copy skill files ---
Write-Host "`n[2/6] Copying skill files to $SKILL_DIR..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $SKILL_DIR | Out-Null
Copy-Item -Recurse -Force "$SKILL_SRC\*" $SKILL_DIR
Write-Host "  Done."

# --- 3. Install notebooklm-py + Playwright Chromium ---
Write-Host "`n[3/6] Installing notebooklm-py[browser] (may take ~30 sec)..." -ForegroundColor Yellow
& $PYTHON -m pip install --quiet "notebooklm-py[browser]"
Write-Host "  Installed."

Write-Host "`n[4/6] Installing Playwright Chromium (~330 MB total — may take a few minutes)..." -ForegroundColor Yellow
Write-Host "  IMPORTANT: This MUST run from your interactive PowerShell so the binaries get proper Win32 execution permissions."
& $PYTHON -m playwright install chromium
Write-Host "  Installed."

# --- 5. Interactive login ---
Write-Host "`n[5/6] One-time Google login..." -ForegroundColor Yellow
$existingAuth = "$env:USERPROFILE\.notebooklm\profiles\default\storage_state.json"
if (Test-Path $existingAuth) {
    Write-Host "  Found existing auth at $existingAuth — skipping login. (Delete the file first if you want a fresh login.)"
} else {
    Write-Host "  A Chromium window will open. Sign into your Google account that has NotebookLM,"
    Write-Host "  wait for the NotebookLM homepage, then press ENTER in this PowerShell."
    Read-Host "  Press ENTER to start login"
    $env:PYTHONUTF8 = "1"
    & "$SKILL_DIR\scripts\nlm.bat" login
}

# --- 6. Verify + scheduled task ---
Write-Host "`n[6/6] Verifying access and setting up auto-refresh..." -ForegroundColor Yellow
$env:PYTHONUTF8 = "1"
$listOutput = & "$SKILL_DIR\scripts\nlm.bat" list 2>&1
if ($LASTEXITCODE -ne 0 -or $listOutput -match "ERROR") {
    Write-Host "  Verification failed. Output:" -ForegroundColor Red
    Write-Host $listOutput
    exit 1
}
Write-Host "  list works — you see your NotebookLM notebooks."
$listOutput | Select-Object -Last 1 | Write-Host

Write-Host ""
Write-Host "  Creating scheduled task 'NotebookLM Cookie Refresh' (every 3 days, 05:30)..."
schtasks /Create /SC DAILY /MO 3 /TN "NotebookLM Cookie Refresh" /TR "$SKILL_DIR\scripts\refresh.bat" /ST 05:30 /F | Out-Null
Write-Host "  Scheduled task created."

Write-Host "`n=== Install complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Try it:"
Write-Host "  & ""$SKILL_DIR\scripts\nlm.bat"" ask ""What is aliasing?"" --notebook-id dsp"
Write-Host ""
Write-Host "Aliases (already configured): iot, iae2, lcd1, dsd, dsp"
Write-Host ""
Write-Host "In your next Claude Code session, the 'notebooklm' skill will auto-discover from $SKILL_DIR."
