from fastapi import APIRouter, HTTPException
from app.services.technical_indicators import get_technical_raw
from app.services.technical_scoring import calculate_score, decision
from app.services.technical_text import generate_text
from app.services import fundamentals as fund_service
from app.services.data_fetcher import get_stock_history
import pandas as pd
import math

router = APIRouter(
    prefix="/decision",
    tags=["decision"]
)

# ---------------- JSON-Safe Helper ----------------
def make_json_safe(d):
    """
    Recursively convert NaN/inf/-inf in dict/list to None
    """
    if isinstance(d, dict):
        return {k: make_json_safe(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [make_json_safe(x) for x in d]
    elif isinstance(d, float):
        if math.isnan(d) or math.isinf(d):
            return None
        return d
    else:
        return d

# ---------------- Decision Endpoint ----------------
@router.get("/{symbol}")
def decide(symbol: str):
    """
    Returns a combined decision for a stock:
    - Technical indicators and decision
    - Fundamental analysis and insights
    - Confidence scoring (Day 62)
    - Explainable output (Day 63)
    - Edge-case handling (Day 64)
    - Final stable decision API (Day 65)
    """
    # ---------------- Get Historical Data ----------------
    history = get_stock_history(symbol)
    if not history:
        raise HTTPException(status_code=404, detail="No historical data found for this stock")

    # Convert to DataFrame
    df = pd.DataFrame(history)
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock history is empty")

    # ---------------- Technical Analysis ----------------
    technicals = get_technical_raw(df, stock_symbol=symbol)

    # ---------- Day 62: Confidence Scoring ----------
    score = calculate_score(technicals)
    confidence = min(max(score, 0), 100)  # normalize score to 0-100

    # ---------- Day 63: Explainable Output ----------
    insights = generate_text(technicals)

    # ---------- Technical Decision ----------
    verdict = decision(score)

    # ---------------- Fundamental Analysis ----------------
    try:
        fund_metrics = fund_service.rank_metrics()  # ⚠️ Do NOT pass symbol
        fund_score = fund_metrics.get(symbol, None) if isinstance(fund_metrics, dict) else None
        layman = fund_service.layman_insights(symbol)
        top5 = fund_service.top5_positives_risks(symbol)
    except Exception:
        fund_score = layman = top5 = None

    # ---------------- Prepare JSON Response (Day 64 & 65) ----------------
    response = {
        "symbol": symbol,
        "technical": make_json_safe(technicals),        # Day 64: Edge-case safe
        "technical_score": score,
        "technical_confidence": confidence,             # Day 62
        "technical_decision": verdict,
        "technical_insights": insights,                 # Day 63
        "fundamental_score": make_json_safe(fund_score),
        "fundamental_layman": layman,
        "fundamental_top5": top5
    }

    # Day 65: Final decision API – all combined, safe, explainable
    return response
