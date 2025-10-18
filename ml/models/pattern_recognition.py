"""
Pattern Recognition using K-Means Clustering
Identifies user behavior patterns (Morning Person, Night Owl, etc.)
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os

class PatternRecognizer:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.labels = {
            0: "Morning Person",
            1: "Night Owl",
            2: "Consistent Worker"
        }
        
    def prepare_features(self, df):
        """Prepare hourly productivity features"""
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by hour of day and get average productivity
        hourly_avg = df.groupby(df['timestamp'].dt.hour)['productivity_score'].mean()
        
        # Create 24-hour feature vector
        features = np.zeros(24)
        for hour, score in hourly_avg.items():
            features[hour] = score
        
        return features.reshape(1, -1)
    
    def train(self, data_path):
        """
        Train on demo data (simulating multiple user patterns)
        
        Args:
            data_path: Path to CSV with activity data
        """
        print("🎓 Training Pattern Recognizer...")
        
        df = pd.read_csv(data_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create synthetic users by shifting hours
        all_features = []
        
        # Original pattern (morning person)
        features = self.prepare_features(df)
        all_features.append(features[0])
        
        # Shift +8 hours (night owl simulation)
        df_shifted = df.copy()
        df_shifted['timestamp'] = df_shifted['timestamp'] + pd.Timedelta(hours=8)
        features_night = self.prepare_features(df_shifted)
        all_features.append(features_night[0])
        
        # Consistent worker (flatten the pattern)
        df_consistent = df.copy()
        df_consistent['productivity_score'] = df_consistent['productivity_score'].mean()
        features_consistent = self.prepare_features(df_consistent)
        all_features.append(features_consistent[0])
        
        X = np.array(all_features)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        
        print(f"✅ Pattern model trained with {len(all_features)} patterns")
        
    def predict_pattern(self, df):
        """
        Predict user's productivity pattern
        
        Args:
            df: DataFrame with user activity data
            
        Returns:
            Dictionary with pattern analysis
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Prepare features
        features = self.prepare_features(df)
        features_scaled = self.scaler.transform(features)
        
        # Predict cluster
        cluster = self.model.predict(features_scaled)[0]
        
        # Get peak and low energy hours
        hourly_avg = df.groupby(df['timestamp'].dt.hour)['productivity_score'].mean()
        peak_hours = hourly_avg.nlargest(3).index.tolist()
        low_hours = hourly_avg.nsmallest(3).index.tolist()
        
        return {
            'pattern_type': self.labels.get(cluster, "Unknown"),
            'cluster_id': int(cluster),
            'peak_hours': [int(h) for h in peak_hours],
            'low_energy_hours': [int(h) for h in low_hours],
            'avg_productivity': float(df['productivity_score'].mean()),
            'peak_productivity': float(hourly_avg.max()),
            'low_productivity': float(hourly_avg.min())
        }
    
    def save_model(self, path):
        """Save model and scaler"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'labels': self.labels
        }, path)
        print(f"💾 Pattern model saved to {path}")
    
    def load_model(self, path):
        """Load model and scaler"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.labels = data['labels']
        print(f"�� Pattern model loaded from {path}")


# Test the model
if __name__ == "__main__":
    print("="*60)
    print("🔍 Testing Pattern Recognition")
    print("="*60)
    print()
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    
    if not os.path.exists(data_path):
        print("❌ Demo data not found!")
        print("Run: python scripts/generate_demo_data.py")
        exit(1)
    
    # Load data
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} activities")
    
    # Train the recognizer
    recognizer = PatternRecognizer()
    recognizer.train(data_path)
    
    print()
    print("="*60)
    print("📊 Pattern Analysis")
    print("="*60)
    print()
    
    # Predict pattern
    pattern = recognizer.predict_pattern(df)
    
    print(f"🎯 Pattern Type: {pattern['pattern_type']}")
    print(f"🚀 Peak Hours: {pattern['peak_hours']}")
    print(f"😴 Low Energy Hours: {pattern['low_energy_hours']}")
    print(f"📊 Average Productivity: {pattern['avg_productivity']:.2f}/10")
    print(f"📈 Peak Productivity: {pattern['peak_productivity']:.2f}/10")
    print(f"📉 Low Productivity: {pattern['low_productivity']:.2f}/10")
    
    # Save model
    print()
    model_path = os.path.join(ml_dir, 'saved_models', 'pattern_model.pkl')
    recognizer.save_model(model_path)
    
    print()
    print("✅ Pattern Recognition test complete!")
    print()
