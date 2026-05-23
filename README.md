# CDC/NHANES Analysis Pipeline

This repository downloads and analyzes public CDC/NHANES data.

The goal is to make future NHANES analyses easier: the download process, local folder structure, and result-writing process are already set up, so new analyses can reuse the same pipeline.

The current example analysis calculates the mean HbA1c/A1C value for the NHANES 2017-2018 cycle.

## What This Project Does

When you run the project, it will:

1. Download the required NHANES files from the CDC website.
2. Save the downloaded files under `data\raw\cdc_nhanes\`.
3. Run the selected analysis.
4. Save the results under `outputs\cdc_nhanes\`.

The `data\raw\` and `outputs\` folders are generated locally. They are not uploaded to GitHub.

## First-Time Setup

If you are not comfortable with Git, you can download this repository as a ZIP file:

1. Open the GitHub repository page.
2. Click the green `Code` button.
3. Click `Download ZIP`.
4. Unzip the folder on your computer.

Then open PowerShell in the project folder and run:

```powershell
.\scripts\bootstrap_python.ps1
```

This creates a project-specific Python environment inside the folder. It does not require you to change your system PATH, and it does not depend on a system-wide Python installation.

If PowerShell blocks the script, run this command in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run the setup command again:

```powershell
.\scripts\bootstrap_python.ps1
```

## Run the Current Analysis

Run the HbA1c/A1C mean analysis:

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean
```

If it works, you should see output similar to this:

```text
CDC/NHANES 2017-2018 HbA1c/A1C Mean
Valid sample size: 6,045
Unweighted mean:   5.7696
Weighted mean:     5.6377
```

The result files will be saved here:

```text
outputs\cdc_nhanes\
```

## Download the Data Again

Usually, you do not need to download the data again. The project will reuse files that already exist locally.

To force a fresh download from the CDC website, run:

```powershell
.\scripts\run_cdc_nhanes.ps1 hba1c-mean --force-download
```

## Check That the Analysis Still Works

Run the test script:

```powershell
.\.venv\Scripts\python.exe .\test_hba1c_mean.py
```

If you see `mean test passed`, the current HbA1c/A1C analysis is producing the expected result.

## Important Files and Folders

- `scripts\bootstrap_python.ps1`: Sets up the local Python environment.
- `scripts\run_cdc_nhanes.ps1`: The easiest way to run an analysis.
- `run_cdc_nhanes.py`: The main Python entry point.
- `cdc_nhanes\nhanes.py`: Defines NHANES files and handles downloads.
- `cdc_nhanes\analyses\`: Stores individual analysis modules.
- `test_hba1c_mean.py`: Checks the current HbA1c/A1C analysis.
- `data\raw\cdc_nhanes\`: Stores downloaded CDC/NHANES source files.
- `outputs\cdc_nhanes\`: Stores generated analysis results.

## Adding a New Analysis Later

When adding a new CDC/NHANES analysis, use this pattern:

1. Add a new analysis file under `cdc_nhanes\analyses\`.
2. Reuse the download helpers in `cdc_nhanes\nhanes.py`.
3. Register the new analysis name in `run_cdc_nhanes.py`.
4. Add a small test script so the result can be checked later.

This keeps the repository easier to maintain as more analyses are added.
