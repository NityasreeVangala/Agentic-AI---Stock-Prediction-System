from fastapi import APIRouter, HTTPException
from app.services.data_fetcher import get_stock_history
from app.services.technical_indicators import get_technical_raw
from app.services import fundamentals as fund_service
import pandas as pd
import math

router = APIRouter(prefix="/explain", tags=["explanation"])

# ---------------- JSON Safe ----------------
def make_json_safe(x):
    if isinstance(x, dict):
        return {k: make_json_safe(v) for k, v in x.items()}
    if isinstance(x, list):
        return [make_json_safe(i) for i in x]
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        return round(x, 2)
    return x

# ---------------- SCRATCH LLM EXPLANATION ----------------
def generate_explanation(symbol, tech, fund):
    explanations = []

    # ===== RSI =====
    rsi = tech.get("RSI")
    if rsi is not None:
        if rsi < 30:
            explanations.append(
                f"RSI is {rsi}, which means the stock is oversold and may see a bounce."
            )
        elif rsi < 45:
            explanations.append(
                f"RSI is {rsi}, showing weak momentum."
            )
        elif rsi <= 55:
            explanations.append(
                f"RSI is {rsi}, indicating neutral momentum."
            )
        elif rsi <= 70:
            explanations.append(
                f"RSI is {rsi}, indicating healthy bullish momentum."
            )
        else:
            explanations.append(
                f"RSI is {rsi}, suggesting the stock may be overbought."
            )
    else:
        explanations.append("RSI data is not available.")

    # ===== MACD =====
    macd = tech.get("MACD")
    signal = tech.get("MACD_SIGNAL")
    if macd is not None and signal is not None:
        if macd > signal:
            explanations.append(
                "MACD is above the signal line, indicating bullish momentum."
            )
        else:
            explanations.append(
                "MACD is below the signal line, indicating bearish momentum."
            )
    else:
        explanations.append("MACD data is incomplete.")

    # ===== Moving Average =====
    close = tech.get("Close")
    ma50 = tech.get("MA50")
    if close and ma50:
        if close > ma50:
            explanations.append(
                "The stock price is above the 50-day moving average, which is bullish."
            )
        else:
            explanations.append(
                "The stock price is below the 50-day moving average, which is bearish."
            )

    # ===== Volume =====
    vol = tech.get("Volume")
    vol_avg = tech.get("VOL_AVG")
    if vol and vol_avg:
        if vol > vol_avg:
            explanations.append(
                "Trading volume is higher than average, confirming market interest."
            )
        else:
            explanations.append(
                "Trading volume is lower than average, indicating weak participation."
            )

    # ===== Fundamentals =====
    if fund:
        pe = fund.get("PE")
        eps = fund.get("EPS")
        roe = fund.get("ROE")
        debt = fund.get("Debt")

        if pe is not None:
            if pe < 15:
                explanations.append(f"PE ratio is {pe}, which suggests undervaluation.")
            elif pe < 30:
                explanations.append(f"PE ratio is {pe}, which is fairly valued.")
            else:
                explanations.append(f"PE ratio is {pe}, which appears expensive.")

        if eps is not None:
            explanations.append(
                f"EPS is {eps}, showing {'strong' if eps > 3 else 'weak'} earnings."
            )

        if roe is not None:
            explanations.append(
                f"ROE is {roe}%, indicating {'good' if roe > 15 else 'moderate'} profitability."
            )

        if debt is not None:
            explanations.append(
                f"Debt score is {debt}, which means {'low' if debt <= 2 else 'high'} financial risk."
            )
    else:
        explanations.append("Fundamental data is not available.")

    # ===== Risk Disclaimer =====
    explanations.append(
        "Disclaimer: This analysis is for educational purposes only and not financial advice."
    )

    return explanations

# ---------------- API ENDPOINT ----------------
@router.get("/{symbol}")
def explain_stock(symbol: str):
    history = get_stock_history(symbol)
    if not history:
        raise HTTPException(status_code=404, detail="No historical data found")

    df = pd.DataFrame(history)
    if df.empty:
        raise HTTPException(status_code=404, detail="Empty stock data")

    technical = get_technical_raw(df, stock_symbol=symbol)

    try:
        fund_metrics = fund_service.rank_metrics()
        fundamentals = fund_metrics.get(symbol)
    except Exception:
        fundamentals = None

    explanation = generate_explanation(
        symbol,
        make_json_safe(technical),
        make_json_safe(fundamentals)
    )

    return {
        "symbol": symbol,
        "technical": make_json_safe(technical),
        "fundamental": make_json_safe(fundamentals),
        "explanation": explanation
    }
