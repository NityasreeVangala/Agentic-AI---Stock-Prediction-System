# backend/app/services/fundamentals_service.py
import pandas as pd

# 1️⃣ Simulated fundamentals for 5 stocks
FUNDAMENTALS = {
    "TCS.NS": {"PE": 28, "EPS": 120, "ROE": 15, "Debt": 0.2},
    "RELIANCE.NS": {"PE": 25, "EPS": 90, "ROE": 18, "Debt": 0.4},
    "HDFCBANK.NS": {"PE": 22, "EPS": 100, "ROE": 14, "Debt": 0.3},
    "YESBANK.NS": {"PE": 15, "EPS": 20, "ROE": 8, "Debt": 1.2},
    "INFY.NS": {"PE": 30, "EPS": 110, "ROE": 16, "Debt": 0.1},
}

def get_fundamental_raw(stock):
    """
    Return raw fundamental data for a stock.
    """
    return FUNDAMENTALS.get(stock, {})

def fetch_and_normalize_fundamentals(stocks=None):
    """
    Fetch fundamentals for given stocks (or all 5 if none specified)
    and normalize values between 0 and 1.
    """
    # 2️⃣ Filter stocks if specified
    if stocks:
        data = {s: FUNDAMENTALS[s] for s in stocks if s in FUNDAMENTALS}
    else:
        data = FUNDAMENTALS.copy()
    
    # 3️⃣ Convert to DataFrame
    df = pd.DataFrame(data).T  # transpose so rows = stocks
    df.index.name = "Symbol"

    # 4️⃣ Min-Max normalization
    normalized_df = (df - df.min()) / (df.max() - df.min())

    return normalized_df

# ✅ Example usage
if __name__ == "__main__":
    normalized = fetch_and_normalize_fundamentals()
    print("Normalized Fundamentals:\n", normalized)
