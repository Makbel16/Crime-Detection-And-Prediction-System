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
  // Get all crimes with pagination
  getCrimes: (skip = 0, limit = 100) => 
    api.get(`/crimes/?skip=${skip}&limit=${limit}`),
  
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

export default api;
