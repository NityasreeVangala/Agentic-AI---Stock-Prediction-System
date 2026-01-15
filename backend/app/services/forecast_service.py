# backend/app/services/forecast_service.py
import os
import pandas as pd

STOCKS_12M = ["RELIANCE.NS", "TCS.NS", "YESBANK.NS", "HDFCBANK.NS", "INFY.NS"]
FORECAST_DIR = "app/services"  # same as before

def load_12month_forecast(stock_symbol: str):
    if stock_symbol not in STOCKS_12M:
        raise ValueError("Stock not supported")

    path = os.path.join(FORECAST_DIR, f"forecast_12months_{stock_symbol}.csv")

    if not os.path.exists(path):
        raise FileNotFoundError("Forecast CSV missing")

    df = pd.read_csv(path)
    return df.to_dict(orient="records")
