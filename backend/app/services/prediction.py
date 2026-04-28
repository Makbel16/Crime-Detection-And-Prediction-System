"""
Crime Prediction Service
Uses Random Forest to predict crime risk levels
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import os

class CrimePredictor:
    """
    Random Forest based crime risk predictor
    
    Predicts crime risk level (Low, Medium, High) based on time and location
    """
    
    def __init__(self, model_path="models/crime_prediction_model.pkl", 
                 encoder_path="models/label_encoder.pkl"):
        """
        Initialize crime predictor
        
        Args:
            model_path: Path to save/load the trained model
            encoder_path: Path to save/load the label encoder
        """
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.label_encoder = None
        
        # Create models directory
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    def train(self, X, y):
        """
        Train Random Forest model
        
        Args:
            X: Features array (hour, day, month, latitude, longitude)
            y: Target labels (crime_type)
        """
        print("Training Random Forest model...")
        
        # Initialize label encoder
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Initialize Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        
        # Train model
        self.model.fit(X, y_encoded)
        
        # Save model and encoder
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.label_encoder, self.encoder_path)
        
        print(f"✓ Prediction model saved to {self.model_path}")
        print(f"✓ Label encoder saved to {self.encoder_path}")
        
        # Calculate accuracy
        accuracy = self.model.score(X, y_encoded)
        print(f"✓ Training accuracy: {accuracy:.2%}")
    
    def predict(self, X):
        """
        Predict crime risk level
        
        Args:
            X: Features array (hour, day, month, latitude, longitude)
        
        Returns:
            dict with prediction results
        """
        if self.model is None:
            self.load_model()
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X)[0]
        
        # Get predicted class
        predicted_class = self.model.predict(X)[0]
        predicted_crime = self.label_encoder.inverse_transform([predicted_class])[0]
        
        # Calculate risk level based on probability
        max_probability = max(probabilities)
        risk_level = self._calculate_risk_level(max_probability)
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = []
        for idx in top_indices:
            top_predictions.append({
                'crime_type': self.label_encoder.inverse_transform([idx])[0],
                'probability': round(float(probabilities[idx]), 4)
            })
        
        return {
            'predicted_crime': predicted_crime,
            'risk_level': risk_level,
            'confidence': round(float(max_probability), 4),
            'top_predictions': top_predictions
        }
    
    def _calculate_risk_level(self, probability):
        """
        Calculate risk level based on prediction confidence
        
        Args:
            probability: Model confidence score
        
        Returns:
            str: 'Low', 'Medium', or 'High'
        """
        if probability >= 0.7:
            return 'High'
        elif probability >= 0.4:
            return 'Medium'
        else:
            return 'Low'
    
    def load_model(self):
        """Load trained model and encoder from disk"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.label_encoder = joblib.load(self.encoder_path)
            print(f"✓ Prediction model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
    
    def get_feature_importance(self):
        """
        Get feature importance scores
        
        Returns:
            dict with feature names and importance scores
        """
        if self.model is None:
            self.load_model()
        
        feature_names = ['hour', 'day', 'month', 'latitude', 'longitude']
        importances = self.model.feature_importances_
        
        importance_dict = {
            name: round(float(imp), 4) 
            for name, imp in zip(feature_names, importances)
        }
        
        return importance_dict
