import pandas as pd

def preprocess_traffic_data(df):
    # 1) slice + copy to avoid SettingWithCopyWarning
    df = df[['detid', 'curdatetime', 'volume', 'speed', 'occupancy']].copy()
    
    # 2) rename
    df.columns = ['segment_id', 'timestamp', 'volume', 'speed', 'occupancy']
    
    # 3) parse + coerce bad values
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    for col in ['volume', 'speed', 'occupancy']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 4) drop any rows missing our critical fields
    df.dropna(subset=['timestamp','volume','speed','occupancy'], inplace=True)
    
    # 5) set timestamp index
    df.set_index('timestamp', inplace=True)
    
    # 6) group-by segment and resample every 15 minutes, averaging numeric fields
    df_grouped = (
        df
        .groupby('segment_id')
        .resample('15min')
        .mean()
    )
    
    # 7) drop the auto‑aggregated 'segment_id' column before reset_index
    df_grouped = df_grouped.drop(columns=['segment_id'])
    
    # 8) bring 'segment_id' (index level) and 'timestamp' back as columns
    df_agg = df_grouped.reset_index()
    
    print(f"Processed {df_agg.shape[0]} rows (segment × time bins)")
    return df_agg

if __name__ == "__main__":
    # load the raw lines‑JSON you fetched
    df_raw = pd.read_json('../data/raw/raw_traffic.json', lines=True)
    
    df_processed = preprocess_traffic_data(df_raw)
    df_processed.to_csv('../data/processed/traffic_data.csv', index=False)
    print("Saved cleaned data to data/processed/traffic_data.csv")
