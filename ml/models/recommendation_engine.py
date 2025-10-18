
"""
Recommendation Engine
Combines all ML models to generate personalized recommendations
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os

class RecommendationEngine:
    def __init__(self, predictor=None, pattern_recognizer=None, anomaly_detector=None):
        self.predictor = predictor
        self.pattern_recognizer = pattern_recognizer
        self.anomaly_detector = anomaly_detector
    
    def generate_recommendations(self, user_data, predictions=None, pattern=None, anomaly=None):
        """
        Generate personalized recommendations
        
        Args:
            user_data: DataFrame with user's recent activity data
            predictions: Predictions from ProductivityPredictor (optional)
            pattern: Pattern analysis from PatternRecognizer (optional)
            anomaly: Anomaly detection from AnomalyDetector (optional)
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # 1. Recommendations from Predictions
        if predictions is not None and len(predictions) > 0:
            # Find peak productivity hour
            peak_hour_idx = predictions['predicted_score'].idxmax()
            peak_hour = predictions.loc[peak_hour_idx]
            
            recommendations.append({
                'type': 'timing',
                'priority': 'high',
                'icon': '🎯',
                'title': 'Schedule Your Most Important Task',
                'message': f"Your productivity peaks at {int(peak_hour['hour'])}:00 with a predicted score of {peak_hour['predicted_score']:.1f}/10. Schedule deep work then!",
                'action': 'schedule_deep_work',
                'data': {'hour': int(peak_hour['hour']), 'score': float(peak_hour['predicted_score'])}
            })
            
            # Find low productivity hours
            low_hour_idx = predictions['predicted_score'].idxmin()
            low_hour = predictions.loc[low_hour_idx]
            
            if low_hour['predicted_score'] < 6:
                recommendations.append({
                    'type': 'timing',
                    'priority': 'medium',
                    'icon': '📅',
                    'title': 'Avoid Deep Work During Low Energy',
                    'message': f"Your energy dips at {int(low_hour['hour'])}:00. Schedule meetings or light tasks then.",
                    'action': 'schedule_light_work',
                    'data': {'hour': int(low_hour['hour'])}
                })
        
        # 2. Recommendations from Pattern Recognition
        if pattern is not None:
            if pattern['pattern_type'] == 'Morning Person':
                recommendations.append({
                    'type': 'pattern',
                    'priority': 'high',
                    'icon': '🌅',
                    'title': "You're a Morning Person!",
                    'message': f"Your peak hours are {pattern['peak_hours']}. Block these for creative work.",
                    'action': 'block_peak_hours',
                    'data': pattern
                })
            elif pattern['pattern_type'] == 'Night Owl':
                recommendations.append({
                    'type': 'pattern',
                    'priority': 'high',
                    'icon': '🌙',
                    'title': "You're a Night Owl!",
                    'message': f"You work best in the evening. Consider flexible hours.",
                    'data': pattern
                })
        
        # 3. Recommendations from Anomaly Detection
        if anomaly is not None:
            if anomaly['is_anomaly']:
                if anomaly['risk_level'] in ['critical', 'high']:
                    recommendations.append({
                        'type': 'health',
                        'priority': 'critical',
                        'icon': '🚨',
                        'title': 'Burnout Risk Detected!',
                        'message': 'Take a break today. Your wellbeing matters more than work.',
                        'action': 'take_day_off',
                        'data': anomaly
                    })
            
            # Specific alerts
            for alert in anomaly.get('alerts', []):
                if alert['severity'] == 'high':
                    recommendations.append({
                        'type': 'health',
                        'priority': 'high',
                        'icon': '⚠️',
                        'title': alert['type'].replace('_', ' ').title(),
                        'message': alert['message'],
                        'action': f"fix_{alert['type']}",
                        'data': alert
                    })
        
        # 4. General Recommendations
        if len(user_data) > 0:
            # Check recent work hours
            user_data['timestamp'] = pd.to_datetime(user_data['timestamp'])
            today = user_data[user_data['timestamp'].dt.date == user_data['timestamp'].dt.date.max()]
            
            work_today = today[today['activity_type'] == 'work']['duration'].sum() / 60
            breaks_today = len(today[today['activity_type'] == 'break'])
            
            # Break recommendation
            if work_today > 2 and breaks_today < 2:
                recommendations.append({
                    'type': 'break',
                    'priority': 'medium',
                    'icon': '☕',
                    'title': 'Time for a Break',
                    'message': f"You've worked {work_today:.1f} hours with only {breaks_today} breaks. Take a 5-10 minute break!",
                    'action': 'take_break',
                    'data': {'work_hours': work_today, 'breaks': breaks_today}
                })
            
            # Positive reinforcement
            avg_productivity = today['productivity_score'].mean()
            if avg_productivity > 7:
                recommendations.append({
                    'type': 'encouragement',
                    'priority': 'low',
                    'icon': '🎉',
                    'title': 'Great Work Today!',
                    'message': f"Your productivity is {avg_productivity:.1f}/10 - above your average! Keep it up!",
                    'action': 'celebrate',
                    'data': {'score': avg_productivity}
                })
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 99))
        
        return recommendations


# Test the engine
if __name__ == "__main__":
    print("="*60)
    print("�� Testing Recommendation Engine")
    print("="*60)
    print()
    
    # Import other models
    import sys
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    sys.path.insert(0, ml_dir)
    
    from models.productivity_predictor import ProductivityPredictor
    from models.pattern_recognition import PatternRecognizer
    from models.anomaly_detection import AnomalyDetector
    
    # Load data
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} activities")
    
    # Initialize and run all models
    print("🤖 Running all ML models...")
    
    # Predictor
    predictor = ProductivityPredictor()
    predictor.train(data_path)
    predictions = predictor.predict(periods=24)
    
    # Pattern
    recognizer = PatternRecognizer()
    recognizer.train(data_path)
    pattern = recognizer.predict_pattern(df)
    
    # Anomaly
    detector = AnomalyDetector()
    detector.train(data_path)
    anomaly = detector.detect(df)
    
    # Generate recommendations
    engine = RecommendationEngine()
    recommendations = engine.generate_recommendations(df, predictions, pattern, anomaly)
    
    print()
    print("="*60)
    print(f"💡 Generated {len(recommendations)} Recommendations")
    print("="*60)
    print()
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['icon']} [{rec['priority'].upper()}] {rec['title']}")
        print(f"   {rec['message']}")
        print()
    
    print("✅ Recommendation Engine test complete!")
    print()
