# Crime Hotspot Detection and Prediction System

A complete web-based system that analyzes crime data, detects hotspots using machine learning clustering, and predicts crime risk levels.

## 🎯 Features

- **Crime Data Management**: Upload CSV datasets or generate sample data
- **Data Preprocessing**: Automatic feature extraction and cleaning
- **Hotspot Detection**: K-Means clustering to identify crime hotspots
- **Crime Prediction**: Random Forest model to predict crime risk levels
- **Interactive Dashboard**: Charts and statistics
- **Map Visualization**: Leaflet.js interactive map with cluster markers
- **Modern UI**: Clean, responsive design with Tailwind CSS

## 🏗 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite
- **ML Libraries**: Scikit-learn, Pandas, NumPy
- **Model Persistence**: Joblib

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Maps**: Leaflet.js + React-Leaflet
- **Charts**: Chart.js + React-Chartjs-2
- **API Client**: Axios
- **Routing**: React Router v6
- **Icons**: Lucide React

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## 🚀 Installation & Setup

### Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup script (creates database, generates data, trains models)
python setup.py
```

### Step 2: Start Backend Server

```bash
# In the backend directory
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at: `http://localhost:8000`
API Documentation (Swagger): `http://localhost:8000/docs`

### Step 3: Setup Frontend

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Step 4: Start Frontend Server

```bash
# In the frontend directory
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 📁 Project Structure

```
Crime Hotspot Detection and Prediction System/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── database.py          # Database configuration
│   │   ├── models/
│   │   │   └── crime.py         # Crime data model
│   │   ├── routes/
│   │   │   ├── crimes.py        # Crime data endpoints
│   │   │   ├── hotspots.py      # Hotspot detection endpoints
│   │   │   └── predict.py       # Prediction endpoints
│   │   ├── services/
│   │   │   ├── preprocessing.py # Data preprocessing
│   │   │   ├── hotspot_detection.py  # K-Means clustering
│   │   │   └── prediction.py    # Random Forest prediction
│   │   └── utils/
│   │       ├── generate_data.py # Sample data generator
│   │       └── model_trainer.py # Model training utility
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── setup.py                 # Setup script
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx      # Navigation sidebar
│   │   │   └── Loading.jsx      # Loading component
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx    # Dashboard with charts
│   │   │   ├── MapView.jsx      # Interactive map view
│   │   │   ├── Prediction.jsx   # Crime prediction form
│   │   │   └── DataView.jsx     # Data table view
│   │   ├── services/
│   │   │   └── api.js           # API integration
│   │   ├── App.jsx              # Main app component
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

## 🔌 API Endpoints

### Crimes
- `GET /api/crimes/` - Get all crimes (with pagination)
- `GET /api/crimes/stats` - Get crime statistics
- `POST /api/crimes/upload` - Upload CSV file
- `POST /api/crimes/generate-sample` - Generate sample data

### Hotspots
- `GET /api/hotspots/` - Get hotspots with clusters
- `GET /api/hotspots/centers` - Get cluster centers
- `POST /api/hotspots/retrain` - Retrain hotspot model

### Prediction
- `POST /api/predict/` - Predict crime risk
- `POST /api/predict/batch` - Batch predictions
- `GET /api/predict/feature-importance` - Get feature importance

## 🧠 Machine Learning Models

### Hotspot Detection (K-Means)
- **Algorithm**: K-Means Clustering
- **Features**: Latitude, Longitude
- **Output**: Cluster labels (hotspot assignments)
- **Model File**: `backend/models/hotspot_model.pkl`

### Crime Prediction (Random Forest)
- **Algorithm**: Random Forest Classifier
- **Features**: Hour, Day, Month, Latitude, Longitude
- **Output**: Crime type prediction with confidence scores
- **Risk Levels**: Low, Medium, High
- **Model Files**: 
  - `backend/models/crime_prediction_model.pkl`
  - `backend/models/label_encoder.pkl`

## 📊 Sample Dataset

The system includes a sample data generator that creates 500+ realistic crime records with:
- Crime types: Theft, Assault, Burglary, Vandalism, Robbery, Fraud
- Locations: San Francisco area (customizable)
- Time range: Past year
- Geographic clustering for realistic hotspots

## 🎨 UI Pages

1. **Dashboard**: Overview with statistics and charts
   - Total crimes count
   - Crimes by type (pie chart)
   - Crimes by hour (bar chart)
   - Crimes by day of week
   - Key metrics cards

2. **Map View**: Interactive crime hotspot map
   - Leaflet.js map with OpenStreetMap
   - Crime markers with popups
   - Cluster center circles
   - Filter by cluster
   - Real-time statistics

3. **Prediction**: Crime risk prediction form
   - Input: Time and location parameters
   - Output: Risk level (Low/Medium/High)
   - Top 3 crime predictions
   - Confidence scores
   - Safety recommendations

4. **Data Table**: Browse crime records
   - Paginated table view
   - Upload CSV files
   - Generate sample data
   - Sort and filter

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=sqlite:///./crime_data.db
MODEL_DIR=./models
UPLOAD_DIR=./uploads
```

### Frontend (vite.config.js)
```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port with `uvicorn app.main:app --reload --port 8001`
- **Module not found**: Ensure you're in the backend directory and virtual environment is activated
- **Database errors**: Delete `crime_data.db` and run `python setup.py` again

### Frontend Issues
- **Cannot connect to API**: Ensure backend is running on port 8000
- **Map not showing**: Check internet connection (Leaflet loads tiles from CDN)
- **Dependencies error**: Delete `node_modules` and run `npm install` again

## 📝 Usage Guide

1. **Start both servers** (backend and frontend)
2. **Generate sample data** from the Data Table page (or it auto-generates on setup)
3. **View dashboard** to see crime statistics
4. **Explore map** to see hotspot clusters
5. **Make predictions** using the Prediction page
6. **Upload your own data** using CSV format with columns: crime_type, latitude, longitude, date

## 🎯 Future Enhancements

- [ ] User authentication and authorization
- [ ] Real-time crime alerts
- [ ] Advanced filtering and search
- [ ] Export reports (PDF, Excel)
- [ ] Time-series forecasting
- [ ] DBSCAN clustering option
- [ ] Mobile responsive improvements
- [ ] PostgreSQL support

## 📄 License

This project is built for educational and demonstration purposes.

## 👨‍💻 Developer

Built with ❤️ using FastAPI, React, and Machine Learning

---

**Note**: This system uses synthetic sample data for demonstration. For production use, replace with real crime data from official sources.
