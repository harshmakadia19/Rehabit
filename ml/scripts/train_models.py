
"""
Train all ML models at once
"""
import sys
import os

# Fix imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.productivity_predictor import ProductivityPredictor
from models.pattern_recognition import PatternRecognizer
from models.anomaly_detection import AnomalyDetector

def main():
    print("="*60)
    print("🤖 REHABIT ML MODEL TRAINING")
    print("="*60)
    print()
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    models_dir = os.path.join(ml_dir, 'saved_models')
    
    # Check data exists
    if not os.path.exists(data_path):
        print("❌ Demo data not found!")
        print("Run: python scripts/generate_demo_data.py")
        exit(1)
    
    print(f"📂 Data: {data_path}")
    print(f"💾 Models will be saved to: {models_dir}")
    print()
    
    # Train Productivity Predictor
    print("1️⃣  Training Productivity Predictor...")
    predictor = ProductivityPredictor()
    predictor.train(data_path)
    predictor.save_model(os.path.join(models_dir, 'productivity_model.pkl'))
    print()
    
    # Train Pattern Recognizer
    print("2️⃣  Training Pattern Recognizer...")
    recognizer = PatternRecognizer()
    recognizer.train(data_path)
    recognizer.save_model(os.path.join(models_dir, 'pattern_model.pkl'))
    print()
    
    # Train Anomaly Detector
    print("3️⃣  Training Anomaly Detector...")
    detector = AnomalyDetector()
    detector.train(data_path)
    detector.save_model(os.path.join(models_dir, 'anomaly_model.pkl'))
    print()
    
    print("="*60)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*60)
    print()
    print("�� Saved models:")
    print("  - productivity_model.pkl")
    print("  - pattern_model.pkl")
    print("  - anomaly_model.pkl")
    print()
    print("🚀 Next step: Test with scripts/test_integration.py")
    print()

if __name__ == "__main__":
    main()
