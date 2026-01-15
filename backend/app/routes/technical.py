from fastapi import APIRouter
from app.services.technical_indicators import apply_indicators
from app.services.technical_scoring import calculate_score, decision
from app.services.technical_text import generate_text
from app.services.data_fetcher import get_stock_history
import pandas as pd

router = APIRouter()

@router.get("/technical/{symbol}")
def technical(symbol: str):
    """
    Returns technical analysis for a stock
    """

    # Get historical price data (list of dicts)
    history = get_stock_history(symbol)

    # Convert to DataFrame
    df = pd.DataFrame(history)

    if df.empty:
        return {"error": "No data found"}

    # Apply indicators
    df = apply_indicators(df)

    # Use latest row for decision
    latest = df.iloc[-1]

    score = calculate_score(latest)
    decision_text = decision(score)
    insights = generate_text(latest)

    return {
        "symbol": symbol,
        "score": score,
        "decision": decision_text,
        "insights": insights
    }
