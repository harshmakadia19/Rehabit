
"""
Rehabit Backend API with ML Integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Create FastAPI app
app = FastAPI(
    title="Rehabit API",
    description="AI-powered productivity tracking and insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ML Service
ml_service = None

@app.on_event("startup")
def startup_event():
    """Initialize ML service and database on startup"""
    global ml_service
    
    # Initialize database
    try:
        from app.database import init_db
        init_db()
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
    
    # Initialize ML service
    try:
        # Get correct path to ml directory
        # backend/app/main.py -> backend/app -> backend -> Rehabit -> ml
        current_file = os.path.abspath(__file__)  # .../backend/app/main.py
        app_dir = os.path.dirname(current_file)   # .../backend/app
        backend_dir = os.path.dirname(app_dir)    # .../backend
        project_dir = os.path.dirname(backend_dir) # .../Rehabit
        ml_path = os.path.join(project_dir, 'ml')  # .../Rehabit/ml
        
        sys.path.insert(0, ml_path)
        print(f"✅ ML Path: {ml_path}")
        
        from models.productivity_predictor import ProductivityPredictor
        from models.pattern_recognition import PatternRecognizer
        from models.anomaly_detection import AnomalyDetector
        from models.recommendation_engine import RecommendationEngine
        import pandas as pd
        
        class MLService:
            def __init__(self):
                print("🤖 Initializing ML Service...")
                self.predictor = ProductivityPredictor()
                self.recognizer = PatternRecognizer()
                self.detector = AnomalyDetector()
                self.engine = RecommendationEngine()
                self.ml_path = ml_path
                
                models_dir = os.path.join(ml_path, 'saved_models')
                self.predictor.load_model(os.path.join(models_dir, 'productivity_model.pkl'))
                self.recognizer.load_model(os.path.join(models_dir, 'pattern_model.pkl'))
                self.detector.load_model(os.path.join(models_dir, 'anomaly_model.pkl'))
                print("✅ All ML models loaded successfully")
            
            def get_dashboard_data(self, user_id):
                import pandas as pd
                demo_path = os.path.join(self.ml_path, 'data', 'demo_activities.csv')
                user_data = pd.read_csv(demo_path)
                
                predictions = self.predictor.predict(periods=24)
                pattern = self.recognizer.predict_pattern(user_data)
                anomaly = self.detector.detect(user_data)
                recommendations = self.engine.generate_recommendations(
                    user_data, predictions, pattern, anomaly
                )
                
                return {
                    'predictions': predictions.to_dict('records'),
                    'pattern': pattern,
                    'anomaly': anomaly,
                    'recommendations': recommendations
                }
        
        ml_service = MLService()
        print("🚀 Rehabit API started successfully with ML models")
        
    except Exception as e:
        print(f"⚠️  ML Service failed: {e}")
        print("   Dashboard will use fallback data")
        import traceback
        traceback.print_exc()

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Rehabit API",
        "version": "1.0.0",
        "status": "running",
        "ml_loaded": ml_service is not None,
        "endpoints": {
            "dashboard": "/api/dashboard/1",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ml_loaded": ml_service is not None
    }

# Dashboard endpoint
@app.get("/api/dashboard/{user_id}")
async def get_dashboard(user_id: int):
    """Get complete dashboard data with ML insights"""
    
    # Basic stats
    stats = {
        'current_productivity': 8.3,
        'productivity_change': 23.5,
        'work_time_today': 245,
        'work_time_change': 12.0,
        'streak_days': 7,
        'streak_change': 1,
        'avg_weekly_productivity': 7.8,
        'weekly_change': 15.3,
    }
    
    # Try to get ML data
    if ml_service:
        try:
            print(f"🔮 Getting ML data for user {user_id}")
            ml_data = ml_service.get_dashboard_data(user_id)
            return {
                'status': 'success',
                'data': {
                    'stats': stats,
                    'predictions': ml_data['predictions'],
                    'pattern': ml_data['pattern'],
                    'anomaly': ml_data['anomaly'],
                    'recommendations': ml_data['recommendations']
                }
            }
        except Exception as e:
            print(f"❌ ML error: {e}")
            import traceback
            traceback.print_exc()
    
    # Fallback without ML (mock data for frontend development)
    return {
        'status': 'success',
        'data': {
            'stats': stats,
            'predictions': [
                {'hour': i, 'predicted_score': 5.0 + abs(12 - i) * 0.3, 'confidence': 0.85}
                for i in range(24)
            ],
            'pattern': {
                'pattern_type': 'Morning Person',
                'peak_hours': [9, 10, 11],
                'low_energy_hours': [14, 15, 16],
                'avg_productivity': 7.8
            },
            'anomaly': {
                'is_anomaly': False,
                'risk_level': 'normal',
                'alerts': []
            },
            'recommendations': [
                {
                    'icon': '🎯',
                    'priority': 'high',
                    'title': 'Schedule Deep Work in the Morning',
                    'message': 'Your productivity peaks between 9-11 AM. Schedule your most important tasks during this time.'
                },
                {
                    'icon': '☕',
                    'priority': 'medium',
                    'title': 'Take Breaks',
                    'message': 'Your energy dips around 2-4 PM. Take short breaks to recharge.'
                },
                {
                    'icon': '🎉',
                    'priority': 'low',
                    'title': 'Great Streak!',
                    'message': 'You\'re on a 7-day productivity streak. Keep it up!'
                }
            ]
        }
    }
