from __future__ import annotations

from cdc_nhanes.analyses.hba1c_mean import Hba1cMeanSummary, compute_hba1c_mean_summary


EXPECTED_VALID_SAMPLE_SIZE = 6045
EXPECTED_UNWEIGHTED_MEAN = 5.769561621174525
EXPECTED_WEIGHTED_MEAN = 5.637673633348107
TOLERANCE = 1e-12


def assert_expected_hba1c_mean(summary: Hba1cMeanSummary) -> None:
    assert summary.lab_file == "data/raw/cdc_nhanes/2017-2018/GHB_J.xpt"
    assert summary.demographics_file == "data/raw/cdc_nhanes/2017-2018/DEMO_J.xpt"
    assert summary.valid_sample_size == EXPECTED_VALID_SAMPLE_SIZE
    assert abs(summary.unweighted_mean - EXPECTED_UNWEIGHTED_MEAN) < TOLERANCE
    assert abs(summary.weighted_mean - EXPECTED_WEIGHTED_MEAN) < TOLERANCE


def test_hba1c_mean() -> None:
    assert_expected_hba1c_mean(compute_hba1c_mean_summary())


def main() -> None:
    summary = compute_hba1c_mean_summary()
    assert_expected_hba1c_mean(summary)
    print("CDC/NHANES 2017-2018 HbA1c/A1C mean test passed")
    print(f"Valid sample size: {summary.valid_sample_size:,}")
    print(f"Unweighted mean:   {summary.unweighted_mean:.4f}")
    print(f"Weighted mean:     {summary.weighted_mean:.4f}")


if __name__ == "__main__":
    main()
