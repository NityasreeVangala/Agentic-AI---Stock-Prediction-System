from backend.app.services.data_fetcher import fetch_stock_data, clean_stock_data
from backend.app.services.market_merger import merge_nse_bse
def run_test():
    nse = fetch_stock_data("TCS.NS")
    bse = fetch_stock_data("TCS.BO")

    nse = clean_stock_data(nse)
    bse = clean_stock_data(bse)

    merged = merge_nse_bse(nse, bse)

    print("NSE rows:", len(nse))
    print("BSE rows:", len(bse))
    print("Merged rows:", len(merged))
    print("\nSample data:")
    print(merged.head())
    print("\nLast date:", merged["Date"].max())

if __name__ == "__main__":
    run_test()
