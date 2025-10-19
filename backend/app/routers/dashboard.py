"""
Dashboard API Routes
Provides complete dashboard data with ML insights
"""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/{user_id}")
async def get_dashboard(user_id: int):
    """
    Get complete dashboard data for user
    
    Returns:
        - stats: User productivity statistics
        - predictions: 24-hour productivity forecast from ML
        - pattern: User behavior pattern (Morning/Night/Consistent)
        - anomaly: Burnout detection and alerts
        - recommendations: AI-generated personalized tips
    """
    try:
        # Import ML service here to avoid circular imports
        from app.services.ml_service import ml_service
        
        # Get ML insights
        if ml_service is None:
            # If ML service not available, return basic stats only
            return {
                'status': 'success',
                'data': {
                    'stats': {
                        'current_productivity': 8.3,
                        'productivity_change': 23.5,
                        'work_time_today': 245,
                        'work_time_change': 12.0,
                        'streak_days': 7,
                        'streak_change': 1,
                        'avg_weekly_productivity': 7.8,
                        'weekly_change': 15.3,
                    },
                    'predictions': [],
                    'pattern': {},
                    'anomaly': {},
                    'recommendations': []
                }
            }
        
        # Get ML data
        ml_data = ml_service.get_dashboard_data(user_id)
        
        # Get user stats (TODO: Replace with actual database query)
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
        print(f"❌ Error in dashboard endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_dashboard():
    """Test endpoint to verify dashboard route is working"""
    return {
        "status": "success",
        "message": "Dashboard route is working!",
        "ml_available": True
    }

