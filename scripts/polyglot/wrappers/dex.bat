@echo off
rem ============================================================================
rem DEX Polyglot Script Engine v7.0 / v8.0 — Windows Batch Wrapper
rem ============================================================================
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\..\"
set "DEX_PY=%REPO_ROOT%scripts\polyglot\dex.py"

if not exist "%DEX_PY%" (
    echo [ERROR] Cannot locate dex.py at "%DEX_PY%"
    exit /b 1
)

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python "%DEX_PY%" %*
    exit /b !ERRORLEVEL!
)

where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    python3 "%DEX_PY%" %*
    exit /b !ERRORLEVEL!
)

echo [ERROR] Python 3 is required but not found in PATH.
exit /b 127
