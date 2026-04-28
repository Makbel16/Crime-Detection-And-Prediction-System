"""
Model Training Utility
Trains and saves ML models on startup
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app.services.hotspot_detection import HotspotDetector
from app.services.prediction import CrimePredictor
from app.services.preprocessing import preprocess_crime_data
from dotenv import load_dotenv
import os

load_dotenv()

def train_all_models():
    """
    Train both hotspot detection and prediction models using database data
    """
    print("=" * 60)
    print("Starting model training...")
    print("=" * 60)
    
    # Get database URL
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crime_data.db")
    
    # Load data from database
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.read_sql("SELECT * FROM crimes", engine)
        
        if len(df) == 0:
            print("⚠ No data found in database. Please upload crime data first.")
            return False
        
        print(f"✓ Loaded {len(df)} records from database")
        
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False
    
    # Preprocess data
    df_processed = preprocess_crime_data(df)
    
    # Train Hotspot Detection Model
    try:
        print("\n" + "=" * 60)
        print("Training Hotspot Detection Model (K-Means)")
        print("=" * 60)
        
        detector = HotspotDetector(n_clusters=5, model_path="models/hotspot_model.pkl")
        
        # Extract coordinates for clustering
        coordinates = df_processed[['latitude', 'longitude']].values
        
        # Train and get cluster labels
        cluster_labels = detector.train(coordinates)
        
        # Update database with cluster labels
        df_processed['hotspot_cluster'] = cluster_labels
        df_processed.to_sql('crimes', engine, if_exists='replace', index=False)
        
        print(f"✓ Hotspot detection complete")
        
        # Print statistics
        stats = detector.get_hotspot_statistics(cluster_labels)
        print(f"\nHotspot Statistics:")
        for cluster_id, stat in stats.items():
            print(f"  Cluster {cluster_id}: {stat['count']} crimes ({stat['percentage']}%)")
        
    except Exception as e:
        print(f"✗ Error training hotspot model: {e}")
        return False
    
    # Train Crime Prediction Model
    try:
        print("\n" + "=" * 60)
        print("Training Crime Prediction Model (Random Forest)")
        print("=" * 60)
        
        predictor = CrimePredictor(
            model_path="models/crime_prediction_model.pkl",
            encoder_path="models/label_encoder.pkl"
        )
        
        # Prepare features and target
        X = df_processed[['hour', 'day', 'month', 'latitude', 'longitude']].values
        y = df_processed['crime_type'].values
        
        # Train model
        predictor.train(X, y)
        
        print(f"✓ Crime prediction training complete")
        
    except Exception as e:
        print(f"✗ Error training prediction model: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All models trained successfully!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    train_all_models()
