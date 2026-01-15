def calculate_score(row):
    score = 50  # neutral baseline

    # RSI
    if row["RSI"] < 30:
        score += 15
    elif row["RSI"] > 70:
        score -= 15

    # MACD
    if row["MACD"] > row["MACD_SIGNAL"]:
        score += 15
    else:
        score -= 15

    # Moving Average
    if row["Close"] > row["MA50"]:
        score += 10
    else:
        score -= 10

    # Bollinger
    if row["Close"] < row["BB_LOWER"]:
        score += 5
    elif row["Close"] > row["BB_UPPER"]:
        score -= 5

    # Volume
    if row["Volume"] > row["VOL_AVG"]:
        score += 5

    return max(0, min(100, score))


def decision(score):
    if score >= 70:
        return "BUY"
    elif score >= 40:
        return "HOLD"
    else:
        return "SELL"
