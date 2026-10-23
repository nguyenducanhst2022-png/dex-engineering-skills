<#
.SYNOPSIS
    DEX Polyglot Script Engine v7.0 / v8.0 — PowerShell Wrapper
.DESCRIPTION
    Executes DEX CLI commands across all 11 supported programming languages.
.EXAMPLE
    .\dex.ps1 status
    .\dex.ps1 doctor
    .\dex.ps1 test --lang python
    .\dex.ps1 generate --lang rust --task data_parser
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ForwardArgs
)

$ErrorActionPreference = "Stop"

# Locate repo root relative to this wrapper
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$DexPy = Join-Path $RepoRoot "scripts\polyglot\dex.py"

if (-not (Test-Path $DexPy)) {
    Write-Error "Cannot locate dex.py at $DexPy"
    exit 1
}

# Resolve python
$PythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } elseif (Get-Command python3 -ErrorAction SilentlyContinue) { "python3" } else { $null }

if (-not $PythonCmd) {
    Write-Error "Python 3 is required but not found in PATH."
    exit 127
}

& $PythonCmd $DexPy @ForwardArgs
exit $LASTEXITCODE
