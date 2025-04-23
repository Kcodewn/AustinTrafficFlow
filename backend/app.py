from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR   = os.path.dirname(__file__)
HIST_PATH  = os.path.join(BASE_DIR, '../data/processed/traffic_with_loc.csv')
META_PATH  = os.path.join(BASE_DIR, '../data/processed/detector_locations.csv')

# 1) Load historical traffic (with lat/lon)
df_hist = pd.read_csv(HIST_PATH, parse_dates=['timestamp'])

# 2) Build full metadata lookup
loc_df = pd.read_csv(META_PATH)
loc_lookup = {
    row['segment_id']:(row['latitude'], row['longitude'])
    for _, row in loc_df.iterrows()
}

# 3) Precompute time‐of‐day averages
df_hist['dow']     = df_hist['timestamp'].dt.dayofweek
df_hist['timebin']= df_hist['timestamp'].dt.strftime('%H:%M')
avg_df = (
    df_hist
    .groupby(['segment_id','dow','timebin'])['speed']
    .mean()
    .reset_index()
)
avg_lookup = {
    (row.segment_id, row.dow, row.timebin): row.speed
    for row in avg_df.itertuples()
}

# 4) Precompute per‐segment overall average
seg_avg = (
    df_hist
    .groupby('segment_id')['speed']
    .mean()
    .to_dict()
)

def get_color(speed):
    if speed < 15: return 'red'
    if speed < 30: return 'yellow'
    return 'gray'

@app.route('/traffic')
def traffic():
    ts_req = pd.to_datetime(request.args.get('time'))
    timebin = ts_req.strftime('%H:%M')
    dow     = ts_req.dayofweek

    results = []
    # Historical exact matches
    hist = (
        df_hist[df_hist['timestamp'] == ts_req]
        .dropna(subset=['latitude','longitude'])
    )
    done = set()
    for _, row in hist.iterrows():
        seg = int(row.segment_id)
        results.append({
            'segment_id': seg,
            'latitude': float(row.latitude),
            'longitude': float(row.longitude),
            'speed': float(row.speed),
            'color': get_color(row.speed)
        })
        done.add(seg)

    # Fallback for every other segment
    for seg, (lat, lon) in loc_lookup.items():
        if seg in done:
            continue
        # invalid coords?
        if pd.isna(lat) or pd.isna(lon):
            continue

        # 1) try time‐of‐day average
        pred = avg_lookup.get((seg, dow, timebin))
        # 2) fallback to overall segment average
        if pred is None or np.isnan(pred):
            pred = seg_avg.get(seg)
        # 3) if still missing, skip
        if pred is None or np.isnan(pred):
            continue

        results.append({
            'segment_id': seg,
            'latitude': float(lat),
            'longitude': float(lon),
            'speed': float(pred),
            'color': get_color(pred)
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
