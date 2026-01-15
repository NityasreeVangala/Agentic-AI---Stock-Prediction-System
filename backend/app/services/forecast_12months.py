import sys
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def forecast_12months(stock_symbol):
    print(f"\n📈 Generating 12-month forecast for {stock_symbol}")

    # --- Load CSV ---
    df = pd.read_csv("app/data/all_stock_prices.csv", parse_dates=["Date"])
    df = df[df["Symbol"] == stock_symbol].sort_values("Date")
    print(f"Rows for {stock_symbol}: {len(df)}")

    close_prices = df["Close"].values.reshape(-1, 1)

    # --- Load XGBoost model ---
    xgb_model_path = f"app/services/models/xgb_model_{stock_symbol}.pkl"
    xgb_model = joblib.load(xgb_model_path)
    print("✅ XGBoost model loaded!")

    # --- Load LSTM model + scaler ---
    lstm_model_path = f"app/services/models/lstm_model_{stock_symbol}.h5"
    lstm_scaler_path = f"app/services/models/lstm_scaler_{stock_symbol}.pkl"

    lstm_model = load_model(lstm_model_path, compile=False)
    scaler = joblib.load(lstm_scaler_path)
    print("✅ LSTM model and scaler loaded!")

    # --- Prepare XGBoost input ---
    lag1, lag2, lag3 = close_prices[-1, 0], close_prices[-2, 0], close_prices[-3, 0]
    ma3 = close_prices[-3:, 0].mean()
    ma7 = close_prices[-7:, 0].mean() if len(close_prices) >= 7 else close_prices[:, 0].mean()
    xgb_input = np.array([[lag1, lag2, lag3, ma3, ma7]])

    # --- Prepare LSTM input ---
    timesteps = 30
    if len(close_prices) < timesteps:
        raise ValueError("Not enough data for LSTM timesteps")
    lstm_input = close_prices[-timesteps:]
    lstm_input_scaled = scaler.transform(lstm_input)
    lstm_input_scaled = lstm_input_scaled.reshape(1, timesteps, 1)

    # --- Forecast for 12 months ---
    xgb_forecast = []
    lstm_forecast = []

    for month in range(12):
        # XGBoost prediction
        pred_xgb = xgb_model.predict(xgb_input)[0]
        xgb_forecast.append(pred_xgb)

        # Shift lags for next iteration
        lag1, lag2, lag3 = pred_xgb, lag1, lag2
        ma3 = np.mean([lag1, lag2, lag3])
        ma7 = np.mean([lag1, lag2, lag3, ma3, ma3, ma3, ma3])
        xgb_input = np.array([[lag1, lag2, lag3, ma3, ma7]])

        # LSTM prediction
        pred_lstm_scaled = lstm_model.predict(lstm_input_scaled, verbose=0)[0, 0]
        lstm_forecast.append(scaler.inverse_transform([[pred_lstm_scaled]])[0, 0])

        # Update LSTM input for next step
        lstm_input_scaled = np.roll(lstm_input_scaled, -1, axis=1)
        lstm_input_scaled[0, -1, 0] = pred_lstm_scaled

    # --- Combine results ---
    forecast_df = pd.DataFrame({
        "Month": [f"Month {i+1}" for i in range(12)],
        "XGB": xgb_forecast,
        "LSTM": lstm_forecast
    })

    forecast_df["Ensemble"] = (forecast_df["XGB"] + forecast_df["LSTM"]) / 2

    print("\n✅ 12-month forecast complete!\n")
    print(forecast_df)

    # --- Save forecasts ---
    forecast_df.to_csv(f"app/services/forecast_12months_{stock_symbol}.csv", index=False)
    print(f"✅ Forecast saved: app/services/forecast_12months_{stock_symbol}.csv")

    return forecast_df


# --- CLI execution ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python forecast_12months.py <STOCK_SYMBOL>")
        sys.exit(1)

    stock = sys.argv[1]
    forecast_12months(stock)
