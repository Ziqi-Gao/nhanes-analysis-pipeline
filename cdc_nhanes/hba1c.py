from __future__ import annotations

from .analyses.hba1c_mean import (
    Hba1cMeanSummary,
    compute_hba1c_mean_summary,
    write_hba1c_mean_outputs,
)


Hba1cSummary = Hba1cMeanSummary
compute_hba1c_summary = compute_hba1c_mean_summary
write_hba1c_outputs = write_hba1c_mean_outputs

__all__ = [
    "Hba1cMeanSummary",
    "Hba1cSummary",
    "compute_hba1c_mean_summary",
    "compute_hba1c_summary",
    "write_hba1c_mean_outputs",
    "write_hba1c_outputs",
]
