$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$EntryPoint = Join-Path $ProjectRoot "run_cdc_nhanes.py"

if (-not (Test-Path -LiteralPath $Python)) {
    & (Join-Path $PSScriptRoot "bootstrap_python.ps1")
}

& $Python $EntryPoint @args
