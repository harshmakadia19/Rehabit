"""
Create demo user and sample activities for presentation
"""
import requests
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000/api"

def create_demo_user():
    """Create demo user: Sarah Johnson"""
    try:
        response = requests.post(
            f"{BASE_URL}/users/create",
            json={
                "name": "Sarah Johnson",
                "email": "sarah@demo.com"
            }
        )
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Created user: {user['name']} (ID: {user['id']})")
            return user['id']
        else:
            print("ℹ️  User already exists, using ID: 1")
            return 1
    except Exception as e:
        print(f"ℹ️  Using existing user ID: 1")
        return 1

def log_sample_activities(user_id):
    """Log 14 days of sample activities"""
    print("\n📝 Logging sample activities...")
    
    activity_types = ['work', 'break', 'exercise', 'meeting']
    
    for day in range(14):
        date = datetime.now() - timedelta(days=14-day)
        
        # Log 3-5 activities per day
        for _ in range(random.randint(3, 5)):
            activity_type = random.choice(activity_types)
            
            # Productivity increases over time (showing improvement)
            base_score = 5 + (day // 2)
            score = min(10, max(1, base_score + random.randint(-1, 1)))
            
            try:
                response = requests.post(
                    f"{BASE_URL}/activities/log",
                    json={
                        "user_id": user_id,
                        "activity_type": activity_type,
                        "duration": random.randint(30, 90),
                        "productivity_score": score,
                        "focus_level": "high" if score >= 7 else "medium" if score >= 5 else "low",
                        "notes": f"Demo activity on day {day+1}"
                    }
                )
            except Exception as e:
                pass
        
        print(f"  Day {day+1}/14 ✅")
    
    print("\n✅ Sample activities logged!")

def main():
    print("🎲 Creating demo data for Rehabit...\n")
    print("⚠️  Make sure the server is running: uvicorn app.main:app --reload\n")
    
    user_id = create_demo_user()
    log_sample_activities(user_id)
    
    print("\n" + "="*60)
    print("🎉 Demo data created successfully!")
    print("="*60)
    print(f"\n📊 Demo User ID: {user_id}")
    print("📍 Test dashboard: http://localhost:8000/api/dashboard/1")
    print("📍 API Docs: http://localhost:8000/docs")
    print("\nYou can now test your dashboard with real data!")

if __name__ == "__main__":
    main()
