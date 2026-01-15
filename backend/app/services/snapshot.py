# backend/app/services/snapshot.py
import pandas as pd
from pathlib import Path

# Path to the merged CSV file containing all 5 stocks
BASE_DIR = Path(__file__).parent
ALL_DATA_PATH = BASE_DIR / "../data/all_stock_prices.csv"

def generate_snapshot(date: str = "2025-12-30") -> pd.DataFrame:
    """
    Generate a snapshot of all stock prices for a specific date.

    Parameters:
        date (str): The date to snapshot in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: A dataframe containing stock prices for the given date.
    """
    # Check if the merged CSV exists
    if not ALL_DATA_PATH.exists():
        raise FileNotFoundError(f"Historical data CSV not found at {ALL_DATA_PATH}")

    # Load the merged CSV
    df = pd.read_csv(ALL_DATA_PATH, parse_dates=["Date"])

    # Filter rows for the given date
    snapshot_df = df[df["Date"] == date].copy()

    # If no data exists for the date, raise an error
    if snapshot_df.empty:
        raise ValueError(f"No stock data available for {date}")

    # Optional: Keep only relevant columns
    snapshot_df = snapshot_df[["Date", "Open", "High", "Low", "Close", "Volume", "Symbol"]]

    return snapshot_df
