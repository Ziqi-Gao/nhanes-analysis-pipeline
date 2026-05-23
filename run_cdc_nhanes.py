from __future__ import annotations

import argparse

from cdc_nhanes.analyses.hba1c_mean import compute_hba1c_mean_summary, write_hba1c_mean_outputs
from cdc_nhanes.paths import project_relative


HBA1C_MEAN_ANALYSIS = "hba1c-mean"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run CDC/NHANES download and analysis tasks."
    )
    parser.add_argument(
        "analysis",
        nargs="?",
        default=HBA1C_MEAN_ANALYSIS,
        choices=(HBA1C_MEAN_ANALYSIS,),
        help="Analysis to run.",
    )
    parser.add_argument("--force-download", action="store_true")
    return parser


def run_hba1c_mean(force_download: bool = False) -> None:
    summary = compute_hba1c_mean_summary(force_download=force_download)
    csv_path, json_path = write_hba1c_mean_outputs(summary)
    print("CDC/NHANES 2017-2018 HbA1c/A1C Mean")
    print("------------------------------------")
    print(f"Lab file:          {summary.lab_file}")
    print(f"Demographics file: {summary.demographics_file}")
    print(f"Valid sample size: {summary.valid_sample_size:,}")
    print(f"Unweighted mean:   {summary.unweighted_mean:.4f}")
    print(f"Weighted mean:     {summary.weighted_mean:.4f}")
    print(f"Wrote summary CSV: {project_relative(csv_path)}")
    print(f"Wrote summary JSON: {project_relative(json_path)}")


def main() -> None:
    args = build_parser().parse_args()
    if args.analysis == HBA1C_MEAN_ANALYSIS:
        run_hba1c_mean(force_download=args.force_download)


if __name__ == "__main__":
    main()
