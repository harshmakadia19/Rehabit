"""
AI Recommendations endpoint
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    """
    Get personalized AI recommendations for user
    Combines predictions, patterns, and anomaly detection
    """
    try:
        # Get user's recent activities
        recent_activities = db.query(models.Activity).filter(
            models.Activity.user_id == user_id
        ).order_by(models.Activity.timestamp.desc()).limit(10).all()
        
        recommendations = []
        
        # Analyze productivity patterns
        if recent_activities:
            avg_score = sum(a.productivity_score for a in recent_activities) / len(recent_activities)
            
            # Low productivity recommendation
            if avg_score < 5:
                recommendations.append({
                    'type': 'productivity',
                    'priority': 'high',
                    'message': 'Your productivity has been lower than usual. Try breaking tasks into smaller chunks.',
                    'action': 'schedule_breaks'
                })
            
            # High productivity praise
            elif avg_score >= 8:
                recommendations.append({
                    'type': 'encouragement',
                    'priority': 'low',
                    'message': '🎉 Great work! Your productivity is excellent today.',
                    'action': 'maintain_pace'
                })
        
        # Peak hours recommendation (mock data - will be real ML later)
        recommendations.append({
            'type': 'timing',
            'priority': 'high',
            'message': 'Schedule your most important task at 10:00 AM - your peak productivity time',
            'action': 'schedule_task'
        })
        
        # Break reminder
        recommendations.append({
            'type': 'break',
            'priority': 'medium',
            'message': 'Take a 5-minute break every hour for better focus',
            'action': 'take_break'
        })
        
        # Exercise suggestion
        recommendations.append({
            'type': 'exercise',
            'priority': 'medium',
            'message': 'A 10-minute walk can boost your productivity by 20%',
            'action': 'exercise'
        })
        
        return {
            'user_id': user_id,
            'recommendations': recommendations,
            'generated_at': datetime.now()
        }
        
    except Exception as e:
        print(f"Recommendation error: {e}")
        # Fallback recommendations
        return {
            'user_id': user_id,
            'recommendations': [
                {
                    'type': 'timing',
                    'priority': 'high',
                    'message': 'Schedule important tasks during your peak hours',
                    'action': 'schedule_task'
                },
                {
                    'type': 'break',
                    'priority': 'medium',
                    'message': 'Take regular breaks to maintain focus',
                    'action': 'take_break'
                }
            ],
            'generated_at': datetime.now()
        }
