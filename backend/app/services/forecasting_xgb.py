# app/services/forecasting_xgb.py
import sys
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
import numpy as np
import os

def train_xgb(stock_symbol, stock_csv_path="app/data/all_stock_prices.csv"):
    print(f"✅ Loading CSV: {stock_csv_path}")
    df = pd.read_csv(stock_csv_path, parse_dates=["Date"])
    
    # Filter for selected stock
    df = df[df['Symbol'] == stock_symbol].sort_values("Date")
    print(f"Initial rows for {stock_symbol}: {len(df)}")

    # Feature engineering
    for lag in range(1, 4):
        df[f"Close_lag{lag}"] = df["Close"].shift(lag)
    df["MA3"] = df["Close"].rolling(3).mean()
    df["MA7"] = df["Close"].rolling(7).mean()

    df = df.dropna()
    print(f"Rows after lag/rolling features: {len(df)}")

    feature_cols = ["Close_lag1", "Close_lag2", "Close_lag3", "MA3", "MA7"]
    X = df[feature_cols]
    y = df["Close"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )
    print(f"Training rows: {len(X_train)}, Testing rows: {len(X_test)}")

    # Train model
    model = xgb.XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics (avoid `squared` keyword issue)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    print(f"XGBoost RMSE: {rmse:.2f}, MAE: {mae:.2f}")

    # Save model
    os.makedirs("app/services/models", exist_ok=True)
    model_path = f"app/services/models/xgb_model_{stock_symbol}.pkl"
    joblib.dump(model, model_path)
    print(f"✅ XGBoost model saved: {model_path}")

    return model, X_test, y_test, y_pred

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python forecasting_xgb.py STOCK_SYMBOL")
        sys.exit(1)
    stock_symbol = sys.argv[1]
    train_xgb(stock_symbol)
