from sodapy import Socrata
import requests
import pandas as pd

def fetch_traffic_data(limit=50000):
    # domain, no app_token → public reads only
    client = Socrata("data.austintexas.gov", None)
    # “i626-g7ub” is the Austin Traffic Detectors dataset
    results = client.get("i626-g7ub", limit=limit)
    df = pd.DataFrame.from_records(results)
    print(f"Fetched {df.shape[0]} records")
    return df

def fetch_weather_data(lat, lon, start_date, end_date, api_key):
    url = "https://history.openweathermap.org/data/2.5/history/city"
    params = {
        "lat": lat,
        "lon": lon,
        "type": "hour",
        "start": int(pd.Timestamp(start_date).timestamp()),
        "end": int(pd.Timestamp(end_date).timestamp()),
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather_data = response.json()['list']
        weather_df = pd.json_normalize(weather_data)
        weather_df['timestamp'] = pd.to_datetime(weather_df['dt'], unit='s')
        return weather_df
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")

if __name__ == "__main__":
    df_traffic = fetch_traffic_data()
    df_traffic.to_json('../data/raw/raw_traffic.json', orient='records', lines=True)
    # Optional: fetch and save weather data similarly
