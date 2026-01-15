import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib

def train_lstm(stock_csv_path="app/data/all_stock_prices.csv", timesteps=30):
    df = pd.read_csv(stock_csv_path, parse_dates=["Date"]).sort_values("Date")
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

    model = Sequential()
    model.add(LSTM(50, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")

    model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

    model.save("app/services/lstm_model.h5")
    joblib.dump(scaler, "app/services/models/lstm_scaler.pkl")
    print("✅ LSTM model and scaler saved!")

train_lstm()
