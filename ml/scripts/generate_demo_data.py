"""
Generate demo data for Rehabit
Creates 14 days of realistic activity data for training ML models
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# NO IMPORTS FROM models - we don't need them yet!

def generate_demo_data(user_id=1, days=14):
    """
    Generate realistic activity data for demo user
    
    Args:
        user_id: ID of the user
        days: Number of days of historical data to generate
    
    Returns:
        DataFrame with generated activities
    """
    
    print(f"📊 Generating {days} days of demo data...")
    
    activities = []
    start_date = datetime.now() - timedelta(days=days)
    
    # Simulate a "morning person" pattern with some variation
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        # Skip some weekends (more realistic)
        is_weekend = current_date.weekday() >= 5
        if is_weekend and np.random.random() > 0.3:
            continue
        
        # Determine if this is a "good day" or "bad day"
        day_quality = np.random.choice(['good', 'normal', 'bad'], p=[0.3, 0.5, 0.2])
        
        # Morning session (9 AM - high productivity for morning person)
        if day_quality == 'good':
            morning_score = np.random.randint(8, 11)
            morning_duration = np.random.randint(100, 150)
        elif day_quality == 'normal':
            morning_score = np.random.randint(7, 9)
            morning_duration = np.random.randint(80, 120)
        else:
            morning_score = np.random.randint(5, 8)
            morning_duration = np.random.randint(60, 90)
        
        activities.append({
            'user_id': user_id,
            'timestamp': current_date.replace(hour=9, minute=0, second=0),
            'activity_type': 'work',
            'duration': morning_duration,
            'productivity_score': min(10, morning_score),
            'focus_level': 'high' if morning_score >= 7 else 'medium',
            'notes': 'Morning deep work session'
        })
        
        # Mid-morning break
        activities.append({
            'user_id': user_id,
            'timestamp': current_date.replace(hour=10, minute=45, second=0),
            'activity_type': 'break',
            'duration': 15,
            'productivity_score': 5,
            'focus_level': 'low',
            'notes': 'Coffee break'
        })
        
        # Late morning work (11 AM)
        activities.append({
            'user_id': user_id,
            'timestamp': current_date.replace(hour=11, minute=0, second=0),
            'activity_type': 'work',
            'duration': np.random.randint(60, 90),
            'productivity_score': max(5, morning_score - 1),
            'focus_level': 'high' if morning_score >= 7 else 'medium',
            'notes': 'Continued work before lunch'
        })
        
        # Lunch break
        activities.append({
            'user_id': user_id,
            'timestamp': current_date.replace(hour=12, minute=30, second=0),
            'activity_type': 'break',
            'duration': np.random.randint(45, 75),
            'productivity_score': 4,
            'focus_level': 'low',
            'notes': 'Lunch break'
        })
        
        # Post-lunch dip (2 PM)
        afternoon_score = np.random.randint(4, 7)
        activities.append({
            'user_id': user_id,
            'timestamp': current_date.replace(hour=14, minute=0, second=0),
            'activity_type': 'work',
            'duration': np.random.randint(60, 90),
            'productivity_score': afternoon_score,
            'focus_level': 'medium' if afternoon_score >= 6 else 'low',
            'notes': 'Post-lunch session'
        })
        
        # Late afternoon (4 PM)
        if np.random.random() > 0.4:
            activity_type = 'meeting' if np.random.random() > 0.5 else 'work'
            activities.append({
                'user_id': user_id,
                'timestamp': current_date.replace(hour=16, minute=0, second=0),
                'activity_type': activity_type,
                'duration': np.random.randint(30, 90),
                'productivity_score': np.random.randint(5, 7),
                'focus_level': 'medium',
                'notes': 'Team meeting' if activity_type == 'meeting' else 'Late afternoon work'
            })
        
        # Exercise (some days)
        if not is_weekend and np.random.random() > 0.4:
            activities.append({
                'user_id': user_id,
                'timestamp': current_date.replace(hour=17, minute=30, second=0),
                'activity_type': 'exercise',
                'duration': np.random.randint(30, 60),
                'productivity_score': 6,
                'focus_level': 'medium',
                'notes': 'Gym / Exercise session'
            })
    
    # Create DataFrame
    df = pd.DataFrame(activities)
    
    # Ensure data directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(ml_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(data_dir, 'demo_activities.csv')
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(activities)} activities")
    print(f"📁 Saved to: {output_path}")
    print(f"📊 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"📈 Avg productivity: {df['productivity_score'].mean():.2f}/10")
    
    return df

def main():
    """Main execution function"""
    print("="*60)
    print("🎲 REHABIT - DEMO DATA GENERATOR")
    print("="*60)
    print()
    
    # Generate data
    df = generate_demo_data(user_id=1, days=14)
    
    print()
    print("="*60)
    print("📊 SAMPLE OF GENERATED DATA")
    print("="*60)
    print(df.head(10).to_string())
    
    print()
    print("="*60)
    print("📈 DATA STATISTICS")
    print("="*60)
    print(f"Total activities: {len(df)}")
    print(f"Activity types: {df['activity_type'].value_counts().to_dict()}")
    print(f"Avg productivity score: {df['productivity_score'].mean():.2f}/10")
    print(f"Avg duration: {df['duration'].mean():.0f} minutes")
    print(f"Focus levels: {df['focus_level'].value_counts().to_dict()}")
    
    print()
    print("✅ Demo data generation complete!")
    print("📝 Next step: Run train_models.py to train ML models")
    print()

if __name__ == "__main__":
    main()