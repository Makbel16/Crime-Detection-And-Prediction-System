"""
Database Configuration
Sets up SQLAlchemy connection with SQLite database
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crime_data.db")

# Create SQLAlchemy engine
# Use a StaticPool for SQLite to avoid connection pool exhaustion in a multi-threaded FastAPI app
engine_args = {}
if "sqlite" in DATABASE_URL:
    engine_args["connect_args"] = {"check_same_thread": False}
    engine_args["poolclass"] = StaticPool
else:
    engine_args["pool_pre_ping"] = True

engine = create_engine(
    DATABASE_URL,
    **engine_args
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Database session dependency
    Yields a session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
