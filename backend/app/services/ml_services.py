"""
ML Service - Integrates Harsh's ML models
"""
import sys
import os
import pandas as pd

# Calculate path to ml directory
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
project_dir = os.path.dirname(backend_dir)
ml_path = os.path.join(project_dir, 'ml')

# Add ml directory to Python path
sys.path.insert(0, ml_path)
print(f"✅ ML Path: {ml_path}")

try:
    # Import ML models
    from models.productivity_predictor import ProductivityPredictor
    from models.pattern_recognition import PatternRecognizer
    from models.anomaly_detection import AnomalyDetector
    from models.recommendation_engine import RecommendationEngine
    
    class MLService:
        """Service to interact with ML models"""
        
        def __init__(self):
            print("🤖 Initializing ML Service...")
            
            # Initialize models
            self.predictor = ProductivityPredictor()
            self.recognizer = PatternRecognizer()
            self.detector = AnomalyDetector()
            self.engine = RecommendationEngine()
            
            # Load trained models
            models_dir = os.path.join(ml_path, 'saved_models')
            
            try:
                self.predictor.load_model(os.path.join(models_dir, 'productivity_model.pkl'))
                self.recognizer.load_model(os.path.join(models_dir, 'pattern_model.pkl'))
                self.detector.load_model(os.path.join(models_dir, 'anomaly_model.pkl'))
                print("✅ All ML models loaded successfully")
            except Exception as e:
                print(f"⚠️  Warning: Could not load models: {e}")
        
        def get_dashboard_data(self, user_id: int):
            """Get complete dashboard data for user"""
            print(f"🔮 Generating ML insights for user {user_id}...")
            
            # Get user data
            user_data = self._get_user_data(user_id)
            
            # Generate predictions
            predictions = self.predictor.predict(periods=24)
            
            # Recognize pattern
            pattern = self.recognizer.predict_pattern(user_data)
            
            # Detect anomalies
            anomaly = self.detector.detect(user_data)
            
            # Generate recommendations
            recommendations = self.engine.generate_recommendations(
                user_data, predictions, pattern, anomaly
            )
            
            return {
                'predictions': predictions.to_dict('records'),
                'pattern': pattern,
                'anomaly': anomaly,
                'recommendations': recommendations
            }
        
        def _get_user_data(self, user_id: int):
            """Get user's activity data"""
            demo_data_path = os.path.join(ml_path, 'data', 'demo_activities.csv')
            if os.path.exists(demo_data_path):
                df = pd.read_csv(demo_data_path)
                return df
            else:
                print("⚠️  Warning: Demo data not found")
                return pd.DataFrame()
    
    # Create singleton instance
    ml_service = MLService()
    
except Exception as e:
    print(f"⚠️  Warning: ML Service initialization failed: {e}")
    print(f"   ML models will not be available")
    ml_service = None

