"""
Backend Startup Script
Initializes database, generates sample data if needed, and trains models
"""

import os
import sys
from app.database import engine, Base
from app.models.crime import Crime

def setup_backend():
    """Setup backend: create database, generate data, train models"""
    
    print("=" * 70)
    print("Crime Hotspot Detection System - Backend Setup")
    print("=" * 70)
    
    # Step 1: Create database tables
    print("\n[1/3] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Step 2: Generate sample data
    print("\n[2/3] Checking for data...")
    from sqlalchemy import create_engine
    import pandas as pd
    
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crime_data.db")
    db_engine = create_engine(DATABASE_URL)
    
    try:
        df = pd.read_sql("SELECT * FROM crimes", db_engine)
        if len(df) > 0:
            print(f"✓ Found {len(df)} existing records in database")
        else:
            print("No data found. Generating sample data...")
            from app.utils.generate_data import generate_sample_crime_data
            df = generate_sample_crime_data(num_records=500, output_file="temp_sample.csv")
            
            # Load into database
            df.to_sql('crimes', db_engine, if_exists='replace', index=False)
            print(f"✓ Loaded {len(df)} records into database")
            
            # Clean up
            if os.path.exists("temp_sample.csv"):
                os.remove("temp_sample.csv")
    except:
        print("Generating sample data...")
        from app.utils.generate_data import generate_sample_crime_data
        df = generate_sample_crime_data(num_records=500, output_file="temp_sample.csv")
        
        # Load into database
        df.to_sql('crimes', db_engine, if_exists='replace', index=False)
        print(f"✓ Loaded {len(df)} records into database")
        
        # Clean up
        if os.path.exists("temp_sample.csv"):
            os.remove("temp_sample.csv")
    
    # Step 3: Train models
    print("\n[3/3] Training ML models...")
    from app.utils.model_trainer import train_all_models
    success = train_all_models()
    
    if success:
        print("\n" + "=" * 70)
        print("✓ Backend setup complete! You can now start the server.")
        print("=" * 70)
    else:
        print("\n✗ Setup incomplete. Check errors above.")

if __name__ == "__main__":
    setup_backend()
