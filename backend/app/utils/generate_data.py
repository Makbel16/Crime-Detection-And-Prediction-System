"""
Sample Crime Data Generator
Generates realistic synthetic crime data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_crime_data(num_records=500, output_file="sample_crime_data.csv"):
    """
    Generate synthetic crime dataset with realistic patterns
    
    Args:
        num_records: Number of crime records to generate (default: 500)
        output_file: Output CSV file path
    
    Returns:
        pandas.DataFrame with generated crime data
    """
    print(f"Generating {num_records} crime records...")
    
    np.random.seed(42)  # For reproducibility
    
    # Define crime types with realistic distribution
    crime_types = ['Theft', 'Assault', 'Burglary', 'Vandalism', 'Robbery', 'Fraud']
    crime_weights = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]  # Probabilities
    
    # Generate crime types
    crimes = np.random.choice(crime_types, size=num_records, p=crime_weights)
    
    # Generate locations (centered around a city - using San Francisco as example)
    # San Francisco coordinates: ~37.7749° N, 122.4194° W
    base_lat = 37.7749
    base_lon = -122.4194
    
    # Create clusters around different neighborhoods
    num_clusters = 8
    cluster_centers_lat = np.random.uniform(base_lat - 0.05, base_lat + 0.05, num_clusters)
    cluster_centers_lon = np.random.uniform(base_lon - 0.05, base_lon + 0.05, num_clusters)
    
    latitudes = []
    longitudes = []
    
    for _ in range(num_records):
        # Pick a random cluster center
        cluster_idx = np.random.randint(0, num_clusters)
        
        # Add random offset from cluster center (creates realistic hotspots)
        lat = cluster_centers_lat[cluster_idx] + np.random.normal(0, 0.01)
        lon = cluster_centers_lon[cluster_idx] + np.random.normal(0, 0.01)
        
        latitudes.append(round(lat, 6))
        longitudes.append(round(lon, 6))
    
    # Generate dates over the past year
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 4, 28)
    date_range = (end_date - start_date).days
    
    dates = []
    for _ in range(num_records):
        # Random date within range
        random_days = np.random.randint(0, date_range)
        random_hours = np.random.randint(0, 24)
        random_minutes = np.random.randint(0, 60)
        
        crime_date = start_date + timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes
        )
        dates.append(crime_date)
    
    # Create DataFrame
    df = pd.DataFrame({
        'crime_type': crimes,
        'latitude': latitudes,
        'longitude': longitudes,
        'date': dates
    })
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Add ID column
    df.insert(0, 'id', range(1, len(df) + 1))
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✓ Data saved to {output_file}")
    print(f"✓ Generated {len(df)} records")
    print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"✓ Crime types: {df['crime_type'].value_counts().to_dict()}")
    
    return df

if __name__ == "__main__":
    # Generate data when script is run directly
    generate_sample_crime_data(num_records=500, output_file="sample_crime_data.csv")
