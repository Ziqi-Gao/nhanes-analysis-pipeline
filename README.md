# CDC/NHANES Analysis Pipeline

Reusable Python pipeline for downloading public CDC/NHANES files and running analysis modules.

The current analysis computes the NHANES 2017-2018 HbA1c/A1C mean using the glycohemoglobin lab file and MEC exam weights.

## Setup

Run from the project root:

```powershell
.\scripts\bootstrap_python.ps1
```

This creates a local Python runtime and virtual environment under `.python\` and `.venv\`, then installs `requirements.txt`.

If PowerShell blocks local scripts, run this once in the same terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean
```

Equivalent Python command:

```powershell
.\.venv\Scripts\python.exe .\run_cdc_nhanes.py hba1c-mean
```

Force a fresh CDC download:

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean --force-download
```

Downloaded source files are cached under `data\raw\cdc_nhanes\`. Analysis outputs are written under `outputs\cdc_nhanes\`. Both directories are generated locally and ignored by git.

## Test

```powershell
.\.venv\Scripts\python.exe .\test_hba1c_mean.py
```

Expected current result:

```text
Valid sample size: 6,045
Unweighted mean:   5.7696
Weighted mean:     5.6377
```

## Project Layout

- `cdc_nhanes\nhanes.py`: NHANES cycle/file definitions, download helpers, and XPT reader.
- `cdc_nhanes\analyses\`: analysis modules.
- `cdc_nhanes\analyses\hba1c_mean.py`: current HbA1c/A1C mean analysis.
- `run_cdc_nhanes.py`: CLI entry point.
- `scripts\`: PowerShell setup and run wrappers.
- `test_hba1c_mean.py`: smoke test for the current analysis.

## Adding Analyses

1. Add a module under `cdc_nhanes\analyses\`.
2. Reuse `download_nhanes_files` from `cdc_nhanes\nhanes.py`.
3. Register the analysis in `run_cdc_nhanes.py`.
4. Add a focused test or smoke script with expected outputs.
