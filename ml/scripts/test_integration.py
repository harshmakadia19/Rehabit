
"""
Test that all models work together
This simulates what the backend will do
"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.productivity_predictor import ProductivityPredictor
from models.pattern_recognition import PatternRecognizer
from models.anomaly_detection import AnomalyDetector
from models.recommendation_engine import RecommendationEngine
import pandas as pd

def test_integration():
    print("="*60)
    print("🧪 INTEGRATION TEST - All Models")
    print("="*60)
    print()
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    
    # Load models
    print("📂 Loading trained models...")
    
    predictor = ProductivityPredictor()
    predictor.load_model(os.path.join(ml_dir, 'saved_models', 'productivity_model.pkl'))
    
    recognizer = PatternRecognizer()
    recognizer.load_model(os.path.join(ml_dir, 'saved_models', 'pattern_model.pkl'))
    
    detector = AnomalyDetector()
    detector.load_model(os.path.join(ml_dir, 'saved_models', 'anomaly_model.pkl'))
    
    engine = RecommendationEngine()
    
    # Load user data
    df = pd.read_csv(data_path)
    
    print()
    print("🤖 Running ML pipeline...")
    print()
    
    # 1. Get predictions
    print("1️⃣  Productivity Predictions (next 24 hours)")
    predictions = predictor.predict(periods=24)
    print(f"   ✅ Generated {len(predictions)} hourly predictions")
    peak = predictions.loc[predictions['predicted_score'].idxmax()]
    print(f"   🚀 Peak hour: {int(peak['hour'])}:00 with score {peak['predicted_score']:.2f}/10")
    print()
    
    # 2. Get pattern
    print("2️⃣  Pattern Recognition")
    pattern = recognizer.predict_pattern(df)
    print(f"   ✅ Pattern: {pattern['pattern_type']}")
    print(f"   🎯 Peak hours: {pattern['peak_hours']}")
    print()
    
    # 3. Detect anomalies
    print("3️⃣  Anomaly Detection")
    anomaly = detector.detect(df)
    print(f"   ✅ Anomaly detected: {anomaly['is_anomaly']}")
    print(f"   🚨 Risk level: {anomaly['risk_level']}")
    print(f"   ⚠️  Alerts: {len(anomaly['alerts'])}")
    print()
    
    # 4. Generate recommendations
    print("4️⃣  Recommendations")
    recommendations = engine.generate_recommendations(df, predictions, pattern, anomaly)
    print(f"   ✅ Generated {len(recommendations)} recommendations")
    print()
    
    # Display top 3 recommendations
    print("="*60)
    print("📋 TOP RECOMMENDATIONS")
    print("="*60)
    print()
    
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"{i}. {rec['icon']} [{rec['priority'].upper()}]")
        print(f"   {rec['title']}")
        print(f"   {rec['message']}")
        print()
    
    # Save sample output for backend
    output = {
        'predictions': predictions.to_dict('records')[:5],  # First 5 hours
        'pattern': pattern,
        'anomaly': anomaly,
        'recommendations': recommendations[:5]  # Top 5
    }
    
    output_path = os.path.join(ml_dir, 'sample_output.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("="*60)
    print("✅ INTEGRATION TEST PASSED!")
    print("="*60)
    print()
    print(f"📄 Sample output saved to: sample_output.json")
    print("🚀 Backend team can use this format for integration")
    print()

if __name__ == "__main__":
    test_integration()
