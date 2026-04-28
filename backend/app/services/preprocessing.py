"""
Data Preprocessing Service
Handles data cleaning, feature extraction, and normalization
"""

import pandas as pd
import numpy as np
from datetime import datetime

def preprocess_crime_data(df):
    """
    Preprocess crime data by handling missing values and extracting features
    
    Args:
        df: pandas DataFrame with raw crime data
    
    Returns:
        pandas DataFrame with processed data
    """
    print("Preprocessing crime data...")
    
    # Make a copy to avoid modifying original data
    df_processed = df.copy()
    
    # 1. Handle missing values
    # Drop rows with missing critical fields
    df_processed = df_processed.dropna(subset=['latitude', 'longitude', 'crime_type'])
    
    # Fill missing dates with current date
    if 'date' in df_processed.columns:
        df_processed['date'] = df_processed['date'].fillna(datetime.now())
    
    # 2. Extract time-based features
    if 'date' in df_processed.columns:
        df_processed['date'] = pd.to_datetime(df_processed['date'])
        
        # Extract hour (0-23)
        df_processed['hour'] = df_processed['date'].dt.hour
        
        # Extract day of week (0=Monday, 6=Sunday)
        df_processed['day'] = df_processed['date'].dt.dayofweek
        
        # Extract month (1-12)
        df_processed['month'] = df_processed['date'].dt.month
        
        # Extract day of month (1-31)
        df_processed['day_of_month'] = df_processed['date'].dt.day
    
    # 3. Validate coordinates
    # Ensure latitude is between -90 and 90
    df_processed = df_processed[
        (df_processed['latitude'] >= -90) & 
        (df_processed['latitude'] <= 90)
    ]
    
    # Ensure longitude is between -180 and 180
    df_processed = df_processed[
        (df_processed['longitude'] >= -180) & 
        (df_processed['longitude'] <= 180)
    ]
    
    # 4. Normalize crime types (convert to lowercase, strip whitespace)
    df_processed['crime_type'] = df_processed['crime_type'].str.strip().str.title()
    
    print(f"✓ Preprocessing complete. {len(df_processed)} records remaining.")
    
    return df_processed

def prepare_features_for_prediction(hour, day, month, latitude, longitude):
    """
    Prepare input features for ML model prediction
    
    Args:
        hour: Hour of day (0-23)
        day: Day of week (0-6)
        month: Month (1-12)
        latitude: Geographic latitude
        longitude: Geographic longitude
    
    Returns:
        numpy array of features
    """
    features = np.array([[hour, day, month, latitude, longitude]])
    return features

def prepare_features_for_clustering(df):
    """
    Extract features for clustering (hotspot detection)
    
    Args:
        df: pandas DataFrame with crime data
    
    Returns:
        numpy array with latitude and longitude
    """
    features = df[['latitude', 'longitude']].values
    return features
