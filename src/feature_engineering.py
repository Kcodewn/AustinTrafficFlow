import pandas as pd
import numpy as np


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based and cyclical features for modeling traffic flow.

    Args:
        df: DataFrame with columns ['segment_id', 'timestamp', 'volume', 'speed', 'occupancy']

    Returns:
        DataFrame with additional feature columns.
    """
    # Extract basic time features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

    # Cyclical encoding for hour (24h) and day_of_week (7 days)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)

    return df


if __name__ == '__main__':
    # Load preprocessed data
    df = pd.read_csv('../data/processed/traffic_data.csv', parse_dates=['timestamp'])

    # Generate features
    df_feat = feature_engineering(df)

    # Save feature-engineered dataset
    df_feat.to_csv('../data/processed/traffic_features.csv', index=False)
    print(f"✅ Saved feature-engineered data to data/processed/traffic_features.csv ({df_feat.shape[0]} rows, {df_feat.shape[1]} columns)")
