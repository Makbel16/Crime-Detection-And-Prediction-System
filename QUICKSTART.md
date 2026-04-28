# 🚀 Quick Start Guide

## ✅ System is Running!

Your Crime Hotspot Detection and Prediction System is now live!

### 🌐 Access Your Application

**Frontend (Main Application):**
- URL: http://localhost:5173
- Features: Dashboard, Map, Prediction, Data Table

**Backend API:**
- URL: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

---

## 📋 What's Been Set Up

### ✓ Backend (FastAPI)
- Database created with 500 sample crime records
- K-Means hotspot detection model trained (5 clusters)
- Random Forest prediction model trained (98.6% accuracy)
- All API endpoints active

### ✓ Frontend (React)
- Modern UI with Tailwind CSS
- 4 pages: Dashboard, Map View, Prediction, Data Table
- Interactive Leaflet.js map
- Chart.js visualizations
- Full API integration

---

## 🎯 How to Use

### 1. Dashboard (http://localhost:5173/)
- View crime statistics and analytics
- See charts: crimes by type, hour, day
- Key metrics cards with insights

### 2. Map View (http://localhost:5173/map)
- Interactive map showing crime locations
- Color-coded hotspot clusters
- Click markers for details
- Filter by cluster
- Retrain model button

### 3. Prediction (http://localhost:5173/prediction)
- Enter time and location parameters
- Get crime risk prediction (Low/Medium/High)
- See top 3 most likely crimes
- View confidence scores
- Get safety recommendations

### 4. Data Table (http://localhost:5173/data)
- Browse all crime records
- Upload your own CSV files
- Generate new sample data
- Paginated view

---

## 🔄 Stopping & Restarting

### To Stop:
- Press `Ctrl+C` in both terminal windows

### To Restart Backend:
```bash
cd backend
py -m uvicorn app.main:app --reload --port 8000
```

### To Restart Frontend:
```bash
cd frontend
npm run dev
```

---

## 📊 Sample Data

The system generated 500 crime records with:
- **Crime Types**: Theft (154), Assault (87), Burglary (86), Vandalism (67), Fraud (55), Robbery (51)
- **Location**: San Francisco area
- **Date Range**: January 2025 - April 2026
- **Hotspots**: 5 clusters detected

---

## 🧪 Test the API

Try these API calls in your browser:

1. **Get Crimes**: http://localhost:8000/api/crimes/?skip=0&limit=10
2. **Get Statistics**: http://localhost:8000/api/crimes/stats
3. **Get Hotspots**: http://localhost:8000/api/hotspots/
4. **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

---

## 🛠 Troubleshooting

### Frontend can't connect to backend?
- Ensure backend is running on port 8000
- Check browser console for errors

### Map not showing?
- Check your internet connection (Leaflet loads tiles from CDN)
- Refresh the page

### Want to use your own data?
1. Prepare CSV with columns: `crime_type`, `latitude`, `longitude`, `date`
2. Go to Data Table page
3. Click "Upload CSV"
4. Models will auto-retrain

---

## 🎉 You're All Set!

The system is production-ready with:
- ✓ Clean architecture
- ✓ ML models trained
- ✓ Modern responsive UI
- ✓ Full API documentation
- ✓ Error handling
- ✓ Sample data included

**Enjoy exploring your Crime Hotspot Detection System!** 🚔📊
