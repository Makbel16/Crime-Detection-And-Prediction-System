"""
Crime Prediction Routes
API endpoints for crime risk prediction
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import numpy as np

from app.services.prediction import CrimePredictor
from app.services.preprocessing import prepare_features_for_prediction

router = APIRouter(prefix="/predict", tags=["Prediction"])

class PredictionInput(BaseModel):
    """Input model for prediction request"""
    hour: int
    day: int
    month: int
    latitude: float
    longitude: float

@router.post("/")
async def predict_crime(input_data: PredictionInput):
    """
    Predict crime risk level based on time and location
    
    Args:
        input_data: PredictionInput with hour, day, month, latitude, longitude
    
    Returns:
        Prediction results with risk level
    """
    try:
        # Validate inputs
        if not (0 <= input_data.hour <= 23):
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 23")
        
        if not (0 <= input_data.day <= 6):
            raise HTTPException(status_code=400, detail="Day must be between 0 and 6 (0=Monday)")
        
        if not (1 <= input_data.month <= 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        
        if not (-90 <= input_data.latitude <= 90):
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        
        if not (-180 <= input_data.longitude <= 180):
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        
        # Prepare features
        features = prepare_features_for_prediction(
            input_data.hour,
            input_data.day,
            input_data.month,
            input_data.latitude,
            input_data.longitude
        )
        
        # Make prediction
        predictor = CrimePredictor(
            model_path="models/crime_prediction_model.pkl",
            encoder_path="models/label_encoder.pkl"
        )
        
        try:
            result = predictor.predict(features)
        except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail="Prediction model not trained yet. Please upload data first."
            )
        
        # Format response
        response = {
            "input": {
                "hour": input_data.hour,
                "day": input_data.day,
                "month": input_data.month,
                "latitude": input_data.latitude,
                "longitude": input_data.longitude
            },
            "prediction": result,
            "risk_assessment": get_risk_assessment(result['risk_level'])
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/batch")
async def batch_predict(inputs: list[PredictionInput]):
    """
    Make batch predictions for multiple inputs
    
    Args:
        inputs: List of PredictionInput objects
    
    Returns:
        List of prediction results
    """
    try:
        predictor = CrimePredictor(
            model_path="models/crime_prediction_model.pkl",
            encoder_path="models/label_encoder.pkl"
        )
        
        results = []
        for input_data in inputs:
            # Prepare features
            features = prepare_features_for_prediction(
                input_data.hour,
                input_data.day,
                input_data.month,
                input_data.latitude,
                input_data.longitude
            )
            
            # Make prediction
            result = predictor.predict(features)
            
            results.append({
                "input": {
                    "hour": input_data.hour,
                    "day": input_data.day,
                    "month": input_data.month,
                    "latitude": input_data.latitude,
                    "longitude": input_data.longitude
                },
                "prediction": result
            })
        
        return {"predictions": results}
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Prediction model not trained yet."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@router.get("/feature-importance")
async def get_feature_importance():
    """
    Get feature importance scores from the trained model
    
    Returns:
        Dictionary with feature importance scores
    """
    try:
        predictor = CrimePredictor(
            model_path="models/crime_prediction_model.pkl",
            encoder_path="models/label_encoder.pkl"
        )
        
        importance = predictor.get_feature_importance()
        
        return {"feature_importance": importance}
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Model not trained yet."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def get_risk_assessment(risk_level: str) -> dict:
    """
    Get detailed risk assessment based on risk level
    
    Args:
        risk_level: 'Low', 'Medium', or 'High'
    
    Returns:
        Dictionary with risk assessment details
    """
    assessments = {
        'Low': {
            'color': 'green',
            'message': 'Low crime risk detected. Exercise normal precautions.',
            'recommendation': 'Stay aware of your surroundings.'
        },
        'Medium': {
            'color': 'orange',
            'message': 'Moderate crime risk detected. Exercise increased caution.',
            'recommendation': 'Avoid isolated areas, especially at night.'
        },
        'High': {
            'color': 'red',
            'message': 'High crime risk detected. Exercise maximum caution.',
            'recommendation': 'Consider alternative routes or times. Stay in well-lit areas.'
        }
    }
    
    return assessments.get(risk_level, assessments['Low'])
