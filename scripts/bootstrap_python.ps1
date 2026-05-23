$ErrorActionPreference = "Stop"

$PythonVersion = "3.12.8"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$CacheDir = Join-Path $ProjectRoot ".cache"
$PythonDir = Join-Path $ProjectRoot ".python"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Installer = Join-Path $CacheDir "python-$PythonVersion-amd64.exe"
$InstallerUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-amd64.exe"

New-Item -ItemType Directory -Force -Path $CacheDir | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $PythonDir "python.exe"))) {
    if (-not (Test-Path -LiteralPath $Installer)) {
        Invoke-WebRequest -Uri $InstallerUrl -OutFile $Installer
    }

    & $Installer /quiet InstallAllUsers=0 TargetDir="$PythonDir" Include_pip=1 Include_launcher=0 AssociateFiles=0 Shortcuts=0 PrependPath=0 Include_test=0
}

if (-not (Test-Path -LiteralPath $VenvPython)) {
    & (Join-Path $PythonDir "python.exe") -m venv (Join-Path $ProjectRoot ".venv")
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt")
& $VenvPython -c "import sys, pandas, numpy, requests; print(sys.version); print('pandas', pandas.__version__); print('numpy', numpy.__version__); print('requests', requests.__version__)"
