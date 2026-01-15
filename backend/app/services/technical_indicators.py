import pandas as pd

def apply_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ---------- Moving Averages ----------
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    # ---------- RSI ----------
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # ---------- MACD ----------
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # ---------- Bollinger Bands ----------
    std = df["Close"].rolling(20).std()
    df["BB_UPPER"] = df["MA20"] + (2 * std)
    df["BB_LOWER"] = df["MA20"] - (2 * std)

    # ---------- Volume ----------
    df["VOL_AVG"] = df["Volume"].rolling(20).mean()

    return df

def get_technical_raw(df, stock_symbol=None):
    """
    Return raw technical indicators
    """
    df = apply_indicators(df)
    if stock_symbol:
        return df.iloc[-1].to_dict()
    return df.to_dict(orient="records")