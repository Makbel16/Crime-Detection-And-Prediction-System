"""
Quick script to view database contents
"""

import pandas as pd
from sqlalchemy import create_engine

# Connect to database
DATABASE_URL = "sqlite:///./crime_data.db"
engine = create_engine(DATABASE_URL)

# Read data
df = pd.read_sql("SELECT * FROM crimes LIMIT 10", engine)

print("=" * 70)
print("DATABASE CONTENTS (First 10 Records)")
print("=" * 70)
print(df.to_string())
print("\n" + "=" * 70)

# Get total count
total = pd.read_sql("SELECT COUNT(*) as total FROM crimes", engine)
print(f"Total records in database: {total['total'][0]}")
print("=" * 70)

# Show table info
print("\nTABLE STRUCTURE:")
print("=" * 70)
info = pd.read_sql("PRAGMA table_info(crimes)", engine)
print(info.to_string())
