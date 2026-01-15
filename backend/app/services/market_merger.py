import pandas as pd

def merge_nse_bse(nse_df: pd.DataFrame, bse_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge NSE and BSE data, preferring NSE prices.
    """

    nse_df["Exchange"] = "NSE"
    bse_df["Exchange"] = "BSE"

    merged = pd.merge(
        nse_df,
        bse_df,
        on="Date",
        how="outer",
        suffixes=("_nse", "_bse")
    )

    merged["Close_Final"] = merged["Close_nse"].combine_first(
        merged["Close_bse"]
    )

    final_df = merged[["Date", "Close_Final"]].sort_values("Date")

    return final_df
