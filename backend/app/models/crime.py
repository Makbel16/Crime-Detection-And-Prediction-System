"""
Crime Database Model
Defines the structure for storing crime records
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class Crime(Base):
    """
    Crime model representing a crime record in the database
    
    Attributes:
        id: Unique identifier
        crime_type: Type of crime (theft, assault, burglary, etc.)
        latitude: Geographic latitude
        longitude: Geographic longitude
        date: Date and time when crime occurred
        hour: Hour extracted from date (0-23)
        day: Day of week (0=Monday, 6=Sunday)
        month: Month (1-12)
        hotspot_cluster: Cluster label from K-Means (hotspot detection)
    """
    __tablename__ = "crimes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crime_type = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    hour = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    hotspot_cluster = Column(Integer, nullable=True, default=-1)
    
    def __repr__(self):
        return f"<Crime(id={self.id}, type={self.crime_type}, location=({self.latitude}, {self.longitude}))>"
