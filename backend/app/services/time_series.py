"""
Time-Series Analysis Service
Provides trend analysis, seasonal patterns, and future predictions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.crime import Crime
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesAnalyzer:
    """
    Time-series analysis for crime data trends and predictions
    """

    def __init__(self, db: Session):
        self.db: Session = db

    def get_monthly_trends(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Get monthly crime trends

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Monthly trend data
        """
        query = self.db.query(
            Crime.date,
            Crime.crime_type,
            Crime.latitude,
            Crime.longitude
        )

        if start_date:
            query = query.filter(Crime.date >= start_date)
        if end_date:
            query = query.filter(Crime.date <= end_date)

        crimes = query.all()

        if not crimes:
            return {"error": "No crime data found"}

        # Convert to DataFrame
        df = pd.DataFrame([{
            'date': crime.date,
            'crime_type': crime.crime_type,
            'latitude': crime.latitude,
            'longitude': crime.longitude
        } for crime in crimes])

        # Group by month
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        monthly_data = df.groupby('month').size().reset_index(name='count')

        # Convert period to string for JSON serialization
        monthly_data['month'] = monthly_data['month'].astype(str)

        # Calculate trends
        monthly_data['trend'] = monthly_data['count'].pct_change() * 100
        
        # Handle NaN values for JSON serialization
        monthly_data['trend'] = monthly_data['trend'].fillna(0.0)

        return {
            "monthly_trends": monthly_data.to_dict('records'),
            "total_crimes": len(crimes),
            "periods": len(monthly_data)
        }

    def get_yearly_trends(self, start_year: int = None, end_year: int = None) -> Dict[str, Any]:
        """
        Get yearly crime trends

        Args:
            start_year: Start year
            end_year: End year

        Returns:
            Yearly trend data
        """
        query = self.db.query(Crime.date, Crime.crime_type)

        if start_year:
            start_date = f"{start_year}-01-01"
            query = query.filter(Crime.date >= start_date)
        if end_year:
            end_date = f"{end_year}-12-31"
            query = query.filter(Crime.date <= end_date)

        crimes = query.all()

        if not crimes:
            return {"error": "No crime data found"}

        df = pd.DataFrame([{
            'date': crime.date,
            'crime_type': crime.crime_type
        } for crime in crimes])

        # Group by year
        df['year'] = pd.to_datetime(df['date']).dt.year
        yearly_data = df.groupby('year').size().reset_index(name='count')

        # Calculate year-over-year growth
        yearly_data['yoy_growth'] = yearly_data['count'].pct_change() * 100
        
        # Handle NaN values for JSON serialization
        yearly_data['yoy_growth'] = yearly_data['yoy_growth'].fillna(0.0)

        return {
            "yearly_trends": yearly_data.to_dict('records'),
            "total_crimes": len(crimes),
            "years": len(yearly_data)
        }

    def get_seasonal_analysis(self) -> Dict[str, Any]:
        """
        Perform seasonal analysis of crime data

        Returns:
            Seasonal decomposition results
        """
        query = self.db.query(Crime.date)
        crimes = query.all()

        if len(crimes) < 24:  # Need at least 2 years of data
            return {"error": "Insufficient data for seasonal analysis (need at least 24 months)"}

        # Create time series
        dates = [crime.date for crime in crimes]
        df = pd.DataFrame({'date': dates})
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.resample('M').size().asfreq('M', fill_value=0)

        if len(df) < 24:
            return {"error": "Insufficient data for seasonal analysis (need at least 24 monthly periods)"}

        # Seasonal decomposition
        try:
            decomposition = seasonal_decompose(df, model='additive', period=12)

            seasonal_data = {
                "observed": [float(x) if not np.isnan(x) else 0.0 for x in decomposition.observed.tolist()],
                "trend": [float(x) if not np.isnan(x) else 0.0 for x in decomposition.trend.tolist()],
                "seasonal": [float(x) if not np.isnan(x) else 0.0 for x in decomposition.seasonal.tolist()],
                "residual": [float(x) if not np.isnan(x) else 0.0 for x in decomposition.resid.tolist()],
                "dates": [d.strftime('%Y-%m') for d in decomposition.observed.index]
            }

            return {
                "seasonal_analysis": seasonal_data,
                "total_periods": len(df),
                "seasonal_strength": self._calculate_seasonal_strength(decomposition)
            }
        except Exception as e:
            return {"error": f"Seasonal analysis failed: {str(e)}"}

    def predict_future_patterns(self, months_ahead: int = 12) -> Dict[str, Any]:
        """
        Predict future crime patterns using ARIMA

        Args:
            months_ahead: Number of months to predict

        Returns:
            Future predictions
        """
        query = self.db.query(Crime.date)
        crimes = query.all()

        if len(crimes) < 24:  # Need at least 2 years
            return {"error": "Insufficient data for prediction (need at least 24 months)"}

        # Create time series
        dates = [crime.date for crime in crimes]
        df = pd.DataFrame({'date': dates})
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        monthly_crimes = df.resample('M').size().asfreq('M', fill_value=0)

        if len(monthly_crimes) < 24:
            return {"error": "Insufficient data for prediction (need at least 24 monthly periods)"}

        try:
            # Fit ARIMA model
            model = ARIMA(monthly_crimes, order=(1, 1, 1))
            model_fit = model.fit()

            # Make predictions
            forecast = model_fit.forecast(steps=months_ahead)

            # Generate future dates
            last_date = monthly_crimes.index[-1]
            future_dates = pd.date_range(
                start=last_date + pd.offsets.MonthBegin(1),
                periods=months_ahead,
                freq='M'
            )

            predictions = {
                "dates": [d.strftime('%Y-%m') for d in future_dates],
                "predicted_crimes": [float(x) if not np.isnan(x) else 0.0 for x in forecast.tolist()],
                "confidence_intervals": {
                    "lower": [float(x) if not np.isnan(x) else 0.0 for x in (forecast - 1.96 * np.sqrt(model_fit.mse)).tolist()],
                    "upper": [float(x) if not np.isnan(x) else 0.0 for x in (forecast + 1.96 * np.sqrt(model_fit.mse)).tolist()]
                }
            }

            return {
                "future_predictions": predictions,
                "model_summary": str(model_fit.summary()),
                "aic": float(model_fit.aic),
                "bic": float(model_fit.bic)
            }
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}

    def get_crime_type_trends(self, crime_type: str = None) -> Dict[str, Any]:
        """
        Get trends for specific crime types

        Args:
            crime_type: Specific crime type to analyze

        Returns:
            Crime type specific trends
        """
        query = self.db.query(Crime.date, Crime.crime_type)

        if crime_type:
            query = query.filter(Crime.crime_type == crime_type)

        crimes = query.all()

        if not crimes:
            return {"error": "No data found for the specified crime type"}

        df = pd.DataFrame([{
            'date': crime.date,
            'crime_type': crime.crime_type
        } for crime in crimes])

        # Group by month and crime type
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        trends = df.groupby(['month', 'crime_type']).size().reset_index(name='count')

        # Convert period to string
        trends['month'] = trends['month'].astype(str)

        # Pivot for better visualization
        pivot_trends = trends.pivot(index='month', columns='crime_type', values='count').fillna(0)

        return {
            "crime_type_trends": trends.to_dict('records'),
            "pivot_data": pivot_trends.to_dict('index'),
            "crime_types": pivot_trends.columns.tolist(),
            "total_crimes": len(crimes)
        }

    def _calculate_seasonal_strength(self, decomposition) -> float:
        """
        Calculate seasonal strength metric

        Args:
            decomposition: Seasonal decomposition result

        Returns:
            Seasonal strength (0-1)
        """
        try:
            seasonal_var = np.var(decomposition.seasonal.dropna())
            residual_var = np.var(decomposition.resid.dropna())
            return seasonal_var / (seasonal_var + residual_var)
        except:
            return 0.0