# precompute_forecasts.py
from backend.app.services.forecast_12months import forecast_12months

STOCKS = ["RELIANCE.NS", "TCS.NS", "YESBANK.NS", "HDFCBANK.NS", "INFY.NS"]

if __name__ == "__main__":
    for stock in STOCKS:
        print(f"\n--- Processing {stock} ---")
        try:
            forecast_12months(stock)
        except Exception as e:
            print(f"❌ Failed for {stock}: {e}")
    print("\n🎉 All forecasts precomputed!")
