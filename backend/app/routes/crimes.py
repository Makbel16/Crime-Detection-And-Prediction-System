"""
Crime Data Routes
API endpoints for crime data management
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from datetime import datetime
import io

from app.database import get_db
from app.models.crime import Crime
from app.services.preprocessing import preprocess_crime_data

router = APIRouter(prefix="/crimes", tags=["Crimes"])

@router.get("/")
async def get_crimes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all crime records with pagination
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of crime records
    """
    try:
        crimes = db.query(Crime).offset(skip).limit(limit).all()
        total = db.query(Crime).count()
        
        return {
            "data": [
                {
                    "id": crime.id,
                    "crime_type": crime.crime_type,
                    "latitude": crime.latitude,
                    "longitude": crime.longitude,
                    "date": crime.date.isoformat() if crime.date else None,
                    "hour": crime.hour,
                    "day": crime.day,
                    "month": crime.month,
                    "hotspot_cluster": crime.hotspot_cluster
                }
                for crime in crimes
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crimes: {str(e)}")

@router.get("/stats")
async def get_crime_statistics(db: Session = Depends(get_db)):
    """
    Get crime statistics for dashboard
    
    Returns:
        Dictionary with various statistics
    """
    try:
        # Total crimes
        total_crimes = db.query(Crime).count()
        
        # Crimes by type
        crimes_by_type = {}
        for crime_type in db.query(Crime.crime_type).distinct():
            count = db.query(Crime).filter(Crime.crime_type == crime_type[0]).count()
            crimes_by_type[crime_type[0]] = count
        
        # Crimes by hour
        crimes_by_hour = {}
        for hour in range(24):
            count = db.query(Crime).filter(Crime.hour == hour).count()
            crimes_by_hour[str(hour)] = count
        
        # Crimes by day of week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        crimes_by_day = {}
        for i, day in enumerate(days):
            count = db.query(Crime).filter(Crime.day == i).count()
            crimes_by_day[day] = count
        
        # Crimes by month
        crimes_by_month = {}
        for month in range(1, 13):
            count = db.query(Crime).filter(Crime.month == month).count()
            crimes_by_month[str(month)] = count
        
        return {
            "total_crimes": total_crimes,
            "crimes_by_type": crimes_by_type,
            "crimes_by_hour": crimes_by_hour,
            "crimes_by_day": crimes_by_day,
            "crimes_by_month": crimes_by_month
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@router.post("/upload")
async def upload_crime_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload crime data from CSV file
    
    Args:
        file: CSV file with crime data
    
    Returns:
        Upload status and statistics
    """
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        required_columns = ['crime_type', 'latitude', 'longitude', 'date']
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required column: {col}"
                )
        
        # Preprocess data
        df_processed = preprocess_crime_data(df)
        
        # Clear existing data
        db.query(Crime).delete()
        db.commit()
        
        # Insert new data
        records_added = 0
        for _, row in df_processed.iterrows():
            crime = Crime(
                crime_type=row['crime_type'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                date=pd.to_datetime(row['date']),
                hour=int(row['hour']) if 'hour' in row else None,
                day=int(row['day']) if 'day' in row else None,
                month=int(row['month']) if 'month' in row else None,
                hotspot_cluster=-1
            )
            db.add(crime)
            records_added += 1
        
        db.commit()
        
        return {
            "message": f"Successfully uploaded {records_added} records",
            "records_added": records_added
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading data: {str(e)}")

@router.post("/generate-sample")
async def generate_sample_data(db: Session = Depends(get_db)):
    """
    Generate and load sample crime data for testing
    """
    try:
        from app.utils.generate_data import generate_sample_crime_data
        import os
        
        # Generate sample data
        df = generate_sample_crime_data(num_records=500, output_file="temp_sample.csv")
        
        # Use pandas to directly replace the table (more reliable than ORM for bulk insert)
        from app.database import engine
        
        # Prepare dataframe for database
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].dt.hour
        df['day'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['hotspot_cluster'] = -1
        
        # Add ID column
        df['id'] = range(1, len(df) + 1)
        
        # Rename crime_type column to match if needed
        if 'crime_type' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'crime_type' column")
        
        # Drop and recreate table with new data
        df[['id', 'crime_type', 'latitude', 'longitude', 'date', 'hour', 'day', 'month', 'hotspot_cluster']].to_sql(
            'crimes', 
            engine, 
            if_exists='replace', 
            index=False
        )
        
        # Clean up temp file
        if os.path.exists("temp_sample.csv"):
            os.remove("temp_sample.csv")
        
        return {
            "message": f"Generated {len(df)} sample records",
            "records_added": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Error generating data: {str(e)}")
