import os

def save_to_csv(df, symbol):
    # Ensure 'data/' folder exists
    os.makedirs("data", exist_ok=True)
    
    # Path for this stock
    file_path = f"data/{symbol}.csv"
    
    # Save CSV, overwrite if exists
    df.to_csv(file_path, index=False)
    
    print(f"[INFO] Saved {symbol} data to {file_path}")
