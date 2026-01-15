from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd

# ----------------- Services -----------------
from app.services.search_service import search_stocks
from app.services.data_fetcher import get_stock_history, load_stock_df  # ✅ ADD load_stock_df
from app.services import fundamentals as fund_service
from app.data.fundamentals_data import fundamentals
from app.services.technical_indicators import apply_indicators
from app.services.technical_scoring import calculate_score, decision
from app.services.technical_text import generate_text

# ----------------- Routers -----------------
from app.routes.technical import router as technical_router
from app.routes.decision import router as decision_router
from app.routes.explanation import router as explanation_router

# ----------------- FastAPI App -----------------
app = FastAPI(title="Agentic Stock AI")

# ----------------- CORS -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Include Routers -----------------
app.include_router(technical_router)
app.include_router(decision_router)
app.include_router(explanation_router)

# ----------------- Root -----------------
@app.get("/")
def root():
    return {"status": "Backend running"}

# ----------------- Search -----------------
@app.get("/search")
def search(q: str = Query(...)):
    return {"results": search_stocks(q)}

# ----------------- History (FRONTEND SAFE) -----------------
@app.get("/history/{symbol}")
def history(symbol: str, limit: int = 200):
    return {
        "history": get_stock_history(symbol, limit=limit)
    }

# ----------------- Fundamentals -----------------
@app.get("/fundamentals")
def all_fundamentals():
    return fundamentals

@app.get("/fundamentals/rank")
def rank():
    return fund_service.rank_metrics()

@app.get("/fundamentals/insight/{symbol}")
def insight(symbol: str):
    return fund_service.layman_insights(symbol)

@app.get("/fundamentals/top5/{symbol}")
def top5(symbol: str):
    return fund_service.top5_positives_risks(symbol)

# ----------------- Technical Indicators (🔥 FIXED) -----------------
@app.get("/technical/{symbol}")
def technical(symbol: str):
    # ✅ BACKEND-ONLY full dataframe
    df = load_stock_df(symbol)

    if df.empty:
        raise HTTPException(status_code=404, detail="No historical data found")

    df = apply_indicators(df)
    latest = df.iloc[-1]

    score = calculate_score(latest)
    verdict = decision(score)
    explanation = generate_text(latest)

    return {
        "symbol": symbol,
        "technical": {
            "date": str(latest.get("Date")),
            "open": float(latest.get("Open", 0)),
            "high": float(latest.get("High", 0)),
            "low": float(latest.get("Low", 0)),
            "close": float(latest.get("Close", 0)),
            "volume": float(latest.get("Volume", 0)),
            "rsi": round(float(latest.get("RSI", 0)), 2),
            "macd": round(float(latest.get("MACD", 0)), 2),
            "macd_signal": round(float(latest.get("MACD_SIGNAL", 0)), 2),
            "ma20": round(float(latest.get("MA20", 0)), 2),
            "ma50": round(float(latest.get("MA50", 0)), 2),
            "ma200": round(float(latest.get("MA200", 0)), 2),
            "bb_upper": round(float(latest.get("BB_UPPER", 0)), 2),
            "bb_lower": round(float(latest.get("BB_LOWER", 0)), 2),
        },
        "score": score,
        "decision": verdict,
        "explanation": explanation
    }

# ----------------- 12-Month Forecast -----------------
FORECAST_DIR = "app/services"
STOCKS_12M = ["RELIANCE.NS", "TCS.NS", "YESBANK.NS", "HDFCBANK.NS", "INFY.NS"]

def load_12month_forecast(stock_symbol: str):
    if stock_symbol not in STOCKS_12M:
        raise HTTPException(status_code=404, detail="Stock not supported")

    path = os.path.join(FORECAST_DIR, f"forecast_12months_{stock_symbol}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Forecast CSV missing")

    df = pd.read_csv(path)
    return df.to_dict(orient="records")

@app.get("/forecast/12months/{symbol}")
def forecast_12months(symbol: str):
    return {
        "stock": symbol,
        "forecast": load_12month_forecast(symbol)
    }

@app.get("/forecast/12months_all")
def forecast_12months_all():
    return {
        stock: load_12month_forecast(stock)
        for stock in STOCKS_12M
    }

# ----------------- Backtesting -----------------
@app.get("/backtest/{symbol}")
def backtest(symbol: str):
    return {"status": f"Backtesting logic for {symbol} coming soon"}
