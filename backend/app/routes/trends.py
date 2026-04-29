"""
Time-Series Analysis Routes
API endpoints for trend analysis and predictions
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.time_series import TimeSeriesAnalyzer

router = APIRouter(prefix="/trends", tags=["Trends"])

@router.get("/monthly")
async def get_monthly_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get monthly crime trends

    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter

    Returns:
        Monthly trend data
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)
        result = analyzer.get_monthly_trends(start_date, end_date)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly trends: {str(e)}")

@router.get("/yearly")
async def get_yearly_trends(
    start_year: Optional[int] = Query(None, description="Start year"),
    end_year: Optional[int] = Query(None, description="End year"),
    db: Session = Depends(get_db)
):
    """
    Get yearly crime trends

    Args:
        start_year: Optional start year filter
        end_year: Optional end year filter

    Returns:
        Yearly trend data
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)
        result = analyzer.get_yearly_trends(start_year, end_year)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching yearly trends: {str(e)}")

@router.get("/seasonal")
async def get_seasonal_analysis(db: Session = Depends(get_db)):
    """
    Get seasonal analysis of crime patterns

    Returns:
        Seasonal decomposition data
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)
        result = analyzer.get_seasonal_analysis()

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing seasonal analysis: {str(e)}")

@router.get("/predict")
async def predict_future_patterns(
    months_ahead: int = Query(12, description="Number of months to predict", ge=1, le=60),
    db: Session = Depends(get_db)
):
    """
    Predict future crime patterns

    Args:
        months_ahead: Number of months to predict (1-60)

    Returns:
        Future crime predictions
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)
        result = analyzer.predict_future_patterns(months_ahead)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting future patterns: {str(e)}")

@router.get("/crime-types")
async def get_crime_type_trends(
    crime_type: Optional[str] = Query(None, description="Specific crime type to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get trends for specific crime types

    Args:
        crime_type: Optional crime type filter

    Returns:
        Crime type specific trends
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)
        result = analyzer.get_crime_type_trends(crime_type)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crime type trends: {str(e)}")

@router.get("/summary")
async def get_trends_summary(db: Session = Depends(get_db)):
    """
    Get comprehensive trends summary

    Returns:
        Summary of all trend analyses
    """
    try:
        analyzer = TimeSeriesAnalyzer(db)

        monthly = analyzer.get_monthly_trends()
        yearly = analyzer.get_yearly_trends()
        seasonal = analyzer.get_seasonal_analysis()
        predictions = analyzer.predict_future_patterns(12)

        summary = {
            "monthly_summary": {
                "total_crimes": monthly.get("total_crimes", 0),
                "periods": monthly.get("periods", 0),
                "latest_trend": monthly.get("monthly_trends", [])[-1] if monthly.get("monthly_trends") else None
            },
            "yearly_summary": {
                "total_crimes": yearly.get("total_crimes", 0),
                "years": yearly.get("years", 0),
                "latest_year": yearly.get("yearly_trends", [])[-1] if yearly.get("yearly_trends") else None
            },
            "seasonal_available": "seasonal_analysis" in seasonal,
            "predictions_available": "future_predictions" in predictions,
            "last_updated": "2024-01-01"  # Could be dynamic based on data
        }

        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating trends summary: {str(e)}")