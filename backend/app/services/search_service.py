# A simple in-memory list for autocomplete
STOCK_SYMBOLS = ["TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "YESBANK.NS", "INFY.NS"]

def search_stocks(query: str):
    query = query.lower()
    matches = [s for s in STOCK_SYMBOLS if s.lower().startswith(query)]
    return matches
