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

# Install dependencies (use 'py' on Windows)
py -m pip install -r requirements.txt

# Run setup script (creates database, generates data, trains models)
py setup.py
```

**⚠️ Important for VS Code Users:**
- Use `py` command instead of `python` on Windows
- If you get "ModuleNotFoundError", select the correct Python interpreter:
  1. Press `Ctrl + Shift + P`
  2. Type "Python: Select Interpreter"
  3. Choose Python 3.14 (not a venv from another project)

### Step 2: Start Backend Server

```bash
# In the backend directory
py -m uvicorn app.main:app --reload --port 8000
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

---

## 💻 Running in VS Code (Quick Start)

### Option 1: Using the Startup Script (Easiest)
Just double-click `start.bat` in File Explorer!

### Option 2: Manual Start in VS Code

**Terminal 1 (Backend):**
```bash
cd backend
py -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open: http://localhost:5173

## 📁 Project Structure

```
Crime Hotspot Detection and Prediction System/
├── 📄 README.md                           # Main documentation
├── 📄 QUICKSTART.md                       # Quick start guide
├── 📄 PROJECT_STRUCTURE.md               # Detailed file structure
├── 🚀 start.bat                          # Windows startup script
│
├── 📂 backend/                           # Python FastAPI Backend
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 .env                          # Environment variables
│   ├── 📄 setup.py                      # Setup & initialization script
│   ├── 📄 crime_data.db                 # SQLite database (auto-created)
│   ├── 📄 fix_database.py               # Database fix utility
│   │
│   ├── 📂 app/
│   │   ├── 📄 main.py                   # FastAPI entry point
│   │   ├── 📄 database.py               # Database configuration
│   │   ├── 📂 models/
│   │   │   └── 📄 crime.py              # Crime data model
│   │   ├── 📂 routes/
│   │   │   ├── 📄 crimes.py             # Crime data endpoints
│   │   │   ├── 📄 hotspots.py           # Hotspot detection endpoints
│   │   │   └── 📄 predict.py            # Prediction endpoints
│   │   ├── 📂 services/
│   │   │   ├── 📄 preprocessing.py      # Data preprocessing
│   │   │   ├── 📄 hotspot_detection.py  # K-Means clustering
│   │   │   └── 📄 prediction.py         # Random Forest prediction
│   │   └── 📂 utils/
│   │       ├── 📄 generate_data.py      # Sample data generator
│   │       └── 📄 model_trainer.py      # Model training utility
│   │
│   └── 📂 models/                        # Trained ML models (auto-created)
│       ├── 📄 hotspot_model.pkl          # K-Means model
│       ├── 📄 crime_prediction_model.pkl # Random Forest model
│       └── 📄 label_encoder.pkl          # Label encoder
│
└── 📂 frontend/                          # React Frontend
    ├── 📄 package.json                   # Node dependencies
    ├── 📄 vite.config.js                 # Vite configuration
    ├── 📄 tailwind.config.js             # Tailwind CSS config
    ├── 📄 postcss.config.js              # PostCSS config
    ├── 📄 index.html                     # HTML entry point
    │
    └── 📂 src/
        ├── 📄 main.jsx                   # React entry point
        ├── 📄 App.jsx                    # Main app with routing
        ├── 📄 index.css                  # Global styles
        ├── 📂 components/
        │   ├── 📄 Sidebar.jsx            # Navigation sidebar
        │   └── 📄 Loading.jsx            # Loading spinner
        ├── 📂 pages/
        │   ├── 📄 Dashboard.jsx          # Dashboard with charts
        │   ├── 📄 MapView.jsx            # Interactive map view
        │   ├── 📄 Prediction.jsx         # Crime prediction form
        │   └── 📄 DataView.jsx           # Data table view
        ├── 📂 services/
        │   └── 📄 api.js                 # API integration
        └── 📂 hooks/                     # Custom hooks (extensible)
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

**ModuleNotFoundError: No module named 'pandas' (or other packages)**
- This happens when VS Code uses the wrong Python interpreter
- **Fix**: Select the correct Python interpreter:
  1. Press `Ctrl + Shift + P`
  2. Type "Python: Select Interpreter"
  3. Choose Python 3.14 (the one at `C:\Users\ybeka\AppData\Local\Programs\Python\Python314`)
  4. **Do NOT** select a venv from another project
- **Alternative**: Run `py -m pip install -r requirements.txt` in the backend directory

**Port already in use**
- Change port with: `py -m uvicorn app.main:app --reload --port 8001`

**Database errors or empty data**
- Run the fix script: `py fix_database.py`
- Or recreate database: Delete `crime_data.db` and run `py setup.py`

**Generate Sample Data button fails**
- This was fixed! The database now includes the `id` column
- If it happens again, run: `py fix_database.py`

### Frontend Issues
- **Cannot connect to API**: Ensure backend is running on port 8000
- **Map not showing**: Check internet connection (Leaflet loads tiles from CDN)
- **Dependencies error**: Delete `node_modules` folder and run `npm install` again
- **Blank page**: Check browser console (F12) for errors

### Database Issues

**Database is empty or missing columns**
```bash
cd backend
py fix_database.py
```

**View database contents**
```bash
cd backend
py view_database.py
```

## 📝 Usage Guide

1. **Start both servers** (backend and frontend)
   - Use `start.bat` for automatic startup, OR
   - Manually start both terminals as shown above
2. **Generate sample data** from the Data Table page (or it auto-generates on setup)
3. **View dashboard** to see crime statistics
4. **Explore map** to see hotspot clusters
5. **Make predictions** using the Prediction page
6. **Upload your own data** using CSV format with columns: crime_type, latitude, longitude, date

## 📊 Database Information

**Location**: `backend/crime_data.db`

**Contents**:
- 500 sample crime records (after running setup.py)
- Columns: id, crime_type, latitude, longitude, date, hour, day, month, hotspot_cluster

**View Database**:
```bash
cd backend
py view_database.py
```

**Fix Database** (if corrupted):
```bash
cd backend
py fix_database.py
```

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

## 🛠️ Helper Scripts

The project includes several helpful scripts:

| Script | Purpose | Usage |
|--------|---------|-------|
| `start.bat` | Start both servers automatically | Double-click in File Explorer |
| `setup.py` | Initialize database and train models | `py setup.py` |
| `fix_database.py` | Fix database schema issues | `py fix_database.py` |
| `view_database.py` | View database contents | `py view_database.py` |

---

**Note**: This system uses synthetic sample data for demonstration. For production use, replace with real crime data from official sources.
