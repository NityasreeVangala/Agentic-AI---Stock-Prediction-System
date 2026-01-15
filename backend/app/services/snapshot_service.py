import pandas as pd
import os

# Path to the merged stock CSV
ALL_STOCKS_PATH = os.path.join(os.path.dirname(__file__), "../data/all_stock_prices.csv")
SNAPSHOT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../data/snapshot_2025-12-31_all.csv")

def generate_snapshot(snapshot_date="2025-12-31"):
    """
    Generates a snapshot of all stocks for the given date.
    Only keeps the last known price per stock on or before snapshot_date.
    """
    # Load merged historical data
    if not os.path.exists(ALL_STOCKS_PATH):
        raise FileNotFoundError(f"Historical data CSV not found at {ALL_STOCKS_PATH}")

    df = pd.read_csv(ALL_STOCKS_PATH, parse_dates=["Date"])

    # Filter data to only keep the last known price per stock on or before snapshot_date
    df = df[df['Date'] <= snapshot_date]

    if df.empty:
        print("No data available before the snapshot date!")
        return pd.DataFrame()  # return empty dataframe if nothing found

    # Get the last known price for each stock
    snapshot_df = df.sort_values("Date").groupby("Symbol").tail(1)

    # Save snapshot CSV
    snapshot_df.to_csv(SNAPSHOT_OUTPUT_PATH, index=False)
    print(f"✅ Snapshot saved at {SNAPSHOT_OUTPUT_PATH}")
    print(snapshot_df)
    return snapshot_df
