"""
ML Predictions endpoints - integrates with Harsh's models
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import sys
import os

# Add ML directory to path so we can import Harsh's models
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../ml'))

router = APIRouter()

@router.get("/{user_id}")
def get_predictions(user_id: int, db: Session = Depends(get_db)):
    """
    Get 24-hour productivity predictions for user
    Uses Harsh's ProductivityPredictor model
    """
    try:
        # TODO: Import Harsh's model when it's ready
        # from models.productivity_predictor import ProductivityPredictor
        
        # For now, return mock predictions
        # Once Harsh's model is ready, we'll integrate it here
        
        # Mock predictions for 24 hours
        predictions = []
        for hour in range(24):
            # Simple pattern: higher productivity during work hours (9-17)
            if 9 <= hour <= 17:
                base_score = 7.5
            else:
                base_score = 5.0
            
            predictions.append({
                'hour': hour,
                'score': round(base_score + (hour % 3) * 0.5, 1),
                'confidence': 0.75
            })
        
        # Identify peak hours (top 3 scores)
        sorted_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)
        peak_hours = [p['hour'] for p in sorted_predictions[:3]]
        
        return {
            'user_id': user_id,
            'hourly_predictions': predictions,
            'peak_hours': peak_hours,
            'confidence': 0.75,
            'note': 'Mock predictions - will integrate Harsh\'s ML model'
        }
        
    except Exception as e:
        print(f"ML model error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")