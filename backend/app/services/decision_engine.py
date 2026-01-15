def fundamental_score(fundamentals):
    score = 0
    if fundamentals["roe"] > 15: score += 30
    if fundamentals["pe"] < 20: score += 30
    if fundamentals["debt_to_equity"] < 0.5: score += 40
    return score


def technical_score(tech):
    score = 0
    if tech["rsi"] < 30: score += 30
    if tech["macd"] > 0: score += 30
    if tech["trend"] == "Uptrend": score += 40
    return score


def forecast_score(current, forecast):
    change = (forecast - current) / current

    if change > 0.2: return 100
    if change > 0.1: return 70
    if change > 0: return 40
    return 0

def final_decision(f_score, t_score, fcast_score):
    final = (
        0.4 * f_score +
        0.3 * t_score +
        0.3 * fcast_score
    )

    if final >= 75:
        decision = "BUY"
    elif final >= 50:
        decision = "HOLD"
    else:
        decision = "SELL"

    return round(final, 2), decision

def explain(f_score, t_score, fcast_score):
    reasons = []

    if f_score >= 70:
        reasons.append("Strong company fundamentals")
    if t_score >= 70:
        reasons.append("Bullish technical indicators")
    if fcast_score >= 70:
        reasons.append("Positive 12-month forecast")

    if not reasons:
        reasons.append("Weak signals across indicators")

    return reasons

