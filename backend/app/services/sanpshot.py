import pandas as pd
import os

def generate_snapshot(snapshot_date: str = "2025-12-31"):
    """
    Generate a snapshot CSV of all stocks for a given date.

    Args:
        snapshot_date (str): The date to snapshot in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: The snapshot dataframe.
    """

    # 1️⃣ Path to your full historical data
    all_data_path = os.path.join(os.path.dirname(__file__), "../data/all_stock_prices.csv")

    if not os.path.exists(all_data_path):
        raise FileNotFoundError(f"Historical data CSV not found at {all_data_path}")

    # 2️⃣ Load all historical stock data
    df_all = pd.read_csv(all_data_path)

    # 3️⃣ Ensure 'Date' column is in datetime format
    df_all['Date'] = pd.to_datetime(df_all['Date'])

    # 4️⃣ Convert snapshot_date to datetime
    snapshot_dt = pd.to_datetime(snapshot_date)

    # 5️⃣ Filter for the snapshot date
    snapshot_df = df_all[df_all['Date'] == snapshot_dt]

    if snapshot_df.empty:
        print(f"⚠️ No data found for {snapshot_date}. Snapshot will be empty.")
    else:
        print(f"✅ Found {len(snapshot_df)} rows for {snapshot_date}")

    # 6️⃣ Save snapshot CSV
    snapshot_file = os.path.join(os.path.dirname(__file__), f"../data/snapshot_{snapshot_date}_all.csv")
    snapshot_df.to_csv(snapshot_file, index=False)
    print(f"💾 Snapshot saved to {snapshot_file}")

    return snapshot_df
