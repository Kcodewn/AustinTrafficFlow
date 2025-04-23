# fetch_metadata.py
import pandas as pd
import os

def fetch_detector_locations():
    """
    Reads the 'Traffic_Detectors_20250421.csv' from data/processed,
    parses WKT 'LOCATION' into latitude/longitude, and writes
    a cleaned 'detector_locations.csv'.
    """
    # Path to the manually downloaded CSV within the project
    src_file = os.path.join(
        os.path.dirname(__file__),
        '../data/processed/Traffic_Detectors_20250421.csv'
    )
    df = pd.read_csv(src_file, low_memory=False)

    # Extract only the detector_id and WKT location
    df = df[['detector_id', 'LOCATION']].copy()
    df.columns = ['segment_id', 'location_wkt']

    # Parse "POINT (lon lat)" into numeric latitude & longitude
    def parse_wkt(wkt):
        try:
            coords = wkt.strip().lstrip('POINT (').rstrip(')').split()
            lon, lat = float(coords[0]), float(coords[1])
            return pd.Series([lat, lon])
        except:
            return pd.Series([pd.NA, pd.NA])

    df[['latitude', 'longitude']] = df['location_wkt'].apply(parse_wkt)
    df.drop(columns=['location_wkt'], inplace=True)
    df.dropna(subset=['latitude', 'longitude'], inplace=True)

    # Ensure processed folder exists
    out_dir = os.path.join(os.path.dirname(__file__), '../data/processed')
    os.makedirs(out_dir, exist_ok=True)

    # Write cleaned metadata
    out_path = os.path.join(out_dir, 'detector_locations.csv')
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} detector locations to {out_path}")

if __name__ == '__main__':
    fetch_detector_locations()
