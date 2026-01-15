def generate_text(row):
    insights = []

    # RSI
    if row["RSI"] > 70:
        insights.append("RSI indicates the stock is overbought")
    elif row["RSI"] < 30:
        insights.append("RSI indicates the stock is oversold")
    else:
        insights.append("RSI is in a healthy range")

    # MACD
    if row["MACD"] > row["MACD_SIGNAL"]:
        insights.append("MACD shows bullish momentum")
    else:
        insights.append("MACD shows bearish momentum")

    # Moving averages
    if row["Close"] > row["MA50"]:
        insights.append("Price is above 50-day average (bullish)")
    else:
        insights.append("Price is below 50-day average (bearish)")

    # Bollinger Bands
    if row["Close"] > row["BB_UPPER"]:
        insights.append("Price is above upper Bollinger Band (overextended)")
    elif row["Close"] < row["BB_LOWER"]:
        insights.append("Price is below lower Bollinger Band (possible bounce)")

    # Volume
    if row["Volume"] > row["VOL_AVG"]:
        insights.append("High volume confirms the price move")

    return insights
