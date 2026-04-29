import axios from 'axios';

// API base URL
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Crime APIs
export const crimeAPI = {
  // Get all crimes with pagination, search and filters
  getCrimes: (params = {}) => {
    const {
      skip = 0,
      limit = 100,
      search,
      crime_type,
      start_date,
      end_date,
      start_hour,
      end_hour,
      day,
      month,
      hotspot_cluster
    } = params;
    
    const queryParams = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString()
    });
    
    if (search) queryParams.append('search', search);
    if (crime_type) queryParams.append('crime_type', crime_type);
    if (start_date) queryParams.append('start_date', start_date);
    if (end_date) queryParams.append('end_date', end_date);
    if (start_hour !== undefined) queryParams.append('start_hour', start_hour.toString());
    if (end_hour !== undefined) queryParams.append('end_hour', end_hour.toString());
    if (day !== undefined) queryParams.append('day', day.toString());
    if (month !== undefined) queryParams.append('month', month.toString());
    if (hotspot_cluster !== undefined) queryParams.append('hotspot_cluster', hotspot_cluster.toString());
    
    return api.get(`/crimes/?${queryParams.toString()}`);
  },
  
  // Get crime statistics
  getStats: () => 
    api.get('/crimes/stats'),
  
  // Upload CSV file
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/crimes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  // Generate sample data
  generateSample: () => 
    api.post('/crimes/generate-sample'),
};

// Hotspot APIs
export const hotspotAPI = {
  // Get hotspots
  getHotspots: () => 
    api.get('/hotspots/'),
  
  // Get cluster centers
  getCenters: () => 
    api.get('/hotspots/centers'),
  
  // Retrain model
  retrain: (nClusters = 5) => 
    api.post(`/hotspots/retrain?n_clusters=${nClusters}`),
};

// Prediction APIs
export const predictionAPI = {
  // Predict crime risk
  predict: (data) => 
    api.post('/predict/', data),
  
  // Batch prediction
  batchPredict: (inputs) => 
    api.post('/predict/batch', inputs),
  
  // Get feature importance
  getFeatureImportance: () => 
    api.get('/predict/feature-importance'),
};

// Trends APIs
export const trendsAPI = {
  // Get monthly trends
  getMonthlyTrends: (startDate, endDate) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return api.get(`/trends/monthly?${params.toString()}`);
  },
  
  // Get yearly trends
  getYearlyTrends: (startYear, endYear) => {
    const params = new URLSearchParams();
    if (startYear) params.append('start_year', startYear);
    if (endYear) params.append('end_year', endYear);
    return api.get(`/trends/yearly?${params.toString()}`);
  },
  
  // Get seasonal analysis
  getSeasonalAnalysis: () => 
    api.get('/trends/seasonal'),
  
  // Get future predictions
  getFuturePredictions: (monthsAhead = 12) => 
    api.get(`/trends/predict?months_ahead=${monthsAhead}`),
  
  // Get crime type trends
  getCrimeTypeTrends: (crimeType) => {
    const params = new URLSearchParams();
    if (crimeType) params.append('crime_type', crimeType);
    return api.get(`/trends/crime-types?${params.toString()}`);
  },
  
  // Get trends summary
  getTrendsSummary: () => 
    api.get('/trends/summary'),
};

export default api;
