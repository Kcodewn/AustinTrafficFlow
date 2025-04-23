import pandas as pd

if __name__ == "__main__":
    # Load your cleaned traffic data
    df = pd.read_csv(
        '../data/processed/traffic_data.csv',
        parse_dates=['timestamp']
    )

    # Load the manually downloaded detector locations
    loc = pd.read_csv(
        '../data/processed/detector_locations.csv'
    )

    # Keep/rename the columns we need
    loc = loc.rename(columns={
        'detector_id': 'segment_id',
        'location_latitude': 'latitude',
        'location_longitude': 'longitude'
    })[['segment_id','latitude','longitude']]

    # Merge on segment_id
    df_with_loc = df.merge(loc, how='left', on='segment_id')

    # Check for any missing coords
    missing = df_with_loc['latitude'].isna().sum()
    print(f"{missing} rows without location—if >0, verify your CSV")

    # Save the enriched file
    df_with_loc.to_csv(
        '../data/processed/traffic_with_loc.csv',
        index=False
    )
    print("✅ Saved: data/processed/traffic_with_loc.csv")
