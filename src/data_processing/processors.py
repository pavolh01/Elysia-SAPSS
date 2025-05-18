"""
src/data_processing/processors.py

Reads raw Google Trends CSV, pivots keywords into columns,
computes week-over-week changes, and writes two CSVs:
  - interest levels (wide format)
  - interest deltas
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def process_google_trends(
    raw_path: str = "data/raw/google_trends.csv",
    out_interest_path: str = "data/processed/google_trends_interest.csv",
    out_delta_path: str = "data/processed/google_trends_delta.csv",
):
    # 1) Load
    df = pd.read_csv(raw_path, parse_dates=["date"])
    if df.empty:
        logger.error(f"No data found at {raw_path}")
        return

    # 2) Pivot to wide format: date × keyword → interest
    df_wide = df.pivot(index="date", columns="keyword", values="interest")
    df_wide = df_wide.sort_index()
    logger.info(f"Pivoted to wide format: {df_wide.shape[0]} rows × {df_wide.shape[1]} keywords")

    # 3) Compute period-over-period change
    df_delta = df_wide.diff().reset_index().melt(
        id_vars="date", var_name="keyword", value_name="interest_delta"
    )
    logger.info(f"Computed deltas: {df_delta.shape[0]} total records")

    # 4) Ensure output folder exists
    Path(out_interest_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_delta_path).parent.mkdir(parents=True, exist_ok=True)

    # 5) Write CSVs
    df_wide.reset_index().to_csv(out_interest_path, index=False)
    df_delta.to_csv(out_delta_path, index=False)
    logger.info(f"Wrote interest data to {out_interest_path}")
    logger.info(f"Wrote delta data to    {out_delta_path}")

if __name__ == "__main__":
    process_google_trends()
