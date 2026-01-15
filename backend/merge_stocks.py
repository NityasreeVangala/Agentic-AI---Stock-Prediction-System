import pandas as pd
import os

# Path where your separate stock CSVs are
stocks_folder = "app/data/"

# List of your 5 stock files
stock_files = [
    "TCS.NS.csv",
    "RELIANCE.NS.csv",
    "HDFCBANK.NS.csv",
    "YESBANK.NS.csv",
    "INFY.NS.csv"
]

# List to store individual dataframes
dfs = []

# Read each file and append to dfs
for file in stock_files:
    path = os.path.join(stocks_folder, file)
    df = pd.read_csv(path)
    
    # Add a column for symbol if not present
    if 'Symbol' not in df.columns:
        df['Symbol'] = file.replace(".csv","")
    
    dfs.append(df)

# Concatenate all 5 dataframes
all_stocks_df = pd.concat(dfs, ignore_index=True)

# Save as the single combined CSV for your backend
all_stocks_df.to_csv("app/data/all_stock_prices.csv", index=False)

print("✅ Combined CSV created!")
print("Shape:", all_stocks_df.shape)
print("Columns:", all_stocks_df.columns.tolist())
