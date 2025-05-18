"""
src/data_ingestion/google_trends.py

Fetches daily search‐volume data for a list of keywords using pytrends.
"""

import argparse
import logging
from datetime import datetime
import pandas as pd
from pytrends.request import TrendReq

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def fetch_trends(keywords, timeframe="today 12-m"):
    """
    Fetches interest-over-time data for each keyword.
    Returns a DataFrame with columns: date, keyword, interest.
    """
    pytrends = TrendReq(hl="en-US", tz=0)
    all_data = []

    for kw in keywords:
        logger.info(f"Fetching Google Trends for '{kw}'")
        pytrends.build_payload([kw], timeframe=timeframe)
        df = pytrends.interest_over_time()
        if df.empty:
            logger.warning(f"No data returned for {kw}")
            continue

        df = df.reset_index()[["date", kw]]
        df = df.rename(columns={kw: "interest"})
        df["keyword"] = kw
        all_data.append(df)

    if not all_data:
        logger.error("No trend data fetched for any keyword.")
        return pd.DataFrame()

    result = pd.concat(all_data, ignore_index=True)
    return result

def main():
    parser = argparse.ArgumentParser(description="Pull Google Trends data for given keywords.")
    parser.add_argument(
        "--keywords", nargs="+", required=True,
        help="List of keywords or tickers (e.g. TSLA AAPL GME)"
    )
    parser.add_argument(
        "--timeframe", default="today 12-m",
        help="pytrends timeframe (e.g. 'today 12-m', 'now 7-d')"
    )
    parser.add_argument(
        "--output", default="data/raw/google_trends.csv",
        help="Path to write the CSV (folder must exist)"
    )
    args = parser.parse_args()

    df = fetch_trends(args.keywords, timeframe=args.timeframe)
    if df.empty:
        logger.error("No data to save. Exiting.")
        return

    # Ensure output directory exists
    df.to_csv(args.output, index=False)
    logger.info(f"Saved trends data to {args.output}")

if __name__ == "__main__":
    main()
