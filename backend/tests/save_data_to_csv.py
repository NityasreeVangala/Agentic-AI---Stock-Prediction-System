import sys
import os
sys.path.append(os.path.abspath("app"))

from services.data_fetcher import fetch_stock_data, clean_stock_data
from services.market_merger import merge_nse_bse
from services.data_saver import save_to_csv


# Example: save 5 stocks
symbols = ["TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "YESBANK.NS", "INFY.NS"]

for sym in symbols:
    nse = fetch_stock_data(sym)
    bse = fetch_stock_data(sym.replace(".NS", ".BO"))
    
    nse_clean = clean_stock_data(nse)
    bse_clean = clean_stock_data(bse)
    
    merged = merge_nse_bse(nse_clean, bse_clean)
    
    save_to_csv(merged, sym.replace(".NS",""))
