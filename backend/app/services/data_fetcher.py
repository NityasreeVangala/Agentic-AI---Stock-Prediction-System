# app/services/data_fetcher.py
import yfinance as yf
import pandas as pd
import os

START_DATE = "2010-01-01"
END_DATE = "2025-12-31"

# Supported stocks
STOCKS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "YESBANK.NS"]

# Ensure data folder exists
os.makedirs("data", exist_ok=True)


# ------------------ FETCH FROM YFINANCE ------------------
def fetch_stock_data(symbol: str) -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.
    """
    stock = yf.Ticker(symbol)
    df = stock.history(start=START_DATE, end=END_DATE)
    df.reset_index(inplace=True)
    return df


# ------------------ CLEAN DATA ------------------
def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning: sort data and remove empty rows.
    """
    df = df.sort_values("Date")
    df = df.dropna(subset=["Close"])
    return df


# ------------------ SAVE ALL (ONE-TIME) ------------------
def save_all_stocks():
    """
    Fetch, clean, and save all stock CSVs.
    Run once if needed.
    """
    for symbol in STOCKS:
        df = fetch_stock_data(symbol)
        df = clean_stock_data(df)
        df.to_csv(f"data/{symbol}.csv", index=False)
        print(f"Saved {symbol}")


# ========================================================
# 🔥 BACKEND-ONLY RAW DATA LOADER (CRITICAL)
# ========================================================
def load_stock_df(symbol: str) -> pd.DataFrame:
    """
    Load FULL cleaned DataFrame.
    Used ONLY by backend services (indicators, scoring).
    """
    csv_path = f"data/{symbol}.csv"

    if not os.path.exists(csv_path):
        df = fetch_stock_data(symbol)
        df = clean_stock_data(df)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    return df.sort_values("Date")


# ========================================================
# 🌐 FRONTEND-SAFE HISTORY ENDPOINT
# ========================================================
def get_stock_history(symbol: str, limit: int = 200):
    """
    Return ONLY last `limit` rows for frontend charts.
    Prevents browser crashes.
    """
    df = load_stock_df(symbol)

    df = df.tail(limit)

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    return df[
        ["Date", "Open", "High", "Low", "Close", "Volume"]
    ].to_dict(orient="records")
