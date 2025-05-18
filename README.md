````markdown
# Elysia-SAPSS

**Minimal MVP for first experiment**

## Overview
Elysia-SAPSS (System for Analysis of Potential Short Squeezes) is an experimental platform for detecting early signals of market anomalies—particularly short squeezes—by combining traditional financial metrics with alternative data sources and sentiment analysis.

## Quickstart
1. Clone the repository:
   ```bash
   git clone https://github.com/pavolh01/Elysia-SAPSS.git
   cd Elysia-SAPSS
````

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Populate API keys and credentials in `src/utils/helpers.py` (see template).
4. Run sample ingestion pipeline:

   ```bash
   python src/data_ingestion/google_trends.py --keywords TSLA AAPL
   ```
5. Process raw data and compute features:

   ```bash
   python src/data_processing/processors.py
   ```

## Variables & Data Sources

Predictive analysis in this MVP is based on the following primary and supplementary data groups. For each, we list our target cadence (daily for MVP) and the ingestion method:

1. **Search Volumes**

   * **Cadence**: Daily snapshots
   * **Description**: Trends of user searches on specific stock symbols or topics, measured as daily changes.
   * **Source**: Google Trends API (via `pytrends`) in `src/data_ingestion/google_trends.py`.

2. **Media Coverage**

   * **Cadence**: Daily article counts
   * **Description**: Number of news articles published per symbol/topic each day.
   * **Source**: Media Cloud REST API client (to be implemented in `src/data_ingestion/media_cloud.py`).

3. **Stock Returns (Dependent Variable)**

   * **Cadence**: Daily OHLC prices + volatility
   * **Description**: Open, high, low, close prices; compute returns as $R_t = (P_t - P_{t-1}) / P_{t-1}$.
   * **Source**: Yahoo Finance (`yfinance` library) in `src/data_ingestion/finance.py`.

4. **Trading Volumes**

   * **Cadence**: Daily total shares traded
   * **Description**: Captures investor activity; used as a feature.
   * **Source**: Yahoo Finance (via `yfinance`) or directly from Nasdaq API.

5. **CBOE Volatility Index (VIX)**

   * **Cadence**: Daily closing values
   * **Description**: Market volatility gauge; extracted as daily changes.
   * **Source**: CBOE or Yahoo Finance (`^VIX` ticker).

6. **Interaction Terms**

   * **Cadence**: Derived daily
   * **Description**: Combined effects such as Search Volume × Media Coverage to capture amplification.
   * **Computation**: Generated in `src/data_processing/processors.py`.

### Supplementary Variables (Hypothetical for future phases)

7. **Social Media Engagement & Sentiment**

   * **Cadence**: Daily metrics
   * **Description**: Counts of posts, comments, upvotes; sentiment via NLP.
   * **Source**: Reddit API (`praw`), X API; sentiment with VADER/FinBERT (`src/sentiment_analysis/sentiment.py`).

8. **YouTube Discussion Volume**

   * **Cadence**: Daily counts
   * **Description**: Video uploads on finance topics; engagement metrics.
   * **Source**: YouTube Data API (to be added).

9. **Podcast Episodes**

   * **Cadence**: Daily new episode counts
   * **Description**: Tracks finance-related podcast publications.
   * **Source**: Spotify Podcast API / Apple Podcasts API.

10. **Institutional Investor Holdings**

    * **Cadence**: Weekly (raw), Daily refresh for MVP
    * **Description**: Recent changes in institutional positions.
    * **Source**: Yahoo Finance Institutional Holdings endpoint.

11. **Political Trading Activity**

    * **Cadence**: Daily updates
    * **Description**: Trades reported by politicians.
    * **Source**: Quiver Quantitative API.

12. **C-Level Executive Trades**

    * **Cadence**: Daily updates
    * **Description**: Insider trades by corporate executives.
    * **Source**: EDGAR filings or third-party API (to be determined).

## Folder Structure

```text
Elysia-SAPSS/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── data_ingestion/
│   ├── data_processing/
│   ├── sentiment_analysis/
│   ├── modeling/
│   └── api/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
└── tests/
```

```
```
