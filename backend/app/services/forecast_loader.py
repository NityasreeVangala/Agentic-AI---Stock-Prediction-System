import os
import pandas as pd
from fastapi import HTTPException

from app.services.data_fetcher import get_stock_history

FORECAST_DIR = "app/services"

def load_forecast(symbol: str):
    path = os.path.join(
        FORECAST_DIR,
        f"forecast_12months_{symbol}.csv"
    )

    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail=f"Forecast file missing for {symbol}"
        )

    df = pd.read_csv(path)

    if df.empty:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast CSV empty for {symbol}"
        )

    # ✅ REAL current market price
    history = get_stock_history(symbol)
    current_price = float(history[-1]["Close"])

    # ✅ 12-month outlook
    last_row = df.iloc[-1]
    forecast_price = float(last_row["Ensemble"])

    return {
        "current_price": round(current_price, 2),
        "forecast_price": round(forecast_price, 2),
        "full": df.to_dict(orient="records")
    }
