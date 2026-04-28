"""
Hotspot Detection Routes
API endpoints for crime hotspot analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from app.database import get_db
from app.models.crime import Crime
from app.services.hotspot_detection import HotspotDetector
from app.services.preprocessing import preprocess_crime_data

router = APIRouter(prefix="/hotspots", tags=["Hotspots"])

@router.get("/")
async def get_hotspots(db: Session = Depends(get_db)):
    """
    Get crime hotspots with cluster information
    
    Returns:
        List of crimes with their hotspot cluster assignments
    """
    try:
        # Load data from database
        df = pd.read_sql("SELECT * FROM crimes", db.bind)
        
        if len(df) == 0:
            return {
                "hotspots": [],
                "cluster_centers": [],
                "statistics": {}
            }
        
        # Preprocess data
        df_processed = preprocess_crime_data(df)
        
        # Load or train hotspot detector
        detector = HotspotDetector(n_clusters=5, model_path="models/hotspot_model.pkl")
        
        try:
            # Try to load existing model
            detector.load_model()
            
            # Predict clusters for all data
            coordinates = df_processed[['latitude', 'longitude']].values
            cluster_labels = detector.predict(coordinates)
            
        except FileNotFoundError:
            # Train new model if not exists
            coordinates = df_processed[['latitude', 'longitude']].values
            cluster_labels = detector.train(coordinates)
            
            # Update database with cluster labels
            df_processed['hotspot_cluster'] = cluster_labels
            df_processed.to_sql('crimes', db.bind, if_exists='replace', index=False)
        
        # Get cluster centers
        cluster_centers = detector.get_cluster_centers()
        
        # Prepare hotspot data
        hotspots = []
        for idx, row in df_processed.iterrows():
            hotspots.append({
                "id": int(row['id']),
                "crime_type": row['crime_type'],
                "latitude": float(row['latitude']),
                "longitude": float(row['longitude']),
                "cluster": int(cluster_labels[idx])
            })
        
        # Get statistics
        statistics = detector.get_hotspot_statistics(cluster_labels)
        
        # Format cluster centers
        centers_list = []
        for i, center in enumerate(cluster_centers):
            centers_list.append({
                "cluster_id": i,
                "latitude": float(center[0]),
                "longitude": float(center[1]),
                "crime_count": statistics.get(i, {}).get('count', 0)
            })
        
        return {
            "hotspots": hotspots,
            "cluster_centers": centers_list,
            "statistics": statistics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting hotspots: {str(e)}")

@router.get("/centers")
async def get_hotspot_centers(db: Session = Depends(get_db)):
    """
    Get only hotspot cluster centers
    
    Returns:
        List of cluster center coordinates
    """
    try:
        # Load detector
        detector = HotspotDetector(n_clusters=5, model_path="models/hotspot_model.pkl")
        
        try:
            detector.load_model()
            centers = detector.get_cluster_centers()
            
            centers_list = []
            for i, center in enumerate(centers):
                centers_list.append({
                    "cluster_id": i,
                    "latitude": float(center[0]),
                    "longitude": float(center[1])
                })
            
            return {"cluster_centers": centers_list}
            
        except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail="Hotspot model not trained yet. Call /hotspots/ first."
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/retrain")
async def retrain_hotspot_model(n_clusters: int = 5, db: Session = Depends(get_db)):
    """
    Retrain hotspot detection model
    
    Args:
        n_clusters: Number of clusters to detect
    
    Returns:
        Training results
    """
    try:
        # Load data from database
        df = pd.read_sql("SELECT * FROM crimes", db.bind)
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="No data available for training")
        
        # Preprocess
        df_processed = preprocess_crime_data(df)
        
        # Train model
        detector = HotspotDetector(
            n_clusters=n_clusters,
            model_path="models/hotspot_model.pkl"
        )
        
        coordinates = df_processed[['latitude', 'longitude']].values
        cluster_labels = detector.train(coordinates)
        
        # Update database
        df_processed['hotspot_cluster'] = cluster_labels
        df_processed.to_sql('crimes', db.bind, if_exists='replace', index=False)
        
        # Get statistics
        statistics = detector.get_hotspot_statistics(cluster_labels)
        
        return {
            "message": "Hotspot model retrained successfully",
            "n_clusters": n_clusters,
            "statistics": statistics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retraining model: {str(e)}")
