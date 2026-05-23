from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from cdc_nhanes.nhanes import NHANES_2017_2018, download_nhanes_files, read_xpt
from cdc_nhanes.paths import CDC_NHANES_OUTPUT_DIR, project_relative


@dataclass(frozen=True)
class Hba1cMeanSummary:
    analysis: str
    cycle: str
    lab_file: str
    demographics_file: str
    value_variable: str
    weight_variable: str
    valid_sample_size: int
    unweighted_mean: float
    weighted_mean: float


def compute_hba1c_mean_summary(force_download: bool = False) -> Hba1cMeanSummary:
    files = download_nhanes_files(
        cycle=NHANES_2017_2018,
        keys=("glycohemoglobin", "demographics"),
        force=force_download,
    )
    ghb = read_xpt(files["glycohemoglobin"])
    demo = read_xpt(files["demographics"])

    value_variable = "LBXGH"
    weight_variable = "WTMEC2YR"
    merged = ghb[["SEQN", value_variable]].merge(
        demo[["SEQN", weight_variable]],
        on="SEQN",
        how="inner",
    )
    valid = merged.dropna(subset=[value_variable, weight_variable])
    if valid.empty:
        raise ValueError("No records have both LBXGH and WTMEC2YR present.")

    weight_sum = valid[weight_variable].sum()
    if weight_sum == 0:
        raise ValueError("The sum of WTMEC2YR is zero; weighted mean is undefined.")

    return Hba1cMeanSummary(
        analysis="hba1c_mean",
        cycle=NHANES_2017_2018.cycle,
        lab_file=project_relative(files["glycohemoglobin"]),
        demographics_file=project_relative(files["demographics"]),
        value_variable=value_variable,
        weight_variable=weight_variable,
        valid_sample_size=int(len(valid)),
        unweighted_mean=float(valid[value_variable].mean()),
        weighted_mean=float((valid[value_variable] * valid[weight_variable]).sum() / weight_sum),
    )


def write_hba1c_mean_outputs(summary: Hba1cMeanSummary) -> tuple[Path, Path]:
    CDC_NHANES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = CDC_NHANES_OUTPUT_DIR / "nhanes_2017_2018_hba1c_mean_summary.csv"
    json_path = CDC_NHANES_OUTPUT_DIR / "nhanes_2017_2018_hba1c_mean_summary.json"

    pd.DataFrame([asdict(summary)]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(asdict(summary), indent=2) + "\n", encoding="utf-8")
    return csv_path, json_path
