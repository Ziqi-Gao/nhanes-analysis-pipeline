from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

CDC_NHANES_RAW_DIR = RAW_DATA_DIR / "cdc_nhanes"
CDC_NHANES_OUTPUT_DIR = OUTPUT_DIR / "cdc_nhanes"


def ensure_cdc_nhanes_dirs() -> None:
    for path in (CDC_NHANES_RAW_DIR, CDC_NHANES_OUTPUT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def project_relative(path: str | Path) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate

    try:
        return candidate.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()
