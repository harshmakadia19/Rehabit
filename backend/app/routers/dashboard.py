"""
Dashboard endpoint - returns complete dashboard data
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter()

@router.get("/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    """
    Get complete dashboard data for user
    Combines: today's stats, predictions, recommendations
    """
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get today's activities
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    activities_today = db.query(models.Activity).filter(
        models.Activity.user_id == user_id,
        models.Activity.timestamp >= today
    ).all()
    
    # Calculate today's stats
    if activities_today:
        avg_productivity = sum(a.productivity_score for a in activities_today) / len(activities_today)
        total_work_time = sum(a.duration for a in activities_today if a.activity_type == 'work')
        total_activities = len(activities_today)
    else:
        avg_productivity = 0
        total_work_time = 0
        total_activities = 0
    
    # Get 24-hour predictions (mock for now - will be real ML)
    current_hour = datetime.now().hour
    predictions = []
    for i in range(12):  # Next 12 hours
        hour = (current_hour + i) % 24
        # Create wave pattern (peaks at 10am and 2pm)
        if 9 <= hour <= 11:
            score = 8.5 + (i * 0.1)
        elif 14 <= hour <= 16:
            score = 8.0 + (i * 0.1)
        elif 6 <= hour <= 8 or 17 <= hour <= 19:
            score = 7.0
        else:
            score = 5.5
        
        predictions.append({
            'hour': hour,
            'score': round(score, 1),
            'time': f"{hour:02d}:00"
        })
    
    # Get recommendations (basic logic)
    recommendations = []
    
    # Peak time recommendation
    recommendations.append({
        'type': 'timing',
        'priority': 'high',
        'message': 'Schedule your most important task at 10:00 AM - your peak productivity time',
        'action': 'schedule_task',
        'icon': '⏰'
    })
    
    # Break recommendation based on work time
    if total_work_time > 120:  # More than 2 hours
        recommendations.append({
            'type': 'break',
            'priority': 'high',
            'message': "You've been working hard! Take a 10-minute break to recharge",
            'action': 'take_break',
            'icon': '☕'
        })
    else:
        recommendations.append({
            'type': 'break',
            'priority': 'medium',
            'message': 'Take a 5-minute break every hour for better focus',
            'action': 'take_break',
            'icon': '☕'
        })
    
    # Productivity feedback
    if avg_productivity >= 8:
        recommendations.append({
            'type': 'encouragement',
            'priority': 'low',
            'message': '🎉 Excellent work today! Your productivity is outstanding',
            'action': 'maintain_pace',
            'icon': '🌟'
        })
    elif avg_productivity < 5 and total_activities > 0:
        recommendations.append({
            'type': 'productivity',
            'priority': 'high',
            'message': 'Try the Pomodoro technique: 25 min focus + 5 min break',
            'action': 'use_pomodoro',
            'icon': '🍅'
        })
    
    # Exercise suggestion
    recommendations.append({
        'type': 'exercise',
        'priority': 'medium',
        'message': 'A 10-minute walk can boost your productivity by 20%',
        'action': 'exercise',
        'icon': '🚶'
    })
    
    # Calculate streak (simplified - count consecutive days with activities)
    # For demo, we'll calculate last 7 days
    streak = 0
    for i in range(7):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        day_activities = db.query(models.Activity).filter(
            models.Activity.user_id == user_id,
            models.Activity.timestamp >= day_start,
            models.Activity.timestamp < day_end
        ).count()
        
        if day_activities > 0:
            streak += 1
        else:
            break  # Streak broken
    
    # Get weekly summary
    week_ago = today - timedelta(days=7)
    weekly_activities = db.query(models.Activity).filter(
        models.Activity.user_id == user_id,
        models.Activity.timestamp >= week_ago
    ).all()
    
    weekly_avg = sum(a.productivity_score for a in weekly_activities) / len(weekly_activities) if weekly_activities else 0
    
    # Return complete dashboard data
    return {
        'user_id': user_id,
        'user_name': user.name,
        'today': {
            'date': today.strftime('%Y-%m-%d'),
            'score': round(avg_productivity, 1),
            'work_time': total_work_time,
            'activities_count': total_activities
        },
        'weekly': {
            'avg_score': round(weekly_avg, 1),
            'total_activities': len(weekly_activities)
        },
        'predictions': predictions,
        'recommendations': recommendations,
        'streak': streak,
        'timestamp': datetime.now().isoformat()
    }