"""
Main FastAPI Application
Entry point for the Crime Hotspot Detection and Prediction System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routes
from app.routes import crimes, hotspots, predict

# Create FastAPI app instance
app = FastAPI(
    title="Crime Hotspot Detection and Prediction System",
    description="AI-powered crime analysis and prediction platform",
    version="1.0.0"
)

# Configure CORS - Allow frontend to access backend APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(crimes.router, prefix="/api", tags=["Crimes"])
app.include_router(hotspots.router, prefix="/api", tags=["Hotspots"])
app.include_router(predict.router, prefix="/api", tags=["Prediction"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Crime Hotspot Detection and Prediction System API",
        "status": "running",
        "docs": "/docs"  # Swagger UI documentation
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
