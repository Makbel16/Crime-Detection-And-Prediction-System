"""
Fix database by recreating it with proper schema
"""

import os
from app.database import engine, Base
from app.models.crime import Crime
from app.utils.generate_data import generate_sample_crime_data
import pandas as pd

print("=" * 70)
print("Fixing Database...")
print("=" * 70)

# Generate sample data
df = generate_sample_crime_data(num_records=500, output_file="temp_fix.csv")

# Prepare dataframe
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['hotspot_cluster'] = -1

# Add ID column
df['id'] = range(1, len(df) + 1)

# Drop and recreate table
print("\nRecreating database table with proper schema...")
df[['id', 'crime_type', 'latitude', 'longitude', 'date', 'hour', 'day', 'month', 'hotspot_cluster']].to_sql(
    'crimes', 
    engine, 
    if_exists='replace', 
    index=False
)

print(f"✓ Database recreated with {len(df)} records")

# Verify
df_verify = pd.read_sql("SELECT COUNT(*) as count FROM crimes", engine)
print(f"✓ Verified: {df_verify['count'][0]} records in database")

df_columns = pd.read_sql("SELECT * FROM crimes LIMIT 1", engine)
print(f"✓ Columns: {df_columns.columns.tolist()}")

# Clean up
if os.path.exists("temp_fix.csv"):
    os.remove("temp_fix.csv")

print("\n" + "=" * 70)
print("✓ Database fixed! Refresh your browser now.")
print("=" * 70)
