# app/services/forecasting_lstm.py
import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

def train_lstm(stock_symbol, stock_csv_path="app/data/all_stock_prices.csv", timesteps=30):
    print(f"✅ Loading CSV: {stock_csv_path}")
    df = pd.read_csv(stock_csv_path, parse_dates=["Date"])
    
    # Filter for selected stock
    df = df[df['Symbol'] == stock_symbol].sort_values("Date")
    print(f"Rows for {stock_symbol}: {len(df)}")

    close_prices = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    close_scaled = scaler.fit_transform(close_prices)

    X, y = [], []
    for i in range(timesteps, len(close_scaled)):
        X.append(close_scaled[i-timesteps:i, 0])
        y.append(close_scaled[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Build LSTM
    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")

    # Train
    model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

    # Save model and scaler
    os.makedirs("app/services/models", exist_ok=True)
    model_path = f"app/services/models/lstm_model_{stock_symbol}.h5"
    scaler_path = f"app/services/models/lstm_scaler_{stock_symbol}.pkl"
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    print(f"✅ LSTM model saved: {model_path}")
    print(f"✅ LSTM scaler saved: {scaler_path}")

    return model, X_test, y_test, scaler

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python forecasting_lstm.py STOCK_SYMBOL")
        sys.exit(1)
    stock_symbol = sys.argv[1]
    train_lstm(stock_symbol)
