from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests

from .paths import CDC_NHANES_RAW_DIR, ensure_cdc_nhanes_dirs


@dataclass(frozen=True)
class NhanesFile:
    key: str
    filename: str
    component: str
    description: str


@dataclass(frozen=True)
class NhanesCycle:
    cycle: str
    public_year: str
    files: tuple[NhanesFile, ...]

    @property
    def base_url(self) -> str:
        return f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{self.public_year}/DataFiles"

    def url_for(self, filename: str) -> str:
        return f"{self.base_url}/{filename}"


NHANES_2017_2018 = NhanesCycle(
    cycle="2017-2018",
    public_year="2017",
    files=(
        NhanesFile(
            key="glycohemoglobin",
            filename="GHB_J.xpt",
            component="Laboratory",
            description="Glycohemoglobin",
        ),
        NhanesFile(
            key="demographics",
            filename="DEMO_J.xpt",
            component="Demographics",
            description="Demographic variables and sample weights",
        ),
    ),
)


def download_file(url: str, destination: Path, force: bool = False) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return destination

    with requests.get(url, timeout=60, stream=True) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return destination


def download_nhanes_files(
    cycle: NhanesCycle,
    keys: Iterable[str] | None = None,
    force: bool = False,
) -> dict[str, Path]:
    ensure_cdc_nhanes_dirs()
    selected_keys = set(keys) if keys is not None else {file.key for file in cycle.files}
    available = {file.key: file for file in cycle.files}
    unknown = selected_keys - set(available)
    if unknown:
        unknown_list = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown NHANES file key(s) for {cycle.cycle}: {unknown_list}")

    cache_dir = CDC_NHANES_RAW_DIR / cycle.cycle
    downloaded: dict[str, Path] = {}
    for key in selected_keys:
        source = available[key]
        downloaded[key] = download_file(
            url=cycle.url_for(source.filename),
            destination=cache_dir / source.filename,
            force=force,
        )
    return downloaded


def read_xpt(path: str | Path) -> pd.DataFrame:
    return pd.read_sas(path, format="xport")
