
"""
Anomaly Detection using Isolation Forest
Detects overwork, burnout, and unusual behavior patterns
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        
    def prepare_daily_features(self, df):
        """Aggregate data by day and create features"""
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        daily_data = []
        
        for date in df['date'].unique():
            day_data = df[df['date'] == date]
            
            # Calculate daily metrics
            total_work = day_data[day_data['activity_type'] == 'work']['duration'].sum()
            avg_productivity = day_data['productivity_score'].mean()
            break_count = len(day_data[day_data['activity_type'] == 'break'])
            
            # Late work (after 8 PM)
            late_work = day_data[
                (day_data['activity_type'] == 'work') & 
                (day_data['timestamp'].dt.hour >= 20)
            ]['duration'].sum()
            
            # Number of activities
            activity_count = len(day_data)
            
            daily_data.append({
                'date': date,
                'total_work_hours': total_work / 60,
                'avg_productivity': avg_productivity,
                'break_count': break_count,
                'late_work_hours': late_work / 60,
                'activity_count': activity_count
            })
        
        return pd.DataFrame(daily_data)
    
    def train(self, data_path):
        """
        Train anomaly detection model
        
        Args:
            data_path: Path to CSV with historical data
        """
        print("�� Training Anomaly Detector...")
        
        df = pd.read_csv(data_path)
        print(f"✅ Loaded {len(df)} activities")
        
        daily_df = self.prepare_daily_features(df)
        print(f"📊 Aggregated to {len(daily_df)} days")
        
        # Prepare features
        features = daily_df[[
            'total_work_hours',
            'avg_productivity',
            'break_count',
            'late_work_hours',
            'activity_count'
        ]].values
        
        # Scale and train
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled)
        
        print("✅ Anomaly detector trained")
    
    def detect(self, df):
        """
        Detect anomalies in recent behavior
        
        Args:
            df: DataFrame with recent activity data
            
        Returns:
            Dictionary with anomaly analysis
        """
        daily_df = self.prepare_daily_features(df)
        
        if len(daily_df) == 0:
            return {
                'is_anomaly': False,
                'anomaly_score': 0.0,
                'risk_level': 'normal',
                'alerts': [],
                'metrics': {}
            }
        
        # Prepare features
        features = daily_df[[
            'total_work_hours',
            'avg_productivity',
            'break_count',
            'late_work_hours',
            'activity_count'
        ]].values
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        predictions = self.model.predict(features_scaled)
        scores = self.model.score_samples(features_scaled)
        
        # Check if latest day is anomaly (-1 = anomaly, 1 = normal)
        is_anomaly = predictions[-1] == -1
        
        # Get latest day metrics
        latest_day = daily_df.iloc[-1]
        
        # Generate specific alerts
        alerts = []
        
        if latest_day['total_work_hours'] > 10:
            alerts.append({
                'type': 'overwork',
                'severity': 'high',
                'message': f"Working {latest_day['total_work_hours']:.1f} hours - that's too much!"
            })
        
        if latest_day['break_count'] < 2:
            alerts.append({
                'type': 'no_breaks',
                'severity': 'high',
                'message': f"Only {latest_day['break_count']} breaks today - take more breaks!"
            })
        
        if latest_day['late_work_hours'] > 2:
            alerts.append({
                'type': 'late_work',
                'severity': 'medium',
                'message': f"Worked {latest_day['late_work_hours']:.1f} hours after 8 PM"
            })
        
        if latest_day['avg_productivity'] < 5:
            alerts.append({
                'type': 'low_productivity',
                'severity': 'medium',
                'message': f"Productivity at {latest_day['avg_productivity']:.1f}/10 - below your average"
            })
        
        # Determine risk level
        if is_anomaly and len(alerts) >= 3:
            risk_level = 'critical'
        elif is_anomaly and len(alerts) >= 2:
            risk_level = 'high'
        elif len(alerts) >= 1:
            risk_level = 'medium'
        else:
            risk_level = 'normal'
        
        return {
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': float(scores[-1]),
            'risk_level': risk_level,
            'alerts': alerts,
            'metrics': {
                'work_hours': float(latest_day['total_work_hours']),
                'productivity': float(latest_day['avg_productivity']),
                'breaks': int(latest_day['break_count']),
                'late_work': float(latest_day['late_work_hours'])
            }
        }
    
    def save_model(self, path):
        """Save model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, path)
        print(f"💾 Anomaly model saved to {path}")
    
    def load_model(self, path):
        """Load model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        print(f"📂 Anomaly model loaded from {path}")


# Test the model
if __name__ == "__main__":
    print("="*60)
    print("🚨 Testing Anomaly Detection")
    print("="*60)
    print()
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_path = os.path.join(ml_dir, 'data', 'demo_activities.csv')
    
    if not os.path.exists(data_path):
        print("❌ Demo data not found!")
        exit(1)
    
    # Load data
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} activities")
    
    # Train detector
    detector = AnomalyDetector()
    detector.train(data_path)
    
    print()
    print("="*60)
    print("🔍 Anomaly Detection Results")
    print("="*60)
    print()
    
    # Detect anomalies
    result = detector.detect(df)
    
    print(f"⚠️  Anomaly Detected: {result['is_anomaly']}")
    print(f"📊 Anomaly Score: {result['anomaly_score']:.3f}")
    print(f"🚨 Risk Level: {result['risk_level'].upper()}")
    
    print("\n📈 Today's Metrics:")
    for key, value in result['metrics'].items():
        print(f"  - {key}: {value}")
    
    if result['alerts']:
        print(f"\n⚠️  Alerts ({len(result['alerts'])}):")
        for alert in result['alerts']:
            print(f"  [{alert['severity'].upper()}] {alert['message']}")
    else:
        print("\n✅ No alerts - healthy work pattern!")
    
    # Save model
    print()
    model_path = os.path.join(ml_dir, 'saved_models', 'anomaly_model.pkl')
    detector.save_model(model_path)
    
    print()
    print("✅ Anomaly Detection test complete!")
    print()
