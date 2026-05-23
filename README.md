# CDC/NHANES Analysis Pipeline

This workspace uses a project-local Python installation:

- Runtime: `.python\python.exe`
- Virtual environment: `.venv\Scripts\python.exe`
- Dependencies: `requirements.txt`

The setup does not require the system `python` command or changes to PATH.

## Project Scope

This project provides a reusable download and analysis pipeline for public CDC/NHANES data. Source files are downloaded into `data\raw\cdc_nhanes\`, generated results are written to `outputs\cdc_nhanes\`, and both directories are ignored by git.

## Rebuild Environment

```powershell
.\scripts\bootstrap_python.ps1
```

## Run Analysis

Run the CDC/NHANES 2017-2018 HbA1c task:

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean
```

Equivalent explicit Python command:

```powershell
.\.venv\Scripts\python.exe .\run_cdc_nhanes.py hba1c-mean
```

Force NHANES source files to redownload:

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean --force-download
```

This downloads CDC/NHANES XPT files into `data\raw\cdc_nhanes\` and writes to `outputs\cdc_nhanes\`.

## Test Analysis

Run the HbA1c mean smoke test:

```powershell
.\.venv\Scripts\python.exe .\test_hba1c_mean.py
```

## Project Layout

- `cdc_nhanes\nhanes.py`: reusable CDC/NHANES file definitions and download helpers.
- `cdc_nhanes\analyses\`: analysis modules.
- `run_cdc_nhanes.py`: CDC/NHANES command-line entry point.
- `test_hba1c_mean.py`: reproducible test for the current HbA1c mean analysis.
- `data\raw\cdc_nhanes\`: generated cache for downloaded source files.
- `outputs\cdc_nhanes\`: generated analysis outputs.

## Add a New Analysis

1. Add an analysis module under `cdc_nhanes\analyses\`.
2. Reuse `download_nhanes_files` from `cdc_nhanes\nhanes.py` instead of writing new download code.
3. Register the analysis in `run_cdc_nhanes.py`.
4. Add a focused test script or pytest test that verifies the expected output.
