import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def train_arima_for_segment(csv_path: str, segment_id: int, order=(2,0,2)):
    """
    Train and evaluate an ARIMA model for one road segment's volume time series.

    Args:
        csv_path: Path to processed CSV with columns ['segment_id','timestamp','volume',...]
        segment_id: ID of the road segment to model
        order: ARIMA(p,d,q) order
    """
    # Load the data
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    df.set_index('timestamp', inplace=True)
    # Filter to the chosen segment
    df_seg = df[df['segment_id'] == segment_id]
    # Ensure regular frequency and fill missing values
    ts = df_seg['volume'].asfreq('15min').ffill()
    # Split into train/test (e.g., last 20% for test)
    split_idx = int(len(ts) * 0.8)
    train, test = ts.iloc[:split_idx], ts.iloc[split_idx:]
    # Fit the model
    model = ARIMA(train, order=order).fit()
    # Forecast
    forecast = model.forecast(steps=len(test))
    # Metrics
    mae = mean_absolute_error(test, forecast)
    rmse = mean_squared_error(test, forecast, squared=False)
    print(f"Segment {segment_id} ARIMA{order} MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    # Ensure models directory exists
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f'arima_segment_{segment_id}.pkl')
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    train_arima_for_segment(
        csv_path='../data/processed/traffic_data.csv',
        segment_id=80,
        order=(2,0,2)
    )
