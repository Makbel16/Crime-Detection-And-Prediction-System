"""
Hotspot Detection Service
Uses K-Means clustering to identify crime hotspots
"""

from sklearn.cluster import KMeans
import numpy as np
import joblib
import os

class HotspotDetector:
    """
    K-Means based crime hotspot detector
    
    Identifies geographic clusters where crimes occur frequently
    """
    
    def __init__(self, n_clusters=5, model_path="models/hotspot_model.pkl"):
        """
        Initialize hotspot detector
        
        Args:
            n_clusters: Number of hotspot clusters to detect
            model_path: Path to save/load the trained model
        """
        self.n_clusters = n_clusters
        self.model_path = model_path
        self.kmeans = None
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    def train(self, coordinates):
        """
        Train K-Means model on crime coordinates
        
        Args:
            coordinates: numpy array of shape (n_samples, 2) with [latitude, longitude]
        
        Returns:
            numpy array of cluster labels
        """
        print(f"Training K-Means with {self.n_clusters} clusters...")
        
        # Initialize and fit K-Means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        
        # Fit model and get cluster labels
        labels = self.kmeans.fit_predict(coordinates)
        
        # Save model
        joblib.dump(self.kmeans, self.model_path)
        print(f"✓ Hotspot model saved to {self.model_path}")
        
        return labels
    
    def predict(self, coordinates):
        """
        Predict hotspot cluster for given coordinates
        
        Args:
            coordinates: numpy array of shape (n_samples, 2)
        
        Returns:
            numpy array of cluster labels
        """
        if self.kmeans is None:
            # Load model if not already loaded
            self.load_model()
        
        return self.kmeans.predict(coordinates)
    
    def load_model(self):
        """Load trained K-Means model from disk"""
        if os.path.exists(self.model_path):
            self.kmeans = joblib.load(self.model_path)
            print(f"✓ Hotspot model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
    
    def get_cluster_centers(self):
        """
        Get coordinates of cluster centers (hotspot centers)
        
        Returns:
            numpy array of cluster center coordinates
        """
        if self.kmeans is None:
            self.load_model()
        
        return self.kmeans.cluster_centers_
    
    def get_hotspot_statistics(self, labels):
        """
        Get statistics for each hotspot cluster
        
        Args:
            labels: numpy array of cluster labels
        
        Returns:
            dict with statistics for each cluster
        """
        unique, counts = np.unique(labels, return_counts=True)
        
        stats = {}
        for cluster_id, count in zip(unique, counts):
            stats[int(cluster_id)] = {
                'count': int(count),
                'percentage': round(float(count / len(labels) * 100), 2)
            }
        
        return stats
