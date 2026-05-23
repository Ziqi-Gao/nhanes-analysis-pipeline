$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "run_cdc_nhanes.ps1") @args
